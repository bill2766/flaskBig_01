import json
import pickle

item_dict = {'static': [0, 0, 0],
             'ground': [81, 0, 81],
             'road': [128, 64, 128],
             'sidewalk': [244, 35, 232],
             'parking': [250, 170, 160],
             'rail track': [230, 150, 140],
             'building': [70, 70, 70],
             'wall': [102, 102, 156],
             'fence': [190, 153, 153],
             'guard rail': [180, 165, 180],
             'bridge': [150, 100, 100],
             'tunnel': [150, 120, 90],
             'pole': [153, 153, 153],
             'traffic light': [250, 170, 30],
             'traffic sign': [220, 220, 0],
             'vegetation': [107, 142, 35],
             'terrain': [152, 251, 152],
             'sky': [70, 130, 180],
             'person': [220, 20, 60],
             'rider': [255, 0, 0],
             'car': [0, 0, 142],
             'truck': [0, 0, 70],
             'bus': [0, 60, 100],
             'caravan': [0, 0, 90],
             'trailer': [0, 0, 110],
             'train': [0, 80, 100],
             'motorcycle': [0, 0, 230],
             'bicycle': [119, 11, 32],
             'license plate': [0, 0, 142]
             }
item_dict_json = json.dumps(item_dict)
with open("./class_config.json","w") as f:
    json.dump(item_dict_json,f)
# print(type(item_dict_json))
# class_dict=json.loads(item_dict_json)
# print(type(class_dict))
