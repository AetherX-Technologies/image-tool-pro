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
    ActionPanel,
    ResizePanel
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
        self.zoom_level = 1.0      # 手动缩放级别
        self.manual_zoom = False   # 是否使用手动缩放

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

        # 创建画布容器（用于容纳画布和滚动条）
        self.canvas_container = tk.Frame(left_frame)
        self.canvas_container.pack(fill='both', expand=True)

        # 创建横向滚动条
        self.h_scrollbar = tk.Scrollbar(self.canvas_container, orient='horizontal')
        self.h_scrollbar.pack(side='bottom', fill='x')

        # 创建纵向滚动条
        self.v_scrollbar = tk.Scrollbar(self.canvas_container, orient='vertical')
        self.v_scrollbar.pack(side='right', fill='y')

        # 创建画布并绑定滚动条
        self.canvas = tk.Canvas(
            self.canvas_container,
            bg='white',
            cursor='crosshair',
            xscrollcommand=self.h_scrollbar.set,
            yscrollcommand=self.v_scrollbar.set
        )
        self.canvas.pack(side='left', fill='both', expand=True)

        # 配置滚动条
        self.h_scrollbar.config(command=self.canvas.xview)
        self.v_scrollbar.config(command=self.canvas.yview)

        # 为画布绑定鼠标滚轮（支持横向和纵向滚动）
        def on_canvas_mousewheel(event):
            if self.manual_zoom and self.current_image:
                # Shift+滚轮 = 横向滚动，普通滚轮 = 纵向滚动
                if event.state & 0x1:  # 检测 Shift 键
                    self.canvas.xview_scroll(int(-1*(event.delta/120)), "units")
                else:
                    self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

        self.canvas.bind("<MouseWheel>", on_canvas_mousewheel)

        # 创建缩放按钮
        self.create_zoom_buttons()

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

        # 绑定鼠标滚轮（递归绑定到所有子控件）
        def on_mousewheel(event):
            canvas_scroll.yview_scroll(int(-1*(event.delta/120)), "units")

        def bind_mousewheel_recursively(widget):
            """递归绑定鼠标滚轮到控件及其所有子控件"""
            widget.bind("<MouseWheel>", on_mousewheel)
            for child in widget.winfo_children():
                bind_mousewheel_recursively(child)

        # 绑定到 canvas_scroll 和所有子控件
        canvas_scroll.bind("<MouseWheel>", on_mousewheel)
        # 保存递归绑定函数供后续使用
        self._bind_mousewheel_to_panel = bind_mousewheel_recursively

        canvas_scroll.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # 添加各个控制面板
        # 1. 像素信息面板
        self.pixel_info_panel = PixelInfoPanel(scrollable_frame, self.apply_interactive_crop)
        self.pixel_info_panel.frame.pack(fill='x', pady=5)

        # 2. 中心点切割面板
        self.center_crop_panel = CenterCropPanel(scrollable_frame, self.on_center_crop)
        self.center_crop_panel.frame.pack(fill='x', pady=5)

        # 3. 压缩面板
        self.compress_panel = CompressPanel(scrollable_frame, self.on_compress)
        self.compress_panel.frame.pack(fill='x', pady=5)

        # 4. 尺寸调整面板
        self.resize_panel = ResizePanel(scrollable_frame, self.on_resize)
        self.resize_panel.frame.pack(fill='x', pady=5)

        # 5. 操作按钮面板
        self.action_panel = ActionPanel(scrollable_frame, self.save_image, self.show_preview)
        self.action_panel.frame.pack(fill='x', pady=5)

        # 递归绑定鼠标滚轮到所有面板（确保所有控件都支持滚动）
        self._bind_mousewheel_to_panel(scrollable_frame)

        # 底部状态栏
        self.status_bar = tk.Label(
            self.root, text="就绪", bd=1, relief='sunken', anchor='w'
        )
        self.status_bar.pack(side='bottom', fill='x')

    def create_zoom_buttons(self):
        """在画布右上角创建缩放按钮（固定位置覆盖层）"""
        # 创建按钮覆盖层Frame（固定在canvas_container右上角）
        button_overlay = tk.Frame(self.canvas_container, bg='')
        button_overlay.place(relx=1.0, rely=0.0, anchor='ne', x=-30, y=10)

        # 重置按钮（最左边）
        self.zoom_reset_btn = tk.Button(
            button_overlay,
            text="1:1",
            font=('Arial', 10, 'bold'),
            width=3,
            height=1,
            command=self.zoom_reset,
            bg='white',
            relief='raised'
        )
        self.zoom_reset_btn.pack(side='left', padx=2)

        # 缩小按钮（中间）
        self.zoom_out_btn = tk.Button(
            button_overlay,
            text="-",
            font=('Arial', 16, 'bold'),
            width=2,
            height=1,
            command=self.zoom_out,
            bg='white',
            relief='raised'
        )
        self.zoom_out_btn.pack(side='left', padx=2)

        # 放大按钮（最右边）
        self.zoom_in_btn = tk.Button(
            button_overlay,
            text="+",
            font=('Arial', 16, 'bold'),
            width=2,
            height=1,
            command=self.zoom_in,
            bg='white',
            relief='raised'
        )
        self.zoom_in_btn.pack(side='left', padx=2)

    def zoom_in(self):
        """放大图像"""
        if self.current_image is None:
            return

        # 每次放大 20%
        self.zoom_level *= 1.2
        self.manual_zoom = True

        # 限制最大缩放 5倍
        if self.zoom_level > 5.0:
            self.zoom_level = 5.0
            messagebox.showinfo(get_text('info'), "Maximum zoom level reached (5x)")
            return

        self.display_image_on_canvas()
        self.update_status(f"Zoom: {self.zoom_level:.1f}x")

    def zoom_out(self):
        """缩小图像"""
        if self.current_image is None:
            return

        # 每次缩小 20%
        self.zoom_level /= 1.2
        self.manual_zoom = True

        # 限制最小缩放 0.1倍
        if self.zoom_level < 0.1:
            self.zoom_level = 0.1
            messagebox.showinfo(get_text('info'), "Minimum zoom level reached (0.1x)")
            return

        self.display_image_on_canvas()
        self.update_status(f"Zoom: {self.zoom_level:.1f}x")

    def zoom_reset(self):
        """重置缩放到适应窗口"""
        if self.current_image is None:
            return

        self.zoom_level = 1.0
        self.manual_zoom = False
        self.display_image_on_canvas()
        self.update_status("Zoom reset")

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

                # 重置缩放级别
                self.zoom_level = 1.0
                self.manual_zoom = False

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

        if self.manual_zoom:
            # 手动缩放模式：根据 zoom_level 缩放
            img_width, img_height = self.current_image.size

            # 首先计算适配Canvas的基础缩放
            base_resized, base_scale, _, _ = \
                image_processor.fit_image_to_canvas(self.current_image, canvas_width, canvas_height)

            # 应用手动缩放级别
            self.scale = base_scale * self.zoom_level
            self.display_width = int(img_width * self.scale)
            self.display_height = int(img_height * self.scale)

            # 缩放图像
            resized_image = self.current_image.resize(
                (self.display_width, self.display_height),
                Image.LANCZOS
            )

            # 手动缩放模式：如果图片大于画布，则左上角对齐；否则居中
            if self.display_width > canvas_width or self.display_height > canvas_height:
                # 图片超出画布，左上角对齐（便于滚动查看）
                self.offset_x = 0
                self.offset_y = 0

                # 设置滚动区域为图片的实际大小，并考虑滚动条占用的空间
                scrollbar_size = 20  # 滚动条大约占用20像素

                # 计算实际需要的滚动区域大小
                scroll_width = self.display_width
                scroll_height = self.display_height

                # 如果垂直滚动条会出现，横向需要额外空间
                if self.display_height > canvas_height:
                    scroll_width = max(scroll_width, self.display_width + scrollbar_size)

                # 如果横向滚动条会出现，纵向需要额外空间
                if self.display_width > canvas_width:
                    scroll_height = max(scroll_height, self.display_height + scrollbar_size)

                self.canvas.config(scrollregion=(0, 0, scroll_width, scroll_height))
            else:
                # 图片小于画布，居中显示
                self.offset_x = (canvas_width - self.display_width) // 2
                self.offset_y = (canvas_height - self.display_height) // 2

                # 重置滚动区域
                self.canvas.config(scrollregion=(0, 0, canvas_width, canvas_height))
        else:
            # 自动适配模式：缩放图像以适配Canvas
            resized_image, self.scale, self.display_width, self.display_height = \
                image_processor.fit_image_to_canvas(self.current_image, canvas_width, canvas_height)

            # 计算居中显示的偏移量
            self.offset_x = (canvas_width - self.display_width) // 2
            self.offset_y = (canvas_height - self.display_height) // 2

            # 重置滚动区域
            self.canvas.config(scrollregion=(0, 0, canvas_width, canvas_height))

        # 转换为PhotoImage
        self.photo_image = ImageTk.PhotoImage(resized_image)

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

    def apply_interactive_crop(self):
        """应用交互式裁剪框"""
        if self.current_image is None:
            messagebox.showwarning(get_text('warning'), get_text('warn_no_image'))
            return

        # 获取裁剪框坐标
        crop_rect = self.crop_tool.get_crop_rect()
        if not crop_rect:
            messagebox.showwarning(get_text('warning'), 'No crop box found')
            return

        try:
            x1, y1, x2, y2 = crop_rect
            # 转换为原始图像坐标（使用正确的坐标转换函数）
            x1_orig, y1_orig = image_processor.canvas_to_image_coords(
                x1, y1, self.offset_x, self.offset_y, self.scale
            )
            x2_orig, y2_orig = image_processor.canvas_to_image_coords(
                x2, y2, self.offset_x, self.offset_y, self.scale
            )

            # 裁剪图片
            cropped = image_processor.crop_image(
                self.current_image, x1_orig, y1_orig, x2_orig, y2_orig
            )

            # 更新当前图像
            self.current_image = cropped
            self.display_image_on_canvas()

            # 清除裁剪框
            self.crop_tool.clear()
            self.pixel_info_panel.clear()

            crop_w, crop_h = cropped.size
            self.update_status(f'Interactive crop applied: {crop_w}x{crop_h}')
            messagebox.showinfo(get_text('success'), get_text('success_interactive_crop', width=crop_w, height=crop_h))

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

    def on_resize(self, target_width, target_height, mode):
        """执行图像尺寸调整"""
        if self.current_image is None:
            messagebox.showwarning(get_text('warning'), get_text('warn_no_image'))
            return False

        try:
            # 获取原始尺寸
            orig_width, orig_height = self.current_image.size

            self.update_status(f"Resizing: {orig_width}×{orig_height} → {target_width}×{target_height}")

            # 根据模式调整尺寸
            if mode == 'stretch':
                # 强制拉伸
                resized = self.current_image.resize(
                    (target_width, target_height),
                    Image.LANCZOS
                )
            elif mode == 'crop':
                # 保持比例，裁剪超出部分
                resized = image_processor.resize_with_crop(
                    self.current_image, target_width, target_height
                )
            elif mode == 'pad':
                # 保持比例，填充空白
                resized = image_processor.resize_with_pad(
                    self.current_image, target_width, target_height
                )
            else:
                messagebox.showerror(get_text('error'), f"Unknown resize mode: {mode}")
                return False

            # 更新当前图像
            self.current_image = resized
            self.display_image_on_canvas()

            # 清除裁剪框
            self.crop_tool.clear()
            self.pixel_info_panel.clear()

            self.update_status(f"Resize complete: {target_width}×{target_height}")
            messagebox.showinfo(get_text('success'), get_text('success_resize', width=target_width, height=target_height))
            return True

        except Exception as e:
            messagebox.showerror(get_text('error'), f"Resize failed: {str(e)}")
            return False

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

        # 设置预览窗口图标
        try:
            icon_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'icon.ico')
            if os.path.exists(icon_path):
                preview_window.iconbitmap(icon_path)
        except Exception:
            pass  # 如果图标加载失败，继续运行

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

        # 重置缩放级别
        self.zoom_level = 1.0
        self.manual_zoom = False

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
