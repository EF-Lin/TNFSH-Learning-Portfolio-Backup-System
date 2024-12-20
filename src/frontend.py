from backend import Request
from icon import icon
from dataclasses import dataclass
import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
import tkinter.ttk as ttk
import pyperclip
import os
import base64


def add_icon(window: tk.Tk):
    with open('tmp.ico', 'wb+') as d:
        d.write(base64.b64decode(icon))
    window.iconbitmap(default='tmp.ico')
    os.remove('tmp.ico')
    return window


@dataclass
class Main_interface(Request):
    """Usage: check_user_data()"""
    city = '12'
    schNo = '210305.國立台南第一高級中學'
    v: int

    def __post_init__(self):
        # init
        super().__init__()
        self.data = {
            'city': self.city,
            'schNo': self.schNo,
            'validateCode': '',
            'formToken': ''
        }
        # vars
        self.login_window: tk.Tk() = None
        self.selection_window: tk.Tk() = None
        self.if_login_str: tk.StringVar() = None
        self.if_login = False
        # user info
        self.user_info_path = self.main_path + self.path_list[3] + self.file_type
        # run
        # self.check_user_data()

    def __str__(self) -> str:
        return 'This is the main interface'

    def show_login(self):
        def login():
            loginId = loginId_entry.get()
            password = password_entry.get()
            self.init_user_info(loginId, password)
            self.show_validate_window() if self.v == 1 else self.check_user_data()

        def check():
            password_entry.config(show='') if v.get() else password_entry.config(show='*')

        self.login_window = tk.Tk()
        self.login_window.geometry('300x200')
        self.login_window.title('台南一中學習歷程備份系統')
        self.login_window = add_icon(self.login_window)
        loginId_label = tk.Label(self.login_window, text='帳號：', font=self.font_text_2)
        loginId_label.pack()
        loginId_entry = tk.Entry(self.login_window, width=30)
        loginId_entry.pack()
        v = tk.BooleanVar()
        v.set(False)
        password_label = tk.Label(self.login_window, text='密碼：', font=self.font_text_2)
        password_label.pack()
        password_entry = tk.Entry(self.login_window, show='*', width=30)
        password_entry.pack()
        password_check = tk.Checkbutton(self.login_window, text='顯示密碼', variable=v, height=2, command=check,
                                        font=self.font_text_2)
        password_check.pack()
        login_button = tk.Button(self.login_window, text='登入', command=login, font=self.font_text_2)
        login_button.pack()
        developer_label = tk.Label(self.login_window, text='Developed by EFLin')
        developer_label.pack(side='bottom', anchor='e')
        self.login_window.mainloop()

    def show_validate_window(self):
        def check_validate():
            self.data['validateCode'] = str(validate_entry.get())
            validate_window.destroy()
            self.try_login()

        img = self.get_validate_photo()
        if img == 'Please check your internet.':
            messagebox.showerror(title='錯誤', message=img)
        else:
            validate_window = tk.Toplevel()
            validate_window.title('驗證碼')
            validate_window.geometry('300x200')
            validate_label = tk.Label(validate_window, image=img)
            validate_label.pack()
            validate_title = tk.Label(validate_window, text='請輸入驗證碼')
            validate_title.pack()
            validate_entry = tk.Entry(validate_window)
            validate_entry.pack()
            validate_button = tk.Button(validate_window, text='確認', command=check_validate, width=5, height=2)
            validate_button.pack()
            validate_window.mainloop()

    def init_user_info(self, loginId: str, password: str):
        user_info = {
            'loginId': loginId,
            'password': password,
        }
        self.replace_text(self.user_info_path, user_info)

    def check_user_data(self) -> bool or None:
        f = os.path.exists(self.user_info_path)
        if not f:
            self.show_login()
        elif f and self.v == 1:
            self.show_selection_window()
        else:
            self.try_login()

    def try_login(self):
        def try_delete_windows():
            try:
                self.login_window.destroy()
            except:
                pass
            try:
                self.selection_window.destroy()
            except:
                pass

        with open(self.user_info_path, 'r') as f:
            user_info = eval(f.read())
        self.data.update(user_info)
        response = self.login(self.v)
        if response == 'S':
            self.if_login = True
            if self.v == 1:
                messagebox.showinfo(title='訊息', message='登入成功')
                try:
                    self.login_window.destroy()
                    self.show_selection_window()
                except:
                    self.if_login_str.set('是否登入:是')
            else:
                try_delete_windows()
                self.show_selection_window()
        elif response == 'ConnectionError':
            f = messagebox.askyesnocancel(title='錯誤',
                                          message='連線錯誤，是否重試?',
                                          detail='點擊「是」重新嘗試登入，點擊「否」進入選單介面，在離線模式下運行系統。')
            if self.v == 1 and f:
                self.show_validate_window()
            elif self.v == 2 and f:
                self.try_login()
            elif f is False:
                try_delete_windows()
                self.if_login = False
                self.show_selection_window()
            else:
                pass
        elif response == 'AccountOrPasswordError':
            f = messagebox.askyesnocancel(title='錯誤',
                                          message='帳號或密碼錯誤，是否重新輸入?',
                                          detail='點擊「是」重新輸入，點擊「否」進入選單介面，在離線模式下運行系統。')
            try_delete_windows()
            if f:
                self.show_login()
            elif f is False:
                self.if_login = False
                self.show_selection_window()
            else:
                pass
        elif response == 'ValidateError' and self.v == 1:
            f = messagebox.askyesnocancel(title='錯誤',
                                          message='驗證碼錯誤，是否重新輸入?',
                                          detail='點擊「是」重新輸入，點擊「否」進入選單介面，在離線模式下運行系統。')
            if f:
                self.show_validate_window()
            elif f is False:
                try_delete_windows()
                self.if_login = False
                self.show_selection_window()
            else:
                pass
        elif response == 'ValidateError' and self.v == 2:
            f = messagebox.askyesnocancel(title='錯誤',
                                          message='驗證碼錯誤，請重新嘗試。',
                                          detail='點擊「是」重新嘗試，點擊「否」進入選單介面，在離線模式下運行系統。')
            if f:
                self.try_login()
            elif f is False:
                try_delete_windows()
                self.if_login = False
                self.show_selection_window()
            else:
                pass
        else:
            f = messagebox.askyesnocancel(title='錯誤',
                                          message='點擊「是」重新嘗試登入，點擊「否」重新輸入帳號密碼。',
                                          detail=response)
            if f and self.v == 1:
                self.show_validate_window()
            elif f and self.v == 2:
                self.try_login()
            elif f is False:
                try_delete_windows()
                self.show_login()
            else:
                pass

    def load_data(self, i: int, repeater: int = 2) -> list or str:
        try:
            path = self.main_path + self.path_list[i] * repeater + self.file_type
            with open(path, 'r', encoding="utf-8") as f:
                if repeater == 1:
                    return f'最後備份時間: {str(f.read())}'
                else:
                    return eval(f.read())
        except SyntaxError:
            # SyntaxError: Please backup first.
            if repeater == 1:
                return ['尚未備份']
            else:
                messagebox.showerror(title='錯誤', message='無資料，請先備份，若已備份就是你沒有資料，爛透了。')
                return []
        except Exception as ex:
            messagebox.showerror(title='錯誤', message=f'{str(ex)}\nUnknown Error.')
            if repeater == 1:
                return ['尚未備份']
            else:
                return []

    def show_selection_window(self):
        def backup_all_and_show_message():
            error_message = self.backup_all()
            if error_message:
                for j in error_message:
                    messagebox.showerror(title='錯誤', message=j)
            else:
                self.last_bt_var.set(self.load_data(4, repeater=1))
                messagebox.showinfo(title='訊息', message='備份成功')

        def reset():
            yes = messagebox.askyesno(title='警告', message='是否要重新輸入帳號密碼?')
            if yes:
                self.selection_window.destroy()
                self.show_login()

        def delete_backup():
            yes = messagebox.askyesno(title='警告', message='此舉將刪除所有已備份文件、紀錄，並且不可回復!!!')
            if yes:
                check = simpledialog.askstring(parent=self.selection_window,
                                               title='確認', prompt='請輸入\"delete\"刪除所有已備份文件、紀錄。')
                self.delete_all_files() if check == 'delete' else 0

        self.selection_window = tk.Tk()
        self.if_login_str = tk.StringVar()
        self.if_login_str.set('是否登入:是') if self.if_login else self.if_login_str.set('是否登入:否')
        self.selection_window.title('台南一中學習歷程備份系統')
        self.selection_window.geometry('360x400')
        self.selection_window = add_icon(self.selection_window)
        self.selection_window.rowconfigure(tuple(i for i in range(6 - self.v)), weight=1)
        self.selection_window.columnconfigure((0, 1), weight=1)
        w = 8
        h = 3
        announcement_button = tk.Button(self.selection_window, text='公告', font=self.font_button,
                                        command=self.show_anno, width=w, height=h)
        announcement_button.grid(row=0, column=0, sticky='se')
        cadre_button = tk.Button(self.selection_window, text='幹部經歷', font=self.font_button,
                                 command=lambda: self.show_subject_window(0), width=w, height=h)
        cadre_button.grid(row=0, column=1, sticky='sw')
        course_ach_button = tk.Button(self.selection_window, text='學習成果', font=self.font_button,
                                      command=lambda: self.show_subject_window(1), width=w, height=h)
        course_ach_button.grid(row=1, column=0, sticky='e')
        per_button = tk.Button(self.selection_window, text='多元表現', font=self.font_button,
                               command=lambda: self.show_subject_window(2), width=w, height=h)
        per_button.grid(row=1, column=1, sticky='w')
        backup_button = tk.Button(self.selection_window, text='備份', font=self.font_button,
                                  command=backup_all_and_show_message, width=w, height=h)
        backup_button.grid(row=2, column=0, sticky='e')
        c = Covert()
        covert_img_button = tk.Button(self.selection_window, text='轉檔工具', font=self.font_button,
                                      command=c.show_covert_img, width=w, height=h)
        covert_img_button.grid(row=2, column=1, sticky='w')
        relogin_button = tk.Button(self.selection_window, text='重新登入', font=self.font_button,
                                   command=reset, width=w, height=h)
        relogin_button.grid(row=3, column=0, sticky='ne')
        delete_backup_button = tk.Button(self.selection_window, text='刪除備份', font=self.font_button,
                                         command=delete_backup, width=w, height=h)
        delete_backup_button.grid(row=3, column=1, sticky='nw')
        if self.v == 1:
            login_button = tk.Button(self.selection_window, text='登入', font=self.font_button,
                                     command=self.show_validate_window, width=16, height=2)
            login_button.grid(row=4, column=0, columnspan=2, sticky='n')
        frame = tk.Frame(self.selection_window)
        self.last_bt_var = tk.StringVar()
        self.last_bt_var.set(self.load_data(4, repeater=1))
        last_bt_lbl = tk.Label(frame, textvariable=self.last_bt_var)
        last_bt_lbl.pack()
        if_login_label = tk.Label(frame, textvariable=self.if_login_str)
        if_login_label.pack(anchor='e')
        developer_label = tk.Label(frame, text='Developed by EFLin')
        developer_label.pack(side='bottom', anchor='e')
        frame.grid(column=0, columnspan=2)
        self.selection_window.lift()
        self.selection_window.mainloop()

    def show_subject_window(self, sub_num: int):
        def create_tree_data():
            def copy_from_treeview():
                # refer from https://blog.csdn.net/vae565056149/article/details/128218467
                # 選取列
                selection = tree.selection()
                values = tree.item(selection[0])["values"]
                copy_str = ''
                items = list(self.cols.values())
                for i, j in zip(values, items):
                    copy_str += f'{j}: {str(i)}\n'
                pyperclip.copy(copy_str)

            global tree
            self.data = self.load_data(sub_num)
            window.lift()
            tree = ttk.Treeview(
                window,
                show='headings',
                columns=[i for i in range(len(self.cols))],
                yscrollcommand=scrollbar.set
            )
            for i in range(len(self.cols)):
                tree.column(i, width=80)
            j = 1
            for i in self.cols.values():
                tree.heading(f"#{j}", text=i)
                j += 1
            for i in self.data:
                data_list = []
                for j in self.cols.keys():
                    data_list.append(i[j])
                tree.insert('', index='end', text='', values=data_list)
            tree.bind('<3>', lambda x: copy_from_treeview())
            tree.pack()

        def backup_and_show_message() -> bool:
            s = self.backup(sub_num)
            self.last_bt_var.set(self.load_data(4, repeater=1))
            if s == 'S':
                messagebox.showinfo(parent=window, title='訊息', message='備份成功')
                return True
            else:
                messagebox.showerror(parent=window, title='錯誤', message=s)
                return False

        def rebuild_tree():
            successful = backup_and_show_message()
            if successful:
                tree.destroy()
                create_tree_data()

        window = tk.Toplevel()
        window.title(self.subject[sub_num])
        window.geometry('600x350')
        developer_label = tk.Label(window, text='Developed by EFLin')
        developer_label.pack(side='top', anchor='e')
        if sub_num == 0:
            self.cols = self.cadre_cols
        elif sub_num == 1:
            self.cols = self.course_cols
        elif sub_num == 2:
            self.cols = self.per_cols
        else:
            messagebox.showerror(title='警告', message='Unknown error')
            exit()
        path = self.main_path + self.path_list[sub_num]
        backup_button = tk.Button(window, text=f'備份{self.subject[sub_num]}', command=rebuild_tree)
        backup_button.pack()
        open_file_button = tk.Button(window, text='開啟資料夾', command=lambda: os.startfile(path))
        open_file_button.pack()
        note1_label = tk.Label(window, text='選中後點擊右鍵可複製。')
        note1_label.pack()
        scrollbar = tk.Scrollbar(window)
        scrollbar.pack(side='right', fill='y')
        create_tree_data()
        window.mainloop()

    def show_anno(self):
        successful, data = self.announcement()
        text = ''
        if successful:
            announcement, date, deadline = data[0], data[1], data[2]
            anno_window = tk.Toplevel()
            anno_window.title('公告')
            anno_window.geometry('500x300')
            anno_title_label = tk.Label(anno_window, text='公告', font=self.font_title_1)
            anno_title_label.pack()
            j = 0
            for i in range(len(announcement)):
                text += f'{announcement[i]} {date[j]} {date[j + 1]}\n'
                if not deadline[j + 1]:
                    text += '時間截止，你死了!\n\n'
                else:
                    text += f'距離時間截止還剩下{deadline[j + 1]}，趕快去做事，懶骨頭。\n\n'
                j += 2
            anno_label = tk.Label(anno_window, text=text, font=self.font_text_1)
            anno_label.pack()
            developer_label = tk.Label(anno_window, text='Developed by EFLin')
            developer_label.pack(side='bottom', anchor='e')
            anno_window.mainloop()
        else:
            messagebox.showerror(title='錯誤', message=data)


@dataclass
class Covert(Request):
    def __post_init__(self):
        self.files: tuple = ()
        self.img_size: list = []

    def __str__(self):
        return 'This is a tool which can covert images to pdf.'

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
                                                 filetypes=[('image files', '.png;*.jpg;*.jpeg')])
        self.frame.pack_forget()
        self.frame = tk.Frame(self.show_covert_img_window)
        self.img_size = [tk.IntVar() for _ in range(len(self.files))]
        message = tk.Label(self.frame, text='調整大小，10為不變，9為0.9倍，以此類推。')
        message.pack()
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
            covert_successful = self.covert_image_to_pdf(files=self.files,
                                                         name=self.file_name.get(),
                                                         size=size)
            if covert_successful:
                os.startfile(self.main_path)
            else:
                messagebox.showerror(title='錯誤', message=f'{covert_successful}\n轉換失敗。')


if __name__ == '__main__':
    version = 2
    interface = Main_interface(version)
    interface.check_user_data()
