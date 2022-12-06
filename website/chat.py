from flask import Blueprint, request
from nltk.stem import WordNetLemmatizer
import numpy as np
import json
import pickle
import random
import nltk
from tensorflow.keras.models import load_model

lemmatizer = WordNetLemmatizer()
chat = Blueprint('chat', __name__)

# chat initialization
model = load_model("chatbot_model.h5")
intents = json.loads(open("intents1.json").read())
words = pickle.load(open("words.pkl", "rb"))
classes = pickle.load(open("classes.pkl", "rb"))

# chat functionalities
def clean_text(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

# return BoW array: 0 or 1 for each word in the bag that exists in the sentence
def bag(sentence, words, show_details=True):
    sentence_words = clean_text(sentence)

    bow = [0] * len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                # assign 1 if current word is in the vocabulary position
                bow[i] = 1
                if show_details:
                    print("found in bag: %s" % w)
    return np.array(bow)

# filter out any predictions that is below the threshold
def predict_class(sentence, model):
    p = bag(sentence, words, show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

def getResponse(ints, intents_json):
    tag = ints[0]["intent"]
    list_of_intents = intents_json["intents"]
    for i in list_of_intents:
        if i["tag"] == tag:
            result = random.choice(i["responses"])
            break
    return result

# chatbot
@chat.route("/get", methods=["POST"])
def bot_response():
    msg = request.data.decode()
    if msg.startswith('my name is'):
        name = msg[11:]
        ints = predict_class(msg, model)
        res1 = getResponse(ints, intents)
        res = res1.replace("{n}",name)
    elif msg.startswith('hi my name is'):
        name = msg[14:]
        ints = predict_class(msg, model)
        res1 = getResponse(ints, intents)
        res = res1.replace("{n}",name)
    else:
        ints = predict_class(msg, model)
        res = getResponse(ints, intents)
    return res