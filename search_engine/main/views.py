import re
import sys
from imp import reload
from urllib.request import urlopen

import requests
from bs4 import BeautifulSoup

from django.http import HttpResponse
from django.shortcuts import redirect, render


def analysis_list(item):
    dic = {}
    dic['title'] = item.find('h2').get_text()
    dic['link'] = item.find('a')['href']
    dic['abstract'] = item.find('p').get_text()
    dic['safety'] = ('https' in dic['link'])
    return dic


def bing_search_by_keywords(keyword):
    url_base = 'https://cn.bing.com/search'
    req = url_base + '?q=' + keyword

    html = urlopen(req).read().decode('utf-8')
    soup = BeautifulSoup(html, features='lxml')

    content_list = []
    result = soup.find_all('li', {'class': 'b_algo'})
    for item in result:
        t = analysis_list(item)
        content_list.append(t)
    return content_list


def page(request):
    return render(request, 'page.html')


def home(request):
    if request.method == 'GET':
        return render(request, 'home.html')
    else:
        content = {}
        content['keywords'] = request.POST['search-content']
        temp = bing_search_by_keywords(request.POST['search-content'])
        content['reslist'] = temp
        return render(request, 'page.html', content)
