import librosa
import math

def round_up(n, decimals=0):
    multiplier = 10**decimals

    return math.ceil(n * multiplier) / multiplier


def btonset(samples, peakpos):
    peakval = samples[peakpos]
    ind = peakpos

    while True:
        if ind == 0:
            break

        cur = samples[ind]
        prev = samples[ind - 10]

        if cur < 0.001*peakval or prev == 0.0:
            break

        ind -= 10

    return ind


def RMS(samples):
    sqsum = 0
    N = len(samples)

    for s in samples:
        sqsum += s**2
    
    return math.sqrt(sqsum/N)


def fonset(samples, num, count=0):
    if (count+6000) > len(samples):
        return False
    
    print(f'\n\nBuscando inicio {count//88200 +1} del audio {num}')

    ind = count
    bg = samples[(count):(count+6000)]
    Lbg = max(bg)

    while True:
        if len(samples) <= ind + 111:
            return False
        
        print(f'{ind}/{len(samples)}', end='\r')

        compval = RMS(samples[ind+100:ind+111])
        cur = samples[ind]

        if count != 0:    
            if cur > 5*Lbg and compval < cur and ind > count:
                return ind
        else:
            if cur > 5*Lbg and compval < cur:
                return ind
            
        ind+=1


def allpeaks(samples, num):
    res = []
    c = 0

    while True:
        curind = fonset(samples, num, c)

        if not curind:
            return res
        
        res.append(curind)
        c += 88200
        


def tdiffer(p1, p2, srd=48000):
    tups = list(map(lambda x, y: (x,y), p1, p2))
    res = []

    for (peak1, peak2) in tups:
        res.append(librosa.samples_to_time(peak2 - peak1, sr=srd))

    return res


def statsvel(tdiffs, d):
    vels = []

    for tdiff in tdiffs:
        vels.append(round(d/tdiff, 2))

    avg = round(sum(vels) / len(vels), 2)
    sqsum = 0

    for vel in vels:
        sqsum += (vel - avg)**2

    sdev = round(math.sqrt(sqsum/len(vels)), 2)

    return f'La velocidad media del sonido hallada es ({avg} ± {sdev}) m/s'
