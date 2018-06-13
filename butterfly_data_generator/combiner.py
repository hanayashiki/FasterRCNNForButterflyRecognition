import butterfly_data_generator.config as config
import butterfly_data_generator.utils as utils
import os.path

original_dict = utils.get_annotation(config.LINUX_SOURCE_DATA_LIST_COMPRESSED, "original")
augmented_dict = utils.get_annotation(config.AUGMENTED_DATA_LIST, "augmented")

total_dict = {**original_dict, **augmented_dict}

class_dict = {}

def is_mode(file_name):
    return utils.get_source_type(total_dict[file_name]) == "mode"

def is_wild(file_name):
    return utils.get_source_type(total_dict[file_name]) == "wild"

def is_original(file_name):
    return is_mode(file_name) or is_wild(file_name)

def is_augmented(file_name):
    return utils.get_source_type(total_dict[file_name]) == "augmented"

for image_key in total_dict:
    image_value = total_dict[image_key]
    class_name = image_value["box_list"][0][5]
    if class_name not in class_dict:
        class_dict[class_name] = []
    class_dict[class_name].append(image_key)

for class_name in class_dict:
    print("%s: %d" % (class_name, len(class_dict[class_name])))
    print("original: %d" % len([file_name for file_name in class_dict[class_name]
                                if is_original(file_name)]))
    print("augmented: %d" % len([file_name for file_name in class_dict[class_name]
                                if is_augmented(file_name)]))

print("total count: %d" % len(total_dict))
print("original count: %d" % len(original_dict))
print("augmented_dict: %d" % len(augmented_dict))

# 原则：
# test 全部加入 original, 但如果 original 用完了，给 augmented
# train 加入剩余的，至少一张original

test_list = {}
train_list = {}

test_per_kind = 4
train_per_kind = 40

test_set_count = 0
train_set_count = 0
original_train_set_count = 0

for class_name in class_dict:
    test_count = 0
    train_count = 0
    file_list = class_dict[class_name]
    wild_set = set([file_name for file_name in file_list if is_wild(file_name)])
    mode_set = set([file_name for file_name in file_list if is_mode(file_name)])
    augmented_set = set([file_name for file_name in file_list if is_augmented(file_name)])
    # original first, then augment
    if class_name not in test_list:
        test_list[class_name] = []
    if class_name not in train_list:
        train_list[class_name] = []
    for file_name in file_list:
        if test_count < test_per_kind:
            if len(wild_set) > 7:
                test_list[class_name].append(wild_set.pop())
            elif len(mode_set) > 1:
                test_list[class_name].append(mode_set.pop())
            else:
                test_list[class_name].append(augmented_set.pop())
            test_count += 1
            test_set_count += 1
        elif train_count < train_per_kind:
            if len(wild_set) > 0:
                original_train_set_count += 1
                train_list[class_name].append(wild_set.pop())
            elif len(mode_set) > 0:
                original_train_set_count += 1
                train_list[class_name].append(mode_set.pop())
            elif len(augmented_set) > 0:
                train_list[class_name].append(augmented_set.pop())
            train_count += 1
            train_set_count += 1
    for file_name in wild_set:
        original_train_set_count += 1
        train_count += 1
        train_list[class_name].append(file_name)

print(test_list)
print("#test_set: %d" % test_set_count)
print(train_list)
print("#train_set: %d" % train_set_count)
print("original_train_set_count: %d" % original_train_set_count)

# generate source list

output_windows = open(config.MIXED_DATA_LIST, "w", encoding="utf-8")
output_linux = open(config.LINUX_MIXED_DATA_LIST, "w", encoding="utf-8")

def print_from_list(data_list, type):
    for class_name in data_list:
        for file_name in data_list[class_name]:
            file_annotation = total_dict[file_name]["box_list"]
            for tuple in file_annotation:
                info_list = [str(x) for x in tuple]
                info_list[0] = os.path.join(config.LINUX_BASE_WILD_IMAGES_COMPRESSED, file_name)
                output_linux.write((','.join(info_list + [type]) + '\n').replace('\\', '/'))
                info_list[0] = os.path.join(config.BASE_WILD_IMAGES_COMPRESSED, file_name)
                output_windows.write(','.join(info_list + [type]) + '\n')


print_from_list(test_list, 'test')
print_from_list(train_list, 'train')
