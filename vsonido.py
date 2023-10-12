from matplotlib import pyplot as plt
import librosa
from timetools import allpeaks, tdiffer, statsvel

y1, sr1 = librosa.load('./mic1.wav', offset=0.0, sr=None, mono=True)

librosa.display.waveshow(y1)
peaks1 = allpeaks(y1, 1)
for peak in peaks1:
    plt.axvline(librosa.samples_to_time(peak), color='g')

y2, sr2 = librosa.load('./mic2.wav', offset=0.0, sr=None, mono=True)

librosa.display.waveshow(y2)
peaks2 = allpeaks(y2, 2)
for peak in peaks2:      
    plt.axvline(librosa.samples_to_time(peak), color='g')

print('\n\n' + statsvel(tdiffer(peaks1, peaks2, srd=sr1), 12.75))

plt.show()