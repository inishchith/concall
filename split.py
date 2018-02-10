from pydub import AudioSegment

newAudio = AudioSegment.from_wav("./source/genevieve.wav")
st = 0
prev = 3000
for i in range(2):
    nd = newAudio[st:prev]
    st += prev
    newAudio.export('parts/out00000000'+ str(i+1) +'.wav', format="wav")
    prev += 3000
