from xml.dom import minidom
import os
import butterfly_data_generator.config as config


def get_bound_boxes(root: minidom.Element):
    bound_box = root.getElementsByTagName(name="bndbox")
    assert len(bound_box) == 1
    bound_box: minidom.Element = bound_box[0]
    return [str(bound_box.getElementsByTagName(name="xmin")[0].childNodes[0].data),
            str(bound_box.getElementsByTagName(name="xmax")[0].childNodes[0].data),
            str(bound_box.getElementsByTagName(name="ymin")[0].childNodes[0].data),
            str(bound_box.getElementsByTagName(name="ymax")[0].childNodes[0].data)]


def get_name(root: minidom.Element):
    return str(root.getElementsByTagName(name="name")[0].childNodes[0].data)


def get_objects(root: minidom.Element):
    object_list = []
    for object in root.getElementsByTagName(name='object'):
        box = get_bound_boxes(object)
        name = get_name(object)
        object_list.append(','.join(box) + ',' + name)

    return object_list


def get_file_address(root: minidom.Element, base: str):
    filename = root.getElementsByTagName(name="filename")[0].childNodes[0].data
    return os.path.join(base, str(filename))


def translate_annotation(source_dir: str, result_file: str):
    out = open(result_file, 'w+', encoding='utf-8')
    for root, dirs, files in os.walk(source_dir):
        for annotation in files:
            annotation = open(os.path.join(root, annotation), 'r', encoding='utf-8')
            xml_root = minidom.parse(annotation)
            object_list = get_objects(xml_root)
            for object in object_list:
                new_line = get_file_address(xml_root, config.BASE_WILD_IMAGES) + ',' + object
                # print(new_line)
                out.write(new_line + '\n')

    out.close()

if __name__ == '__main__':
    translate_annotation(config.BASE_WILD_ANNOTATIONS, config.SOURCE_DATA_LIST)
