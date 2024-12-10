from PIL import Image
from random import choice
import os

PARTS_DIR_LIST = ['Бороды', 'Глаза',  'Макушка', 'Рты', 'Уши']


def generate_random():
    base_layer = Image.open('template.png').convert('RGBA')
    for parts_dir in PARTS_DIR_LIST:
        part_dir_path = os.path.join(os.getcwd(), parts_dir)
        parts_list = os.listdir(part_dir_path)
        part_filename = choice(parts_list)
        part_layer = Image.open(os.path.join(part_dir_path, part_filename)).convert('RGBA')
        base_layer.alpha_composite(part_layer)
    base_layer.show()

generate_random()




