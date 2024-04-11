import tkinter as tk
from tkinter import messagebox
import tkinter.font as font
import tkinter.ttk as ttk
import os
from backstage import Request


class Interface(Request):
    cadre_cols = {
        'syear': '學年',
        'seme': '學期',
        'title': '幹部名稱',
        'unit': '單位',
        'kind': '類別',
        'beginDt': '開始日期',
        'endDt': '結束日期',
    }
    course_cols = {
        'syear': '學年',
        'seme': '學期',
        'subjCname': '學科',
        'dn': '檔案名稱',
        'brief': '成果簡述',
        'verifyM': '是否驗證',
    }
    per_cols = {
        'syear': '學年',
        'seme': '學期',
        'tickSyear': '上傳學年',
        'certiName': '檔案名稱',
        'brief': '成果簡述',
    }
    """
        '': '',
        '': '',
        '': '',
        '': ''
    """

    def __init__(self):
        self.city = '12'
        self.schNo = '210305.國立台南第一高級中學'
        self.data = {
            'city': self.city,
            'schNo': self.schNo,
            'validateCode': '',
            'formToken': ''
        }
        self.k = False
        # 初始化
        super().__init__(self.data)
        r = self.check_login_data()
        if r == False:
            show_login(self)

    def __str__(self) -> str:
        return 'This is a interface'

    def check_login_data(self) -> bool or None:
        """登錄功能"""
        path_name = super().main_path + super().path_list[3] + '.txt'
        f = os.path.exists(path_name)
        if not f:
            self.k = True
            show_login(self)
        else:
            with open(path_name, 'r') as f:
                user_info = eval(f.read())
            self.data.update(user_info)
            response = self.login()
            if response == 'S' and self.k:
                return True
            elif response == 'S':
                show_selection_window(self)
            elif response == 'ConnectionError, please check your internet':
                f = messagebox.askyesnocancel(title='錯誤', message=response + '連線錯誤，是否重試?\n點擊「否」將進入選單介面')
                if f:
                    self.check_login_data()
                elif f == False:
                    show_selection_window(self)
                else:
                    pass
            else:
                messagebox.showerror('錯誤', response)
                return False

    def load_data(self, i: int) -> list or dict:
        path = self.main_path + self.path_list[i] * 2 + self.file_type
        with open(path, 'r') as f:
            d = eval(f.read())
        return d


def create_tree_data(data: list, cols: dict, window: tk.Toplevel) -> tk.Toplevel:
    scrollbar = tk.Scrollbar(window)
    scrollbar.pack(side='right', fill='y')
    tree = ttk.Treeview(
        window,
        show='headings',
        columns=[i for i in range(len(cols))],
        yscrollcommand=scrollbar.set
    )
    for i in range(len(cols)):
        tree.column(i, width=80)
    j = 1
    for i in cols.values():
        tree.heading(f"#{j}", text=i)
        j += 1
    for i in data:
        data_list = []
        for j in cols.keys():
            data_list.append(i[j])
        tree.insert('', index="end", text='', values=data_list)
    tree.pack()
    return window


def show_cadre_ex(inter: Interface):
    cadre_data: list = inter.load_data(0)
    cadre_window = tk.Toplevel()
    cadre_window.title("幹部經歷")
    cadre_window.geometry('600x300')
    """
    cadre_scrollbar = tk.Scrollbar(cadre_window)
    cadre_scrollbar.pack(side='right', fill='y')
    cadre_tree = ttk.Treeview(cadre_window, show='headings', columns=[i for i in range(len(inter.cadre_cols))],  yscrollcommand=cadre_scrollbar.set)
    for i in range(len(inter.cadre_cols)):
        cadre_tree.column(i, width=80)
    j = 1
    for i in inter.cadre_cols.values():
        cadre_tree.heading(f"#{j}", text=i)
        j += 1
    for i in cadre_data:
        data_list = []
        for j in inter.cadre_cols.keys():
            data_list.append(i[j])
        cadre_tree.insert('', index="end", text='', values=data_list)
    cadre_tree.pack()
    """
    cadre_window = create_tree_data(data=cadre_data, cols=inter.cadre_cols, window=cadre_window)
    #backup_button = tk.Button(cadre_window, text="備份", command=Interface.backup_cadre_ex, width=20, height=3)
    #backup_button.pack()
    cadre_window.mainloop()


