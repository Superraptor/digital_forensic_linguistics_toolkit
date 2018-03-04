#!/usr/bin/env python

#
#	Charles Kronk
#	3 March 2018
#	
#	
#

#
#	IMPORTANT LINKS:
#

#
#	PLEASE NOTE:
#	This script was designed and tested on a 64-bit Windows system.
#	It further assumes that Python 3.4 has been installed correctly.
#

#
#	Guesslang supports 20 programming languages:
#	- C
#	- C#
#	- C++
#	- CSS
#	- Erlang
#	- Go
#	- HTML
#	- Java
#	- JavaScript
#	- Markdown
#	- Objective-C
#	- Perl
#	- Python
#	- Ruby
#	- Rust
#	- SQL
#	- Scala
#	- Shell
#	- Swift
#

#
#	Langdetect supports 55 natural languages:
#	- af (Afrikaans)
#	- ar (Arabic)
#	- bg (Bulgarian)
#	- bn (Bengali)
#	- ca (Catalan, Valencian)
#	- cs (Czech)
#	- cy (Welsh)
#	- da (Danish)
#	- de (German)
#	- el (Modern Greek)
#	- en (English)
#	- es (Spanish, Castillian)
#	- et (Estonian)
#	- fa (Persian)
#	- fi (Finnish)
#	- fr (French)
#	- gu (Gujarati)
#	- he (Modern Hebrew)
#	- hi (Hindi)
#	- hr (Croatian)
#	- hu (Hungarian)
#	- id (Indonesian)
#	- it (Italian)
#	- ja (Japanese)
#	- kn (Kannada)
#	- ko (Korean)
#	- lt (Lithuanian)
#	- lv (Latvian)
#	- mk (Macedonian)
#	- ml (Malayalam)
#	- mr (Marathi)
#	- ne (Nepali)
#	- nl (Dutch, Flemish)
#	- no (Norwegian)
#	- pa (Panjabi, Punjabi)
#	- pl (Polish)
#	- pt (Portuguese)
#	- ro (Romanian, Moldavian, Moldovan)
#	- ru (Russian)
#	- sk (Slovak)
#	- sl (Slovenian)
#	- so (Somali)
#	- sq (Albanian)
#	- sv (Swedish)
#	- sw (Swahili)
#	- ta (Tamil)
#	- te (Telugu)
#	- th (Thai)
#	- tl (Tagalog)
#	- tr (Turkish)
#	- uk (Ukrainian)
#	- ur (Urdu)
#	- vi (Vietnamese)
#	- zh-cn (Simplified Chinese)
#	- zh-tw (Traditional Chinese)
#

#
#	DEPENDENCIES:
#	- Python 3.4
#	- Python 3.5
#

#
#	IMPORTS
#	- PIL
#	- cognitive_face
#	- collections
#	- io
#	- json
#	- langdetect
#	- numpy
#	- os
#	- pathlib
#	- random
#	- requests
#	- subprocess
#	- time
#	- tkinter
#	- tqdm
#	- traceback
#	- urllib
#

from PIL import ImageTk
from collections import Counter
from io import BytesIO
from langdetect import detect, detect_langs
from os.path import expanduser
from random import randint
from tkinter import *
from tqdm import tqdm
import PIL.Image
import cognitive_face as CF
import http.client
import json
import numpy as np
import os
import pathlib
import requests
import subprocess
import time
import traceback
import urllib

azure_subscription_key = ""

github_client_id = ""
github_client_secret = ""

face_api_uses = 0
face_api_allowed_use_per_minute = 20

github_api_uses = 0
github_api_allowed_use_per_minute = 83

#   MAIN
def main():
	get_all_natural_language_probabilities()
	
	#file_dict = {}
	#with open("./prog_lang/lang_dict.txt", "r", encoding="utf8") as f:
	#	file_dict = eval(f.read())
		
	#keyword_dict_for_user = {}
	#for username, sub_dict in tqdm(file_dict.items()):
	#	keyword_dict_for_user[username], non_keywords = keyword_distribution(sub_dict["program_files"])
		
	#	with open("./keywords/distributions/keywords.txt", "w", encoding="utf8") as f:
	#		f.write(str(keyword_dict_for_user))

	#find_users(250, save=True)
	#use_face_api(save=True)
	
#	Get single user profile image.
def get_user_image(username, user_image_url)
	img_url = user_image_url
	user = {}
	user["avatar_url"] = img_url
	user["username"] = username
	use_face_api(user, save=True)
	
#	Get all natural language probabilities
#	from dictionary.
def get_all_natural_language_probabilities():
	file_dict = {}
	with open("./prog_lang/lang_dict.txt", "r", encoding="utf8") as f:
		file_dict = eval(f.read())
	
	lang_dict_for_user = {}
	for username, sub_dict in tqdm(file_dict.items()):
		lang_dict_for_user[username] = classify_comments(sub_dict["program_files"])
		
		with open("./nat_lang/nat_lang.txt", "w", encoding="utf8") as f:
			f.write(str(lang_dict_for_user))
	
#	Get all program statistics from
#	language dictionary.
def get_all_program_stats():

	file_dict = {}
	with open("./prog_lang/lang_dict.txt", "r", encoding="utf8") as f:
		file_dict = eval(f.read())
	
	for username, sub_dict in tqdm(file_dict.items()):
		stats_dict, overall_dict = median_program_length(sub_dict["program_files"])
		
		file_dict[username]["file_stats"] = stats_dict
		file_dict[username]["user_stats"] = overall_dict
		
		with open("./metrics/median.txt", "w", encoding="utf8") as f:
			f.write(str(file_dict))
	
#	Get all programming language information
#	from all users/repos specified.
def get_all_programming_languages(repo_dict):
	
	# Load known extensions dictionary.
	known_extensions = {}
	for ext_file in os.listdir("./extensions/"):
		with open("./extensions/"+ext_file) as f:
			proc_file = ext_file.rsplit(".")
			lang_name = proc_file[0]
			extensions = f.readlines()
			for ext in extensions:
				if ext.lower().strip() in known_extensions:
					known_extensions[ext.lower().strip()].append(lang_name)
				else:
					known_extensions[ext.lower().strip()] = [lang_name]
	
	lang_dict = {}
	for username, repo_sub_dict in tqdm(repo_dict.items()):
		
		major_langs, new_lang_dict, file_is_program = classify_user_code(repo_sub_dict, username=username, save=False, known_extensions=known_extensions)
		
		lang_dict[username] = {
			"major_languages": major_langs,
			"language_dictionary": new_lang_dict,
			"program_files": file_is_program
		}
		
		with open("./prog_lang/lang_dict.txt", "w", encoding="utf8") as f:
			f.write(str(lang_dict))
	
#	Create complete repo dictionary
#	from incomplete repo dictionary.
def complete_repo_dict(repo_dict):

	repo_dict = {}
	with open("./repos/repo_dict.txt", "r", encoding="utf8") as f:
		repo_dict = eval(f.read())
	
	new_repo_dict = {}
	for username, repo_array in repo_dict.items():
		dirs = os.listdir("T:/repos/"+str(username))
	
		all_user_repos = []
		for dir in dirs:
			all_user_repos.append(dir)
	
		new_repo_dict[username] = {}
		for repo_name in all_user_repos:
			if repo_name in repo_array:
				new_repo_dict[username][repo_name] = repo_array[repo_name]
			else:
				new_repo_dict[username][repo_name] = None
	
	with open("./repos/new_repo_dict.txt", "w", encoding="utf8") as f:
		f.write(str(new_repo_dict))
		
	return new_repo_dict

