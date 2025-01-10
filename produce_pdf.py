from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from PIL import Image
import os

def images_to_pdf(image_paths, output_pdf):
    # A4 页面宽高（点）
    page_width, page_height = A4

    # 创建 PDF 文档
    c = canvas.Canvas(output_pdf, pagesize=A4)

    for image_path in image_paths:
        # 打开图片并获取尺寸
        img = Image.open(image_path)
        img_width, img_height = img.size

        # 计算图片适应 A4 页面时的缩放比例
        scale = min(page_width / img_width, page_height / img_height)

        # 缩放后的图片尺寸
        new_width = img_width * scale
        new_height = img_height * scale

        # 图片放置的位置（居中）
        x = (page_width - new_width) / 2
        y = (page_height - new_height) / 2

        # 绘制图片到 PDF
        c.drawImage(image_path, x, y, width=new_width, height=new_height)

        # 添加新页
        c.showPage()

    # 保存 PDF
    c.save()
    print(f"PDF 文件已生成：{output_pdf}")

# 示例调用
image_folder = "extracted_images"  # 拆分图片的文件夹
image_files = [os.path.join(image_folder, f) for f in sorted(os.listdir(image_folder)) if f.endswith(".png") or f.endswith(".jpg")]
output_pdf = "output.pdf"
images_to_pdf(image_files, output_pdf)
