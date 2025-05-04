import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
from sklearn.preprocessing import StandardScaler
import tensorflow as tf


class PredictorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Прогнозирование соотношения матрица-наполнитель")
        self.root.geometry("600x700")

        # Список параметров
        self.columns = ['Плотность, кг/м3',
                        'модуль упругости, ГПа',
                        'Количество отвердителя, м.%',
                        'Содержание эпоксидных групп,%_2',
                        'Температура вспышки, С_2',
                        'Поверхностная плотность, г/м2',
                        'Модуль упругости при растяжении, ГПа',
                        'Прочность при растяжении, МПа',
                        'Потребление смолы, г/м2',
                        'Угол нашивки, град',
                        'Шаг нашивки',
                        'Плотность нашивки']

        self.target = 'Соотношение матрица-наполнитель'

        # Загрузка модели
        try:
            self.model = tf.keras.models.load_model('data/Matrix-filler.keras')
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить модель: {str(e)}")
            self.root.destroy()
            return

        # Создание интерфейса
        self.create_widgets()

    def create_widgets(self):
        # Основной фрейм
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Заголовок
        ttk.Label(main_frame,
                  text="Введите параметры материала:",
                  font=('Arial', 12, 'bold')).pack(pady=10)

        # Поля ввода
        self.entries = {}
        for i, column in enumerate(self.columns):
            frame = ttk.Frame(main_frame)
            frame.pack(fill=tk.X, pady=5)

            ttk.Label(frame, text=column, width=40).pack(side=tk.LEFT)
            entry = ttk.Entry(frame)
            entry.pack(side=tk.RIGHT, expand=True, fill=tk.X)
            self.entries[column] = entry

        # Кнопка прогноза
        ttk.Button(main_frame,
                   text="Рассчитать соотношение",
                   command=self.predict).pack(pady=20)

        # Поле результата
        self.result_frame = ttk.LabelFrame(main_frame,
                                           text="Результат прогноза",
                                           padding="10")
        self.result_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        self.result_label = ttk.Label(self.result_frame,
                                      text="",
                                      font=('Arial', 14, 'bold'),
                                      foreground='blue')
        self.result_label.pack(pady=10)

        # Кнопка очистки
        ttk.Button(main_frame,
                   text="Очистить поля",
                   command=self.clear_fields).pack(pady=10)

    def predict(self):
        try:
            # Сбор данных из полей ввода
            data = []
            for column in self.columns:
                value = self.entries[column].get()
                if not value:
                    messagebox.showwarning("Предупреждение", f"Поле '{column}' не заполнено!")
                    return
                try:
                    data.append(float(value))
                except ValueError:
                    messagebox.showerror("Ошибка", f"Некорректное значение в поле '{column}'!")
                    return

            # Масштабирование данных
            scaler = StandardScaler()
            scaled_data = scaler.fit_transform(np.array([data]))

            # Прогнозирование
            prediction = self.model.predict(scaled_data)
            result = prediction[0][0]

            # Вывод результата
            self.result_label.config(text=f"{self.target} = {result:.4f}")

        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {str(e)}")

    def clear_fields(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        self.result_label.config(text="")


if __name__ == "__main__":
    root = tk.Tk()
    app = PredictorApp(root)
    root.mainloop()