#	Find random users.
#	Note: For requests using Basic Authentication or OAuth,
#	you can only make up to 5,000 requests per hour. For
#	unauthenticated requests, the rate limit allows for up
#	to 60 requests per hour.
#
#	For more information, see here:
#	https://developer.github.com/v3/
#
#	For information specifically about the users API, see here:
#	https://developer.github.com/v3/users/
#
#	Params:
#	- n: number of users to find.
def find_users(n, client_id=github_client_id, client_secret=github_client_secret, save=False):
	print("NOT FUNCTIONAL.")
	
	# As of 4 December 2016, there were 24,377,273 GitHub users.
	# Therefore, to pull "randomly" from this set, we simply
	# generate numbers between 1 and 24377273.
	#
	# This helps us to only pick users who have had accounts for
	# at least 1 year.
	total_github_users = 24377273
	
	user_array = []
	
	filename = "./users/user_identifiers_" + str(n) + ".txt"
	
	github_api_uses = 0
	
	if os.path.isfile(filename):
	
		with open(filename, "r", encoding="utf8") as f:
			for line in f.readlines():
				line_array = line.split("\t")
				username = line_array[0].strip()
				repos_url = line_array[1].strip()
				location = line_array[2].strip()
				avatar_url = line_array[3].strip()
				public_repos = line_array[4].strip()
				name = line_array[5].strip()
				
				temp_user = {
					"username": username,
					"repos_url": repos_url,
					"location": location,
					"avatar_url": avatar_url,
					"public_repos": public_repos,
					"name": name,
				}
						
				# Check if any faces are in avatar URL.
				faces = use_face_api(temp_user, save=True)
				
				if faces:
					for face in faces:
						
						print("NOT FUNCTIONAL")
						
				user_array.append(temp_user)
	
	else:
		
		pbar = tqdm(total = n)
	
		old_time = time.time()
	
		while len(user_array) < n:
			if (time.time() >= old_time + 60) or (github_api_uses > 70):
				if github_api_uses > 70:
					time.sleep(60)
					github_api_uses = 0
					old_time = time.time()
				else: 
					github_api_uses = 0
					old_time = time.time()
		
			rand_num = randint(1, total_github_users)
			
			base = "https://api.github.com/users"
			ext = "?since=" + str(rand_num) + "&client_id=" + client_id + "&client_secret=" + client_secret
			
			r = requests.get(base+ext, headers={})
			github_api_uses += 1
				
			if not r.ok:
				r.raise_for_status()
			else:
				user = r.json()[0]
		
				username = user["login"]
				repos_url = user["repos_url"]
				
				base = "https://api.github.com/users"
				ext = "/" + str(username) + "?&client_id=" + client_id + "&client_secret=" + client_secret
				
				r = requests.get(base+ext)
				github_api_uses += 1
				
				if not r.ok:
					r.raise_for_status()
				else:
					
					user = r.json()
					
					avatar_url = user["avatar_url"]
					location = user["location"]
					public_repos = user["public_repos"]
					name = user["name"]
					
					if public_repos > 0 and public_repos < 10 and location is not None and username is not None and repos_url is not None and avatar_url is not None and name is not None and public_repos is not None:
					
						temp_user = {
							"username": username,
							"repos_url": repos_url,
							"location": location.encode('ascii','ignore').decode(),
							"avatar_url": avatar_url,
							"public_repos": public_repos,
							"name": name.encode('ascii','ignore').decode(),
						}
						
						# Check if any faces are in avatar URL.
						faces = use_face_api(temp_user, save=True)
						
						if faces:
							for face in faces:
								
								print("NOT FUNCTIONAL")
								
						user_array.append(temp_user)
						pbar.update(1)
								
						if save:
							with open(filename, "w", encoding="utf8") as f:
								for user in user_array:
									f.write(user["username"]+"\t"+user["repos_url"]+"\t"+user["location"]+"\t"+user["avatar_url"]+"\t"+str(user["public_repos"])+"\t"+user["name"]+"\n")
					
		pbar.close()
	
#	Find user features via Microsoft Azure Face API.
#	Note: This allows up to 20 transactions per minute
#	and 30,000 transactions per month for free, but
#	surpassing these requirements requires selection
#	of a pricing plan.
#
#	For example, at 20 per minute, this script will
#	take about 50 minutes to run 1,000 face detections.
#
#	Pricing plans available here:
#	https://azure.microsoft.com/en-us/pricing/details/cognitive-services/face-api/
#
#	For more information on code setup, see here:
#	https://docs.microsoft.com/en-us/azure/cognitive-services/face/tutorials/faceapiinpythontutorial
#
#	Params:
#	- user: user object.
#	- key: Azure subscription key.
def use_face_api(user=None, key=azure_subscription_key, open_image=False, save=False):
	#print("NOT FUNCTIONAL.")
	
	#CF.Key.set(key)

	BASE_URL = "https://eastus.api.cognitive.microsoft.com/face/v1.0"
	#CF.BaseUrl.set(BASE_URL)
	
	if user:
		
		# Check if file exists...
		filename = "./images/" + user["username"] + ".jpg"
		
		if os.path.isfile(filename):
		
			print("Already exists.")
		
		else:
		
			img_url = user["avatar_url"]
			img_req = requests.get(img_url)
			
			if open_image:
				root = Tk()
				canvas = Canvas(width=500, height=500, bg="white")
				canvas.pack()
				img = PIL.Image.open(BytesIO(img_req.content))
				photo = ImageTk.PhotoImage(img)
				canvas.create_image(250,250,image=photo)
				root.mainloop()
			else:
				img = PIL.Image.open(BytesIO(img_req.content))
				
			if save:
				with open(filename, "wb") as f:
					f.write(img_req.content)
					
			saved_img = open(expanduser(filename), "rb")
		
		# If the API is being overused, force the user to wait.
		#if face_api_uses >= face_api_allowed_use_per_minute - 2:
		#	sleep(60)
		
		#faces = CF.face.detect(img_url)
		
		#face_api_uses += 1
		
			# If problems, use this instead?
			# https://gist.github.com/devStepsize/f815abf224953a72253cb73fb44e933a
		
		#return faces
		
	else:
	
		user_array = []
	
		for file in os.listdir("./users/"):
		
			with open("./users/"+file, "r", encoding="utf8") as f:
				for line in f.readlines():
					line_array = line.split("\t")
					username = line_array[0].strip()
					repos_url = line_array[1].strip()
					location = line_array[2].strip()
					avatar_url = line_array[3].strip()
					public_repos = line_array[4].strip()
					name = line_array[5].strip()
					
					if os.path.isfile("./proc_images/"+username+".jpg"):
					
						temp_user = {
							"username": username,
							"repos_url": repos_url,
							"location": location,
							"avatar_url": avatar_url,
							"public_repos": public_repos,
							"name": name,
						}
								
						user_array.append(temp_user)
	
		face_api_uses = 0
		old_time = time.time()
		face_dict = {}
		
		if os.path.isfile("./faces/faces.txt"):
			with open("./faces/faces.txt", "r") as f:
				face_dict = eval(f.read())
	
		for user in tqdm(user_array):
		
			if (time.time() >= old_time + 60) or (face_api_uses > 18):
				if face_api_uses > 18:
					time.sleep(60)
					face_api_uses = 0
					old_time = time.time()
				else:
					face_api_uses = 0
					old_time = time.time()
			
			# Check if file exists...
			filename = "./images/" + user["username"] + ".jpg"
			
			if not os.path.isfile(filename):
			
				img_url = user["avatar_url"]
				img_req = requests.get(img_url)
				
				if open_image:
					root = Tk()
					canvas = Canvas(width=500, height=500, bg="white")
					canvas.pack()
					img = PIL.Image.open(BytesIO(img_req.content))
					photo = ImageTk.PhotoImage(img)
					canvas.create_image(250,250,image=photo)
					root.mainloop()
				else:
					img = PIL.Image.open(BytesIO(img_req.content))
					
				if save:
					with open(filename, "wb") as f:
						f.write(img_req.content)
						
				saved_img = open(expanduser(filename), "rb")
				
			headers = {
				"Content-Type": "application/octet-stream",
				"Ocp-Apim-Subscription-Key": key
			}
			
			params = urllib.parse.urlencode({
				"returnFaceId": "true",
				"returnFaceLandmarks": "true",
				"returnFaceAttributes": "age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise"
			})
			
			if os.stat(filename).st_size >= 1000:
			
				file_img = open(expanduser(filename), "rb")
				
				#body = file_img.read()
				url = BASE_URL+"/detect?%s" % params
				print(url)
				resp = requests.post(url, data=file_img, headers=headers)
				file_img.close()
				
				face_api_uses += 1
				
				if resp.status_code != 200:
					print("Request to Azure returned an error %s, the response is:\n%s" % (resp.status_code, resp.text))
					exit()
					time.sleep(10)
					
				else:
					return_stuff = resp.json()
					face_dict[user["username"]] = return_stuff
					
					if save:
						with open("./faces/faces.txt", "w", encoding="utf8") as f:
							f.write(str(face_dict))
							
					time.sleep(10)

