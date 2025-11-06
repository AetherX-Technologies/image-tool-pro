"""
图像处理核心逻辑模块
包含裁剪、压缩、保存等核心功能
"""

import io
from PIL import Image, ImageTk


def load_image(file_path):
    """
    加载图像文件

    参数:
        file_path: 图像文件路径

    返回:
        PIL.Image对象
    """
    try:
        image = Image.open(file_path)
        return image
    except Exception as e:
        raise Exception(f"无法加载图像: {str(e)}")


def fit_image_to_canvas(image, canvas_width, canvas_height):
    """
    缩放图像以适配Canvas，保持宽高比

    参数:
        image: PIL.Image对象
        canvas_width: Canvas宽度
        canvas_height: Canvas高度

    返回:
        (缩放后的PIL.Image对象, 缩放比例, 显示宽度, 显示高度)
    """
    img_width, img_height = image.size

    # 计算缩放比例
    scale_w = canvas_width / img_width
    scale_h = canvas_height / img_height
    scale = min(scale_w, scale_h, 1.0)  # 不放大，只缩小

    # 缩放图像
    new_width = int(img_width * scale)
    new_height = int(img_height * scale)
    resized = image.resize((new_width, new_height), Image.LANCZOS)

    return resized, scale, new_width, new_height


def crop_image(image, x1, y1, x2, y2):
    """
    裁剪图像

    参数:
        image: PIL.Image对象
        x1, y1: 左上角坐标
        x2, y2: 右下角坐标

    返回:
        裁剪后的PIL.Image对象
    """
    # 确保坐标顺序正确
    left = min(x1, x2)
    top = min(y1, y2)
    right = max(x1, x2)
    bottom = max(y1, y2)

    # 边界检查
    img_width, img_height = image.size
    left = max(0, int(left))
    top = max(0, int(top))
    right = min(img_width, int(right))
    bottom = min(img_height, int(bottom))

    return image.crop((left, top, right, bottom))


def center_crop(image, crop_width, crop_height, center_x=None, center_y=None):
    """
    以指定中心点为基准裁剪图像，处理边界情况

    参数:
        image: PIL.Image对象
        crop_width: 裁剪宽度
        crop_height: 裁剪高度
        center_x: 中心点X（默认为图像中心）
        center_y: 中心点Y（默认为图像中心）

    返回:
        裁剪后的PIL.Image对象
    """
    img_width, img_height = image.size

    # 默认中心点为图像中心
    if center_x is None:
        center_x = img_width // 2
    if center_y is None:
        center_y = img_height // 2

    # 计算理想的裁剪区域
    left = center_x - crop_width // 2
    top = center_y - crop_height // 2
    right = left + crop_width
    bottom = top + crop_height

    # 边界处理：计算交集
    left = max(0, left)
    top = max(0, top)
    right = min(img_width, right)
    bottom = min(img_height, bottom)

    # 裁剪
    return image.crop((left, top, right, bottom))


def compress_to_size(image, target_size_kb, format='JPEG'):
    """
    压缩图像到指定文件大小

    参数:
        image: PIL.Image对象
        target_size_kb: 目标文件大小（KB）
        format: 保存格式（JPEG/PNG）

    返回:
        (压缩后的PIL.Image对象, 实际文件大小KB)
    """
    target_size_bytes = target_size_kb * 1024

    # RGB转换（JPEG不支持RGBA）
    work_image = image.copy()
    if format == 'JPEG' and work_image.mode == 'RGBA':
        # 创建白色背景
        background = Image.new('RGB', work_image.size, (255, 255, 255))
        background.paste(work_image, mask=work_image.split()[3])
        work_image = background
    elif format == 'JPEG' and work_image.mode != 'RGB':
        work_image = work_image.convert('RGB')

    # 二分查找最佳质量参数
    quality_min = 1
    quality_max = 95
    best_quality = quality_max
    best_buffer = None

    # 先尝试质量调整
    while quality_min <= quality_max:
        quality = (quality_min + quality_max) // 2

        # 测试当前质量的文件大小
        buffer = io.BytesIO()
        work_image.save(buffer, format=format, quality=quality, optimize=True)
        size = buffer.tell()

        if size <= target_size_bytes:
            best_quality = quality
            best_buffer = buffer
            quality_min = quality + 1  # 尝试更高质量
        else:
            quality_max = quality - 1  # 降低质量

    # 如果仍然超出大小，尝试降低分辨率
    if best_buffer is None or best_buffer.tell() > target_size_bytes:
        scale = 0.9
        while scale > 0.1:
            new_size = (int(work_image.width * scale), int(work_image.height * scale))
            resized = work_image.resize(new_size, Image.LANCZOS)
            buffer = io.BytesIO()
            resized.save(buffer, format=format, quality=best_quality, optimize=True)

            if buffer.tell() <= target_size_bytes:
                best_buffer = buffer
                work_image = resized
                break

            scale -= 0.1

    # 如果找到了合适的压缩结果
    if best_buffer:
        best_buffer.seek(0)
        compressed_image = Image.open(best_buffer)
        compressed_image.load()  # 确保图像数据已加载
        actual_size_kb = best_buffer.tell() / 1024
        return compressed_image, actual_size_kb

    # 如果无法压缩到目标大小，返回尽可能小的版本
    buffer = io.BytesIO()
    work_image.save(buffer, format=format, quality=1, optimize=True)
    buffer.seek(0)
    compressed_image = Image.open(buffer)
    compressed_image.load()
    actual_size_kb = buffer.tell() / 1024

    return compressed_image, actual_size_kb


def save_image(image, file_path, format=None, quality=95):
    """
    保存图像

    参数:
        image: PIL.Image对象
        file_path: 保存路径
        format: 保存格式（None表示根据文件扩展名自动判断）
        quality: 保存质量（1-100）
    """
    try:
        # 处理JPEG格式的RGBA图像
        if format == 'JPEG' or (format is None and file_path.lower().endswith('.jpg')):
            if image.mode == 'RGBA':
                background = Image.new('RGB', image.size, (255, 255, 255))
                background.paste(image, mask=image.split()[3])
                image = background
            elif image.mode != 'RGB':
                image = image.convert('RGB')

        if format:
            image.save(file_path, format=format, quality=quality, optimize=True)
        else:
            image.save(file_path, quality=quality, optimize=True)

        return True
    except Exception as e:
        raise Exception(f"保存图像失败: {str(e)}")


def canvas_to_image_coords(canvas_x, canvas_y, offset_x, offset_y, scale):
    """
    将Canvas坐标转换为原图坐标

    参数:
        canvas_x, canvas_y: Canvas坐标
        offset_x, offset_y: 图像在Canvas上的偏移量
        scale: 缩放比例

    返回:
        (原图x坐标, 原图y坐标)
    """
    real_x = (canvas_x - offset_x) / scale
    real_y = (canvas_y - offset_y) / scale
    return int(real_x), int(real_y)


def image_to_canvas_coords(img_x, img_y, offset_x, offset_y, scale):
    """
    将原图坐标转换为Canvas坐标

    参数:
        img_x, img_y: 原图坐标
        offset_x, offset_y: 图像在Canvas上的偏移量
        scale: 缩放比例

    返回:
        (Canvas x坐标, Canvas y坐标)
    """
    canvas_x = img_x * scale + offset_x
    canvas_y = img_y * scale + offset_y
    return int(canvas_x), int(canvas_y)
