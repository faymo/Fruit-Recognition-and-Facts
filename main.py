import os
from tkinter.ttk import Style
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import LabelEncoder
import json
from py_edamam import Edamam
from NutrientFacts import Nutrients
import tkinter as tk
import joblib
from tkinter import filedialog
from PIL import ImageTk, Image

directory = ""

def browseFiles():
    global directory
    filename = filedialog.askopenfilename()
    # Change label contents
    directory = filename
    img = ImageTk.PhotoImage(Image.open(directory))
    labelBox.configure(image=img)
    labelBox.image = img

def predict():
    # Parameters
    BATCH_SIZE = 32
    IMAGE_SIZE = 100
    global directory
    # loading in and preprocessing the train and test datasets
    train_dataset = tf.keras.preprocessing.image_dataset_from_directory(
        "fruits-360_dataset/fruits-360/Training",
        shuffle=True,
        image_size=(IMAGE_SIZE, IMAGE_SIZE),
        batch_size=BATCH_SIZE
    )
    count = 0
    directory = list(directory)
    for i, d in reversed(list(enumerate(directory))):
        if d == "/":
            count += 1
        else:
            del directory[i]
        if count == 2:
            break
    newDirectory = "".join(directory)
    input_dataset = tf.keras.preprocessing.image_dataset_from_directory(
        newDirectory,
        shuffle=False,
        image_size=(IMAGE_SIZE, IMAGE_SIZE),
        batch_size=1
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
        bam = fruitItem.getAll(y["totalNutrients"], y["totalDaily"])
        textOutput.insert(tk.END, bam)
    except:
        textOutput.insert(tk.END, "No such fruit found")

def reset():
    textOutput.delete("1.0", "end")
    img = ImageTk.PhotoImage(Image.open("black.jpg"))
    labelBox.configure(image=img)
    labelBox.image = img

root = tk.Tk()
root.title("Fruity Facts")
root.geometry("1000x600")
img = ImageTk.PhotoImage(Image.open("black.jpg"))
labelTitle = tk.Label(root, text="Fruity Facts", font= ('calibri', 20, 'bold'))
labelBox = tk.Label(root, image=img)
labelPredicted = tk.Label(root, text="", font= ('calibri', 20, 'bold'))
labelFacts = tk.Label(root, text="Here are the Fruity Facts!", font= ('calibri', 20, 'bold'))
buttonCalc = tk.Button(root, text="Find Fruity Facts", command=predict, font= ('calibri', 20, 'bold'))
buttonImage = tk.Button(root, text="Click here to insert image", command = browseFiles, font= ('calibri', 20, 'bold'))
buttonReset = tk.Button(root, text="Reset", command=reset, font= ('calibri', 20, 'bold'))
textOutput = tk.Text(root, width = 40, height = 18, font= ('calibri'))

style = Style()

style.configure('TButton', font=
('calibri', 20, 'bold'),
                borderwidth='4')

# Changes will be reflected
# by the movement of mouse.
style.map('TButton', foreground=[('active', '!disabled', 'green')],
          background=[('active', 'black')])


labelTitle.grid(row = 1, column = 2)
labelBox.grid(row = 2, column = 2)
labelPredicted.grid(row = 5, column = 2)
labelFacts.grid(row = 1, column = 4)
buttonCalc.grid(row = 7, column = 3)
buttonReset.grid(row = 7, column = 4)
buttonImage.grid(row = 7, column = 2)
textOutput.grid(row = 2, column = 4)
root.mainloop()