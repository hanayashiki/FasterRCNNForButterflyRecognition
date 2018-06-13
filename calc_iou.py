def get_IoU(rect1, rect2):
    # square1 = (x_min, x_max, y_min, y_max)
    # square2 = (x_min, x_max, y_min, y_max)
    x_cross = min(rect1[1], rect2[1]) - max(rect1[0], rect2[0])
    y_cross = min(rect1[3], rect2[3]) - max(rect1[2], rect2[2])
    if x_cross < 0 or y_cross < 0:
        return 0.
    s1 = (rect1[1] - rect1[0]) * (rect1[3] - rect1[2])
    s2 = (rect2[1] - rect2[0]) * (rect2[3] - rect2[2])
    cross = x_cross * y_cross
    return cross / (s1 + s2 - cross)

if __name__ == '__main__':
    print(get_IoU((0, 1, 0, 1), (1.25, 1.5, 1, 1.5)))