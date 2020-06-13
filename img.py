
# ----------config-----------------

size = 150
path = "./data/129/"
path_out = "./x/"

prefix = ""
suffix = ""

quality = 70  # 0-100
cores = 2

minimized = True # Start window minimized has priority over maximized
maximized = False # Start window maximized

priority_class = "" # For multicore only || "LOW" | "BELOWNORMAL" | "NORMAL" | "ABOVENORMAL" | "HIGH" | "REALTIME"

# ---------------------------------



import os
import sys
import shutil
import json
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
		elif os.path.isfile(c_path) and (os.path.splitext(c_path)[1] == ".png" or os.path.splitext(c_path)[1] == ".jpg" or os.path.splitext(c_path)[1] == ".jpeg"):
			paths, file = os.path.split(c_path)
			filename, ext = os.path.splitext(file)
			images.insert(0, (paths+"/",os.path.split(c_pathT)[0]+"/", file, filename, ext))

print("Starting..")
TD = TemporaryDirectory(prefix="img_tmp_")
try:
	shutil.copytree(path, TD.name+path)
	get_tree(path, path_out)
	j = 0
	list_json = []
	for x in range(cores):
		list_json.append([])
	for i in images:
		list_json[j % cores].append(list(i))
		j += 1
	print("Appling...")
	file1 = open(f"{TD.name}/data.json", "w+")
	file1.write(Get_JSON(list_json))
	file1.close()
	files = []
	for i in range(cores):
		shutil.copyfile(f"{os.path.dirname(os.path.abspath(__file__))}/core.py", f"{TD.name}/core{i}.py")
		files.append(f"{TD.name}/core{i}.data")
		f = open(f"{TD.name}/core{i}.py", "a")
		f.write(f"\nstart(int({i}), int({size}), int({quality}),r'{os.path.dirname(os.path.abspath(__file__))}',r'{TD.name}',r'{prefix}',r'{suffix}')")
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
			os.system(f"{TD.name}\\core{i}.py")
	done = False
	while done == False:
		sleep(1)
		d = True
		for f in files:
			if d == True:
				d = os.path.isfile(f)
		done = d
	log = open("./core.log", "a")
	log.write("\n"+"-"*100+"\n")
	for x in range(cores):
		f = open(f"{TD.name}/core{x}.log", "r")
		log.write(f'\n{"-"*10}{x}{"-"*10}')
		log.write(f.read())
		f.close()
	log.close()

	print("Done")
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
	print(f"ERROR:{E}")
TD.cleanup()
try:
	print("CTRL+C to exit")
	sleep(100)
except:
	pass	