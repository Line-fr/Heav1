from DependencyCheck import *

class SSIMU2Score:
    def __init__(self):
        self.scores = []
        self.source = "None"
        self.distorded = "None"

    def compute(self, originalFile : str, distordedFile : str, skip : int = 5, begin : int = 0, end : int = None) -> None:
        src = vs.core.bs.VideoSource(originalFile, threads=24)[begin:end:skip]
        dis = vs.core.bs.VideoSource(distordedFile, threads=24)[begin:end:skip]
			
        #src = src.resize.Bicubic(height=dis.height, width=dis.width, format=vs.RGBS, matrix_in_s="709", transfer_in_s="srgb", transfer_s="linear")
        #dis = dis.resize.Bicubic(format=vs.RGBS, matrix_in_s="709", transfer_in_s="srgb", transfer_s="linear")

        result = src.vszip.Metrics(dis, mode = 0)
        res = [[begin + ind*skip, fr.props["_SSIMULACRA2"]] for (ind, fr) in enumerate(result.frames())]
        res = [k for k in res if k[1] > 0]
        self.scores = res
        self.source = originalFile
        self.distorded = distordedFile

    def statistics(self) -> tuple[int, int, int, int, int]:
		#returns (avg, deviation, median, 5th percentile, 95th percentile)
        intlist = [k[1] for k in self.scores]
        avg = sum(intlist)/len(intlist)
        deviation = ((sum([k*k for k in intlist])/len(intlist)) - avg*avg)**0.5
        sortedlist = sorted(intlist)
        return (avg, deviation, sortedlist[len(intlist)//2], sortedlist[len(intlist)//20], sortedlist[19*len(intlist)//20])

    def __repr__(self):
        stats = self.statistics()
        res = f"SSIMU2 for files {self.source} and {self.distorded}\n"
        res += f"Mean : {stats[0]}\n"
        res += f"Standard deviation : {stats[1]}\n"
        res += f"Median : {stats[2]}\n"
        res += f"5th percentile : {stats[3]}\n"
        res += f"95th percentile : {stats[4]}\n"
        return res

    def save(self, savefile : str) -> None:
    	with open(savefile, "w") as file:
            json.dump([self.scores, self.source, self.distorded], file) 
			
    def load(self, savefile : str) -> None:
        with open(savefile, "r") as file:
            res = json.load(file)
        self.scores = res[0]
        self.source = res[1]
        self.distorded = res[2] 
			
    def histogram(self):
        x = [k*0.5 for k in range(201)]
        y = [0 for k in x]
        for score1 in self.scores:
            score = score1[1]
            if score >= 0 and score <= 100:
                y[int(score*2)] += 1
        pyplot.plot(x, y)
        pyplot.show()