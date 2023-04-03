import os
import base64
import numpy as np
import cv2




def extract_img(image):
    image = image[image.find(',')+1:]
    image = np.frombuffer(base64.b64decode(image), np.uint8)
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    cv2.imwrite('smartQ/images/img.jpg', image)
    with open('smartQ/images/img.jpg', 'rb') as f:
        contents = f.read()
    os.remove('smartQ/images/img.jpg')
    
    return contents