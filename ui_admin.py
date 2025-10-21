import customtkinter as ctk

class AdminUI(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="white")
        self.master = master
        self.pack(expand=True, fill="both")
        self.create_header()

    def create_header(self):
        header = ctk.CTkFrame(self, fg_color="#e5e5e5", height=60, corner_radius=0)
        header.pack(side="top", fill="x")