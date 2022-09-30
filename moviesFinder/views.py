from pickle import GET
from types import TracebackType
from django.shortcuts import render
from django.http import HttpResponse
import requests
from bs4 import BeautifulSoup

# Create your views here.

def index(request):
    return render(request, "index.html")

def finder(request):
    movieName = request.POST["movieName"]
    context = {
        'movieName': movieName.upper(),
        'isPlaying': isPlaying(movieName),
        'usersReviews': getUsersReviews(movieName),
        'criticsReviews': getCriticsReviews(movieName),
        'criticsSize': len(getCriticsReviews(movieName)),
        'usersSize': len(getUsersReviews(movieName)),
        'posterSource': getPosterSource(movieName)
    }
    return render(request, 'finder.html', context)



#AMC and RottenTomatoes methods
def getMoviesList():
    response = requests.get('https://amctheatres.com/movies').text
    soup = BeautifulSoup(response, 'lxml')
    moviesList = []

    for moviesInfo in soup.find_all('div', class_='PosterContent'):
        movieName = moviesInfo.h3.text
        moviesList.append(movieName)

    return moviesList

def isPlaying(movieName):
    for movie in getMoviesList():
        if movie == movieName:
            return True
    return False

def getCriticsReviews(movieName):

    #In case the movie name is more than one word, need to replace spaces with underscores
    split = movieName.split()
    newName = ""
    for x in split:
        newName += "_" + x
    newName = newName[1:len(newName)]
    
    url = "https://rottentomatoes.com/m/" + newName.lower() + "/reviews"
    criticsReviews = []

    raw = requests.get(url).text
    soup = BeautifulSoup(raw, 'lxml')
    for reviewArea in soup.find_all('div', class_='the_review'):
        criticReview = reviewArea.text
        criticReview = criticReview[22:len(criticReview)]
        criticsReviews.append(criticReview)
    
    if len(criticsReviews) == 0:
        print("No critic reviews for " + movieName + ". ")
    return criticsReviews

def getUsersReviews(movieName):
     #In case the movie name is more than one word, need to replace spaces with underscores
    split = movieName.split()
    newName = ""
    for x in split:
        newName += "_" + x
    newName = newName[1:len(newName)]

    url = "https://rottentomatoes.com/m/" + newName.lower() + "/reviews?type=user"
    usersReviews = []

    raw = requests.get(url).text
    soup = BeautifulSoup(raw, 'lxml')
    for reviewArea in soup.find_all('p', class_='audience-reviews__review--mobile js-review-text clamp clamp-4 js-clamp'):
        userReview = reviewArea.text
        #userReview = userReview[22: len(userReview)]
        usersReviews.append(userReview)
    
    if len(usersReviews) == 0:
        print("No audience reviews for " + movieName + ". ")
    return usersReviews

def getPosterSource(movieName):
    raw = requests.get("https://amctheatres.com/movies").text
    soup = BeautifulSoup(raw, 'lxml')
    
    for poster in soup.find_all('img'):
        if poster.attrs.get('alt') == "movie poster for " + movieName:
            return (poster.attrs.get('src'))