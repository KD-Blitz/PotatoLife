# Importing libraries
from fastapi import FastAPI,File,UploadFile
import uvicorn
import numpy as np
from io import BytesIO
from PIL import Image
import tensorflow as tf
app=FastAPI()

MODEL = tf.keras.models.load_model("C:/Users/Krishna/Downloads/PotatoDC/saved_models/4", compile=False)     # .. --> to go to parent directory
CLASS_NAMES = ["Early Blight", "Late Blight", "Healthy"]

@app.get("/ping")  # specifying entry/end point

# To check if our server is alive or stopped 
async def ping():    
    return "Hello, I am alive"

def read_file_as_image(data) -> np.ndarray:
    image = np.array(Image.open(BytesIO(data)))    # reading pillow image as a numpy array
    return image

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    image=read_file_as_image(await file.read())
    img_batch = np.expand_dims(image, 0)   # adding extra dimension to image
    
    predictions = MODEL.predict(img_batch)
    predicted_class = CLASS_NAMES[np.argmax(predictions[0])]
    confidence = np.max(predictions[0])
    return {
        'class': predicted_class,
        'confidence': float(confidence)
    }

if __name__=="__main__":
    uvicorn.run(app,host='localhost',port=8000)