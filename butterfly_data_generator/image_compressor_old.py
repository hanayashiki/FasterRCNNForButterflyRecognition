import cv2, numpy as np
import butterfly_data_generator.config as config
import os
from PIL import Image

"`filepath,x1,x1,y1,y2,class_name`"

if __name__ == '__main__':
    data_list_wild = open(config.SOURCE_DATA_LIST, 'r', encoding='utf-8')
    data_list_mode = open(config.SOURCE_DATA_LIST_MODE, 'r', encoding='utf-8')
    data_list = (data_list_wild.read() + data_list_mode.read()).strip().split('\n')

    if os.path.isfile(config.SOURCE_DATA_LIST_COMPRESSED):
        ans = input(config.SOURCE_DATA_LIST_COMPRESSED + " is already here. Continue? y/n")
        if ans.lower() == "y":
            pass
        else:
            exit(0)
    data_list_compressed = open(config.SOURCE_DATA_LIST_COMPRESSED, 'w', encoding='utf-8')
    for line in data_list:
        splitted = line.split(",")
        img_source = splitted[0]

        xmin = int(splitted[1])
        xmax = int(splitted[2])
        ymin = int(splitted[3])
        ymax = int(splitted[4])
        class_name = splitted[5]

        img_name = img_source.split('\\')[-1]
        img_path = os.path.join(config.BASE_WILD_IMAGES_COMPRESSED, img_name)

        (width, height) = Image.open(img_source, "r").size

        ratio = 600 / min(width, height)
        new_height, new_width = int(ratio * height), int(ratio * width)
        xmin, xmax, ymin, ymax = int(xmin * ratio), int(xmax * ratio), int(ymin * ratio), int(ymax * ratio)
        data_list_compressed.write(','.join([img_path, str(xmin), str(ymin), str(xmax), str(ymax), class_name]) + '\n')

        if os.path.exists(img_path):
            print("Exist: " + img_path)
            continue

        img = cv2.imdecode(np.fromfile(img_source,dtype=np.uint8),-1)
        (height, width, _) = img.shape
        # (width, height) = Image.open(img_source).size

        img_compressed = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_CUBIC)
        cv2.imencode('.jpg', img_compressed)[1].tofile(img_path)

        print("Compressed: " + img_path)


    data_list_compressed.close()




