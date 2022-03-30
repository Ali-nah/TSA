import array
from django.shortcuts import render
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Embedding, LSTM, SpatialDropout1D
import pickle
import numpy as np


def home(request):
    return render(request, "base/home.html")


def getSentiment(request):
    if request.method == 'POST':
        twt = request.POST['txtarea']
        text = twt
        twt = [twt]
        with open('model/sentiment.pickle', 'rb') as handle:
            loaded_tokenizer = pickle.load(handle)

        seq = loaded_tokenizer.texts_to_sequences(twt)
        padded = pad_sequences(seq, maxlen=28, dtype='int32', value=0)

        model = load_model('model/sentiment.h5')
        sentiment = model.predict(padded, batch_size=1)[0]
        # prob = model.predict(array([np.vectorize][0]))[0][0]
        if(np.argmax(sentiment) == 0):
            return render(request, "base/home.html", {'result': 'Sentiment is Negative. 😌 '})
        elif (np.argmax(sentiment) == 1):
            return render(request, "base/home.html", {'result': 'Sentiment is Positive. 😃'})
