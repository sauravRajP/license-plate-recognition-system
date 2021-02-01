import cv2
import numpy as np


class NpDetector:

    def detect(self, img):
        """

        :param img: image array
        :return:
        """
        image = cv2.resize(img,(1200,1200))
        kernel = np.ones((5, 5), np.uint8)
        erosion = cv2.erode(image, kernel, iterations=9)
        dilate = cv2.dilate(erosion, kernel, iterations=9)
        img = cv2.resize(dilate,(1200,1200))
        img = cv2.bilateralFilter(img, 9, 100, 100)
        median = cv2.medianBlur(img, 7)

        hsv = cv2.cvtColor(median, cv2.COLOR_BGR2HSV)

        lower_red = np.array([140, 100, 110])
        upper_red = np.array([240, 255, 255])

        #img = cv2.resize(img,(1000,1000))
        mask = cv2.inRange(hsv, lower_red, upper_red)
        res = cv2.bitwise_and(hsv, image, mask=mask)
        res = cv2.cvtColor(res,cv2.COLOR_BGR2GRAY)
        binary = cv2.threshold(res, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]


        contours, _ = cv2.findContours(binary, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)


        a=[]
        x_max= []
        y_max = []
        xv = []
        yv = []
        countrect=[]
        finalimg=[]
        finalroi = []
        for cnt in contours:
            if cv2.contourArea(cnt)>5000:
                x, y, w, h = cv2.boundingRect(cnt)

                a.append(cv2.contourArea(cnt))
                peri = cv2.arcLength(cnt, True)
                approx = cv2.approxPolyDP(cnt, 0.04 * peri, True)
                if len(approx) == 4:
                    countrect.append(cv2.contourArea(cnt))
        print("i am count rect",len(countrect))
        for contour in contours:
            if cv2.contourArea(contour) > 5000:
                x, y, w, h = cv2.boundingRect(contour)


                if len(a)>1 and len(countrect)==1:
                    peri = cv2.arcLength(contour, True)
                    approx = cv2.approxPolyDP(contour, 0.04 * peri, True)
                    print(len(approx))
                    if len(approx) == 4:
                        final_roi = cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),3)                
                        final_image = image[y:y + h, x:x + w]
                        finalimg.append(final_image)
                        finalroi.append(final_roi)

                elif len(a)>1 and (len(countrect) != 1):
                    minvalueX=[]
                    maxvalueX=[]
                    minvalueY=[]
                    maxvalueY=[]
                    finalh=[]
                    finalw=[]
                    max_x = x + w
                    max_y = y + h
                    x_max.append(max_x)
                    y_max.append(max_y)
                    xv.append(x)
                    yv.append(y)
                    maxvalueX.append(max(max(x_max), max(xv)))
                    minvalueX.append(min(min(x_max), min(xv)))
                    minvalueY.append(min(min(y_max), min(yv)))
                    maxvalueY.append(max(max(y_max), min(yv)))
                    finalh.append(maxvalueY[0] - minvalueY[0])
                    finalw.append(maxvalueX[0] - minvalueX[0])
                    final_roi = cv2.rectangle(image, (minvalueX[0], minvalueY[0]), (minvalueX[0] + finalw[0], minvalueY[0] + finalh[0]), (0, 0, 255), 3)
                    final_image = image[minvalueY[0]:minvalueY[0] + finalh[0], minvalueX[0]:minvalueX[0] + finalw[0]]
                    finalimg.append(final_image)
                    finalroi.append(final_roi)
                    break


                elif(len(a)==1):
                    final_roi = cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 3)
                    
                    final_image=image[y:y+h,x:x+w]
                    finalimg.append(final_image)
                    finalroi.append(final_roi)


                else:
                    print("no contour found")


        #print(finalimg)
        final_image = finalimg[0]
        final_roi = finalroi[0]
        roi = cv2.resize(final_roi,(690,800))
        return final_image,roi



