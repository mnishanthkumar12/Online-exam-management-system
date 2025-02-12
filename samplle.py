import librosa

y, sr = librosa.load('uploads/student_audio.wav')
print(f"Audio shape: {y.shape}, Sample rate: {sr}")
