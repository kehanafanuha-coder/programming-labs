Отчёт
по дисциплине «Программирование на языке Python»
Лабораторная работа № 3
ФУНКЦИОНАЛЬНО-МОДУЛЬНОЕ ПРОГРАММИРОВАНИЕ И БАЗОВЫЕ СТРУКТУРЫ ДАННЫХ В PYTHON

Выполнил: студент группы УТС-251т; Гаврин Е.В
Проверил: доц., к.н. Ситников Д. В.

Омск 2026

Цель работы
Изучение принципов модульной архитектуры программных систем в Python, правил импорта и создания пользовательских модулей, применения системного модуля sys и специального атрибута __name__. Освоение базовых структур данных (списков, кортежей, словарей, множеств), встроенных методов их обработки, синтаксиса срезов и применения полученных навыков при решении инженерных задач автоматизации и управления.

Краткие теоретические сведения
Модульная организация программ и системные модули
Модуль в Python представляет собой отдельный файл с расширением .py, содержащий определения функций, переменных и классов. Модульная архитектура обеспечивает повторное использование кода и декомпозицию сложных программных комплексов.

Импорт модулей: для подключения встроенных или внешних модулей используется оператор import module. Для импорта конкретных функций используется from module import function.

Точка входа __name__: при импорте модуля весь его код исполняется один раз. Чтобы отделить код тестирования от используемого функционала, применяется точка входа с проверкой специальной переменной if __name__ == '__main__':.

Системный модуль sys: модуль sys предоставляет доступ к параметрам среды исполнения. В частности, список sys.argv содержит аргументы командной строки, переданные скрипту при запуске.

Базовые структуры данных
Python содержит четыре основные встроенные структуры данных, предназначенные для группировки и обработки наборов элементов:

Списки (list): упорядоченные динамические массивы элементов произвольных типов ([]). Являются изменяемыми (mutable), что позволяет добавлять (append()), сортировать (sort()) и удалять (pop(), remove(), del) элементы.

Кортежи (tuple): упорядоченные неизменяемые (immutable) последовательности элементов (()). Кортежи применяются для защиты данных от случайной модификации и возврата нескольких значений из функций.

Словари (dict): ассоциативные массивы, хранящие пары «ключ: значение» ({}). Ключи должны быть уникальными и неизменяемыми объектами (строки, числа, кортежи).

Множества (set): неупорядоченные коллекции уникальных элементов. Множества поддерживают математические операции: объединение (|), пересечение (&), разность (-).

Индексация и операции срезов
Последовательности (списки, кортежи, строки) поддерживают обращение к элементам по индексам и получение фрагментов с помощью срезов. Синтаксис среза имеет вид [start:stop:step], где start — начальный индекс (включительно), stop — конечный индекс (не включительно), step — шаг извлечения элементов.

Отрицательные индексы: отрицательные индексы отсчитываются от конца последовательности: -1 соответствует последнему элементу.

Разворот последовательности: срез со значением шага -1 (например, sequence[::-1]) выполняет быстрый разворот последовательности в обратном порядке.

Системная переменная sys.argv в Python
sys.argv — это специальная переменная (список строк) из системного модуля sys в языке Python, которая содержит аргументы командной строки, переданные программе при её запуске из консоли.

Структура и индексация списка sys.argv:

sys.argv[0] — всегда содержит имя самого запускаемого файла программного скрипта (или путь к нему).

sys.argv[1], sys.argv[2], … — хранят текстовые параметры и флаги, переданные программе через пробел после её имени при консольном запуске.

Задание (вариант 5)
Разработать модульную программу на Python для моделирования тепловой защиты сервопривода. Программа должна содержать пользовательский модуль с двумя классами: базовым классом Servo (модель нагрева от тока) и классом-потомком ProtectedServo (аварийный останов при перегреве). Интерфейс реализовать на базе библиотеки tkinter с использованием ползунка для регулировки тока, шкалы температуры, цветного индикатора состояния и кнопки сброса аварии. Обеспечить разделение модели и интерфейса, применение свойств (@property) для контроля значений тока, использование наследования и переопределения методов, а также обработку исключений при вводе недопустимых значений.