#	Download repositories based on user name.
#
#	Params:
#	- user: user object.	
def download_repos(user=None, client_id=github_client_id, client_secret=github_client_secret, save=False):
	print("NOT FUNCTIONAL.")
	
	repo_dict = {}
	
	if user:
	
		base = "https://api.github.com/users"
		ext = "/" + user["username"] + "/repos" + "?client_id=" + client_id + "&client_secret=" + client_secret
		
		r = requests.get(base+ext)
			
		if not r.ok:
			r.raise_for_status()
		else:
			repo_array = r.json()
			
			repo_dict[user["username"]] = {}
			
			for repo in repo_array:
				options = ["git", "clone", repo["clone_url"], "./repos/" + repo["full_name"]]
				print(subprocess.check_call(options))
				
				repository_name = repo["name"]
				primary_programming_language = repo["language"]
				
				repo_dict[user["username"]][repository_name] = primary_programming_language
				
	else:
	
		user_array = []
	
		for file in os.listdir("./users"):
		
			with open("./users/"+file, "r", encoding="utf8") as f:
				for line in f.readlines():
					line_array = line.split("\t")
					username = line_array[0].strip()
					repos_url = line_array[1].strip()
					location = line_array[2].strip()
					avatar_url = line_array[3].strip()
					public_repos = line_array[4].strip()
					name = line_array[5].strip()
					
					if os.path.isfile("./proc_images/"+username+".jpg"):
					
						temp_user = {
							"username": username,
							"repos_url": repos_url,
							"location": location,
							"avatar_url": avatar_url,
							"public_repos": public_repos,
							"name": name,
						}
								
						user_array.append(temp_user)
						
		old_time = time.time()
		github_api_uses = 0
						
		for user in user_array:
			if time.time() >= old_time + 60:
				if github_api_uses > 70:
					time.sleep(60)
					github_api_uses = 0
					old_time = time.time()
				else: 
					github_api_uses = 0
					old_time = time.time()
		
			base = "https://api.github.com/users"
			ext = "/" + user["username"] + "/repos" + "?client_id=" + client_id + "&client_secret=" + client_secret
			
			r = requests.get(base+ext)
				
			if not r.ok:
				r.raise_for_status()
			else:
				repo_array = r.json()
				
				repo_dict[user["username"]] = {}
				
				if not os.path.exists("T:/repos/"+user["username"]):
					os.makedirs("T:/repos/"+user["username"])
				
				for repo in repo_array:
					if not os.path.exists("T:/repos/"+repo["full_name"]):
						try:
							options = ["git", "clone", repo["clone_url"], "T:/repos/" + repo["full_name"]]
							print(subprocess.check_call(options))
							
							repository_name = repo["name"]
							primary_programming_language = repo["language"]
							
							repo_dict[user["username"]][repository_name] = primary_programming_language
						
						except Exception as exc:
							print(traceback.format_exc())
							print(exc)
	
	if save:
		with open("./repos/repo_dict.txt", "w", encoding="utf8") as f:
			f.write(str(repo_dict))
	
	return repo_dict

#	Select only program files which are not empty
#	from repos.
#
#	Params:
#	- repo_dict: dictionary of repositories and
#	  their primary languages.	
def program_files(repo_dict, save=False):
	print("NOT FUNCTIONAL.")
	
#	Classify user based on programming languages.
#
#	Params:
#	- repo_dict: dictionary of repositories and
#	  their primary languages.	
def classify_user_code(repo_dict, username=False, save=False, known_extensions=None):

	if known_extensions is None:
		# Load known extensions dictionary.
		known_extensions = {}
		for ext_file in os.listdir("./extensions/"):
			with open("./extensions/"+ext_file) as f:
				proc_file = ext_file.rsplit(".")
				lang_name = proc_file[0]
				extensions = f.readlines()
				for ext in extensions:
					if ext.lower().strip() in known_extensions:
						known_extensions[ext.lower().strip()].append(lang_name)
					else:
						known_extensions[ext.lower().strip()] = [lang_name]
	
	major_langs = []
	lang_dict = {}
	file_is_program = {}
	
	if username:
		
		for repo, major_lang in repo_dict.items():
			if major_lang is not None:
				major_langs.append(major_lang)
			for path, subdirs, files in os.walk("T:/repos/" + username + "/" + repo):
				for name in files:
					file_path = pathlib.PurePath(path, name)
					language = classify_code(file_path, known_extensions=known_extensions) 
					if language:
						file_is_program[str(file_path)] = language
						if language in lang_dict:
							lang_dict[language] += 1
						else:
							lang_dict[language] = 1
		
	else:
	
		for repo, major_lang in repo_dict.items():
			if major_lang is not None:
				major_langs.append(major_lang)
			for path, subdirs, files in os.walk("T:/repos/" + repo):
				for name in files:
					file_path = pathlib.PurePath(path, name)
					language = classify_code(file_path, known_extensions=known_extensions) 
					if language:
						file_is_program[str(file_path)] = language
						if language in lang_dict:
							lang_dict[language] += 1
						else:
							lang_dict[language] = 1
	
	return major_langs, lang_dict, file_is_program
	
#	Classify code based on programming language.
#
#	Params:
#	- file: file name, complete with path.	
def classify_code(file, known_extensions=None):
	file = str(file)
	programming_language = None
	
	# Load and check extensions from files.
	extension_dict = {}
	
	if known_extensions is None:
		# Load known extensions dictionary.
		known_extensions = {}
		for ext_file in os.listdir("./extensions/"):
			with open("./extensions/"+ext_file) as f:
				proc_file = ext_file.rsplit(".")
				lang_name = proc_file[0]
				extensions = f.readlines()
				for ext in extensions:
					if ext.lower().strip() in known_extensions:
						known_extensions[ext.lower().strip()].append(lang_name)
					else:
						known_extensions[ext.lower().strip()] = [lang_name]
						
	if "." in file:
		poss_ext = file.rsplit(".")[1].lower()
		if poss_ext in known_extensions.keys():
			if len(known_extensions[poss_ext]) == 1:
				programming_language = known_extensions[poss_ext][0]
	
	# Will need guesslang:
	# https://github.com/yoeo/guesslang
	# However, requires at least Python3.5
	# and TensorFlow, so will have to subprocess
	# the thing.
	
	return programming_language

#	Classify user based on tabs or spaces.
#
#	Params:
#	- user: user object.	
def spaces_or_tabs(user):
	print("NOT FUNCTIONAL.")
	
	# Repurpose code here?
	# https://medium.com/@hoffa/400-000-github-repositories-1-billion-files-14-terabytes-of-code-spaces-or-tabs-7cfe0b5dd7fd
	#
	# Specifically,
	#
	# SELECT ext, tabs, spaces, countext, LOG((spaces+1)/(tabs+1)) lratio
	# FROM (
	#  SELECT REGEXP_EXTRACT(sample_path, r'\.([^\.]*)$') ext, 
	#		 SUM(best='tab') tabs, SUM(best='space') spaces, 
	#		 COUNT(*) countext
	#  FROM (
	#	SELECT sample_path, sample_repo_name, IF(SUM(line=' ')>SUM(line='\t'), 'space', 'tab') WITHIN RECORD best,
	#		   COUNT(line) WITHIN RECORD c
	#	FROM (
	#	  SELECT LEFT(SPLIT(content, '\n'), 1) line, sample_path, sample_repo_name 
	#	  FROM [fh-bigquery:github_extracts.contents_top_repos_top_langs]
	#	  HAVING REGEXP_MATCH(line, r'[ \t]')
	#	)
	#	HAVING c>10 # at least 10 lines that start with space or tab
	#  )
	#  GROUP BY ext
	# )
	
