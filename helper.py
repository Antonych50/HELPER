import tkinter as tk
from operator import index
from tkinter import ttk
from tkinter import *
#from operator import index
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image, ImageTk
import re
import os


S1 = 'Выберите категорию товаров в правом верхнем углу окна'
S2 = 'В меню "Файл" откройте уже существующий учёт ("Открыть"), либо создайте новый ("Создать")'

def ctrl_frame_visibility():
    #if frame.winfo_viewable():  # Проверяем, видим ли фрейм сейчас
        frame.pack_forget()  # Убираем фрейм со всеми подчиненными с экрана
    #else:
        #frame.pack()  # Возвращаем фрейм обратно на экран

def check_focus(widget):
    current_focus = root.focus_get()
    return current_focus == widget

def on_key_press(event):
    #widget = event.widget
    #print(widget.winfo_name)
    if event.keysym == 'Up':
        move_selection(-1)
    elif event.keysym == 'Down':
        move_selection(1)
    elif ((event.keysym == 'Return') or (event.keysym == 'Tab')) and (check_focus(entry1) or check_focus(listbox)):
        selected_indices = listbox.curselection()
        i = selected_indices[0]
        entry1.delete(0, tk.END)
        entry1.insert(0,str(listbox.get(i)))
        listbox.place_forget()
        listbox3.focus_set()
        lbl1.config(background='SystemWindow')
        entry1.config(background='SystemWindow')
        lbl2.config(background='LightCyan')
        listbox3.config(background='LightCyan')
    elif ((event.keysym == 'Return') or (event.keysym == 'Tab')) and check_focus(listbox3):
        lbl2.config(background='SystemWindow')
        listbox3.config(background='SystemWindow')
        lbl3.config(background='LightCyan')
        entry2.config(background='LightCyan')
        entry2.focus_set()
    elif ((event.keysym == 'Return') or (event.keysym == 'Tab')) and check_focus(entry2):
        lbl3.config(background='SystemWindow')
        entry2.config(background='SystemWindow')
        lbl4.config(background='LightCyan')
        entry3.config(background='LightCyan')
        entry3.focus_set()
    elif ((event.keysym == 'Return') or (event.keysym == 'Tab')) and check_focus(entry3):
        lbl4.config(background='SystemWindow')
        entry3.config(background='SystemWindow')
        lbl5.config(background='LightCyan')
        # Вычисляем и выводим общую стоимость выбранного товара
        cost = float(entry2.get())*float(entry3.get())
        cost = round(cost,2)
        lbl6.config(text = str(cost), background='LightCyan')

def category_selected(event):
    if event.keysym != 'Return':
        return
    global listbox2
    listbox.delete(0, tk.END)
    cur_listbox = event.widget
    curr_sel = cur_listbox.curselection()
    category_name = cur_listbox.get(curr_sel[0])

    # Получаем абсолютный путь к текущему файлу
    current_file_path = os.path.abspath(__file__)

    # Получаем путь к директории, в которой находится текущий файл
    current_directory = os.path.dirname(current_file_path)
    match category_name:
        case 'Продукты':
            category_name = 'Products.txt'
        case "Металлоизделия":
            category_name = 'Metal.txt'
        case "Стройматериалы":
            category_name = 'Build.txt'
        case "Автозапчасти":
            category_name = 'Avto.txt'


    with open(current_directory + "/" + category_name, 'r', encoding='utf-8') as f:
        listbox2 = f.readlines()#Заполняем лист "подсказок"
        # print(listbox2)
        #global listbox

        for item in listbox2:
            listbox.insert(tk.END, item.strip())
    frame.place(x=0,y=0, width=350, height=450)#Показываем фрейм со всем содержимым
    entry1.focus_set()

