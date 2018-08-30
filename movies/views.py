from django.shortcuts import render, redirect
from django.contrib import messages
from airtable import Airtable
import os


AT = Airtable(os.environ.get('AIRTABLE_MOVIESTABLE_BASE_ID'),
              'Movies',
              api_key=os.environ.get('AIRTABLE_API_KEY'))

# Create your views here.
def home_page(request):
    user_query = str(request.GET.get('query', ''))
    search_result = AT.get_all(formula="FIND('" + user_query.lower() + "', LOWER({Name}))")
    stuff_for_frontend = {'search_result': search_result}
    return render(request, 'movies/movies_stuff.html', stuff_for_frontend)


def create(request):
    if request.method == 'POST':
        data = {
            'Name': request.POST.get('name'),
            'Pictures': [{'url': request.POST.get('url') or 'https://vignette.wikia.nocookie.net/janethevirgin/images/4/42/Image-not-available_1.jpg/revision/latest?cb=20150721102313'}],
            'Rating': int(request.POST.get('rating')),
            'Notes': request.POST.get('notes')
        }

        try:
            response = AT.insert(data)
            messages.success(request, 'Added New Game: {}'.format(response['fields'].get('Name')))
        except Exception as e:
            messages.warning(request, 'Uh-oh, Something went wrong: {}'.format(e))
    return redirect('/')


def edit(request, movie_id):
    if request.method == 'POST':
        data = {
            'Name': request.POST.get('name'),
            'Pictures': [{'url': request.POST.get('url') or 'https://vignette.wikia.nocookie.net/janethevirgin/images/4/42/Image-not-available_1.jpg/revision/latest?cb=20150721102313'}],
            'Rating': int(request.POST.get('rating')),
            'Notes': request.POST.get('notes')
        }
        try:
            response = AT.update(movie_id, data)
            messages.success(request, 'Successfully Edited Game Info For: {}'.format(response['fields'].get('Name')))
        except Exception as e:
            messages.warning(request, 'Uh-oh, Something went wrong: {}'.format(e))
    return redirect('/')

def delete(request, movie_id):
    try:
        movie_name = AT.get(movie_id)['fields'].get('Name')
        AT.delete(movie_id)
        messages.warning(request, 'Game Deleted: {}'.format(movie_name))
    except Exception as e:
        messages.warning(request, 'Uh-oh, Something went wrong: {}'.format(e))
    return redirect('/')
