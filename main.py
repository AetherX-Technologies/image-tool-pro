"""
图像处理桌面应用 - 主入口文件
"""

import tkinter as tk
from src.app import ImageProcessorApp


def main():
    """应用程序主入口"""
    root = tk.Tk()
    app = ImageProcessorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
