import ctypes
import customtkinter as ctk

from ctypes import wintypes

class LowLevel:
    def __init__(self):
        pass
        
    @staticmethod
    def LoadFontFromTTF(fp: str) -> None:
        ctypes.windll.gdi32.AddFontResourceExW(fp, 0x10, 0)

    @staticmethod
    def RoundWinCorners(radius: int, window: ctk.CTk) -> None:
        hwnd = ctypes.windll.user32.GetParent(window.winfo_id())

        DWMWA_WINDOW_CORNER_PREFERENCE = 33

        value = ctypes.c_int(radius)

        ctypes.windll.dwmapi.DwmSetWindowAttribute( wintypes.HWND(hwnd), DWMWA_WINDOW_CORNER_PREFERENCE, ctypes.byref(value), ctypes.sizeof(value))
