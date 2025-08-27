# archivo: app_gui.py

import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
import threading
from cracker_logic import ZipCracker # <-- IMPORTANTE: Importamos la clase de lógica

class AppGUI(TkinterDnD.Tk):
    """La ventana principal de la aplicación y sus componentes."""

    def __init__(self):
        super().__init__()
        self.title("Descifrador de ZIP Educativo")
        self.geometry("550x450")
        self.configure(bg="#f0f4f8")

        self.zip_path = ""
        self.dict_path = ""

        self._setup_widgets()

    def _setup_widgets(self):
        """Crea y posiciona todos los componentes de la interfaz."""
        self.drop_label = tk.Label(self, text="Arrastra aquí tu archivo ZIP", bg="#e0e7ef", relief="ridge", font=("Segoe UI", 12), padx=10, pady=10)
        self.drop_label.pack(fill="x", padx=20, pady=(20, 10), ipady=30)
        self.drop_label.drop_target_register(DND_FILES)
        self.drop_label.dnd_bind('<<Drop>>', self.on_drop_zip)

        style = ttk.Style()
        style.configure("TButton", font=("Segoe UI", 10))
        self.dict_btn = ttk.Button(self, text="Seleccionar Diccionario (.txt)", command=self.select_dict)
        self.dict_btn.pack(pady=5)

        self.zip_label = tk.Label(self, text="Archivo ZIP: Ninguno", bg="#f0f4f8", font=("Segoe UI", 9))
        self.zip_label.pack(pady=(5, 0))
        self.dict_label = tk.Label(self, text="Diccionario: Ninguno", bg="#f0f4f8", font=("Segoe UI", 9))
        self.dict_label.pack()

        self.start_btn = ttk.Button(self, text="Iniciar Proceso", command=self.start_crack_thread, state="disabled")
        self.start_btn.pack(pady=10, ipady=5)

        self.console = scrolledtext.ScrolledText(self, height=10, font=("Consolas", 10), bg="#1e1e1e", fg="#d4d4d4", relief="sunken", bd=2)
        self.console.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    def on_drop_zip(self, event):
        path = event.data.strip('{}')
        if path.lower().endswith('.zip'):
            self.zip_path = path
            self.zip_label.config(text=f"Archivo ZIP: ...{self.zip_path[-40:]}")
            self.check_if_ready()
        else:
            messagebox.showwarning("Archivo Inválido", "Por favor, arrastra solo archivos .zip")

    def select_dict(self):
        path = filedialog.askopenfilename(title="Selecciona un diccionario", filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")])
        if path:
            self.dict_path = path
            self.dict_label.config(text=f"Diccionario: ...{self.dict_path[-40:]}")
            self.check_if_ready()

    def check_if_ready(self):
        if self.zip_path and self.dict_path:
            self.start_btn.config(state="normal")
        else:
            self.start_btn.config(state="disabled")

    def log_to_console(self, message):
        self.console.insert(tk.END, message)
        self.console.see(tk.END)
        self.update_idletasks()

    def start_crack_thread(self):
        self.console.delete("1.0", tk.END)
        self.start_btn.config(state="disabled")
        thread = threading.Thread(target=self.run_crack, daemon=True)
        thread.start()

    def run_crack(self):
        cracker = ZipCracker(self.zip_path, self.dict_path)
        cracker.crack(self.log_to_console)
        self.start_btn.config(state="normal")