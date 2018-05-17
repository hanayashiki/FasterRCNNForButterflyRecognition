import re

def get_annotation(source_addr, source):
    f = open(source_addr, "r", encoding="utf-8")
    annotation_dict = {}
    for line in f:
        (file_path, xmin, xmax, ymin, ymax, class_name) = line.strip().split(',')
        file_name : str = file_path.split('/')[-1]
        if file_name not in annotation_dict:
            annotation_dict[file_name] = {
                "photo_type": "",
                "box_list": []
            }
        box_list = annotation_dict[file_name]["box_list"]
        if file_name.startswith("A"):
            annotation_dict[file_name]["photo_type"] = "mode"
        elif re.match(r"[0-9^].s*",file_name):
            annotation_dict[file_name]["photo_type"] = "augmented"
        else:
            annotation_dict[file_name]["photo_type"] = "wild"
        box_list.append((file_path, eval(xmin), eval(xmax), eval(ymin), eval(ymax), class_name, source))
    return annotation_dict

def get_source_type(annotation):
    return annotation["photo_type"]