def get_annotation(source_addr, source):
    f = open(source_addr, "r", encoding="utf-8")
    annotation_dict = {}
    for line in f:
        (file_path, xmin, xmax, ymin, ymax, class_name) = line.strip().split(',')
        file_name = file_path.split('/')[-1]
        if file_name not in annotation_dict:
            annotation_dict[file_name] = []
        box_list = annotation_dict[file_name]
        box_list.append((file_path, eval(xmin), eval(xmax), eval(ymin), eval(ymax), class_name, source))
    return annotation_dict

def get_source_type(annotation):
    return annotation[0][6]