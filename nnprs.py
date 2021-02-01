import cv2
import utils
from plate_detect import NpDetector
#from roi import RoiDetector
from plate_segment import NpSegment
from predict import NpOcr

#print (dir(utils))


class Nnprs:
    def __init__(self):
        self.ocr_model = None
        self.plate_detector_model = None
        #self.roi_detector_model = None
        self.plate_segmentor_model = None
        self.build()

    def build(self):
        self.plate_detector_model = NpDetector()
        #self.roi_detector_model = RoiDetector()
        self.plate_segmentor_model = NpSegment()
        self.ocr_model = NpOcr("numberplate.h5")

    def predict(self, filename):
        """
        :param img: input image
        :return:
        """

        img = cv2.imread(filename)
        #image = self.roi_detector_model.detect(img)
        if img is None:
            return None
        plate, roi = self.plate_detector_model.detect(img)
        if plate is None:
            return None
        segmented = self.plate_segmentor_model.segment(plate)
        if segmented is None:
            return None

        predictions = []
        i=1
        for segment in segmented:

            cv2.imshow("segment"+ str(i),segment)
            pred = self.ocr_model.predict(segment)
            predictions.append(pred)
            i = i+1
        result = ""
        for pred in predictions:
            result += pred + " "
        
        cv2.putText(roi, result, (150,250), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 4)
        cv2.imshow("Result", roi)
        return result


if __name__ == '__main__':
    image_path = "accepted_done"
    images = utils.get_files(image_path, [".jpg", ".png"], shuffle=True)
    model = Nnprs()
    for image in images:
        try:
            print(image)
            result = model.predict(filename=image)
            print(result)
            print("\n\n")
            cv2.waitKey(0)
        except Exception as e:
            print(e)
