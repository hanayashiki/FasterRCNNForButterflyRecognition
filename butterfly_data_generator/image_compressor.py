import cv2
import butterfly_data_generator.config as config
import os
from PIL import Image

if __name__ == '__main__':
    data_list = open(config.SOURCE_DATA_LIST, 'r', encoding='utf-8')
    if os.path.isfile(config.SOURCE_DATA_LIST_COMPRESSED):
        ans = input(config.SOURCE_DATA_LIST_COMPRESSED + " is already here. Continue? y/n")
        if ans.lower() == "y":
            pass
        else:
            exit(1)
    data_list_compressed = open(config.SOURCE_DATA_LIST_COMPRESSED, 'w', encoding='utf-8')
    for line in data_list:
        splitted = line.split(",")
        img_source = splitted[0]
        xmin = int(splitted[1])
        xmax = int(splitted[2])
        ymin = int(splitted[3])
        ymax = int(splitted[4])
        class_name = splitted[5]

        img = cv2.imread(img_source)
        (height, width, _) = img.shape
        # (width, height) = Image.open(img_source).size
        ratio = 600 / min(width, height)
        new_height, new_width = int(ratio * height), int(ratio * width)

       #  img_compressed = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_CUBIC)

        img_name = img_source.split('\\')[-1]
        img_path = os.path.join(config.BASE_WILD_IMAGES_COMPRESSED, img_name)
        # cv2.imwrite(img_path, img_compressed)

        print("Compressed: " + img_path)
        xmin, xmax, ymin, ymax = int(xmin * ratio), int(xmax * ratio), int(ymin * ratio), int(ymax * ratio)
        data_list_compressed.write(','.join([img_path, str(xmin), str(xmax), str(ymin), str(ymax), class_name]))

    data_list_compressed.close()
    data_list.close()




