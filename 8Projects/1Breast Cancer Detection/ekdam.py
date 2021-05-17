from matplotlib.image import imread
from tensorflow.keras.models import load_model
import cv2

loaded_model = load_model('Model')


unknown_image = imread('image.jpg')
unknown_image.shape   # You will see (1024,1024) image


img = cv2.resize(unknown_image, (224, 224))
preds = loaded_model.predict(img.reshape(1, 224, 224, 1))

result = None

if preds <= 0.5:
    print("The cancer is Malignant")
    result = False
else:
    print("The cancer is Benign")
    result = True

# localhost:3000/result?true
# localhost:3000/result?false
