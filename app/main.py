import os
import json
from PIL import Image

import numpy as np
import tensorflow as tf
import streamlit as st

working_dir = os.path.dirname(os.path.abspath(__file__))

model_path = f"{working_dir}/trained_model/plant_disease_prediction_model.h5"
model = tf.keras.models.load_model(model_path)

#loading the class names
class_indices = json.load(open(f"{working_dir}/class_indices.json"))

#function to load and preprocess the image
def load_and_preprocess_image(image_path, target_size=(224, 224)):
  #load the image
  img = Image.open(image_path)
  #resize the image
  img = img.resize(target_size)
  #convert the image to a numpy array
  img_arr = np.array(img)
  #add dimension i.e. batch_size
  img_arr = np.expand_dims(img_arr, axis=0)
  #scale the image values to [0, 1]
  img_arr = img_arr.astype('float32') / 255.0
  return img_arr

#function to predict the class of an image
def predict_image_class(model, image_path, class_indices):
  preprocessed_img = load_and_preprocess_image(image_path)
  prediction = model.predict(preprocessed_img)
  predicted_class_index = np.argmax(prediction, axis=1)[0]
  predicted_class_name = class_indices[str(predicted_class_index)]
  return predicted_class_name

#streamlit app

st.title('🌿 Plant Disease Classifier')

uploaded_image = st.file_uploader('Upload an image...', type=['jpg', 'jpeg', 'png'])

if uploaded_image:
  image = Image.open(uploaded_image)
  col1, col2 = st.columns(2)

  with col1:
    resized_img = image.resize((150, 150))
    st.image(resized_img)

  with col2:
    if st.button('Classify'):
      prediction = predict_image_class(model, uploaded_image, class_indices)
      st.success(f'Prediction: {str(prediction)}')