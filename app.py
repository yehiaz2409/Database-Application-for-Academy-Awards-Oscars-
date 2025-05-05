import mysql.connector
from datetime import datetime

# Connect to the MySQL database
def connect_to_db():
    return mysql.connector.connect(
        host="sql.freedb.tech",
        user="freedb_freedb_yehia_db_user",
        password="K7h!hCK4!3Xw?S*",
        database="freedb_oscars_db"
    )

# Function to show nominated movies by year/category
# Function to show nominated movies by category
def show_top_nominated_movies(iteration):
    connection = connect_to_db()  # Connect to the database
    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT nf.movie_name, nf.name, n.cat_name, n.num_of_votes
            FROM nominated_for nf
            JOIN Nomination n on nf.nom_id = n.nom_id
            WHERE nf.iteration = %s
            AND n.num_of_votes > 0
            AND n.cat_name NOT LIKE '%actor%'
            AND n.cat_name NOT LIKE '%actress%'
            AND n.cat_name NOT LIKE '%direct%'
            ORDER BY n.num_of_votes DESC
        """,(iteration,))
        
        rows = cursor.fetchall()
        if rows:
            print("Top Nominated Movies:")
            for row in rows:
                print(f"Category: {row[2]} | Movie Name: {row[0]} | Crew Name: {row[1]} | Number of Votes: {row[3]}")
        else:
            print("No nominated movies found.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()  # Close the cursor
        connection.close()  # Close the connection

# Function to register a user
def register_user(username, email, age, birth_date, gender, country):
    connection = connect_to_db()  # Connect to the database
    cursor = connection.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO User (username, email, age, birth_date, gender, country)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (username, email, age, birth_date, gender, country))
        connection.commit()
        print(f"User {username} has been registered successfully.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()  # Close the cursor
        connection.close()  # Close the connection

# Function to add a nomination for a staff member
def add_nomination(username, nom_id, iteration):
    connection = connect_to_db()  # Connect to the database
    cursor = connection.cursor()

    try:
        cursor.execute("""
            INSERT INTO user_nomination (username, nom_id, iteration)
            VALUES (%s, %s, %s)
        """, (username, nom_id, iteration))
        connection.commit()
        print(f"Nomination {nom_id} for {username} has been added successfully.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()  # Close the cursor
        connection.close()  # Close the connection

def check_username(username):
    connection = connect_to_db()  # Connect to the database
    cursor = connection.cursor()
    
    try:
        cursor.execute("""
            SELECT username
            FROM User
            WHERE username = %s
        """, (username,))
        rows = cursor.fetchall()
        if rows:
            return True
        else:
            return False
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()  # Close the cursor
        connection.close()  # Close the connection

def show_nomination_categories(iteration, username):
    connection = connect_to_db()  # Connect to the database
    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT DISTINCT n2.cat_name 
            FROM nominated_for n1
            Join Nomination n2 on  n1.nom_id = n2.nom_id
            WHERE n1.iteration = %s
        """, (iteration,))
        categories = cursor.fetchall()
        
        # Show the categories to the user
        print(f"\nNomination Categories for Iteration {iteration}:")
        for idx, category in enumerate(categories, 1):
            print(f"{idx}. {category[0]}")

        # Let the user select a category
        category_choice = int(input("\nEnter the category number to see nominees: "))
        selected_category_name = categories[category_choice - 1][0]

        # Call function to show the nominees for the selected category
        show_nominees_for_category(iteration, selected_category_name, username)
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()  # Close the cursor
        connection.close()  # Close the connection

def show_nominees_for_category(iteration, category_name, username):
    connection = connect_to_db()  # Connect to the database
    cursor = connection.cursor()

    try:
        # Get the nominees for the selected category and iteration
        cursor.execute("""
            SELECT nf.nom_id, nf.name, nf.movie_name, n.num_of_votes
            FROM nominated_for nf
            JOIN Nomination n ON nf.nom_id = n.nom_id
            WHERE nf.iteration = %s AND n.cat_name = %s
        """, (iteration, category_name))

        nominees = cursor.fetchall()

        # Show the nominees to the user
        print(f"\nNominees for {category_name} in Iteration {iteration}:")
        for idx, nominee in enumerate(nominees, 1):
            print(f"{idx}. {nominee[1]} for {nominee[2]} (Votes: {nominee[3]})")

        # Let the user select a nominee to vote for
        nominee_choice = int(input("\nEnter the nominee number you want to vote for: "))
        selected_nominee = nominees[nominee_choice - 1]

        # Increment the number of votes for the selected nominee and record the user's nomination
        increment_votes_and_add_nomination(username, selected_nominee[0], iteration)

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()  # Close the cursor
        connection.close()  # Close the connection

