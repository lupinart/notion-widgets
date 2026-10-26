# Notion Widgets

Lupin 的 Notion 專用 HTML 小工具集合。每個小工具放在獨立資料夾，可用 GitHub Pages 網址直接嵌入 Notion。

## 小工具

| 名稱 | 資料夾 | Pages 網址 |
|---|---|---|
| 社群連結 | `social-links/` | `https://lupinart.github.io/notion-widgets/social-links/` |

## 專案原則

- 使用原生 HTML、CSS、JavaScript；需求真的需要時才加入工具或套件。
- 每個小工具互相獨立，避免共用樣式修改後一起壞掉。
- 預設透明背景，適合放進 Notion iframe。
- 不自行增加外框、標籤、背景或裝飾；只實作已確認的需求。
- 不放 API 金鑰、密碼或其他私人資料。

## 結構

```text
notion-widgets/
├── README.md
└── social-links/
    ├── index.html
    ├── DESIGN.md
    └── tests/
```

## 維護方式

iCloud 內的 `100_Todo/projects/notion-widgets/` 是權威原始碼。測試與 GitHub 發布只在 `/private/tmp/codex-builds/` 的暫存副本執行，不在 iCloud 內建立巢狀 Git 儲存庫或衍生檔。

