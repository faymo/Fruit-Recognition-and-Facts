import os
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import LabelEncoder
import json
from py_edamam import Edamam
from NutrientFacts import Nutrients
import tkinter as tk
import joblib
from tkinter import filedialog

# root = tk.Tk()
# root.withdraw()
# file_path = filedialog.askopenfilename()

#Parameters
BATCH_SIZE = 32
IMAGE_SIZE = 100

#loading in and preprocessing the train and test datasets
train_dataset = tf.keras.preprocessing.image_dataset_from_directory(
    "fruits-360_dataset/fruits-360/Training",
    shuffle=True,
    image_size=(IMAGE_SIZE, IMAGE_SIZE),
    batch_size=BATCH_SIZE
)

input_dataset = tf.keras.preprocessing.image_dataset_from_directory(
    "fruits-360_dataset/fruits-360/input",
    shuffle=False,
    image_size=(IMAGE_SIZE, IMAGE_SIZE),
    batch_size= 1
)

class_names_train = os.listdir('fruits-360_dataset/fruits-360/Training')

le = LabelEncoder()

le.fit(class_names_train)

class_labels_train = le.transform(class_names_train)
classes = []
for i in range(len(class_names_train)):
    classes.append(class_names_train[i])

# save the model to disk
filename = 'finalized_model.sav'


# load the model from disk
loaded_model = joblib.load(filename)

for test_images, test_labels in input_dataset.take(1):
    test_images = test_images.numpy()
    predictions = loaded_model.predict(test_images)

e = Edamam(nutrition_appid='60411624', nutrition_appkey='d51c2c10fb84b7f5cb6c470dda575338')
food = classes[int(np.argmax(predictions[0]))]
try:
    fruit = e.search_nutrient("1 " + food)
    x = json.dumps(fruit)  # deserializing dict
    y = json.loads(x)
    fruitItem = Nutrients()
    fruitItem.name = food
    fruitItem.getAll(y["totalNutrients"], y["totalDaily"])
except:
    print("No fruit found")