"""
UI组件封装
包含像素信息面板、裁剪控制面板、压缩面板等
"""

import tkinter as tk
from tkinter import ttk, messagebox
from .language import get_text


class PixelInfoPanel:
    """像素信息显示面板"""

    def __init__(self, parent_frame):
        """
        初始化像素信息面板

        参数:
            parent_frame: 父容器
        """
        self.frame = tk.LabelFrame(parent_frame, text=get_text('pixel_info_title'), padx=10, pady=10)

        # 创建标签
        self.width_label = tk.Label(self.frame, text=f"{get_text('pixel_width')}: 0 {get_text('pixel_unit')}", font=('Arial', 10))
        self.width_label.pack(anchor='w', pady=2)

        self.height_label = tk.Label(self.frame, text=f"{get_text('pixel_height')}: 0 {get_text('pixel_unit')}", font=('Arial', 10))
        self.height_label.pack(anchor='w', pady=2)

    def update(self, x1, y1, x2, y2):
        """
        更新显示的像素值

        参数:
            x1, y1, x2, y2: 选区坐标
        """
        width = abs(x2 - x1)
        height = abs(y2 - y1)
        self.width_label.config(text=f"{get_text('pixel_width')}: {int(width)} {get_text('pixel_unit')}")
        self.height_label.config(text=f"{get_text('pixel_height')}: {int(height)} {get_text('pixel_unit')}")

    def clear(self):
        """清除显示"""
        self.width_label.config(text=f"{get_text('pixel_width')}: 0 {get_text('pixel_unit')}")
        self.height_label.config(text=f"{get_text('pixel_height')}: 0 {get_text('pixel_unit')}")


class CenterCropPanel:
    """中心点切割控制面板"""

    def __init__(self, parent_frame, on_crop_callback):
        """
        初始化中心点切割面板

        参数:
            parent_frame: 父容器
            on_crop_callback: 执行切割的回调函数
        """
        self.frame = tk.LabelFrame(parent_frame, text=get_text('center_crop_title'), padx=10, pady=10)
        self.on_crop_callback = on_crop_callback

        # 中心点坐标
        center_frame = tk.Frame(self.frame)
        center_frame.pack(fill='x', pady=5)

        tk.Label(center_frame, text=f"{get_text('center_x')}:").grid(row=0, column=0, sticky='w')
        self.center_x_var = tk.StringVar()
        self.center_x_entry = tk.Entry(center_frame, textvariable=self.center_x_var, width=10)
        self.center_x_entry.grid(row=0, column=1, padx=5)

        tk.Label(center_frame, text=f"{get_text('center_y')}:").grid(row=0, column=2, sticky='w', padx=(10, 0))
        self.center_y_var = tk.StringVar()
        self.center_y_entry = tk.Entry(center_frame, textvariable=self.center_y_var, width=10)
        self.center_y_entry.grid(row=0, column=3, padx=5)

        # 裁剪尺寸
        size_frame = tk.Frame(self.frame)
        size_frame.pack(fill='x', pady=5)

        tk.Label(size_frame, text=f"{get_text('crop_width')}:").grid(row=0, column=0, sticky='w')
        self.width_var = tk.StringVar()
        self.width_entry = tk.Entry(size_frame, textvariable=self.width_var, width=10)
        self.width_entry.grid(row=0, column=1, padx=5)

        tk.Label(size_frame, text=f"{get_text('crop_height')}:").grid(row=0, column=2, sticky='w', padx=(10, 0))
        self.height_var = tk.StringVar()
        self.height_entry = tk.Entry(size_frame, textvariable=self.height_var, width=10)
        self.height_entry.grid(row=0, column=3, padx=5)

        # 执行按钮
        self.crop_button = tk.Button(
            self.frame, text=get_text('execute_crop'), command=self.execute_crop,
            bg='#4CAF50', fg='white', padx=20, pady=5
        )
        self.crop_button.pack(pady=10)

        # 提示标签
        self.hint_label = tk.Label(
            self.frame, text=get_text('center_crop_hint'),
            font=('Arial', 8), fg='gray'
        )
        self.hint_label.pack()

    def execute_crop(self):
        """执行中心点切割"""
        try:
            # 获取参数
            center_x = self.center_x_var.get().strip()
            center_y = self.center_y_var.get().strip()
            width = self.width_var.get().strip()
            height = self.height_var.get().strip()

            # 验证必填参数
            if not width or not height:
                messagebox.showwarning(get_text('warning'), get_text('warn_enter_size'))
                return

            # 转换为整数
            width = int(width)
            height = int(height)
            center_x = int(center_x) if center_x else None
            center_y = int(center_y) if center_y else None

            # 调用回调函数
            if self.on_crop_callback:
                self.on_crop_callback(width, height, center_x, center_y)

        except ValueError:
            messagebox.showerror(get_text('error'), get_text('error_invalid_number'))

    def set_center_point(self, x, y):
        """设置中心点坐标"""
        self.center_x_var.set(str(int(x)))
        self.center_y_var.set(str(int(y)))


