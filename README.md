
# Oscars Nomination System

This project is a command-line Python application designed to manage and display Oscar nominations and related information. The system allows users to register, vote for nominations, view top nominated movies, and query various statistics about nominated actors, directors, movies, and more. The data has been scraped from Wikipedia using this [repo](https://github.com/yehiaz2409/Web-Scraping-Oscars-Awards-and-Nominees-from-Wikipedia)

## Features

- **Register User**: Users can create an account with their personal information.
- **Add User Nomination**: Users can nominate movies and staff for a given iteration and category.
- **Show My Nominations**: Users can view their nominations.
- **Show Top Nominated Movies**: View the top nominated movies for a specific iteration.
- **Various Reports**: Generate reports based on nominations and movies, such as top countries for actors, top production companies, etc.

## Database Structure

The database has several tables with relationships defined between them. Some of the key tables include:

- **User**: Stores user information.
- **Nomination**: Stores information about Oscar nominations.
- **Crew**: Stores information about movie crew (actors, directors, producers).
- **Movie**: Stores information about movies.
- **User Nomination**: Stores the nominations made by users.

## File Structure

- **app.py**: Main Python application with the logic for user interactions and database queries.

## How to Use

1. **Register a User**: Enter your username, email, birth date, gender, and country.
2. **Add Nomination**: Choose an iteration and a category, then nominate a movie or crew member.
3. **View Top Nominated Movies**: See a list of top movies nominated in a specific iteration.
4. **Generate Reports**: You can generate various reports like top birth countries for actors or top production companies.

