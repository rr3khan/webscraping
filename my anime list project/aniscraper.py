import requests
from bs4 import BeautifulSoup
import re
import csv
import numpy as np

fields = ['Name', 'Score', 'Episodes','Air Date', 'Source', 'Studio', 'id' , 'Genre']
urllist = []
filename = 'ani.csv'

with open(filename, 'w') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(fields)


url2 = 'https://myanimelist.net/topanime.php?limit='


def scrape_name(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    links = soup.findAll('a', attrs={'href': re.compile("^https://myanimelist.net/anime/")})
        # print (link.get('href'))
    for nam in links:
        # print(nam.text)
        if '/video' not in (nam.get('href')):
            urllist.append(nam.get('href'))

def scrape(url, filename):
    
    ani = []
    genrelist = []
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    try:
        name = soup.find('span',{ 'class' : 'title-english'})  ## // this works
        ani.append(name.text)
    except:
        name = soup.find('span',{ 'itemprop' : 'name'})  ## // this works
        ani.append(name.text)
    else:
        pass

    try:
        genre = soup.find_all('span',{ 'itemprop' : 'genre'})  ## // this works
        for gen in genre:
            genrelist.append(gen.text)
    except:
        pass
    try:
        score = soup.find('span',{ 'itemprop' : 'ratingValue'}) # gets the score
        ani.append(score.text)
        # print(ani)
    except:
        pass 
    try:
        etc = soup.find_all('div', {'class': 'spaceit' })

        span_element = soup.find_all('span', {'class': 'dark_text'})
        for element in span_element:
            element.replace_with('')

        for item in range(0,2):
            ani.append(etc[item].text.strip())

        ani.append(etc[3].text.strip())
    except:
        pass
    try:
        studio = soup.findAll('a', attrs={'href': re.compile("^/anime/producer")})
        ani.append(studio[-1].text)
    except:
        pass
    try:
        id = soup.find('input', {'id': 'myinfo_anime_id' })
        ani.append(id['value'])
    except:
        pass
    print(ani)
    with open(filename, 'a', encoding="utf-8") as csvfile:
         csvwriter = csv.writer(csvfile)
         csvwriter.writerow(ani + [genrelist])


count = 0
while count < 1050:
    url3 = url2 + str(count)
    scrape_name(url3)
    count += 50

#remove duplicates in the urllist

urllist = list(set(urllist))

for item in urllist:
    scrape(item, filename)





