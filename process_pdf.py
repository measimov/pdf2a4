import fitz  # PyMuPDF
import os
from pathlib import Path

def extract_images_from_pdf(pdf_path):
    try:
        # 确保PDF文件存在
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF文件未找到: {pdf_path}")

        # 创建输出目录
        output_dir = Path("extracted_images")
        output_dir.mkdir(exist_ok=True)

        # 打开PDF文件
        doc = fitz.open(pdf_path)
        print(f"正在处理PDF文件: {pdf_path}")
        print(f"总页数: {len(doc)}")

        # 遍历每一页
        for page_number in range(len(doc)):
            print(f"正在处理第 {page_number + 1} 页...")
            for img_index, img in enumerate(doc[page_number].get_images(full=True)):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                
                # 构建输出文件路径
                pdf_name = Path(pdf_path).stem
                output_path = output_dir / f"{pdf_name}_page{page_number+1}_img{img_index+1}.png"
                
                # 保存图片
                with open(output_path, "wb") as f:
                    f.write(image_bytes)
                print(f"已保存图片: {output_path}")

        print("所有图片提取完成！")
        doc.close()

    except fitz.FileDataError:
        print("PDF文件损坏或格式不正确")
    except Exception as e:
        print(f"处理过程中出现错误: {str(e)}")
