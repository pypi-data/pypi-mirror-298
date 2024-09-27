import time
import cv2, numpy as np
import win32api
import win32con
import win32gui
import ctypes.wintypes
import ctypes
from mss.base import MSSBase
import mss
import cv2, numpy as np

# from opencv_helper.main import OpencvHelper


class CapcityHelper:
    sct: MSSBase = None
    window_name: str = ""
    hwnd: int = None
    winuser32 = ctypes.windll.LoadLibrary("user32.dll")
    active_window = False
    window_class_name = None

    def __init__(self, window_name, window_class_name=None, active_window=True):
        hwnd, title, class_name = self.find_window(window_name, window_class_name)
        self.sct = mss.mss()
        self.active_window = active_window
        self.hwnd = hwnd
        self.window_class_name = class_name
        self.window_name = title
        if self.hwnd is None:
            raise Exception("窗口未找到")

    def find_window(self, window_name, window_class_name=None):
        window_list = []
        win32gui.EnumWindows(
            lambda hWnd, param: param.append(
                (
                    hWnd,
                    win32gui.GetWindowText(hWnd),
                    win32gui.GetClassName(hWnd),
                )
            ),
            window_list,
        )
        equal_list = []
        for hwnd, title, class_name in window_list:
            if title == window_name:
                if window_class_name is not None and window_class_name != class_name:
                    continue
                equal_list.append((hwnd, title, class_name))
        if len(equal_list) == 1:
            return equal_list[0]
        elif len(equal_list) > 1:
            print("存在多个窗口，请指定窗口类名：", equal_list)
        return None, None, None

    def get_client_pos(self, hwnd):
        # 获取窗口位置
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)

        # 获取客户区位置
        client_left, client_top, client_right, client_bottom = win32gui.GetClientRect(
            hwnd
        )
        client_width, client_height = (
            client_right - client_left,
            client_bottom - client_top,
        )

        # 考虑毛玻璃效果导致的偏移
        border_thickness = win32api.GetSystemMetrics(win32con.SM_CXSIZEFRAME)
        title_bar_height = win32api.GetSystemMetrics(win32con.SM_CYCAPTION)
        left += border_thickness
        top += title_bar_height + border_thickness
        # 考虑窗口边界的偏移
        border_thickness = win32api.GetSystemMetrics(win32con.SM_CXFRAME)
        top += border_thickness
        left += border_thickness
        bottom += border_thickness
        right += border_thickness

        # 计算客户区位置在桌面的绝对地址
        client_left += left
        client_top += top
        client_right = client_left + client_width
        client_bottom = client_top + client_height
        return client_left, client_top, client_right, client_bottom

    # mss截图
    def mss_capture(self, hwnd):
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        monitor = {
            "left": left,
            "top": top,
            "width": right - left,
            "height": bottom - top,
        }
        img = self.sct.grab(monitor)
        img = np.array(img)
        capture = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        return capture

    # 前台截图
    def activate_window_capture(self, hwnd):
        if self.active_window:
            # 它会向 hwnd 指定的窗口发送一个系统命令消息，命令该窗口恢复到正常状态（如果它被最小化了）或者将其带到前台（如果它不在前台）
            if win32gui.GetWindowPlacement(hwnd)[1] != win32con.SW_SHOWNORMAL:
                win32gui.SendMessage(
                    hwnd, win32con.WM_SYSCOMMAND, win32con.SC_RESTORE, 0
                )
            # 获取前台的窗口句柄
            topHwnd = win32gui.GetForegroundWindow()
            # 如果顶层窗口不是目标窗口
            if topHwnd != hwnd:
                try:
                    # 将目标窗口设置为前台窗口
                    win32gui.SetForegroundWindow(hwnd)
                except Exception as e:
                    print(f"设置目标窗口为前台窗口失败 error:{e}")
        # 获取桌面窗口的句柄
        desk_hwnd = win32gui.GetDesktopWindow()
        # 截取桌面窗口
        img = self.mss_capture(desk_hwnd)
        # 如果截图的目标窗口不是桌面的话，需要裁剪掉其它窗口
        if hwnd != self.winuser32.GetDesktopWindow():
            x1, y1, x2, y2 = self.get_client_pos(hwnd)
            img = img[y1:y2, x1:x2]
        return img

    # 截图
    def capture(self, x1=None, y1=None, x2=None, y2=None, file=None):
        """
        :param x1: x1 整形数:区域的左上X坐标
        :param y1: y1 整形数:区域的左上Y坐标

        :param x2: x2 整形数:区域的右下X坐标
        :param y2: y2 整形数:区域的右下Y坐标
        :param file: 保存文件路径，不填写则写入cv图像到属性self._img
        :return:
        """
        # 截取并写入
        img = self.activate_window_capture(self.hwnd)
        img = self.cutOut(img, x1, y1, x2, y2)
        if 0 in img.shape[:2] or img is None:
            print("截图失败")
            return None
        if file:
            cv2.imwrite(file, img)
        return img

    # 截取图像范围
    def cutOut(self, img, x1, y1, x2, y2):
        if None in [x1, y1, x2, y2] or sum([x1, y1, x2, y2]) == 0:
            return img
        height, width = img.shape[:2]
        if y1 <= y2 <= height and x1 <= x2 <= width:
            return img[y1:y2, x1:x2]
        else:
            raise "x1,y1,x2,y2图像范围溢出"


# c = CapcityHelper("媒体播放器", "ApplicationFrameWindow")
# for i in range(10):
#     img = c.capture(0, 198, 665, 298, file=f"./img/{i}.png")
#     if img is not None:
#         r = OpencvHelper.find_pic(img, "1.png")
#         print(r)
#     time.sleep(0.01)
