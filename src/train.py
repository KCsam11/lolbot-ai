import json
import numpy as np
import random
import pickle
import nltk

from nltk.stem import PorterStemmer
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import SGD

nltk.download('punkt_tab')

print("Loading NLTK resources...")

stemmer = PorterStemmer()

with open('data/intents.json') as file:
    data = json.load(file)

words = []
labels = []
docs_x = []
docs_y = []

for intent in data['intents']:
    for pattern in intent["patterns"]:
        token = nltk.word_tokenize(pattern.lower())
        words.extend(token)
        docs_x.append(token)
        docs_y.append(intent["tag"])
    if intent["tag"] not in labels:
        labels.append(intent["tag"])

words = [stemmer.stem(w.replace("'", "")) for w in words if w.replace("'", "").isalnum()]
words = sorted(set(words))
labels = sorted(labels)


training = []
output_empty = [0] * len(labels)

for x, doc in enumerate(docs_x):
    bag = []
    stemmed_words = [stemmer.stem(w_doc.replace("'", "")) for w_doc in doc if w_doc.replace("'", "").isalnum()]

    for w in words:
        bag.append(1 if w in stemmed_words else 0)

    output_row = output_empty[:]
    output_row[labels.index(docs_y[x])] = 1
    #print(f"Processed pattern: {doc} -> Bag: {bag} -> Output: {output_row}")

    training.append([bag, output_row])


random.shuffle(training)
training = np.array(training, dtype=object)

# bag 
train_x = np.array(list(training[:, 0])) 

#labels
train_y = np.array(list(training[:, 1]))

# Création du modèle
model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation='softmax'))

sgd = SGD(learning_rate=0.01, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy']) 

model.fit(train_x, train_y, epochs=200, batch_size=5, verbose=1)

model.save('model/chatbot_model.h5')

pickle.dump((words, labels, train_x), open("model/training_data.pkl", "wb"))
