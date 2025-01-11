import cv2
import os
# 遍历extracted_images文件夹下的所有图片
image_dir = 'extracted_images'
image_files = [f for f in os.listdir(image_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]

for image_file in image_files:
    image_path = os.path.join(image_dir, image_file)
    image = cv2.imread(image_path)

    # 确保图片加载成功
    if image is not None:
        # 获取图片的高度和宽度
        height, width = image.shape[:2]

        # 计算长宽比
        aspect_ratio = height / width
        print(f"图片: {image_file}")
        print(f"宽度: {width}, 高度: {height}, 长宽比: {aspect_ratio:.2f}")
        print("-" * 50)
    else:
        print(f"无法加载图片: {image_file}")
