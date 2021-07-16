

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
	if size[0] > size[1]:
		newS = to
		newP = round((size[1]/size[0]) * to)
	else:
		newP = to
		newS = round((size[0]/size[1]) * to)
	return (newS, newP)


def make_square(path, max_size=600, fill_color=(255, 255, 255)):
	# find image dimensions
	old_img = Image.open(path)
	size = (min(max_size, max(old_img.size)),) * 2

	# resize if old image is larger than max_size
	if size[0] < old_img.size[0] or size[1] < old_img.size[1]:
		old_img.thumbnail(size)

	# create new image with the given color and computed size
	new_img = Image.new(old_img.mode, size, fill_color)

	# find coordinates of upper-left corner to center the old image in the new image
	assert new_img.size[0] >= old_img.size[0]
	assert new_img.size[1] >= old_img.size[1]

	x = (new_img.size[0] - old_img.size[0]) // 2
	y = (new_img.size[1] - old_img.size[1]) // 2

	# paste image
	new_img.paste(old_img, (x, y))

	# file = pathlib.path(path)
	# file.unlink()
	# save image
	new_img.save(path)


def start(worker, size, quality, folder, temp, preffix, suffix, upscale, downscale, copy_ud, cores,make_rect,out_ext):
	curr = ""
	d = open(f"{temp}/core{worker}.log", "w")
	d.close()
	d = open(f"{temp}/core{worker}.log", "a")
	try:
		images = get_data(worker, temp)
		# , bar_format= "{l_bar}{bar}|{n_fmt}/{total_fmt}"
		bar = trange(len(images), leave=True, dynamic_ncols=True, ascii=True)
		terminalsize = 100**10
		for x in bar:
			if os.path.isfile("./stop.all"):
				break
			try:
				curr = images[x][1]
				if(out_ext): images[x][4] = out_ext
				img = Image.open(f"{folder}{images[x][0]}{images[x][2]}")
				if not os.path.isdir(folder + images[x][1]):
					os.makedirs(folder + images[x][1])
				if (((img.size[0] > size or img.size[1] > size) and downscale) or ((img.size[0] < size and img.size[1] < size) and upscale)):
					img.resize(get_pos(img.size, size), resample=Image.BICUBIC).save(
						f"{folder}{images[x][1]}{preffix}{images[x][3]}{suffix}{images[x][4]}", quality=quality, optimize=True)
					if make_rect:
						make_square(f"{folder}{images[x][1]}{preffix}{images[x][3]}{suffix}{images[x][4]}", size)
						pass
				elif copy_ud:
					img.save(f"{folder}{images[x][1]}{preffix}{images[x][3]}{suffix}{images[x][4]}", quality=quality, optimize=True)
				img = None
				fa = open(f"{temp}/core{worker}.progress", "w")
				fa.write(str(x))
				fa.close()
				if os.get_terminal_size()[0] < terminalsize or bar.ncols+1 > os.get_terminal_size()[0]:
					terminalsize = os.get_terminal_size()[0]
					bar.refresh()
					os.system("cls")
					if (cores == 1):
						print("Starting..")
						print("Appling...")
						print("Ctrl+C to stop")
				elif os.get_terminal_size()[0] != terminalsize:
					terminalsize = os.get_terminal_size()[0]
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
