"""
PyInstaller打包脚本
自动生成EXE可执行文件
"""

import os
import subprocess
import shutil

def clean_build_files():
    """清理旧的构建文件"""
    print("清理旧的构建文件...")
    dirs_to_remove = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_remove:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"  ✓ 已删除: {dir_name}")

    # 删除spec文件
    if os.path.exists('ImageProcessor.spec'):
        os.remove('ImageProcessor.spec')
        print("  ✓ 已删除: ImageProcessor.spec")

def build_exe():
    """构建EXE文件"""
    print("\n" + "="*50)
    print("开始打包EXE...")
    print("="*50)

    # PyInstaller命令
    cmd = [
        'pyinstaller',
        '--name=ImageProcessor',           # 应用名称
        '--onefile',                        # 打包成单个文件
        '--windowed',                       # 无控制台窗口
        '--icon=assets/icon.ico',          # 应用图标
        '--add-data=assets;assets',        # 包含assets文件夹
        '--hidden-import=PIL._tkinter_finder',  # 隐藏导入
        '--noconsole',                      # 不显示控制台
        'main.py'                           # 主程序
    ]

    print("\n执行命令:")
    print(" ".join(cmd))
    print()

    # 执行打包
    result = subprocess.run(cmd, capture_output=False)

    if result.returncode == 0:
        print("\n" + "="*50)
        print("✓ 打包成功！")
        print("="*50)

        # 检查输出文件
        exe_path = os.path.join('dist', 'ImageProcessor.exe')
        if os.path.exists(exe_path):
            size_mb = os.path.getsize(exe_path) / (1024 * 1024)
            print(f"\nEXE文件位置: {exe_path}")
            print(f"文件大小: {size_mb:.2f} MB")

            # 创建发布文件夹
            print("\n创建发布包...")
            create_release_package()

            return True
        else:
            print("\n✗ 错误: 找不到生成的EXE文件")
            return False
    else:
        print("\n" + "="*50)
        print("✗ 打包失败！")
        print("="*50)
        return False

def create_release_package():
    """创建发布包"""
    release_dir = 'ImageProcessor_Release'

    # 创建发布目录
    if os.path.exists(release_dir):
        shutil.rmtree(release_dir)
    os.makedirs(release_dir)

    # 复制EXE文件
    shutil.copy('dist/ImageProcessor.exe', release_dir)

    # 复制README
    if os.path.exists('README.md'):
        shutil.copy('README.md', release_dir)

    # 复制QUICKSTART
    if os.path.exists('QUICKSTART.md'):
        shutil.copy('QUICKSTART.md', release_dir)

    # 创建使用说明
    create_user_guide(release_dir)

    print(f"✓ 发布包已创建: {release_dir}/")
    print("\n包含文件:")
    for item in os.listdir(release_dir):
        print(f"  - {item}")

def create_user_guide(release_dir):
    """创建用户指南"""
    guide_content = """# Image Processing Tool - User Guide

## Quick Start

1. **Run the Application**
   - Double-click `ImageProcessor.exe`
   - No installation required!

2. **Open an Image**
   - Click `File → Open Image` (or press Ctrl+O)
   - Select a JPG or PNG file

3. **Process Your Image**
   - **Interactive Cropping**: Left-click and drag to draw a crop box
   - **Center Crop**: Right-click to set center point, enter dimensions
   - **Compression**: Enter target file size and format
   - **Save**: Click `Save Image` button (or press Ctrl+S)

## Features

- ✓ Interactive cropping with adjustable corners
- ✓ Center-point based cropping
- ✓ Smart compression (precise file size control)
- ✓ Preview comparison
- ✓ Multi-language support (English/Chinese)

## Language Settings

- Menu: `Language → English` or `Chinese (简体中文)`
- Restart the app after changing language

## Keyboard Shortcuts

- `Ctrl+O`: Open Image
- `Ctrl+S`: Save Image
- `Left-drag`: Draw crop box
- `Right-click`: Set center point

## System Requirements

- Windows 7/8/10/11
- No Python required
- Works standalone

## Troubleshooting

**Q: The app won't start?**
A: Make sure you have .NET Framework installed

**Q: Can't open certain image formats?**
A: Supported formats: JPG, PNG, BMP, GIF

**Q: Language setting not working?**
A: Restart the application after changing language

## Support

For issues or suggestions, please report at:
https://github.com/anthropics/claude-code/issues

---

Version: 1.0
Build Date: 2025-11-06
"""

    guide_path = os.path.join(release_dir, 'USER_GUIDE.txt')
    with open(guide_path, 'w', encoding='utf-8') as f:
        f.write(guide_content)

def main():
    """主函数"""
    print("="*50)
    print("图像处理工具 - EXE打包脚本")
    print("="*50)

    # 确保在正确的目录
    if not os.path.exists('main.py'):
        print("✗ 错误: 找不到main.py文件")
        print("  请确保在项目根目录运行此脚本")
        return

    # 确保assets目录存在
    if not os.path.exists('assets/icon.ico'):
        print("✗ 错误: 找不到assets/icon.ico文件")
        return

    # 清理旧文件
    clean_build_files()

    # 构建EXE
    success = build_exe()

    if success:
        print("\n" + "="*50)
        print("打包完成！")
        print("="*50)
        print("\n你可以将 'ImageProcessor_Release' 文件夹分发给用户")
        print("用户只需双击 ImageProcessor.exe 即可运行")
    else:
        print("\n请检查错误信息并重试")

if __name__ == "__main__":
    main()
