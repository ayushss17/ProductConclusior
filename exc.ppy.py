def sent_anly_prediction():
    data=request.json
    global model 
    try:
        # Load the pre-trained Keras model
        model = load_model('D:\Projects\ProductConclusior\Conclusior\sentiment_analysis.h5')
        print("Model loaded successfully.")
    except Exception as e:
        print(f"Error loading model: {e}")
        model = None  # Set model to None if loading fails # Declare model as global to access the loaded model
    if request.method == 'POST':
        text = data.get('user-input')
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

        return render_template('Homepage.html', text=text, sentiment=sentiment, probability=probability, image=img_filename)