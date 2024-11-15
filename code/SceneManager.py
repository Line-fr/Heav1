from DependencyCheck import *
from ssimu2 import *

class Scene:
	sceneTempIndex = 0
	def __init__(self):
		self.file = os.path.join("temp", f"scene{Scene.sceneTempIndex}.json")
		if os.path.isfile(self.file):
			print("warning: rewriting over an existing scene.json file")
			os.remove(self.file)
		self.videosource = "None"
		Scene.sceneTempIndex += 1

	def compute(self, videosource : str, downscale : int = 720) -> None:
		self.videosource = videosource
		check_output(f'av1an -i "{videosource}" --sc-only -s {self.file} --sc-downscale-height {downscale}', shell = True, env=os.environ.copy() )

	def decodeJson(self):
		with open(self.file) as file:
			c = file.read().replace("null", "0")
		return json.loads(c)

	def clean(self) -> None:
		scenes = self.decodeJson()
		for sceneind in range(len(scenes["scenes"])):
			scenes["scenes"][sceneind]["zone_overrides"] = "null"
		res = json.dumps(scenes)
		res = res.replace('"null"', "null")
		with open(self.file, "w") as file:
			file.write(res)

	def numberOfScenes(self):
		j = self.decodeJson()
		return len(j["scenes"])

	def cutSSIMU2byScene(self, ssimu2:SSIMU2Score): #each scene has a list of scores
		scoreind = 0
		res = []
		scores = ssimu2.scores
		scenes = self.decodeJson()
		for scene in scenes["scenes"]:
			res.append([])
			while (scoreind < len(scores) and scores[scoreind][0] < scene["end_frame"]):
				if (scores[scoreind][0] >= scene["start_frame"]):
					res[-1].append(scores[scoreind][1])
				else:
					print("there s an error somewhere in scenes or in scores")
				scoreind += 1
		return res

	def writeJson(self, data):
		res = json.dumps(data)
		with open(self.file, "w") as file:
			file.write(res)

	def __repr__(self) -> str:
		return f"<Scene object of {self.videosource}>"

	def __del__(self):
		if False and os.path.isfile(self.file):
			os.remove(self.file)

allscenes = {}
def getscene(source:str):
	#this function allows automatic managment of scene detection when needed throughout the run
	if source in allscenes:
		return allscenes[source]
	else:
		allscenes[source] = Scene()
		allscenes[source].compute(source)
		return allscenes[source]