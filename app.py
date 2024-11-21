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
import requests
from analysis import getReviews
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from tensorflow.keras.preprocessing.sequence import pad_sequences

import time

app = Flask(__name__)

def init():
    global model,graph
    # load the pre-trained Keras model
    model = load_model('sentiment_analysis.h5')

@app.route('/', methods=['GET', 'POST'])
def home():
    print("rendered")
    emotions=""
    emot=0.0
    emot_unq=""
    sentiment=""
    if request.method=="POST":
        user_inp=request.form.get('user_input')
        if user_inp:
            emotions,emot,sentiment=sent_anly_prediction(user_inp)                    
        else:
            emotions="Invalid link"
            emot=69

        print(emotions,emot)
            
    return render_template("Homepage.html",data=emotions,val=emot,sentiment=sentiment)

@app.route('/#sec2', methods=['GET', 'POST'])
def sent_anly_prediction(prod_link):
    emotions=[]
    emot=0.0
    url = prod_link
    service=Service("C:\Drivers\chromedriver.exe")
    options=webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver=webdriver.Chrome(service=service,options=options)

    try:
        driver.get(url)
        time.sleep(5)

        reviews = driver.find_elements(By.CSS_SELECTOR, ".card-padding")
        review_texts = [review.text for  review in reviews]

        if not review_texts:
            print("No reviews found")
            return None
        rev_data="\n".join(review_texts)
        emotions,emot=getReviews(rev_data)
    finally:
        driver.quit()
    print("Function excuted")
    global model 
    try:
        # Load the pre-trained Keras model
        model = load_model('D:\Projects\ProductConclusior\Conclusior\sentiment_analysis.h5')
        print("Model loaded successfully.")
    except Exception as e:
        print(f"Error loading model: {e}")
        model = None  # Set model to None if loading fails # Declare model as global to access the loaded model
    print(model.summary())
    word_to_id = imdb.get_word_index()
    vocab_size = 5000
    word_to_id = {k: (v + 3) for k, v in word_to_id.items()}  # Shift indices for special tokens
    word_to_id["<PAD>"] = 0
    word_to_id["<START>"] = 1
    word_to_id["<UNK>"] = 2
    word_to_id["<UNUSED>"] = 3
    word_to_id = {k: v for k, v in word_to_id.items() if v < vocab_size}
    data = rev_data
    sentiment = ''
    max_review_length = 500
    strip_special_chars = re.compile("[^A-Za-z0-9 ]+")
    text = data.lower().replace("<br />", " ")
    text = re.sub(strip_special_chars, "", text.lower())

    words = text.split()  # split string into a list
    vocab_size = 5000  # Match this to the embedding layer's input_dim
    x_test = [[word_to_id.get(word, 0) if word_to_id.get(word, 0) < vocab_size else 0 for word in words]]
    x_test = pad_sequences(x_test, maxlen=500)  # Should be same which you used for training data
    vector = np.array([x_test.flatten()])

        # No need to use graph in TensorFlow 2.x
    if model is None:
        return "Model not loaded.", 500  # Return an error response if model is None
    probability = model.predict(array([vector][0]))[0][0]
    class1 = (probability > 0.5).astype(int)  # 0 for Negative, 1 for Positive

    if class1 == 0:
        sentiment = 'Negative'
        print(sentiment)
    else:
        sentiment = 'Positive'
        print(sentiment)

    return (emotions,probability,sentiment)

if __name__ == "__main__":
    init()
    app.run()
