import tkinter as tk
import tkinter.filedialog
import tkinter.messagebox
import urllib.request
from bs4 import BeautifulSoup
import requests
import os
from os import listdir
from os.path import isfile, join

HEIGHT = 250
WIDTH = 600

file_name_characters_check = r'\/:*?"<>|'
########################### Functions ##############################
def folder_input():
	print(entry_folder.get())
	entry_folder.config(state = 'normal')
	entry_folder.delete(0, tk.END)
	entry_folder.insert(0, tkinter.filedialog.askdirectory())
	entry_folder.config(state = 'disabled')
	print(entry_folder.get())

def dl_img(url, file_path, file_name):
	full_path = file_path + file_name + ".jpg"
	urllib.request.urlretrieve(url, full_path)

# This is to make sure the website doesn't think we're a bot 
def i_am_not_a_bot_deal_with_it():
	opener = urllib.request.build_opener()
	opener.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11')]
	urllib.request.install_opener(opener)

i_am_not_a_bot_deal_with_it() #https://www.youtube.com/watch?v=fsF7enQY8uI

def validation():
	for character in img_name.get():
		if character in file_name_characters_check:
			return False, ("Image names cannot have the following characters: \n"+ r'\/:*?"<>|')
	try:
		webpage_response = requests.get(web_url.get())
		return True, None
	except:
		return False, "Please input a valid URL, which includes HTTP"

def save_images():
	if not validation()[0]:
		tkinter.messagebox.showerror(title="Oops!", message = validation()[1])
		return
	print('hello ' + web_url.get() + ' and ' + img_name.get() + ' and ' + folder_path.get())
	temp_web_url = web_url.get()
	temp_img_name = img_name.get()
	temp_folder_path = folder_path.get()

	webpage_response = requests.get(temp_web_url)
	webpage = webpage_response.content

	soup = BeautifulSoup(webpage,"html.parser")
	all_atr = soup.findAll("img")
	my_list = [] # append all the img.src here, and find the set to remove duplicates

	for img in all_atr:
		for value in img.attrs.values():
			print(value)
			if type(value) == str:
				if value[-3:] == "svg":
					continue
				else:
					if len(value) >= 4:
						if value[0:4] == "http":
							if "jpg" in value or "png" in value:
								try:
									try:
										my_list.append(value[0:value.index("jpg")+3])
									except:
										my_list.append(value[0:value.index("png")+3])
								except:
									print()
							else:
								my_list.append(value)
						elif value[0] == "/":
							if "jpg" in value or "png" in value:
								try:
									try:
										my_list.append(temp_web_url+value[0:value.index("jpg")+3])
									except:
										my_list.append(temp_web_url+value[0:value.index("png")+3])
								except:
									print()
							else:
								my_list.append(temp_web_url+value)
			elif type(value) == list:
				for thing in value:
					if thing[-3:] == "svg":
						continue
					else:
						if len(thing) >= 4:
							if thing[0:4] == "http":
								if "jpg" in thing or "png" in thing:
									try:
										try:
											my_list.append(thing[0:thing.index("jpg")+3])
										except:
											my_list.append(thing[0:thing.index("png")+3])
									except:
										print()
								else:
									my_list.append(thing)
							elif thing[0] == "/":
								if "jpg" in thing or "png" in thing:
									try:
										try:
											my_list.append(temp_web_url+thing[0:thing.index("jpg")+3])
										except:
											my_list.append(temp_web_url+thing[0:thing.index("png")+3])
									except:
										print()
								else:
									my_list.append(temp_web_url+thing)

	my_list = list(set(my_list))

	# Make a list of numbers sorted lexicographically
	my_numbers = []
	start_number = 1
	# Check to see if file name is already in the folder 
	onlyfiles = [f for f in listdir(temp_folder_path) if isfile(join(temp_folder_path, f))]
	# Concatentate them all into a string if there's items in the file
	if len(onlyfiles) > 0:
		big_string = ""
		for one_file in onlyfiles:
			big_string += one_file
		if temp_img_name in big_string:
			start_index = big_string.rfind(temp_img_name) + len(temp_img_name) + 1
			end_index = big_string.rfind('.')
			start_number = int(big_string[start_index:end_index]) + 1


	for i in range(start_number, start_number + len(my_list)+1):
		my_numbers.append('0'*(len(str(len(my_list)))-len(str(i)))+str(i))


	#Download the images

	count = 0
	for img in my_list:
		try:
			dl_img(img,temp_folder_path+'/',temp_img_name + '_' + my_numbers[count])
			count += 1
		except Exception as e:
			print(e)


# Everything in the GUI goes between .Tk() and .mainloop()
root = tk.Tk()
root.title("Image Scraper")
# Lock resize of window
root.resizable(width = False, height = False)

# Make the window size
canvas = tk.Canvas(root, height = HEIGHT, width = WIDTH, bg="#3CCBD9")
canvas.pack()

label_welcome = tk.Label(canvas, text = "Welcome to Image Scraper!", font = 20, bg = "#3CCBD9")
label_welcome.place(relx = 0.5, rely = 0.1, anchor = "center") 

######################################FOLDER##################################
frame_folder = tk.Frame(canvas, bg = '#40AADC')
frame_folder.place(relx = 0.5, rely = 0.2, relwidth = 0.75, relheight = 0.1, anchor = 'n')

folder_path = tk.StringVar()
entry_folder = tk.Entry(frame_folder, textvariable = folder_path, bg = '#FDFEFE', font = 14)
entry_folder.place(relwidth = 0.8, relheight = 1)

button_folder = tk.Button(frame_folder, text = "Browse", command = lambda: folder_input())
button_folder.place(relx = 0.7, relwidth = 0.3, relheight = 1)
#######################################WEB URL###############################
frame_temp_web_url = tk.Frame(canvas, bg = "#3CCBD9")
frame_temp_web_url.place(relx = 0.5, rely = 0.35, relwidth = 0.75, relheight = 0.2, anchor = 'n')

label_temp_web_url = tk.Label(frame_temp_web_url, text = "Enter Web URL:", font = 18, bg = "#3CCBD9")
label_temp_web_url.place(anchor = 'nw')

web_url = tk.StringVar()
entry_temp_web_url = tk.Entry(frame_temp_web_url, textvariable = web_url, font = 14)
entry_temp_web_url.place(rely = .5, relwidth = 1, relheight = .5)
###################################IMAGE NAME################################
frame_temp_img_name = tk.Frame(canvas, bg = "#3CCBD9")
frame_temp_img_name.place(relx = 0.5, rely = 0.60, relwidth = 0.75, relheight = 0.2, anchor = 'n')

label_temp_img_name = tk.Label(frame_temp_img_name, text = "Enter Image Name:", font = 18, bg = "#3CCBD9")
label_temp_img_name.place(anchor = 'nw')

img_name = tk.StringVar()
entry_temp_img_name = tk.Entry(frame_temp_img_name, textvariable = img_name, font = 14)
entry_temp_img_name.place(rely = 0.5, relwidth = .5, relheight = 0.5)

button_save = tk.Button(frame_temp_img_name, text = "Save Image(s)", command = save_images)
button_save.place(relx = 0.75, rely = 0.5, relwidth = 0.20, relheight = 0.5)
#############################################################################
root.mainloop()