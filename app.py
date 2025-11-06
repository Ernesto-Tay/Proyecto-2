import customtkinter as ctk
from ui.login import LoginUI

if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.title("BAWIZ SYSTEM")
    root.geometry("1200x800")
    root.resizable(True, True)
    root.configure(fg_color="white")

    LoginUI(root)
    root.mainloop()