from PIL import Image
import os

# 输入文件夹和输出文件夹的路径
input_folder = "images"
output_folder = "out_images"

# 目标图像的宽度和高度
target_width = 250
target_height = 250

# 确保输出文件夹存在
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 列出输入文件夹中的所有图像文件
image_files = [f for f in os.listdir(input_folder) if f.endswith((".jpg", ".png", ".jpeg"))]

# 遍历每个图像文件并调整大小
for image_file in image_files:
    input_path = os.path.join(input_folder, image_file)
    output_path = os.path.join(output_folder, image_file)

    try:
        image = Image.open(input_path)
        # 使用thumbnail方法调整图像大小并保持纵横比
        image.thumbnail((target_width, target_height))
        image.save(output_path)
        print(f"已处理 {image_file}")
    except Exception as e:
        print(f"处理 {image_file} 时出错：{e}")

print("图像大小已统一调整完成")
