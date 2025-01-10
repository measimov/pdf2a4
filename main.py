import process_pdf
import cut_image
import image_ocr
from pathlib import Path
import os

if __name__ == "__main__":
    pdf_files = [f for f in os.listdir('.') if f.endswith('.pdf')]
    for pdf_document in pdf_files:
        print(f"\n开始处理PDF文件: {pdf_document}")
        process_pdf.extract_images_from_pdf(pdf_document)
    image_dir = Path("extracted_images")
    image_ocr.delete_watermark_images_and_correct_orientation(image_dir)
    # 示例调用
    # 处理image_dir下的所有图片
    image_files = [f for f in os.listdir(image_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]
    for image_file in image_files:
        input_path = image_dir / image_file
        output_prefix = image_dir / Path(image_file).stem
        cut_image.detect_columns(str(input_path), str(output_prefix))

    image_files = [f for f in os.listdir(image_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]
    for image_file in image_files:
        input_path = image_dir / image_file
        image_ocr.check_text_content(input_path)
