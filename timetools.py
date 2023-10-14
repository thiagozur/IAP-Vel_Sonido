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
    """Busca todos los índices en una lista de muestras en los que la presión sonora comienza a subir hacia un pico.
    
    Parámetros
    ----------
    samples: np.ndarray
        La lista de muestras en la que se quiere encontrar los índices
    
    id: str
        Nombre identificador del archivo siendo analizado para mostrar por pantalla
    
    sr: int
        La frecuencia de muestreo del audio a analizar
    
    Devuelve
    --------
    res: list
        La lista con todos los índices encontrados"""
    
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
    """Calcula las diferencias de tiempo entre los pares de índices correspondientes
    en dos listas de índices de muestras.

    Los índices de muestras deben provenir de audios de igual frecuencia de muestreo (por defecto ``srd=44100``).
    
    Parámetros
    ----------
    p1: list
        La primera lista de índices
    
    p1: list
        La segunda lista de índices
    
    sr: int
        La frecuencia de muestreo de los archivos de donde se obtuvieron los índices
    
    Devuelve
    --------
    res: list
        La lista con todas las diferencias de tiempo (en segundos) entre los pares
        de índices de las listas encontrados

    Errores
    -------    
        ValueError si las listas de índices no tienen la misma cantidad de elementos"""
    
    if len(p1) != len(p2):
        raise ValueError('Las listas de índices no tienen la misma cantidad de elementos')

    tups = list(map(lambda x, y: (x,y), p1, p2))
    res = []

    for (peak1, peak2) in tups:
        res.append(librosa.samples_to_time(peak2 - peak1, sr=srd))

    return res


def statsvel(tdiffs: list, d: int):
    """Calcula la velocidad media del sonido y su error estadístico redondeados a dos decimales a partir de una lista de diferencias de tiempo (en segundos)
    y la distancia recorrida (en metros) entre los puntos que determinan las diferencias de tiempo.

    La distancia entre los puntos debe ser la misma para todas las diferencias de tiempo calculadas.
    
    Parámetros
    ----------
    tdiffs: list
        La lista de diferencias de tiempo

    d: int
        La distancia recorrida
    
    Devuelve
    --------
    resstring: str
        Texto reportando la velocidad media hallada con su error estadístico"""
    
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
