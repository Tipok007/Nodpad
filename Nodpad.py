import requests
from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from io import BytesIO


def get_random_dog_image():
    try:
        response = requests.get('https://dog.ceo/api/breeds/image/random')
        response.raise_for_status()
        data = response.json()
        return data['message']
    except requests.RequestException as e:
        messagebox.showerror("Ошибка", f"Ошибка при запросе к API: {e}")
        return None


def show_image():
    image_url = get_random_dog_image()
    if image_url:
        try:
            response = requests.get(image_url, stream=True)
            response.raise_for_status()
            img_data = BytesIO(response.content)
            img = Image.open(img_data)
            img_size = (int(width_spinbox.get()), int(height_spinbox.get()))
            img.thumbnail(img_size)
            img = ImageTk.PhotoImage(img)


            top_level_window.geometry(f"{img.width()}x{img.height()}")

            tab = ttk.Frame(notebook)
            notebook.add(tab, text=f"Изображение {notebook.index('end') + 1}")
            label = ttk.Label(tab, image=img)
            label.image = img  # Сохраняем ссылку на изображение
            label.pack(padx=10, pady=10)

            # Сохраняем URL изображения в истории
            history_list.append(image_url)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить изображение: {e}")


def start_progress():
    progress['value'] = 0
    progress.start(30)
    window.after(3000, lambda: [progress.stop(), show_image()])


def show_history():
    history_window = Toplevel(window)
    history_window.title("История загрузок")

    history_listbox = Listbox(history_window, width=50)
    history_listbox.pack(padx=10, pady=10)

    for url in history_list:
        history_listbox.insert(END, url)


window = Tk()
window.title("Случайное изображение")

button = ttk.Button(window, text="Загрузить изображение", command=start_progress)
button.pack(padx=10, pady=10)

history_button = ttk.Button(window, text="Просмотр истории загрузок", command=show_history)
history_button.pack(padx=10, pady=10)

progress = ttk.Progressbar(window, mode='determinate', length=300)
progress.pack(padx=10, pady=5)

width_label = ttk.Label(window, text="Ширина:")
width_label.pack(side='left', padx=(10, 0))

width_spinbox = ttk.Spinbox(window, from_=200, to=500, increment=50, width=5)
width_spinbox.pack(side='left', padx=(0, 10))

height_label = ttk.Label(window, text="Высота:")
height_label.pack(side='left', padx=(10, 0))

height_spinbox = ttk.Spinbox(window, from_=200, to=500, increment=50, width=5)
height_spinbox.pack(side='left', padx=(0, 10))


top_level_window = Toplevel(window)
top_level_window.title("Изображения пёсиков")

notebook = ttk.Notebook(top_level_window)
notebook.pack(expand=True, fill='both', padx=10, pady=10)


history_list = []

window.mainloop()
