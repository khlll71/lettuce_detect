from rembg import remove
import os,cv2,time



def remove_background(input_dir,output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    image_files = [f for f in os.listdir(input_dir) if f.endswith(('.jpg', '.png', '.jpeg'))]

    for image_file in image_files:
        image_path = os.path.join(input_dir, image_file)
        image = cv2.imread(image_path)

        img = remove(image)

        # Save the extracted green area with the original filename
        output_path = os.path.join(output_dir, image_file)
        cv2.imwrite(output_path, img)

        print(f"Processed {image_file}")



img_dir = "images"
output_path = "image"

remove_background(img_dir,output_path)
