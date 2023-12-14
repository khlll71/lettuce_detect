from PIL import Image
import os

input_folder = "images"
output_folder = "out_images"

target_width = 250
target_height = 250

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

image_files = [f for f in os.listdir(input_folder) if f.endswith((".jpg", ".png", ".jpeg"))]

for image_file in image_files:
    input_path = os.path.join(input_folder, image_file)
    output_path = os.path.join(output_folder, image_file)

    try:
        image = Image.open(input_path)
        image.thumbnail((target_width, target_height))
        image.save(output_path)
        print(f"finish {image_file}")
    except Exception as e:
        print(f" {image_file} error：{e}")

print("finish")
