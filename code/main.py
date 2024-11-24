from DependencyCheck import *
from SceneManager import *
from ssimu2 import *
from encode import *

reference = r"C:\Users\leofr\Desktop\Nav1\code\src.mp4"
encoded = r"C:\Users\leofr\Desktop\Nav1\code\des.mkv"
ou = "resheav1.mkv"

#sc = Heav1_precompute(reference)
#Heav1_encode(ou, reference, sc)
score = SSIMU2Score()
score.compute(reference, "resNB.mkv")
print(score)
score.compute(reference, ou)
print(score)