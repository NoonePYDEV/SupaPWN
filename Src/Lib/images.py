import customtkinter as ctk
from PIL import Image

class ImageLoader:
    @staticmethod
    def RenderCTkImage(fp: str, size: tuple[int, int]) -> ctk.CTkImage:
        return ctk.CTkImage(Image.open(fp), size=size)
    