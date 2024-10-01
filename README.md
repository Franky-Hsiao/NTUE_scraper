# NTUE_scraper

## 簡介
  這個程式來自我和朋友製作的 NTUE 學習管理應用的片段，其主要功能為從 iNTUE 的網頁上，抓取該學生的課表等資訊傳送我們的 APP 裡，
  另外因應網頁裡的驗證碼需求，我使用了 OCR 技術做辨識，並利用 openCV 做影像處理，有效的將辨識成功率提升至九成以上。

### 困難的點

- 存取驗證碼網址會導致其圖片更換
- 直接對驗證碼圖片做辨識的成功率極低

### 驗證碼作處理前後差異
<table>
  <tr>
    <td><img src="https://github.com/Franky-Hsiao/NTUE_scraper/blob/main/image/input_1.png" alt="圖一輸出前" width="300"/></td>
    <td><img src="https://github.com/Franky-Hsiao/NTUE_scraper/blob/main/image/input_2.png" alt="圖二輸出前" width="300"/></td>
  </tr>
  <tr>
    <td><img src="https://github.com/Franky-Hsiao/NTUE_scraper/blob/main/image/output_1.png" alt="圖一輸出後" width="300"/></td>
    <td><img src="https://github.com/Franky-Hsiao/NTUE_scraper/blob/main/image/output_2.png" alt="圖二輸出後" width="300"/></td>
  </tr>
</table>

### 功能&特點

- 能從 iNTUE 網頁上有效地讀取資料
- 正確擷取驗證碼圖片做辨識
- 利用 openCV 裡的侵蝕、膨脹和二值化等功能做處理，使辨識成功率超過 90%

