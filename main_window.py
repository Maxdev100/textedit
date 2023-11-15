from tkinter import filedialog, messagebox, ttk
from search_window import SearchWindow
from tkinter import *
import run_code
from github_autoupdate_lib.ppupdater.updater import *


# ИСПРАВИТЬ НЕВОЗМОЖНОСТЬ ЗАПУСКАТЬ ФАЙЛЫ С РУССКИМ ИМЕНЕМ!!


# 1. Сделать возможность открыть окно поиска только 1 раз
# 2. Сделать окно замены и редактирования: замена слов в тексте, предложения с большой буквы, перенос строки после определенного символа
# 3. Сделать настройки: настраиваемый цвет выделения (в т.ч. при поиске), цвет шрифта, заднего фона шрифта, фона поля ввода,
# размер шрифта по умолчанию
# 4. Сделать возможность копировать и вставлять текст
# 5. Сделать контекстное меню при нажатии правой кнопкой мышки (Копировать, вставить (если нечего - неактивно), искать выделенный текст)
# 7. Cделать выбор кодировки и конвертацию кодировок


# Main Window (init and widgets)
class MainWindow:
    avaible_filetypes = [('Все файлы', '*.*'),
                         ('Текстовый файл', '*.txt'),
                         ('Python скрипт', '*.py'),
                         ('BAT скрипт', '*.bat'),
                         ('VBS скрипт', '*.vbs')]

    is_file_changed = False
    not_saved_sign = "*"
    font_size_change_step = 2
    font_size = 24
    font_name = "Calibri"

    def __init__(self, title: str, window_size_x: int, window_size_y: int, resizable: bool, current_version,
                 file=None, new_ver_av=False):
        self.textfield = None
        self.file_path = file

        self.app = Tk()
        self.app.title(title)
        self.app.geometry(f"{window_size_x}x{window_size_y}")
        self.app.resizable(resizable, resizable)
        self.app.iconbitmap(r'./img/ico.ico')
        self.app.protocol('WM_DELETE_WINDOW', self.ask_save_when_closing)

        self.text_wrap_type = IntVar(value=0)

        # Hotkeys
        self.app.bind("<Control-KeyPress>", self.hotkeys_catcher)
        self.app.bind("<Control-MouseWheel>", self.mouse_wheel_zoom)

        self.init_widgets()
        self.init_menu()

        # Если при открытии приложения указан файл
        if self.file_path is not None:
            self.open_file()

        # ЕСЛИ ВЫШЛО ОБНОВЛЕНИЕ
        if new_ver_av:
            start_update = messagebox.askyesno(title="Доступно обновление!", message="Установить прямо сейчас?")
            # Если пользователь нажал ДА
            if start_update:
                updater = Updater(current_version=current_version, repository="https://github.com/Maxdev100/textedit",
                              target_path="./", tag="textedit")
                new_ver = updater.update()

                # Запись в файл новой версии
                version_file = open("version.txt", 'w')
                version_file.write(str(new_ver))
                version_file.close()

                messagebox.showinfo(title="Обновление завершено", message=f"TextEdit обновился до версии {new_ver}. Перезапустите приложение для применения изменений!")
                self.app.destroy()

        self.app.mainloop()

    # Widgets initialization
    def init_widgets(self):
        # Toolbar
        frame = Frame(self.app, bd=2)
        frame.pack(side=TOP, fill=X)

        # Text field
        textframe = Frame(self.app, pady=2)
        textframe.grid_propagate(False)
        textframe.pack(fill=BOTH, expand=True)

        self.textfield = Text(textframe, font=(self.font_name, self.font_size), wrap=NONE, undo=True)
        self.set_textfield_data("")
        self.textfield.bind("<Key>", self.key_pressed)  # File changed

        # Scrollbar
        scrolly = ttk.Scrollbar(textframe, orient="vertical", command=self.textfield.yview)
        scrollx = ttk.Scrollbar(textframe, orient="horizontal", command=self.textfield.xview)

        self.textfield['yscrollcommand'] = scrolly.set
        self.textfield['xscrollcommand'] = scrollx.set

        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.pack(side=BOTTOM, fill=X)
        self.textfield.pack(fill=BOTH, expand=True)

    # Menu initialization
    def init_menu(self):
        main_menu = Menu(self.app)
        self.app.config(menu=main_menu)

        # FILE ACTIONS
        filemenu = Menu(main_menu, tearoff=0)
        filemenu.add_command(label="Сохранить            Ctrl+S", command=self.save)
        filemenu.add_command(label="Сохранить как     Ctrl+W", command=self.save_as)
        filemenu.add_command(label="Открыть                Ctrl+O", command=self.open_file)

        # EDITOR ACTIONS
        editmenu = Menu(main_menu, tearoff=0)
        editmenu.add_command(label="Увеличить шрифт    (Ctrl+MouseWheel)",
                             command=lambda: self.inc_font_size(size_step=13))
        editmenu.add_command(label="Уменьшить шрифт  (Ctrl+MouseWheel)",
                             command=lambda: self.dec_font_size(size_step=13))

        editmenu.add_separator()
        editmenu.add_radiobutton(label="Без переноса текста", value=0, selectcolor="#006400",
                                 variable=self.text_wrap_type, command=self.check_text_wrap_radiobutton)
        editmenu.add_radiobutton(label="Перенос текста по словам", value=1, selectcolor="#006400",
                                 variable=self.text_wrap_type, command=self.check_text_wrap_radiobutton)
        editmenu.add_radiobutton(label="Перенос текста по буквам", value=2, selectcolor="#006400",
                                 variable=self.text_wrap_type, command=self.check_text_wrap_radiobutton)

        editmenu.add_separator()
        editmenu.add_command(label="Поиск по тексту       Ctrl+F", command=lambda: SearchWindow(self))
        editmenu.add_command(label="Сброс выделения    Ctrl+D", command=self.deselect)

        editmenu.add_command(label="Назад                          Ctrz+Z", command=lambda: self.textfield.edit_undo())

        # RUN ACTIONS
        runmenu = Menu(main_menu, tearoff=0)
        runmenu.add_command(label="Запустить скрипт", command=lambda: run_code.run(self.file_path))

        # Adding cascade FILE
        main_menu.add_cascade(label="Файл", menu=filemenu)

        # Adding Cascade EDIT
        main_menu.add_cascade(label="Редактор", menu=editmenu)

        # Adding cascade RUN
        main_menu.add_cascade(label="Запуск", menu=runmenu)

    # Deselecting text which selected in FIND window
    def deselect(self):
        try:
            self.textfield.tag_delete("highlightline")
        except Exception:
            pass

    # Dialog window when closing program
    def ask_save_when_closing(self, exit_program=True):
        if self.is_file_changed == True:
            res = messagebox.askyesnocancel(title="Сохранить изменения в файле?", message=f"Сохранить файл?")
            # Да
            if res:
                self.save()
                if exit_program: self.app.destroy()
            # Нет
            elif res == False:
                if exit_program: self.app.destroy()
            # Отмена
            else:
                return False
        else:
            if exit_program: self.app.destroy()

    # Checking text-warp rediobuttons if pressed
    def check_text_wrap_radiobutton(self):
        if self.text_wrap_type.get() == 0:
            self.textfield.configure(wrap=NONE)
        elif self.text_wrap_type.get() == 1:
            self.textfield.configure(wrap=WORD)
        elif self.text_wrap_type.get() == 2:
            self.textfield.configure(wrap=CHAR)

    # Saving file
    def save(self):
        # If file already opened
        if self.file_path is not None:
            try:
                file = open(self.file_path, "w")

                file.write(self.get_textfield_data()[:-1])
                file.close()

                self.app.title(self.file_path)
                self.is_file_changed = False
            except Exception:
                messagebox.showerror(title="Ошибка сохранения", message="Не удалось сохранить файл!")
        else:
            self.save_as()

    def open_file(self, filepath=None):
        if filepath is not None:
            if self.ask_save_when_closing(exit_program=False) != False:
                file_path = filedialog.askopenfile(title="Открыть")
                if hasattr(file_path, 'name'):
                    try:
                        self.file_path = file_path.name
                        file = open(self.file_path, "r", encoding="utf-8")
                        self.set_textfield_data(file.read())
                        file.close()
                        self.app.title(self.file_path)
                    except Exception:
                        messagebox.showerror(title="Ошибка открытия", message="Не удалось открыть файл!")
        else:
            try:
                file = open(self.file_path, "r", encoding="utf-8")
                self.set_textfield_data(file.read())
                file.close()
                self.app.title(self.file_path)
            except Exception:
                messagebox.showerror(title="Ошибка открытия", message="Не удалось открыть файл!")

    def save_as(self):
        file_path = filedialog.asksaveasfile(filetypes=self.avaible_filetypes, defaultextension="txt",
                                             title="Сохранить как", initialfile="Новый файл.txt")
        if hasattr(file_path, 'name'):
            try:
                self.file_path = file_path.name
                file = open(self.file_path, "w+")
                file.write(self.get_textfield_data())
                file.close()
                self.app.title(self.file_path)
                self.is_file_changed = False
            except Exception:
                messagebox.showerror(title="Ошибка сохранения", message="Не удалось сохранить файл!")

    def set_textfield_data(self, data):
        self.textfield.delete(1.0, END)
        self.textfield.insert(1.0, data)

    def get_textfield_data(self):
        return self.textfield.get(1.0, END)

    # If key pressed on text field => file changed but not saved
    def key_pressed(self, event):
        # Checking is file changed
        title = self.app.title()
        if (title[0] != self.not_saved_sign and
                event.keysym not in ["Shift_L", "Shift_L", "Control_L", "Control_R",
                                     "Alt_L", "Alt_R", "Win_L", "Win_R",
                                     "Insert", "End", "Next", "Prior",
                                     "Home", "Scroll_Lock", "Pause", "Num_Lock",
                                     "Left", "Right", "Up", "Down", "Escape", "Caps_Lock",
                                     "F1", "F2", "F3", "F4", "F5", "F6", "F7",
                                     "F8", "F9", "F10", "F01", "F12", "Control-s",
                                     "Control-w", "Control-o", "Control-d", "Control-f"] and event.state not in [131080,
                                                                                                                 12]):
            self.app.title(f"{self.not_saved_sign}{title}")
            self.is_file_changed = True

    def hotkeys_catcher(self, event):
        if event.keycode == 83:
            self.save()
        elif event.keycode == 79:
            self.open_file()
        elif event.keycode == 87:
            self.save_as()
        elif event.keycode == 68:
            self.deselect()
        elif event.keycode == 70:
            SearchWindow(self)

    # Ctrl+Mouse wheel to zoom

    def inc_font_size(self, size_step=0):
        if size_step != 0:
            self.font_size += size_step
            self.textfield.configure(font=(self.font_name, self.font_size))
        else:
            self.font_size += self.font_size_change_step
            self.textfield.configure(font=(self.font_name, self.font_size))

    def dec_font_size(self, size_step=0):
        if self.font_size - self.font_size_change_step > 5 and self.font_size - size_step > 5:
            if size_step != 0:
                self.font_size -= size_step
                self.textfield.configure(font=(self.font_name, self.font_size))
            else:
                self.font_size -= self.font_size_change_step
                self.textfield.configure(font=(self.font_name, self.font_size))

    def mouse_wheel_zoom(self, event):
        if event.delta > 0:
            self.inc_font_size()
        elif event.delta < 0:
            self.dec_font_size()
