# Gemini in Chrome Enabler 🚀

[English](#english) | [中文](#中文)

---

## 中文

### ⚡ 三步搞定

```bash
# 1. 克隆项目
git clone https://github.com/Kenny-BBDog/gemini-in-chrome-enabler.git
cd gemini-in-chrome-enabler

# 2. 安装依赖
pip install psutil

# 3. 运行（会自动关闭 Chrome，修复配置，然后重启）
python enable_gemini.py --fix
```

> 💡 修复后需要**手动重启 Chrome 一次**，然后就能看到 Gemini 图标了！

---

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
| 🚩 Chrome Flags | ✅ | **新增** 自动启用 9 个 GLIC 实验功能 |
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

---

### ❌ 修复后仍无法使用？故障排查

#### 1️⃣ 先检查账号资格（最重要！）

在运行本工具之前，请先确认你的 Google 账号有 Gemini 资格：

1. 打开 Chrome，访问 `chrome://sync-internals/`
2. 在左侧找到 **Priority Preferences** → **sync.glic_rollout_eligibility**
3. 查看右侧 JSON 中的 `"value"` 字段

| value | 含义 |
|-------|-----|
| `true` | ✅ 账号有资格，可以继续 |
| `false` | ❌ 账号无资格，无法使用 Gemini |

> 💡 如果是 `false`，可以尝试登录其他 Google 账号再检查

#### 2️⃣ 网络环境要求

| 网络类型 | 可用性 | 说明 |
|---------|-------|------|
| 🏠 住宅 IP (美国) | ✅ 最佳 | 推荐使用 |
| 🏢 商业宽带 | ⚠️ 可能 | 部分可用 |
| 🖥️ 机房 IP / VPS | ❌ 大概率不行 | Google 会检测并限制 |
| 📱 手机热点 | ⚠️ 可能 | 取决于运营商 |

**网络自检方法**：
- 访问 [ipinfo.io](https://ipinfo.io)，查看 `org` 字段
- 如果显示 "hosting"、"datacenter" 等关键词，说明是机房 IP，建议更换节点

#### 3️⃣ 其他常见问题

| 问题 | 解决方案 |
|------|---------|
| 地址栏没有 Gemini 图标 | 确保重启 Chrome **两次** |
| Chrome 界面仍是中文 | 运行 `--fix`，并手动检查 设置 → 语言 |
| 访问 google.com 跳转到 google.com.hk | 检查 VPN 节点是否真的在美国 |
| 显示 "Gemini is not available" | 账号无资格或网络环境问题 |

---

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

### ⚡ Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/Kenny-BBDog/gemini-in-chrome-enabler.git
cd gemini-in-chrome-enabler

# 2. Install dependency
pip install psutil

# 3. Run (will auto-close Chrome, fix config, then restart)
python enable_gemini.py --fix
```

> 💡 After fixing, **restart Chrome once manually** to see the Gemini icon!

---

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
| 🚩 Chrome Flags | ✅ | **NEW** Auto-enable 9 GLIC experiment flags |
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

### ❌ Still Not Working? Troubleshooting

#### 1️⃣ Check Account Eligibility First (Most Important!)

Before running this tool, verify your Google account is eligible for Gemini:

1. Open Chrome, visit `chrome://sync-internals/`
2. Find **Priority Preferences** → **sync.glic_rollout_eligibility** in the left panel
3. Check the `"value"` field in the right JSON panel

| value | Meaning |
|-------|---------|
| `true` | ✅ Account eligible, proceed with the tool |
| `false` | ❌ Account not eligible, cannot use Gemini |

> 💡 If `false`, try logging into a different Google account

#### 2️⃣ Network Requirements

| Network Type | Availability | Notes |
|--------------|--------------|-------|
| 🏠 Residential IP (US) | ✅ Best | Recommended |
| 🏢 Business Broadband | ⚠️ Maybe | Partially works |
| 🖥️ Datacenter IP / VPS | ❌ Likely blocked | Google detects and restricts |
| 📱 Mobile Hotspot | ⚠️ Maybe | Depends on carrier |

**How to check your IP**:
- Visit [ipinfo.io](https://ipinfo.io), check the `org` field
- If it shows "hosting", "datacenter", etc., it's a datacenter IP - try a different node

#### 3️⃣ Common Issues

| Issue | Solution |
|-------|----------|
| No Gemini icon in address bar | Restart Chrome **twice** |
| Chrome UI still in non-English | Run `--fix`, manually check Settings → Language |
| google.com redirects to local domain | Check if VPN is actually in US |
| "Gemini is not available" | Account not eligible or network issue |

---

## ⚠️ Notes

- The script writes to your existing Chrome profile; back up `User Data` if you want a safety net.
- Run as the same OS user who owns the Chrome profile to ensure write access.
- VPN connection to US is required to use Gemini.
- Not affiliated with Google—use at your own risk.

## License

MIT License - 随便用，记得给个 Star ⭐

**Made with ❤️ by Kenny-BBDog**
