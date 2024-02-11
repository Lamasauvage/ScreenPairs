from django.http import JsonResponse
import requests
import os


def auto_completion(request):
    api_key = os.environ.get('TMDB_API_KEY', '')
    query = request.GET.get('query', '')

    if query:
        url = f"https://api.themoviedb.org/3/search/person?api_key={api_key}&query={query}&include_adult=false"
        response = requests.get(url)
        data = response.json()

        # Limit to top 5 results for brevity
        top_results = data.get('results', [])[:5]

        # Extract names and profile paths, ensuring only actors are included if possible
        results = [{
            'name': actor['name'],
            'profile_path': actor.get('profile_path'),
            'popularity': actor.get('popularity', 0),
            'id': actor['id']
        } for actor in top_results]

        # Sort by popularity if not already sorted
        results.sort(key=lambda x: x['popularity'], reverse=True)

        return JsonResponse({'results': results}, safe=False)
    return JsonResponse({'results': []})
