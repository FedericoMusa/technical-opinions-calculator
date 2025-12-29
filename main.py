# main.py
import ttkbootstrap as ttk
from ui import CalculatorApp  # Asegúrate que coincida con el nombre en ui.py

if __name__ == "__main__":
    app_root = ttk.Window(themename="flatly")
    # Instanciamos la clase con el nuevo nombre traducido
    app = CalculatorApp(app_root) 
    app_root.mainloop()