import librosa
import math

#RMS devuelve el valor eficaz de una lista de muestras (samples)
def RMS(samples):
    sqsum = 0
    N = len(samples)

    for s in samples:
        sqsum += s**2
    
    return math.sqrt(sqsum/N)


#fonset devuelve el índice en una lista de muestras (samples)
#del primer disparo que encuentra después de un índice inicial (count).
#De no encontrar ninguno, devuelve False
def fonset(samples, num=1, count=0, sr=44100):
    if (count+6000) > len(samples):
        return False
    
    print(f'\n\nBuscando inicio {count//(2*sr) + 1} del audio {num}')

    inc = math.trunc(sr*0.15)
    ic = math.trunc(sr*0.002)
    sc = math.trunc(sr*0.0025)
    ind = count
    bg = samples[(count):(count+inc)]
    Lbg = max(bg)

    while True:
        if len(samples) <= ind + sc:
            return False
        
        print(f'{ind}/{len(samples)}', end='\r')

        compval = RMS(samples[ind+ic:ind+sc])
        cur = samples[ind]

        if count != 0:    
            if cur > 5*Lbg and compval < cur and ind > count:
                return ind
        else:
            if cur > 5*Lbg and compval < cur:
                return ind
            
        ind+=1


#allpeakonsets devuelve una lista con todos los índices de una
#lista de muestras (samples) en los que se da un disparo
def allpeakonsets(samples, num, sr=44100):
    res = []
    c = 0

    while True:
        curind = fonset(samples, num, c, sr)

        if not curind:
            return res
        
        res.append(curind)
        c += 88200
        

#tdiffer devuelve una lista con las diferencias de tiempo en segundos
#entre cada par de valores de dos listas de muestras (p1 y p2)
def tdiffer(p1, p2, srd=44100):
    tups = list(map(lambda x, y: (x,y), p1, p2))
    res = []

    for (peak1, peak2) in tups:
        res.append(librosa.samples_to_time(peak2 - peak1, sr=srd))

    return res


#statsvel devuelve una string con la velocidad media hallada
#junto a su error estadístico a partir de una lista de diferencias
#de tiempo (tdiffs) y una distancia (d)
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