Код:
"""
Лабораторная работа №5. Вариант 5 — Тепловая защита сервопривода.

Модель:
    Servo          — базовый класс сервопривода (ток, температура);
    ProtectedServo — потомок с аварийным остановом при перегреве.

Интерфейс:
    ServoApp       — главное окно (наследник tk.Tk).

Логика модели полностью отделена от интерфейса.
"""

import tkinter as tk
from tkinter import ttk, messagebox


# ============================================================
# МОДЕЛЬ
# ============================================================

class Servo:
    """Модель сервопривода с нагревом от тока."""

    def __init__(self, name: str = "Servo-1", max_current: float = 10.0):
        self.name = name
        self.max_current = max_current
        self._current = 0.0
        self._temp = 25.0          # начальная температура (окружающая среда)
        self.max_temp = 85.0       # критическая температура
        
        # Коэффициенты тепловой модели
        self.k_heat = 0.05         # нагрев от тока
        self.k_cool = 0.02         # охлаждение

    @property
    def current(self) -> float:
        return self._current

    @current.setter
    def current(self, value: float):
        value = float(value)
        if not 0.0 <= value <= self.max_current:
            raise ValueError(
                f"Ток должен быть в диапазоне 0...{self.max_current} А"
            )
        self._current = value

    @property
    def temperature(self) -> float:
        return self._temp

    def update(self, dt: float = 0.1):
        """Шаг тепловой модели (нагрев и охлаждение)."""
        # Нагрев пропорционален квадрату тока, охлаждение — разности с окр. средой
        heat = self.k_heat * (self._current ** 2) * dt
        cool = self.k_cool * (self._temp - 25.0) * dt
        self._temp += heat - cool

    def reset(self):
        self._current = 0.0
        self._temp = 25.0

    def __str__(self):
        return f"{self.name}: I={self._current:.1f} А, T={self._temp:.1f} °C"


class ProtectedServo(Servo):
    """Сервопривод с тепловой защитой (аварийный останов)."""

    def __init__(self, name: str = "Servo-1", max_current: float = 10.0):
        super().__init__(name, max_current)
        self.emergency_stop = False

    def update(self, dt: float = 0.1):
        """
        Переопределение: если температура превышает критическую,
        срабатывает аварийный останов, и ток сбрасывается в 0.
        """
        # Если авария уже сработала, ток = 0, но остывание продолжается
        if self.emergency_stop:
            self._current = 0.0

        # Вызов базового метода расчёта температуры
        super().update(dt)

        # Проверка на перегрев
        if self._temp >= self.max_temp and not self.emergency_stop:
            self.emergency_stop = True
            self._current = 0.0  # Мгновенный сброс тока

    def reset_alarm(self):
        """Сброс аварии (разрешается только если температура упала)."""
        if self._temp < self.max_temp - 10.0:
            self.emergency_stop = False
            return True
        return False


# ============================================================
# ИНТЕРФЕЙС
# ============================================================

