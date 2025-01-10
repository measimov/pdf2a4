import pytesseract
from PIL import Image, ImageEnhance
import os
from pathlib import Path

def preprocess_image(image_path):
    image = Image.open(image_path)
    # 增强对比度、灰度化和调整大小
    image = ImageEnhance.Contrast(image).enhance(2.0)
    image = image.convert('L')
    image = image.resize((image.width * 2, image.height * 2), Image.Resampling.LANCZOS)
    return image

def correct_image_orientation(image, output_path):
    try:
        # 检测方向
        osd_data = pytesseract.image_to_osd(image, config='--psm 0')
        rotate_angle = int(osd_data.split("Rotate: ")[1].split("\n")[0])  # 提取旋转角度

        if rotate_angle != 0:
            image = image.rotate(-rotate_angle, expand=True)
            print(f"Image rotated by {rotate_angle} degrees")
        image.save(output_path)
    except pytesseract.TesseractError as e:
        print(f"TesseractError: {e}")


def delete_watermark_images_and_correct_orientation(image_dir):
    # 获取 extracted_images 文件夹下的所有图片
    # image_dir = Path("extracted_images")
    image_files = [f for f in os.listdir(image_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]

    for image_file in image_files:
        
        image = Image.open(image_dir / image_file)
        # OCR 识别
        text = pytesseract.image_to_string(image, lang='eng+chi_sim')  # lang 参数指定语言
        # print(text)
        # 移除所有空格后检查是否包含水印文字
        if "扫描全能王" in text.replace(" ", ""):
            os.remove(image_dir / image_file)
            print(f"检测到水印,已删除图片: {image_file}")
            continue
        correct_image_orientation(image, image_dir / image_file)
        
def check_text_content(image_path):
    image = Image.open(image_path)
    # 重新OCR识别文字内容
    text = pytesseract.image_to_string(image, lang='eng+chi_sim')
    # 移除所有空格和换行符
    text = text.replace(" ", "").replace("\n", "")
    print(f"图片路径: {image_path} 文本长度: {len(text)}")
    aspect_ratio = image.height / image.width
    print(f"长宽比: {aspect_ratio:.2f}")
    # 统计字符数量
    if len(text) < 20 or aspect_ratio > 10:
        os.remove(image_path)
        print(f"检测到文字内容过少或者长宽比过大,已删除图片: {image_path}")
