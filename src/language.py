"""
多语言配置模块
支持英文（默认）和中文
"""

import json
import os

# 语言配置文件路径
LANGUAGE_CONFIG_FILE = 'language_config.json'

# 默认语言
DEFAULT_LANGUAGE = 'en'

# 所有支持的语言文本
LANGUAGES = {
    'en': {
        # 窗口标题
        'app_title': 'Image Processing Tool',

        # 菜单栏
        'menu_file': 'File',
        'menu_open': 'Open Image',
        'menu_save': 'Save Image',
        'menu_exit': 'Exit',
        'menu_edit': 'Edit',
        'menu_reset': 'Reset Image',
        'menu_clear_crop': 'Clear Crop Box',
        'menu_language': 'Language',
        'menu_help': 'Help',
        'menu_user_guide': 'User Guide',
        'menu_about': 'About',

        # Canvas标签
        'canvas_label': 'Image Display Area (Left-drag to crop, Right-click to set center)',

        # 像素信息面板
        'pixel_info_title': 'Current Selection Info',
        'pixel_width': 'Width',
        'pixel_height': 'Height',
        'pixel_unit': 'px',

        # 中心点切割面板
        'center_crop_title': 'Center Crop',
        'center_x': 'Center X',
        'center_y': 'Center Y',
        'crop_width': 'Width',
        'crop_height': 'Height',
        'execute_crop': 'Execute Crop',
        'center_crop_hint': 'Tip: Right-click image to set center, or leave blank to use image center',

        # 压缩面板
        'compress_title': 'Image Compression',
        'target_size': 'Target Size',
        'unit_kb': 'KB',
        'unit_mb': 'MB',
        'format_label': 'Format',
        'start_compress': 'Start Compression',
        'compress_result': 'Compression complete! Actual size: {size:.2f} KB',

        # 操作按钮
        'save_button': 'Save Image',
        'preview_button': 'Preview Comparison',

        # 状态栏
        'status_ready': 'Ready',
        'status_loaded': 'Loaded: {filename} | Size: {width}x{height}',
        'status_center_set': 'Center point set: ({x}, {y})',
        'status_crop_complete': 'Center crop complete | New size: {width}x{height}',
        'status_compressing': 'Compressing to {size:.2f} KB...',
        'status_compress_complete': 'Compression complete | Target: {target:.2f} KB, Actual: {actual:.2f} KB',
        'status_saved': 'Saved: {filename}',
        'status_reset': 'Image reset',

        # 对话框
        'warning': 'Warning',
        'error': 'Error',
        'success': 'Success',
        'info': 'Information',

        # 警告消息
        'warn_no_image': 'Please open an image first',
        'warn_no_save': 'No image to save',
        'warn_enter_size': 'Please enter width and height',
        'warn_enter_target_size': 'Please enter target file size',
        'warn_no_preview': 'Please load and process an image first',

        # 错误消息
        'error_open_image': 'Cannot open image: {error}',
        'error_invalid_number': 'Please enter valid numbers',
        'error_crop_failed': 'Crop failed: {error}',
        'error_compress_failed': 'Compression failed: {error}',
        'error_save_failed': 'Save failed: {error}',

        # 成功消息
        'success_crop': 'Crop complete!\nNew size: {width}x{height}',
        'success_save': 'Image saved successfully!',

        # 保存选项对话框
        'save_option_title': 'Save Options',
        'save_option_message': 'Crop box detected. Crop first?\n\nYes: Crop then save\nNo: Save current image\nCancel: Cancel save',

        # 预览窗口
        'preview_title': 'Preview Comparison',
        'preview_header': 'Image Comparison Preview',
        'preview_original': 'Original Image',
        'preview_processed': 'Processed Image',
        'preview_size': 'Size: {width}x{height}',

        # 语言切换
        'language_change_title': 'Language Change',
        'language_change_message': 'Language changed to English!\nPlease restart the application for changes to take effect.',
        'language_chinese': 'Chinese (简体中文)',
        'language_english': 'English',

        # 帮助文本
        'help_title': 'User Guide',
        'help_text': '''Image Processing Tool - User Guide

1. Open Image:
   - Click "File" → "Open Image", or press Ctrl+O

2. Interactive Cropping:
   - Left-click and drag on the image to draw a crop box
   - Drag the corner circles to adjust the crop box size
   - The right panel shows the pixel dimensions

3. Center Crop:
   - Right-click on the image to set the center point (blue crosshair)
   - Enter width and height in the right panel
   - Click "Execute Crop" button
   - If no center point is set, image center is used by default

4. Image Compression:
   - Enter target file size (supports KB/MB)
   - Select output format (JPEG/PNG)
   - Click "Start Compression" button

5. Save Image:
   - Click "Save Image" button, or press Ctrl+S
   - If crop box exists, you'll be asked whether to crop first

6. Preview Comparison:
   - Click "Preview Comparison" to view before/after comparison

Keyboard Shortcuts:
  Ctrl+O: Open Image
  Ctrl+S: Save Image
''',

        # 关于文本
        'about_title': 'About',
        'about_text': '''Image Processing Tool v1.0

Features:
- Interactive Cropping (drag corners to adjust)
- Center Crop (with boundary handling)
- Smart Compression (precise file size control)
- Preview Comparison

Tech Stack:
- Python 3.8+
- Tkinter (GUI)
- Pillow (Image Processing)

Development Date: 2025-11-06
''',
    },

    'zh': {
        # 窗口标题
        'app_title': '图像处理工具',

        # 菜单栏
        'menu_file': '文件',
        'menu_open': '打开图片',
        'menu_save': '保存图片',
        'menu_exit': '退出',
        'menu_edit': '编辑',
        'menu_reset': '重置图片',
        'menu_clear_crop': '清除裁剪框',
        'menu_language': '语言',
        'menu_help': '帮助',
        'menu_user_guide': '使用说明',
        'menu_about': '关于',

        # Canvas标签
        'canvas_label': '图像显示区（左键拖拽裁剪，右键设置中心点）',

        # 像素信息面板
        'pixel_info_title': '当前选区信息',
        'pixel_width': '宽度',
        'pixel_height': '高度',
        'pixel_unit': 'px',

        # 中心点切割面板
        'center_crop_title': '中心点切割',
        'center_x': '中心X',
        'center_y': '中心Y',
        'crop_width': '宽度',
        'crop_height': '高度',
        'execute_crop': '执行切割',
        'center_crop_hint': '提示: 点击图片设置中心点，或留空使用图像中心',

        # 压缩面板
        'compress_title': '图像压缩',
        'target_size': '目标大小',
        'unit_kb': 'KB',
        'unit_mb': 'MB',
        'format_label': '格式',
        'start_compress': '开始压缩',
        'compress_result': '压缩完成！实际大小: {size:.2f} KB',

        # 操作按钮
        'save_button': '保存图片',
        'preview_button': '预览对比',

        # 状态栏
        'status_ready': '就绪',
        'status_loaded': '已加载: {filename} | 尺寸: {width}x{height}',
        'status_center_set': '中心点已设置: ({x}, {y})',
        'status_crop_complete': '中心点切割完成 | 新尺寸: {width}x{height}',
        'status_compressing': '正在压缩到 {size:.2f} KB...',
        'status_compress_complete': '压缩完成 | 目标: {target:.2f} KB, 实际: {actual:.2f} KB',
        'status_saved': '已保存: {filename}',
        'status_reset': '图片已重置',

        # 对话框
        'warning': '警告',
        'error': '错误',
        'success': '成功',
        'info': '信息',

        # 警告消息
        'warn_no_image': '请先打开图片',
        'warn_no_save': '没有可保存的图片',
        'warn_enter_size': '请输入裁剪的宽度和高度',
        'warn_enter_target_size': '请输入目标文件大小',
        'warn_no_preview': '请先加载并处理图片',

        # 错误消息
        'error_open_image': '无法打开图片: {error}',
        'error_invalid_number': '请输入有效的数字',
        'error_crop_failed': '切割失败: {error}',
        'error_compress_failed': '压缩失败: {error}',
        'error_save_failed': '保存失败: {error}',

        # 成功消息
        'success_crop': '切割完成！\n新尺寸: {width}x{height}',
        'success_save': '图片保存成功！',

        # 保存选项对话框
        'save_option_title': '保存选项',
        'save_option_message': '检测到裁剪框，是否先执行裁剪？\n\n是：先裁剪再保存\n否：直接保存当前图像\n取消：取消保存',

        # 预览窗口
        'preview_title': '预览对比',
        'preview_header': '图像对比预览',
        'preview_original': '原始图像',
        'preview_processed': '处理后图像',
        'preview_size': '尺寸: {width}x{height}',

        # 语言切换
        'language_change_title': '语言切换',
        'language_change_message': '语言已切换到中文！\n请重启应用以使更改生效。',
        'language_chinese': '中文 (简体中文)',
        'language_english': '英文 (English)',

        # 帮助文本
        'help_title': '使用说明',
        'help_text': '''图像处理工具 - 使用说明

1. 打开图片：
   - 点击 "文件" → "打开图片"，或按 Ctrl+O

2. 交互式裁剪：
   - 在图像上按住左键拖动，绘制裁剪框
   - 拖动四角的圆点可调整裁剪框大小
   - 右侧显示当前选区的像素尺寸

3. 中心点切割：
   - 右键点击图像设置中心点（会显示蓝色十字标记）
   - 在右侧输入裁剪的宽度和高度
   - 点击 "执行切割" 按钮
   - 如不设置中心点，默认使用图像中心

4. 图像压缩：
   - 输入目标文件大小（支持KB/MB）
   - 选择输出格式（JPEG/PNG）
   - 点击 "开始压缩" 按钮

5. 保存图片：
   - 点击 "保存图片" 按钮，或按 Ctrl+S
   - 如有裁剪框，会询问是否先裁剪

6. 预览对比：
   - 点击 "预览对比" 查看原图和处理后的对比

快捷键：
  Ctrl+O: 打开图片
  Ctrl+S: 保存图片
''',

        # 关于文本
        'about_title': '关于',
        'about_text': '''图像处理工具 v1.0

功能特性：
- 交互式裁剪（拖拽四角调整）
- 中心点切割（支持边界处理）
- 智能压缩（精确控制文件大小）
- 预览对比

技术栈：
- Python 3.8+
- Tkinter (GUI)
- Pillow (图像处理)

开发日期：2025-11-06
''',
    }
}


