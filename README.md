# ! IN PROGRESS / NOT FINAL VERSION !

# ScreenPairs Movie Search

## Introduction
ScreenPairs is a dynamic web application that allows users to search for common movies between two actors. It utilizes The Movie Database (TMDB) API to fetch and display detailed information about actors and their shared filmography.

## Features
- **Actor Autocomplete:** As users begin to type an actor's name into the search fields, the app suggests possible matches, including profile pictures, leveraging jQuery UI's Autocomplete widget for a seamless user experience.
- **Common Movie Display:** Once two actors are selected, the app displays a list of movies that both actors have appeared in, along with additional details like movie posters, release years, and director names.
- **Performance Optimization:** To enhance performance, movie details are cached to reduce API call overhead, ensuring faster subsequent searches for the same actors or movies.

## Technologies Used
- **Frontend:** HTML, CSS, JavaScript, jQuery, jQuery UI
- **Backend:** Django (Python), Django Templates
- **API:** The Movie Database (TMDB) API
- **Caching:** Django's built-in caching framework

## Setup and Installation
1. Clone the repository to your local machine.
2. Set up a virtual environment and install project dependencies.
3. Obtain an API key from TMDB and set it as an environment variable `TMDB_API_KEY`.
4. No database setup is required as of the current version of the application.
5. Start the Django development server.

## Database
This application currently does not use a database for storing any data. All information is retrieved in real-time from The Movie Database (TMDB) API and temporarily cached for performance optimization.

## Usage
Navigate to the /search/ page, enter the names of two actors in the search fields, and click the "Search" button. Browse through the shared movies list and explore detailed information about each film.

## Future Enhancements
- Build a decent UI (in progress)
- Refining actor search results to prioritize more relevant suggestions.
- Adding more interactive elements such as modals to display detailed movie descriptions.
