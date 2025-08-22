# 台南一中學習歷程備份系統
一個簡單的學習歷程的本地端。

>[!WARNING]
>自114學年度起因開發者畢業，學習歷程系統帳號被註銷無法進行任何測試。故往後更新僅確保程式順利運行，不保證能否正確爬到資料。


## 簡介
- 教育部的學習歷程伺服器經常無故損毀，因此這個備份系統便誕生了，此系統能夠幫助你快速**登入學習歷程網站、備份課程學習成果、多元表現與幹部經歷的檔案和資料**，並以清單形式呈現，讓使用者能隨時隨地取用學習歷程資料。
- 除了備份功能外，本系統還附有簡易轉檔工具，能將多張圖片轉為單個pdf，幫助要上傳檢定證照、證明的使用者快速將掃描後的圖片整合為pdf，而不用將個人隱私資料上傳到來路不明的網站。
- 本系統**僅限台南一中學生專用**，其他學校要用請自行修改`src/frontend.py/Interface`中的`city`和`schNo`，但需先確認學校使用的學習歷程網站是[這個網站](https://epf-mlife.k12ea.gov.tw/)。
- 本系統為提供學生二次確認的備份系統，主要的學習歷程資料請以[台南一中學習歷程網站](https://epf-mlife.k12ea.gov.tw/)為主。


## 聲明
1. 本系統不會蒐集任何使用者的資料，系統運行僅限於使用者之電腦。
2. 本系統不會修改、刪除使用者於學習歷程網站中的任何資料，請安心服用。
3. 本系統不對使用者備份之學習歷程資料遺失、損毀、內容錯誤等異常情況負擔任何責任。


## 版本差異
### v1
- 無自動登入，每次均需手動需輸入驗證碼登入。
- 有windows執行擋。

### v2
- 使用ddddocr自動辨別驗證碼，開啟系統即會自動登入。


## 安裝
### v1
1. 至[Releases](https://github.com/EF-Lin/TNFSH-Learning-Portfolio-Backup-System/releases)中下載最新版本的"TNFSH_Backup_System_v1_vxxx.exe"。
2. 運行"TNFSH_Backup_System_v1_vxxx.exe"。
3. ~~等待教育部學習檔案網站被損毀體現備份系統的重要性。~~

*v1也可以不使用執行擋改用python運行，請參考[v2](#v2)。

### v2
#### 安裝Python
1. 至[Python官網](https://www.python.org/downloads/release/python-3123/)下載Python3.12，或點[這裡](https://www.python.org/ftp/python/3.12.3/python-3.12.3-amd64.exe)下載。
2. 一路點選Next並確認選取方塊都有打勾。

#### 安裝環境
1. 下載[台南一中學習歷程備份系統](https://github.com/EF-Lin/TNFSH-Learning-Portfolio-Backup-System/archive/refs/heads/master.zip)並解壓縮至本機。
2. 在"台南一中學習歷程備份系統"所在資料夾開啟命令提示字元並運行指令：
```bash
# pip
pip install -e .

# uv
uv sync
```
3. 確認運行過程中沒有出現紅字，有的話請檢查Python以及基本套件是否安裝正確或查看[常見錯誤](#無法運行v2版本系統)。
4. 運行"TNFSH_Learning_Portfolio_Backup_System_v2.bat"或運行以下指令。
```bash
# powershell
.venv\Scripts\Activate.ps1
python v2_main.py

# cmd
.venv\Scripts\activate.bat
python v2_main.py

# uv
uv run v2_main.py
```
5. ~~等待教育部學習檔案網站被損毀體現備份系統的重要性。~~


## 使用
### 首次登入
#### v1
輸入帳號、密碼和驗證碼即可登入並進入系統。
#### v2
輸入帳號和密碼即可登入並進入系統。

### 後續使用
系統會自動紀錄使用者的帳號、密碼，不須重複輸入。
#### v1
預設以離線模式進入系統，每次均需手動點選「**登入**」按鈕並輸入驗證碼，否則會導致無法爬取資料而報錯，詳見[常見錯誤](#please-login-first)。
#### v2
直接開啟系統即可進入主選單介面，若失敗請查看[常見錯誤](#登入錯誤)
>[!NOTE]
>附註:右下角會顯示當前登入狀態。

### 重新登入
若要登入其他帳號請點選主選單中的「**重新登入**」，可轉跳至登入介面，若想維持原先帳號直接關閉視窗並重啟本系統即可。

### 公告
登入後點選「**公告**」可查看課程學習成果與多元表現上傳、勾選截止時間，並~~貼心地敦促或嘲諷使用者~~。

### 備份
登入後點選主選單中的「**備份**」可備份幹部經歷，另外，在各單項視窗中也能單獨備份課程學習成果、多元表現與幹部經歷，若備份失敗請查看[常見錯誤](#backup--failed-please-try-again)。
>[!CAUTION]
> - 點選「備份」後需耐心等待系統完成下載資料，提早關閉、縮小視窗可能導致備份失敗。
> - 重複的檔案名稱將自動被命名為"原檔案名稱(*2, 3...*).副檔名"

### 查看已備份資料
在各單項視窗中能查看已備份資料，即使無連上網路、登入也能查看，且選中項目後點擊右鍵能夠複製該行資料，點擊「**開啟資料夾**」能打開存放備份文件的資料夾，供使用者自行取用檔案。

### 刪除備份
點選「**刪除備份**」並確認後會刪除所有已備份之課程學習成果、多元表現與幹部經歷檔案與資料。
>[!CAUTION]
>此過程為不可逆，刪除前請三思!!!

### 圖片轉pdf
點選「**轉檔工具**」後會進入轉檔視窗，請選取圖片(格式可為png、jpg、jpge)、輸入檔案名稱(默認為file.pdf)並分別調整每張圖片大小。
>[!TIP]
>調整大小也會影響到圖片畫質及大小，若想壓縮檔案者可善用此功能。


## 常見錯誤
### 無法運行v2版本系統
可能是安裝Python時出現問題，請檢查pip是否已被安裝，並[安裝環境](#安裝環境)。
或嘗試在安裝Python後手動安裝以下庫：
| 函式庫名稱      | 安裝指令                     |
| :------------- | :-------------------------- |
| BeautifulSoup4 | pip install bs4             |
| Requests       | pip install requests        |
| PIL            | pip install Pillow          |
| Pyperclip      | pip install pyperclip       |
| 带带弟弟OCR     | pip install ddddocr         |

### 登入錯誤
#### 連線錯誤，是否重試?
網路連線錯誤，請檢查網路是否正確連接；或以離線模式運行系統。

#### 帳號或密碼錯誤，是否重新輸入?
請檢查帳號或密碼是否正確；或以離線模式運行系統。

#### 驗證碼錯誤，是否重新輸入?
v1版本錯誤，使用者輸入錯誤的驗證碼，請重新輸入；或以離線模式運行系統。

#### 驗證碼錯誤，請重新嘗試。
v2版本錯誤，ddddocr自動辨別驗證碼失敗或辨別錯誤的驗證碼，多試幾次即可解決；或以離線模式運行系統。

#### 錯誤
未知錯誤，請回報到[issues](https://github.com/EF-Lin/TNFSH-Learning-Portfolio-Backup-System/issues)。

### 備份錯誤
#### Please check your internet.
網路連線錯誤，請檢查網路是否正確連接。

#### Backup ... failed, please check your internet.
同上。

#### 無資料，請先備份...
系統讀取不到資料，這可能是由於未備份或使用者無資料所導致，若未備份，點擊相關「**備份**」即可。

#### Backup ... failed, please try again.
無法爬取檔案，大多數情況重複試幾次即可解決。

#### Backup ... data list failed
備份檔案清單失敗，請重新嘗試。

#### Please login first.
v1版本特殊錯誤，需先點選「**登入**」並輸入驗證碼，跳出訊息「**登入成功**」即可解決。

#### Unknown Error.
未知錯誤，請回報至[issues](https://github.com/EF-Lin/TNFSH-Learning-Portfolio-Backup-System/issues)。

### 圖片轉pdf錯誤
#### 請選擇檔案
不可無圖檔，請先選擇圖片。

#### 請輸入檔案名稱
pdf檔案名不可為空，請輸入生成pdf的檔案名稱。
