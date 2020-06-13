#image_thumbler	

- dependents
	- python 3.x
	- pip => requirements.txt

- run
	- edit setting in img.py
	- run img.py

# settings

	size     -> #rect size to fit image in
	path     -> catalog with you images
	path_out -> save path
	prefix   -> prefix for output filename
	suffix   -> suffix for output filename
	quality  ->  0-100 quality for jpg
	cores    ->  Number of streams :)

	# For multicore only
	minimized      ->  Start window minimized has priority over maximized
	maximized      ->  Start window maximized
	priority_class ->  "LOW" | "BELOWNORMAL" | "NORMAL" | "ABOVENORMAL" | "HIGH" | "REALTIME"
