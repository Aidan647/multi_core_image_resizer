
# ----------config-----------------

size = 200       #rect size to fit image in
upscale = True   #upscale image IF smaller than [size]
downscale = True #downscale image IF bigger than [size]
copy_ud = True   #copy IF image are NOT downscaled and/or upscaled



path = "./VoiceSquad/"      #catalog with you images
path_out = "./out/" #save path
overwrite = True   #overwrite if image exist in [path_out]
file_extensions = [".png", ".jpg", ".jpeg"] # tested only on ".png", ".jpg", ".jpeg"

prefix = "" #prefix for output filename
suffix = "" #suffix for output filename

quality = 70 # 0-100 quality for jpg
cores = 20    # Number of streams :)


# For multicore only
minimized = True  # Start window minimized has priority over maximized
maximized = False # Start window maximized
priority_class = "" # "LOW" | "BELOWNORMAL" | "NORMAL" | "ABOVENORMAL" | "HIGH" | "REALTIME"



# Other
TDprefix = "img_tmp_" # Temporary directory prefix
# ---------------------------------



import os
import sys
import shutil
import json
from tqdm import tqdm, trange
# import glob
from time import sleep
from tempfile import TemporaryDirectory



images = []
os.system("cls")

def Get_JSON(lis):
	return json.JSONEncoder().encode(lis)


def get_tree(path, pathT):
	list_ = os.listdir(path)
	bar = tqdm(list_, leave=False, ascii=True, dynamic_ncols=True)
	for i in bar:
		if bar.total < 100:
			bar.set_description(i)
		else:
			bar.set_description(i, refresh=False)
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
def get_progress(TD,cores,cors):
	progress = 0
	for i in range(cores):
		if (os.path.isfile(f"{TD}/core{i}.progress")):
			try:
				shutil.copyfile(f"{TD}/core{i}.progress", f"{TD}/core{i}.progress2")
				f = open(f"{TD}/core{i}.progress2", "r")
				progress += int(f.read())
				cors[i] = int(f.read())
			except ValueError:
				progress += cors[i]
			f.close()
	return progress

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
		if cores != 1:
			tqdm_p = tqdm(total=len(images), ascii=True, desc="Progress", dynamic_ncols=True, bar_format="{desc}: {percentage:3.0f}%|{bar}{r_bar}")
		if cores > 1:
			for i in trange(cores, leave=False, ascii=True, dynamic_ncols=True, desc="Starting cores", bar_format="{l_bar}{bar}|"):
				sleep(0.2)
				shutil.copyfile(f"{os.path.dirname(os.path.abspath(__file__))}/core.py", f"{TD.name}/core{i}.py")
				files.append(f"{TD.name}/core{i}.data")
				f = open(f"{TD.name}/core{i}.py", "a")
				f.write(f"\nstart(int({i}), int({size}), int({quality}),r'{os.path.dirname(os.path.abspath(__file__))}',r'{TD.name}',r'{prefix}',r'{suffix}',{upscale},{downscale},{copy_ud},{cores})")
				f.close()
				PC = ""
				MIN = ""
				MAX = ""
				if priority_class != "": PC = f"/{priority_class}"
				if minimized: MIN = "/MIN"
				if maximized: MAX = "/MAX"
				os.system(f'start "core {i}" {PC} {MAX} {MIN} cmd /C "cd /d {TD.name} & py core{i}.py')
				progress = get_progress(TD.name,cores,cors)
				tqdm_p.n = progress
				tqdm_p.refresh()
		else:
			import core
			core.start(0, size, quality,"./",TD.name,prefix,suffix,upscale,downscale,copy_ud,cores)
		done = False
		terminalsize = 100**10
		while done == False:
			sleep(0.1)
			d = True
			if cores != 1:
				tqdm_p.desc = ""
				if os.get_terminal_size()[0] < terminalsize or tqdm_p.ncols+1 > os.get_terminal_size()[0]:
					terminalsize = os.get_terminal_size()[0]
					# tqdm_p.ncols = os.get_terminal_size()[0]
					tqdm_p.refresh()
					os.system("cls")
					print("Starting..")
					print("Appling...")
					print("Ctrl+C to stop")
				elif os.get_terminal_size()[0] != terminalsize:
					terminalsize = os.get_terminal_size()[0]
					# tqdm_p.ncols
					
				# tqdm_p.ncols = os.get_terminal_size()[0]
				tqdm_p.n = get_progress(TD.name,cores,cors)
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
except KeyboardInterrupt as E:
	try:
		log = open("./core.log", "a")
		log.write("\n"+"-"*100+"\n")
		for x in range(cores):
			try:
				f = open(f"{TD.name}/core{x}.log", "r")
				log.write(f'\n{"-"*10}{x}{"-"*10}')
				log.write(f.read())
				f.close()
			except:
				pass
		log.close()
	except:
		pass
except Exception as E:
	try:
		log = open("./core.log", "a")
		log.write("\n"+"-"*100+"\n")
		for x in range(cores):
			try:
				f = open(f"{TD.name}/core{x}.log", "r")
				log.write(f'\n{"-"*10}{x}{"-"*10}')
				log.write(f.read())
				f.close()
			except:
				pass
		log.close()
	except:
		pass
	print(f"ERROR (sector 1):{E}")
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