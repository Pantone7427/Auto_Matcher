# 🧠 AutoMatcher - Emparejador de Soportes y Transacciones Bancarias

AutoMatcher es una herramienta inteligente con interfaz gráfica moderna, diseñada para automatizar el emparejamiento de comprobantes bancarios ("soportes") escaneados en PDF con registros de transacciones bancarias (TBs) almacenadas en Excel.

---

## 🚀 Características

✅ Extrae automáticamente imágenes de soportes desde archivos PDF con múltiples páginas.

✅ Utiliza OCR (reconocimiento óptico de caracteres) para detectar estado y valor de cada soporte.

✅ Empareja cada soporte ABONADO con la primera transacción disponible que coincida en valor ±100.

✅ Genera un PDF individual por soporte válido, incluyendo imagen y datos de TB.

✅ Interfaz gráfica intuitiva, moderna y con barra de progreso en tiempo real.

✅ Registro en consola y archivo para trazabilidad del proceso.

---

## 🛠️ Tecnologías usadas

- Python 3.10+
- `pdfplumber`, `pytesseract`, `pandas`, `reportlab`
- `customtkinter` para GUI moderna
- `openpyxl` para manipulación de Excel

---

## 📦 Instalación

1. Clona el repositorio:
```bash
git clone https://github.com/pantone7427/auto_matcher.git
cd auto_matcher
```

2. Crea un entorno virtual y actívalo:
```bash
python -m venv venv
source venv/bin/activate  # en Windows: venv\Scripts\activate
```

3. Instala las dependencias:
```bash
pip install -r requirements.txt
```

4. Asegúrate de tener instalado [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) y que esté disponible en tu PATH.

---

## 🖥️ Uso

Puedes lanzar la aplicación gráfica desde terminal:
```bash
python gui/main_window.py
```

### Flujo del proceso:
1. Selecciona el archivo PDF de soportes.
2. Selecciona el archivo Excel con las transacciones.
3. Selecciona la carpeta donde se guardarán los PDFs generados.
4. Haz clic en **Ejecutar Proceso** y relájate mientras la magia sucede. 🧙‍♀️✨

---

## 📝 Formato esperado

### Excel:
Debe tener al menos las columnas:
- `No Egreso`
- `Girado a`
- `Valor`

---

## 💬 Créditos

Desarrollado con 💙 por [Melissa María](https://github.com/pantone7427)

---

## 📄 Licencia
Este proyecto está bajo licencia MIT. ¡Libertad para usar, modificar y mejorar!

