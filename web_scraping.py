"""
download metadata
download videos
download all media files across the web domain
turn this into an app
don't let it replace the files in the folder
"""



import urllib.request
from bs4 import BeautifulSoup
import requests
import os
import tkinter as tk
import tkinter.filedialog

def dl_img(url, file_path, file_name):
	full_path = file_path + file_name + ".jpg"
	urllib.request.urlretrieve(url, full_path)

#This function asks the user to select the folder they want their content to be saved in.
def folder_input():
	folder = tkinter.filedialog.askdirectory()
	print(folder)
	return folder

my_folder = folder_input()
#if not os.path.exists('images'):
#		os.mkdir('images')
# This is to make sure the website doesn't think we're a bot 
opener = urllib.request.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11')]
urllib.request.install_opener(opener)

img_url = input("Enter the URL: ")

webpage_response = requests.get(img_url)
webpage = webpage_response.content

soup = BeautifulSoup(webpage,"html.parser")
count = 1

my_list = [] #append all the img.src here, and find the set to remove duplicates

for img in soup.findAll("img"):
	#temp = img.get("src")
	my_list.append(img.get("src"))

my_list = list(set(my_list))

#Download the images
for img in my_list:
	temp = img
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
			dl_img(image,my_folder+'/',"images" + str(count))
			count += 1
		except Exception as e:
			print(e)
	except Exception as e:
		print(e)