#	Find natural language of program comments.
#
#	Currently only supports C, C++, C#, Java,
#	JavaScript, Perl, Python, Ruby, SQL, and
#	Visual Basic.
#
#	Params:
#	- user_program_files: user files which are known to
#	  be programs.
def classify_comments(user_program_files, regex=False):
	print("NOT FUNCTIONAL.")
	
	lang_dict = {}
	
	# use regular expressions in comments folder
	
	# Then use langdetect
	# https://pypi.python.org/pypi/langdetect?
	
	if not regex:
	
		keywords = []
		for file, language in user_program_files.items():
			keywords = []
		
			if language.lower() == "c":
				with open("./keywords/c_90.0_1990.txt", "r") as f:
					keywords = [x.strip() for x in f.readlines()]
				try:
					with open(file, "r", encoding="utf8") as f:
						file_str = " ".join(f.readlines())
						file_words = file_str.split()
						no_keywords_file_list = [word for word in file_words if word.lower() not in keywords]
						no_keywords_file_str = ' '.join(no_keywords_file_list)
						if no_keywords_file_str and not no_keywords_file_str.isspace():
							try:
								detect = detect_langs(no_keywords_file_str)
								detect_dict = {}
								for x in detect:
									detect_dict[x.lang] = x.prob
								lang_dict[file] = detect_dict
							except:
								pass
				except UnicodeDecodeError as e:
					with open(file, "r", encoding="latin-1") as f:
						file_str = " ".join(f.readlines())
						file_words = file_str.split()
						no_keywords_file_list = [word for word in file_words if word.lower() not in keywords]
						no_keywords_file_str = ' '.join(no_keywords_file_list)
						if no_keywords_file_str and not no_keywords_file_str.isspace():
							try:
								detect = detect_langs(no_keywords_file_str)
								detect_dict = {}
								for x in detect:
									detect_dict[x.lang] = x.prob
								lang_dict[file] = detect_dict
							except:
								pass
					
			elif language.lower() in ["c++", "cplusplus"]:
				with open("./keywords/cplusplus_17.0_2017.txt", "r") as f:
					keywords = [x.strip() for x in f.readlines()]
				try:
					with open(file, "r", encoding="utf8") as f:
						file_str = " ".join(f.readlines())
						file_words = file_str.split()
						no_keywords_file_list = [word for word in file_words if word.lower() not in keywords]
						no_keywords_file_str = ' '.join(no_keywords_file_list)
						if no_keywords_file_str and not no_keywords_file_str.isspace():
							try:
								detect = detect_langs(no_keywords_file_str)
								detect_dict = {}
								for x in detect:
									detect_dict[x.lang] = x.prob
								lang_dict[file] = detect_dict
							except:
								pass
				except UnicodeDecodeError as e:
					with open(file, "r", encoding="latin-1") as f:
						file_str = " ".join(f.readlines())
						file_words = file_str.split()
						no_keywords_file_list = [word for word in file_words if word.lower() not in keywords]
						no_keywords_file_str = ' '.join(no_keywords_file_list)
						if no_keywords_file_str and not no_keywords_file_str.isspace():
							try:
								detect = detect_langs(no_keywords_file_str)
								detect_dict = {}
								for x in detect:
									detect_dict[x.lang] = x.prob
								lang_dict[file] = detect_dict
							except:
								pass
					
			elif language.lower() in ["c#", "csharp"]:
				with open("./keywords/csharp_7.0_2017.txt", "r") as f:
					keywords = [x.strip() for x in f.readlines()]
				try:
					with open(file, "r", encoding="utf8") as f:
						file_str = " ".join(f.readlines())
						file_words = file_str.split()
						no_keywords_file_list = [word for word in file_words if word.lower() not in keywords]
						no_keywords_file_str = ' '.join(no_keywords_file_list)
						if no_keywords_file_str and not no_keywords_file_str.isspace():
							try:
								detect = detect_langs(no_keywords_file_str)
								detect_dict = {}
								for x in detect:
									detect_dict[x.lang] = x.prob
								lang_dict[file] = detect_dict
							except:
								pass
				except UnicodeDecodeError as e:
					with open(file, "r", encoding="latin-1") as f:
						file_str = " ".join(f.readlines())
						file_words = file_str.split()
						no_keywords_file_list = [word for word in file_words if word.lower() not in keywords]
						no_keywords_file_str = ' '.join(no_keywords_file_list)
						if no_keywords_file_str and not no_keywords_file_str.isspace():
							try:
								detect = detect_langs(no_keywords_file_str)
								detect_dict = {}
								for x in detect:
									detect_dict[x.lang] = x.prob
								lang_dict[file] = detect_dict
							except:
								pass
					
			elif language.lower() in ["delphiobjectpascal", "delphi/object pascal", "delphi", "object pascal"]:
				with open("./keywords/delphiobjectpascal_6.0_1990.txt", "r") as f:
					keywords = [x.strip() for x in f.readlines()]
				try:
					with open(file, "r", encoding="utf8") as f:
						file_str = " ".join(f.readlines())
						file_words = file_str.split()
						no_keywords_file_list = [word for word in file_words if word.lower() not in keywords]
						no_keywords_file_str = ' '.join(no_keywords_file_list)
						if no_keywords_file_str and not no_keywords_file_str.isspace():
							try:
								detect = detect_langs(no_keywords_file_str)
								detect_dict = {}
								for x in detect:
									detect_dict[x.lang] = x.prob
								lang_dict[file] = detect_dict
							except:
								pass
				except UnicodeDecodeError as e:
					with open(file, "r", encoding="latin-1") as f:
						file_str = " ".join(f.readlines())
						file_words = file_str.split()
						no_keywords_file_list = [word for word in file_words if word.lower() not in keywords]
						no_keywords_file_str = ' '.join(no_keywords_file_list)
						if no_keywords_file_str and not no_keywords_file_str.isspace():
							try:
								detect = detect_langs(no_keywords_file_str)
								detect_dict = {}
								for x in detect:
									detect_dict[x.lang] = x.prob
								lang_dict[file] = detect_dict
							except:
								pass
					
			elif language.lower() in ["go"]:
				with open("./keywords/go_1.9.4_2017.txt", "r") as f:
					keywords = [x.strip() for x in f.readlines()]
				try:
					with open(file, "r", encoding="utf8") as f:
						file_str = " ".join(f.readlines())
						file_words = file_str.split()
						no_keywords_file_list = [word for word in file_words if word.lower() not in keywords]
						no_keywords_file_str = ' '.join(no_keywords_file_list)
						if no_keywords_file_str and not no_keywords_file_str.isspace():
							try:
								detect = detect_langs(no_keywords_file_str)
								detect_dict = {}
								for x in detect:
									detect_dict[x.lang] = x.prob
								lang_dict[file] = detect_dict
							except:
								pass 
				except UnicodeDecodeError as e:
					with open(file, "r", encoding="latin-1") as f:
						file_str = " ".join(f.readlines())
						file_words = file_str.split()
						no_keywords_file_list = [word for word in file_words if word.lower() not in keywords]
						no_keywords_file_str = ' '.join(no_keywords_file_list)
						if no_keywords_file_str and not no_keywords_file_str.isspace():
							try:
								detect = detect_langs(no_keywords_file_str)
								detect_dict = {}
								for x in detect:
									detect_dict[x.lang] = x.prob
								lang_dict[file] = detect_dict
							except:
								pass
					
			elif language.lower() == "java":
				with open("./keywords/java_5.0_2008.txt", "r") as f:
					keywords = [x.strip() for x in f.readlines()]
				try:
					with open(file, "r", encoding="utf8") as f:
						file_str = " ".join(f.readlines())
						file_words = file_str.split()
						no_keywords_file_list = [word for word in file_words if word.lower() not in keywords]
						no_keywords_file_str = ' '.join(no_keywords_file_list)
						if no_keywords_file_str and not no_keywords_file_str.isspace():
							try:
								detect = detect_langs(no_keywords_file_str)
								detect_dict = {}
								for x in detect:
									detect_dict[x.lang] = x.prob
								lang_dict[file] = detect_dict
							except:
								pass 
				except UnicodeDecodeError as e:
					with open(file, "r", encoding="latin-1") as f:
						file_str = " ".join(f.readlines())
						file_words = file_str.split()
						no_keywords_file_list = [word for word in file_words if word.lower() not in keywords]
						no_keywords_file_str = ' '.join(no_keywords_file_list)
						if no_keywords_file_str and not no_keywords_file_str.isspace():
							try:
								detect = detect_langs(no_keywords_file_str)
								detect_dict = {}
								for x in detect:
									detect_dict[x.lang] = x.prob
								lang_dict[file] = detect_dict
							except:
								pass
					
			elif language.lower() == "javascript":
				with open("./keywords/javascript_6.0_2015.txt", "r") as f:
					keywords = [x.strip() for x in f.readlines()]
				try:
					with open(file, "r", encoding="utf8") as f:
						file_str = " ".join(f.readlines())
						file_words = file_str.split()
						no_keywords_file_list = [word for word in file_words if word.lower() not in keywords]
						no_keywords_file_str = ' '.join(no_keywords_file_list)
						if no_keywords_file_str and not no_keywords_file_str.isspace():
							try:
								detect = detect_langs(no_keywords_file_str)
								detect_dict = {}
								for x in detect:
									detect_dict[x.lang] = x.prob
								lang_dict[file] = detect_dict
							except:
								pass
				except UnicodeDecodeError as e:
					with open(file, "r", encoding="latin-1") as f:
						file_str = " ".join(f.readlines())
						file_words = file_str.split()
						no_keywords_file_list = [word for word in file_words if word.lower() not in keywords]
						no_keywords_file_str = ' '.join(no_keywords_file_list)
						if no_keywords_file_str and not no_keywords_file_str.isspace():
							try:
								detect = detect_langs(no_keywords_file_str)
								detect_dict = {}
								for x in detect:
									detect_dict[x.lang] = x.prob
								lang_dict[file] = detect_dict
							except:
								pass
					
			elif language.lower() in ["objectivec", "objective c"]:
				with open("./keywords/objectivec_2.0_2009.txt", "r") as f:
					keywords = [x.strip() for x in f.readlines()]
				try:
					with open(file, "r", encoding="utf8") as f:
						file_str = " ".join(f.readlines())
						file_words = file_str.split()
						no_keywords_file_list = [word for word in file_words if word.lower() not in keywords]
						no_keywords_file_str = ' '.join(no_keywords_file_list)
						if no_keywords_file_str and not no_keywords_file_str.isspace():
							try:
								detect = detect_langs(no_keywords_file_str)
								detect_dict = {}
								for x in detect:
									detect_dict[x.lang] = x.prob
								lang_dict[file] = detect_dict
							except:
								pass
				except UnicodeDecodeError as e:
					with open(file, "r", encoding="latin-1") as f:
						file_str = " ".join(f.readlines())
						file_words = file_str.split()
						no_keywords_file_list = [word for word in file_words if word.lower() not in keywords]
						no_keywords_file_str = ' '.join(no_keywords_file_list)
						if no_keywords_file_str and not no_keywords_file_str.isspace():
							try:
								detect = detect_langs(no_keywords_file_str)
								detect_dict = {}
								for x in detect:
									detect_dict[x.lang] = x.prob
								lang_dict[file] = detect_dict
							except:
								pass
					
			elif language.lower() == "perl":
				with open("./keywords/perl_5.10.0_2007.txt", "r") as f:
					keywords = [x.strip() for x in f.readlines()]
				try:
					with open(file, "r", encoding="utf8") as f:
						file_str = " ".join(f.readlines())
						file_words = file_str.split()
						no_keywords_file_list = [word for word in file_words if word.lower() not in keywords]
						no_keywords_file_str = ' '.join(no_keywords_file_list)
						if no_keywords_file_str and not no_keywords_file_str.isspace():
							try:
								detect = detect_langs(no_keywords_file_str)
								detect_dict = {}
								for x in detect:
									detect_dict[x.lang] = x.prob
								lang_dict[file] = detect_dict
							except:
								pass
				except UnicodeDecodeError as e:
					with open(file, "r", encoding="latin-1") as f:
						file_str = " ".join(f.readlines())
						file_words = file_str.split()
						no_keywords_file_list = [word for word in file_words if word.lower() not in keywords]
						no_keywords_file_str = ' '.join(no_keywords_file_list)
						if no_keywords_file_str and not no_keywords_file_str.isspace():
							try:
								detect = detect_langs(no_keywords_file_str)
								detect_dict = {}
								for x in detect:
									detect_dict[x.lang] = x.prob
								lang_dict[file] = detect_dict
							except:
								pass
					
			elif language.lower() in ["php"]:
				with open("./keywords/php_5.5_2013.txt", "r") as f:
					keywords = [x.strip() for x in f.readlines()]
				try:
					with open(file, "r", encoding="utf8") as f:
						file_str = " ".join(f.readlines())
						file_words = file_str.split()
						no_keywords_file_list = [word for word in file_words if word.lower() not in keywords]
						no_keywords_file_str = ' '.join(no_keywords_file_list)
						if no_keywords_file_str and not no_keywords_file_str.isspace():
							try:
								detect = detect_langs(no_keywords_file_str)
								detect_dict = {}
								for x in detect:
									detect_dict[x.lang] = x.prob
								lang_dict[file] = detect_dict
							except:
								pass
				except UnicodeDecodeError as e:
					with open(file, "r", encoding="latin-1") as f:
						file_str = " ".join(f.readlines())
						file_words = file_str.split()
						no_keywords_file_list = [word for word in file_words if word.lower() not in keywords]
						no_keywords_file_str = ' '.join(no_keywords_file_list)
						if no_keywords_file_str and not no_keywords_file_str.isspace():
							try:
								detect = detect_langs(no_keywords_file_str)
								detect_dict = {}
								for x in detect:
									detect_dict[x.lang] = x.prob
								lang_dict[file] = detect_dict
							except:
								pass
					
			elif language.lower() in ["plsql", "pl/sql"]:
				with open("./keywords/plsql_10.2_2010.txt", "r") as f:
					keywords = [x.strip() for x in f.readlines()]
				try:
					with open(file, "r", encoding="utf8") as f:
						file_str = " ".join(f.readlines())
						file_words = file_str.split()
						no_keywords_file_list = [word for word in file_words if word.lower() not in keywords]
						no_keywords_file_str = ' '.join(no_keywords_file_list)
						if no_keywords_file_str and not no_keywords_file_str.isspace():
							try:
								detect = detect_langs(no_keywords_file_str)
								detect_dict = {}
								for x in detect:
									detect_dict[x.lang] = x.prob
								lang_dict[file] = detect_dict
							except:
								pass 
				except UnicodeDecodeError as e:
					with open(file, "r", encoding="latin-1") as f:
						file_str = " ".join(f.readlines())
						file_words = file_str.split()
						no_keywords_file_list = [word for word in file_words if word.lower() not in keywords]
						no_keywords_file_str = ' '.join(no_keywords_file_list)
						if no_keywords_file_str and not no_keywords_file_str.isspace():
							try:
								detect = detect_langs(no_keywords_file_str)
								detect_dict = {}
								for x in detect:
									detect_dict[x.lang] = x.prob
								lang_dict[file] = detect_dict
							except:
								pass
					
			elif language.lower() == "python":
				with open("./keywords/python_3.x_2008.txt", "r") as f:
					keywords = [x.strip() for x in f.readlines()]
				try:
					with open(file, "r", encoding="utf8") as f:
						file_str = " ".join(f.readlines())
						file_words = file_str.split()
						no_keywords_file_list = [word for word in file_words if word.lower() not in keywords]
						no_keywords_file_str = ' '.join(no_keywords_file_list)
						if no_keywords_file_str and not no_keywords_file_str.isspace():
							try:
								detect = detect_langs(no_keywords_file_str)
								detect_dict = {}
								for x in detect:
									detect_dict[x.lang] = x.prob
								lang_dict[file] = detect_dict
							except:
								pass
				except UnicodeDecodeError as e:
					with open(file, "r", encoding="latin-1") as f:
						file_str = " ".join(f.readlines())
						file_words = file_str.split()
						no_keywords_file_list = [word for word in file_words if word.lower() not in keywords]
						no_keywords_file_str = ' '.join(no_keywords_file_list)
						if no_keywords_file_str and not no_keywords_file_str.isspace():
							try:
								detect = detect_langs(no_keywords_file_str)
								detect_dict = {}
								for x in detect:
									detect_dict[x.lang] = x.prob
								lang_dict[file] = detect_dict
							except:
								pass 
					
			elif language.lower() in ["r"]:
				with open("./keywords/r_3.5.0_2018.txt", "r") as f:
					keywords = [x.strip() for x in f.readlines()]
				try:
					with open(file, "r", encoding="utf8") as f:
						file_str = " ".join(f.readlines())
						file_words = file_str.split()
						no_keywords_file_list = [word for word in file_words if word.lower() not in keywords]
						no_keywords_file_str = ' '.join(no_keywords_file_list)
						if no_keywords_file_str and not no_keywords_file_str.isspace():
							try:
								detect = detect_langs(no_keywords_file_str)
								detect_dict = {}
								for x in detect:
									detect_dict[x.lang] = x.prob
								lang_dict[file] = detect_dict
							except:
								pass 
				except UnicodeDecodeError as e:
					with open(file, "r", encoding="latin-1") as f:
						file_str = " ".join(f.readlines())
						file_words = file_str.split()
						no_keywords_file_list = [word for word in file_words if word.lower() not in keywords]
						no_keywords_file_str = ' '.join(no_keywords_file_list)
						if no_keywords_file_str and not no_keywords_file_str.isspace():
							try:
								detect = detect_langs(no_keywords_file_str)
								detect_dict = {}
								for x in detect:
									detect_dict[x.lang] = x.prob
								lang_dict[file] = detect_dict
							except:
								pass
					
			elif language.lower() == "ruby":
				with open("./keywords/ruby_2.2.0_2014.txt", "r") as f:
					keywords = [x.strip() for x in f.readlines()]
				try:
					with open(file, "r", encoding="utf8") as f:
						file_str = " ".join(f.readlines())
						file_words = file_str.split()
						no_keywords_file_list = [word for word in file_words if word.lower() not in keywords]
						no_keywords_file_str = ' '.join(no_keywords_file_list)
						if no_keywords_file_str and not no_keywords_file_str.isspace():
							try:
								detect = detect_langs(no_keywords_file_str)
								detect_dict = {}
								for x in detect:
									detect_dict[x.lang] = x.prob
								lang_dict[file] = detect_dict
							except:
								pass 
				except UnicodeDecodeError as e:
					with open(file, "r", encoding="latin-1") as f:
						file_str = " ".join(f.readlines())
						file_words = file_str.split()
						no_keywords_file_list = [word for word in file_words if word.lower() not in keywords]
						no_keywords_file_str = ' '.join(no_keywords_file_list)
						if no_keywords_file_str and not no_keywords_file_str.isspace():
							try:
								detect = detect_langs(no_keywords_file_str)
								detect_dict = {}
								for x in detect:
									detect_dict[x.lang] = x.prob
								lang_dict[file] = detect_dict
							except:
								pass
					
			elif language.lower() in ["scala"]:
				with open("./keywords/scala_2.9_2014.txt", "r") as f:
					keywords = [x.strip() for x in f.readlines()]
				try:
					with open(file, "r", encoding="utf8") as f:
						file_str = " ".join(f.readlines())
						file_words = file_str.split()
						no_keywords_file_list = [word for word in file_words if word.lower() not in keywords]
						no_keywords_file_str = ' '.join(no_keywords_file_list)
						if no_keywords_file_str and not no_keywords_file_str.isspace():
							try:
								detect = detect_langs(no_keywords_file_str)
								detect_dict = {}
								for x in detect:
									detect_dict[x.lang] = x.prob
								lang_dict[file] = detect_dict
							except:
								pass 
				except UnicodeDecodeError as e:
					with open(file, "r", encoding="latin-1") as f:
						file_str = " ".join(f.readlines())
						file_words = file_str.split()
						no_keywords_file_list = [word for word in file_words if word.lower() not in keywords]
						no_keywords_file_str = ' '.join(no_keywords_file_list)
						if no_keywords_file_str and not no_keywords_file_str.isspace():
							try:
								detect = detect_langs(no_keywords_file_str)
								detect_dict = {}
								for x in detect:
									detect_dict[x.lang] = x.prob
								lang_dict[file] = detect_dict
							except:
								pass
					
			elif language.lower() in ["shell", "bash"]:
				with open("./keywords/shell_4.4_2016.txt", "r") as f:
					keywords = [x.strip() for x in f.readlines()]
				try:
					with open(file, "r", encoding="utf8") as f:
						file_str = " ".join(f.readlines())
						file_words = file_str.split()
						no_keywords_file_list = [word for word in file_words if word.lower() not in keywords]
						no_keywords_file_str = ' '.join(no_keywords_file_list)
						if no_keywords_file_str and not no_keywords_file_str.isspace():
							try:
								detect = detect_langs(no_keywords_file_str)
								detect_dict = {}
								for x in detect:
									detect_dict[x.lang] = x.prob
								lang_dict[file] = detect_dict
							except:
								pass
				except UnicodeDecodeError as e:
					with open(file, "r", encoding="latin-1") as f:
						file_str = " ".join(f.readlines())
						file_words = file_str.split()
						no_keywords_file_list = [word for word in file_words if word.lower() not in keywords]
						no_keywords_file_str = ' '.join(no_keywords_file_list)
						if no_keywords_file_str and not no_keywords_file_str.isspace():
							try:
								detect = detect_langs(no_keywords_file_str)
								detect_dict = {}
								for x in detect:
									detect_dict[x.lang] = x.prob
								lang_dict[file] = detect_dict
							except:
								pass
					
			elif language.lower() == "sql":
				with open("./keywords/sql_7.2.1_2016.txt", "r") as f:
					keywords = [x.strip() for x in f.readlines()]
				try:
					with open(file, "r", encoding="utf8") as f:
						file_str = " ".join(f.readlines())
						file_words = file_str.split()
						no_keywords_file_list = [word for word in file_words if word.lower() not in keywords]
						no_keywords_file_str = ' '.join(no_keywords_file_list)
						if no_keywords_file_str and not no_keywords_file_str.isspace():
							try:
								detect = detect_langs(no_keywords_file_str)
								detect_dict = {}
								for x in detect:
									detect_dict[x.lang] = x.prob
								lang_dict[file] = detect_dict
							except:
								pass
				except UnicodeDecodeError as e:
					with open(file, "r", encoding="latin-1") as f:
						file_str = " ".join(f.readlines())
						file_words = file_str.split()
						no_keywords_file_list = [word for word in file_words if word.lower() not in keywords]
						no_keywords_file_str = ' '.join(no_keywords_file_list)
						if no_keywords_file_str and not no_keywords_file_str.isspace():
							try:
								detect = detect_langs(no_keywords_file_str)
								detect_dict = {}
								for x in detect:
									detect_dict[x.lang] = x.prob
								lang_dict[file] = detect_dict
							except:
								pass
					
			elif language.lower() in ["swift"]:
				with open("./keywords/swift_4.1_2017.txt", "r") as f:
					keywords = [x.strip() for x in f.readlines()]
				try:
					with open(file, "r", encoding="utf8") as f:
						file_str = " ".join(f.readlines())
						file_words = file_str.split()
						no_keywords_file_list = [word for word in file_words if word.lower() not in keywords]
						no_keywords_file_str = ' '.join(no_keywords_file_list)
						if no_keywords_file_str and not no_keywords_file_str.isspace():
							try:
								detect = detect_langs(no_keywords_file_str)
								detect_dict = {}
								for x in detect:
									detect_dict[x.lang] = x.prob
								lang_dict[file] = detect_dict
							except:
								pass
				except UnicodeDecodeError as e:
					with open(file, "r", encoding="latin-1") as f:
						file_str = " ".join(f.readlines())
						file_words = file_str.split()
						no_keywords_file_list = [word for word in file_words if word.lower() not in keywords]
						no_keywords_file_str = ' '.join(no_keywords_file_list)
						if no_keywords_file_str and not no_keywords_file_str.isspace():
							try:
								detect = detect_langs(no_keywords_file_str)
								detect_dict = {}
								for x in detect:
									detect_dict[x.lang] = x.prob
								lang_dict[file] = detect_dict
							except:
								pass
					
			elif language.lower() in ["typescript"]:
				with open("./keywords/typescript_2.7_2018.txt", "r") as f:
					keywords = [x.strip() for x in f.readlines()]
				try:
					with open(file, "r", encoding="utf8") as f:
						file_str = " ".join(f.readlines())
						file_words = file_str.split()
						no_keywords_file_list = [word for word in file_words if word.lower() not in keywords]
						no_keywords_file_str = ' '.join(no_keywords_file_list)
						if no_keywords_file_str and not no_keywords_file_str.isspace():
							try:
								detect = detect_langs(no_keywords_file_str)
								detect_dict = {}
								for x in detect:
									detect_dict[x.lang] = x.prob
								lang_dict[file] = detect_dict
							except:
								pass
				except UnicodeDecodeError as e:
					with open(file, "r", encoding="latin-1") as f:
						file_str = " ".join(f.readlines())
						file_words = file_str.split()
						no_keywords_file_list = [word for word in file_words if word.lower() not in keywords]
						no_keywords_file_str = ' '.join(no_keywords_file_list)
						if no_keywords_file_str and not no_keywords_file_str.isspace():
							try:
								detect = detect_langs(no_keywords_file_str)
								detect_dict = {}
								for x in detect:
									detect_dict[x.lang] = x.prob
								lang_dict[file] = detect_dict
							except:
								pass
					
			elif language.lower() in ["visual basic", "visual basic .net", "visualbasicnet"]:
				with open("./keywords/visualbasic_14.0_2015.txt", "r") as f:
					keywords = [x.strip() for x in f.readlines()]
				try:
					with open(file, "r", encoding="utf8") as f:
						file_str = " ".join(f.readlines())
						file_words = file_str.split()
						no_keywords_file_list = [word for word in file_words if word.lower() not in keywords]
						no_keywords_file_str = ' '.join(no_keywords_file_list)
						if no_keywords_file_str and not no_keywords_file_str.isspace():
							try:
								detect = detect_langs(no_keywords_file_str)
								detect_dict = {}
								for x in detect:
									detect_dict[x.lang] = x.prob
								lang_dict[file] = detect_dict
							except:
								pass
				except UnicodeDecodeError as e:
					with open(file, "r", encoding="latin-1") as f:
						file_str = " ".join(f.readlines())
						file_words = file_str.split()
						no_keywords_file_list = [word for word in file_words if word.lower() not in keywords]
						no_keywords_file_str = ' '.join(no_keywords_file_list)
						if no_keywords_file_str and not no_keywords_file_str.isspace():
							try:
								detect = detect_langs(no_keywords_file_str)
								detect_dict = {}
								for x in detect:
									detect_dict[x.lang] = x.prob
								lang_dict[file] = detect_dict
							except:
								pass
				
			else:
				print("Language (%s) not currently supported." % language)
	
	return lang_dict
	
