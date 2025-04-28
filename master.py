from PIL import Image
from random import choice
import os

PARTS_DIR_LIST = ['Бороды', 'Глаза',  'Макушка', 'Рты', 'Уши']


def generate_random_show():
    base_layer = Image.open('template.png').convert('RGBA')
    for parts_dir in PARTS_DIR_LIST:
        part_dir_path = os.path.join(os.getcwd(), parts_dir)
        parts_list = os.listdir(part_dir_path)
        part_filename = choice(parts_list)
        part_layer = Image.open(os.path.join(part_dir_path, part_filename)).convert('RGBA')
        base_layer.alpha_composite(part_layer)
    base_layer.show()


def generate_random_n_save(n:int, folder:str):
    for i in range(1, n + 1):
        base_layer = Image.open('template.png').convert('RGBA')
        for parts_dir in PARTS_DIR_LIST:
            part_dir_path = os.path.join(os.getcwd(), parts_dir)
            parts_list = os.listdir(part_dir_path)
            part_filename = choice(parts_list)
            part_layer = Image.open(os.path.join(part_dir_path, part_filename)).convert('RGBA')
            base_layer.alpha_composite(part_layer)
        base_layer.save(f'{folder}/{i}.png')

