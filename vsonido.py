from matplotlib import pyplot as plt
import librosa
from timetools import allpeakonsets, tdiffer, statsvel

#cargamos el audio del primer micrófono
y1, sr1 = librosa.load('./mic1.wav', sr=None, mono=True)

#cargamos el audio del segundo micrófono
y2, sr2 = librosa.load('./mic2.wav', sr=None, mono=True)

#detenemos la ejecución si las frecuencias de muestreo son distintas
if sr1 != sr2:
    raise ValueError(f'\nError: frecuencias de muestreo de los dos archivos son distintas.\n  -Archivo 1: {sr1}Hz\n  -Archivo 2: {sr2}Hz')

#graficamos la onda del audio del primer micrófono
librosa.display.waveshow(y1)

#calculamos los momentos (en muestras) en los que se dispara la pistola en el audio del primer micrófono
peaks1 = allpeakonsets(y1, 1, sr1)

#graficamos una recta vertical en cada uno de esos momentos
for peak in peaks1:
    plt.axvline(librosa.samples_to_time(peak), color='g')

#graficamos la onda del audio del segundo micrófono
librosa.display.waveshow(y2)

#calculamos los momentos (en muestras) en los que se dispara la pistola en el audio del segundo micrófono
peaks2 = allpeakonsets(y2, 2, sr2)

#graficamos una recta vertical en cada uno de esos momentos
for peak in peaks2:      
    plt.axvline(librosa.samples_to_time(peak), color='g')

#mostramos por pantalla la velocidad media hallada
print('\n\n' + statsvel(tdiffer(peaks1, peaks2, srd=sr1), 12.75))

#mostramos el gráfico
plt.show()