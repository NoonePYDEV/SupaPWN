import sys
import customtkinter as ctk

from typing import Any

from Lib.images import ImageLoader

class WinUtils:
    @staticmethod
    def CreateTitleBar(host: ctk.CTk, title: str, phase: int, exitOnClose: bool = True, beforeCloseCommand: Any | None = None) -> ctk.CTkFrame:
        if phase == 1:
            c, m, f = 0.013, 0.053, 0.097
        else:
            c, m, f = 0.013, 0.038, 0.063

        titleBar = ctk.CTkFrame(host, height=30, fg_color="#1b1b1b", corner_radius=0)
        titleBar.place(relx=0, rely=0, relwidth=1.0)
        titleBar.lift()

        titleLabel = ctk.CTkLabel(titleBar, text=title, font=("Arial", 15, "bold"), text_color="#ffffff")
        titleLabel.place(relx=0.5, rely=0.5, anchor='center')

        closeBtn = ctk.CTkButton(titleBar, text="", width=13, height=13, corner_radius=7, fg_color="#ff5f57", hover_color="#e0443e", bg_color="transparent", command=lambda: (host.destroy(), sys.exit(0) if exitOnClose else print('', end=''), beforeCloseCommand() if beforeCloseCommand is not None else print('', end='')))
        closeBtn.place(relx=c, rely=0.27)

        minBtn = ctk.CTkButton(titleBar, text="", width=13, height=13, corner_radius=7, fg_color="#febc2e", hover_color="#e0a320", bg_color="transparent")
        minBtn.place(relx=m, rely=0.27)

        fullBtn = ctk.CTkButton(titleBar, text="", width=13, height=13, corner_radius=7, fg_color="#28c840", hover_color="#1fa832", bg_color="transparent")
        fullBtn.place(relx=f, rely=0.27)

        titleBar.bind("<Double-Button-1>", lambda e: host.deiconify())

        dragData = {"startX": 0, "startY": 0, "winX": 0, "winY": 0}

        def _OnDragStart(event):
            dragData["startX"] = event.x_root
            dragData["startY"] = event.y_root
            dragData["winX"]   = host.winfo_x()
            dragData["winY"]   = host.winfo_y()

        def _OnDragMotion(event):
            deltaX = event.x_root - dragData["startX"]
            deltaY = event.y_root - dragData["startY"]

            newX = dragData["winX"] + deltaX
            newY = dragData["winY"] + deltaY

            host.geometry(f"+{newX}+{newY}")

        titleBar.bind("<Button-1>", _OnDragStart)
        titleBar.bind("<B1-Motion>", _OnDragMotion)

        titleLabel.bind("<Button-1>", _OnDragStart)
        titleLabel.bind("<B1-Motion>", _OnDragMotion)

        for btn in (closeBtn, minBtn, fullBtn):
            btn.bind("<Button-1>", _OnDragStart)
            btn.bind("<B1-Motion>", _OnDragMotion)

        return titleBar

    @staticmethod
    def CenterWin(mainWin: ctk.CTk) -> None:
        width = mainWin.winfo_width()
        height = mainWin.winfo_height()

        screenWidth = mainWin.winfo_screenwidth()
        screenHeight = mainWin.winfo_screenheight()

        x = (screenWidth // 2) - (width // 2)
        y = (screenHeight // 2) - (height // 2)

        mainWin.geometry(f"{width}x{height}+{x}+{y}")

    @staticmethod
    def CreateSidebarBtn(sidebar: ctk.CTkFrame, name: str, iconFp: str, y: int | float, command) -> ctk.CTkFrame:
        btn = ctk.CTkFrame(sidebar, fg_color="#1b1b1b", corner_radius=1, height=50, width=175)
        btn.place(x=0, y=y)

        icon = ctk.CTkLabel(btn, text="", image=ImageLoader.RenderCTkImage("./Assets/Img/info.png", (30, 30)))
        icon.place(x=25, rely=0.5, anchor='center')

        nameLabel = ctk.CTkLabel(btn, text=name, font=("Arial", 18, "bold"), text_color="#ffffff")
        nameLabel.place(x=85, rely=0.5, anchor='center')

        for widget in [btn, icon, nameLabel]:
            widget.bind("<Enter>", lambda e: (btn.configure(fg_color="#171717"), icon.configure(fg_color="#171717"), nameLabel.configure(text_color="#e0e0e0")))
            widget.bind("<Leave>", lambda e: (btn.configure(fg_color="#1b1b1b"), icon.configure(fg_color="#1b1b1b"), nameLabel.configure(text_color="#ffffff")))
            widget.bind("<Button-1>", command)

        return btn