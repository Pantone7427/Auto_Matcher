import os
import threading
import logging
import customtkinter as ctk
from tkinter import filedialog, messagebox

from core.extractor import extract_soportes
from core.excel_reader import leer_excel, guardar_excel
from core.matcher import matchear_soportes
from core.pdf_generator import generar_pdfs

# Configurar logging para la GUI
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

ctk.set_appearance_mode("System")  # Modo claro/oscuro según sistema
ctk.set_default_color_theme("blue")  # Tema primario

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("AutoMatcher - Emparejador de Soportes y TBs")
        self.geometry("700x500")
        self.resizable(False, False)

        # Variables de ruta
        self.pdf_path = ctk.StringVar()
        self.excel_path = ctk.StringVar()
        self.output_dir = ctk.StringVar()

        self._build_ui()

    def _build_ui(self):
        # Título
        ctk.CTkLabel(self, text="AutoMatcher", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=20)

        # Selección de PDF
        frame_pdf = ctk.CTkFrame(self)
        frame_pdf.pack(fill="x", padx=20, pady=(0, 10))
        ctk.CTkLabel(frame_pdf, text="PDF Soportes:").grid(row=0, column=0, sticky="w")
        ctk.CTkEntry(frame_pdf, textvariable=self.pdf_path, width=400).grid(row=0, column=1, padx=5)
        ctk.CTkButton(frame_pdf, text="Examinar", command=self._select_pdf).grid(row=0, column=2)

        # Selección de Excel
        frame_excel = ctk.CTkFrame(self)
        frame_excel.pack(fill="x", padx=20, pady=(0, 10))
        ctk.CTkLabel(frame_excel, text="Excel TBs:").grid(row=0, column=0, sticky="w")
        ctk.CTkEntry(frame_excel, textvariable=self.excel_path, width=400).grid(row=0, column=1, padx=5)
        ctk.CTkButton(frame_excel, text="Examinar", command=self._select_excel).grid(row=0, column=2)

        # Selección carpeta de salida
        frame_output = ctk.CTkFrame(self)
        frame_output.pack(fill="x", padx=20, pady=(0, 10))
        ctk.CTkLabel(frame_output, text="Carpeta salida:").grid(row=0, column=0, sticky="w")
        ctk.CTkEntry(frame_output, textvariable=self.output_dir, width=400).grid(row=0, column=1, padx=5)
        ctk.CTkButton(frame_output, text="Examinar", command=self._select_output).grid(row=0, column=2)

        # Botón de ejecución
        self.run_button = ctk.CTkButton(self, text="Ejecutar Proceso", command=self._start_process, width=200)
        self.run_button.pack(pady=10)

        # Área de logs
        self.log_box = ctk.CTkTextbox(self, width=650, height=230, state="disabled")
        self.log_box.pack(padx=20, pady=(10, 20))

    def _select_pdf(self):
        path = filedialog.askopenfilename(
            filetypes=[("PDF Files", "*.pdf")]
        )
        if path:
            self.pdf_path.set(path)

    def _select_excel(self):
        path = filedialog.askopenfilename(
            filetypes=[("Excel Files", "*.xlsx;*.xls")]
        )
        if path:
            self.excel_path.set(path)

    def _select_output(self):
        path = filedialog.askdirectory()
        if path:
            self.output_dir.set(path)

    def _start_process(self):
        # Disable button during processing
        self.run_button.configure(state="disabled")
        threading.Thread(target=self._run_flow, daemon=True).start()

    def _run_flow(self):
        try:
            self._log("Iniciando proceso...")
            # 1. Extraer soportes
            soportes = extract_soportes(self.pdf_path.get(), self.output_dir.get())
            self._log(f"Soportes extraídos: {len(soportes)}")

            # 2. Leer Excel
            df = leer_excel(self.excel_path.get())
            self._log(f"Transacciones en Excel: {len(df)}")

            # 3. Emparejar
            resultados = matchear_soportes(soportes, df)
            self._log("Emparejamiento completado.")

            # 4. Guardar Excel actualizado
            guardar_excel(df, self.excel_path.get())
            self._log("Excel actualizado con marcas de usados.")

            # 5. Generar PDFs
            pdfs = generar_pdfs(resultados, self.output_dir.get())
            self._log(f"PDFs generados: {len(pdfs)}")

            self._log("Proceso finalizado con éxito.")
            messagebox.showinfo("Éxito", "Proceso completado exitosamente.")
        except Exception as e:
            logger.exception("Error durante el proceso:")
            self._log(f"Error: {e}")
            messagebox.showerror("Error", str(e))
        finally:
            self.run_button.configure(state="normal")

    def _log(self, msg: str):
        self.log_box.configure(state="normal")
        self.log_box.insert("end", f"{msg}\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")

if __name__ == '__main__':
    app = App()
    app.mainloop()