#	Classify user based on camel case, snake case,
#	kebab case, or pascal case.
#
#	Params:
#	- user: user object.
def variable_case(user):
	print("NOT FUNCTIONAL.")
	
	# Working on regexs...
	
#	Find median program length.
#
#	Params:
#	- user_program_files: user files which are known to
#	  be programs.	
def median_program_length(user_program_files, write=False):
	print("NOT FUNCTIONAL.")
	
	stats_dict = {}
	
	for file, language in user_program_files.items():
		try:
			with open(file, "r", encoding="utf8") as f:
				text = f.read().splitlines()

				num_lines = len(text)
				num_chars = sum(len(line) for line in text)
				num_words = sum(len(line.split()) for line in text)
				
				num_spaces = sum(line.count(" ") for line in text)
				num_tabs = sum(line.count("\t") for line in text)
				
				stats_dict[file] = {
					"lines": num_lines,
					"chars": num_chars,
					"words": num_words,
					"spaces": num_spaces,
					"tabs": num_tabs
				}
		except UnicodeDecodeError as e:
			with open(file, "r", encoding="latin-1") as f:
				text = f.read().splitlines()

				num_lines = len(text)
				num_chars = sum(len(line) for line in text)
				num_words = sum(len(line.split()) for line in text)
				
				num_spaces = sum(line.count(" ") for line in text)
				num_tabs = sum(line.count("\t") for line in text)
				
				stats_dict[file] = {
					"lines": num_lines,
					"chars": num_chars,
					"words": num_words,
					"spaces": num_spaces,
					"tabs": num_tabs
				}
			
			
	lines_array = []
	chars_array = []
	words_array = []
	spaces_array = []
	tabs_array = []
	
	for key, val in stats_dict.items():
		lines_array.append(val["lines"])
		chars_array.append(val["chars"])
		words_array.append(val["words"])
		spaces_array.append(val["spaces"])
		tabs_array.append(val["tabs"])
		
	overall = {
		"mean_lines": np.mean(lines_array) if lines_array else 0,
		"mean_chars": np.mean(chars_array) if chars_array else 0,
		"mean_words": np.mean(words_array) if words_array else 0,
		"mean_spaces": np.mean(spaces_array) if spaces_array else 0,
		"mean_tabs": np.mean(tabs_array) if tabs_array else 0,
		"median_lines": np.median(lines_array) if lines_array else 0,
		"median_chars": np.median(chars_array) if chars_array else 0,
		"median_words": np.median(words_array) if words_array else 0,
		"median_spaces": np.median(spaces_array) if spaces_array else 0,
		"median_tabs": np.median(tabs_array) if tabs_array else 0
	}
			
	return stats_dict, overall
	
