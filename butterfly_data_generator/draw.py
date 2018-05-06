import cv2

def draw_rect(image, xmin, xmax, ymin, ymax):
    return cv2.rectangle(image, (xmin, ymin), (xmax, ymax), (255, 0, 0), 2)

image = cv2.imread(r'E:\butterfly-recognition\training-set-wild\training-set\JPEGImagesCompressed\IMG_000425.jpg')
image = draw_rect(image,349,491,211,347)
cv2.imshow('image',image)
cv2.waitKey(0)