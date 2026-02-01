# Gemini in Chrome Enabler (v6.2 精准版) 🚀

一键解锁 Google Chrome 的 Gemini AI 功能及隐藏的 AI 创新功能（如：Glic 桌面悬浮助手、Google AI 历史搜索等）。

基于 `lcandy2` 核心原理实现，支持 Windows 和 macOS，动态版本检测，纯净逻辑。

---

## 🗺️ 目录结构

本项目现已分为 Windows 和 macOS 两个独立版本，操作极其简单：

- **`win/`**: Windows 用户专用。
  - `Gemini-Setup-Win.bat`: 一键运行入口。
  - `enable_gemini_win.py`: 核心解锁脚本 (v6.2)。
- **`mac/`**: macOS 用户专用。
  - `Gemini-Setup-Mac-v6.2.command`: 一键运行脚本，包含系统持久化设置。

---

## 🚀 快速开始

### 🍎 macOS 用户
1. **下载并复制**: 将 `mac/` 文件夹复制到本地。
2. **赋予权限**: 在终端运行 `chmod +x Gemini-Setup-Mac-v6.2.command`。
3. **一键修复**: 双击 **`Gemini-Setup-Mac-v6.2.command`**。
   - *脚本会自动修改 Local State 并注入 macOS 系统级策略，防止地区重置。*
4. **重启 Chrome**: 修复完成后正常启动浏览器。

### 💻 Windows 用户
1. **进入目录**: 打开 `win/` 文件夹。
2. **一键修复**: 双击 **`Gemini-Setup-Win.bat`**。
   - *脚本会自动清理注册表冲突，并应用 v6.2 动态版本补丁。*
3. **重启 Chrome**: 完成后按提示启动浏览器。

---

## 🛠️ 重要前提 (必看)

即使脚本修复了本地配置，您仍需满足以下条件才能成功开启 Gemini：

1. **VPN 环境**: 必须连接到 **美国 (USA)** 节点。
2. **Google 账号语言**:
   - 访问 [Google Account Settings](https://myaccount.google.com/personal-info)。
   - 将 **Language** 设置为 **English (United States)** 并置顶。
3. **英文启动 (如界面仍是中文)**:
   - 若 UI 还是中文，请尝试带参数启动：`chrome.exe --lang=en-US`

---

## ✨ 解锁功能列表

1. **Gemini Live in Chrome (Glic)**: 桌面全局悬浮的 AI 助手。
2. **Google AI 历史搜索**: 使用自然语言搜索您的历史记录。
3. **侧边栏 Gemini**: 在侧边栏随时调用 AI。
4. **浏览器控制 (Actuation)**: 在 Gemini 侧边栏输入 `Summarize this page` 或 `Type help in the textbox` 触发。

---

## 📋 版本更新 (v6.2)

- **精准 lcandy2 逻辑**: 动态读取 Chrome 内部版本号，解决版本不匹配导致的校验失败。
- **macOS 持久化**: 加回 `VariationsRestrictParameter` 系统策略，防止功能消失。
- **纯净模式**: 移除所有手动注入的干扰 Flags，完全依赖 Chrome 自动下发配置。

---

## 📄 免责声明
本工具仅供学习研究使用，通过修改公开配置项实现功能开启，不涉及任何破解及侵权行为。

---
**Author**: [Kenny-BBDog](https://github.com/Kenny-BBDog)
