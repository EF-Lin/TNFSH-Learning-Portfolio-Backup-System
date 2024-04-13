from dataclasses import dataclass
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import filedialog
import tkinter.font as font
import tkinter.ttk as ttk
import pyperclip
import os
from backend import Request


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

    def init_user_info(self, loginId: str, password: str):
        path = self.main_path + self.path_list[3] + self.file_type
        user_info = {
            'loginId': loginId,
            'password': password,
        }
        self.generate_text(path, user_info)

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
                elif f is False:
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
            # SyntaxError: Please backup first.
            messagebox.showerror(title='錯誤', message='無資料，請先備份，若已備份就是你沒有資料，爛透了。')
            return []
        except Exception:
            messagebox.showerror(title='錯誤', message='Unknown Error.')
            return []


@dataclass
class Tree:
    inter: Interface
    window: tk.Toplevel
    i: int
    data: list = None

    def __post_init__(self):
        self.tree: ttk.Treeview
        if self.i == 0:
            self.cols = self.inter.cadre_cols
        elif self.i == 1:
            self.cols = self.inter.course_cols
        else:
            self.cols = self.inter.per_cols
        self.path = self.inter.main_path + self.inter.path_list[self.i]
        self.create_tree_data()

    def backup_and_show_message(self) -> bool:
        s = self.inter.backup(self.i)
        if s == 'S':
            messagebox.showinfo("訊息", "備份成功")
            return True
        else:
            messagebox.showerror("錯誤", s)
            return False

    def open_folder(self):
        os.startfile(self.path)

    def create_tree_data(self):
        def copy_from_treeview():
            # from https://blog.csdn.net/vae565056149/article/details/128218467
            # 選取列
            selection = self.tree.selection()
            values = self.tree.item(selection[0])["values"]
            copy_str = ''
            items = list(self.cols.values())
            for i, j in zip(values, items):
                copy_str += f'{j}: {str(i)}\n'
            pyperclip.copy(copy_str)

        self.data = self.inter.load_data(self.i)
        scrollbar = tk.Scrollbar(self.window)
        scrollbar.pack(side='right', fill='y')
        self.tree = ttk.Treeview(
            self.window,
            show='headings',
            columns=[i for i in range(len(self.cols))],
            yscrollcommand=scrollbar.set
        )
        for i in range(len(self.cols)):
            self.tree.column(i, width=80)
        j = 1
        for i in self.cols.values():
            self.tree.heading(f"#{j}", text=i)
            j += 1
        for i in self.data:
            data_list = []
            for j in self.cols.keys():
                data_list.append(i[j])
            self.tree.insert('', index="end", text='', values=data_list)
        self.tree.bind('<3>', lambda x: copy_from_treeview())
        self.tree.pack()
        note1_label = tk.Label(self.window, text='選中後點擊右鍵可複製。')
        note1_label.pack()
        open_file_button = tk.Button(self.window, text='開啟資料夾', command=self.open_folder)
        open_file_button.pack()

    def rebuild_tree(self):
        successful = self.backup_and_show_message()
        if successful:
            self.tree.delete()
            self.create_tree_data()
        else:
            pass


def show_cadre_ex(inter: Interface):
    cadre_window = tk.Toplevel()
    cadre_window.title("幹部經歷")
    cadre_window.geometry('600x300')
    cadre_tree = Tree(inter=inter, window=cadre_window, i=0)
    backup_cadre_button = tk.Button(cadre_window, text="備份幹部經歷", command=cadre_tree.rebuild_tree)
    backup_cadre_button.pack()
    cadre_window.mainloop()


def show_course_ach(inter: Interface):
    course_ach_window = tk.Toplevel()
    course_ach_window.title("課程學習成果")
    course_ach_window.geometry('600x300')
    course_ach_tree = Tree(inter=inter, window=course_ach_window, i=1)
    backup__course_ach_button = tk.Button(course_ach_window, text="備份課程學習成果", command=course_ach_tree.rebuild_tree)
    backup__course_ach_button.pack()
    course_ach_window.mainloop()


def show_per(inter: Interface):
    per_window = tk.Toplevel()
    per_window.title("多元表現")
    per_window.geometry('600x300')
    per_tree = Tree(inter=inter, window=per_window, i=2)
    backup_per_button = tk.Button(per_window, text="備份多元表現", command=per_tree.rebuild_tree)
    backup_per_button.pack()
    per_window.mainloop()


def show_selection_window(inter: Interface):
    def reset():
        yes = messagebox.askyesno(title="警告", message="是否要重新輸入帳號密碼?")
        if yes:
            selection_window.destroy()
            show_login(inter)
        else:
            pass

    def backup_all_and_show_message():
        s = inter.backup(0)
        if s:
            for j in s:
                messagebox.showerror("錯誤", j)
        else:
            messagebox.showinfo("訊息", "備份成功")

    def delete_backup():
        yes = messagebox.askyesno(title="警告", message="此舉將刪除所有已備份文件、紀錄，並且不可回復!!!")
        if yes:
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
    backup_button = tk.Button(selection_window, text="備份", font=f, command=backup_all_and_show_message, width=w, height=h)
    backup_button.grid(row=2, column=0, sticky='ne')
    delete_backup_button = tk.Button(selection_window, text="刪除備份", font=f, command=delete_backup, width=w,
                                     height=h)
    delete_backup_button.grid(row=2, column=1, sticky='nw')
    selection_window.mainloop()


def show_login(inter: Interface):
    def create():
        loginId = loginId_entry.get()
        password = password_entry.get()
        inter.init_user_info(loginId, password)
        f = inter.check_login_data()
        if f:
            login_window.destroy()
            show_selection_window(inter)
        else:
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
