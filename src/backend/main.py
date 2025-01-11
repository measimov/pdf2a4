import process_pdf
import cut_image
import image_ocr
import produce_pdf
from pathlib import Path
import os
import shutil
import urllib.parse
from datetime import datetime

def process_single_pdf(pdf_path, processed_folder):
    # 获取原始文件名（不含扩展名和时间戳）
    original_name = Path(pdf_path).stem.rsplit('_', 1)[0]
    # 解码文件名
    original_name = urllib.parse.unquote(original_name)
    
    work_dir = Path(f"work_{original_name}")
    work_dir.mkdir(exist_ok=True)
    
    # 创建原始图片和分割后图片的目录
    raw_images_dir = work_dir / "raw_images"
    raw_images_dir.mkdir(exist_ok=True)
    split_images_dir = work_dir / "split_images" 
    split_images_dir.mkdir(exist_ok=True)
    
    # 1. 提取图片到raw_images目录
    print(f"\n开始处理PDF文件: {pdf_path}")
    process_pdf.extract_images_from_pdf(pdf_path, raw_images_dir)
    
    # 2. 处理水印和旋转
    image_ocr.delete_watermark_images_and_correct_orientation(raw_images_dir)
    
    # 3. 分割图片
    image_files = [f for f in os.listdir(raw_images_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]
    for image_file in image_files:
        input_path = raw_images_dir / image_file
        output_prefix = split_images_dir / Path(image_file).stem
        cut_image.detect_columns(str(input_path), str(output_prefix))
    
    # 4. 检查分割后的图片
    image_files = [f for f in os.listdir(split_images_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]
    for image_file in image_files:
        input_path = split_images_dir / image_file
        image_ocr.check_text_content(input_path)
    
    output_pdf = Path(processed_folder) / f"{original_name}_处理完成.pdf"
    image_files = sorted([f for f in os.listdir(split_images_dir) if f.endswith(('.png', '.jpg', '.jpeg'))])
    image_paths = [str(split_images_dir / f) for f in image_files]
    produce_pdf.images_to_pdf(image_paths, str(output_pdf))
    
    return output_pdf
