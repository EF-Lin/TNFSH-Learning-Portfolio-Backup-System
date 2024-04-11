import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import filedialog
import tkinter.font as font
import tkinter.ttk as ttk
import pyperclip
import os
from backstage import Request


class Interface(Request):
    cadre_cols = {
        'syear': '學年',
        'seme': '學期',
        'title': '幹部名稱',
        # 'unit': '單位',
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
        'tickSyear': '勾選學年',
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
        r: bool = self.check_login_data()
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
            elif response == 'S' and not self.k:
                show_selection_window(self)
            elif response == 'ConnectionError: Please check your internet.':
                f = messagebox.askyesnocancel(title='錯誤',
                                              message=response + '\n連線錯誤，是否重試?\n點擊「否」將進入選單介面')
                if f:
                    self.check_login_data()
                    return True
                elif f == False:
                    show_selection_window(self)
                else:
                    return True
            else:
                f = messagebox.askyesnocancel(title='錯誤',
                                              message=response + '\n點擊是重新嘗試登陸，點擊否重新輸入帳號密碼。')
                if f:
                    self.check_login_data()
                else:
                    return False

    def load_data(self, i: int) -> list:
        try:
            path = self.main_path + self.path_list[i] * 2 + self.file_type
            with open(path, 'r') as f:
                d = eval(f.read())
            return d
        except SyntaxError:
            #  TypeError
            messagebox.showerror(title='錯誤', message='SyntaxError: Please backup first.')
            return []


def create_tree_data(data: list, cols: dict, window: tk.Toplevel, path: str) -> tk.Toplevel:
    def open_folder():
        os.startfile(path)

    def copy_from_treeview():
        # from https://blog.csdn.net/vae565056149/article/details/128218467
        # 選取列
        selection = tree.selection()
        values = tree.item(selection[0])["values"]
        copy_str = ''
        items = list(cols.values())
        for i, j in zip(values, items):
            copy_str += f'{j}: {str(i)}\n'
        pyperclip.copy(copy_str)

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
    tree.bind('<3>', lambda x: copy_from_treeview())
    tree.pack()
    note1_label = tk.Label(window, text='選中後點擊右鍵可複製。')
    note1_label.pack()
    open_file_button = tk.Button(window, text='開啟資料夾', command=open_folder)
    open_file_button.pack()
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
    cadre_window = create_tree_data(data=cadre_data, cols=inter.cadre_cols, window=cadre_window,
                                    path=inter.main_path + inter.path_list[0])
    #backup_button = tk.Button(cadre_window, text="備份", command=Interface.backup_cadre_ex, width=20, height=3)
    #backup_button.pack()
    cadre_window.mainloop()


def show_course_ach(inter: Interface):
    course_ach_data: list = inter.load_data(1)
    course_ach_window = tk.Toplevel()
    course_ach_window.title("課程學習成果")
    course_ach_window.geometry('600x300')
    course_ach_window = create_tree_data(data=course_ach_data, cols=inter.course_cols, window=course_ach_window,
                                         path=inter.main_path + inter.path_list[1])
    #backup_button = tk.Button(achievement_window, text="備份", command=Interface.backup_course_ach, width=20, height=3)
    #backup_button.pack()
    course_ach_window.mainloop()


def show_per(inter: Interface):
    per_data: list = inter.load_data(2)
    per_window = tk.Toplevel()
    per_window.title("多元表現")
    per_window.geometry('600x300')
    per_window = create_tree_data(data=per_data, cols=inter.per_cols, window=per_window,
                                  path=inter.main_path + inter.path_list[2])
    #backup_button = tk.Button(per_window, text="備份", command=interface.backup_per())
    #backup_button.pack()
    per_window.mainloop()


def show_selection_window(inter: Interface):
    def backupall():
        s = inter.backup_all()
        if s:
            for j in s:
                messagebox.showerror("錯誤", j)
        else:
            messagebox.showinfo("訊息", "備份成功")

    def reset():
        selection_window.destroy()
        show_login(inter)

    def delete_backup():
        yesno = messagebox.askyesno(title="警告", message="此舉將刪除所有已備份文件、紀錄，並且不可回復!!!")
        if yesno:
            check = simpledialog.askstring(title='確認', prompt='請輸入\"delete\"刪除所有已備份文件、紀錄。')
            if check == 'delete':
                inter.delete_all_files()
            else:
                pass
        else:
            pass

    selection_window = tk.Tk()
    selection_window.title("台南一中學習歷程備份系統")
    selection_window.geometry('360x400')
    selection_window.rowconfigure((0, 1, 2), weight=1)
    selection_window.columnconfigure((0, 1), weight=1)
    w = 8
    h = 3
    f = font.Font(family='Microsoft JhengHei', size=15)

    cadre_button = tk.Button(selection_window, text="幹部經歷", font=f, command=lambda: show_cadre_ex(inter), width=w,
                             height=h)
    cadre_button.grid(row=0, column=0, sticky='se')
    course_ach_button = tk.Button(selection_window, text="學習成果", font=f, command=lambda: show_course_ach(inter),
                                  width=w, height=h)
    course_ach_button.grid(row=0, column=1, sticky='sw')
    per_button = tk.Button(selection_window, text="多元表現", font=f, command=lambda: show_per(inter), width=w,
                           height=h)
    per_button.grid(row=1, column=0, sticky='e')
    relogin_button = tk.Button(selection_window, text="重新登錄", font=f, command=reset, width=w, height=h)
    relogin_button.grid(row=1, column=1, sticky='w')
    backup_button = tk.Button(selection_window, text="備份", font=f, command=backupall, width=w, height=h)
    backup_button.grid(row=2, column=0, sticky='ne')
    delete_backup_button = tk.Button(selection_window, text="刪除備份", font=f, command=delete_backup, width=w,
                                     height=h)
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
