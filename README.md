# Chrome Gemini AI 一键解锁工具 🚀

> 让 Chrome 浏览器解锁隐藏的 Gemini AI 功能，包括侧边栏智能助手、浏览器控制等强大特性！

---

## ✨ 能解锁什么功能？

使用本工具后，你的 Chrome 将获得以下 AI 功能：

1. **Gemini 侧边栏** 📱  
   在浏览器右侧随时唤起 AI 助手，无需离开当前页面

2. **智能浏览器控制** 🎯  
   对 Gemini 说 "帮我总结这个网页" 或 "在输入框帮我写点东西"，AI 会自动操作浏览器

3. **AI 辅助写作** ✍️  
   在任何网页输入框右键，选择 "Help Me Write" 让 AI 帮你写内容

4. **智能历史搜索** 🔍  
   用自然语言搜索你的浏览历史，比如 "上周看过的关于 AI 的文章"

---

## 🚀 快速开始（3 步搞定）

### 📱 **如果你用的是 Windows 电脑**

1. **下载文件**  
   点击右上角绿色 `Code` 按钮 → `Download ZIP`，解压后打开 `win` 文件夹

2. **一键运行**  
   双击 `Gemini-Setup-Win.bat`，等待脚本自动完成

3. **重启浏览器**  
   关闭 Chrome 后重新打开，**记得要用美国 VPN**

---

### 🍎 **如果你用的是 Mac 电脑**

1. **下载文件**  
   点击右上角绿色 `Code` 按钮 → `Download ZIP`，解压后打开 `mac` 文件夹

2. **赋予执行权限**  
   右键点击 `Gemini-Setup-Mac-v6.2.command` → `打开方式` → `终端`  
   （或在终端输入 `chmod +x Gemini-Setup-Mac-v6.2.command`）

3. **一键运行**  
   双击运行脚本，按照提示操作完成后，**用美国 VPN 重启 Chrome**

---

## ⚠️ 重要提醒（必看！）

即使运行了脚本，你还需要满足这些条件才能成功：

### 1️⃣ 必须用美国 VPN
- Gemini 功能只在美国地区开放
- 确保 VPN 连接到**美国节点**（推荐洛杉矶、纽约等）
- 建议用稳定、速度快的 VPN，避免断连

### 2️⃣ Google 账号语言设置为英文
1. 访问 [Google 账号设置](https://myaccount.google.com/personal-info)
2. 找到 **Language（语言）** 选项
3. 添加 **English (United States)** 并**拖到最上面**
4. 刷新页面确认生效

### 3️⃣ 如果界面还是中文
如果 Chrome 界面显示中文，用这个方法强制启动英文版：

**Windows**：  
```
"C:\Program Files\Google\Chrome\Application\chrome.exe" --lang=en-US
```

**Mac**：  
```
open -a "Google Chrome" --args --lang=en-US
```

---

## 🎯 如何验证成功？

运行脚本并重启 Chrome 后，检查以下几点：

1. **侧边栏出现 Gemini 图标**  
   浏览器右上角应该有一个 Gemini 的图标（星星状）

2. **设置里有 AI 选项**  
   打开 `chrome://settings/ai`，应该能看到 Gemini 相关开关

3. **触发浏览器控制功能**  
   在侧边栏对 Gemini 说：  
   - "Summarize this page" (总结这个网页)  
   - "Type help in the textbox" (在输入框帮我输入)  
   
   如果弹出**允许 Gemini 控制浏览器**的提示，说明成功了！🎉

---

## ❓ 常见问题

**Q: 为什么我运行后还是没有 Gemini？**  
A: 请依次检查：  
   1. VPN 是否连接到美国  
   2. Google 账号语言是否设为英文  
   3. 是否重启了 Chrome（完全关闭再打开）  
   4. Chrome 版本是否是最新的（建议 120+）

**Q: 重启电脑后功能消失了？**  
A: 
   - Windows 用户：重新运行一次脚本即可
   - Mac 用户：脚本已经设置了系统持久化，理论上不会消失。如果消失，请确认 VPN 稳定连接美国

**Q: 这个工具安全吗？**  
A: 
   - 完全安全！本工具仅修改 Chrome 的公开配置文件，不涉及任何破解或侵权
   - 所有代码开源，可以自行审查
   - 本质上是告诉 Chrome "我在美国"，让它自动开启功能

**Q: 这个工具收费吗？**  
A: 完全免费！本项目开源供学习研究使用

---

## 📖 工作原理（技术向）

> 小白用户可以跳过这部分

本工具通过修改 Chrome 配置文件中的以下字段来实现功能解锁：

1. 动态读取 Chrome 版本号
2. 设置 `variations_country = "us"`（告诉 Chrome 用户在美国）
3. 递归设置 `is_glic_eligible = true`（开启 Gemini 资格）
4. 强制语言为 `en-US`（避免中文环境锁定）
5. macOS 额外设置系统级策略防止重置

---

## 📄 免责声明

本工具仅供学习研究使用，通过修改公开配置项实现功能开启，不涉及任何破解及侵权行为。使用本工具产生的任何后果由使用者自行承担。

---

## 🙏 鸣谢

感谢开源社区对 Chrome AI 功能解锁方案的探索与贡献。

---

**作者**: [Kenny-BBDog](https://github.com/Kenny-BBDog)  
**最后更新**: 2026-02-01 (v6.2)