#	Find where brackets/parentheses are placed.
#
#	Params:
#	- file: file name.	
def brackets_and_parentheses(file):
	print("NOT FUNCTIONAL.")
	
	# Basically, if brackets/parentheses are on their own
	# for an entire line or not.
	#
	# This is simple--take line of file, find if
	# bracket or parenthesis on that line, find if the bracket
	# is the only thing on that line or if a left parenthesis
	# does not have a right parenthesis on the same line.
	
#	Find keyword distribution. Also returns non-keyword
#	distributions to be further parsed.
#
#	Currently only supports C, C++, C#, Delphi/Object Pascal,
#	Go, Java, JavaScript, Objective-C, Perl, PHP, PL/SQL,
#	Python, R, Ruby, Scala, Shell (Bash), SQL, Swift, TypeScript,
#	and Visual Basic.
#
#	Params:
#	- user_program_files: user files which are known to
#	  be programs.
def keyword_distribution(user_program_files, save=False):
	print("NOT FUNCTIONAL.")
	
	keyword_distribution = {}
	non_keywords = {}
	
	for file, language in user_program_files.items():
	
		keyword_distribution[file] = {}
	
		if language.lower() == "c":
			try:
				with open("./keywords/c_90.0_1990.txt", "r", encoding="utf8") as f:
					keyword_array = f.read().split("\n")
					
					with open(file, "r") as g:
						wordcount = Counter(g.read().split())
						
						for kw in keyword_array:
							if kw in wordcount:
								keyword_distribution[file][kw] = wordcount[kw]
								del wordcount[kw]
							else:
								keyword_distribution[file][kw] = 0
							
						non_keywords[file] = wordcount
			except:
				pass
					
		elif language.lower() in ["c++", "cplusplus"]:
			try:
				with open("./keywords/cplusplus_17.0_2017.txt", "r", encoding="utf8") as f:
					keyword_array = f.read().split("\n")
					
					with open(file, "r") as g:
						wordcount = Counter(g.read().split())
						
						for kw in keyword_array:
							if kw in wordcount:
								keyword_distribution[file][kw] = wordcount[kw]
								del wordcount[kw]
							else:
								keyword_distribution[file][kw] = 0
							
						non_keywords[file] = wordcount
			except:
				pass
					
		elif language.lower() in ["c#", "csharp"]:
			try:
				with open("./keywords/csharp_7.0_2017.txt", "r", encoding="utf8") as f:
					keyword_array = f.read().split("\n")
					
					with open(file, "r") as g:
						wordcount = Counter(g.read().split())
						
						for kw in keyword_array:
							if kw in wordcount:
								keyword_distribution[file][kw] = wordcount[kw]
								del wordcount[kw]
							else:
								keyword_distribution[file][kw] = 0
							
						non_keywords[file] = wordcount
			except:
				pass
					
		elif language.lower() in ["delphi", "object pascal", "free pascal", "delphiobjectpascal"]:
			try:
				with open("./keywords/delphiobjectpascal_6.0_1990.txt", "r", encoding="utf8") as f:
					keyword_array = f.read().split("\n")
					
					with open(file, "r") as g:
						wordcount = Counter(g.read().split())
						
						for kw in keyword_array:
							if kw in wordcount:
								keyword_distribution[file][kw] = wordcount[kw]
								del wordcount[kw]
							else:
								keyword_distribution[file][kw] = 0
							
						non_keywords[file] = wordcount
			except:
				pass
					
		elif language.lower() == "go":
			try:
				with open("./keywords/go_1.9.4_2017.txt", "r", encoding="utf8") as f:
					keyword_array = f.read().split("\n")
					
					with open(file, "r") as g:
						wordcount = Counter(g.read().split())
						
						for kw in keyword_array:
							if kw in wordcount:
								keyword_distribution[file][kw] = wordcount[kw]
								del wordcount[kw]
							else:
								keyword_distribution[file][kw] = 0
							
						non_keywords[file] = wordcount
			except:
				pass
					
		elif language.lower() == "java":
			try:
				with open("./keywords/java_5.0_2008.txt", "r", encoding="utf8") as f:
					keyword_array = f.read().split("\n")
					
					with open(file, "r") as g:
						wordcount = Counter(g.read().split())
						
						for kw in keyword_array:
							if kw in wordcount:
								keyword_distribution[file][kw] = wordcount[kw]
								del wordcount[kw]
							else:
								keyword_distribution[file][kw] = 0
							
						non_keywords[file] = wordcount
			except:
				pass
					
		elif language.lower() == "javascript":
			try:
				with open("./keywords/javascript_6.0_2015.txt", "r", encoding="utf8") as f:
					keyword_array = f.read().split("\n")
					
					with open(file, "r") as g:
						wordcount = Counter(g.read().split())
						
						for kw in keyword_array:
							if kw in wordcount:
								keyword_distribution[file][kw] = wordcount[kw]
								del wordcount[kw]
							else:
								keyword_distribution[file][kw] = 0
							
						non_keywords[file] = wordcount
			except:
				pass
					
		elif language.lower() in ["objective-c", "objectivec"]:
			try:
				with open("./keywords/objectivec_2.0_2009.txt", "r", encoding="utf8") as f:
					keyword_array = f.read().split("\n")
					
					with open(file, "r") as g:
						wordcount = Counter(g.read().split())
						
						for kw in keyword_array:
							if kw in wordcount:
								keyword_distribution[file][kw] = wordcount[kw]
								del wordcount[kw]
							else:
								keyword_distribution[file][kw] = 0
							
						non_keywords[file] = wordcount
			except:
				pass
					
		elif language.lower() == "perl":
			try:
				with open("./keywords/perl_5.10.0_2007.txt", "r", encoding="utf8") as f:
					keyword_array = f.read().split("\n")
					
					with open(file, "r") as g:
						wordcount = Counter(g.read().split())
						
						for kw in keyword_array:
							if kw in wordcount:
								keyword_distribution[file][kw] = wordcount[kw]
								del wordcount[kw]
							else:
								keyword_distribution[file][kw] = 0
							
						non_keywords[file] = wordcount
			except:
				pass
					
		elif language.lower() == "php":
			try:
				with open("./keywords/php_5.5_2013.txt", "r", encoding="utf8") as f:
					keyword_array = f.read().split("\n")
					
					with open(file, "r") as g:
						wordcount = Counter(g.read().split())
						
						for kw in keyword_array:
							if kw in wordcount:
								keyword_distribution[file][kw] = wordcount[kw]
								del wordcount[kw]
							else:
								keyword_distribution[file][kw] = 0
							
						non_keywords[file] = wordcount
			except:
				pass
					
		elif language.lower() in ["pl/sql", "plsql"]:
			try:
				with open("./keywords/plsql_10.2_2010.txt", "r", encoding="utf8") as f:
					keyword_array = f.read().split("\n")
					
					with open(file, "r") as g:
						wordcount = Counter(g.read().split())
						
						for kw in keyword_array:
							if kw in wordcount:
								keyword_distribution[file][kw] = wordcount[kw]
								del wordcount[kw]
							else:
								keyword_distribution[file][kw] = 0
							
						non_keywords[file] = wordcount
			except:
				pass
					
		elif language.lower() == "python":
			try:
				with open("./keywords/python_3.x_2008.txt", "r", encoding="utf8") as f:
					keyword_array = f.read().split("\n")
					
					with open(file, "r") as g:
						wordcount = Counter(g.read().split())
						
						for kw in keyword_array:
							if kw in wordcount:
								keyword_distribution[file][kw] = wordcount[kw]
								del wordcount[kw]
							else:
								keyword_distribution[file][kw] = 0
							
						non_keywords[file] = wordcount
			except:
				pass
					
		elif language.lower() == "r":
			try:
				with open("./keywords/r_3.5.0_2018.txt", "r", encoding="utf8") as f:
					keyword_array = f.read().split("\n")
					
					with open(file, "r") as g:
						wordcount = Counter(g.read().split())
						
						for kw in keyword_array:
							if kw in wordcount:
								keyword_distribution[file][kw] = wordcount[kw]
								del wordcount[kw]
							else:
								keyword_distribution[file][kw] = 0
							
						non_keywords[file] = wordcount
			except:
				pass
					
		elif language.lower() == "ruby":
			try:
				with open("./keywords/ruby_2.2.0_2014.txt", "r", encoding="utf8") as f:
					keyword_array = f.read().split("\n")
					
					with open(file, "r") as g:
						wordcount = Counter(g.read().split())
						
						for kw in keyword_array:
							if kw in wordcount:
								keyword_distribution[file][kw] = wordcount[kw]
								del wordcount[kw]
							else:
								keyword_distribution[file][kw] = 0
							
						non_keywords[file] = wordcount
			except:
				pass
					
		elif language.lower() == "scala":
			try:
				with open("./keywords/scala_2.9_2014.txt", "r", encoding="utf8") as f:
					keyword_array = f.read().split("\n")
					
					with open(file, "r") as g:
						wordcount = Counter(g.read().split())
						
						for kw in keyword_array:
							if kw in wordcount:
								keyword_distribution[file][kw] = wordcount[kw]
								del wordcount[kw]
							else:
								keyword_distribution[file][kw] = 0
							
						non_keywords[file] = wordcount
			except:
				pass
					
		elif language.lower() in ["shell", "bash"]:
			try:
				with open("./keywords/shell_4.4_2016.txt", "r", encoding="utf8") as f:
					keyword_array = f.read().split("\n")
					
					with open(file, "r") as g:
						wordcount = Counter(g.read().split())
						
						for kw in keyword_array:
							if kw in wordcount:
								keyword_distribution[file][kw] = wordcount[kw]
								del wordcount[kw]
							else:
								keyword_distribution[file][kw] = 0
							
						non_keywords[file] = wordcount
			except:
				pass
					
		elif language.lower() == "sql":
			try:
				with open("./keywords/sql_7.2.1_2016.txt", "r", encoding="utf8") as f:
					keyword_array = f.read().split("\n")
					
					with open(file, "r") as g:
						wordcount = Counter(g.read().split())
						
						for kw in keyword_array:
							if kw in wordcount:
								keyword_distribution[file][kw] = wordcount[kw]
								del wordcount[kw]
							else:
								keyword_distribution[file][kw] = 0
							
						non_keywords[file] = wordcount
			except:
				pass
					
		elif language.lower() == "swift":
			try:
				with open("./keywords/swift_4.1_2017.txt", "r", encoding="utf8") as f:
					keyword_array = f.read().split("\n")
					
					with open(file, "r") as g:
						wordcount = Counter(g.read().split())
						
						for kw in keyword_array:
							if kw in wordcount:
								keyword_distribution[file][kw] = wordcount[kw]
								del wordcount[kw]
							else:
								keyword_distribution[file][kw] = 0
							
						non_keywords[file] = wordcount
			except:
				pass
			
		elif language.lower() == "typescript":
			try:
				with open("./keywords/typescript_2.7_2018.txt", "r", encoding="utf8") as f:
					keyword_array = f.read().split("\n")
					
					with open(file, "r") as g:
						wordcount = Counter(g.read().split())
						
						for kw in keyword_array:
							if kw in wordcount:
								keyword_distribution[file][kw] = wordcount[kw]
								del wordcount[kw]
							else:
								keyword_distribution[file][kw] = 0
							
						non_keywords[file] = wordcount
			except:
				pass
					
		elif language.lower() in ["visual basic", "visual basic .net", "visualbasic", "visualbasicnet"]:
			with open("./keywords/visualbasic_14.0_2015.txt", "r", encoding="utf8") as f:
				keyword_array = f.read().split("\n")
				
				with open(file, "r") as g:
					wordcount = Counter(g.read().split())
					
					for kw in keyword_array:
						if kw in wordcount:
							keyword_distribution[file][kw] = wordcount[kw]
							del wordcount[kw]
						else:
							keyword_distribution[file][kw] = 0
						
					non_keywords[file] = wordcount
					
	return keyword_distribution, non_keywords
	
#	Find names of things in code which are not
#	keywords, restricted words, or comments.
#
#	Params:
#	- file: file name.	
def variable_names(user):
	print("NOT FUNCTIONAL.")
	
	# Remove keywords/restricted words.
	
	# Remove comments.
	
	# Analyze what is left.
	
	# Create distribution of these words.
	
	# Use langdetect.
	
	# Return word distribution and language detection result.
	
#   MAIN
if __name__ == "__main__": main()