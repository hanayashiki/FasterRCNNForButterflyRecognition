import json

class Release:

    def __init__(self):
        self.position_output_file = open("A225_task1.txt", "w", encoding="utf-8")
        self.category_output_file = open("A225_task2.txt", "w", encoding="utf-8")
        self.name2code = json.loads(open("source/name2code.json", encoding="utf-8").read(), encoding="utf-8")
        self.lastcate = ""


    def write_position(self, x1=0, y1=0, x2=0, y2=0):
        x1 = 0 if x1 < 0 else x1
        y1 = 0 if y1 < 0 else y1
        x2 = 0 if x2 < 0 else x2
        y2 = 0 if y2 < 0 else y2
        self.position_output_file.write("%d %d %d %d\n" % (x1, y1, x2, y2))
        self.position_output_file.flush()

    def write_category(self, category_name="Unknown"):
        if category_name in self.name2code:
            code = self.name2code[category_name]
        else:
            code = self.lastcate
        self.category_output_file.write(code + "\n")
        self.category_output_file.flush()
        self.lastcate = code

    def __del__(self):
        self.position_output_file.close()
        self.category_output_file.close()
