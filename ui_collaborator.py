import customtkinter as ctk

class CollabUI(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="white")
        self.master = master
        self.pack(expand=True, fill="both")

        ctk.CTkLabel(self, text="Panel del Colaborador", font=("Open Sans", 32, "bold"), text_color="#111").pack(pady=40)

        ctk.CTkButton(self, text="Cerrar sesión", command=self.logout).pack(pady=30)

    def logout(self):
        from ui_login import LoginUI
        self.pack_forget()
        LoginUI(self.master)