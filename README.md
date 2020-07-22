- dependents
	- python 3.x x64
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
	
	
# perfomance
ram usage 10-30MB per core  
16.5GB of data: 28000 png Images (1280x720) to size = 200 (200x112) 
  
i7-4770 (8 threads) with background cpu ~10-20%  
| Cores |  Time |  it/s |
|:-----:|:-----:|:-----:|
|   1   | 38:30 | 12.12 |
|   2   | 20:25 | 22.85 |
|   4   | 11:09 | 41.79 |
|   8   | 08:26 | 55.23 |
|   16  | 08:23 | 55.56 |
	
	



