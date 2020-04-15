#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  erewan.py
#  
#  Copyright 2020 Jarecki <https://github.com/JaroslawHryszko/ErewanDownloader>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

import requests, json, re, uuid, datetime, urllib
from bs4 import BeautifulSoup

numer_poczatkowy = 1
sciezka = ""
nazwa_audycji = ""
domena_www = ""
domena_mp3 = ""
adres_request = ""
referer = ""
tab_id = ""
box_instance_id = ""
category_id = ""
tag_index_id = ""

for page_number in range(numer_poczatkowy,0,-1):
	print('Strona: %s') % (numer)
	formularz = '{tabId : %s, boxInstanceId : %s, sectionId : 9, categoryId : %s, categoryType : 0, subjectIds : \'\', tagIndexId : %s, queryString : \'stid=9&ctid=%s\', name : \'\', pageNumber : %s, pagerMode : 0, openArticlesInParentTemplate : \'False\', idSectionFromUrl : 9, maxDocumentAge : 6000, showCategoryForArticle : \'False\' }' % (tab_id, box_instance_id, category_id, tag_index_id, category_id, page_number)
	response = requests.post(adres_request,
		data = formularz,
		headers={
			"Accept": "application/json, text/javascript, */*; q=0.01",
			"Accept-Language": "",
			"Connection": "keep-alive",
			"Content-Type": "application/json; charset=utf-8",
			"DNT": "1",
			"Origin": domena_www,
			"Referer": referer,
			"User-Agent": "",
			"X-Requested-With": "XMLHttpRequest"
		},
		cookies={
			"ASP.NET_SessionId": "",
			"ViewedDocuments": "",
			"__AntiXsrfToken": "",
			"cookies-accepted": "true"
		},
		)
	json_raw = response.json()
	json_dump = json.dumps(json_raw)
	json_load = json.loads(json_dump)
	json2 = json_load['d']
	strona_www = json2['Content']
	soup = BeautifulSoup(strona_www, 'lxml')
	for link in soup.find_all('a', href=True):
		link2 = domena_www + link['href']
		komunikat = "Nowa podstrona: " + link2
		print(komunikat)
		podstrona = requests.get(link2)
		podstrona_decode = podstrona.content
		y = re.findall(r'[.][p][l][/].*[.][m][p][3]', podstrona_decode)
		if y:
			url = domena_mp3 + y[0]
			identifajer = uuid.uuid4().hex
			nazwa_pliku = nazwa_audycji + "-" + identifajer + ".mp3"
			podstrona_soup = BeautifulSoup(podstrona.content, 'lxml')
			data_styl_1 = podstrona_soup.find_all("span", attrs={'class': 'date'})
			data_styl_2 = podstrona_soup.find_all("div", attrs={'class': 'content'})
			if data_styl_1:
				data3 = "blad_daty-" + identifajer
				data2 = data_styl_1[0].string.strip()
				if re.findall(r'[.]', data2):
					data3 = datetime.datetime.strptime(data2, '%d.%m.%Y').strftime('%Y.%m.%d')
				elif re.findall(r'[/]', data2):
					data3 = datetime.datetime.strptime(data2, '%Y/%m/%d').strftime('%Y.%m.%d')
				nazwa_pliku = data3 + "-" + nazwa_audycji + ".mp3"
			elif len(data_styl_2) == 1:
				data3 = "blad_daty-" + identifajer
				for paragraf in data_styl_2[0].find_all('p'):
					if len(paragraf) == 2:
						if paragraf.strong.text == "Data emisji: " or paragraf.strong.text == "Data emisji:":
							data2 = paragraf.contents[1].strip()
							if re.findall(r'[.]', data2):
								data3 = datetime.datetime.strptime(data2, '%d.%m.%Y').strftime('%Y.%m.%d')
							elif re.findall(r'[/]', data2):
								data3 = datetime.datetime.strptime(data2, '%Y/%m/%d').strftime('%Y.%m.%d')
				nazwa_pliku = data3 + "-" + nazwa_audycji + ".mp3"
			pelna_nazwa_pliku = sciezka + nazwa_pliku
			komunikat = "Pobieranie: " + url
			print(komunikat)
			komunikat = "...i zapisywanie jako: " + pelna_nazwa_pliku
			print(komunikat)
			urllib.urlretrieve(url, pelna_nazwa_pliku)
			komunikat = "Skończono zapis."
			print(komunikat)
print("Koniec.")