class CompressPanel:
    """图像压缩控制面板"""

    def __init__(self, parent_frame, on_compress_callback):
        """
        初始化压缩面板

        参数:
            parent_frame: 父容器
            on_compress_callback: 执行压缩的回调函数
        """
        self.frame = tk.LabelFrame(parent_frame, text=get_text('compress_title'), padx=10, pady=10)
        self.on_compress_callback = on_compress_callback

        # 目标大小
        size_frame = tk.Frame(self.frame)
        size_frame.pack(fill='x', pady=5)

        tk.Label(size_frame, text=f"{get_text('target_size')}:").pack(side='left')
        self.target_size_var = tk.StringVar()
        self.target_size_entry = tk.Entry(size_frame, textvariable=self.target_size_var, width=10)
        self.target_size_entry.pack(side='left', padx=5)

        # 单位选择
        self.unit_var = tk.StringVar(value='KB')
        unit_frame = tk.Frame(size_frame)
        unit_frame.pack(side='left', padx=5)
        tk.Radiobutton(unit_frame, text=get_text('unit_kb'), variable=self.unit_var, value='KB').pack(side='left')
        tk.Radiobutton(unit_frame, text=get_text('unit_mb'), variable=self.unit_var, value='MB').pack(side='left')

        # 格式选择
        format_frame = tk.Frame(self.frame)
        format_frame.pack(fill='x', pady=5)

        tk.Label(format_frame, text=f"{get_text('format_label')}:").pack(side='left')
        self.format_var = tk.StringVar(value='JPEG')
        tk.Radiobutton(format_frame, text="JPEG", variable=self.format_var, value='JPEG').pack(side='left', padx=5)
        tk.Radiobutton(format_frame, text="PNG", variable=self.format_var, value='PNG').pack(side='left')

        # 执行按钮
        self.compress_button = tk.Button(
            self.frame, text=get_text('start_compress'), command=self.execute_compress,
            bg='#2196F3', fg='white', padx=20, pady=5
        )
        self.compress_button.pack(pady=10)

        # 结果显示
        self.result_label = tk.Label(self.frame, text="", font=('Arial', 9), fg='green')
        self.result_label.pack()

    def execute_compress(self):
        """执行压缩"""
        try:
            # 获取参数
            target_size = self.target_size_var.get().strip()
            if not target_size:
                messagebox.showwarning(get_text('warning'), get_text('warn_enter_target_size'))
                return

            target_size = float(target_size)
            unit = self.unit_var.get()
            format_type = self.format_var.get()

            # 转换为KB
            if unit == 'MB':
                target_size_kb = target_size * 1024
            else:
                target_size_kb = target_size

            # 调用回调函数
            if self.on_compress_callback:
                actual_size = self.on_compress_callback(target_size_kb, format_type)
                if actual_size:
                    self.result_label.config(text=get_text('compress_result', size=actual_size))

        except ValueError:
            messagebox.showerror(get_text('error'), get_text('error_invalid_number'))

    def clear_result(self):
        """清除结果显示"""
        self.result_label.config(text="")


class ActionPanel:
    """操作按钮面板"""

    def __init__(self, parent_frame, on_save_callback, on_preview_callback):
        """
        初始化操作面板

        参数:
            parent_frame: 父容器
            on_save_callback: 保存回调函数
            on_preview_callback: 预览回调函数
        """
        self.frame = tk.Frame(parent_frame, padx=10, pady=10)

        # 保存按钮
        self.save_button = tk.Button(
            self.frame, text=get_text('save_button'), command=on_save_callback,
            bg='#FF9800', fg='white', padx=30, pady=10, font=('Arial', 10, 'bold')
        )
        self.save_button.pack(fill='x', pady=5)

        # 预览按钮
        self.preview_button = tk.Button(
            self.frame, text=get_text('preview_button'), command=on_preview_callback,
            bg='#9C27B0', fg='white', padx=30, pady=10, font=('Arial', 10, 'bold')
        )
        self.preview_button.pack(fill='x', pady=5)
