import cv2

def draw_rect(image, xmin, ymin, xmax, ymax):
    return cv2.rectangle(image, (xmin, ymin), (xmax, ymax), (255, 0, 0), 2)

image = cv2.imread(r'E:\butterfly-recognition\training-set-wild\training-set\JPEGImagesCompressed\2250.jpg')
image = draw_rect(image,343,333,432,402)
cv2.imshow('image',image)
cv2.waitKey(0)