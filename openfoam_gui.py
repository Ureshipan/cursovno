import math
import tkinter as tk
from tkinter import ttk, messagebox
import os
import shutil
import subprocess
import threading
import signal
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
from PIL import Image, ImageTk  # pip install pillow

class OpenFOAMController:
    def __init__(self, root):
        self.root = root
        self.root.title("OpenFOAM Controller")
        self.root.geometry("700x500")
        self.calc_thread = None
        self.calc_process = None
        self.paraview_thread = None
        self.paraview_process = None
        self.create_widgets()
        
    def create_widgets(self):
        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=0)
        self.root.columnconfigure(0, weight=1)

        main_frame = ttk.Frame(self.root)
        main_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)
        
        params_frame = ttk.LabelFrame(main_frame, text="Параметры", padding="10")
        params_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        params_frame.columnconfigure(0, weight=1)
        params_frame.columnconfigure(1, weight=1)
        
        self.params = {}
        row = 0
        def create_param_entry(label, param_name, row):
            ttk.Label(params_frame, text=label).grid(row=row, column=0, sticky=tk.W, pady=2)
            entry = ttk.Entry(params_frame, width=10)
            entry.insert(0, str(DEFAULT_PARAMS[param_name]))
            entry.grid(row=row, column=1, sticky=tk.W, pady=2)
            self.params[param_name] = entry
            return entry
        create_param_entry("L (Длина канала):", "L", row); row += 1
        create_param_entry("l_top (Длина выходного участка):", "l_top", row); row += 1
        create_param_entry("l_bot (Длина входного участка):", "l_bot", row); row += 1
        create_param_entry("w_top (Ширина выходного участка):", "w_top", row); row += 1
        create_param_entry("w_mid (Ширина среднего участка):", "w_mid", row); row += 1
        create_param_entry("w_bot (Ширина входного участка):", "w_bot", row); row += 1
        create_param_entry("a_top (Угол выходной воронки):", "a_top", row); row += 1
        create_param_entry("a_bot (Угол входной воронки):", "a_bot", row); row += 1
        create_param_entry("D (Диаметр цилиндров):", "D", row); row += 1
        create_param_entry("endTime (Время расчета):", "endTime", row); row += 1
        create_param_entry("writeInterval (Интервал записи):", "writeInterval", row); row += 1
        
        image_frame = ttk.Frame(main_frame)
        image_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        image_frame.rowconfigure(0, weight=1)
        image_frame.columnconfigure(0, weight=1)
        try:
            self.img_orig = Image.open("chert_clear.png")
        except Exception as e:
            self.img_orig = None
        self.img_label = ttk.Label(image_frame)
        self.img_label.grid(row=0, column=0, sticky="nsew")
        def resize_image(event):
            if self.img_orig:
                w, h = event.width, event.height
                img = self.img_orig.copy()
                img.thumbnail((w, h), Image.LANCZOS)
                self.tk_img = ImageTk.PhotoImage(img)
                self.img_label.configure(image=self.tk_img)
            else:
                self.img_label.configure(text="Нет изображения")
        image_frame.bind("<Configure>", resize_image)
        
        button_frame = ttk.Frame(self.root, padding="10")
        button_frame.grid(row=1, column=0, sticky="ew")
        
        self.clean_button = ttk.Button(
            button_frame,
            text="Очистить",
            command=self.run_clean_thread
        )
        self.clean_button.pack(side=tk.LEFT, padx=5, pady=10)
        self.build_button = ttk.Button(
            button_frame,
            text="Построить",
            command=self.run_build_thread
        )
        self.build_button.pack(side=tk.LEFT, padx=5, pady=10)
        self.calc_button = ttk.Button(
            button_frame,
            text="Запустить расчет",
            command=self.run_calc_thread
        )
        self.calc_button.pack(side=tk.LEFT, padx=5, pady=10)
        self.paraview_button = ttk.Button(
            button_frame,
            text="Открыть ParaView",
            command=self.run_paraview_thread
        )
        self.paraview_button.pack(side=tk.LEFT, padx=5, pady=10)
        self.status_label = ttk.Label(
            button_frame,
            text="Готов к работе",
            font=("Arial", 10)
        )
        self.status_label.pack(side=tk.LEFT, padx=20, pady=10)

    def validate_params(self, params):
        for name, value in params.items():
            if value <= 0:
                self.status_label.config(text=f"Ошибка: параметр {name} должен быть положительным")
                return False
        if params['w_top'] <= params['w_mid']:
            self.status_label.config(text="Ошибка: w_top должен быть больше w_mid")
            return False
        if params['w_bot'] <= params['w_mid']:
            self.status_label.config(text="Ошибка: w_bot должен быть больше w_mid")
            return False
        if params['a_top'] <= 0 or params['a_top'] >= 130:
            self.status_label.config(text="Ошибка: угол a_top должен быть между 0 и 90 градусами")
            return False
        if params['a_bot'] <= 0 or params['a_bot'] >= 130:
            self.status_label.config(text="Ошибка: угол a_bot должен быть между 0 и 90 градусами")
            return False
        if params['D'] >= params['w_mid'] / 3 * 2:
            self.status_label.config(text="Ошибка: диаметр цилиндров должен быть меньше 2/3 от w_mid")
            return False
        if params['writeInterval'] >= params['endTime'] / 2:
            self.status_label.config(text="Ошибка: writeInterval должен быть меньше половины endTime")
            return False
        vor_top = abs(1/math.tan(params['a_top'] / 2 * math.pi / 180) * (params['w_top'] - params['w_mid']) / 2)
        vor_bot = abs(1/math.tan(params['a_bot'] / 2 * math.pi / 180) * (params['w_bot'] - params['w_mid']) / 2)
        l_mid = params['L'] - params['l_top'] - params['l_bot'] - vor_top - vor_bot
        if l_mid <= params['w_mid'] * 2.1:
            self.status_label.config(text="Ошибка: длина среднего участка должна быть больше 2.1 * w_mid")
            return False
        return True

    def get_params(self):
        params = {}
        for name, entry in self.params.items():
            try:
                params[name] = float(entry.get())
            except ValueError:
                self.status_label.config(text=f"Ошибка: неверное значение параметра {name}")
                return None
        return params

    def run_clean_thread(self):
        threading.Thread(target=self.run_clean, daemon=True).start()

    def run_build_thread(self):
        threading.Thread(target=self.run_build, daemon=True).start()

    def run_calc_thread(self):
        if self.calc_thread and self.calc_thread.is_alive():
            self.stop_calc()
            return
        self.calc_button.config(text="Остановить расчет")
        self.status_label.config(text="Расчет запущен")
        self.calc_thread = threading.Thread(target=self.run_calc, daemon=True)
        self.calc_thread.start()

    def run_clean(self):
        self.status_label.config(text="Очистка...")
        subprocess.run(["./clean.sh"])
        self.status_label.config(text="Очистка завершена")

    def run_build(self):
        self.status_label.config(text="Построение...")
        params = self.get_params()
        if params is None:
            return
        if not self.validate_params(params):
            return
        recalculate_vertices(params)
        self.create_directory_structure(params)
        subprocess.run(["./build.sh"])
        self.status_label.config(text="Построение завершено")

    def run_calc(self):
        try:
            self.calc_process = subprocess.Popen(
                ["./calculate.sh"],
                preexec_fn=os.setsid
            )
            self.calc_process.wait()
            self.status_label.config(text="Расчет завершен")
        except Exception as e:
            self.status_label.config(text=f"Ошибка: {str(e)}")
        finally:
            self.calc_button.config(text="Запустить расчет")
            self.calc_process = None

    def stop_calc(self):
        if self.calc_process and self.calc_process.poll() is None:
            os.killpg(os.getpgid(self.calc_process.pid), signal.SIGTERM)
            self.status_label.config(text="Расчет остановлен")
        self.calc_button.config(text="Запустить расчет")

    def run_paraview_thread(self):
        if self.paraview_thread and self.paraview_thread.is_alive():
            self.stop_paraview()
            return
        self.paraview_button.config(text="Закрыть ParaView")
        self.status_label.config(text="Открытие ParaView...")
        self.paraview_thread = threading.Thread(target=self.run_paraview, daemon=True)
        self.paraview_thread.start()

    def run_paraview(self):
        try:
            self.paraview_process = subprocess.Popen(
                ["./view.sh"],
                preexec_fn=os.setsid
            )
            self.paraview_process.wait()
            self.status_label.config(text="ParaView закрыт")
        except Exception as e:
            self.status_label.config(text=f"Ошибка: {str(e)}")
        finally:
            self.paraview_button.config(text="Открыть ParaView")
            self.paraview_process = None

    def stop_paraview(self):
        if self.paraview_process and self.paraview_process.poll() is None:
            os.killpg(os.getpgid(self.paraview_process.pid), signal.SIGTERM)
            self.status_label.config(text="ParaView закрыт")
        self.paraview_button.config(text="Открыть ParaView")

    def create_directory_structure(self, params):
        os.makedirs("model/constant", exist_ok=True)
        os.makedirs("model/0", exist_ok=True)
        os.makedirs("model/system", exist_ok=True)
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
        with open(path, "w") as f:
            f.write(content)

if __name__ == "__main__":
    root = tk.Tk()
    app = OpenFOAMController(root)
    root.mainloop() 