import urllib.request
from bs4 import BeautifulSoup
import requests

def dl_img(url, file_path, file_name):
	full_path = file_path + file_name + ".jpg"
	urllib.request.urlretrieve(url, full_path)


img_url = "http://www.ayodelecasel.com/headshots"#input("Enter the URL: ")

webpage_response = requests.get(img_url)
webpage = webpage_response.content
#soup = BeautifulSoup(webpage, "html.parser")
soup = BeautifulSoup(webpage,"html.parser")
count = 1
for img in soup.findAll("img"):
	temp = img.get("src")
	print(temp)
	if temp[:1] == "/":
		if img_url[-1] == "/":
			image = img_url[:-1] + temp
		else:
			image = img_url + temp
	else:
		image = temp
	#if "jpg" not in image:
		#continue
	#else:
	dl_img(image,"images/","image" + str(count))
	count += 1