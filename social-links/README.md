# Lupin Notion 社群連結小工具

供 Lupin 的 Notion 個人頁嵌入使用，以四顆圓形圖示提供官網、Facebook、Threads 與 Email 入口。

## 架構決定

- 使用單一原生 HTML 檔，CSS 與 SVG 圖示全部內嵌。
- 外層保持透明，只顯示白底藍圖示的圓形按鈕。
- 不使用 React、套件管理器或外部圖示 CDN，降低載入與維護成本。
- 由 `notion-widgets` 儲存庫的 GitHub Pages 發布，再用 Notion 的 `/embed` 嵌入公開網址。

Facebook 與 Threads 商標路徑取自 [Simple Icons](https://simpleicons.org/)；官網與 Email 使用同尺寸的內嵌 SVG。所有圖示都直接放在 HTML 內，不會因外部 CDN 中斷而消失。

## 嵌入 Notion

在 Notion 輸入 `/embed`，貼上 `https://lupinart.github.io/notion-widgets/social-links/` 並調整區塊高度即可。

## 本機驗證

依工作區規則，網站測試只在 `/private/tmp/codex-builds/` 的暫存副本執行。

