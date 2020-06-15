
# ----------config-----------------

size = 200       #rect size to fit image in
upscale = True   #upscale image IF smaller than [size]
downscale = True #downscale image IF bigger than [size]
copy_ud = True   #copy IF image are NOT downscaled and/or upscaled



path = "./in/"      #catalog with you images
path_out = "./out/" #save path
overwrite = True   #overwrite if image exist in [path_out]
file_extensions = [".png", ".jpg", ".jpeg"] # tested only on ".png", ".jpg", ".jpeg"

prefix = "" #prefix for output filename
suffix = "" #suffix for output filename

quality = 70 # 0-100 quality for jpg
cores = 1    # Number of streams :)


# For multicore only
minimized = True  # Start window minimized has priority over maximized
maximized = False # Start window maximized
priority_class = "" # "LOW" | "BELOWNORMAL" | "NORMAL" | "ABOVENORMAL" | "HIGH" | "REALTIME"

# ---------------------------------



import os
import sys
import shutil
import json
from tqdm import tqdm
# import glob
from time import sleep
from tempfile import TemporaryDirectory
import PIL



images = []
os.system("cls")

def Get_JSON(lis):
	return json.JSONEncoder().encode(lis)



def get_tree(path, pathT):
	list_ = os.listdir(path)
	for i in list_:
		c_path = path + i
		c_pathT = pathT + i
		if os.path.isdir(c_path + "/"):
			get_tree(c_path + "/", c_pathT + "/")
		# elif os.path.isfile(c_path) and (os.path.splitext(c_path)[1] == ".png" or os.path.splitext(c_path)[1] == ".jpg" or os.path.splitext(c_path)[1] == ".jpeg"):
		elif os.path.isfile(c_path) and os.path.splitext(c_path)[1] in file_extensions:
			paths, file = os.path.split(c_path)
			filename, ext = os.path.splitext(file)
			if not os.path.exists(f"{os.path.split(c_pathT)[0]}/{prefix}{filename}{suffix}{ext}") or overwrite:
				images.insert(0, (paths+"/",os.path.split(c_pathT)[0]+"/", file, filename, ext))

print("Starting..")
TD = TemporaryDirectory(prefix="img_tmp_")
try:
	get_tree(path, path_out)
	j = 0
	list_json = []
	cors = []
	if len(images) != 0:
		for x in range(cores):
			list_json.append([])
			cors.append(0)
		for i in images:
			list_json[j % cores].append(list(i))
			j += 1
		print("Appling...")
		print("Ctrl+C to stop")
		file1 = open(f"{TD.name}/data.json", "w+")
		file1.write(Get_JSON(list_json))
		file1.close()
		files = []
		if cores > 1:
			for i in range(cores):
				shutil.copyfile(f"{os.path.dirname(os.path.abspath(__file__))}/core.py", f"{TD.name}/core{i}.py")
				files.append(f"{TD.name}/core{i}.data")
				f = open(f"{TD.name}/core{i}.py", "a")
				f.write(f"\nstart(int({i}), int({size}), int({quality}),r'{os.path.dirname(os.path.abspath(__file__))}',r'{TD.name}',r'{prefix}',r'{suffix}',{upscale},{downscale},{copy_ud},{cores})")
				f.close()
				if cores != 1:
					# os.startfile(f"{TD.name}\\core{i}.py")
					PC = ""
					MIN = ""
					MAX = ""
					if priority_class != "": PC = f"/{priority_class}"
					if minimized: MIN = "/MIN"
					if maximized: MAX = "/MAX"
					os.system(f'start "core {i}" {PC} {MAX} {MIN} cmd /C "cd /d {TD.name} & py core{i}.py')
		else:
			import core
			core.start(0, size, quality,"./",TD.name,prefix,suffix,upscale,downscale,copy_ud,cores)
		done = False
		if cores != 1:
			tqdm_p = tqdm(total=len(images), ascii=True, dynamic_ncols=True)
		while done == False:
			sleep(0.1)
			d = True
			if cores != 1:
				progress = 0
				for i in range(cores):
					if (os.path.isfile(f"{TD.name}/core{i}.progress")):
						shutil.copyfile(f"{TD.name}/core{i}.progress", f"{TD.name}/core{i}.progress2")
						f = open(f"{TD.name}/core{i}.progress2", "r")
						try:
							progress += int(f.read())
							cors[i] = int(f.read())
						except ValueError:
							progress += cors[i] or 0
						f.close()
				tqdm_p.n = progress
				tqdm_p.refresh()
					
			for f in files:
				if d == True:
					d = os.path.isfile(f)
			done = d
		if cores != 1:
			tqdm_p.n = len(images)
			tqdm_p.refresh()
			tqdm_p.close()
		log = open("./core.log", "a")
		log.write("\n"+"-"*100+"\n")
		for x in range(cores):
			f = open(f"{TD.name}/core{x}.log", "r")
			log.write(f'\n{"-"*10}{x}{"-"*10}')
			log.write(f.read())
			f.close()
		log.close()
		print("Done")
	else:
		print("Images not found")
except Exception as E:
	try:
		log = open("./core.log", "a")
		log.write("\n"+"-"*100+"\n")
		for x in range(cores):
			f = open(f"{TD.name}/core{x}.log", "r")
			log.write(f'\n{"-"*10}{x}{"-"*10}')
			log.write(f.read())
			f.close()
		log.close()
	except:
		pass
	print(f"ERROR (sector 1):{E}")
except KeyboardInterrupt as E:
	pass
finally:
	try:
		open(f"{TD.name}/stop.all", "w")
		TD.cleanup()
	except Exception as E:
		print(f"ERROR (sector 2):{E}")
	try:
		print("CTRL+C to exit")
		sleep(100)
	except KeyboardInterrupt:
		pass