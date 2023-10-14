import librosa
import math
import numpy as np
import dearpygui.dearpygui as dpg

def RMS(samples: np.ndarray):
    """Calcula el valor eficaz de una selección de muestras.
    
    Parámetros
    ----------
    samples: np.ndarray
        Las muestras de las que se quiere calcular el valor eficaz
    
    Devuelve
    --------
    RMS: float
        El valor eficaz buscado"""
    
    sqsum = 0
    N = len(samples)

    for s in samples:
        sqsum += s**2
    
    RMS = math.sqrt(sqsum/N)

    return RMS


def fonset(samples: np.ndarray, count=0, sr=44100):
    """Busca el índice en una lista de muestras de la primera muestra en
    la que comienza a subir la presión sonora hacia un pico.

    La lista comienza a recorrerse desde un índice inicial
    elegido (por defecto ``count=0``).
    
    Parámetros
    ----------
    samples: np.ndarray
        La lista de muestras en la que se quiere encontrar el índice
    
    id: str
        Nombre identificador del archivo siendo analizado para mostrar por pantalla

    count: int
        Índice desde el que se comienza a recorrer la lista
    
    sr: int
        La frecuencia de muestreo del audio a analizar
    
    Devuelve
    --------
    ind: float|False
        El índice encontrado, o False en caso de no poderse realizar el cálculo o no encontrarse un índice"""
    
    if (count+6000) > len(samples):
        return False
    

    inc = math.trunc(sr*0.15)
    ic = math.trunc(sr*0.002)
    sc = math.trunc(sr*0.0025)
    ind = count
    bg = samples[(count):(count+inc)]
    Lbg = max(bg)

    while True:
        if len(samples) <= ind + sc:
            return False

        compval = RMS(samples[ind+ic:ind+sc])
        cur = samples[ind]

        if count != 0:    
            if cur > 5*Lbg and compval < cur and ind > count:
                return ind
        else:
            if cur > 5*Lbg and compval < cur:
                return ind
            
        ind+=1


def allpeakonsets(samples: np.ndarray, pinc: float, pbar, sr=44100):
    res = []
    c = 0

    while True:
        curind = fonset(samples, c, sr)

        if not curind:
            return res
        
        res.append(curind)
        cbar = dpg.get_value(pbar)
        cbar += pinc
        dpg.set_value(pbar, cbar)

        c += 88200
        

def tdiffer(p1: list, p2: list, srd=44100):
    if len(p1) != len(p2):
        raise ValueError('Las listas de índices no tienen la misma cantidad de elementos')

    tups = list(map(lambda x, y: (x,y), p1, p2))
    res = []

    for (peak1, peak2) in tups:
        res.append(librosa.samples_to_time(peak2 - peak1, sr=srd))

    return res


def statsvel(tdiffs: list, d: int):
    vels = []

    for tdiff in tdiffs:
        vels.append(round(d/tdiff, 2))

    avg = round(sum(vels) / len(vels), 2)
    sqsum = 0

    for vel in vels:
        sqsum += (vel - avg)**2

    sdev = round(math.sqrt(sqsum/len(vels)), 2)

    resstring = f'({avg} ± {sdev}) m/s'

    return resstring
