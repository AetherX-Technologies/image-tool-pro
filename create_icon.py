"""
创建应用图标
生成一个带有图像处理元素的图标
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_app_icon():
    """创建应用图标"""
    # 创建256x256的图标（高清）
    size = 256
    img = Image.new('RGBA', (size, size), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)

    # 背景渐变色（蓝色到紫色）
    for i in range(size):
        # 从上到下渐变
        r = int(33 + (156 - 33) * i / size)  # 从深蓝到紫色
        g = int(150 + (39 - 150) * i / size)
        b = int(243 + (176 - 243) * i / size)
        draw.line([(0, i), (size, i)], fill=(r, g, b, 255))

    # 绘制圆角矩形背景
    margin = 20
    corner_radius = 30

    # 绘制主图标元素 - 代表图像裁剪的框架
    # 外框（白色）
    frame_margin = 50
    frame_width = 8
    draw.rounded_rectangle(
        [frame_margin, frame_margin, size - frame_margin, size - frame_margin],
        radius=corner_radius,
        outline=(255, 255, 255, 255),
        width=frame_width
    )

    # 内框（浅色）
    inner_margin = 70
    draw.rounded_rectangle(
        [inner_margin, inner_margin, size - inner_margin, size - inner_margin],
        radius=corner_radius // 2,
        outline=(255, 255, 255, 200),
        width=4
    )

    # 绘制四个角的控制点（代表裁剪工具）
    corner_size = 20
    corners = [
        (frame_margin, frame_margin),  # 左上
        (size - frame_margin, frame_margin),  # 右上
        (frame_margin, size - frame_margin),  # 左下
        (size - frame_margin, size - frame_margin),  # 右下
    ]

    for cx, cy in corners:
        draw.ellipse(
            [cx - corner_size, cy - corner_size, cx + corner_size, cy + corner_size],
            fill=(255, 100, 100, 255),
            outline=(255, 255, 255, 255),
            width=3
        )

    # 绘制中心十字（代表中心点切割）
    center = size // 2
    cross_size = 30
    cross_width = 6
    draw.line(
        [(center - cross_size, center), (center + cross_size, center)],
        fill=(255, 255, 100, 255),
        width=cross_width
    )
    draw.line(
        [(center, center - cross_size), (center, center + cross_size)],
        fill=(255, 255, 100, 255),
        width=cross_width
    )

    # 绘制中心圆点
    center_dot_size = 8
    draw.ellipse(
        [center - center_dot_size, center - center_dot_size,
         center + center_dot_size, center + center_dot_size],
        fill=(255, 255, 100, 255),
        outline=(255, 255, 255, 255),
        width=2
    )

    # 保存为PNG（高质量）
    png_path = 'assets/icon.png'
    img.save(png_path, 'PNG', quality=100)
    print(f"✓ PNG图标已创建: {png_path}")

    # 保存多个尺寸的ICO文件
    icon_sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
    images = []
    for icon_size in icon_sizes:
        resized = img.resize(icon_size, Image.LANCZOS)
        images.append(resized)

    ico_path = 'assets/icon.ico'
    images[0].save(ico_path, format='ICO', sizes=icon_sizes)
    print(f"✓ ICO图标已创建: {ico_path}")

    # 创建一个小预览图
    preview = img.resize((64, 64), Image.LANCZOS)
    preview_path = 'assets/icon_preview.png'
    preview.save(preview_path, 'PNG')
    print(f"✓ 预览图已创建: {preview_path}")

    return ico_path, png_path

if __name__ == "__main__":
    print("=" * 50)
    print("创建应用图标...")
    print("=" * 50)

    # 确保assets目录存在
    os.makedirs('assets', exist_ok=True)

    try:
        ico_path, png_path = create_app_icon()
        print("\n" + "=" * 50)
        print("✓ 图标创建成功！")
        print("=" * 50)
        print(f"\nICO文件: {ico_path}")
        print(f"PNG文件: {png_path}")
    except Exception as e:
        print(f"\n✗ 创建失败: {str(e)}")
        import traceback
        traceback.print_exc()
