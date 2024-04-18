# 台南一中學習歷程備份系統
一個簡單的學習歷程的本地端。


## 簡介
- 教育部的學習歷程伺服器經常無故損毀，因此這個備份系統便誕生了，此系統能夠幫助你快速**登入學習歷程網站、備份課程學習成果、多元表現與幹部經歷的檔案和資料**，並以清單形式呈現，讓使用者能隨時隨地取用學習歷程資料。
- 除了備份功能外，本系統還附有簡易轉檔工具，能將多張圖片轉為單個pdf，幫助要上傳檢定證照、證明的使用者快速將掃描後的圖片整合為pdf，而不用將個人隱私資料上傳到來路不明的網站。
- 本系統**僅限台南一中學生專用**，其他學校要用請自行修改Resource/frontend.py/Interface中的city和schNo，但需先確認學校使用的學習歷程網站是[這個網站](https://epf-mlife.k12ea.gov.tw/)。
- 本系統為提供學生二次確認的備份系統，主要之學習歷程資料請以[台南一中學習歷程網站](https://epf-mlife.k12ea.gov.tw/)為主。


## 版本
### v1
- 需手動輸入驗證碼，運行速度較快。
- 無自動登入，每次均需手動登入。

### v2
- 自動辨別驗證碼，需要較大空間，運行速度較慢。
- 辨識驗證碼功能使用ddddocr。
- 有自動登入功能。
- 有使用fake_useragent，每次向網站要求資料均會生成隨機header，較不容易被封鎖。


## 安裝
### v1
1. 下載"TNFSH_Backup_System_v1.exe"和"icon.ioc"。
2. 將兩個檔案放進同個資料夾中，運行"TNFSH_Backup_System_v1.exe"。
3. ~~等待教育部學習檔案網站被損毀體現備份系統的重要性。~~ 

### v2
1. 自[Python官網](https://www.python.org/downloads/release/python-3123/)下載Python3.12，或點[這裡](https://www.python.org/ftp/python/3.12.3/python-3.12.3-amd64.exe)下載。
2. 安裝Python
   - 自動安裝：一路點選Next並確認選取方塊都有打勾。
   - 手動安裝：所有Option Features皆須安裝。
3. 選擇要下載的備份系統版本。
4. 運行setup.bat。
5. 確認運行過程中沒有出現紅字，有的話請檢查Python以及基本套件是否安裝正確或查看[常見錯誤](#無法運行系統)。
6. 運行TNFSH_Learning_Portfolio_Backup_System.bat。
7. ~~等待教育部學習檔案網站被損毀體現備份系統的重要性。~~ 


## 使用
### 登入
#### v1
第一次登入後系統會自動紀錄使用者的帳號、密碼，往後開啟皆會直接進入主選單介面。
#### v2
每次開啟系統均需手動點選「**登入**」按鈕並輸入驗證碼，否則會導致無法爬取資料而報錯，詳見[常見錯誤](#please-login-first)。

*附註:登入狀態均顯示在右下角。*

### 重新登入
若要登入其他帳號請點選主選單中的「**重新登入**」，可轉跳至登入介面，若想維持原先帳號直接關閉視窗並重啟本系統即可。

### 公告
登入後點選「**公告**」可查看課程學習成果與多元表現上傳、勾選截止時間，並~~貼心地敦促或嘲諷使用者~~。

### 備份
登入後點選主選單中的「**備份**」可備份幹部經歷，另外，在各單項視窗中也能單獨備份課程學習成果、多元表現與幹部經歷，若備份失敗請查看[常見錯誤](#backup--failed-please-try-again)。

<mark>注意</mark>:***點選「備份」後需耐心等待系統完成下載資料，提早關閉、縮小視窗可能導致備份失敗。***

### 查看已備份資料
在各單項視窗中能查看已備份資料，即使無連上網路、登入也能查看，且選中項目後點擊右鍵能夠複製該行資料，點擊「**開啟資料夾**」能打開存放備份文件的資料夾，供使用者自行取用檔案。

### 刪除備份
點選「**刪除備份**」並確認後會刪除所有已備份之課程學習成果、多元表現與幹部經歷檔案與資料。

<mark>注意</mark>:***此過程為不可逆，刪除前請三思!!!***

### 圖片轉pdf
點選「**轉檔工具**」後會進入轉檔視窗，請選取圖片(格式可為png、jpg、jpge)、輸入檔案名稱(默認為file.pdf)並分別調整每張圖片大小。

<mark>注意</mark>:***調整大小也會影響到圖片畫質及大小，若想壓縮檔案者可善用此功能。***


## 常見錯誤
### 無法運行系統
可能是安裝Python時出現問題，請檢查pip是否已被安裝，並重新執行setup.bat。
或是嘗試在安裝Python後手動安裝以下庫：
| 函式庫名稱       | 安裝指令                      |
| :------------- | :-------------------------- |
| Asyncio        | pip install asyncio         |
| IO             | pip install Python-IO&nbsp; |
| BeautifulSoup4 | pip install bs4             |
| Requests       | pip install requests        |
| Shutil         | pip install pytest-shutil   |
| PIL            | pip install Pillow          |
| Fake_useragent | pip install fake_useragent  |
| DateTime       | pip install DateTime        |
| Dataclasses    | pip install dataclasses     |
| Tkinter        | pip install tk              |
| Pyperclip      | pip install pyperclip       |
| 带带弟弟OCR      | pip install ddddocr         |

### 系統錯誤
#### Please check your internet.
網路連線錯誤，請檢查網路是否正確連接。

#### Backup ... failed, please check your internet.
同上。

#### 無資料，請先備份...
系統讀取不到資料，這可能是由於未備份或使用者無資料所導致，若未備份，點擊相關「**備份**」即可。

#### Backup ... failed, please try again.
無法爬取檔案，大多數情況重複試幾次即可解決。

#### ....txt is not exist.
儲存備份文件的文字檔不存在，這可能是由於使用者意外刪除了文字檔，重啟系統即可解決。

#### Unknown Error.
未知錯誤，請回報至issues。

#### Please login first.
v1版本特殊錯誤，需先點選「**登入**」並輸入驗證碼，跳出訊息「**登入成功**」即可解決。


## 改善目標(未定)
- 新增選擇縣市與學校功能，擴大使用群體。
- 新增備份進度條。
- 重新建構程式邏輯。
