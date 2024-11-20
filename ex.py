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
from tensorflow.keras.preprocessing.sequence import pad_sequences

def sent_anly_prediction():
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
    data = "Good morning everyone, I'm truly honored to be here today to discuss the recent developments in our company's sustainability initiatives. While we've made significant strides in reducing our carbon footprint through renewable energy adoption and responsible sourcing, we acknowledge that there's still a long road ahead. Our commitment to ethical practices and community engagement remains unwavering, even as we navigate the challenges of a rapidly changing market. We're actively exploring innovative solutions to address concerns about waste management and employee wellbeing, and we're confident that with your continued support, we can achieve our ambitious goals of creating a more sustainable future for all stakeholders.However, we must also address the recent controversies surrounding our operations in certain regions. We take these allegations very seriously and have initiated a comprehensive internal audit to ensure full transparency and accountability. We are committed to upholding the highest standards of corporate governance and will not hesitate to take decisive action against any violations of our ethical code.Looking forward, we are excited about the opportunities to collaborate with our partners, industry experts, and local communities to drive positive change. Our focus on research and development will be pivotal in developing sustainable technologies that benefit not only our company but the planet as a whole. Thank you for your continued trust and support as we strive to be a leader in environmentally responsible business practices."
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

sent_anly_prediction()

        