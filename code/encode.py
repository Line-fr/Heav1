from DependencyCheck import *
from SceneManager import *

class SVTParameters:
	def __init__(self, preset:int = 6, crf:int = 30, threads:int = 4, lookahead:int = 60, film_grain:int = 0, film_grain_denoise:int = 0, tune:int = 3, variance_octile:int = 6, variance_boost:int = 2):
		self.preset = preset
		self.crf = crf
		self.threads = threads
		self.lookahead = lookahead
		self.film_grain = film_grain
		self.film_grain_denoise = film_grain_denoise
		self.tune = tune
		self.variance_octile = variance_octile
		self.variance_boost = variance_boost

	def __str__(self) -> str:
		return f'--preset {self.preset} --crf {self.crf} --keyint 240 --lp {self.threads} --film-grain {self.film_grain} --film-grain-denoise {self.film_grain_denoise} --color-primaries 1 --transfer-characteristics 1 --matrix-coefficients 1 --color-range 0 --irefresh-type 2 --aq-mode 2 --enable-overlays 1 --scd 0 --lookahead {self.lookahead} --tune {self.tune} --variance-boost-strength {self.variance_boost} --variance-octile {self.variance_octile}'

	def zoning_override(self):
		return {"encoder": "svt_av1", "passes": 1, "min_scene_len" : 8, "video_params": ["--preset", str(self.preset), "--crf", str(self.crf), "--film-grain", str(self.film_grain), "--film-grain-denoise", str(self.film_grain_denoise), "--lookahead", str(self.lookahead), "--lp", str(self.threads)]}

	def copy(self):
		ret = SVTParameters()
		ret.preset = self.preset
		ret.crf = self.crf
		ret.threads = self.threads
		ret.lookahead = self.lookahead
		ret.film_grain = self.film_grain
		ret.film_grain_denoise = self.film_grain_denoise
		return ret

class AOMParameters:
	def __init__(self, preset:int = 4, crf:int = 30, threads:int = 2, tune_content:str = "psy", tune:str = "ssim", aq_mode:int = 1, enable_qm:int = 1, lag_in_frame:int = 96):
		self.preset = preset
		self.crf = crf
		self.threads = threads
		self.tune_content = tune_content
		self.tune = tune
		self.aq_mode = aq_mode
		self.enable_qm = enable_qm
		self.lag_in_frame = lag_in_frame

	def __str__(self) -> str:
		return f"--end-usage=q --cq-level={self.crf} --cpu-used={self.preset} --disable-kf --kf-min-dist=12 --kf-max-dist=240 --enable-dnl-denoising=0 --denoise-noise-level=0 --threads={self.threads} --tile-columns=1 --tile-rows=0 --enable-keyframe-filtering=2 --aq-mode={self.aq_mode} --tune-content={self.tune_content} --tune={self.tune} --enable-qm={self.enable_qm} --lag-in-frames={self.lag_in_frame}"

	def zoning_override(self):
		return {"encoder": "aom", "passes": 2, "min_scene_len": 8, "video_params": ["--end-usage=q", f"--cq-level={self.crf}", f"--cpu-used={self.preset}", f"--disable-kf", f"--kf-min-dist=12", f"--kf-max-dist=240", f"--enable-dnl-denoising=0", f"--denoise-noise-level=0", f"--threads={self.threads}", f"--tile-columns=1", f"--tile-rows=0", f"--enable-keyframe-filtering=2", f"--aq-mode={self.aq_mode}", f"--tune-content={self.tune_content}", f"--tune={self.tune}", f"--enable-qm={self.enable_qm}", f"--lag-in-frames={self.lag_in_frame}"]}

	def copy(self):
		ret = AOMParameters()
		ret.preset = self.preset
		ret.crf = self.crf
		ret.threads = self.threads
		ret.tune_content = self.tune_content
		ret.tune = self.tune
		ret.aq_mode = self.aq_mode
		ret.enable_qm = self.enable_qm
		ret.lag_in_frame = self.lag_in_frame
		return ret

class AV1ANParameters:
	def __init__(self, encoder:str = "svt-av1", svtparam:SVTParameters = SVTParameters(), aomparam:AOMParameters = AOMParameters(), workers:int = 6, rescale:(int, int) = None, audio_bitrate:int = 128, discard_audio:bool = False, keep:bool = False, tempdir:str = None):
		#encoder between: "svt-av1" and "aom"
		assert encoder == "svt-av1" or encoder == "aom"
		self.encoder = encoder
		self.svtparam = svtparam
		self.aomparam = aomparam
		self.workers = workers
		self.rescale = rescale
		self.audio_bitrate = audio_bitrate
		self.keep = keep
		self.an = discard_audio
		self.tempdir = tempdir

	def __str__(self) -> str:
		encoder_param = None
		if self.encoder == "svt-av1":
			encoder_param = str(self.svtparam)
		elif self.encoder == "aom":
			encoder_param = str(self.aomparam)

		if self.rescale == None:
			rescale = ""
		else:
			rescale = f'-f "-vf scale={str(self.rescale[0])+":"+str(self.rescale[1])},setsar=1:1"' 
		if self.keep:
			keepstr = " --keep"
		else:
			keepstr = " "
		if self.tempdir != None:
			tempdir = " --temp "+self.tempdir
		else:
			tempdir = " "
		if self.an:
			audstr = '"-an"'
		else:
			audstr = f'"-c:a libopus -ac:a 2 -b:a {self.audio_bitrate}k"'
		return f'-y{keepstr}{tempdir} --verbose -c mkvmerge --set-thread-affinity {self.svtparam.threads} --chunk-order long-to-short -e {self.encoder} -v="{encoder_param}" --pix-format yuv420p10le {rescale} -a {audstr} -w {self.workers}'

	def copy(self):
		ret = AV1ANParameters()
		ret.encoder = self.encoder
		ret.svtparam = self.svtparam.copy()
		ret.aomparam = self.aomparam.copy()
		ret.workers = self.workers
		ret.rescale = self.rescale
		ret.audio_bitrate = self.audio_bitrate
		return ret

