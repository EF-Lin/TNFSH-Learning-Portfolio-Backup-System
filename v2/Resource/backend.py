import asyncio
import io
import bs4
import requests as re
import ddddocr
import base64
import json
import os
from fake_useragent import UserAgent
import shutil
from PIL import Image
from datetime import datetime
import time


class Request:
    """爬資料"""
    # info
    # main_path = '.\\files'
    main_path = os.path.normpath('./files')
    path_list = ['/cadre', '/course_achievements', '/performers', '/user_info']
    tem_path_list = ['', '/course_achievements_2', '/performers_2']
    subject = ['幹部經歷', '課程學習成果', '多元表現']
    headers = {'user-agent': ''}
    file_list = []
    cadre_ex_list = []
    course_ach_list = []
    per_list = []
    tem_list = []
    file_type = '.txt'

    def __init__(self, data: dict):
        # init path
        for i in range(1, len(self.tem_path_list)):
            self.tem_path_list[i] = os.path.normpath(self.tem_path_list[i])
        for i in range(len(self.path_list)):
            self.path_list[i] = os.path.normpath(self.path_list[i])
        # info
        self.init_folders()
        self.init_texts()
        self.data = data
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

    def login(self) -> str:
        try:
            return self.req_login()
        except re.exceptions.ConnectionError:
            return 'Please check your internet.'
        except Exception as ex:
            return f'Unknown Error.\n{str(ex)}\n'

    def announcement(self) -> [bool, list, list, list] or [bool, str]:
        try:
            a, b, c = self.req_announcement()
            return True, [a, b, c]
        except re.exceptions.ConnectionError:
            return False, 'Please check your internet.'
        except Exception:
            return False, 'Unknown Error.'

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
            # f"JSONDecodeError: Backup {name[i]} failed, please try again."
            return f"Backup {name[i]} failed, please try again."
        except FileNotFoundError:
            return f"{name[i]}.txt is not exist."
        except re.exceptions.ConnectionError:
            # f'ConnectionError: Backup {name[i]} failed, please check your internet.'
            return f'Backup {name[i]} failed, please check your internet.'
        except Exception as ex:
            return f'Unknown Error.\n{str(ex)}\n'

    def backup_cadre_ex(self) -> str:
        try:
            asyncio.run(self.cadre_experience())
            return "S"
        except json.decoder.JSONDecodeError:
            # "JSONDecodeError: Backup cadre experiment failed, please try again."
            return "Backup cadre experiment failed, please try again."
        except re.exceptions.ConnectionError:
            # 'ConnectionError: Backup cadre experiment failed, please check your internet.'
            return 'Backup cadre experiment failed, please check your internet.'
        except Exception as ex:
            return f'Unknown Error.\n{str(ex)}\n'

    def backup_course_ach(self) -> str:
        try:
            asyncio.run(self.course_achievement())
            asyncio.run(self.download_course_ach())
            self.replace_folder(1)
            return "S"
        except FileNotFoundError:
            return "course_achievement.txt is not exist."
        except json.decoder.JSONDecodeError:
            # "JSONDecodeError: Backup course achievements failed, please try again."
            return "Backup course achievements failed, please try again."
        except re.exceptions.ConnectionError:
            # 'ConnectionError: Backup course achievements failed, please check your internet.'
            return 'Backup course achievements failed, please check your internet.'
        except Exception as ex:
            return f'Unknown Error.\n{str(ex)}\n'

    def backup_per(self) -> str:
        try:
            asyncio.run(self.performers())
            asyncio.run(self.download_per())
            self.replace_folder(2)
            return "S"
        except FileNotFoundError:
            return "FileNotFoundError: Performers.txt is not exist."
        except json.decoder.JSONDecodeError:
            # "JSONDecodeError: Backup performers failed, please try again."
            return "Backup performers failed, please try again."
        except re.exceptions.ConnectionError:
            # 'ConnectionError: Backup performers failed, please check your internet.'
            return 'Backup performers failed, please check your internet.'
        except Exception as ex:
            return f'Unknown Error.\n{str(ex)}\n'

    def orc(self, img):
        ORC = ddddocr.DdddOcr(show_ad=False)
        self.val_words = ORC.classification(img).lower()

    def generate_header(self):
        ua = UserAgent()
        self.headers['user-agent'] = ua.random

    def req_login(self):
        url = 'https://epf-mlife.k12ea.gov.tw/Login2.do'
        # request
        response = self.session_requests.get(url)
        soup = bs4.BeautifulSoup(response.text, 'html.parser')
        # get token
        token = soup.find('input', {'name': 'formToken'})['value']
        self.data['formToken'] = token
        # get validate photo
        response = self.session_requests.post('https://epf-mlife.k12ea.gov.tw/validate.do', {'d': 1})
        pic_url = response.text.split('\"')
        img = base64.b64decode(pic_url[3])
        self.orc(img)
        self.data['validateCode'] = self.val_words
        self.generate_header()
        response = self.session_requests.post(
            url=url,
            data=self.data,
            headers=self.headers
        )
        html = str(response.text)
        a = html.find('帳號或密碼錯誤')
        b = html.find('驗證碼輸入錯誤')
        if a == -1 and b == -1:
            i = html.find("name=\"session_key\" value=") + 26
            # 以i為指針找到"""
            j = html.find("\"", i)
            self.key = html[i:j]
            return 'S'
        else:
            return 'LOGIN ERROR: 帳號、密碼或驗證碼錯誤，請重新登錄。'

    def rewrite_text(self, i: int, file):
        if i == 4:
            path = self.main_path + 'file_list' + self.file_type
        else:
            path = self.main_path + self.path_list[i] * 2 + self.file_type
        self.generate_text(path, file)

    def req_text(self, i, url: str, data: dict):
        self.generate_header()
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
        """
        #資料整理
        file_info_str = response.text.split('},{')
        for i in file_info_str:
            try:
                # find name
                j = i.find("\"file\":\"") + 8
                k = i.find("\"", j)
                name = i[j:k]
                self.file_name.append(name)
                # find year
                j = i.find("\"syear\":\"") + 9
                k = i.find("\"", j)
                year = i[j:k]
                self.file_year.append(year)
            except:
                continue
        """

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
                self.generate_header()
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
                self.generate_header()
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

    def covert_image_to_pdf(self, files: tuple, name: str, size: list):
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
            print(ex)
            # IOError or Exception
            return False

    def req_announcement(self) -> [list, list, list]:
        url = 'https://epf-mlife.k12ea.gov.tw/student.do'
        self.generate_header()
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
        return announcement, date, deadline


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
    response = Request(Data)
    s = response.login()
