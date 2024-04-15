from dataclasses import dataclass
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import filedialog
import tkinter.ttk as ttk
import pyperclip
import os
from Resource.backend import Request


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
                                              message=response + '\n連線錯誤，是否重試?\n點擊「否」將進入選單介面，並在離線模式下運行系統。')
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

    #def announcement(self):


@dataclass
class Show_subject_window:
    inter: Interface
    i: int
    data: list = None

    def __post_init__(self):
        self.window = tk.Toplevel()
        self.window.title(self.inter.subject[self.i])
        self.window.geometry('600x350')
        developer_label = tk.Label(self.window, text='Developed by EFLin')
        developer_label.pack(side='top', anchor='e')
        self.tree = None
        if self.i == 0:
            self.cols = self.inter.cadre_cols
        elif self.i == 1:
            self.cols = self.inter.course_cols
        elif self.i == 2:
            self.cols = self.inter.per_cols
        else:
            messagebox.showerror(title='警告', message='Unknown error')
            exit()
        self.path = self.inter.main_path + self.inter.path_list[self.i]
        backup_button = tk.Button(self.window, text=f'備份{self.inter.subject[self.i]}', command=self.rebuild_tree)
        backup_button.pack()
        open_file_button = tk.Button(self.window, text='開啟資料夾', command=self.open_folder)
        open_file_button.pack()
        note1_label = tk.Label(self.window, text='選中後點擊右鍵可複製。')
        note1_label.pack()
        self.scrollbar = tk.Scrollbar(self.window)
        self.scrollbar.pack(side='right', fill='y')
        self.create_tree_data()
        self.window.mainloop()

    def backup_and_show_message(self) -> bool:
        s = self.inter.backup(self.i)
        if s == 'S':
            messagebox.showinfo('訊息', '備份成功')
            return True
        else:
            messagebox.showerror('錯誤', s)
            return False

    def open_folder(self):
        os.startfile(self.path)

    def create_tree_data(self):
        def copy_from_treeview():
            # refer from https://blog.csdn.net/vae565056149/article/details/128218467
            # 選取列
            selection = self.tree.selection()
            values = self.tree.item(selection[0])["values"]
            copy_str = ''
            items = list(self.cols.values())
            for i, j in zip(values, items):
                copy_str += f'{j}: {str(i)}\n'
            pyperclip.copy(copy_str)

        self.data = self.inter.load_data(self.i)
        self.tree = ttk.Treeview(
            self.window,
            show='headings',
            columns=[i for i in range(len(self.cols))],
            yscrollcommand=self.scrollbar.set
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
            self.tree.insert('', index='end', text='', values=data_list)
        self.tree.bind('<3>', lambda x: copy_from_treeview())
        self.tree.pack()

    def rebuild_tree(self):
        successful = self.backup_and_show_message()
        if successful:
            self.tree.destroy()
            self.create_tree_data()
        else:
            pass


class Covert:
    def __init__(self, inter: Interface):
        self.inter = inter
        self.files: tuple = ()
        self.img_size: list = []

    def show_covert_img(self):
        self.show_covert_img_window = tk.Toplevel()
        self.show_covert_img_window.title('Image To pdf')
        self.show_covert_img_window.geometry('300x400')
        self.frame = tk.Frame(self.show_covert_img_window)
        self.frame.pack()
        self.img_name = tk.StringVar()
        self.img_name.set('None')
        self.file_name = tk.StringVar()
        self.file_name.set('file')
        select_button = tk.Button(self.show_covert_img_window, text='選擇圖片', command=self.select_images)
        select_button.pack()
        name_label = tk.Label(self.show_covert_img_window, text='pdf檔案名稱')
        name_label.pack()
        name_entry = tk.Entry(self.show_covert_img_window, textvariable=self.file_name)
        name_entry.pack()
        covert_button = tk.Button(self.show_covert_img_window, text='轉換', command=self.covert_img)
        covert_button.pack()
        developer_label = tk.Label(self.show_covert_img_window, text='Developed by EFLin')
        developer_label.pack(side='bottom', anchor='e')
        self.show_covert_img_window.mainloop()

    def select_images(self):
        self.files = filedialog.askopenfilenames(parent=self.show_covert_img_window, title='請選擇圖片',
                                                 filetypes=[('image files', '.png;.jpg;.jpge')])
        self.frame.pack_forget()
        self.frame = tk.Frame(self.show_covert_img_window)
        self.img_size = [tk.IntVar() for _ in range(len(self.files))]
        title = tk.Label(self.frame, text='調整大小，10為不變，9為0.9倍，以此類推。')
        for i in range(len(self.img_size)):
            self.img_size[i].set(10)
        for i in range(len(self.files)):
            quality_scale = tk.Scale(self.frame, from_=1, to=10, orient='horizontal',
                                     variable=self.img_size[i], length=150)
            quality_scale.pack()
            quality_label = tk.Label(self.frame, text=self.files[i])
            quality_label.pack()
        self.frame.pack()

    def covert_img(self):
        if self.file_name.get() == '':
            messagebox.showerror(title='錯誤', message='請輸入檔案名稱。')
        elif self.files == ():
            messagebox.showerror(title='錯誤', message='請選擇檔案。')
        else:
            size = []
            for i in range(len(self.img_size)):
                size.append(self.img_size[i].get())
            covert_successful = self.inter.covert_image_to_pdf(files=self.files,
                                                               name=self.file_name.get(),
                                                               size=size)
            if covert_successful:
                # messagebox.showinfo(title='訊息', message='轉換成功')
                os.startfile(self.inter.main_path)
            else:
                messagebox.showerror(title='錯誤', message='轉換失敗。')


def show_anno(inter: Interface):
    successful, data = inter.announcement()
    text = ''
    f_title = 'Microsoft_JhengHei 18 bold'
    f_text = 'Microsoft_JhengHei 12 bold'
    if successful:
        announcement, date, deadline = data[0], data[1], data[2]
        anno_window = tk.Toplevel()
        anno_window.title('公告')
        anno_window.geometry('500x300')
        anno_title_label = tk.Label(anno_window, text='公告', font=f_title)
        anno_title_label.pack()
        j = 0
        for i in range(len(announcement)):
            text += f'{announcement[i]} {date[j]} {date[j + 1]}\n'
            if not deadline[j+1]:
                text += '時間截止，你死了!\n\n'
            else:
                text += f'距離時間截止還剩下{deadline[j+1]}，趕快去做事，懶骨頭。\n\n'
            j += 2
        anno_label = tk.Label(anno_window, text=text, font=f_text)
        anno_label.pack()
        developer_label = tk.Label(anno_window, text='Developed by EFLin')
        developer_label.pack(side='bottom', anchor='e')
        anno_window.mainloop()
    else:
        messagebox.showerror(title='錯誤', message=data)


def show_selection_window(inter: Interface):
    def backup_all_and_show_message():
        s = inter.backup_all()
        if s:
            for j in s:
                messagebox.showerror('錯誤', j)
        else:
            messagebox.showinfo('訊息', '備份成功')

    def reset():
        yes = messagebox.askyesno(title='警告', message='是否要重新輸入帳號密碼?')
        if yes:
            selection_window.destroy()
            show_login(inter)
        else:
            pass

    def delete_backup():
        yes = messagebox.askyesno(title='警告', message='此舉將刪除所有已備份文件、紀錄，並且不可回復!!!')
        if yes:
            check = simpledialog.askstring(title='確認', prompt='請輸入\"delete\"刪除所有已備份文件、紀錄。')
            if check == 'delete':
                inter.delete_all_files()
            else:
                pass
        else:
            pass

    def create_subject_window(i: int):
        subject_window = Show_subject_window(inter=inter, i=i)

    selection_window = tk.Tk()
    selection_window.title('台南一中學習歷程備份系統')
    selection_window.geometry('360x400')
    selection_window.rowconfigure((0, 1, 2, 3), weight=1)
    selection_window.columnconfigure((0, 1), weight=1)
    w = 8
    h = 3
    f = 'Microsoft_JhengHei 15'
    covert = Covert(inter)

    announcement_button = tk.Button(selection_window, text='公告', font=f, command=lambda :show_anno(inter),
                                    width=w, height=h)
    announcement_button.grid(row=0, column=0, sticky='se')
    cadre_button = tk.Button(selection_window, text='幹部經歷', font=f, command=lambda: create_subject_window(0),
                             width=w, height=h)
    cadre_button.grid(row=0, column=1, sticky='sw')
    course_ach_button = tk.Button(selection_window, text='學習成果', font=f, command=lambda: create_subject_window(1),
                                  width=w, height=h)
    course_ach_button.grid(row=1, column=0, sticky='e')
    per_button = tk.Button(selection_window, text='多元表現', font=f, command=lambda: create_subject_window(2),
                           width=w, height=h)
    per_button.grid(row=1, column=1, sticky='w')
    backup_button = tk.Button(selection_window, text='備份', font=f, command=backup_all_and_show_message,
                              width=w, height=h)
    backup_button.grid(row=2, column=0, sticky='e')
    covert_img_button = tk.Button(selection_window, text='轉檔工具', font=f, command=covert.show_covert_img,
                                  width=w, height=h)
    covert_img_button.grid(row=2, column=1, sticky='w')
    relogin_button = tk.Button(selection_window, text='重新登錄', font=f, command=reset,
                               width=w, height=h)
    relogin_button.grid(row=3, column=0, sticky='ne')
    delete_backup_button = tk.Button(selection_window, text='刪除備份', font=f, command=delete_backup,
                                     width=w, height=h)
    delete_backup_button.grid(row=3, column=1, sticky='nw')
    frame = tk.Frame(selection_window)
    developer_label = tk.Label(frame, text='Developed by EFLin')
    developer_label.pack(side='bottom', anchor='e')
    frame.grid(column=1)
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
    login_window.geometry('300x200')
    login_window.title('台南一中學習歷程備份系統')
    f = 'Microsoft_JhengHei 12'
    loginId_label = tk.Label(login_window, text='帳號：', font=f)
    loginId_label.pack()
    loginId_entry = tk.Entry(login_window, width=30)
    loginId_entry.pack()
    v = tk.BooleanVar()
    v.set(False)
    password_label = tk.Label(login_window, text='密碼：', font=f)
    password_label.pack()
    password_entry = tk.Entry(login_window, show='*', width=30)
    password_entry.pack()
    password_check = tk.Checkbutton(login_window, text='顯示密碼', variable=v, height=2, command=check, font=f)
    password_check.pack()
    login_button = tk.Button(login_window, text='登錄', command=create, font=f)
    login_button.pack()
    developer_label = tk.Label(login_window, text='Developed by EFLin')
    developer_label.pack(side='bottom', anchor='e')
    login_window.mainloop()


if __name__ == '__main__':
    interface = Interface()
