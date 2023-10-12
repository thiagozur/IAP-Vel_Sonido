from matplotlib import pyplot as plt
import librosa
from timetools import allpeaks, tdiffer, statsvel

y1, sr1 = librosa.load('E:/E/Canciones/Experimento IAP/bounces/mic1.wav', offset=0.0, sr=None, mono=True)

librosa.display.waveshow(y1)
peaks1 = allpeaks(y1)
print(peaks1)
for peak in peaks1:
    plt.axvline(librosa.samples_to_time(peak), color='g')

y2, sr2 = librosa.load('E:/E/Canciones/Experimento IAP/bounces/mic2.wav', offset=0.0, sr=None, mono=True)

librosa.display.waveshow(y2)
peaks2 = allpeaks(y2)
print(peaks2)
for peak in peaks2:      
    plt.axvline(librosa.samples_to_time(peak), color='g')

diffs = tdiffer(peaks1, peaks2, srd=sr1)
print(statsvel(diffs, 12.75))

plt.show()