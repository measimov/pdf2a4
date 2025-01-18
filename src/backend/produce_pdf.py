from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from PIL import Image

def images_to_pdf(image_paths, output_pdf):
    # A4 页面宽高（点）
    page_width, page_height = A4

    # 创建 PDF 文档
    c = canvas.Canvas(output_pdf, pagesize=A4)

    # 预处理所有图片的尺寸信息
    images_info = []
    for image_path in image_paths:
        img = Image.open(image_path)
        img_width, img_height = img.size
        scale = min(page_width / img_width, page_height / img_height)
        new_width = img_width * scale
        new_height = img_height * scale
        images_info.append({
            'path': image_path,
            'width': new_width,
            'height': new_height
        })

    i = 0
    while i < len(images_info):
        current_img = images_info[i]
        
        # 检查是否可以与下一张图片合并到同一页
        if (i + 1 < len(images_info) and 
            current_img['width'] <= page_width / 2 and 
            images_info[i + 1]['width'] <= page_width / 2):
            
            next_img = images_info[i + 1]
            
            # 第一张图片放在左边
            x1 = (page_width/2 - current_img['width']) / 2
            y1 = (page_height - current_img['height']) / 2
            c.drawImage(current_img['path'], x1, y1, 
                       width=current_img['width'], 
                       height=current_img['height'])
            
            # 第二张图片放在右边
            x2 = page_width/2 + (page_width/2 - next_img['width']) / 2
            y2 = (page_height - next_img['height']) / 2
            c.drawImage(next_img['path'], x2, y2,
                       width=next_img['width'],
                       height=next_img['height'])
            
            c.showPage()
            i += 2  # 跳过下一张图片
            
        else:
            # 单张图片居中显示
            x = (page_width - current_img['width']) / 2
            y = (page_height - current_img['height']) / 2
            c.drawImage(current_img['path'], x, y,
                       width=current_img['width'],
                       height=current_img['height'])
            
            c.showPage()
            i += 1

    # 保存 PDF
    c.save()
    print(f"PDF 文件已生成：{output_pdf}")
