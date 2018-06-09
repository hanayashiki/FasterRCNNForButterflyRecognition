import cv2
import numpy as np
import random
import json
from math import ceil

test_train_cut_output = open("source/test_train_cut.json", "w", encoding="utf-8")
test_train_cut = {}

def get_data(input_path):
    found_bg = False
    all_imgs = {}

    classes_count = {}

    classes_list = {}

    class_name_list = []

    class_mapping = {}

    visualise = True

    file_count = 0

    random.seed(0)

    with open(input_path, 'r', encoding='utf-8') as f:

        print('Parsing annotation files')

        for line in f:
            line_split = line.strip().split(',')
            (filename, x1, y1, x2, y2, class_name, source, set_name) = line_split

            if class_name not in classes_count:
                classes_list[class_name] = []
                classes_count[class_name] = 1
            else:
                classes_count[class_name] += 1

            if class_name not in class_mapping:
                if class_name == 'bg' and found_bg == False:
                    print(
                        'Found class name with special name bg. Will be treated as a background region (this is usually for hard negative mining).')
                    found_bg = True
                class_name_list.append(class_name)

            if filename not in all_imgs:
                all_imgs[filename] = {}

                img = cv2.imdecode(np.fromfile(filename, dtype=np.uint8), -1)
                file_count += 1
                print("reading: " + str(file_count))
                (rows, cols) = img.shape[:2]
                all_imgs[filename]['filepath'] = filename
                all_imgs[filename]['width'] = cols
                all_imgs[filename]['height'] = rows
                all_imgs[filename]['bboxes'] = []
                if set_name == 'train':
                    all_imgs[filename]['imageset'] = 'trainval'
                elif set_name == 'test':
                    all_imgs[filename]['imageset'] = 'test'

                # if np.random.randint(0,6) > 0:
                # 	all_imgs[filename]['imageset'] = 'trainval'
                # else:
                # 	all_imgs[filename]['imageset'] = 'test'

            all_imgs[filename]['bboxes'].append(
                {'class': class_name, 'x1': int(float(x1)), 'x2': int(float(x2)), 'y1': int(float(y1)), 'y2': int(float(y2))})
            classes_list[class_name].append(all_imgs[filename])

    all_data = []
    for key in all_imgs:
        all_data.append(all_imgs[key])

    # make sure the bg class is last in the list
    class_name_list.sort()
    for idx, class_name in enumerate(class_name_list):
        class_mapping[class_name] = idx

    if found_bg:
        class_mapping['bg'] = len(class_mapping)


    return all_data, classes_count, class_mapping

if __name__ == '__main__':
    get_data("./source/data_list_mixed.txt")
    test_train_cut_output.write(json.dumps(test_train_cut, ensure_ascii=False, indent=2))