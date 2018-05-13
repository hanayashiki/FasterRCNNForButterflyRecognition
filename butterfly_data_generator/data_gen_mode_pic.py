import os, shutil
import butterfly_data_generator.filename_to_code as filename_to_code
import butterfly_data_generator.config as config
import cv2
import re
from PIL import Image

addr_base = r"E:\butterfly-recognition\第三届中国数据挖掘大赛-蝴蝶模式照片\蝴蝶图库"


fc_dict = filename_to_code.filename_to_code
wild_names = filename_to_code.wild_names

def copy_wild_images():
    included_in_wild_names = 0
    total = 0
    copied = []
    for root, dirs, files in os.walk(addr_base):
        for file in files:
            file_name = file.split('.')[0]
            suffix = file.split('.')[1]
            class_name = fc_dict[file_name]
            total += 1
            if class_name in wild_names:
                included_in_wild_names += 1
                src_path = os.path.join(root, file)
                new_path = os.path.join(config.BASE_WILD_IMAGES, file_name + "_" + class_name + "." + suffix)
                print(new_path)
                shutil.copy(src_path, new_path)
                copied.append(new_path)

    print("included: " + str(included_in_wild_names) + ", total: " + str(total))
    return copied


def annotate_copied_images(copied: list):
    output = open(config.SOURCE_DATA_LIST_MODE, "w", encoding="utf-8")
    for image_addr in copied:
        (width, height) = Image.open(image_addr, "r").size
        class_name = re.search(r'_(\S*)\.', image_addr).group(1)
        output.write("%s,0,%d,0,%d,%s\n" % (image_addr, width, height, class_name))

copied = copy_wild_images()
annotate_copied_images(copied)
