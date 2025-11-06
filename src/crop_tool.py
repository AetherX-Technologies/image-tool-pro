"""
交互式裁剪工具
支持鼠标拖拽绘制裁剪框、四角调整大小
"""

import tkinter as tk


class CropTool:
    """交互式裁剪工具类"""

    def __init__(self, canvas, callback=None):
        """
        初始化裁剪工具

        参数:
            canvas: tkinter Canvas对象
            callback: 回调函数，当裁剪框改变时调用，参数为(x1, y1, x2, y2)
        """
        self.canvas = canvas
        self.callback = callback

        # 裁剪框状态
        self.rect = None  # 矩形对象
        self.corners = {}  # 四个角的控制点
        self.start_x = None
        self.start_y = None

        # 拖拽状态
        self.drag_mode = None  # None, 'new', 'move', 'nw', 'ne', 'sw', 'se'
        self.drag_start_coords = None

        # 绑定鼠标事件
        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

    def on_press(self, event):
        """鼠标按下事件"""
        x, y = event.x, event.y

        # 检测是否点击在角点上
        corner = self.detect_corner(x, y)
        if corner:
            self.drag_mode = corner
            self.drag_start_coords = self.canvas.coords(self.rect)
            return

        # 检测是否点击在矩形内部（移动）
        if self.rect and self.is_inside_rect(x, y):
            self.drag_mode = 'move'
            self.start_x = x
            self.start_y = y
            self.drag_start_coords = self.canvas.coords(self.rect)
            return

        # 在空白处开始绘制新矩形
        self.drag_mode = 'new'
        self.start_x = x
        self.start_y = y

        # 清除旧的裁剪框
        if self.rect:
            self.canvas.delete(self.rect)
            self.rect = None
        self.clear_corners()

    def on_drag(self, event):
        """鼠标拖拽事件"""
        x, y = event.x, event.y

        if self.drag_mode == 'new':
            # 绘制新矩形
            if self.rect:
                self.canvas.delete(self.rect)

            self.rect = self.canvas.create_rectangle(
                self.start_x, self.start_y, x, y,
                outline='red', width=2, tags='crop_rect'
            )

            # 触发回调
            if self.callback:
                self.callback(self.start_x, self.start_y, x, y)

        elif self.drag_mode == 'move':
            # 移动矩形
            dx = x - self.start_x
            dy = y - self.start_y

            x1, y1, x2, y2 = self.drag_start_coords
            new_x1 = x1 + dx
            new_y1 = y1 + dy
            new_x2 = x2 + dx
            new_y2 = y2 + dy

            self.canvas.coords(self.rect, new_x1, new_y1, new_x2, new_y2)
            self.update_corners(new_x1, new_y1, new_x2, new_y2)

            # 触发回调
            if self.callback:
                self.callback(new_x1, new_y1, new_x2, new_y2)

        elif self.drag_mode in ['nw', 'ne', 'sw', 'se']:
            # 调整矩形大小
            x1, y1, x2, y2 = self.drag_start_coords

            if self.drag_mode == 'nw':  # 左上角
                new_x1, new_y1, new_x2, new_y2 = x, y, x2, y2
            elif self.drag_mode == 'ne':  # 右上角
                new_x1, new_y1, new_x2, new_y2 = x1, y, x, y2
            elif self.drag_mode == 'sw':  # 左下角
                new_x1, new_y1, new_x2, new_y2 = x, y1, x2, y
            else:  # 'se' 右下角
                new_x1, new_y1, new_x2, new_y2 = x1, y1, x, y

            self.canvas.coords(self.rect, new_x1, new_y1, new_x2, new_y2)
            self.update_corners(new_x1, new_y1, new_x2, new_y2)

            # 触发回调
            if self.callback:
                self.callback(new_x1, new_y1, new_x2, new_y2)

    def on_release(self, event):
        """鼠标释放事件"""
        if self.drag_mode == 'new' and self.rect:
            # 显示四个角的控制点
            x1, y1, x2, y2 = self.canvas.coords(self.rect)
            self.draw_corners(x1, y1, x2, y2)

        self.drag_mode = None
        self.drag_start_coords = None

    def detect_corner(self, x, y):
        """
        检测鼠标是否点击在角点上

        返回: 角点名称 ('nw', 'ne', 'sw', 'se') 或 None
        """
        if not self.rect:
            return None

        x1, y1, x2, y2 = self.canvas.coords(self.rect)
        corners_pos = {
            'nw': (x1, y1),  # 左上
            'ne': (x2, y1),  # 右上
            'sw': (x1, y2),  # 左下
            'se': (x2, y2),  # 右下
        }

        # 检测点是否在角点附近（容差10像素）
        tolerance = 10
        for name, (cx, cy) in corners_pos.items():
            if abs(x - cx) < tolerance and abs(y - cy) < tolerance:
                return name

        return None

    def is_inside_rect(self, x, y):
        """检测点是否在矩形内部"""
        if not self.rect:
            return False

        x1, y1, x2, y2 = self.canvas.coords(self.rect)
        left, right = min(x1, x2), max(x1, x2)
        top, bottom = min(y1, y2), max(y1, y2)

        return left < x < right and top < y < bottom

    def draw_corners(self, x1, y1, x2, y2):
        """绘制四个角的控制点"""
        self.clear_corners()

        radius = 5
        corners_pos = {
            'nw': (x1, y1),
            'ne': (x2, y1),
            'sw': (x1, y2),
            'se': (x2, y2),
        }

        for name, (cx, cy) in corners_pos.items():
            corner = self.canvas.create_oval(
                cx - radius, cy - radius,
                cx + radius, cy + radius,
                fill='red', outline='white', width=2,
                tags='corner'
            )
            self.corners[name] = corner

    def update_corners(self, x1, y1, x2, y2):
        """更新四个角的控制点位置"""
        if not self.corners:
            return

        radius = 5
        corners_pos = {
            'nw': (x1, y1),
            'ne': (x2, y1),
            'sw': (x1, y2),
            'se': (x2, y2),
        }

        for name, (cx, cy) in corners_pos.items():
            if name in self.corners:
                self.canvas.coords(
                    self.corners[name],
                    cx - radius, cy - radius,
                    cx + radius, cy + radius
                )

    def clear_corners(self):
        """清除所有角点"""
        for corner in self.corners.values():
            self.canvas.delete(corner)
        self.corners = {}

    def get_crop_rect(self):
        """
        获取当前裁剪框坐标

        返回: (x1, y1, x2, y2) 或 None
        """
        if not self.rect:
            return None

        return self.canvas.coords(self.rect)

    def clear(self):
        """清除裁剪框"""
        if self.rect:
            self.canvas.delete(self.rect)
            self.rect = None
        self.clear_corners()

    def draw_center_point(self, x, y):
        """
        绘制中心点标记

        参数:
            x, y: 中心点坐标
        """
        # 先清除旧的中心点标记
        self.canvas.delete('center_point')

        radius = 5
        # 绘制十字线
        self.canvas.create_line(
            x - 10, y, x + 10, y,
            fill='blue', width=2, tags='center_point'
        )
        self.canvas.create_line(
            x, y - 10, x, y + 10,
            fill='blue', width=2, tags='center_point'
        )
        # 绘制圆圈
        self.canvas.create_oval(
            x - radius, y - radius,
            x + radius, y + radius,
            outline='blue', width=2, tags='center_point'
        )

    def clear_center_point(self):
        """清除中心点标记"""
        self.canvas.delete('center_point')
