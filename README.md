- dependents
	- python 3.x
	- pip => requirements.txt

- run
	- copy img.py and core.py in working directory
	- edit setting in img.py
	- run img.py

# settings

	size      -> rect size to fit image in
	upscale   -> upscale image IF smaller than [size]
	downscale -> downscale image IF bigger than [size]
	copy_ud   -> copy IF image are NOT downscaled and/or upscaled

	path      -> catalog with you images
	path_out  -> save path
	overwrite -> overwrite if image exist in [path_out]
	file_extensions = [".png", ".jpg", ".jpeg"] -> tested only on ".png", ".jpg", ".jpeg"

	prefix -> prefix for output filename
	suffix -> suffix for output filename

	quality  ->  0-100 quality for jpg
	cores    ->  Number of streams :)

	# For multicore only
	minimized      ->  Start window minimized has priority over maximized
	maximized      ->  Start window maximized
	priority_class ->  "LOW" | "BELOWNORMAL" | "NORMAL" | "ABOVENORMAL" | "HIGH" | "REALTIME"



