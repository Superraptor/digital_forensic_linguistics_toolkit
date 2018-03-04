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
#	DEPENDENCIES:
#	- Python 3.4
#	- Python 3.5
#

#
#	IMPORTS
#

from geopy.geocoders import Nominatim, GoogleV3
from sklearn import linear_model
from sklearn import svm
from sklearn.ensemble import GradientBoostingRegressor, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, explained_variance_score, r2_score, precision_score, roc_auc_score, recall_score, median_absolute_error, mean_absolute_error
from sklearn.multioutput import MultiOutputRegressor
from sklearn.neighbors import KNeighborsClassifier
from tqdm import tqdm
import geopy
import json
import numpy as np
import os
import pandas as pd
import time

#   MAIN
def main():
	input, output = preprocessing()
	
	#clf.fit(input, output)
	#predictions = clf.predict(input)
	
	#print(output[["gender"]])
	
	#clf = linear_model.Lasso()
	clf = linear_model.LinearRegression()
	clf.fit(input, output[["black_hair_color"]])
	predictions = clf.predict(input)
	
	print("\n")
	print("BLACK HAIR COLOR:")
	print(explained_variance_score(output[["black_hair_color"]], predictions))
	print(median_absolute_error(output[["black_hair_color"]], predictions))
	print(mean_absolute_error(output[["black_hair_color"]], predictions))
	
	clf = linear_model.LinearRegression()
	clf.fit(input, output[["red_hair_color"]])
	predictions = clf.predict(input)
	
	print("\n")
	print("RED HAIR COLOR:")
	print(explained_variance_score(output[["red_hair_color"]], predictions))
	print(median_absolute_error(output[["red_hair_color"]], predictions))
	print(mean_absolute_error(output[["red_hair_color"]], predictions))
	
	clf = linear_model.LinearRegression()
	clf.fit(input, output[["brown_hair_color"]])
	predictions = clf.predict(input)
	
	print("\n")
	print("BROWN HAIR COLOR:")
	print(explained_variance_score(output[["brown_hair_color"]], predictions))
	print(median_absolute_error(output[["brown_hair_color"]], predictions))
	print(mean_absolute_error(output[["brown_hair_color"]], predictions))
	
	clf = linear_model.LinearRegression()
	clf.fit(input, output[["blond_hair_color"]])
	predictions = clf.predict(input)
	
	print("\n")
	print("BLOND HAIR COLOR:")
	print(explained_variance_score(output[["blond_hair_color"]], predictions))
	print(median_absolute_error(output[["blond_hair_color"]], predictions))
	print(mean_absolute_error(output[["blond_hair_color"]], predictions))
	
	clf = linear_model.LinearRegression()
	clf.fit(input, output[["moustache"]])
	predictions = clf.predict(input)
	
	print("\n")
	print("MOUSTACHE:")
	print(explained_variance_score(output[["moustache"]], predictions))
	print(median_absolute_error(output[["moustache"]], predictions))
	print(mean_absolute_error(output[["moustache"]], predictions))
	
	clf = linear_model.LinearRegression()
	clf.fit(input, output[["beard"]])
	predictions = clf.predict(input)
	
	print("\n")
	print("BEARD:")
	print(explained_variance_score(output[["beard"]], predictions))
	print(median_absolute_error(output[["beard"]], predictions))
	print(mean_absolute_error(output[["beard"]], predictions))
	
	clf = linear_model.LinearRegression()
	clf.fit(input, output[["bald"]])
	predictions = clf.predict(input)
	
	print("\n")
	print("BALD:")
	print(explained_variance_score(output[["bald"]], predictions))
	print(median_absolute_error(output[["bald"]], predictions))
	print(mean_absolute_error(output[["bald"]], predictions))
	
	exit()
	
	#clf = svm.SVC(kernel="linear")
	#clf.fit(input, output[["country"]].values.flatten())
	#predictions = clf.predict(input)
	
	#clf = RandomForestClassifier(max_depth=2, random_state=0)
	#clf.fit(input, output[["country"]].values.flatten())
	#predictions = clf.predict(input)
	
	#clf = KNeighborsClassifier()
	#clf.fit(input, output[["country"]].values.flatten())
	#predictions = clf.predict(input)
	
	#print("\n")
	#print("COUNTRY:")
	#print(clf.feature_importances_)
	#print(accuracy_score(output[["country"]], predictions))
	#print(explained_variance_score(output[["country"]], predictions))
	#print(r2_score(output[["country"]], predictions))
	#print(precision_score(output[["country"]], predictions))
	#print(recall_score(output[["country"]], predictions))
	#print(roc_auc_score(output[["country"]], predictions))
	
	#clf = svm.SVC(kernel="linear")
	#clf.fit(input, output[["gender"]].values.flatten())
	#predictions = clf.predict(input)
	
	#clf = RandomForestClassifier(max_depth=2, random_state=0)
	#clf.fit(input, output[["gender"]].values.flatten())
	#predictions = clf.predict(input)
	
	#clf = KNeighborsClassifier()
	#clf.fit(input, output[["gender"]].values.flatten())
	#predictions = clf.predict(input)
	
	#print("\n")
	#print("GENDER:")
	#print(clf.feature_importances_)
	#print(accuracy_score(output[["gender"]], predictions))
	#print(explained_variance_score(output[["gender"]], predictions))
	#print(r2_score(output[["gender"]], predictions))
	#print(precision_score(output[["gender"]], predictions))
	#print(recall_score(output[["gender"]], predictions))
	#print(roc_auc_score(output[["gender"]], predictions))

	clf = svm.SVC(kernel="linear")
	clf.fit(input, output[["age"]].values.flatten().astype(int))
	predictions = clf.predict(input)
	
	#clf = RandomForestClassifier(max_depth=2, random_state=0)
	#clf.fit(input, output[["age"]].values.flatten().astype(int))
	#predictions = clf.predict(input)
	
	#clf = KNeighborsClassifier()
	#clf.fit(input, output[["age"]].values.flatten().astype(int))
	#predictions = clf.predict(input)
	
	print("\n")
	print("AGE:")
	#print(clf.feature_importances_)
	print(accuracy_score(output[["age"]].values.flatten().astype(int), predictions))
	print(explained_variance_score(output[["age"]].values.flatten().astype(int), predictions))
	print(r2_score(output[["age"]].values.flatten().astype(int), predictions))
	#print(precision_score(output[["age"]], predictions))
	#print(recall_score(output[["age"]], predictions))
	#print(roc_auc_score(output[["age"]], predictions))
	
