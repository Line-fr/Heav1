from DependencyCheck import *
from SceneManager import *
from ssimu2 import *
from encode import *

reference = r"C:\Users\leofr\Desktop\Nav1\code\src.mp4"
encoded = r"C:\Users\leofr\Desktop\Nav1\code\des.mkv"
d = "testing source"

data = {}

for ft in os.listdir(d):
    if (ft[-7:] == "bsindex"): continue
    fs = os.path.join(d, ft)
    scene = Scene()
    scene.compute(fs)
    data[ft] = {}
    for sampling_strength in samplings:
        data[ft][sampling_strength] = []
        newscene = Scene()
        newscene.writeJson(scene.decodeJson())
        samples = newscene.sample_scene_encode(sampling_strength, endmiddle= False)

        sample_old_location = [el[0]+el[2]//2 for el in samples]
        sample_new_location = [el[1]+el[2]//2 for el in samples]

        print("sampling done, resulting in", newscene.decodeJson()['frames'], " total frames")

        init = time.time()
        f = EncodeFile(fs)
        resname = f"samplingtest\\{ft}_{sampling_strength}.mkv"
        f.encode(resname, av1anparam=AV1ANParameters(svtparam=SVTParameters(preset=4, crf=36), workers = 6, discard_audio=True), scenefile=newscene)
        print("encoded")

        score = SSIMU2Score()
        score.compute_unmatched_frames(fs, resname, sample_old_location, sample_new_location)
        data[ft][sampling_strength].append(time.time()-init)
        score.save(resname[:-4]+".json")