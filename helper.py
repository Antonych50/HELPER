import tkinter as tk
from operator import index
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image, ImageTk


# Открыть папку проекта (учёта, сметы)
def open_project():
    global project_path
    project_path = filedialog.askdirectory(title="Выберите папку Вашего проекта")
    print(project_path)
    with open(project_path+"/Metal.txt", 'r', encoding='utf-8') as f:
        lst = f.readlines()
        print(lst)
        global listbox
        for item in lst:
           listbox.insert(tk.END, item.strip())

def update_listbox(*args):
    # Получаем текущий текст из текстового поля
    search_term = search_var.get().lower()

    # Очищаем текущий выбор в Listbox
    listbox.selection_clear(0, tk.END)

    # Проходим по всем элементам в Listbox
    items = listbox.get(0, tk.END)
    for item in items:
        if search_term in item.lower():
            # Если текст найден в элементе, выбираем его и прокручиваем к нему
             try:
                # Поиск индекса элемента по значению
                index = items.index(item)
                #listbox.selection_set(index)
                listbox.see(index)
             except ValueError:
                #listbox.hide()
                break

# Здесь добавить логику для открытия и обработки файла

def say_hello():
    messagebox.showinfo("Hello", "Hello, World!")

def about():
    messagebox.showinfo("About", "Учёт расходов 'на коленке'")

def exit_app():
    root.quit()


# Создаем главное окно приложения
root = tk.Tk()
root.title("Пример меню")
# Получаем ширину и высоту экрана
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
#Задаём размеры окна
width = 500
height = 400
# Вычисляем координаты верхнего левого угла окна
x = (screen_width - width) // 2
y = (screen_height - height) // 2

# Устанавливаем размеры и положение окна
root.geometry(f'{width}x{height}+{x}+{y}')

# Загружаем фоновое изображение
image = Image.open("backgrnd.png")
background_image = ImageTk.PhotoImage(image)

# Создаём` Canvas и установливаем фоновое изображение
canvas = tk.Canvas(root, width=image.width, height=image.height)
canvas.pack(fill='both', expand=True)
canvas.create_image(0, 0, image=background_image, anchor='nw')

# Создаем объект меню
menu_bar = tk.Menu(root)

# Создаем подменю "Файл"
file_menu = tk.Menu(menu_bar, tearoff=0)

file_menu.add_command(label="Создать", command=exit_app)
file_menu.add_command(label="Открыть", command=open_project)
file_menu.add_command(label="Сохранить", command=exit_app)
file_menu.add_command(label="Сохранить как", command=exit_app)
file_menu.add_command(label="Выход", command=exit_app)
menu_bar.add_cascade(label="Файл", menu=file_menu)

# Создаем подменю "Помощь"
help_menu = tk.Menu(menu_bar, tearoff=0)
help_menu.add_command(label="Сказать 'Привет'", command=say_hello)
help_menu.add_command(label="О программе", command=about)
menu_bar.add_cascade(label="Помощь", menu=help_menu)

# Устанавливаем меню в главное окно
root.config(menu=menu_bar)

# Создаем текстовое поле для ввода
search_var = tk.StringVar()
search_var.trace("w", update_listbox)  # Связываем изменение текста с функцией
entry = tk.Entry(canvas, textvariable=search_var)
entry.pack()


listbox = tk.Listbox(canvas, width=50, height=20)
listbox.pack(padx=10, pady=10)
# Запускаем главный цикл приложения
root.mainloop()