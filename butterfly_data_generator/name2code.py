import json
import re

names = [re.findall(r'[\u4e00-\u9fa5]+', x)[0] for x in open("source/butterfly_species_names.txt", "r", encoding="utf-8").read().strip().split("\n")]
codes = [x[:-5] for x in open("source/butterfly_species_codes.txt", "r", encoding="utf-8").read().strip().split("\n")]

name2code = dict(zip(names, codes))

open("source/name2code.json", "w", encoding="utf-8").write(json.dumps(name2code, indent=2, ensure_ascii=False))