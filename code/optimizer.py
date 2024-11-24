from DependencyCheck import *

def optimizer(previous_data, target_quality, average_bitrate = 10000, quality_flexibility = 8, alpha = 0.5, strict = True):
    b = average_bitrate/2

    if (len(previous_data) == 1): 
        previous_data = previous_data + [(70, 1, -30)]
    else:
        ssimu2list = [el[2] for el in previous_data]
        sizelist = [el[1] for el in previous_data]
        avgssimu2 = sum(ssimu2list)/len(ssimu2list)
        avgsize = sum(sizelist)/len(sizelist)
        stddevssimu2 = math.sqrt(sum([el*el for el in ssimu2list]) - avgssimu2**2)
        stddevsize = math.sqrt(sum([el*el for el in sizelist]) - avgsize**2)
        if (stddevssimu2 <= 10 and avgssimu2 >= target_quality):
            return (60, 0, 0)
        elif (stddevsize <= 10):
            return (60, 0, 0)

    crfs = [el[0] for el in previous_data]
    ssimu2s = [el[2] for el in previous_data]
    sizes = [el[1] for el in previous_data]

    ssimu2_crf = np.poly1d(np.polyfit(crfs, np.array(ssimu2s), len(ssimu2s)-1))
    size_crf = np.poly1d(np.polyfit(crfs, np.log(np.array(sizes)), len(ssimu2s) - 1))

    if not strict:
        to_minimize = lambda crf : alpha * np.exp(size_crf(crf)) + (1 - alpha) * b * np.exp( (target_quality - ssimu2_crf(crf)) / quality_flexibility )
    else:
        to_minimize = lambda crf : alpha * np.exp(size_crf(crf)) + (1 - alpha) * b * np.exp( abs(target_quality - ssimu2_crf(crf)) / quality_flexibility )

    try:
        mincrf = max(10, min(60, scipy.optimize.minimize_scalar(to_minimize).x))
    except:
        x = [i/10 for i in range(0, 700)]
        y = [to_minimize(el) for el in x]
        pyplot.plot(x, y)
        pyplot.show()
        print(previous_data, target_quality, average_bitrate)
        exit(1)

    return (float(mincrf), float(ssimu2_crf(mincrf)), float(np.exp(size_crf(mincrf))))

#print(optimizer([ (40, 5000, 60), (30, 12000, 73) ], 70, 10000, quality_flexibility=3, alpha = 0.3))