def increment_votes_and_add_nomination(username, nom_id, iteration):
    connection = connect_to_db()  # Connect to the database
    cursor = connection.cursor()

    try:
        # Increment the number of votes for the selected nominee
        cursor.execute("""
            UPDATE Nomination 
            SET num_of_votes = num_of_votes + 1 
            WHERE nom_id = %s
        """, (nom_id,))
        
        # Add a new entry in user_nomination table
        cursor.execute("""
            INSERT INTO user_nomination (username, nom_id) 
            VALUES (%s, %s)
        """, (username, nom_id,))
        
        connection.commit()
        print(f"\nNomination for {nom_id} in the category {iteration} has been successfully added.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()  # Close the cursor
        connection.close()  # Close the connection

def show_user_nomination(username):
    connection = connect_to_db()  # Connect to the database
    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT n.cat_name, nf.movie_name, nf.name, n.num_of_votes
            FROM user_nomination un
            JOIN nominated_for nf ON un.nom_id = nf.nom_id
            JOIN Nomination n ON nf.nom_id = n.nom_id
            WHERE un.username = %s
        """, (username,))
        
        rows = cursor.fetchall()
        if rows:
            print("Top Nominated Movies:")
            for row in rows:
                print(f"Category: {row[0]} | Movie: {row[1]} | Crew: {row[2]} | Votes: {row[3]}")
        else:
            print("No nominated movies found.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()  # Close the cursor
        connection.close()  # Close the connection

def show_total_nominations_and_oscars():
    # Get the person's name and date of birth
    name = input("Enter the name of the person: ").strip()
    date_of_birth = input("Enter the date of birth of the person (YYYY-MM-DD): ").strip()

    connection = connect_to_db()  # Connect to the database
    cursor = connection.cursor()

    try:
        # Search for all nominations for the person in the nominated_for table
        cursor.execute("""
            SELECT COUNT(*) AS total_nominations, 
                   SUM(CASE WHEN n.granted = "TRUE" THEN 1 ELSE 0 END) AS total_oscars
            FROM nominated_for nf
            JOIN Nomination n on nf.nom_id = n.nom_id
            WHERE nf.name = %s AND nf.date_of_birth = %s
        """, (name, date_of_birth))

        result = cursor.fetchone()

        # If the person exists in the nominated_for table, display the results
        if result:
            total_nominations = result[0]
            total_oscars = result[1]

            print(f"\n{total_nominations} nominations and {total_oscars} Oscars for {name} (born {date_of_birth}).")
        else:
            print(f"No nominations found for {name} born on {date_of_birth}.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()  # Close the cursor
        connection.close()  # Close the connection

def show_nominated_staff_by_country(country):
    connection = connect_to_db()  # Connect to the database
    cursor = connection.cursor()

    try:
        # SQL Query to fetch staff members born in the given country along with their nominations and oscars
        cursor.execute("""
            SELECT nf.name, nf.date_of_birth, n.cat_name, COUNT(*) AS num_of_nominations, SUM(CASE WHEN n.granted = "TRUE" THEN 1 ELSE 0 END) AS num_of_oscars
            FROM nominated_for nf
            JOIN Crew c ON nf.name = c.name AND nf.date_of_birth = c.date_of_birth
            JOIN Nomination n ON nf.nom_id = n.nom_id
            WHERE c.country = %s
            GROUP BY nf.name, nf.date_of_birth, n.cat_name
            ORDER BY num_of_oscars DESC, num_of_nominations DESC
        """, (country,))

        # Fetch the results
        result = cursor.fetchall()

        # Check if there are no results
        if not result:
            print(f"No data found for staff born in {country}.")
            return

        print(f"\nStaff Members Born in {country} with their Nominations and Oscars:")
        for idx, (name, dob, category, num_of_nominations, num_of_oscars) in enumerate(result, 1):
            print(f"{idx}. {name} (Born: {dob}) - Category: {category} - Nominations: {num_of_nominations} - Oscars: {num_of_oscars}")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()  # Close the cursor
        connection.close()  # Close the connection

def show_top_5_countries_for_best_actor_winners():
    connection = connect_to_db()  # Connect to the database
    cursor = connection.cursor()

    try:
        # SQL Query to find the top 5 countries with the most Best Actor winners
        cursor.execute("""
            SELECT c.country, COUNT(*) AS win_count
            FROM nominated_for nf
            JOIN Crew c ON nf.name = c.name AND nf.date_of_birth = c.date_of_birth
            JOIN Nomination n ON nf.nom_id = n.nom_id
            WHERE n.granted = "TRUE" AND c.country != "None"
            AND n.cat_name LIKE '%Best Actor%' 
            GROUP BY c.country
            ORDER BY win_count DESC
            LIMIT 5
        """)

        # Fetch the results
        result = cursor.fetchall()

        print("\nTop 5 Birth Countries for Best Actor Winners:")
        for idx, (country, win_count) in enumerate(result, 1):
            print(f"{idx}. {country} - {win_count} wins")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()  # Close the cursor
        connection.close()  # Close the connection
    
def get_dream_team():
    connection = connect_to_db()  # Connect to the database
    cursor = connection.cursor()

    try:
        # Get the director who has won the most Oscars
        cursor.execute("""
            SELECT nf.name, COUNT(*) AS oscars_won
            FROM nominated_for nf
            JOIN Nomination n ON nf.nom_id = n.nom_id
            WHERE n.cat_name = 'Best Director' AND n.granted = "TRUE"
            GROUP BY nf.name
            ORDER BY oscars_won DESC
            LIMIT 1
        """)
        director = cursor.fetchone()

        # Get the Best Actor
        cursor.execute("""
            SELECT nf.name, COUNT(*) AS oscars_won
            FROM nominated_for nf
            JOIN Nomination n ON nf.nom_id = n.nom_id
            WHERE n.cat_name LIKE '%Actor in a Leading%' AND n.granted = "TRUE"
            GROUP BY nf.name
            ORDER BY oscars_won DESC
            LIMIT 1
        """)
        actor = cursor.fetchone()

        # Get the Best Actress
        cursor.execute("""
            SELECT nf.name, COUNT(*) AS oscars_won
            FROM nominated_for nf
            JOIN Nomination n ON nf.nom_id = n.nom_id
            WHERE n.cat_name LIKE '%Actress in a Leading%' AND n.granted = "TRUE"
            GROUP BY nf.name
            ORDER BY oscars_won DESC
            LIMIT 1
        """)
        actress = cursor.fetchone()

        # Get the Best Supporting Actor
        cursor.execute("""
            SELECT nf.name, COUNT(*) AS oscars_won
            FROM nominated_for nf
            JOIN Nomination n ON nf.nom_id = n.nom_id
            WHERE n.cat_name LIKE '%Actor in a Supporting%' AND n.granted = "TRUE"
            GROUP BY nf.name
            ORDER BY oscars_won DESC
            LIMIT 1
        """)
        supporting_actor = cursor.fetchone()

        # Get the Best Supporting Actress
        cursor.execute("""
            SELECT nf.name, COUNT(*) AS oscars_won
            FROM nominated_for nf
            JOIN Nomination n ON nf.nom_id = n.nom_id
            WHERE n.cat_name LIKE '%Actress in a Supporting%' AND n.granted = "TRUE"
            GROUP BY nf.name
            ORDER BY oscars_won DESC
            LIMIT 1
        """)
        supporting_actress = cursor.fetchone()

        # Get the Producer
        cursor.execute("""
            SELECT nf.name, COUNT(*) AS oscars_won
            FROM nominated_for nf
            JOIN Nomination n ON nf.nom_id = n.nom_id
            WHERE n.cat_name LIKE '%Picture%' AND n.granted = "TRUE"
            GROUP BY nf.name
            ORDER BY oscars_won DESC
            LIMIT 1
        """)
        producer = cursor.fetchone()

        # Get the singer for the movie score (Best Original Song)
        cursor.execute("""
            SELECT nf.name, COUNT(*) AS oscars_won
            FROM nominated_for nf
            JOIN Nomination n ON nf.nom_id = n.nom_id
            WHERE n.cat_name LIKE '%Song%' AND n.granted = "TRUE"
            GROUP BY nf.name
            ORDER BY oscars_won DESC
            LIMIT 1
        """)
        singer = cursor.fetchone()

        # Check if all the members are still alive by checking their death date in Crew table
        people = [director, actor, actress, supporting_actor, supporting_actress, producer, singer]
        alive_people = []
        
        for person in people:
            if person:
                person_name, _ = person
                cursor.execute("""
                    SELECT death_date 
                    FROM Crew 
                    WHERE name = %s
                """, (person_name,))
                death_date = cursor.fetchone()

                # If death date is NULL, then they are alive
                if not death_date or death_date[0] is None:
                    alive_people.append(person_name)

        print("\nDream Team (Living):")
        print(f"Director: {director[0] if director else 'N/A'}")
        print(f"Best Actor: {actor[0] if actor else 'N/A'}")
        print(f"Best Actress: {actress[0] if actress else 'N/A'}")
        print(f"Best Supporting Actor: {supporting_actor[0] if supporting_actor else 'N/A'}")
        print(f"Best Supporting Actress: {supporting_actress[0] if supporting_actress else 'N/A'}")
        print(f"Producer: {producer[0] if producer else 'N/A'}")
        print(f"Singer for Movie Score: {singer[0] if singer else 'N/A'}")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()  # Close the cursor
        connection.close()  # Close the connection
    
def top_5_production_companies():
    connection = connect_to_db()  # Connect to the database
    cursor = connection.cursor()

    try:
        # Query to find top 5 production companies by the number of Oscars won in "Best Picture"
        cursor.execute("""
            SELECT m.production_company, COUNT(*) AS oscars_won
            FROM nominated_for nf
            JOIN Nomination n ON nf.nom_id = n.nom_id
            join Movie m on nf.movie_name = m.movie_name and nf.release_date = m.release_date
            WHERE n.cat_name LIKE '%Picture%' AND n.granted = "TRUE" AND m.production_company != "Unknown"
            GROUP BY 1
            ORDER BY oscars_won DESC
            LIMIT 5
        """)

        production_companies = cursor.fetchall()

        print("\nTop 5 Production Companies by Oscars Won:")
        for idx, company in enumerate(production_companies, 1):
            print(f"{idx}. {company[0]} - {company[1]} Oscar(s)")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()  # Close the cursor
        connection.close()  # Close the connection

def list_non_english_oscar_winners():
    connection = connect_to_db()  # Connect to the database
    cursor = connection.cursor()

    try:
        # Query to get all non-English speaking movies that won an Oscar
        cursor.execute("""
            SELECT nf.movie_name, YEAR(m.release_date) AS year
            FROM nominated_for nf
            JOIN Movie m ON nf.movie_name = m.movie_name AND nf.release_date = m.release_date
            JOIN Nomination n ON nf.nom_id = n.nom_id
            WHERE n.granted = "TRUE"
            AND (m.language NOT LIKE '%English%' AND m.language IS NOT NULL AND m.language NOT LIKE '%no spoken dialogue%')
            ORDER BY year
        """)

        non_english_movies = cursor.fetchall()

        print("\nNon-English Speaking Movies That Won an Oscar:")
        for movie in non_english_movies:
            print(f"{movie[0]} - {movie[1]}")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()  # Close the cursor
        connection.close()  # Close the connection

# Main function to display a menu and handle user inputs
def main():
    while True:
        print("1. login")
        print("2. Register")
        choice = input("Enter your choice: ")
        login = False
        if choice == "1":
            username = input("Enter username: ")
            if check_username(username):
                print(f"Welcome back, {username}!")
                login = True
            else:
                print("Username not found. Please register first.")
                continue
        
            if login:
                while True:
                    print("Menu:")
                    print("1. Add User Nomination")
                    print("2. My Nominations")
                    print("3. Top Nominated Movies by Users")
                    print("4. Total Nominations and Oscars for a Person")
                    print("5. Top 5 Birth Countries for the Best Actors")
                    print("6. All Nominated Crew for a Given Country")
                    print("7. Dream Team")
                    print("8. Top 5 Production Companies")
                    print("9. All Non-English movies that Ever Won an Oscar")
                    print("10. Exit")    
                    
                    choice = input("Enter your choice: ")

                    if choice == "1":
                        iteration = int(input("Enter iteration: "))
                        show_nomination_categories(iteration, username)

                    elif choice == "2":
                        show_user_nomination(username)
                    
                    elif choice == "3":
                        iteration = int(input("\nEnter the iteration: "))
                        show_top_nominated_movies(iteration)

                    elif choice == "4":
                        show_total_nominations_and_oscars()

                    elif choice == "5":
                        show_top_5_countries_for_best_actor_winners()

                    elif choice == "6":
                        country = input("Enter the country: ")
                        show_nominated_staff_by_country(country)

                    elif choice == "7":
                        get_dream_team()

                    elif choice == "8":
                        top_5_production_companies()

                    elif choice == "9":
                        list_non_english_oscar_winners()

                    elif choice == "10":
                        print("Exiting the program.")
                        break

                    else:
                        print("Invalid choice. Please try again.")
        elif choice == "2":
                username = input("Enter username: ")
                email = input("Enter email: ")
                # age = int(input("Enter age: "))
                birth_date = input("Enter birth date (YYYY-MM-DD): ")
                birth_date_obj = datetime.strptime(birth_date, "%Y-%m-%d")
                current_date = datetime.today()
                # Calculate the difference in years
                age = current_date.year - birth_date_obj.year
                
                # If the current month and day is before the birth date in the current year, subtract 1 from the age
                if (current_date.month, current_date.day) < (birth_date_obj.month, birth_date_obj.day):
                    age -= 1
                gender = input("Enter gender (Male/Female/Other): ")
                country = input("Enter country: ")
                register_user(username, email, age, birth_date, gender, country)

if __name__ == "__main__":
    main()