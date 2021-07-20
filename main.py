from bs4 import BeautifulSoup
from tqdm import tqdm_notebook
import re
import os
import requests

url = 'https://rustih.ru/stihi-russkih-poetov-klassikov/'  # website url


def response(url):
    response = requests.get(url)
    return response


def FindAuthorsHrefs(tree):
    data = []

    bsObject = tree.find_all('div', {'class': 'taxonomy-description'})

    tmp = re.findall("<a(.*?)</a>", str(bsObject[0]), re.DOTALL)
    href = re.findall("href=(.*?) title=", str(tmp), re.DOTALL)  # list of hrefs

    author = bsObject[0].text.split('\n')
    author = [x for x in author if x != '']  # list of authors

    data.append(author)
    data.append(href)

    return data


def FixHref(array):
    for i in range(len(array[1])):
        array[1][i] = array[1][i][1:-1]
    return array


def FindAllPoems(href):
    tree = BeautifulSoup(href.content, 'html.parser')
    return href


def HrefsAllPoems(ListOfHrefs):
    HrefsList = []
    for href in ListOfHrefs:
        tree = BeautifulSoup(response(href).content, 'html.parser')
        for href1 in tree.find_all('span', {'style': 'font-size: large;'}):
            # print(href1.a.get('href'))
            HrefsList.append(href1.a.get('href'))
    return HrefsList


def PoemsHrefs(HrefByAuthor):
    AllPoemsHrefs = []

    tree = BeautifulSoup(response(HrefByAuthor).content, 'html.parser')
    bsObject = tree.find_all('a', {'class': 'title'})

    for i in range(len(bsObject)):
        href = re.findall("href=(.*?)>", str(bsObject[i]), re.DOTALL)
        AllPoemsHrefs.append(str(href)[1:-1])

    return AllPoemsHrefs


def CleanHrefs(hrefs):
    output = []
    for i in hrefs:
        output.append(i[2:-2])
    return output


def PoemToTxt(href, path, flag):  # params : link to a poem, path to download in .txt, download flag
    tree = BeautifulSoup(response(href).content, 'html.parser')
    title = tree.find('h1', {'entry-title'}).text
    text = tree.find('div', {'class': 'entry-content poem-text'}).text

    if flag:
        os.chdir(path)
        file = open(title + ".txt", "w+")
        file.write(text)
        file.close()
    return text


tree = BeautifulSoup(response(url).content, 'html.parser')
Data = FindAuthorsHrefs(tree)  # names and hrefs for them in 2-dim array

Data = FixHref(Data)  # preparing hrefs

AllAutorsLinks = HrefsAllPoems(Data[1])  # there we have an array with links to authors

ArrayPoemsHrefs = []

for i in AllAutorsLinks:
    ArrayPoemsHrefs.append(PoemsHrefs(i))

ArrayPoemsHrefs = [x for xs in ArrayPoemsHrefs for x in xs]  # list of all links to poems (count = 22760)
ArrayPoemsHrefs = CleanHrefs(ArrayPoemsHrefs)  # list of all links to poems (count = 22760)

for i in tqdm_notebook(range(0, len(ArrayPoemsHrefs))):
    PoemToTxt(ArrayPoemsHrefs[i], "/Users/kuprone/Desktop/test", True)  # input your folder
