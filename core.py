

import os
import shutil
import json
from PIL import Image, ImageFile
from tqdm import trange
from time import sleep
from tempfile import TemporaryDirectory
from datetime import datetime
import re

regex = r".(?<![\x00-\x7F])"
subst = "?"

ImageFile.MAXBLOCK = 2**30

def get_data(worker, temp):
	f = open(f"{temp}/data.json", "r")
	images = json.JSONDecoder().decode(f.read())
	f.close()
	return images[worker]

def get_pos(size, to):
	if size[0]>size[1]:
		newS = to
		newP = round((size[1]/size[0]) * to)
	else:
		newP = to
		newS = round((size[0]/size[1]) * to)
	return (newS, newP)

def start(worker, size, quality, folder, temp, preffix, suffix, upscale, downscale, copy_ud):
	curr = ""
	d = open(f"{temp}/core{worker}.log", "w")
	d.close()
	d = open(f"{temp}/core{worker}.log", "a")
	try:
		images = get_data(worker, temp)
		for x in trange(len(images), leave=True, dynamic_ncols=True, ascii=True):#, bar_format= "{l_bar}{bar}|{n_fmt}/{total_fmt}"
			try:
				curr = images[x][1]
				img = Image.open(f"{images[x][0]}{images[x][2]}")
				if not os.path.isdir(images[x][1]):
					os.makedirs(images[x][1])
				if (((img.size[0] > size or img.size[1] > size) and downscale) or ((img.size[0] < size and img.size[1] < size) and upscale)):
					img.resize(get_pos(img.size, size), resample = Image.BICUBIC).save(f"{folder}{images[x][1]}{preffix}{images[x][3]}{suffix}{images[x][4]}", quality=quality, optimize=True)
				elif copy_ud:
					img.save(f"{folder}{images[x][1]}{preffix}{images[x][3]}{suffix}{images[x][4]}", quality=quality, optimize=True)
				img = None
				os.system("cls")
			except Exception as E:
				d.write("\n" + re.sub(regex, subst, f'{datetime.now().strftime("%d.%m.%Y %H:%M:%S")} [Error] > "{images[x][0]}{images[x][2]}" > {E}'))
	except Exception as E:
		d = open(f"{temp}/core{worker}.log", "a")
		d.write(f"\n{datetime.now()} [Error] > {curr} > {E}")
		d.close()
		f = open(f"{temp}/core{worker}.data", "w+")
		f.close()
	d.close()
	f = open(f"{temp}/core{worker}.data", "w+")
	f.close()