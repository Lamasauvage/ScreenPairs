from django.shortcuts import render
import requests
import os
from django.core.cache import cache


api_key = os.environ.get('TMDB_API_KEY', '')


def get_movie_details(movie_id):
    # Check if movie details are in cache
    cache_key = f"movie_{movie_id}_details"
    cached_movie = cache.get(cache_key)
    if cached_movie:
        return cached_movie

    # If not in cache, make the API call
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&append_to_response=credits"
    response = requests.get(url)
    data = response.json()
    directors = [crew['name'] for crew in data['credits']['crew'] if crew['job'] == 'Director']
    movie_details = {
        'poster_path': data.get('poster_path'),
        'release_year': data['release_date'].split('-')[0] if data.get('release_date') else 'N/A',
        'directors': directors
    }

    # Cache the movie details before returning
    cache.set(cache_key, movie_details, timeout=60*60*24)  # Cache for 24 hours
    return movie_details


def get_movies_by_actor(actor_id):
    """Get list of movies for a given actor ID including poster, release year, director."""
    url = f"https://api.themoviedb.org/3/person/{actor_id}/movie_credits?api_key={api_key}"
    response = requests.get(url)
    data = response.json()
    movies = []
    if data.get('cast'):
        for movie in data['cast']:
            movie_details = get_movie_details(movie['id'])
            movies.append({
                'title': movie['title'],
                'poster_path': movie_details['poster_path'],
                'release_year': movie_details['release_year'],
                'directors': movie_details['directors'],
                'character': movie.get('character'),
                'id': movie['id']
            })
    return movies


def get_actor_info(actor_name):
    """Get the TMDB ID and profile image path for an actor by name."""
    url = f"https://api.themoviedb.org/3/search/person?api_key={api_key}&query={actor_name}"
    response = requests.get(url)
    data = response.json()
    if data['results']:
        actor_info = {
            'id': data['results'][0]['id'],
            'image_path': data['results'][0].get('profile_path')
        }
        return actor_info
    return None


def find_common_movies(actor1_name, actor2_name):
    actor1_info = get_actor_info(actor1_name)
    actor2_info = get_actor_info(actor2_name)
    common_movies = []

    if actor1_info and actor2_info:
        actor1_id = actor1_info['id']
        actor2_id = actor2_info['id']

        actor1_movies = {movie['id']: movie for movie in get_movies_by_actor(actor1_id)}
        actor2_movies = {movie['id']: movie for movie in get_movies_by_actor(actor2_id)}

        common_movie_ids = set(actor1_movies.keys()) & set(actor2_movies.keys())

        for movie_id in common_movie_ids:
            movie_info = actor1_movies[movie_id].copy()  # Make a copy to avoid mutating the original
    # Properly access character names with default value 'N/A' if not found
            movie_info['characters'] = {
                actor1_name: actor1_movies[movie_id].get('character', 'N/A'),
                actor2_name: actor2_movies[movie_id].get('character', 'N/A'),
            }
            common_movies.append(movie_info)

    return common_movies


def search_movies(request):
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
            common_movies = find_common_movies(context['actor1_name'], context['actor2_name'])
            context['common_movies'] = common_movies

    return render(request, 'search_movies.html', context)



