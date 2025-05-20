import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageOps
import numpy as np
import tensorflow as tf  


import sys
import os
import tensorflow as tf

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller .exe """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        # Not running in a bundle
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Load model safely whether running as .py or .exe
model_path = resource_path("mnist_model.keras")
model = tf.keras.models.load_model(model_path)

#model = tf.keras.models.load_model("D:/VS-Code/Kunal-Workspace/MNIST/mnist_model.keras")

def preprocess_image(image_path):
    img = Image.open(image_path).convert('L') 
    img = ImageOps.invert(img)                 
    img = img.resize((28, 28))                
    img_arr = np.array(img) / 255.0            
    img_arr = img_arr.reshape(1, 28, 28, 1)     
    return img_arr, img

def predict_digit():
    file_path = filedialog.askopenfilename()
    if not file_path:
        print("Error opening the file!")
        return
    try:
        image_arr, display_img = preprocess_image(file_path)
        prediction = model.predict(image_arr)
        digit = np.argmax(prediction)
        confidence=np.max(prediction)
    except Exception as e:
        safe_error = str(e).encode("utf-8", "ignore").decode("utf-8")
        result_label.config(text=f"Error: {safe_error}", fg="red", font=("Arial", 12))
        return
    result_label.config(text=f"Predicted Digit: {digit} ({confidence:.2%} confidence)", font=("Arial", 16), fg="green")
    img_tk = ImageTk.PhotoImage(display_img.resize((140, 140)))
    panel.config(image=img_tk)
    panel.image = img_tk



root = tk.Tk()
root.geometry("600x500")
root.title("MNIST Digit Classifier")

frame = tk.Frame(root)
frame.pack(pady=20)

btn = tk.Button(frame, text="Select Image", command=predict_digit, font=("Arial", 14))
btn.pack()

result_label = tk.Label(root, text="", font=("Arial", 16))
result_label.pack(pady=10)

panel = tk.Label(root)
panel.pack()

root.mainloop()