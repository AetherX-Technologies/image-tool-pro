"""
核心功能测试脚本
测试图像处理模块的关键函数
"""

from PIL import Image
import io
from src import image_processor

def test_image_creation():
    """测试图像创建"""
    print("测试1: 创建测试图像...")
    # 创建一个测试图像
    img = Image.new('RGB', (800, 600), color='red')
    assert img.size == (800, 600)
    print("✓ 图像创建成功")
    return img

def test_fit_to_canvas(img):
    """测试图像缩放适配"""
    print("\n测试2: 图像缩放适配...")
    photo, scale, width, height = image_processor.fit_image_to_canvas(img, 400, 300)
    assert scale == 0.5  # 800x600 缩放到 400x300
    assert width == 400
    assert height == 300
    print(f"✓ 缩放比例: {scale}, 显示尺寸: {width}x{height}")

def test_crop(img):
    """测试裁剪"""
    print("\n测试3: 图像裁剪...")
    cropped = image_processor.crop_image(img, 100, 100, 400, 300)
    assert cropped.size == (300, 200)  # 400-100, 300-100
    print(f"✓ 裁剪后尺寸: {cropped.size}")

def test_center_crop(img):
    """测试中心点裁剪"""
    print("\n测试4: 中心点裁剪...")
    # 默认中心
    cropped = image_processor.center_crop(img, 400, 300)
    assert cropped.size == (400, 300)
    print(f"✓ 默认中心裁剪: {cropped.size}")

    # 指定中心
    cropped = image_processor.center_crop(img, 200, 150, 100, 100)
    print(f"✓ 指定中心裁剪: {cropped.size}")

    # 边界测试
    cropped = image_processor.center_crop(img, 1000, 800, 50, 50)
    print(f"✓ 边界裁剪（超出部分被忽略）: {cropped.size}")

def test_compress(img):
    """测试压缩"""
    print("\n测试5: 图像压缩...")
    compressed, actual_size = image_processor.compress_to_size(img, 50, 'JPEG')
    assert actual_size <= 60  # 允许一定误差
    print(f"✓ 目标50KB, 实际: {actual_size:.2f}KB")

def test_coord_conversion():
    """测试坐标转换"""
    print("\n测试6: 坐标转换...")
    # Canvas坐标 -> 原图坐标
    real_x, real_y = image_processor.canvas_to_image_coords(100, 100, 50, 50, 0.5)
    assert real_x == 100 and real_y == 100
    print(f"✓ Canvas->原图: (100,100) -> ({real_x},{real_y})")

    # 原图坐标 -> Canvas坐标
    canvas_x, canvas_y = image_processor.image_to_canvas_coords(100, 100, 50, 50, 0.5)
    assert canvas_x == 100 and canvas_y == 100
    print(f"✓ 原图->Canvas: (100,100) -> ({canvas_x},{canvas_y})")

def main():
    print("=" * 50)
    print("图像处理核心功能测试")
    print("=" * 50)

    try:
        img = test_image_creation()
        test_fit_to_canvas(img)
        test_crop(img)
        test_center_crop(img)
        test_compress(img)
        test_coord_conversion()

        print("\n" + "=" * 50)
        print("✓ 所有测试通过！")
        print("=" * 50)

    except Exception as e:
        print(f"\n✗ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
