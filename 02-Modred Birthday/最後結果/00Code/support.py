from csv import reader
from os import read
from os import walk

def import_csv_layout(path):
    # 不能進去的位置
    terrain_map = []
    with open(path) as level_map:
        layout = reader(level_map,delimiter=',') # delimiter分隔符
        for row in layout:
            terrain_map.append(list(row))
        return terrain_map

# def import_house(path):
#     for _,_,img_files in walk(path):
#         for image in img_files:
#             print(image)

# print(import_house('./03graphics'))
# print(import_csv_layout('./03graphics/block.csv'))