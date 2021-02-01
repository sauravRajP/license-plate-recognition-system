import cv2
from keras.models import load_model
import numpy as np

class NpOcr:
    def __init__(self, model_path):
        self.model = load_model(model_path)
        self.id2label = {0: "0", 1: "1", 2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7", 8: "8", 9: "9", 10: "ko",
                         11: "pa"}
        print("Model is loaded")

    def preprocess(self, img):
        #img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        img = cv2.resize(img, (50, 50))
        # kernel = np.ones((3,3),np.uint8)
        # erosion = cv2.erode(gray,kernel,iterations = 2)
        img = img.reshape(-1, img.shape[0],50, 1)

        #img = np.reshape(img, (-1, 50, 50,1))
        return img

    def predict(self, img):
        """
        :param img:  segmented character
        :return: class name
        """
        img = self.preprocess(img)
        out = self.model.predict_classes(img)[0]
        return self.id2label[out]
