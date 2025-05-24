# F1 Downloader

🎯 **F1 Downloader** 是一个图形界面的 Python 应用程序，用于自动查询、筛选和下载 F1 官方网站发布的最新赛事文件（如违规通知、传唤裁决等）。

> 📦 当前版本：`beta 1.0.0`

---

## ✨ 功能特色

- ✅ 自动加载 F1 Grand Prix 比赛列表（基于 FIA 官网）
- 🔍 支持关键词筛选下载文件（例如 `Infringement`、`Summons`、`Decision`）
- 📅 文件标题中自动提取并转换时间为北京时间
- 📥 文件下载带实时进度条反馈
- 📁 支持打开本地下载目录 & 管理已下载文件
- 📌 文件已存在时不重复下载，自动提示并打开

---

## 🖥️ 使用方式

### ✅ Windows 用户（已打包 .exe）

1. 下载 [`main.exe`](https://github.com/yourname/f1-downloader/releases)（见发布页）
2. 解压至任意目录并双击运行
3. 选择比赛 ➜ 输入关键词或点击快捷按钮 ➜ 点击文件自动下载并打开

---

### 🐍 Python 用户（源码运行）

1. 克隆本项目：
```bash
git clone https://github.com/yourname/f1-downloader.git
cd f1-downloader
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 手动下载 EdgeDriver：

- 打开 Edge 浏览器 → 输入 `edge://settings/help` 查看版本号
- 访问 [EdgeDriver 下载页面](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/)
- 下载与你版本匹配的 `msedgedriver.exe`
- 解压后，将路径写入 `grab_gp_list.py` 的：
```python
driver_path = r"D:\your\path\to\msedgedriver.exe"
```

4. 运行主程序：
```bash
python main.py
```

---

## 📁 项目结构说明

```
f1_downloader/
├── main.py                  # 主图形界面程序
├── utils.py                 # 工具函数模块（爬虫、下载、保存）
├── grab_gp_list.py          # Grand Prix 赛事列表抓取脚本（需要 EdgeDriver）
├── grand_prix_list.json     # 默认赛事列表映射表
├── README.md                # 项目说明文档
├── requirements.txt         # 所需依赖
└── .gitignore               # 忽略缓存和打包内容
```

---

## 📌 快捷关键词说明

| 中文按钮 | 英文关键词（用于搜索） |
|----------|-------------------------|
| 违规通知 | Infringement            |
| 官方裁决 | Decision                |
| 传唤通知 | Summons                 |

---

## 📦 已知问题 / Todo

- [ ] 添加多赛季支持（2023 / 2024 / 2025）
- [ ] 支持文档类型筛选（PDF / DOC）
- [ ] 支持结果排序方式切换（时间优先 / 编号优先）
- [ ] 下载完成自动提示音或托盘提示

---

## 🏁 发布日志

### 📌 `beta 1.0.0` - 初始发布
- 基于 Tkinter 和 requests 构建图形查询器
- 支持关键词搜索与本地分类保存
- 提供 EXE 版本，无需安装 Python 即可运行

---

## 📃 License

MIT License © 2025 MercyNaima
