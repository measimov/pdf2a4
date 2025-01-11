import cv2
import numpy as np

def detect_columns(image_path, output_prefix):
    # 读取图片
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 二值化（Otsu 阈值）
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # 计算垂直投影
    vertical_projection = np.sum(binary, axis=0)  # 对每一列求和

    # 查找列的分隔线（投影值接近 0 的位置）
    column_boundaries = []
    threshold = 10  # 设定一个阈值，低于该值视为空白
    in_column = False
    for i, value in enumerate(vertical_projection):
        if value > threshold and not in_column:
            column_boundaries.append(i)  # 起始边界
            in_column = True
        elif value <= threshold and in_column:
            column_boundaries.append(i)  # 结束边界
            in_column = False

    # 确保最后一列有结束边界
    if len(column_boundaries) % 2 != 0:
        column_boundaries.append(binary.shape[1])  # 添加图像宽度作为最后一列的结束边界
        print(f"Added image width as final boundary: {binary.shape[1]}")

    # 打印检测到的边界，用于调试
    print(f"Detected boundaries: {column_boundaries}")

    # 保存每一列
    for i in range(0, len(column_boundaries), 2):
        if i + 1 >= len(column_boundaries):
            break  # 防止索引越界
        x_start = column_boundaries[i]
        x_end = column_boundaries[i + 1]
        column_image = image[:, x_start:x_end]  # 裁剪每一列
        output_path = f"{output_prefix}_column_{i//2 + 1}.png"
        cv2.imwrite(output_path, column_image)
        print(f"Saved column {i//2 + 1} as {output_path}")

    # # 可视化投影结果
    # projection_image = np.zeros_like(binary)
    # for x, value in enumerate(vertical_projection):
    #     cv2.line(projection_image, (x, 0), (x, int(value // 255)), (255, 255, 255), 1)
    # cv2.imwrite(f"{output_prefix}_projection.png", projection_image)
    # print(f"Saved vertical projection visualization as {output_prefix}_projection.png")
