from tkinter import *
import re


class SearchWindow:
    def __init__(self, main_window_ex):
        self.sw = Toplevel()
        self.sw.title("Поиск")
        self.sw.geometry("400x135")
        self.sw.iconbitmap(r'./img/ico.ico')
        self.sw.resizable(False, False)
        self.sw.focus()
        self.text = ""

        # Экземпляр класса MainWindow для get_texfield_data()
        self.main_window_ex = main_window_ex

        # if main_window_ex.textfield is not None:
        #     self.text = main_window_ex.textfield.get(1.0, END)

        self.sensitive_to_case_checkbox = None
        self.search_button = None
        self.entry = None
        self.coincidences_amount = 0
        self.sensitive_to_case = BooleanVar(value=False)

        self.init_widgets()

    def init_widgets(self):
        label = Label(self.sw, text="Поиск:", font="Arial 15")

        self.entry = Entry(self.sw, font="Arial 15", width=28)
        self.entry.focus()
        self.search_button = Button(self.sw, text="Искать", font="Arial 15", activebackground="#ADD8E6",
                                    command=self.search)
        # Enter - поиск
        self.sw.bind("<Return>", self.search)

        self.sensitive_to_case_checkbox = Checkbutton(self.sw, text="Учитывать регистр", font="Arial 13",
                                                      variable=self.sensitive_to_case)
        self.coincidences = Label(self.sw, text=f"Найдено совпадений: {self.coincidences_amount}", font="Arial 12")

        label.place(x=0, y=5)
        self.entry.place(x=70, y=5)
        self.search_button.pack(side=BOTTOM, fill=X)
        self.sensitive_to_case_checkbox.place(x=0, y=38)
        self.coincidences.place(x=0, y=68)

    def search(self, event=None):
        try:
            self.main_window_ex.textfield.tag_delete("highlightline")
        except Exception:
            pass

        # If string is not null
        if len(self.entry.get()) > 0:
            self.text = self.main_window_ex.get_textfield_data()

            current_str = 1
            results = 0
            # Перебор результатов поиска. Разделительная строка - newline. В списке только координата начала каждого вхождения
            for occ in self.get_occurrences():
                if occ == "newline":
                    current_str += 1
                else:
                    start = occ
                    end = start + len(self.entry.get())
                    self.main_window_ex.textfield.tag_add("highlightline", f"{current_str}.{start}",
                                                          f"{current_str}.{end}")
                    self.main_window_ex.textfield.tag_configure("highlightline", background="#ccc", foreground="red")
                    results += 1

            self.coincidences.configure(text=f"Найдено совпадений: {results}")

    # Получить список координат с началом совпадения
    def get_occurrences(self):
        find = self.entry.get()

        sensitive_to_case_value = self.sensitive_to_case.get()
        if not sensitive_to_case_value:
            find = find.lower()

        resutl = []
        # Перебор каждой строки
        for line_num in range(1, self.main_window_ex.textfield.get("1.0", END).count("\n") + 1):
            # Получение текущей строки
            current_line = self.main_window_ex.textfield.get(f"{line_num}.0", END).split("\n", maxsplit=1)[0]
            if not sensitive_to_case_value:
                current_line = current_line.lower()
            matches = re.finditer(find, current_line)
            indices = [match.start() for match in matches]
            for coor in indices:
                resutl.append(coor)
            resutl.append("newline")

        return resutl
