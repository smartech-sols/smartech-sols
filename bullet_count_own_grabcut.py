import numpy as np
import cv2
from matplotlib import pyplot as plt

img = cv2.imread("camera.jpg")


# Cropping Target

# Grabcut Target
mask = np.zeros(img.shape[:2], np.uint8) 

backgroundModel = np.zeros((1, 65), np.float64) 
foregroundModel = np.zeros((1, 65), np.float64) 

rectangle = (650, 200, 350, 600) 

cv2.grabCut(img, mask, rectangle, 
			backgroundModel, foregroundModel, 
			5, cv2.GC_INIT_WITH_RECT) 

mask2 = np.where((mask == 2)|(mask == 0), 0, 1).astype('uint8') 

cut = img * mask2[:, :, np.newaxis] 
dst = cut [200:800,650:1000]
cut = dst

"""# resize image
scale_percent =100 # percent of original size
width = int(tgt.shape[1] * scale_percent / 100) 
height = int(tgt.shape[0] * scale_percent / 100) 
dim = (width, height) 
resized = cv2.resize(tgt, dim, interpolation = cv2.INTER_LINEAR) 
print('Resized Dimensions : ',resized.shape)""" 

# Perspective Correction
rows,cols,ch = dst.shape
pts1 = np.float32([[80,190],[320,205],[315,600],[70,600]])
pts2 = np.float32([[80,190],[320,195],[300,610],[85,620]])
M = cv2.getPerspectiveTransform(pts1,pts2)
dst = cv2.warpPerspective(dst,M,(350,700))



# Image Correction
gray = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)

blur = cv2.bilateralFilter(gray,5,135,135)

#img_thresholded = cv2.inRange(blur, 60, 140)
ret,th = cv2.threshold(blur, 0,255, cv2.THRESH_OTSU)
#th = cv2.bitwise_not(th)

# Morph Operations
kernel = np.ones((10,10),np.uint8)
opening = cv2.morphologyEx(th, cv2.MORPH_OPEN, kernel)
anded = blur*opening

contours, hierarchy = cv2.findContours(anded.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
print (len(contours))
Bullet_Hits = 0
i = 1
for contour in contours:
    (x,y),radius = cv2.minEnclosingCircle(contour)
    center = (int(x),int(y))
    radius = int(radius)
    area = cv2.contourArea(contour)
    print('Area of Contour No.' ,i, ' = ' ,area)
    if radius < 5 :
        if area < 18 and area >= 8:
            Bullet_Hits = Bullet_Hits + 1
            cv2.circle(dst,center,radius,(0,0,255),2)
            # labelling the circles around the centers, in no particular order.
            position = (center[0] - 10, center[1] + 10)
            text_color = (0, 0, 255)
            cv2.putText(dst, str(i), position, cv2.FONT_HERSHEY_SIMPLEX, 1, text_color, 1)
            i = i + 1
        elif area >= 18 and area < 29:
            Bullet_Hits = Bullet_Hits + 2
            cv2.circle(dst,center,radius,(0,0,255),2)
            # labelling the circles around the centers, in no particular order.
            position = (center[0] - 20, center[1] + 10)
            text_color = (0, 0, 255)
            cv2.putText(dst, str(i), position, cv2.FONT_HERSHEY_SIMPLEX, 1, text_color, 1)
            i = i + 1
            cv2.circle(dst,center,radius,(0,0,255),2)
            # labelling the circles around the centers, in no particular order.
            position = (center[0] - 0, center[1] + 10)
            text_color = (0, 0, 255)
            cv2.putText(dst, str(i), position, cv2.FONT_HERSHEY_SIMPLEX, 1, text_color, 1)
            i = i + 1
        
#print ('Bullet Hits = ',Bullet_Hits)
plt.subplot(121),plt.imshow(img),plt.title('Input')
plt.subplot(122),plt.imshow(cut),plt.title('Output')
plt.show()

#cv2.imshow("Blurred", blur)
#cv2.waitKey(0)
#cv2.imshow("Opening", opening)
#cv2.waitKey(0)
cv2.imshow("Anded Opening & Blurred", anded)
cv2.waitKey(0)
#cv2.imshow("Perspective Corrected & Cropped", dst)
#cv2.waitKey(0)
cv2.imshow("Contours", dst)
cv2.waitKey(0)