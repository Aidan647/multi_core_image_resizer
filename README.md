#image_thumbler	

- dependents
  - python 3.x

- install
	- copy file img.py and core.py in your directory
- run
	- edit setting in img.py
	- run img.py
# settings
	```py
		size = 150 
		path = "./data/129/" #catalog with you image(recursive)
		path_out = "./x/"    #out catalog(save path)

		prefix = ""  #prefix for image name
		suffix = "" #suffix for image name

		quality = 70  # 0-100
		cores = 2  # COUNT STREAM FOR RUN THIS SCRIPT :)

		minimized = True # Start window minimized has priority over maximized
		maximized = False # Start window maximized

		priority_class = "" # For multicore only || "LOW" | "BELOWNORMAL" | "NORMAL" | "ABOVENORMAL" | "HIGH" | "REALTIME"
	```
