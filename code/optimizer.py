from DependencyCheck import *

def optimizer(previous_data, target_quality, b_val = 10000, quality_flexibility = 3, alpha = 0.5):
    b = b_val/2

    if (len(previous_data) == 1): previous_data.append((70, b_val/30, 20))

    crfs = [el[0] for el in previous_data]
    ssimu2s = [el[2] for el in previous_data]
    sizes = [el[1] for el in previous_data]

    ssimu2_crf = np.poly1d(np.polyfit(crfs, np.array(ssimu2s), len(ssimu2s)-1))
    size_crf = np.poly1d(np.polyfit(crfs, np.log(np.array(sizes)), len(ssimu2s) - 1))

    to_minimize = lambda crf : alpha * np.exp(size_crf(crf)) + (1 - alpha) * b * np.exp( (target_quality - ssimu2_crf(crf)) / quality_flexibility )

    mincrf = scipy.optimize.minimize_scalar(to_minimize, (0, 30, 70)).x

    return (float(mincrf), float(ssimu2_crf(mincrf)), float(np.exp(size_crf(mincrf))))

print(optimizer([ (40, 5000, 60), (30, 12000, 73) ], 70, 10000))