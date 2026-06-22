import textwrap
import customtkinter as ctk

from Lib.lowlevel import LowLevel

class MessageBox:
    def __init__(self):
        pass

    @staticmethod
    def _wrapMessage(message: str, width: int):
        lines = []
        for line in message.split("\n"):
            wrapped = textwrap.wrap(line, width)
            lines.extend(wrapped if wrapped else [""])
        return lines

    @staticmethod
    def _setupDrag(widget, target):
        dragData = {"startX": 0, "startY": 0, "winX": 0, "winY": 0}

        def _OnDragStart(event):
            dragData["startX"] = event.x_root
            dragData["startY"] = event.y_root
            dragData["winX"] = target.winfo_x()
            dragData["winY"] = target.winfo_y()

        def _OnDragMotion(event):
            dx = event.x_root - dragData["startX"]
            dy = event.y_root - dragData["startY"]
            target.geometry(f"+{dragData['winX'] + dx}+{dragData['winY'] + dy}")

        widget.bind("<Button-1>", _OnDragStart)
        widget.bind("<B1-Motion>", _OnDragMotion)

    @staticmethod
    def Show(host: ctk.CTk, title: str, message: str, canExit: bool = True) -> ctk.CTkToplevel:
        def _restore():
            msgbox.deiconify()
            msgbox.lift()
            msgbox.focus_force()

        msgLines = MessageBox._wrapMessage(message, 35)
        height = int(120 + len(msgLines) * 18)

        msgbox = ctk.CTkToplevel(host, fg_color="#1b1b1b")
        msgbox.overrideredirect(True)
        msgbox.resizable(False, False)
        msgbox.geometry(f"350x{height}")
        msgbox.attributes("-topmost", True)
        msgbox.transient(host)
        msgbox.grab_set()

        x = host.winfo_x() + (host.winfo_width() // 2) - 175
        y = host.winfo_y() + (host.winfo_height() // 2) - (height // 2)
        msgbox.geometry(f"+{x}+{y}")

        msgbox.after(220, lambda: LowLevel.RoundWinCorners(2, msgbox))

        titleBar = ctk.CTkFrame(msgbox, height=30, fg_color="#1b1b1b", corner_radius=0)
        titleBar.place(relx=0, rely=0, relwidth=1)

        titleLabel = ctk.CTkLabel(titleBar, text=title, font=("Arial", 15, "bold"), text_color="#ffffff")
        titleLabel.place(relx=0.5, rely=0.5, anchor="center")

        if canExit:
            closeBtn = ctk.CTkButton(titleBar, text="", width=14, height=14, corner_radius=7, fg_color="#ff5f57", hover_color="#e0443e", command=msgbox.destroy)
            closeBtn.place(relx=0.02, rely=0.5, anchor="w")

            minBtn = ctk.CTkButton(titleBar, text="", width=14, height=14, corner_radius=7, fg_color="#febc2e", hover_color="#e0a320")
            minBtn.place(relx=0.08, rely=0.5, anchor="w")

            fullBtn = ctk.CTkButton(titleBar, text="", width=14, height=14, corner_radius=7, fg_color="#28c840", hover_color="#1fa832")
            fullBtn.place(relx=0.14, rely=0.5, anchor="w")

            fullBtn.configure(command=_restore)

        MessageBox._setupDrag(titleBar, msgbox)
        MessageBox._setupDrag(titleLabel, msgbox)

        messageText = "\n".join(msgLines)

        messageFrame = ctk.CTkFrame(msgbox, fg_color="#1b1b1b", width=350, height=height - 80)
        messageFrame.place(relx=0.5, rely=0.45, anchor="center")

        label = ctk.CTkLabel(messageFrame, text=messageText, justify="left", text_color="#ffffff")
        label.place(relx=0.5, rely=0.6, anchor="center")

        if canExit:
            okBtn = ctk.CTkButton(msgbox, text="OK", width=80, height=28, text_color="#ffffff", corner_radius=2, fg_color="#545454", hover_color="#464647", border_width=1, command=msgbox.destroy)
            okBtn.place(relx=0.5, rely=0.82, anchor="center")

        return msgbox

    @staticmethod
    def AskYesNo(host: ctk.CTk, title: str, message: str) -> bool:

        def _yes():
            result["value"] = True
            msgbox.destroy()

        def _no():
            result["value"] = False
            msgbox.destroy()

        result = {"value": False}

        wrap_width = 38
        wrapped_lines = textwrap.wrap(message, width=wrap_width)

        height = max(140, 120 + len(wrapped_lines) * 18)

        msgbox = ctk.CTkToplevel(host, fg_color="#1b1b1b")

        msgbox.overrideredirect(True)
        msgbox.resizable(False, False)
        msgbox.geometry(f"350x{height}")
        msgbox.attributes("-topmost", True)
        msgbox.transient(host)
        msgbox.grab_set()

        x = host.winfo_x() + (host.winfo_width() // 2) - 175
        y = host.winfo_y() + (host.winfo_height() // 2) - (height // 2)

        msgbox.geometry(f"350x{height}+{x}+{y}")

        msgbox.after(220, lambda: LowLevel.RoundWinCorners(2, msgbox))

        titleBar = ctk.CTkFrame(msgbox, height=30, fg_color="#1b1b1b", corner_radius=0)
        titleBar.place(relx=0, rely=0, relwidth=1)

        titleLabel = ctk.CTkLabel(titleBar, text=title, font=("Arial", 15, "bold"), text_color="#ffffff")
        titleLabel.place(relx=0.5, rely=0.5, anchor="center")

        closeBtn = ctk.CTkButton(titleBar, text="", width=14, height=14, corner_radius=7, fg_color="#ff5f57", hover_color="#e0443e", command=msgbox.destroy)
        closeBtn.place(relx=0.02, rely=0.5, anchor="w")

        minBtn = ctk.CTkButton(titleBar, text="", width=14, height=14, corner_radius=7, fg_color="#febc2e", hover_color="#e0a320")
        minBtn.place(relx=0.08, rely=0.5, anchor="w")

        fullBtn = ctk.CTkButton(titleBar, text="", width=14, height=14, corner_radius=7, fg_color="#28c840", hover_color="#1fa832")
        fullBtn.place(relx=0.14, rely=0.5, anchor="w")

        MessageBox._setupDrag(titleBar, msgbox)
        MessageBox._setupDrag(titleLabel, msgbox)

        messageFrame = ctk.CTkFrame(msgbox, fg_color="#1b1b1b", width=350, height=height - 80)
        messageFrame.place(relx=0.5, rely=0.45, anchor="center")

        label = ctk.CTkLabel(messageFrame, text=message, justify="left", text_color="#ffffff", wraplength=300)
        label.place(relx=0.5, rely=0.5, anchor="center")

        yesBtn = ctk.CTkButton(msgbox, text="Yes", width=80, height=28, text_color="#ffffff", corner_radius=2, fg_color="#3a9733", hover_color="#2c7927", border_width=1, command=_yes)
        yesBtn.place(relx=0.35, rely=0.82, anchor="center")

        noBtn = ctk.CTkButton(msgbox, text="No", width=80, height=28, text_color="#ffffff", corner_radius=2, fg_color="#C02626", hover_color="#941919", border_width=1, command=_no)
        noBtn.place(relx=0.65, rely=0.82, anchor="center")

        host.wait_window(msgbox)

        return result["value"]