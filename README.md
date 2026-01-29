# Gemini in Chrome Enabler 🚀

[English](#english) | [中文](#中文)

---

## 中文

### 📥 下载与使用

#### 1. 闲鱼版 (作者赚零花钱工具，请优先支持) 📦
如果您是通过购买得到的此工具，或者希望最简单的使用体验：
- **下载**：[releases/GeminiEnabler.exe](https://github.com/Kenny-BBDog/gemini-in-chrome-enabler/raw/main/releases/GeminiEnabler.exe)
- **使用**：一键双击运行。首次运行会显示**设备 ID** -> 发给卖家获取**激活码** -> 输入激活即可使用。
- **说明**：此版本专为小白用户设计，集成了所有环境，无需安装 Python。

#### 2. 开发者版 (源码运行) 🛠️
如果您是技术用户，可以直接运行 Python 脚本，**此方式无需激活码，完全免费开源**。

**运行步骤：**
1. **安装环境** (必须)：
   ```bash
   pip install psutil
   ```
   *作用：允许脚本自动关闭并重启 Chrome 浏览器。*

2. **执行脚本** (三选一)：
   - **推荐方案**：自动检测 + 自动修复 + 自动重启 Chrome
     ```bash
     python enable_gemini.py --fix
     ```
   - **手动方案**：修复配置，但不自动重启 Chrome（需要您手动关闭并打开 Chrome 两次）
     ```bash
     python enable_gemini.py --fix --no-restart
     ```
   - **仅检查**：只查看当前配置状态，不修改任何文件
     ```bash
     python enable_gemini.py
     ```

---

### 功能介绍

一键检测和启用 Chrome 的 AI 功能：
- ✨ **Gemini in Chrome** - 在浏览器地址栏直接开启 AI 聊天
- 🔍 **AI 历史搜索** - 使用自然语言搜索浏览记录
- 🛠️ **DevTools AI** - 开发者工具中的 AI 辅助功能

### 检测项目说明

| 检测项 | 自动修复 | 详细说明 |
|--------|-----------|------|
| 👤 账号资格 | ✅ | **自动检测** 您的 Google 账号是否在灰度测试名单中 |
| 🌍 国家配置 | ✅ | 修改 `variations_country` 为 `us` (Gemini 必须) |
| 🤖 GLIC 设置 | ✅ | 开启 `is_glic_eligible` 核心开关 |
| 🚩 实验项 (Flags) | ✅ | 自动启用 9 个相关的 `chrome://flags` 实验功能 |
| 🌐 界面语言 | ✅ | 将 Chrome 界面设为 English (US) |
| 📝 偏好语言 | ✅ | 将首选搜索语言设为英文 |
| 👤 账号语言 | ❌ | **需手动** 将 Google 账号语言设为英文 (见下文) |

---

### ⚠️ 重要：必须手动完成的设置

脚本无法修改您的 Google 云端账号设置，请务必执行：
1. 访问 [Google 账号语言设置](https://myaccount.google.com/personal-info)
2. 将 **Language** 修改为 **English (United States)**
3. 确保您的 VPN 节点位于**美国**且不是机房 IP。

---

### ❌ 故障排查

#### 1. 账号资格显示 False？
这意味着该 Google 账号目前不在灰度范围内。解决方案：换一个 Google 账号登录 Chrome 再次尝试。

#### 2. 地址栏没出现 Gemini 图标？
脚本运行成功后，请确保**重启 Chrome 两次**。有时第一次启动会加载配置，第二次才会生效。

---

### 原理说明 (开发者参考)
脚本会安全地修改路径下的 `Local State` 和 `Preferences` 文件，并在修改前自动创建备份。涉及的关键键值包括 `variations_country`, `is_glic_eligible` 以及 `browser.enabled_labs_experiments`。

---

**Made with ❤️ by [Kenny-BBDog](https://github.com/Kenny-BBDog)**

> 🔓 **随便用，如果对您有帮助，记得给个 Star ⭐ 鼓励一下！**

---

## English

### 📥 Download & Usage

#### 1. Xianyu Edition (Portable Tool) 📦
If you bought this tool or want a zero-setup experience:
- **Download**: [releases/GeminiEnabler.exe](https://github.com/Kenny-BBDog/gemini-in-chrome-enabler/raw/main/releases/GeminiEnabler.exe)
- **Usage**: Portable EXE. Get **Device ID** -> Enter **Activation Code** -> Enjoy.

#### 2. Developer Edition (Source Code) 🛠️
For developers who wish to run from source. **No activation required, 100% free and open source.**

**Run Steps:**
1. **Prerequisite** (Required):
   ```bash
   pip install psutil
   ```
   *Purpose: Enables the script to safely close and restart Chrome.*

2. **Execute** (Choose one):
   - **Recommended**: Auto Detect + Fix + Restart
     ```bash
     python enable_gemini.py --fix
     ```
   - **Manual**: Fix config but do NOT restart automatically
     ```bash
     python enable_gemini.py --fix --no-restart
     ```
   - **Check Only**: Just view the report
     ```bash
     python enable_gemini.py
     ```

---

### Features
Enable Chrome's AI suite in one click:
- ✨ **Gemini in Chrome** - AI assistant directly in address bar
- 🔍 **AI Search** - Search history using natural language
- 🛠️ **DevTools AI** - AI capabilities in developer tools

### What It Checks

| Item | Auto-fix | Description |
|------|----------|-------------|
| 👤 Eligibility | ✅ | **Auto-detect** if your account is in Google's rollout pool |
| 🌍 Country | ✅ | Set `variations_country` to `us` |
| 🤖 GLIC | ✅ | Enable `is_glic_eligible` core switch |
| 🚩 Flags | ✅ | Enable 9 experimental flags in `chrome://flags` |
| 🌐 UI Locale | ✅ | Set Chrome UI to English (US) |
| 👤 Account Lang | ❌ | **Manual Action Required** (See below) |

---

### ⚠️ Critical Manual Setup
The script cannot modify your cloud-side Google settings. You MUST:
1. Go to [Google Account Language Settings](https://myaccount.google.com/personal-info)
2. Set **Language** to **English (United States)**
3. Use a **US-based VPN** (Residential IP recommended).

---

### ❌ Troubleshooting

- **No Gemini icon?**: Restart Chrome **twice**.
- **Eligibility is False?**: Your account is not in the rollout pool. Try a different Google account.
- **Still redirected to local domain?**: Your VPN node might be flagged as a non-US or datacenter IP.

---

**Made with ❤️ by [Kenny-BBDog](https://github.com/Kenny-BBDog)**

> 🔓 **Free to use! If this tool helps you, please give it a Star ⭐!**

---
