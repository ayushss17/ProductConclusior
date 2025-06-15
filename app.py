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
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from tensorflow.keras.preprocessing.sequence import pad_sequences
import time

app = Flask(__name__)

def init():
    global model

@app.route('/', methods=['GET', 'POST'])
def home():
    emotions = ""
    emot = 0.0
    sentiment = ""
    if request.method == "POST":
        user_inp = request.form.get('user_input')
        if user_inp:
            print(user_inp)
            emotions, emot, sentiment = sent_anly_prediction(user_inp)                    
        else:
            emotions = "Invalid link"
            emot = 18

        print(emotions, emot)
            
    return render_template("NewHome.html", data=emotions, val=emot, sentiment=sentiment)

def sent_anly_prediction(prod_link):
    emotions = []
    emot = 0.0
    sentiment = ""

    url = prod_link
    service = Service("C://chromedriver.exe")
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(url)
        time.sleep(5)

        reviews = driver.find_elements(By.CSS_SELECTOR, ".card-padding")
        review_texts = [review.text for review in reviews]

        if not review_texts:
            print("No reviews found")
            rev_data = "No reviews found"
        else:
            rev_data = "/n".join(review_texts)
            emotions, emot, sentiment = getReviews(rev_data)  
    finally:
        driver.quit()

    print("Function executed")
    
    global model 
    try:
        model = load_model("D:/Projects/ProductConclusior/sentiment_analysis.h5")
        print("Model loaded successfully.")
    except Exception as e:
        print(f"Error loading model: {e}")
        model = None  

    if rev_data != "No reviews found":
        word_to_id = imdb.get_word_index()
        vocab_size = 5000
        word_to_id = {k: (v + 3) for k, v in word_to_id.items()}  
        word_to_id["<PAD>"] = 0
        word_to_id["<START>"] = 1
        word_to_id["<UNK>"] = 2
        word_to_id["<UNUSED>"] = 3
        word_to_id = {k: v for k, v in word_to_id.items() if v < vocab_size}
        sentiment = ''
        strip_special_chars = re.compile("[^A-Za-z0-9 ]+")
        text = rev_data.lower().replace("<br />", " ")
        text = re.sub(strip_special_chars, "", text.lower())

        words = text.split()  #list
        vocab_size = 5000 
        x_test = [[word_to_id.get(word, 0) if word_to_id.get(word, 0) < vocab_size else 0 for word in words]]
        x_test = pad_sequences(x_test, maxlen=500)  
        vector = np.array([x_test.flatten()])

        if model is None:
            return "Model not loaded.", 500, "Neutral"  

        probability = model.predict(array([vector][0]))[0][0]

        if probability < (0.4 - 0.1):
            sentiment = 'Negative'
            print(sentiment)
        elif (0.4 - 0.1) <= probability <= (0.4 + 0.1):
            sentiment = "Neutral"
            print("Neutral")
        else:
            sentiment = 'Positive'
            print(sentiment)

        return emotions, emot, sentiment

    else:
        emotions = ["No emotions"]
        probability = 0.0
        sentiment = "Neutral"
        return emotions, probability, sentiment  

if __name__ == "__main__":
    init()
    app.run()
