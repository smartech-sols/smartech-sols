import numpy as np
import cv2
from matplotlib import pyplot as plt

img = cv2.imread("camera.jpg")
mask = cv2.imread("sh_mask.jpg",0)

# Cropping Target
tgt = img [150:800,650:1050]

# resize image
scale_percent =100 # percent of original size
width = int(tgt.shape[1] * scale_percent / 100) 
height = int(tgt.shape[0] * scale_percent / 100) 
dim = (width, height) 
resized = cv2.resize(tgt, dim, interpolation = cv2.INTER_LINEAR) 
print('Resized Dimensions : ',resized.shape)

scale_percent =15 # percent of original size
width = int(mask.shape[1] * scale_percent / 100) 
height = int(mask.shape[0] * scale_percent / 100) 
dim = (width, height) 
template = cv2.resize(mask, dim, interpolation = cv2.INTER_LINEAR) 
print('Resized Dimensions : ',template.shape)


# Perspective Correction
rows,cols,ch = resized.shape
pts1 = np.float32([[80,190],[320,205],[315,600],[70,600]])
pts2 = np.float32([[80,190],[320,195],[300,610],[85,620]])
M = cv2.getPerspectiveTransform(pts1,pts2)
dst = cv2.warpPerspective(resized,M,(400,650))

# Image Correction
gray = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)
blur = cv2.bilateralFilter(gray,5,135,135)

# Template Matching

res = cv2.matchTemplate(blur, template, cv2.TM_CCORR)
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

# create threshold from min val, find where sqdiff is less than thresh
min_thresh = (min_val + 1e-6) * 1.5
match_locations = np.where(res>=0.8)

# draw template match boxes
w, h = template.shape[::-1]
for (x, y) in zip(match_locations[1], match_locations[0]):
    cv2.rectangle(blur, (x, y), (x+w, y+h), 255, 2)

print(match_locations)

# display result

#blur1 = blur.copy()
    #method = eval(meth)
    # Apply template Matching
#res = cv2.matchTemplate(blur1,template,cv2.TM_CCORR)
#threshold = 0.8
##for pt in zip(*loc[::-1]):
    #cv2.rectangle(blur1, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)

plt.subplot(121),plt.imshow(res,cmap = 'gray')
plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(blur,cmap = 'gray')
plt.title('Detected Point'), plt.xticks([]), plt.yticks([])


    #min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
    #if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
    #    top_left = min_loc
    #else :
     #       top_left = max_loc
      #      bottom_right = (top_left[0] + w, top_left[1] + h)
      #      cv2.rectangle(blur1,top_left, bottom_right, 255, 2)
    #plt.subplot(121),plt.imshow(res,cmap = 'gray')
    #plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
    #plt.subplot(122),plt.imshow(blur1,cmap = 'gray')
    #plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
    #plt.suptitle(meth)
    #plt.show() 