def show_course_ach(inter: Interface):
    course_ach_data: list = inter.load_data(1)
    course_ach_window = tk.Toplevel()
    course_ach_window.title("課程學習成果")
    course_ach_window.geometry('600x300')
    course_ach_window = create_tree_data(data=course_ach_data, cols=inter.course_cols, window=course_ach_window)
    #backup_button = tk.Button(achievement_window, text="備份", command=Interface.backup_course_ach, width=20, height=3)
    #backup_button.pack()
    course_ach_window.mainloop()


def show_per(inter: Interface):
    per_data: list = inter.load_data(2)
    per_window = tk.Toplevel()
    per_window.title("多元表現")
    per_window.geometry('600x300')
    per_window = create_tree_data(data=per_data, cols=inter.per_cols, window=per_window)
    #backup_button = tk.Button(per_window, text="備份", command=interface.backup_per())
    #backup_button.pack()
    per_window.mainloop()


def show_selection_window(inter: Interface):
    def backup_all():
        s = inter.backup_all()
        if s:
            for j in s:
                messagebox.showerror("錯誤", j)
        else:
            messagebox.showinfo("訊息", "備份成功")

    def reset():
        selection_window.destroy()
        show_login(inter)

    selection_window = tk.Tk()
    selection_window.title("台南一中學習歷程備份系統")
    selection_window.geometry('360x400')
    selection_window.rowconfigure((0, 1, 2), weight=1)
    selection_window.columnconfigure((0, 1), weight=1)
    w = 8
    h = 3
    f = font.Font(family='Microsoft JhengHei', size=15)

    cadre_button = tk.Button(selection_window, text="幹部經歷", font=f, command=lambda: show_cadre_ex(inter), width=w, height=h)
    cadre_button.grid(row=0, column=0, sticky='se')
    achievement_button = tk.Button(selection_window, text="學習成果", font=f, command=lambda: show_course_ach(inter), width=w, height=h)
    achievement_button.grid(row=0, column=1, sticky='sw')
    performers_button = tk.Button(selection_window, text="多元表現", font=f, command=lambda: show_per(inter), width=w, height=h)
    performers_button.grid(row=1, column=0, sticky='e')
    settings_button = tk.Button(selection_window, text="重新登錄", font=f, command=reset, width=w, height=h)
    settings_button.grid(row=1, column=1, sticky='w')
    backup_button = tk.Button(selection_window, text="備份", font=f, command=backup_all, width=w, height=h)
    backup_button.grid(row=2, column=0, sticky='ne')
    delete_backup_button = tk.Button(selection_window, text="刪除備份", font=f, command=backup_all, width=w, height=h)
    delete_backup_button.grid(row=2, column=1, sticky='nw')
    selection_window.mainloop()


def show_login(inter: Interface):
    def create():
        loginId = loginId_entry.get()
        password = password_entry.get()
        path_name = inter.main_path + inter.path_list[3] + '.txt'
        user_info = {
            'loginId': loginId,
            'password': password,
        }
        inter.generate_text(path_name, user_info)
        f = inter.check_login_data()
        if f:
            login_window.destroy()
            show_selection_window(inter)
        elif not f:
            pass

    def check():
        if v.get():
            password_entry.config(show='')
        else:
            password_entry.config(show='*')

    login_window = tk.Tk()
    login_window.geometry('250x300')
    login_window.title("台南一中學習歷程備份系統")
    loginId_label = tk.Label(login_window, text="帳號：", width=20, height=4)
    loginId_label.pack()
    loginId_entry = tk.Entry(login_window)
    loginId_entry.pack()
    v = tk.BooleanVar()
    v.set(False)
    password_label = tk.Label(login_window, text="密碼：", width=20, height=2)
    password_label.pack()
    password_entry = tk.Entry(login_window, show='*')
    password_entry.pack()
    password_check = tk.Checkbutton(login_window, text="顯示密碼", variable=v, height=2, command=check)
    password_check.pack()
    login_button = tk.Button(login_window, text="登錄", command=create, width=20, height=2)
    login_button.pack()
    login_window.mainloop()


if __name__ == '__main__':
    interface = Interface()