class EncodeFile: #allows more precise encoding manipulations
    EncodeFileTempIndex = 0
    def __init__(self, inputfile:str):
        self.inputfile = inputfile

        EncodeFile.EncodeFileTempIndex += 1

    def __str__(self):
        return self.inputfile
	
    def __repr__(self):
        return self.inputfile

    def encode(self, outputfile:str, av1anparam:AV1ANParameters = AV1ANParameters(), scenefile:Scene = None):
        if scenefile == None:
            scene_arg = ""
        else:
            scene_arg = f"-s {scenefile.file}"

        try:
            check_output(f"av1an -i \"{self.inputfile}\" {scene_arg} {str(av1anparam)} -o \"{outputfile}\"", shell = True)
        except Exception as e:
            print("Error occured while encoding in av1an, skipping it... ", e)

def convertAudioWithOpusenc(inputfile:str, outputfile:str, audio_bitrate:int = 128, stereo:bool = True, deletesource:bool = False):
	if os.path.isfile(os.path.join('temp', os.path.basename(inputfile)+'.flac')): os.remove (os.path.join('temp', os.path.basename(inputfile)+'.flac'))
	call(f"ffmpeg -i {inputfile} -c:a flac{[' -ac 2', ' '][1-int(stereo)]} {os.path.join('temp', os.path.basename(inputfile)+'.flac')}", stderr=DEVNULL)
	if deletesource: os.remove(inputfile)
	call(f"opusenc --bitrate {audio_bitrate} --comp 10 {os.path.join('temp', os.path.basename(inputfile)+'.flac')} {outputfile}", stderr=DEVNULL)
	os.remove(f"{os.path.join('temp', os.path.basename(inputfile)+'.flac')}")

def encode(outputfile:str, inputfile:str, av1anparam:AV1ANParameters = AV1ANParameters(), use_opus_enc:bool = True):
	if use_opus_enc:
		sourcefile = MKVFile(inputfile)
		numaudio = 0
		to_delete = []
		metadata = []
		for track in sourcefile.get_track():
			if track.track_type == "audio":
				#intercepting the audio !
				audiofile = MKVFile()
				audiofile.add_track(track)
				if os.path.isfile(os.path.join("temp", f"audiotemp{numaudio}.mka")): os.remove(os.path.join("temp", f"audiotemp{numaudio}.mka"))
				audiofile.mux(os.path.join("temp", f"audiotemp{numaudio}.mka"))
				metadata.append([track.track_name, track.default_track, track.forced_track, track.language])
				to_delete.append(track.track_id)
				numaudio += 1
		print("encoding to opus...")
		for i in range(numaudio):
			if os.path.isfile(os.path.join("temp", f"audiotemp{i}.opus")): os.remove(os.path.join("temp", f"audiotemp{i}.opus"))
			convertAudioWithOpusenc(os.path.join("temp", f"audiotemp{i}.mka"), os.path.join("temp", f"audiotemp{i}.opus"), audio_bitrate = av1anparam.audio_bitrate, deletesource=True, stereo=True)
		tempoutput = os.path.join('temp', 'encodedvideo.mkv')
	else:
		tempoutput = outputfile

	#compute scene if needed
	sc = getscene(inputfile)
	scene_arg = f"-s {sc.file}"

	try:
		check_output(f"av1an -i \"{inputfile}\" {scene_arg} {str(av1anparam)} -o \"{tempoutput}\"", shell = True)
	except Exception as e:
		print("Error occured while encoding in av1an, skipping it... ", e)

	if use_opus_enc:
		finalFile = MKVFile(os.path.join("temp", "encodedvideo.mkv"))
		for i in to_delete[-1::-1]:
			finalFile.remove_track(i)
		for i in range(numaudio):
			nt = MKVTrack(os.path.join("temp", f"audiotemp{i}.opus"))
			nt.track_name = metadata[i][0]
			nt.default_track = metadata[i][1]
			nt.forced_track = metadata[i][2]
			if metadata[i][3] != None: nt.language = metadata[i][3]
			finalFile.add_track(nt)
		finalFile.mux(outputfile)
		for i in range(numaudio):
			os.remove(os.path.join("temp", f"audiotemp{i}.opus"))
		os.remove(os.path.join("temp", "encodedvideo.mkv"))