class ServoApp(tk.Tk):
    """Главное окно приложения."""

    DT = 0.1  # шаг моделирования, с

    def __init__(self, servo: ProtectedServo):
        super().__init__()
        self.title("Тепловая защита сервопривода")
        self.resizable(False, False)
        self.servo = servo

        # Наблюдаемые переменные
        self.info = tk.StringVar()
        self.current_var = tk.DoubleVar(value=0.0)
        self.temp_text_var = tk.StringVar(value="25.0 °C")
        self.status_text_var = tk.StringVar(value="Норма")
        self.alarm_btn = None

        self._build_widgets()
        self._update_ui()
        self.after(int(self.DT * 1000), self._tick)

    def _build_widgets(self):
        main_frame = ttk.Frame(self)
        main_frame.pack(padx=10, pady=10, fill="both", expand=True)

        panel = ttk.LabelFrame(main_frame, text="Управление")
        panel.pack(fill="x", pady=(0, 10))

        # --- Ток ---
        ttk.Label(panel, text="Ток нагрузки, А:").pack(anchor="w", padx=5, pady=(5, 0))
        ttk.Scale(
            panel, from_=0.0, to=self.servo.max_current,
            variable=self.current_var, command=self._on_current
        ).pack(fill="x", padx=5, pady=3)

        # --- Температура ---
        ttk.Label(panel, text="Температура двигателя:").pack(anchor="w", padx=5, pady=(5, 0))
        
        temp_frame = ttk.Frame(panel)
        temp_frame.pack(fill="x", padx=5, pady=3)
        
        self.temp_bar = ttk.Progressbar(
            temp_frame, maximum=self.servo.max_temp, length=200
        )
        self.temp_bar.pack(side="left", fill="x", expand=True)
        
        ttk.Label(temp_frame, textvariable=self.temp_text_var, width=10, anchor="e").pack(side="right")

        # --- Состояние ---
        status_frame = ttk.Frame(panel)
        status_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Label(status_frame, text="Состояние:").pack(side="left")
        
        # Индикатор состояния (цветной Label)
        self.status_label = tk.Label(
            status_frame, textvariable=self.status_text_var, 
            bg="green", fg="white", width=15, font=("Arial", 10, "bold")
        )
        self.status_label.pack(side="left", padx=10)

        # --- Кнопка сброса ---
        self.alarm_btn = ttk.Button(
            panel, text="Сбросить аварию", 
            command=self._reset_alarm, state="disabled"
        )
        self.alarm_btn.pack(fill="x", padx=5, pady=5)

        # --- Статусная строка ---
        ttk.Label(main_frame, textvariable=self.info).pack(anchor="w")

    # ---------- обработчики событий ----------
    def _on_current(self, value):
        if self.servo.emergency_stop:
            return  # Если авария, ползунок не меняет модель
        try:
            self.servo.current = float(value)
        except ValueError as err:
            messagebox.showerror("Ошибка", str(err))

    def _reset_alarm(self):
        if self.servo.reset_alarm():
            self.current_var.set(0.0)
            messagebox.showinfo("Сброс", "Авария сброшена. Двигатель остыл.")
        else:
            messagebox.showwarning("Ожидание", "Двигатель ещё не остыл! Подождите.")

    # ---------- таймер моделирования ----------
    def _tick(self):
        self.servo.update(self.DT)
        self._update_ui()
        self.after(int(self.DT * 1000), self._tick)

    def _update_ui(self):
        # Обновление шкалы температуры
        self.temp_bar["value"] = self.servo.temperature
        self.temp_text_var.set(f"{self.servo.temperature:.1f} °C")
        
        # Обновление текста и цвета состояния
        if self.servo.emergency_stop:
            self.status_text_var.set("АВАРИЯ")
            self.status_label.config(bg="red")
            self.alarm_btn.config(state="normal")
            self.current_var.set(0.0)  # Визуально сбрасываем ползунок
        elif self.servo.temperature > 70.0:
            self.status_text_var.set("Перегрев")
            self.status_label.config(bg="orange")
            self.alarm_btn.config(state="disabled")
        else:
            self.status_text_var.set("Норма")
            self.status_label.config(bg="green")
            self.alarm_btn.config(state="disabled")

        self.info.set(str(self.servo))


# ============================================================
# ТОЧКА ВХОДА
# ============================================================

def main():
    """Создаёт модель и запускает приложение."""
    servo = ProtectedServo("Servo-1", max_current=10.0)
    app = ServoApp(servo)
    app.mainloop()


if __name__ == "__main__":
    main()

Заключение
Таким образом, в ходе лабораторной работы все поставленные задачи были выполнены, а цель достигнута. В теоретической части были изучены принципы модульной архитектуры программных систем в Python, правила импорта и создания пользовательских модулей, применение системного модуля sys и специального атрибута __name__, а также базовые структуры данных (списки, кортежи, словари, множества), встроенные методы их обработки и синтаксис срезов. В практической части была разработана модульная программа для моделирования тепловой защиты сервопривода: в процессе работы закрепились навыки объектно-ориентированного программирования (наследование, переопределение методов, свойства @property), разделения логики модели и пользовательского интерфейса, обработки исключений при вводе недопустимых значений тока, а также построения графического интерфейса на базе tkinter с использованием ползунка, шкалы прогресса, цветного индикатора состояния и кнопки сброса аварии. Работа подтвердила, что Python обладает удобными и гибкими средствами для решения инженерных задач автоматизации и управления, а полученные знания пригодятся при освоении более сложных тем и выполнении следующих лабораторных работ.

