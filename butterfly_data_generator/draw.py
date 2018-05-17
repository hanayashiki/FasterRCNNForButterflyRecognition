import cv2

def draw_rect(image, xmin, ymin, xmax, ymax):
    return cv2.rectangle(image, (xmin, ymin), (xmax, ymax), (255, 0, 0), 2)

image = cv2.imread(r'E:\butterfly-recognition\training-set-wild\training-set\JPEGImagesCompressed\219.jpg')
image = draw_rect(image,290,320,375,393)
cv2.imshow('image',image)
cv2.waitKey(0)