from django.shortcuts import render
import requests
from django.conf import settings
from rest_framework.response import Response
from django.shortcuts import render, redirect
import json
import imdb
from django.http import HttpResponse, Http404
from pytube import YouTube
from django.contrib import messages
# Create your views here.

down_progress = 0



    

def query_search(request):
    context = {} 
    if request.method == 'POST':

        url = settings.RAPID_API_BASE_URL_NAME
        name = request.POST['search']
        print(request.POST['search'])
        url = url + f"?s={ request.POST['search'] }&page=1&r=json"
        print(url)

        headers = {
            'x-rapidapi-key': settings.RAPID_API_IMDB_KEY,
            'x-rapidapi-host': settings.RAPID_API_HOST_NAME_NAME,
            'useQueryString': 'true',
            'Content-Type': 'application/json'
        }

        payload = json.dumps({
            "upload_date": "",
            "read": "True"
        })

        try:
            response = requests.request(
                "GET", url, headers=headers, data=payload)
            context = {
                'movie_list': response.json()['Search']
            }

        except Exception as e:
            return render(request, '404.html')

    return render(request, 'search.html', context)


def watchTrailer(request):
    # context = {}

    # print(type(imdb), imdb)
    # url = settings.RAPID_API_BASE_URL_ID
    # querystring = {"type": "get-movie-details", "imdb": imdb}
    # headers = {
    #     'x-rapidapi-key': settings.RAPID_API_IMDB_KEY,
    #     'x-rapidapi-host': settings.RAPID_API_HOST_NAME_ID,
    # }

    # try:
    #     response = requests.request("GET", url, headers=headers, params=querystring)

    #     print(response.json())

    #     # movieName ="inception"
    #     # params = {
    #     #     'part': "snippet",
    #     #     'q': movieName + " official trailer",
    #     #     'key': settings.YOUTUBE_API_KEY
    #     # }
    #     # result = requests.get(settings.YOUTUBE_API_BASE_URL, params=params)
    #     # data = result.json()
    #     # print(data)
    #     # print(type(result.json()),result.json()['items'][0]['id']['videoId'])

    #     trailerUrl = settings.YOUTUBE_BASE_URL + response.json()['youtube_trailer_key']

    #     print(trailerUrl)
    #     context = {
    #         'trailerUrl': trailerUrl,
    #         'movieDetails': response.json()
    #     }
    # except Exception as e:
    #     return render(request, '404.html')

    
    imdb = request.GET.get('imdb', -1)
    title = request.GET.get('title', -1)
    context = {}
    print(type(title), title,type(imdb),imdb)

    trailerUrl = ""
    try:             
        params = {
            'part': "snippet",
            'q': title + " official trailer",
            'key': settings.YOUTUBE_API_KEY
        }
        result = requests.get(settings.YOUTUBE_API_BASE_URL, params=params)
        data = result.json()['items'][0]['id']['videoId']
        print(data)
        trailerUrl = settings.YOUTUBE_BASE_URL + result.json()['items'][0]['id']['videoId']

    except Exception as e:
        print("Trailer does not exist")

    try:
        url = settings.RAPID_API_BASE_URL_ID
        querystring = {"type": "get-movie-details", "imdb": imdb}

        headers = {
            'x-rapidapi-key': settings.RAPID_API_IMDB_KEY,
            'x-rapidapi-host': settings.RAPID_API_HOST_NAME_ID,
        }
        response = requests.request("GET", url, headers=headers, params=querystring)
        # print(response.json())

    except Exception as e:
        print("Info not found")
        return render(request, 'pagenotfound.html') 

    context = {
        'trailerUrl' : trailerUrl,
        'movieDetails' : response.json(),
        'movieTitle' : title,
        'ytID': result.json()['items'][0]['id']['videoId']
    }

    return render(request, 'watchTrailer.html', context)

def download(request):

    def download_progress(video, size, progess):
        # print("===========================================================")
        # print(progess, video.filesize)
        # down_progress = ((video.filesize - progess)/video.filesize)*100
        # print(down_progress)
        # messages.info(request, down_progress)
        pass


    ytID = request.GET.get('ytID', -1)
    down_progress = 0

    obj = YouTube("https://www.youtube.com/watch?v=" + ytID, on_progress_callback=download_progress)

    video = obj.streams.get_by_resolution(resolution="720p")
    print(down_progress)
    video.download("C:/Users/DELL/Downloads/")
    
    return redirect('/')
