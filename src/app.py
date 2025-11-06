"""
主应用窗口
整合所有功能模块，提供完整的用户界面
"""

import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os

from . import image_processor
from .crop_tool import CropTool
from .ui_components import (
    PixelInfoPanel,
    CenterCropPanel,
    CompressPanel,
    ActionPanel
)
from .language import get_text, set_language, get_current_language


class ImageProcessorApp:
    """图像处理应用主窗口类"""

    def __init__(self, root):
        """
        初始化应用

        参数:
            root: tkinter根窗口
        """
        self.root = root
        self.root.title(get_text('app_title'))
        self.root.geometry("1200x700")

        # 设置应用图标
        try:
            icon_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'icon.ico')
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
        except Exception:
            pass  # 如果图标加载失败，继续运行

        # 图像数据
        self.original_image = None  # 原始图像
        self.current_image = None   # 当前处理后的图像
        self.display_image = None   # 显示在Canvas上的图像
        self.photo_image = None     # PhotoImage对象（用于Canvas显示）

        # 显示参数
        self.scale = 1.0           # 缩放比例
        self.offset_x = 0          # 图像在Canvas上的X偏移
        self.offset_y = 0          # 图像在Canvas上的Y偏移
        self.display_width = 0     # 显示宽度
        self.display_height = 0    # 显示高度

        # 中心点
        self.center_point = None   # (x, y) 原图坐标

        # 创建UI
        self.create_menu()
        self.create_ui()

        # 初始化裁剪工具
        self.crop_tool = CropTool(self.canvas, callback=self.on_crop_changed)

        # 绑定Canvas点击事件（用于设置中心点）
        self.canvas.bind("<Button-3>", self.on_canvas_right_click)  # 右键设置中心点

        # 状态栏
        self.update_status(get_text('status_ready'))

    def create_menu(self):
        """创建菜单栏"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # 文件菜单
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=get_text('menu_file'), menu=file_menu)
        file_menu.add_command(label=get_text('menu_open'), command=self.open_image, accelerator="Ctrl+O")
        file_menu.add_command(label=get_text('menu_save'), command=self.save_image, accelerator="Ctrl+S")
        file_menu.add_separator()
        file_menu.add_command(label=get_text('menu_exit'), command=self.root.quit)

        # 编辑菜单
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=get_text('menu_edit'), menu=edit_menu)
        edit_menu.add_command(label=get_text('menu_reset'), command=self.reset_image)
        edit_menu.add_command(label=get_text('menu_clear_crop'), command=self.clear_crop)

        # 语言菜单
        language_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=get_text('menu_language'), menu=language_menu)
        language_menu.add_command(label=get_text('language_english'), command=lambda: self.change_language('en'))
        language_menu.add_command(label=get_text('language_chinese'), command=lambda: self.change_language('zh'))

        # 帮助菜单
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=get_text('menu_help'), menu=help_menu)
        help_menu.add_command(label=get_text('menu_user_guide'), command=self.show_help)
        help_menu.add_command(label=get_text('menu_about'), command=self.show_about)

        # 绑定快捷键
        self.root.bind('<Control-o>', lambda e: self.open_image())
        self.root.bind('<Control-s>', lambda e: self.save_image())

    def create_ui(self):
        """创建用户界面"""
        # 主容器
        main_container = tk.Frame(self.root)
        main_container.pack(fill='both', expand=True)

        # 左侧：Canvas图像显示区
        left_frame = tk.Frame(main_container, bg='lightgray')
        left_frame.pack(side='left', fill='both', expand=True, padx=5, pady=5)

        canvas_label = tk.Label(left_frame, text=get_text('canvas_label'), bg='lightgray')
        canvas_label.pack()

        self.canvas = tk.Canvas(left_frame, bg='white', cursor='crosshair')
        self.canvas.pack(fill='both', expand=True)

        # 右侧：控制面板
        right_frame = tk.Frame(main_container, width=300)
        right_frame.pack(side='right', fill='y', padx=5, pady=5)
        right_frame.pack_propagate(False)

        # 创建滚动区域
        canvas_scroll = tk.Canvas(right_frame)
        scrollbar = tk.Scrollbar(right_frame, orient="vertical", command=canvas_scroll.yview)
        scrollable_frame = tk.Frame(canvas_scroll)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas_scroll.configure(scrollregion=canvas_scroll.bbox("all"))
        )

        canvas_scroll.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas_scroll.configure(yscrollcommand=scrollbar.set)

        canvas_scroll.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # 添加各个控制面板
        # 1. 像素信息面板
        self.pixel_info_panel = PixelInfoPanel(scrollable_frame)
        self.pixel_info_panel.frame.pack(fill='x', pady=5)

        # 2. 中心点切割面板
        self.center_crop_panel = CenterCropPanel(scrollable_frame, self.on_center_crop)
        self.center_crop_panel.frame.pack(fill='x', pady=5)

        # 3. 压缩面板
        self.compress_panel = CompressPanel(scrollable_frame, self.on_compress)
        self.compress_panel.frame.pack(fill='x', pady=5)

        # 4. 操作按钮面板
        self.action_panel = ActionPanel(scrollable_frame, self.save_image, self.show_preview)
        self.action_panel.frame.pack(fill='x', pady=5)

        # 底部状态栏
        self.status_bar = tk.Label(
            self.root, text="就绪", bd=1, relief='sunken', anchor='w'
        )
        self.status_bar.pack(side='bottom', fill='x')

    def open_image(self):
        """打开图片文件"""
        file_path = filedialog.askopenfilename(
            title="选择图片",
            filetypes=[
                ("图片文件", "*.jpg *.jpeg *.png *.bmp *.gif"),
                ("JPEG文件", "*.jpg *.jpeg"),
                ("PNG文件", "*.png"),
                ("所有文件", "*.*")
            ]
        )

        if file_path:
            try:
                # 加载图像
                self.original_image = image_processor.load_image(file_path)
                self.current_image = self.original_image.copy()

                # 显示图像
                self.display_image_on_canvas()

                # 清除裁剪框和中心点
                self.crop_tool.clear()
                self.crop_tool.clear_center_point()
                self.center_point = None
                self.pixel_info_panel.clear()
                self.compress_panel.clear_result()

                # 更新状态
                width, height = self.original_image.size
                self.update_status(get_text('status_loaded', filename=os.path.basename(file_path), width=width, height=height))

            except Exception as e:
                messagebox.showerror(get_text('error'), get_text('error_open_image', error=str(e)))

    def display_image_on_canvas(self):
        """在Canvas上显示图像"""
        if self.current_image is None:
            return

        # 获取Canvas尺寸
        self.canvas.update()
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        # 缩放图像以适配Canvas
        resized_image, self.scale, self.display_width, self.display_height = \
            image_processor.fit_image_to_canvas(self.current_image, canvas_width, canvas_height)

        # 转换为PhotoImage
        self.photo_image = ImageTk.PhotoImage(resized_image)

        # 计算居中显示的偏移量
        self.offset_x = (canvas_width - self.display_width) // 2
        self.offset_y = (canvas_height - self.display_height) // 2

        # 清空Canvas并显示图像
        self.canvas.delete("all")
        self.canvas.create_image(
            self.offset_x, self.offset_y,
            image=self.photo_image, anchor='nw', tags='image'
        )

    def on_crop_changed(self, x1, y1, x2, y2):
        """裁剪框改变回调"""
        # 转换为原图坐标
        real_x1, real_y1 = image_processor.canvas_to_image_coords(
            x1, y1, self.offset_x, self.offset_y, self.scale
        )
        real_x2, real_y2 = image_processor.canvas_to_image_coords(
            x2, y2, self.offset_x, self.offset_y, self.scale
        )

        # 更新像素信息显示
        self.pixel_info_panel.update(real_x1, real_y1, real_x2, real_y2)

    def on_canvas_right_click(self, event):
        """Canvas右键点击事件 - 设置中心点"""
        if self.current_image is None:
            return

        # 转换为原图坐标
        real_x, real_y = image_processor.canvas_to_image_coords(
            event.x, event.y, self.offset_x, self.offset_y, self.scale
        )

        # 检查是否在图像范围内
        img_width, img_height = self.current_image.size
        if 0 <= real_x < img_width and 0 <= real_y < img_height:
            self.center_point = (real_x, real_y)
            self.crop_tool.draw_center_point(event.x, event.y)
            self.center_crop_panel.set_center_point(real_x, real_y)
            self.update_status(get_text('status_center_set', x=real_x, y=real_y))

    def on_center_crop(self, width, height, center_x, center_y):
        """执行中心点切割"""
        if self.current_image is None:
            messagebox.showwarning(get_text('warning'), get_text('warn_no_image'))
            return

        try:
            # 使用设置的中心点或默认中心
            if center_x is None or center_y is None:
                img_width, img_height = self.current_image.size
                center_x = img_width // 2
                center_y = img_height // 2

            # 执行中心点裁剪
            cropped = image_processor.center_crop(
                self.current_image, width, height, center_x, center_y
            )

            # 更新当前图像
            self.current_image = cropped
            self.display_image_on_canvas()

            # 清除裁剪框和中心点
            self.crop_tool.clear()
            self.crop_tool.clear_center_point()
            self.center_point = None

            crop_w, crop_h = cropped.size
            self.update_status(get_text('status_crop_complete', width=crop_w, height=crop_h))
            messagebox.showinfo(get_text('success'), get_text('success_crop', width=crop_w, height=crop_h))

        except Exception as e:
            messagebox.showerror(get_text('error'), get_text('error_crop_failed', error=str(e)))

    def on_compress(self, target_size_kb, format_type):
        """执行图像压缩"""
        if self.current_image is None:
            messagebox.showwarning(get_text('warning'), get_text('warn_no_image'))
            return None

        try:
            # 执行压缩
            self.update_status(get_text('status_compressing', size=target_size_kb))
            compressed, actual_size_kb = image_processor.compress_to_size(
                self.current_image, target_size_kb, format_type
            )

            # 更新当前图像
            self.current_image = compressed
            self.display_image_on_canvas()

            self.update_status(get_text('status_compress_complete', target=target_size_kb, actual=actual_size_kb))
            return actual_size_kb

        except Exception as e:
            messagebox.showerror(get_text('error'), get_text('error_compress_failed', error=str(e)))
            return None

    def save_image(self):
        """保存图片"""
        if self.current_image is None:
            messagebox.showwarning(get_text('warning'), get_text('warn_no_save'))
            return

        # 检查是否有裁剪框
        crop_rect = self.crop_tool.get_crop_rect()
        if crop_rect:
            result = messagebox.askyesnocancel(
                get_text('save_option_title'),
                get_text('save_option_message')
            )
            if result is None:  # 取消
                return
            elif result:  # 是 - 执行裁剪
                x1, y1, x2, y2 = crop_rect
                real_x1, real_y1 = image_processor.canvas_to_image_coords(
                    x1, y1, self.offset_x, self.offset_y, self.scale
                )
                real_x2, real_y2 = image_processor.canvas_to_image_coords(
                    x2, y2, self.offset_x, self.offset_y, self.scale
                )
                self.current_image = image_processor.crop_image(
                    self.current_image, real_x1, real_y1, real_x2, real_y2
                )
                self.display_image_on_canvas()
                self.crop_tool.clear()

        # 选择保存路径
        file_path = filedialog.asksaveasfilename(
            title="保存图片",
            defaultextension=".jpg",
            filetypes=[
                ("JPEG文件", "*.jpg"),
                ("PNG文件", "*.png"),
                ("所有文件", "*.*")
            ]
        )

        if file_path:
            try:
                image_processor.save_image(self.current_image, file_path)
                self.update_status(get_text('status_saved', filename=os.path.basename(file_path)))
                messagebox.showinfo(get_text('success'), get_text('success_save'))
            except Exception as e:
                messagebox.showerror(get_text('error'), get_text('error_save_failed', error=str(e)))

    def show_preview(self):
        """显示预览对比窗口"""
        if self.original_image is None or self.current_image is None:
            messagebox.showwarning(get_text('warning'), get_text('warn_no_preview'))
            return

        # 创建预览窗口
        preview_window = tk.Toplevel(self.root)
        preview_window.title(get_text('preview_title'))
        preview_window.geometry("1000x600")

        # 标题
        title_label = tk.Label(
            preview_window, text=get_text('preview_header'),
            font=('Arial', 14, 'bold')
        )
        title_label.pack(pady=10)

        # 创建对比容器
        compare_frame = tk.Frame(preview_window)
        compare_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # 左侧：原图
        left_frame = tk.Frame(compare_frame)
        left_frame.pack(side='left', fill='both', expand=True, padx=5)

        tk.Label(left_frame, text=get_text('preview_original'), font=('Arial', 12, 'bold')).pack()
        orig_w, orig_h = self.original_image.size
        tk.Label(left_frame, text=get_text('preview_size', width=orig_w, height=orig_h)).pack()

        orig_canvas = tk.Canvas(left_frame, bg='white')
        orig_canvas.pack(fill='both', expand=True, pady=5)

        # 右侧：处理后
        right_frame = tk.Frame(compare_frame)
        right_frame.pack(side='right', fill='both', expand=True, padx=5)

        tk.Label(right_frame, text=get_text('preview_processed'), font=('Arial', 12, 'bold')).pack()
        curr_w, curr_h = self.current_image.size
        tk.Label(right_frame, text=get_text('preview_size', width=curr_w, height=curr_h)).pack()

        curr_canvas = tk.Canvas(right_frame, bg='white')
        curr_canvas.pack(fill='both', expand=True, pady=5)

        # 显示图像
        def display_preview():
            # 原图
            orig_canvas.update()
            orig_resized, _, _, _ = image_processor.fit_image_to_canvas(
                self.original_image,
                orig_canvas.winfo_width(),
                orig_canvas.winfo_height()
            )
            orig_photo = ImageTk.PhotoImage(orig_resized)
            orig_canvas.create_image(
                orig_canvas.winfo_width() // 2,
                orig_canvas.winfo_height() // 2,
                image=orig_photo, anchor='center'
            )
            orig_canvas.image = orig_photo  # 保持引用

            # 处理后
            curr_canvas.update()
            curr_resized, _, _, _ = image_processor.fit_image_to_canvas(
                self.current_image,
                curr_canvas.winfo_width(),
                curr_canvas.winfo_height()
            )
            curr_photo = ImageTk.PhotoImage(curr_resized)
            curr_canvas.create_image(
                curr_canvas.winfo_width() // 2,
                curr_canvas.winfo_height() // 2,
                image=curr_photo, anchor='center'
            )
            curr_canvas.image = curr_photo  # 保持引用

        preview_window.after(100, display_preview)

    def reset_image(self):
        """重置图片到原始状态"""
        if self.original_image is None:
            return

        self.current_image = self.original_image.copy()
        self.display_image_on_canvas()
        self.crop_tool.clear()
        self.crop_tool.clear_center_point()
        self.center_point = None
        self.pixel_info_panel.clear()
        self.compress_panel.clear_result()
        self.update_status(get_text('status_reset'))

    def clear_crop(self):
        """清除裁剪框"""
        self.crop_tool.clear()
        self.pixel_info_panel.clear()

    def update_status(self, message):
        """更新状态栏"""
        self.status_bar.config(text=message)

    def show_help(self):
        """显示使用说明"""
        messagebox.showinfo(get_text('help_title'), get_text('help_text'))

    def show_about(self):
        """显示关于信息"""
        messagebox.showinfo(get_text('about_title'), get_text('about_text'))

    def change_language(self, lang_code):
        """
        切换语言

        参数:
            lang_code: 语言代码 ('en' 或 'zh')
        """
        if set_language(lang_code):
            messagebox.showinfo(
                get_text('language_change_title'),
                get_text('language_change_message')
            )
