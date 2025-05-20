import tkinter as tk
from tkinter import ttk, messagebox
import os
import shutil
import subprocess
from configs import (
    TRANSPORT_PROPERTIES,
    TURBULENCE_PROPERTIES,
    PRESSURE_FIELD,
    FV_SOLUTION,
    FV_SCHEMES,
    U_FIELD,
    DEFAULT_PARAMS,
    TRACER_FIELD,
    get_control_dict,
    get_block_mesh_dict,
    recalculate_vertices
)

class OpenFOAMController:
    def __init__(self, root):
        self.root = root
        self.root.title("OpenFOAM Controller")
        self.root.geometry("600x500")
        
        # Создаем и размещаем элементы интерфейса
        self.create_widgets()
        
    def create_widgets(self):
        # Фрейм для параметров
        params_frame = ttk.LabelFrame(self.root, text="Параметры геометрии", padding="10")
        params_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Создаем поля ввода для параметров
        self.params = {}
        row = 0
        
        # Функция для создания поля ввода с меткой
        def create_param_entry(label, param_name, row):
            ttk.Label(params_frame, text=label).grid(row=row, column=0, sticky=tk.W, pady=2)
            entry = ttk.Entry(params_frame, width=10)
            entry.insert(0, str(DEFAULT_PARAMS[param_name]))
            entry.grid(row=row, column=1, sticky=tk.W, pady=2)
            self.params[param_name] = entry
            return entry
        
        # Создаем поля ввода
        create_param_entry("Длина канала (L):", "L", row); row += 1
        create_param_entry("Длина выходного участка (l_top):", "l_top", row); row += 1
        create_param_entry("Длина входного участка (l_bot):", "l_bot", row); row += 1
        create_param_entry("Ширина выходного участка (w_top):", "w_top", row); row += 1
        create_param_entry("Ширина среднего участка (w_mid):", "w_mid", row); row += 1
        create_param_entry("Ширина входного участка (w_bot):", "w_bot", row); row += 1
        create_param_entry("Угол выходной воронки (a_top):", "a_top", row); row += 1
        create_param_entry("Угол входной воронки (a_bot):", "a_bot", row); row += 1
        create_param_entry("Диаметр цилиндров (D):", "D", row); row += 1
        
        # Поля для параметров расчета
        create_param_entry("Время расчета (endTime):", "endTime", row); row += 1
        create_param_entry("Интервал записи (writeInterval):", "writeInterval", row); row += 1
        
        # Фрейм для кнопок
        button_frame = ttk.Frame(self.root, padding="10")
        button_frame.pack(fill=tk.BOTH, expand=True)
        
        # Кнопка запуска
        self.run_button = ttk.Button(
            button_frame,
            text="Запуск",
            command=self.run_simulation
        )
        self.run_button.pack(pady=10)
        
        # Статус
        self.status_label = ttk.Label(
            button_frame,
            text="Готов к работе",
            font=("Arial", 10)
        )
        self.status_label.pack(pady=10)
        
    def get_params(self):
        """Получает значения параметров из полей ввода"""
        params = {}
        for name, entry in self.params.items():
            try:
                params[name] = float(entry.get())
            except ValueError:
                messagebox.showerror("Ошибка", f"Неверное значение параметра {name}")
                return None
        return params
        
    def run_simulation(self):
        try:
            # Получаем параметры
            params = self.get_params()
            if params is None:
                return
            # Пересчитываем вершины
            recalculate_vertices(params)
            # Создаем структуру директорий и файлов
            self.create_directory_structure(params)

            # Очищаем директорию
            subprocess.run(["./clean.sh"])

            # Обновляем статус
            self.status_label.config(text="Расчет запущен")

            # Запускаем расчет
            subprocess.run(["./build.sh"])
            subprocess.run(["./run_calc.sh"])

            self.status_label.config(text="Готов к работе")
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {str(e)}")
            self.status_label.config(text="Ошибка при запуске")
    
    def create_directory_structure(self, params):
        # Создаем основные директории
        os.makedirs("model/constant", exist_ok=True)
        os.makedirs("model/0", exist_ok=True)
        os.makedirs("model/system", exist_ok=True)
        
        # Создаем и заполняем файлы
        self.create_file("model/constant/transportProperties", TRANSPORT_PROPERTIES)
        self.create_file("model/constant/turbulenceProperties", TURBULENCE_PROPERTIES)
        self.create_file("model/0/p", PRESSURE_FIELD)
        self.create_file("model/0/U", U_FIELD)
        self.create_file("model/0/tracer", TRACER_FIELD)
        self.create_file("model/system/blockMeshDict", get_block_mesh_dict(params))
        self.create_file("model/system/controlDict", get_control_dict(params))
        self.create_file("model/system/fvSolution", FV_SOLUTION)
        self.create_file("model/system/fvSchemes", FV_SCHEMES)
    
    def create_file(self, path, content):
        """Создает файл с указанным содержимым"""
        with open(path, "w") as f:
            f.write(content)

if __name__ == "__main__":
    root = tk.Tk()
    app = OpenFOAMController(root)
    root.mainloop() 