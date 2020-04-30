"""
download metadata
select which folder
download videos
download all media files across the web domain
turn this into an app
"""



import urllib.request
from bs4 import BeautifulSoup
import requests
import os

def dl_img(url, file_path, file_name):
	full_path = file_path + file_name + ".jpg"
	urllib.request.urlretrieve(url, full_path)

if not os.path.exists('images'):
		os.mkdir('images')
opener = urllib.request.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11')]
urllib.request.install_opener(opener)

img_url = input("Enter the URL: ")

webpage_response = requests.get(img_url)
webpage = webpage_response.content

soup = BeautifulSoup(webpage,"html.parser")
count = 1
for img in soup.findAll("img"):
	temp = img.get("src")
	try:
		if temp[:1] == "/":
			if img_url[-1] == "/":
				image = img_url[:-1] + temp
				print("1")
				print(image)
			else:
				image = img_url + temp
				print("2")
				print(image)
		else:
			image = temp
			print("3")
			print(image)
		if image[-3:] == "svg":
			continue

		try:
			dl_img(image,"images/","image" + str(count))
			count += 1
		except Exception as e:
			print(e)
	except Exception as e:
		print(e)