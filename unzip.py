import zipfile
import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
import threading

def crack_zip_password(zip_file_path, dictionary_path, log_callback):
    """
    Intenta encontrar la contraseña de un archivo ZIP usando un ataque de diccionario.

    :param zip_file_path: Ruta al archivo .zip protegido.
    :param dictionary_path: Ruta al archivo .txt que contiene la lista de contraseñas.
    :return: La contraseña si se encuentra, de lo contrario None.
    """
    try:
        # Abre el archivo ZIP
        zip_file = zipfile.ZipFile(zip_file_path)

        # Abre el archivo de diccionario y cuenta el número de líneas para la barra de progreso
        with open(dictionary_path, 'r', errors='ignore') as f:
            passwords = f.readlines()
            num_passwords = len(passwords)

        log_callback(f"[*] Probando {num_passwords} contraseñas del diccionario: {dictionary_path}\n")

        # Itera sobre cada contraseña en el diccionario
        for idx, password in enumerate(passwords):
            password = password.strip() # Elimina espacios en blanco y saltos de línea
            log_callback(f"Probando: {password}\n")

            try:
                # Intenta extraer los archivos con la contraseña actual
                # La contraseña debe ser codificada a bytes
                zip_file.extractall(pwd=password.encode('utf-8'))
                
                # Si no hay error, la contraseña es correcta
                log_callback(f"\n[+] ¡Éxito! Contraseña encontrada: {password}\n")
                return password
            except (RuntimeError, zipfile.BadZipFile):
                # Si hay un error, significa que la contraseña es incorrecta, así que continuamos
                continue
        
        # Si el bucle termina, la contraseña no estaba en el diccionario
        log_callback("\n[-] Contraseña no encontrada en el diccionario.\n")
        return None

    except FileNotFoundError:
        log_callback("[!] Error: No se pudo encontrar el archivo ZIP o el diccionario.\n")
        return None
    except Exception as e:
        log_callback(f"[!] Ocurrió un error inesperado: {e}\n")
        return None

class ZipCrackerGUI(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()
        self.title("Desifrador de ZIP - Arrastra y suelta")
        self.geometry("500x400")
        self.configure(bg="#f0f4f8")
        self.zip_path = ""
        self.dict_path = ""

        # Cuadro de arrastrar y soltar ZIP
        self.drop_label = ttk.Label(self, text="Arrastra aquí tu archivo ZIP", background="#e0e7ef", relief="ridge", anchor="center", font=("Segoe UI", 12))
        self.drop_label.pack(fill="x", padx=20, pady=10, ipady=30)
        self.drop_label.drop_target_register(DND_FILES)
        self.drop_label.dnd_bind('<<Drop>>', self.on_drop_zip)

        # Botón para seleccionar diccionario
        self.dict_btn = ttk.Button(self, text="Seleccionar diccionario (.txt)", command=self.select_dict)
        self.dict_btn.pack(pady=10)

        # Etiquetas de ruta
        self.zip_label = ttk.Label(self, text="ZIP: Ninguno", background="#f0f4f8")
        self.zip_label.pack()
        self.dict_label = ttk.Label(self, text="Diccionario: Ninguno", background="#f0f4f8")
        self.dict_label.pack()

        # Botón para iniciar
        self.start_btn = ttk.Button(self, text="Desifrar ZIP", command=self.start_crack, state="disabled")
        self.start_btn.pack(pady=10)

        # Consola de salida
        self.console = scrolledtext.ScrolledText(self, height=10, font=("Consolas", 10), bg="#222", fg="#eee")
        self.console.pack(fill="both", expand=True, padx=10, pady=10)

    def on_drop_zip(self, event):
        self.zip_path = event.data.strip('{}')
        self.zip_label.config(text=f"ZIP: {self.zip_path}")
        self.check_ready()

    def select_dict(self):
        path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if path:
            self.dict_path = path
            self.dict_label.config(text=f"Diccionario: {self.dict_path}")
            self.check_ready()

    def check_ready(self):
        if self.zip_path and self.dict_path:
            self.start_btn.config(state="normal")

    def log(self, text):
        self.console.insert("end", text)
        self.console.see("end")
        self.update()

    def start_crack(self):
        self.console.delete("1.0", "end")
        self.start_btn.config(state="disabled")
        threading.Thread(target=self.run_crack, daemon=True).start()

    def run_crack(self):
        crack_zip_password(self.zip_path, self.dict_path, self.log)
        self.start_btn.config(state="normal")

if __name__ == "__main__":
    app = ZipCrackerGUI()
    app.mainloop()