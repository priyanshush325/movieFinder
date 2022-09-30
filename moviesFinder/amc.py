import requests
from bs4 import BeautifulSoup

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