def move_selection(direction):
    # Получаем текущий выбранный элемент
    current_selection = listbox.curselection()
    if current_selection:
        index = current_selection[0]
        # Вычисляем новый индекс
        new_index = index + direction
        # Проверяем, что новый индекс в пределах списка
        if 0 <= new_index < listbox.size():
            # Удаляем текущее выделение и устанавливаем новое
            listbox.selection_clear(0, 'end')
            listbox.selection_set(new_index)
            listbox.activate(new_index)
            # Прокручиваем к новому выбранному элементу
            listbox.see(new_index)

# Открыть папку проекта (учёта, сметы)
def open_project():
    global project_path
    project_path = filedialog.askdirectory(title="Выберите папку Вашего проекта")
    #print(project_path)
    with open(project_path+"/Metal.txt", 'r', encoding='utf-8') as f:
        listbox2 = f.readlines()
        #print(listbox2)
        global listbox
        for item in listbox2:
           listbox.insert(tk.END, item.strip())

def update_listbox(*args):
    # Получаем текущий текст из текстового поля
    search_term = search_var.get().lower()
    if not listbox.winfo_viewable(): listbox.place(x=10, y=55)
    # Очищаем текущий выбор в Listbox
    listbox.selection_clear(0, tk.END)

    # Проходим по всем элементам в Listbox
    items = listbox.get(0, tk.END)
    for item in items:
        if re.match(search_term, item.lower()): #(search_term in item.lower():
            # Если текст найден в элементе, выбираем его и прокручиваем к нему
            try:
                # Поиск индекса элемента по значению
                index = items.index(item)
                listbox.selection_set(index)
                listbox.see(index)
                break
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
root.title("Контроль и учёт...")
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
root.config(background='#556B2F')
# Загружаем фоновое изображение
#image = Image.open("bg.png")
#background_image = ImageTk.PhotoImage(image)

# Создаём` Canvas и установливаем фоновое изображение
#canvas = tk.Canvas(root, width=image.width, height=image.height)
#canvas.pack(fill='both', expand=True)
#canvas.create_image(0, 0, image=background_image, anchor='nw')
#canvas.lift()

# Создаем фрейм
frame = tk.Frame(root, width=400, height=450, borderwidth=0, bg='#556B2F')#width=root.winfo_width()
frame.pack(anchor=NW, fill=X)
frame.pack_propagate(False)  # Отключаем автоизменение размеров фрейма

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
#Создаём заголовки для полей ввода
lbl1 = tk.Label(frame, text = "1. Введите наименование товара:", font=("Arial", 10), background='LightCyan')
lbl1.place(x=10, y=5, width=200, height=20)
#canvas.create_window(200, 20, window=lbl1)

lbl2 = tk.Label(frame, text = "2. Выберите единицу измерения:", font=("Arial", 10))
#lbl1 =  tk.Label(root, text="Hello, World!", bg="white", fg="black")
lbl2.place(x=10, y=55, width=200, height=20)
#canvas.create_window(200, 20, window=lbl1)

lbl3 = tk.Label(frame, text = "3. Введите количество товара:", font=("Arial", 10))
#lbl1 =  tk.Label(root, text="Hello, World!", bg="white", fg="black")
lbl3.place(x=10, y=80, width=185, height=20)

lbl4 = tk.Label(frame, text = "4. Введите цену единицы товара:", font=("Arial", 10))
#lbl1 =  tk.Label(root, text="Hello, World!", bg="white", fg="black")
lbl4.place(x=10, y=105, width=205, height=20)

lbl5 = tk.Label(frame, text = "Общая стоимость товара: ", font=("Arial", 11), fg="DarkBlue")
#lbl1 =  tk.Label(root, text="Hello, World!", bg="white", fg="black")
lbl5.place(x=10, y=135, width=225, height=20)

