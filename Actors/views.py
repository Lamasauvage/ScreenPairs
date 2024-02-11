from django.shortcuts import render
import requests
import os
from django.core.cache import cache

api_key = os.environ.get('TMDB_API_KEY', '')


def get_actor_info(actor_name):
    """Get the TMDB ID and profile image path for an actor by name."""
    url = f"https://api.themoviedb.org/3/search/person?api_key={api_key}&query={actor_name}"
    response = requests.get(url).json()
    if response['results']:
        return {
            'id': response['results'][0]['id'],
            'image_path': response['results'][0].get('profile_path')
        }
    return None


def get_movies_by_actor(actor_id):
    """Get list of movies for a given actor ID including character played."""
    url = f"https://api.themoviedb.org/3/person/{actor_id}/movie_credits?api_key={api_key}"
    response = requests.get(url).json()
    return [{
        'id': movie['id'],
        'character': movie.get('character')
    } for movie in response.get('cast', [])]


def fetch_common_movie_details(movie_id, actor1_character, actor2_character):
    """Fetch details for a movie given its ID and characters played by two actors."""
    cache_key = f"movie_{movie_id}_details"
    cached_movie = cache.get(cache_key)
    if cached_movie:
        return cached_movie

    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&append_to_response=credits"
    response = requests.get(url).json()
    directors = [crew['name'] for crew in response['credits']['crew'] if crew['job'] == 'Director']

    movie_details = {
        'id': movie_id,
        'title': response.get('title'),
        'poster_path': response.get('poster_path'),
        'release_year': response.get('release_date', '').split('-')[0],
        'directors': directors,
        'characters': {
            'actor1': actor1_character,
            'actor2': actor2_character
        }
    }

    cache.set(cache_key, movie_details, timeout=60*60*24)  # Cache for 24 hours
    return movie_details


def find_common_movies(actor1_name, actor2_name):
    actor1_info = get_actor_info(actor1_name)
    actor2_info = get_actor_info(actor2_name)

    if not actor1_info or not actor2_info:
        return []

    # Fetch movies lists
    actor1_movies = get_movies_by_actor(actor1_info['id'])
    actor2_movies = get_movies_by_actor(actor2_info['id'])

    # Create sets of movie IDs for each actor
    actor1_movie_ids = {movie['id'] for movie in actor1_movies}
    actor2_movie_ids = {movie['id'] for movie in actor2_movies}

    # Find common movie IDs
    common_movie_ids = actor1_movie_ids.intersection(actor2_movie_ids)

    # Fetch details for common movies
    common_movies = []
    for common_id in common_movie_ids:
        # Extract character names from original lists
        actor1_character = next((movie['character'] for movie in actor1_movies if movie['id'] == common_id), 'N/A')
        actor2_character = next((movie['character'] for movie in actor2_movies if movie['id'] == common_id), 'N/A')

        # Fetch and append movie details
        movie_details = fetch_common_movie_details(common_id, actor1_character, actor2_character)
        movie_details['characters'] = {actor1_name: actor1_character, actor2_name: actor2_character}
        common_movies.append(movie_details)

    return common_movies


def search_movies(request):
    """View to render movies common to two searched actors."""
    context = {
        'actor1_name': '',
        'actor2_name': '',
        'common_movies': [],
        'search_attempted': False,
        'actor1_image': None,
        'actor2_image': None,
    }

    if 'actor1' in request.GET and 'actor2' in request.GET:
        context['search_attempted'] = True
        context['actor1_name'] = request.GET['actor1']
        context['actor2_name'] = request.GET['actor2']

        if context['actor1_name'] and context['actor2_name']:
            actor1_info = get_actor_info(context['actor1_name'])
            actor2_info = get_actor_info(context['actor2_name'])
            context['actor1_image'] = f"https://image.tmdb.org/t/p/w500{actor1_info['image_path']}" if actor1_info and actor1_info['image_path'] else None
            context['actor2_image'] = f"https://image.tmdb.org/t/p/w500{actor2_info['image_path']}" if actor2_info and actor2_info['image_path'] else None
            context['common_movies'] = find_common_movies(context['actor1_name'], context['actor2_name'])

    return render(request, 'search_movies.html', context)