class LanguageManager:
    """语言管理器"""

    def __init__(self):
        """初始化语言管理器"""
        self.current_language = self.load_language_config()

    def load_language_config(self):
        """加载语言配置"""
        try:
            if os.path.exists(LANGUAGE_CONFIG_FILE):
                with open(LANGUAGE_CONFIG_FILE, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    return config.get('language', DEFAULT_LANGUAGE)
        except Exception:
            pass
        return DEFAULT_LANGUAGE

    def save_language_config(self, language):
        """保存语言配置"""
        try:
            with open(LANGUAGE_CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump({'language': language}, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Failed to save language config: {e}")

    def set_language(self, language):
        """设置语言"""
        if language in LANGUAGES:
            self.current_language = language
            self.save_language_config(language)
            return True
        return False

    def get(self, key, **kwargs):
        """
        获取文本

        参数:
            key: 文本键
            **kwargs: 格式化参数

        返回:
            格式化后的文本
        """
        text = LANGUAGES.get(self.current_language, LANGUAGES[DEFAULT_LANGUAGE]).get(key, key)
        if kwargs:
            try:
                return text.format(**kwargs)
            except KeyError:
                return text
        return text

    def get_current_language(self):
        """获取当前语言"""
        return self.current_language

    def get_available_languages(self):
        """获取所有可用语言"""
        return list(LANGUAGES.keys())


# 全局语言管理器实例
_language_manager = LanguageManager()


def get_text(key, **kwargs):
    """
    获取文本的快捷函数

    参数:
        key: 文本键
        **kwargs: 格式化参数

    返回:
        文本内容
    """
    return _language_manager.get(key, **kwargs)


def set_language(language):
    """设置语言"""
    return _language_manager.set_language(language)


def get_current_language():
    """获取当前语言"""
    return _language_manager.get_current_language()


def get_language_manager():
    """获取语言管理器实例"""
    return _language_manager
