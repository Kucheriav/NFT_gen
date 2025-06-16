import os
import random
import uuid
from PIL import Image
import hashlib
import json
from crud.nft_crud import is_hash_exists


BASE_CATEGORY = "background"

def get_base_dir():
    # Получаем абсолютный путь к корню проекта (или где images лежит)
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_categories(images_root="images"):
    # images_root — относительный путь (например, "images")
    base_dir = get_base_dir()
    abs_images_root = os.path.join(base_dir, images_root)
    categories = {}
    for name in os.listdir(abs_images_root):
        path = os.path.join(abs_images_root, name)
        if os.path.isdir(path):
            categories[name] = path
    return categories


def get_layers_hash(layers):
    # Упорядочиваем по category, чтобы порядок не влиял на результат
    layers_str = json.dumps(sorted(layers, key=lambda x: x['category']), ensure_ascii=True)
    return hashlib.sha256(layers_str.encode('utf-8')).hexdigest()

def generate_image(output_dir="static/generated", images_root="images", base_category="Фон"):
    selected_layers = []
    categories = get_categories(images_root)
    base_folder = categories[base_category]
    base_files = [f for f in os.listdir(base_folder) if f.endswith(('.png', '.jpg'))]
    if not base_files:
        raise Exception("Нет файлов в базовой категории!")
    base_selected = random.choice(base_files)
    base_path = os.path.join(base_folder, base_selected)
    base_image = Image.open(base_path).convert("RGBA")
    selected_layers.append({"category": base_category, "file": base_selected})

    for category, folder in categories.items():
        if category == base_category:
            continue
        files = [f for f in os.listdir(folder) if f.endswith(('.png', '.jpg'))]
        if not files:
            continue
        selected = random.choice(files)
        img = Image.open(os.path.join(folder, selected)).convert("RGBA")
        base_image = Image.alpha_composite(base_image, img)
        selected_layers.append({"category": category, "file": selected})

    # Генерируем абсолютный путь для сохранения
    base_dir = get_base_dir()
    abs_output_dir = os.path.join(base_dir, output_dir)
    os.makedirs(abs_output_dir, exist_ok=True)
    filename = f"{uuid.uuid4().hex}.png"
    output_path = os.path.join(abs_output_dir, filename)
    base_image.save(output_path)
    auto_title = " + ".join([layer["file"].split('.')[0] for layer in selected_layers])
    return filename, selected_layers, auto_title


def generate_unique_image(db, max_attempts=20):
    for _ in range(max_attempts):
        filename, layers, auto_title = generate_image()
        layers_hash = get_layers_hash(layers)
        if not is_hash_exists(db, layers_hash):
            return filename, layers, auto_title, layers_hash
    raise Exception("Не удалось сгенерировать уникальную картинку")