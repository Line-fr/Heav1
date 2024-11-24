#dependency analyzer
from sys import exit
from subprocess import check_output, call, Popen, DEVNULL
import os
import json
import shutil
import copy
import time
import math
import shutil
try:
	from matplotlib import pyplot
except:
	print("warning: matplotlib is not installed, running pip install matplotlib")
	check_output("pip install matplotlib", stderr = DEVNULL)
	try:
		from matplotlib import pyplot
	except:
		print("fails to install matplotlib")
		exit(1)
try:
	import numpy as np
except:
	print("warning: numpy is not installed, running pip install numpy")
	check_output("pip install numpy", stderr = DEVNULL)
	try:
		import numpy as np
	except:
		print("fails to install numpy")
		exit(1)
try:
	import scipy
except:
	print("warning: scipy is not installed, running pip install scipy")
	check_output("pip install scipy", stderr = DEVNULL)
	try:
		import scipy
	except:
		print("fails to install scipy")
		exit(1)
from multiprocessing import Pool
import time
try:
	import ffmpeg
except:
	print("warning: ffmpeg-python not installed properly, running pip install ffmpeg-python")
	check_output("pip install ffmpeg-python", stderr = DEVNULL)
	try:
		import ffmpeg
	except:
		print("fails to install ffmpeg-python")
		exit(1)

try:
	from pymkv import MKVFile, MKVTrack
except:
	print("warning: pymkv not installed properly, running pip install pymkv")
	check_output("pip install pymkv", stderr = DEVNULL)
	try:
		from pymkv import MKVFile, MKVTrack
	except:
		print("fails to install pymkv")

#vapoursynth dependency checks will not be able to solve anything but only signal problems for now
try:
	import vapoursynth as vs
except:
	print("You need to install vapoursynth...")
	exit(1)

if not "bs" in dir(vs.core):
	print("You must install BestSource to use the script")
	exit(1)
if not "vszip" in dir(vs.core):
	print("you must install vszip by julek to use this script because it allows to compute ssimu2")
	exit(1)
#if not "fmtc" in dir(vs.core):
#	print("You must install fmtc for conversions")
#	exit(1)

try:
	check_output("ffmpeg -h", stderr = DEVNULL)
except Exception as e:
	print("ffmpeg is not installed properly : ", e)

try:
	check_output("av1an -h", stderr = DEVNULL)
except Exception as e:
	print("av1an is not installed properly : ", e)

os.chdir(os.path.dirname(os.path.realpath(__file__)))
if not os.path.isdir("temp"): os.mkdir("temp")

print("dependency check passed")