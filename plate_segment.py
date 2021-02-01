import cv2
import numpy as np


class NpSegment:
    img = cv2.imread("q.jpg")
    #def segment(self, img):
      
    img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    img = cv2.resize(img, (1000, 1000))

    kernel = np.ones((5, 5), np.uint8)
    erosion = cv2.erode(img, kernel, iterations=3)
    dilate = cv2.dilate(erosion, kernel, iterations=3)
    img = cv2.bilateralFilter(dilate, 9, 80, 80)

    median = cv2.medianBlur(img, 5)
    binary = cv2.threshold(median, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    # getting mask with connectComponents
    #ret, labels = cv2.connectedComponents(binary,connectivity=8)
    nlabel,labels,stats,centroids = cv2.connectedComponentsWithStats(binary,connectivity=8)
    mask1=[]
    segmented = []
    for l in range(1,nlabel):
        if stats[l, cv2.CC_STAT_AREA] >= 1500:

            mask = np.array(labels, dtype=np.uint8)
            mask[labels == l] = 255
            mask1.append(mask)


    for i in range(len(mask1)):
        print(i)
        p = mask1[i]
        m = mask1[i]

        m = cv2.bilateralFilter(m, 19, 300, 300)
        kernel = np.ones((3, 3), np.uint8)
        erosion = cv2.erode(m, kernel, iterations=4)
        m = cv2.dilate(erosion, kernel, iterations=2)
        m = cv2.medianBlur(m, 5)
        opening = cv2.morphologyEx(m, cv2.MORPH_OPEN, kernel)
        thresh = cv2.threshold(opening, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        contours, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
        for c in contours:
            cv2.drawContours(m, c, -1, (0, 0, 255), 3)
            x,y,w,h = cv2.boundingRect(c)
            if (h>150 and h<600) and (w>75 and w<600) :
                cv2.rectangle(p, (x, y), (x + w, y + h), (255, 255, 0), 2)
                print("i am height",h)
                print("i am weidth",w)
                final_img = p[y:y+h,x:x+w]
                cv2.imshow("p"+str(c),p)
                cv2.imshow("segment",final_img)
                segmented.append(final_img)
    cv2.waitKey(0)
        
       # return segmented
