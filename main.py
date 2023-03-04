import os
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import LabelEncoder
import json
from py_edamam import Edamam
from NutrientFacts import Nutrients

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

image = "fruits-360_dataset/fruits-360/Test/Apple Red 1/4_100.jpg"

model = tf.keras.models.Sequential([
    tf.keras.layers.Rescaling(1. / 255, input_shape=(100, 100, 3)),  # Rescaling
    tf.keras.layers.Conv2D(32, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2, 2),  # This is the Convolutions layer

    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2, 2),  # This is the Convolutions layer

    tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2, 2),  # This is the Convolutions layer

    tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2, 2),  # This is the Convolutions layer

    tf.keras.layers.Flatten(),  # This is the Output layer
    tf.keras.layers.Dense(512, activation='relu'),  # This is the Output layer
    tf.keras.layers.Dense(131)  # This is the Output layer
])

#Compiling using Adam Optimizer
model.compile(optimizer='adam',
             loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

epochs= 1
history = model.fit(
  train_dataset,
  validation_data=input_dataset,
  epochs=epochs
)

for test_images, test_labels in input_dataset.take(1):
    test_images = test_images.numpy()
    predictions = model.predict(test_images)

predictions.shape


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