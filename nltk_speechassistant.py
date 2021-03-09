
import io
import random
import string # to process standard python strings
import warnings
import speech_recognition as sr
import pyttsx3
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import warnings
warnings.filterwarnings('ignore')

import nltk
from nltk.stem import WordNetLemmatizer
nltk.download('popular', quiet=True) # for downloading packages

# uncomment the following only the first time
#nltk.download('punkt') # first-time use only
#nltk.download('wordnet') # first-time use only
engine = pyttsx3.init('sapi5')
voices=engine.getProperty('voices')
#print(voices[1].id)
engine.setProperty('voice',voices[2].id)
def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()
def takecommand():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        print("I am Listening Your Voice !!!!!!!!!!!!!!!")
        
        r.pause_threshold=1
        audio=r.listen(source)
    #,timeout=5,phrase_time_limit=8
        try:
            print("Recognizing")
            query=r.recognize_google(audio,language='en-in')
            print(f"you said : {query}")
        except Exception as e:
            speak("say that again please <<<<<>>>>>")
            return "none"
        return query
#Reading in the corpus
with open('chatbot.txt','r', encoding='utf8', errors ='ignore') as fin:
    raw = fin.read().lower()

#TOkenisation
sent_tokens = nltk.sent_tokenize(raw)# converts to list of sentences 
word_tokens = nltk.word_tokenize(raw)# converts to list of words

# Preprocessing
lemmer = WordNetLemmatizer()
def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]
remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))


# Keyword Matching
 
GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up","hey","hey alexa","alexa","rahul","soma")
GREETING_RESPONSES = ["hi", "hey", "*nods*", "hi there", "hello", "I am glad! You are talking to me"]

def greeting(sentence):
    """If user's input is a greeting, return a greeting response"""
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)


# Generating response
def response(user_response):
    robo_response=''
    sent_tokens.append(user_response)
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx=vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    if(req_tfidf==0):
        robo_response=robo_response+"I am sorry! I don't understand you"
        return robo_response
    else:
        robo_response = robo_response+sent_tokens[idx]
        return robo_response


flag=True
print("ROBO: My name is Robo. I will answer your queries about Chatbots. If you want to exit, type Bye!")
while(flag==True):
    
    user_response = takecommand().lower
    user_response=takecommand().lower()
    if(takecommand!='bye'):          
        if(greeting(user_response)!=None):
                print("ROBO: "+greeting(user_response))
                speak(f"{greeting(user_response)}")
        
        else:
            if(takecommand=='thanks' or takecommand=='thank you' ):
             flag=False
             print("ROBO: You are welcome..")
            else:
                 print("ROBO: ",end="")
                 print(response(takecommand))
                 sent_tokens.remove(takecommand)
    else:
        flag=False
        print("ROBO: Bye! take care..")    
        