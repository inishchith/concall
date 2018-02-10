import os,re
import speech_recognition as sr
from tqdm import tqdm
from multiprocessing.dummy import Pool
import glob
import pickle


from wit import Wit
import summarize_talk
import analyze_tone
import dist

def transcribe(data):
    r = sr.Recognizer()
    idx, file = data
    name = "parts/" + file
    print(name + " started")
    # Load audio file
    with open("api-key.json") as f:
        GOOGLE_CLOUD_SPEECH_CREDENTIALS = f.read()

    with sr.AudioFile(name) as source:
        audio = r.record(source)
    # Transcribe audio file
    text = r.recognize_google_cloud(audio, credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS)
    print(name + " done")
    return {
        "idx": idx,
        "text": text
    }


def get_data(text):
    auth_token = "43J3PMKM4PLNQFHLQPR75HO3GS6TOTAI"
    client = Wit(access_token = auth_token)
    response = client.message(text)
    print(response)
    return "hello friend"

def convert():
    # convert everything at 
    curr = "./source/*.wav"
    files = glob.glob(curr)
     
    file = open("hash.pickle","rb")
    marked = dict() #pickle.load(file)
    hash_list = dict()
    new_data = []
    
    pool = Pool(8) # Number of concurrent threads
    for f in files:
        if marked.get(f,-1) == -1:
            marked[f] = 1
            os.system("ffmpeg -i " + f[2:] +" -f segment -segment_time 30 -c copy parts/out%09d.wav")

            files = os.listdir('parts/')
            files = sorted(files)

            path = "./transcript"  
            all_text = pool.map(transcribe, enumerate(files))
            pool.close()
            pool.join()

            transcript = ""

            for t in sorted(all_text, key=lambda x: x['idx']):
                total_seconds = t['idx'] * 30
        
                m, s = divmod(total_seconds, 60)
                h, m = divmod(m, 60)
        
                transcript = transcript + t['text']

            # here filename should be a time_stamp of recording 
            # summarize transcript here , change defaults max_sent 
        
            title = "this is a placeholder"
            #print(transcript)
            summary = summarize_talk.summarize(title,transcript)
            name = f

            speakers = dist.diagraph(f) 
            tone_speaker0 = analyze_tone.analyze(speakers[0]) 
            tone_speaker1 = analyze_tone.analyze(speakers[1])
            new_data.append([transcript,tone_speaker0,tone_speaker1])
            print(get_data(title))
    
    os.system("rm -rf parts")
    os.system("mkdir parts")

    file.close()
    file = open("hash.pickle","wb")
    pickle.dump(marked,file)
    #print(new_data)
    return new_data


