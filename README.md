# Gemini in Chrome Enabler 🚀

[English](#english) | [中文](#中文)

---

## 中文

### 功能介绍

一键检测和启用 Chrome 的 AI 功能，包括：
- ✨ **Gemini in Chrome** - 在浏览器中直接使用 Gemini AI 助手
- 🔍 **AI 历史搜索** - 使用 AI 搜索浏览历史
- 🛠️ **DevTools AI** - 开发者工具中的 AI 功能

### 检测项目

| 检测项 | 可自动修复 | 说明 |
|--------|-----------|------|
| 🌍 国家/地区配置 | ✅ | `variations_country` 等配置项 |
| 🤖 GLIC 配置 | ✅ | `is_glic_eligible` 启用 Gemini |
| 🌐 Chrome 语言 | ✅ | `app_locale` 设为英语(美国) |
| 📝 Profile 语言偏好 | ✅ | `accept_languages` 首选英语 |
| 🔄 自动关闭/重启 Chrome | ✅ | 需安装 psutil |
| 👤 Google 账号语言 | ❌ | 需手动设置 |

### 安装

**方式一：使用 uv (推荐)**
```bash
# 安装 uv
# Windows:
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
# macOS/Linux:
curl -LsSf https://astral.sh/uv/install.sh | sh

# 安装依赖并运行
uv sync
uv run enable_gemini.py --fix
```

**方式二：使用 pip**
```bash
pip install psutil
python enable_gemini.py --fix
```

### 使用方法

```bash
# 仅检测（查看当前配置状态）
python enable_gemini.py

# 检测 + 自动修复（会自动关闭并重启 Chrome）
python enable_gemini.py --fix

# 修复但不自动重启 Chrome
python enable_gemini.py --fix --no-restart
```

### 手动设置 Google 账号语言

> ⚠️ **重要**：Google 账号语言无法通过脚本修改，需要手动设置！

1. 访问 [Google 账号 - 个人信息](https://myaccount.google.com/personal-info)
2. 找到 **Language** 选项
3. 设置为 **English (United States)**

### 原理说明

本工具修改以下配置项：

| 配置项 | 作用 |
|--------|------|
| `variations_country` | Chrome 用于评估实验研究的国家代码 |
| `variations_permanent_consistency_country` | 永久一致性研究的国家代码 |
| `variations_safe_seed_*` | 安全种子的国家代码 |
| `is_glic_eligible` | Gemini Live in Chrome 资格标志 |
| `intl.app_locale` | Chrome 界面语言 |
| `intl.accept_languages` | 网页语言偏好 |

---

## English

### Features

One-click detection and enablement of Chrome AI features:
- ✨ **Gemini in Chrome** - Use Gemini AI assistant directly in browser
- 🔍 **AI-Powered History Search** - Search browsing history with AI
- 🛠️ **DevTools AI Innovations** - AI features in Developer Tools

### What It Checks

| Item | Auto-fixable | Description |
|------|-------------|-------------|
| 🌍 Country Config | ✅ | `variations_country` and related |
| 🤖 GLIC Config | ✅ | `is_glic_eligible` for Gemini |
| 🌐 Chrome Language | ✅ | `app_locale` set to en-US |
| 📝 Profile Language | ✅ | `accept_languages` prefers English |
| 🔄 Auto Chrome restart | ✅ | Requires psutil |
| 👤 Google Account Language | ❌ | Manual setup required |

### Installation

**Option 1: Using uv (recommended)**
```bash
# Install uv
# Windows:
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
# macOS/Linux:
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install deps and run
uv sync
uv run enable_gemini.py --fix
```

**Option 2: Using pip**
```bash
pip install psutil
python enable_gemini.py --fix
```

### Usage

```bash
# Check only (view current configuration)
python enable_gemini.py

# Check + Auto-fix (will auto close and restart Chrome)
python enable_gemini.py --fix

# Fix without auto-restarting Chrome
python enable_gemini.py --fix --no-restart
```

### Manual: Set Google Account Language

> ⚠️ **Important**: Google Account language cannot be modified by script!

1. Visit [Google Account - Personal Info](https://myaccount.google.com/personal-info)
2. Find **Language** option
3. Set to **English (United States)**

---

## ⚠️ Notes

- The script writes to your existing Chrome profile; back up `User Data` if you want a safety net.
- Run as the same OS user who owns the Chrome profile to ensure write access.
- VPN connection to US is required to use Gemini.
- Not affiliated with Google—use at your own risk.

## License

MIT License - 随便用，记得给个 Star ⭐

**Made with ❤️ by Kenny-BBDog**