#	Preprocessing.
def preprocessing():
	
	user_dict = {}
	if os.path.isfile("./users/proc_user_dict.txt"):
		with open("./users/proc_user_dict.txt", "r", encoding="utf8") as f:
			user_dict = eval(f.read())
		
	else:
		for file in os.listdir("./users/"):
			if "proc" not in file:
				with open("./users/"+file, "r", encoding="utf8") as f:
					for line in tqdm(f.readlines()):
					
						line_array = line.split("\t")
						username = line_array[0].strip()
						repos_url = line_array[1].strip()
						location = line_array[2].strip()
						avatar_url = line_array[3].strip()
						public_repos = line_array[4].strip()
						name = line_array[5].strip()
						
						if os.path.isfile("./proc_images/"+username+".jpg"):
							if location != "" and location is not None:
								print(location)
						
								geolocator = GoogleV3(api_key="AIzaSyDD9bAmgJQYnqnCM6v-kRtl4hTWIHdaVac")
								try:
									location_result = geolocator.geocode(location.replace(" ", "%20"))
								
									if location_result is not None:
										country = None
										for component in location_result.raw["address_components"]:
											if "country" in component["types"]:
												country = component["long_name"]

										if country is not None:
											temp_user = {
												"username": username,
												"repos_url": repos_url,
												"location": location,
												"avatar_url": avatar_url,
												"public_repos": public_repos,
												"name": name,
												"country": country
											}
											
											user_dict[username] = temp_user
											
											with open("./users/proc_user_dict.txt", "w", encoding="utf8") as f:
												f.write(str(user_dict))
								except geopy.exc.GeocoderTimedOut:
									pass
											
								time.sleep(1)
	
	# Face data arranged by user.
	face_dict = {}
	with open("./faces/faces.txt", "r", encoding="utf8") as f:
		face_dict = eval(f.read())
		
	# Set up output dictionary.
	user_order = []
	output = {}
	output_array = []
	output_df = pd.DataFrame(columns=["gender", "age", "moustache", "sideburns", "beard", "bald", "black_hair_color", "brown_hair_color", "other_hair_color", "gray_hair_color", "red_hair_color", "blond_hair_color", "country"])
	for i, (user, sub_dict) in enumerate(user_dict.items()):
		if user in face_dict:
			if len(face_dict[user]) == 1:
				user_face = face_dict[user][0]
			
				gender = user_face["faceAttributes"]["gender"]
				age = user_face["faceAttributes"]["age"]
				moustache = user_face["faceAttributes"]["facialHair"]["moustache"]
				sideburns = user_face["faceAttributes"]["facialHair"]["sideburns"]
				beard = user_face["faceAttributes"]["facialHair"]["beard"]
				bald = user_face["faceAttributes"]["hair"]["bald"]
				black_hair_color = 0
				brown_hair_color = 0
				other_hair_color = 0
				gray_hair_color = 0
				red_hair_color = 0
				blond_hair_color = 0
				country = sub_dict["country"]
				
				for hair_color in user_face["faceAttributes"]["hair"]["hairColor"]:
					if hair_color["color"] == "black":
						black_hair_color = hair_color["confidence"]
					elif hair_color["color"] == "brown":
						brown_hair_color = hair_color["confidence"]
					elif hair_color["color"] == "other":
						other_hair_color = hair_color["confidence"]
					elif hair_color["color"] == "gray":
						gray_hair_color = hair_color["confidence"]
					elif hair_color["color"] == "red":
						red_hair_color = hair_color["confidence"]
					elif hair_color["color"] == "blond":
						blond_hair_color = hair_color["confidence"]
			
				user_order.append(user)
				
				output[user] = [
					gender, age, moustache, sideburns, beard, bald,
					black_hair_color, brown_hair_color, other_hair_color,
					gray_hair_color, red_hair_color, blond_hair_color, country
				]
				output_array.append([
					gender, age, moustache, sideburns, beard, bald,
					black_hair_color, brown_hair_color, other_hair_color,
					gray_hair_color, red_hair_color, blond_hair_color, country
				])
				
				output_df.loc[i] = output[user]
				
	# Change gender and country into numeric variables.
	output_df["gender"] = output_df["gender"].astype("category")
	output_df["country"] = output_df["country"].astype("category")
	cat_columns = output_df.select_dtypes(["category"]).columns	
	output_df.to_csv("./categories/output.csv")
	output_df[cat_columns] = output_df[cat_columns].apply(lambda x: x.cat.codes)
	output_df.to_csv("./categories/output_encoded.csv")
	
	# Set up input dataframe.
	input_df = pd.DataFrame(columns=["mean_lines", "mean_chars", "mean_words", "mean_spaces", "mean_tabs", "median_lines", "median_chars", "median_words", "median_spaces", "median_tabs", "c", "cplusplus", "csharp", "delphiobjectpascal", "go", "java", "javascript", "objectivec", "perl", "php", "plsql", "python", "r", "ruby", "scala", "shell", "sql", "swift", "typescript", "visualbasicnet",
		"af", "ar", "bg", "bn", "ca", "cs", "cy", "da", "de", "el", "en", "es", 
		"et", "fa", "fi", "fr", "gu", "he", "hi", "hr", "hu", "id", "it", "ja", 
		"kn", "ko", "lt", "lv", "mk", "ml", "mr", "ne", "nl", "no", "pa", "pl", 
		"pt", "ro", "ru", "sk", "sl", "so", "sq", "sv", "sw", "ta", "te", "th", 
		"tl", "tr", "uk", "ur", "vi", "zh_cn", "zh_tw"
	])
		
	## Keyword counts arranged by user and file.
	#file_keyword_distributions = {}
	#with open("./keywords/distributions/keywords.txt", "r", encoding="utf8") as f:
	#	file_keyword_distributions = eval(f.read())
		
	# Metrics 
	metric_dict = {}
	with open("./metrics/median.txt", "r", encoding="utf8") as f:
		metric_dict = eval(f.read())
		
	# Natural languages.
	nat_lang_dict = {}
	with open("./nat_lang/nat_lang.txt", "r", encoding="utf8") as f:
		nat_lang_dict = eval(f.read())
		
	# Programming languages.
	prog_lang_dict = {}
	with open("./prog_lang/lang_dict.txt", "r", encoding="utf8") as f:
		prog_lang_dict = eval(f.read())
	
	for i, user in enumerate(user_order):
		user_stats = metric_dict[user]["user_stats"]
		prog_lang_counts = prog_lang_dict[user]["language_dictionary"]
		c = prog_lang_counts["c"] if "c" in prog_lang_counts else 0
		cplusplus = prog_lang_counts["cplusplus"] if "cplusplus" in prog_lang_counts else 0
		csharp = prog_lang_counts["csharp"] if "csharp" in prog_lang_counts else 0
		delphiobjectpascal = prog_lang_counts["delphiobjectpascal"] if "delphiobjectpascal" in prog_lang_counts else 0
		go = prog_lang_counts["go"] if "go" in prog_lang_counts else 0
		java = prog_lang_counts["java"] if "java" in prog_lang_counts else 0
		javascript = prog_lang_counts["javascript"] if "javascript" in prog_lang_counts else 0
		objectivec = prog_lang_counts["objectivec"] if "objectivec" in prog_lang_counts else 0
		perl = prog_lang_counts["perl"] if "perl" in prog_lang_counts else 0
		php = prog_lang_counts["php"] if "php" in prog_lang_counts else 0
		plsql = prog_lang_counts["plsql"] if "plsql" in prog_lang_counts else 0
		python = prog_lang_counts["python"] if "python" in prog_lang_counts else 0
		r = prog_lang_counts["r"] if "r" in prog_lang_counts else 0
		ruby = prog_lang_counts["ruby"] if "ruby" in prog_lang_counts else 0
		scala = prog_lang_counts["scala"] if "scala" in prog_lang_counts else 0
		shell = prog_lang_counts["shell"] if "shell" in prog_lang_counts else 0
		sql = prog_lang_counts["sql"] if "sql" in prog_lang_counts else 0
		swift = prog_lang_counts["swift"] if "swift" in prog_lang_counts else 0
		typescript = prog_lang_counts["typescript"] if "typescript" in prog_lang_counts else 0
		visualbasicnet = prog_lang_counts["visualbasicnet"] if "visualbasicnet" in prog_lang_counts else 0
		
		af = 0
		ar = 0
		bg = 0
		bn = 0
		ca = 0
		cs = 0
		cy = 0
		da = 0
		de = 0
		el = 0
		en = 0
		es = 0
		et = 0
		fa = 0
		fi = 0
		fr = 0
		gu = 0
		he = 0
		hi = 0
		hr = 0
		hu = 0
		id = 0
		it = 0
		ja = 0
		kn = 0
		ko = 0
		lt = 0
		lv = 0
		mk = 0
		ml = 0
		mr = 0
		ne = 0
		nl = 0
		no = 0
		pa = 0
		pl = 0
		pt = 0
		ro = 0
		ru = 0
		sk = 0
		sl = 0
		so = 0
		sq = 0
		sv = 0
		sw = 0
		ta = 0
		te = 0
		th = 0
		tl = 0
		tr = 0
		uk = 0
		ur = 0
		vi = 0
		zh_cn = 0
		zh_tw = 0
		file_list = []
		for sub_key, sub_val in nat_lang_dict[user].items():
			file_list.append(sub_key)
			for infra_key, infra_val in sub_val.items():
				lang_code = infra_key
				confidence = infra_val
				if lang_code == "af":
					af += confidence
				elif lang_code == "ar":
					ar += confidence
				elif lang_code == "bg":
					bg += confidence
				elif lang_code == "bn":
					bn += confidence
				elif lang_code == "ca":
					ca += confidence
				elif lang_code == "cs":
					cs += confidence
				elif lang_code == "cy":
					cy += confidence
				elif lang_code == "da":
					da += confidence
				elif lang_code == "de":
					de += confidence
				elif lang_code == "el":
					el += confidence
				elif lang_code == "en":
					en += confidence
				elif lang_code == "es":
					es += confidence
				elif lang_code == "et":
					et += confidence
				elif lang_code == "fa":
					fa += confidence
				elif lang_code == "fi":
					fi += confidence
				elif lang_code == "fr":
					fr += confidence
				elif lang_code == "gu":
					gu += confidence
				elif lang_code == "he":
					he += confidence
				elif lang_code == "hi":
					hi += confidence
				elif lang_code == "hr":
					hr += confidence
				elif lang_code == "hu":
					hu += confidence
				elif lang_code == "id":
					id += confidence
				elif lang_code == "it":
					it += confidence
				elif lang_code == "ja":
					ja += confidence
				elif lang_code == "kn":
					kn += confidence
				elif lang_code == "ko":
					ko += confidence
				elif lang_code == "lt":
					lt += confidence
				elif lang_code == "lv":
					lv += confidence
				elif lang_code == "mk":
					mk += confidence
				elif lang_code == "ml":
					ml += confidence
				elif lang_code == "mr":
					mr += confidence
				elif lang_code == "ne":
					ne += confidence
				elif lang_code == "nl":
					nl += confidence
				elif lang_code == "no":
					no += confidence
				elif lang_code == "pa":
					pa += confidence
				elif lang_code == "pl":
					pl += confidence
				elif lang_code == "pt":
					pt += confidence
				elif lang_code == "ro":
					ro += confidence
				elif lang_code == "ru":
					ru += confidence
				elif lang_code == "sk":
					sk += confidence
				elif lang_code == "sl":
					sl += confidence
				elif lang_code == "so":
					so += confidence
				elif lang_code == "sq":
					sq += confidence
				elif lang_code == "sv":
					sv += confidence
				elif lang_code == "sw":
					sw += confidence
				elif lang_code == "ta":
					ta += confidence
				elif lang_code == "te":
					te += confidence
				elif lang_code == "th":
					th += confidence
				elif lang_code == "tl":
					tl += confidence
				elif lang_code == "tr":
					tr += confidence
				elif lang_code == "uk":
					uk += confidence
				elif lang_code == "ur":
					ur += confidence
				elif lang_code == "vi":
					vi += confidence
					
		if len(file_list) > 0:
			af = af / len(file_list)
			ar = ar / len(file_list)
			bg = bg / len(file_list)
			bn = bn / len(file_list)
			ca = ca / len(file_list)
			cs = cs / len(file_list)
			cy = cy / len(file_list)
			da = da / len(file_list)
			de = de / len(file_list)
			el = el / len(file_list)
			en = en / len(file_list)
			es = es / len(file_list)
			et = et / len(file_list)
			fa = fa / len(file_list)
			fi = fi / len(file_list)
			fr = fr / len(file_list)
			gu = gu / len(file_list)
			he = he / len(file_list)
			hi = hi / len(file_list)
			hr = hr / len(file_list)
			hu = hu / len(file_list)
			id = id / len(file_list)
			it = it / len(file_list)
			ja = ja / len(file_list)
			kn = kn / len(file_list)
			ko = ko / len(file_list)
			lt = lt / len(file_list)
			lv = lv / len(file_list)
			mk = mk / len(file_list)
			ml = ml / len(file_list)
			mr = mr / len(file_list)
			ne = ne / len(file_list)
			nl = nl / len(file_list)
			no = no / len(file_list)
			pa = pa / len(file_list)
			pl = pl / len(file_list)
			pt = pt / len(file_list)
			ro = ro / len(file_list)
			ru = ru / len(file_list)
			sk = sk / len(file_list)
			sl = sl / len(file_list)
			so = so / len(file_list)
			sq = sq / len(file_list)
			sv = sv / len(file_list)
			sw = sw / len(file_list)
			ta = ta / len(file_list)
			te = te / len(file_list)
			th = th / len(file_list)
			tl = tl / len(file_list)
			tr = tr / len(file_list)
			uk = uk / len(file_list)
			ur = ur / len(file_list)
			vi = vi / len(file_list)
			zh_cn = zh_cn / len(file_list)
			zh_tw = zh_tw / len(file_list)
		
		input_df.loc[i] = [
			user_stats["mean_lines"], user_stats["mean_chars"], user_stats["mean_words"], user_stats["mean_spaces"], user_stats["mean_tabs"],
			user_stats["median_lines"], user_stats["median_chars"], user_stats["median_words"], user_stats["median_spaces"], user_stats["median_tabs"],
			c, cplusplus, csharp, delphiobjectpascal, go, java, javascript, objectivec,
			perl, php, plsql, python, r, ruby, scala, shell, sql, swift, typescript, visualbasicnet,
			af, ar, bg, bn, ca, cs, cy, da, de, el, en, es, et, fa, fi, fr, gu, he, 
			hi, hr, hu, id, it, ja, kn, ko, lt, lv, mk, ml, mr, ne, nl, no, pa, pl, 
			pt, ro, ru, sk, sl, so, sq, sv, sw, ta, te, th, tl, tr, uk, ur, vi, zh_cn, zh_tw
		]
		
	return input_df, output_df

#   MAIN
if __name__ == "__main__": main()