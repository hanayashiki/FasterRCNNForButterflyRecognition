import butterfly_data_generator.config as config
import cv2
import numpy as np
import os
import re


def read_img(image_address):
    img = cv2.imdecode(np.fromfile(image_address, dtype=np.uint8), -1)
    return img


def compress(image_address, short_side=600):
    img = read_img(image_address)
    (height, width, _) = img.shape
    shorter_side = min(height, width)
    ratio = short_side / shorter_side
    new_height = int(height * ratio)
    new_width = int(width * ratio)
    img_compressed = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_CUBIC)
    return (img_compressed, ratio)


directory = config.BASE_WILD_IMAGES
dump_directory = config.BASE_WILD_IMAGES_COMPRESSED
linux_dump_directory = config.LINUX_BASE_WILD_IMAGES_COMPRESSED
dump_annotation_win = config.SOURCE_DATA_LIST_COMPRESSED
dump_annotation_linux = config.LINUX_SOURCE_DATA_LIST_COMPRESSED
annotated_source = config.SOURCE_DATA_LIST


def get_annotation():
    f = open(annotated_source, "r", encoding="utf-8")
    annotation_dict = {}
    for line in f:
        (file_path, xmin, xmax, ymin, ymax, class_name) = line.strip().split(',')
        file_name = file_path.split('\\')[-1]
        if file_name not in annotation_dict:
            annotation_dict[file_name] = []
        box_list = annotation_dict[file_name]
        box_list.append((file_path, int(xmin), int(xmax), int(ymin), int(ymax), class_name))
    return annotation_dict


if __name__ == '__main__':
    dump_annotation_win_file = open(dump_annotation_win, "w", encoding="utf-8")
    dump_annotation_linux_file = open(dump_annotation_linux, "w", encoding="utf-8")

    annotation_dict = get_annotation()
    for idx, filename in enumerate(os.listdir(directory)):
        file_path = os.path.join(directory, filename)
        new_file_path = os.path.join(dump_directory, filename)
        img_compressed, ratio = compress(file_path)
        linux_new_file_path = os.path.join(linux_dump_directory, filename)
        if filename in annotation_dict:
            for annotation in annotation_dict[filename]:
                (_, xmin, xmax, ymin, ymax, class_name) = annotation
                new_annotation = ','.join(
                    [str(xmin * ratio), str(xmax * ratio), str(ymin * ratio), str(ymax * ratio), str(class_name)])
        else:
            (height, width, _) = img_compressed.shape
            class_name = re.search(r'_(\S*)\.', filename).group(1)
            new_annotation = ','.join(["0", "0", str(width), str(height), class_name])

        dump_annotation_win_file.write(new_file_path + "," + new_annotation + "\n")
        dump_annotation_linux_file.write(linux_new_file_path.replace("\\", "/") + "," + new_annotation + "\n")

        cv2.imencode('.jpg', img_compressed)[1].tofile(new_file_path)
        print("%d, %s to %s" % (idx, filename, new_file_path))
