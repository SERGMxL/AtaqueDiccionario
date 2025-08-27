# archivo: cracker_logic.py

import zipfile

class ZipCracker:
    """Maneja la lógica de cracking de contraseñas para archivos ZIP."""

    def __init__(self, zip_path, dict_path):
        self.zip_path = zip_path
        self.dict_path = dict_path

    def crack(self, log_callback):
        """
        Intenta encontrar la contraseña usando un ataque de diccionario.

        :param log_callback: Una función que se llama para registrar el progreso.
        :return: La contraseña si se encuentra, de lo contrario None.
        """
        try:
            zip_file = zipfile.ZipFile(self.zip_path)

            with open(self.dict_path, 'r', errors='ignore') as f:
                passwords = f.readlines()
            
            num_passwords = len(passwords)
            log_callback(f"[*] Probando {num_passwords} contraseñas del diccionario: {self.dict_path}\n")

            for password in passwords:
                password = password.strip()
                if not password:  # Omitir líneas vacías
                    continue
                
                log_callback(f"Probando: {password}\n")

                try:
                    zip_file.extractall(pwd=password.encode('utf-8'))
                    log_callback(f"\n[+] ¡Éxito! Contraseña encontrada: {password}\n")
                    return password
                except (RuntimeError, zipfile.BadZipFile, zipfile.zlib.error):
                    continue
            
            log_callback("\n[-] Contraseña no encontrada en el diccionario.\n")
            return None

        except FileNotFoundError:
            log_callback(f"[!] Error: No se pudo encontrar el archivo ZIP o el diccionario.\n   - ZIP: {self.zip_path}\n   - Diccionario: {self.dict_path}\n")
            return None
        except Exception as e:
            log_callback(f"[!] Ocurrió un error inesperado: {e}\n")
            return None