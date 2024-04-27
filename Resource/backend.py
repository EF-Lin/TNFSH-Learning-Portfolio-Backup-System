import asyncio
import io
import bs4
import requests as re
import base64
import json
import os
import shutil
from PIL import Image
from datetime import datetime
import time


class Request:
    """爬資料"""
    # info
    # main_path = '.\\files'
    main_path = os.path.normpath('files')
    path_list = ['/cadre', '/course_achievements', '/performers', '/user_info']
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
    tem_list = []
    file_type = '.txt'
    font_title_1 = 'Microsoft_JhengHei 18 bold'
    font_title_2 = 'Microsoft_JhengHei 18'
    font_text_1 = 'Microsoft_JhengHei 12 bold'
    font_text_2 = 'Microsoft_JhengHei 12'
    font_button = 'Microsoft_JhengHei 15'

    def __init__(self):
        # vars
        self.key = None
        self.val_words = None
        # init path
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
        #self.login()

    def __str__(self) -> str:
        return 'This is a spider'

    def mkdir(self, path):
        f = os.path.exists(path)
        if not f:
            os.makedirs(path)
        else:
            pass

    def generate_text(self, path, file):
        with open(path, 'w', encoding="utf-8") as t:
            t.write(str(file))

    def init_folders(self):
        self.mkdir(self.main_path)
        for i in self.path_list[0:3]:
            self.mkdir(self.main_path + i)

    def init_texts(self):
        def generate_blank_text(path):
            f = os.path.exists(path)
            if not f:
                open(path, 'w').close()
            else:
                pass

        for i in self.path_list[0:3]:
            generate_blank_text(self.main_path + i * 2 + self.file_type)

    def delete_all_files(self):
        for i in self.path_list[0:3]:
            path = self.main_path + i
            if os.path.exists(path):
                shutil.rmtree(path)
                self.init_folders()
                self.init_texts()
            else:
                pass

    def login(self, v: int) -> str:
        try:
            return self.req_login(v)
        except re.exceptions.ConnectionError:
            return 'ConnectionError'
        except Exception as ex:
            return f'Unknown Error.\n{str(ex)}\n'

    def announcement(self) -> [bool, list, list, list] or [bool, str]:
        try:
            return True, self.req_announcement()
        except re.exceptions.ConnectionError:
            return False, 'Please check your internet.'
        except AttributeError:
            return False, 'Please login first.'
        except Exception as ex:
            return False, f'Unknown Error.\n{str(ex)}'

    def backup_all(self) -> list:
        # s1 = self.backup_cadre_ex()
        # s2 = self.backup_course_ach()
        # s3 = self.backup_per()
        s1 = self.backup(0)
        s2 = self.backup(1)
        s3 = self.backup(2)
        return_list = []
        for i in [s1, s2, s3]:
            if i != "S":
                return_list.append(i)
        if not return_list:
            return []
        else:
            return return_list

    def backup(self, i: int) -> str:
        name = ['cadre experiment', 'course achievements', 'performers']
        try:
            if i == 0:
                asyncio.run(self.cadre_experience())
            elif i == 1:
                asyncio.run(self.course_achievement())
                asyncio.run(self.download_course_ach())
                self.replace_folder(1)
            elif i == 2:
                asyncio.run(self.performers())
                asyncio.run(self.download_per())
                self.replace_folder(2)
            return 'S'
        except json.decoder.JSONDecodeError:
            return f"Backup {name[i]} failed, please try again."
        except FileNotFoundError:
            return f"{name[i]}.txt is not exist."
        except re.exceptions.ConnectionError:
            return f'Backup {name[i]} failed, please check your internet.'
        except AttributeError:
            return 'Please login first.'
        except Exception as ex:
            return f'Unknown Error.\n{str(ex)}\n'

    def ocr(self):
        import ddddocr
        OCR = ddddocr.DdddOcr(show_ad=False)
        # get validate photo
        response = self.session_requests.post('https://epf-mlife.k12ea.gov.tw/validate.do', {'d': 1})
        self.val_words = OCR.classification(base64.b64decode(response.text.split('\"')[3])).lower()

    def get_validate_photo(self):
        try:
            from PIL import ImageTk
            response = self.session_requests.post('https://epf-mlife.k12ea.gov.tw/validate.do', {'d': 1})
            tk_img = ImageTk.PhotoImage(Image.open(io.BytesIO(base64.b64decode(response.text.split('\"')[3]))))
            return tk_img
        except re.exceptions.ConnectionError:
            return 'Please check your internet.'

    def req_login(self, v: int):
        url = 'https://epf-mlife.k12ea.gov.tw/Login2.do'
        # request
        response = self.session_requests.get(url)
        soup = bs4.BeautifulSoup(response.text, 'html.parser')
        # get token
        token = soup.find('input', {'name': 'formToken'})['value']
        self.data['formToken'] = token
        if v == 2:
            self.ocr()
            self.data['validateCode'] = self.val_words
        response = self.session_requests.post(
            url=url,
            data=self.data,
            headers=self.headers
        )
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
        elif d != -1:
            return 'ServiceError'
        else:
            return 'ValidateError'

    def rewrite_text(self, i: int, file):
        if i == 4:
            path = self.main_path + 'file_list' + self.file_type
        else:
            path = self.main_path + self.path_list[i] * 2 + self.file_type
        self.generate_text(path, file)

    def req_text(self, i, url: str, data: dict):
        response = self.session_requests.post(
            url=url,
            data=data,
            headers=self.headers
        )
        if i == 0:
            self.cadre_ex_list = (json.loads(response.text))['dataRows']
            self.rewrite_text(i, self.cadre_ex_list)
        elif i == 1:
            self.course_ach_list = (json.loads(response.text))['dataRows']
            self.rewrite_text(i, self.course_ach_list)
        elif i == 2:
            self.tem_list.extend(json.loads(response.text)["dataRows"])
        elif i == 2.5:
            self.per_list.extend(json.loads(response.text)["dataRows"])
        elif i == 3:
            self.file_list = json.loads(response.text)['list']
            self.rewrite_text(i, self.file_list)

    async def req_file_list(self):
        url = 'https://epf-mlife.k12ea.gov.tw/listStudentFiles.do'
        data = {
            'page': '1',
            'session_key': self.key
        }
        self.req_text(3, url, data)

    async def cadre_experience(self):
        url = 'https://epf-mlife.k12ea.gov.tw/serviceExperienceQuery.do'
        data = {
            'page': None,
            'session_key': self.key
        }
        self.req_text(0, url, data)

    async def course_achievement(self):
        url = 'https://epf-mlife.k12ea.gov.tw/courseEditQuery.do'
        data = {
            'type': 'upload',
            'subj': None,
            'syears': 'Y',
            'session_key': self.key
        }
        self.req_text(1, url, data)

    async def performers_all(self):
        url = 'https://epf-mlife.k12ea.gov.tw/listStudentPerformance.do'
        data = {
            'type': 'upload',
            'syear': '全部',
            'session_key': self.key
        }
        self.req_text(2, url, data)

    async def performers(self):
        data = {
            'page': '1',
            'session_key': self.key
        }
        for i in range(1, 11, 1):
            url = f'https://epf-mlife.k12ea.gov.tw/performance{i}Query.do'
            self.req_text(2, url, data)
            for j in self.tem_list:
                data2 = {
                    'id': j['id'],
                    'session_key': self.key
                }
                self.req_text(2.5, url, data2)
        self.rewrite_text(2, self.per_list)

    async def download_course_ach(self):
        if self.course_ach_list == {}:
            return FileNotFoundError
        else:
            self.mkdir(self.main_path + self.tem_path_list[1])
            for i in self.course_ach_list:
                uid = i["dp"]
                url = f'https://epf-mlife.k12ea.gov.tw/downloadCourseFile.do?path={uid}'
                response = self.session_requests.get(url, headers=self.headers)
                byte_io = io.BytesIO(response.content)
                with open(self.main_path + self.tem_path_list[1] + f'/{i["dn"]}', 'wb') as f:
                    f.write(byte_io.getvalue())

    async def download_per(self):
        if self.per_list == {}:
            return FileNotFoundError
        else:
            self.mkdir(self.main_path + self.tem_path_list[2])
            for i in self.per_list:
                uid = i['df1']
                url = f'https://epf-mlife.k12ea.gov.tw/performanceFile.do?path={uid}'
                response = self.session_requests.get(url, headers=self.headers)
                byte_io = io.BytesIO(response.content)
                path = self.main_path + self.tem_path_list[2] + f"/{i['certiName']}"
                with open(path, 'wb') as f:
                    f.write(byte_io.getvalue())

    def replace_folder(self, i):
        tem_path = self.main_path + self.tem_path_list[i]
        path = self.main_path + self.path_list[i]
        f = os.path.exists(tem_path)
        g = os.path.exists(path)
        if f is True and f == g:
            shutil.move(path + self.path_list[i] + self.file_type, tem_path + self.path_list[i] + self.file_type)
            shutil.rmtree(path)
            os.rename(tem_path, path)
        else:
            raise FileNotFoundError

    def covert_image_to_pdf(self, files: tuple, name: str, size: list) -> bool or str:
        try:
            img = [
                Image.open(f)
                for f in files
            ]
            for i in range(len(img)):
                w, h = img[i].size
                img[i].thumbnail((int(w * size[i] / 10), int(h * size[i] / 10)))
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
            return str(ex)

    def req_announcement(self) -> [list, list, list]:
        url = 'https://epf-mlife.k12ea.gov.tw/student.do'
        response = self.session_requests.post(
            url=url,
            headers=self.headers,
            data={
                'session_key': self.key,
                'model': '2'
            }
        )
        soup = bs4.BeautifulSoup(response.text, 'html.parser')
        s = str(soup.find(class_='tab-pane fade in active').text).split('\n')
        announcement = []
        date = []
        deadline = []
        now = datetime.fromtimestamp(time.time())
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


if __name__ == '__main__':
    loginId = str(input('請輸入帳號'))
    password = str(input('請輸入密碼'))
    Data = {
        'city': '12',
        'schNo': '210305.國立台南第一高級中學',
        'loginId': loginId,
        'password': password,
        'validateCode': '',
        'formToken': ''
    }
