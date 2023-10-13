from matplotlib import pyplot as plt
import librosa
from timetools import allpeakonsets, tdiffer, statsvel

#cargamos el audio de ambos micrófonos
y1, sr1 = librosa.load('./mic1.wav', sr=None, mono=True)
y2, sr2 = librosa.load('./mic2.wav', sr=None, mono=True)

#detenemos la ejecución si las frecuencias de muestreo son distintas
if sr1 != sr2:
    raise ValueError(f'\nError: frecuencias de muestreo de los dos archivos son distintas.\n  -Archivo 1: {sr1}Hz\n  -Archivo 2: {sr2}Hz')

#graficamos las ondas de los audios de los micrófonos
librosa.display.waveshow(y1)
librosa.display.waveshow(y2)

#calculamos los momentos (en muestras) en los que se dispara la pistola en los audios de los micrófonos
peaks1 = allpeakonsets(y1, "1", sr1)
peaks2 = allpeakonsets(y2, "2", sr2)

#graficamos una recta vertical en cada uno de esos momentos
for peak in peaks1:
    plt.axvline(librosa.samples_to_time(peak), color='g')
for peak in peaks2:      
    plt.axvline(librosa.samples_to_time(peak), color='g')

#mostramos por pantalla la velocidad media hallada
print('\n\n' + statsvel(tdiffer(peaks1, peaks2, srd=sr1), 12.75))

#mostramos el gráfico
plt.show()