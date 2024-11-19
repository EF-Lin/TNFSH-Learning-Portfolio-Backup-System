import asyncio
import io
import bs4
import requests as re
import base64
import json
import os
import shutil
from PIL import Image, ImageFile
from datetime import datetime
import tkinter as tk
from tkinter.ttk import Progressbar


class Request:
    """爬資料"""
    # info
    path_list = ['/cadre', '/course_achievements', '/performers', '/user_info', '/time']
    tem_path_list = ['', '/course_achievements_2', '/performers_2']
    subject = ['幹部經歷', '課程學習成果', '多元表現']
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
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'}
    file_list = []
    cadre_ex_list = []
    course_ach_list = []
    per_list = []
    file_type = '.txt'
    font_title_1 = 'Microsoft_JhengHei 18 bold'
    font_title_2 = 'Microsoft_JhengHei 18'
    font_text_1 = 'Microsoft_JhengHei 12 bold'
    font_text_2 = 'Microsoft_JhengHei 12'
    font_button = 'Microsoft_JhengHei 15'

    def __init__(self):
        # init path
        self.main_path = os.path.normpath('files')
        for i in range(1, len(self.tem_path_list)):
            self.tem_path_list[i] = os.path.normpath(self.tem_path_list[i])
        for i in range(len(self.path_list)):
            self.path_list[i] = os.path.normpath(self.path_list[i])
        # info
        self.init_folders()
        self.init_texts()
        self.data = {
            'city': '12',
            'schNo': '210305.國立台南第一高級中學',
            'loginId': '',
            'password': '',
            'validateCode': '',
            'formToken': ''
        }
        # create session
        self.session_requests = re.session()
        # self.login()

    def __str__(self) -> str:
        return 'This is a spider.'

    @staticmethod
    def mkdir(path):
        f = os.path.exists(path)
        os.makedirs(path) if not f else 0

    @staticmethod
    def replace_text(path, file):
        with open(path, 'w', encoding="utf-8") as t:
            t.write(str(file))

    @staticmethod
    def generate_blank_text(path):
        f = os.path.exists(path)
        if not f:
            open(path, 'w').close()

    @staticmethod
    def generate_processbar(num) -> [tk.Toplevel, Progressbar, tk.StringVar]:
        processbar_window = tk.Toplevel()
        processbar_window.title("下載進度")
        processbar_window.geometry('300x100')
        dl_file_name = tk.StringVar()
        dl_file_name.set('')
        name_label = tk.Label(processbar_window, textvariable=dl_file_name)
        name_label.pack()
        processbar = Progressbar(processbar_window, maximum=num, length=200)
        processbar.pack()
        processbar_window.lift()
        return processbar_window, processbar, dl_file_name

    def init_folders(self):
        self.mkdir(self.main_path)
        for i in self.path_list[0:3]:
            self.mkdir(self.main_path + i)

    def init_texts(self):
        for i in self.path_list[0:3]:
            self.generate_blank_text(f'{self.main_path}{i*2}{self.file_type}')
        self.generate_blank_text(f'{self.main_path}{self.path_list[4]}{self.file_type}')

    def delete_all_files(self):
        for i in self.path_list[0:3]:
            path = self.main_path + i
            if os.path.exists(path):
                shutil.rmtree(path)
                self.init_folders()
                self.init_texts()
            else:
                pass

    def __rewrite_text(self, i: int, file):
        """
        if i == 4:
            path = self.main_path + 'file_list' + self.file_type
        """
        self.replace_text(self.main_path + self.path_list[i] * 2 + self.file_type, file)

    def __post_data(self, url: str, data: dict) -> re.models.Response:
        response = self.session_requests.post(
            url=url,
            data=data,
            headers=self.headers
        )
        return response

    def login(self, v: int) -> str:
        try:
            return self._req_login(v)
        except re.exceptions.ConnectionError:
            return 'ConnectionError'
        except Exception as ex:
            return f'Unknown Error.\n{str(ex)}\n'

    def backup(self, i: int) -> str:
        name = ['cadre experiment', 'course achievements', 'performers']
        try:
            match i:
                case 0:
                    self.cadre_experience()
                case 1:
                    self.course_achievement()
                    self.download_course_ach()
                case 2:
                    self.performers()
                    self.download_per()
                case _:
                    return 'Error input.'
            self.update_time()
            return 'S'
        except json.decoder.JSONDecodeError:
            return f"Backup {name[i]} failed, please try again."
        except FileNotFoundError:
            return f"Backup {name[i]} data list failed"
        except re.exceptions.ConnectionError:
            return f'Backup {name[i]} failed, please check your internet.'
        except AttributeError:
            return 'Please login first.'
        except Exception as ex:
            return f'Unknown Error.\n{str(ex)}\n'

    def backup_all(self) -> list:
        message_list = []
        for i in range(3):
            s = self.backup(i)
            0 if s == 'S' else message_list.append(s)
        return message_list

    def announcement(self) -> [bool, list, list, list] or [bool, str]:
        try:
            return True, self.req_announcement()
        except re.exceptions.ConnectionError:
            return False, 'Please check your internet.'
        except AttributeError:
            return False, 'Please login first.'
        except Exception as ex:
            return False, f'Unknown Error.\n{str(ex)}'

    def get_validate_photo(self):
        try:
            from PIL import ImageTk
            response = self.__post_data(url='https://epf-mlife.k12ea.gov.tw/validate.do', data={'d': 1})
            return ImageTk.PhotoImage(Image.open(io.BytesIO(base64.b64decode(response.text.split('\"')[3]))))
        except re.exceptions.ConnectionError:
            return 'Please check your internet.'

    def _req_login(self, v: int):
        def ocr() -> str:
            import ddddocr
            orc = ddddocr.DdddOcr(show_ad=False, beta=True)
            # get validate photo
            return orc.classification(base64.b64decode(self.__post_data(url='https://epf-mlife.k12ea.gov.tw/validate.do',
                                                                        data={'d': 1}).text.split('\"')[3])).lower()

        url = 'https://epf-mlife.k12ea.gov.tw/Login2.do'
        # request
        response = self.session_requests.get(url)
        soup = bs4.BeautifulSoup(response.text, 'html.parser')
        # get token
        self.data['formToken'] = soup.find('input', {'name': 'formToken'})['value']
        if v == 2:
            self.data['validateCode'] = ocr()
        response = self.__post_data(url=url, data=self.data)
        html = str(response.text)
        a = html.find('帳號或密碼錯誤')
        b = html.find('驗證碼輸入錯誤')
        c = html.find('驗證碼錯誤！')
        d = html.find('資料處理時發生錯誤')
        if a == -1 and b == -1 and c == -1 and d == -1:
            i = html.find("name=\"session_key\" value=") + 26
            # 以i為指針找到"""
            j = html.find("\"", i)
            self.key = html[i:j]
            return 'S'
        elif a != -1:
            return 'AccountOrPasswordError'
        elif b != -1 or c != -1:
            return 'ValidateError'
        else:
            return 'ServiceError'

    def __req_file_list(self):
        url = 'https://epf-mlife.k12ea.gov.tw/listStudentFiles.do'
        data = {
            'page': '1',
            'session_key': self.key
        }
        self.__post_data(url, data)

    def cadre_experience(self):
        url = 'https://epf-mlife.k12ea.gov.tw/serviceExperienceQuery.do'
        data = {
            'page': None,
            'session_key': self.key
        }
        self.cadre_ex_list = (json.loads(self.__post_data(url, data).text))['dataRows']
        self.__rewrite_text(0, self.cadre_ex_list)

    def course_achievement(self):
        url = 'https://epf-mlife.k12ea.gov.tw/courseEditQuery.do'
        data = {
            'type': 'upload',
            'subj': None,
            'syears': 'Y',
            'session_key': self.key
        }
        self.course_ach_list = (json.loads(self.__post_data(url, data).text))['dataRows']

    def __performers_all(self):
        url = 'https://epf-mlife.k12ea.gov.tw/listStudentPerformance.do'
        data = {
            'type': 'upload',
            'syear': '全部',
            'session_key': self.key
        }
        return json.loads(self.__post_data(url, data).text)["dataRows"]

    def performers(self):
        data = {
            'page': '1',
            'session_key': self.key
        }
        tem_list = []
        for i in range(1, 11, 1):
            url = f'https://epf-mlife.k12ea.gov.tw/performance{i}Query.do'
            tem_list.extend(json.loads(self.__post_data(url, data).text)["dataRows"])
            for j in tem_list:
                data2 = {
                    'id': j['id'],
                    'session_key': self.key
                }
                self.per_list.extend(json.loads(self.__post_data(url, data2).text)["dataRows"])

    def __replace_folder(self, i):
        tem_path = self.main_path + self.tem_path_list[i]
        path = self.main_path + self.path_list[i]
        f = os.path.exists(tem_path)
        g = os.path.exists(path)
        if f and g is True:
            shutil.rmtree(path)
            os.rename(tem_path, path)
        else:
            raise FileNotFoundError

    def download_course_ach(self):
        async def dl(url, file, index):
            nonlocal loop, bar, dl_file_name
            response = await loop.run_in_executor(executor=None,
                                                  func=lambda: self.session_requests.get(url, headers=self.headers))
            byte_io = io.BytesIO(response.content)
            name: str = file["dn"]
            dl_file_name.set(name)
            path = self.main_path + self.tem_path_list[1]
            if name in name_dict.keys():
                name_dict[name] += 1
                n = name.split('.')
                n[0: -1] = [''.join(n[0: -1])]
                path += f"/{n[0]} ({name_dict[name]}).{n[1]}"
                rename_course_ach_list[index]["dn"] = f'{n[0]} ({name_dict[name]}).{n[1]}'
            else:
                name_dict[name] = 1
                path += f'/{name}'
            with open(path, 'wb') as f:
                f.write(byte_io.getvalue())
            bar['value'] += 1
            bar.update()

        if self.course_ach_list is []:
            raise FileNotFoundError
        else:
            self.mkdir(self.main_path + self.tem_path_list[1])
            name_dict = {}
            rename_course_ach_list = self.course_ach_list
            window, bar, dl_file_name = self.generate_processbar(len(rename_course_ach_list))
            loop = asyncio.new_event_loop()
            tasks = []
            for i, j in zip(self.course_ach_list, range(len(rename_course_ach_list))):
                tasks.append(loop.create_task(dl(f'https://epf-mlife.k12ea.gov.tw/downloadCourseFile.do?path={i["dp"]}', i, j)))
            loop.run_until_complete(asyncio.wait(tasks))
            self.__replace_folder(1)
            self.__rewrite_text(1, rename_course_ach_list)
            window.destroy()

    def download_per(self):
        async def dl(url, file, index):
            nonlocal loop, bar, dl_file_name
            response = await loop.run_in_executor(executor=None,
                                                  func=lambda: self.session_requests.get(url, headers=self.headers))
            byte_io = io.BytesIO(response.content)
            name: str = file['certiName']
            dl_file_name.set(name)
            path = self.main_path + self.tem_path_list[2]
            if name in name_dict.keys():
                name_dict[name] += 1
                n = name.split('.')
                n[0: -1] = [''.join(n[0: -1])]
                path += f"/{n[0]} ({name_dict[name]}).{n[1]}"
                rename_per_list[index]['certiName'] = f'{n[0]} ({name_dict[name]}).{n[1]}'
            else:
                name_dict[name] = 1
                path += f"/{name}"
            with open(path, 'wb') as f:
                f.write(byte_io.getvalue())
            bar['value'] += 1
            bar.update()

        if self.per_list == {}:
            raise FileNotFoundError
        else:
            self.mkdir(self.main_path + self.tem_path_list[2])
            name_dict = {}
            rename_per_list = self.per_list
            window, bar, dl_file_name = self.generate_processbar(len(rename_per_list))
            loop = asyncio.new_event_loop()
            tasks = []
            for i, j in zip(self.per_list, range(len(rename_per_list))):
                tasks.append(loop.create_task(dl(f'https://epf-mlife.k12ea.gov.tw/performanceFile.do?path={i['df1']}', i, j)))
            loop.run_until_complete(asyncio.wait(tasks))
            self.__replace_folder(2)
            self.__rewrite_text(2, rename_per_list)
            window.destroy()

    def covert_image_to_pdf(self, files: tuple, name: str, size: list) -> bool or str:
        try:
            ImageFile.LOAD_TRUNCATED_IMAGES = True
            img = [
                Image.open(f)
                for f in files
            ]
            for i in range(len(img)):
                w, h = img[i].size
                img[i].thumbnail((int(w * size[i] / 10), int(h * size[i] / 10)))
            img[0] = img[0].transpose(Image.ROTATE_180)
            """
            r = [Image.ROTATE_90, Image.ROTATE_90]
            for i in range(0, 2):
               img[i] = img[i].transpose(r[i])
            """
            pdf_path = os.path.normpath(self.main_path + f"/{name}.pdf")
            img[0].save(
                pdf_path, "PDF",
                save_all=True,
                append_images=img[1:],
                resolution=100.0
            )
            return True
        except Exception as ex:
            # IOError or Exception
            # print(ex)
            return str(ex)

    def req_announcement(self) -> [list, list, list]:
        url = 'https://epf-mlife.k12ea.gov.tw/student.do'
        data = {
            'session_key': self.key,
            'model': '2'
        }
        response = self.__post_data(url, data)
        soup = bs4.BeautifulSoup(response.text, 'html.parser')
        s = str(soup.find(class_='tab-pane fade in active').text).split('\n')
        announcement = []
        date = []
        deadline = []
        now = datetime.now()
        for i in range(len(s)):
            if s[i] != '':
                n = "".join(s[i].split())
                i = n.find('間')
                announcement.append(n[:i + 1])
                for j in n[i + 1:].split('~'):
                    t = datetime.strptime(j, '%Y/%m/%d%H:%S')
                    date.append(str(t.date()))
                    if int((t - now).days) == 0:
                        deadline.append(f'{int((t - now).seconds) / 3600:.1f}小時')
                    elif int((t - now).days) > 0:
                        deadline.append(f'{int((t - now).days)}天')
                    else:
                        deadline.append(False)
            else:
                pass
        return [announcement, date, deadline]

    def update_time(self):
        self.replace_text(path=f'{self.main_path}{self.path_list[4]}{self.file_type}',
                          file=f'{datetime.now().year - 1911}/{datetime.now().strftime('%m/%d %H:%M')}')


if __name__ == '__main__':
    # loginId = str(input('請輸入帳號'))
    # password = str(input('請輸入密碼'))
    Data = {
        'city': '12',
        'schNo': '210305.國立台南第一高級中學',
        'loginId': '',
        'password': '',
        'validateCode': '',
        'formToken': ''
    }
