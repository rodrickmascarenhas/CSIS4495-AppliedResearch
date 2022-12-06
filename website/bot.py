import json
import pickle
import random
import nltk
import numpy as np
from keras.layers import Dense, Dropout
from keras.models import Sequential
from keras.optimizers import Adam
from nltk.stem import WordNetLemmatizer
import tensorflow as tf

nltk.download('omw-1.4')
nltk.download("punkt")
nltk.download("wordnet")

# init files
words = []  # vocabulary for patterns
classes = []  # vocabulary for tags
documents = []  # storing documents
ignore_words = ["?", "!"]
data_file = open("website/intents1.json").read()  # data file
intents = json.loads(data_file)
lemmatizer = WordNetLemmatizer()  # initializing lemmatizer to get stem of words

# words
for intent in intents["intents"]:
    for pattern in intent["patterns"]:

        # take each word and tokenize it
        w = nltk.word_tokenize(pattern)
        words.extend(w)
        # adding documents
        documents.append((w, intent["tag"]))

        # adding a tag to the classes
        if intent["tag"] not in classes:
            classes.append(intent["tag"])

# if words doesnt appear in punctuation
words = [lemmatizer.lemmatize(w.lower()) for w in words if w not in ignore_words]

# sorting the vocab and classes in alphabetical order.
words = sorted(list(set(words)))
classes = sorted(list(set(classes)))

print(len(documents), "documents")
print(len(classes), "classes", classes)
print(len(words), "lemmatized words", words)

pickle.dump(words, open("words.pkl", "wb"))
pickle.dump(classes, open("classes.pkl", "wb"))

# initializing training data
training = []
output_empty = [0] * len(classes)

# creating BoW model
for doc in documents:
    bow = []

    # list of tokenized words for the pattern
    pattern_words = doc[0]

    # lemmatize each word - create base word, in attempt to represent related words
    pattern_words = [lemmatizer.lemmatize(word.lower()) for word in pattern_words]

    # (1) the word is present in the pattern/tag and (0) means absent
    for w in words:
        bow.append(1) if w in pattern_words else bow.append(0)
    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1

    # add BoW and output_row to training
    training.append([bow, output_row])

# shuffle and convert to an array
random.shuffle(training)
training = np.array(training, dtype=object)

# split the features and target labels
train_x = np.array(list(training[:, 0]))
train_y = np.array(list(training[:, 1]))

# actual training
model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]),), activation="relu"))
model.add(Dropout(0.5))
model.add(Dense(64, activation="relu"))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation="softmax"))
adam = Adam(learning_rate=0.01, decay=1e-6)
model.compile(loss='categorical_crossentropy', optimizer=adam, metrics =["accuracy"])
model.summary()


# fitting and saving the model
hist = model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=5, verbose=1)
model.save("chatbot_model.h5", hist)
print("MODEL CREATED!!!")
