import os
import random
import uuid
from PIL import Image

BASE_CATEGORY = "background"

def get_categories(images_root="images"):
    categories = {}
    for name in os.listdir(images_root):
        path = os.path.join(images_root, name)
        if os.path.isdir(path):
            categories[name] = path
    return categories

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

    filename = f"{uuid.uuid4().hex}.png"
    output_path = os.path.join(output_dir, filename)
    os.makedirs(output_dir, exist_ok=True)
    base_image.save(output_path)
    auto_title = " + ".join([layer["file"].split('.')[0] for layer in selected_layers])
    return filename, selected_layers, auto_title