lbl6 = tk.Label(frame, text = "", font=("Arial", 11), foreground="DarkBlue")
#lbl1 =  tk.Label(root, text="Hello, World!", bg="white", fg="black")
lbl6.place(x=245, y=135, width=75, height=20)
#Строка состояния и подсказок
lbl7 = tk.Label(root, text = "", font=("Arial", 8), fg="Purple", justify = "right")#Строка "состояния"
lbl7.pack(side  = BOTTOM, fill = X)
lbl7["text"] = S1
#canvas.create_window(200, 20, window=lbl1)
# Создаем текстовое поле для ввода
search_var = tk.StringVar()
search_var.trace("w", update_listbox)  # Связываем изменение текста с функцией
entry1 = tk.Entry(frame, width=55, background='LightCyan', textvariable=search_var)
entry1.place(x=8, y=30)
entry1.focus_set()  # Установить фокус ввода на виджет Entry
entry1.bind('<KeyPress>', on_key_press)

entry2 = tk.Entry(frame, width=5)
entry2.place(x=200, y=80)
entry2.bind('<KeyPress>', on_key_press)
#print("Entry2:",entry2.cget("bg"))
entry3 = tk.Entry(frame, width=5)
entry3.place(x=220, y=105)
entry3.bind('<KeyPress>', on_key_press)

#Создаём ListBox
listbox = tk.Listbox(frame, width=55, height=20)
listbox.place(x=10, y=55)
listbox.place_forget()
# Устанавливаем связь между событием нажатия клавиши и обработчиком
listbox.bind('<KeyPress>', on_key_press)

category_list =["Продукты", "Металлоизделия", "Стройматериалы", "Автозапчасти"]
# Создаем StringVar
category_string = tk.StringVar(value=" ".join(category_list))

listbox2 = tk.Listbox(root, width=20, height=5, font=("Arial", 10), fg="Purple", justify = "left",
                 bg = "AntiqueWhite", selectmode=SINGLE, listvariable=category_string)
listbox2.pack(anchor = NE)
listbox2.bind('<KeyPress>', category_selected)
listbox2.configure(height=listbox2.size())
# Создаем Combobox
units = ["Кг", "гр (грамм)", "м (метр)", "л (литр)",
    "п (пакет)", "пчк (пачка)", "шт (штука)", "ед (единица)","уп (упаковка)", "стк (сетка)","т (тонна)",
    "кв.м (квадратный метр)", "куб.м (кубометр)"]
listbox3 = tk.Listbox(frame, width=15, height=10)
for item in units:
    listbox3.insert(tk.END, str(item))
listbox3.place(x=215, y=54)
#combo1.current(0)# Устанавливаем значение по умолчанию
listbox3.bind('<KeyPress>', on_key_press)

# Создаем виджет Treeview
'''tree = ttk.Treeview(canvas, columns=("Name", "Measure_unit", "Quantity","Cost","Summa","Date"), show="headings")
#tree.grid(row=0, column=0, sticky='nsew')

# Определяем заголовки столбцов
tree.heading("Name", text="Наименование товара")
tree.heading("Measure_unit", text="Ед.измер.")
tree.heading("Quantity", text="Количество")
tree.heading("Cost", text="Цена")
tree.heading("Summa", text="Стоимость")
tree.heading("Date", text="Дата")
# Определяем ширину столбцов
tree.column("Name", width=100)
tree.column("Measure_unit", width=50)
tree.column("Quantity", width=150)
tree.column("Cost", width=100)
tree.column("Summa", width=50)
tree.column("Date", width=150)
# Добавляем данные в таблицу
data = [
    ("Алексей", "Кг", 30, 3, 90, '12.11.2024'),
    #("Мария", 25, "Дизайнер"),
    #("Иван", 40, "Менеджер"),
    #("Анна", 35, "Маркетолог")
]

for item in data:
    tree.insert("", tk.END, values=item)
# Показать TreeView
tree.pack(fill='both', expand=True)

# Добавляем скроллбар
scrollbar = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
#scrollbar.location(row=0, column=1, sticky='ns')
#tree.configure(yscroll=scrollbar.set)'''

ctrl_frame_visibility()

# Запускаем главный цикл приложения
root.mainloop()