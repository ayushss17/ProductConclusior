# Other imports remain unchanged
from flask import Flask, render_template, flash, request, url_for, redirect, session
import numpy as np
import pandas as pd
import re
import os
import tensorflow as tf
from numpy import array
from keras.datasets import imdb
from keras.preprocessing import sequence
from keras.models import load_model
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import sequence


IMAGE_FOLDER = os.path.join('static', 'img_pool')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = IMAGE_FOLDER

#########################Code for Sentiment Analysis
@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template("home.html")

@app.route('/sentiment_analysis_prediction', methods = ['POST', "GET"])
def sent_anly_prediction():
    global model 
    try:
        # Load the pre-trained Keras model
        model = load_model('D:\Projects\ProductConclusior\Conclusior\AI_App\sentiment_analysis.h5')
        print("Model loaded successfully.")
    except Exception as e:
        print(f"Error loading model: {e}")
        model = None  # Set model to None if loading fails # Declare model as global to access the loaded model
    if request.method == 'POST':
        text = request.form['text']
        sentiment = ''
        max_review_length = 500
        word_to_id = imdb.get_word_index()
        strip_special_chars = re.compile("[^A-Za-z0-9 ]+")
        text = text.lower().replace("<br />", " ")
        text = re.sub(strip_special_chars, "", text.lower())

        words = text.split()  # split string into a list
        x_test = [[word_to_id[word] if (word in word_to_id and word_to_id[word] <= 20000) else 0 for word in words]]
        x_test = sequence.pad_sequences(x_test, maxlen=500)  # Should be same which you used for training data
        vector = np.array([x_test.flatten()])

        # No need to use graph in TensorFlow 2.x
        if model is None:
            return "Model not loaded.", 500  # Return an error response if model is None
        probability = model.predict(array([vector][0]))[0][0]
        class1 = (probability > 0.5).astype(int)  # 0 for Negative, 1 for Positive

        if class1 == 0:
            sentiment = 'Negative'
            img_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'Sad_Emoji.png')
        else:
            sentiment = 'Positive'
            img_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'Smiling_Emoji.png')

        return render_template('home.html', text=text, sentiment=sentiment, probability=probability, image=img_filename)

#########################Code for Sentiment Analysis

if __name__ == "__main__":
    init()
    app.run()
