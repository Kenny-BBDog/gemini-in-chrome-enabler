#!/bin/bash
# =============================================================================
#  Gemini in Chrome Enabler - macOS v6.2 (精准 lcandy2 版)
#  动态版本检测 + 纯净逻辑 + macOS defaults 持久化
# =============================================================================

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m'

# Chrome 配置路径
CHROME_STATE=~/Library/Application\ Support/Google/Chrome/Local\ State
CHROME_PREFS=~/Library/Application\ Support/Google/Chrome/Default/Preferences

clear
echo ""
echo -e "${MAGENTA}╔═══════════════════════════════════════════════════════════╗${NC}"
echo -e "${MAGENTA}║     Gemini in Chrome Enabler - macOS v6.2                 ║${NC}"
echo -e "${MAGENTA}║         精准 lcandy2 版 + macOS defaults 持久化           ║${NC}"
echo -e "${MAGENTA}╚═══════════════════════════════════════════════════════════╝${NC}"
echo ""

# =============================================================================
# 步骤 1: 环境检测
# =============================================================================
echo -e "${CYAN}┌─────────────────────────────────────────────────────────────┐${NC}"
echo -e "${CYAN}│  [1/5] 环境检测                                             │${NC}"
echo -e "${CYAN}└─────────────────────────────────────────────────────────────┘${NC}"
echo ""

# Chrome 安装检测
if [ -d "/Applications/Google Chrome.app" ]; then
    CHROME_VER=$(/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version 2>/dev/null | awk '{print $3}' || echo "未知")
    echo -e "  ${GREEN}✅ Chrome 已安装: $CHROME_VER${NC}"
else
    echo -e "  ${RED}❌ 未检测到 Chrome，请先安装 Google Chrome${NC}"
    read -p "按 Enter 键退出... " -r
    exit 1
fi

# Local State 文件检测
if [ -f "$CHROME_STATE" ]; then
    echo -e "  ${GREEN}✅ Chrome 配置文件存在${NC}"
else
    echo -e "  ${RED}❌ Chrome 配置文件不存在，请先启动一次 Chrome${NC}"
    read -p "按 Enter 键退出... " -r
    exit 1
fi

echo ""
read -p "环境检测完成，按 Enter 键继续... " -r
echo ""

# =============================================================================
# 步骤 2: 关闭 Chrome
# =============================================================================
echo -e "${CYAN}┌─────────────────────────────────────────────────────────────┐${NC}"
echo -e "${CYAN}│  [2/5] 关闭 Chrome                                          │${NC}"
echo -e "${CYAN}└─────────────────────────────────────────────────────────────┘${NC}"
echo ""

check_chrome() {
    pgrep -x "Google Chrome" > /dev/null 2>&1
}

if check_chrome; then
    echo -e "  ${YELLOW}⚠️  检测到 Chrome 正在运行${NC}"
    echo ""
    echo -e "  ${WHITE}请手动关闭 Chrome (Cmd+Q 或点击菜单 > 退出)${NC}"
    echo ""
    read -p "关闭后按 Enter 键继续... " -r
    
    if check_chrome; then
        echo -e "  ${YELLOW}尝试自动关闭 Chrome...${NC}"
        osascript -e 'quit app "Google Chrome"' 2>/dev/null
        sleep 2
        
        if check_chrome; then
            echo -e "  ${RED}❌ Chrome 仍在运行，请手动关闭后重新运行脚本${NC}"
            read -p "按 Enter 键退出... " -r
            exit 1
        fi
    fi
fi

echo -e "  ${GREEN}✅ Chrome 已关闭${NC}"
echo ""

# =============================================================================
# 步骤 3: 备份配置
# =============================================================================
echo -e "${CYAN}┌─────────────────────────────────────────────────────────────┐${NC}"
echo -e "${CYAN}│  [3/5] 备份配置文件                                         │${NC}"
echo -e "${CYAN}└─────────────────────────────────────────────────────────────┘${NC}"
echo ""

BACKUP_TIME=$(date +%Y%m%d_%H%M%S)
cp "$CHROME_STATE" "$CHROME_STATE.backup.$BACKUP_TIME"
echo -e "  ${GREEN}✅ 已备份: Local State.backup.$BACKUP_TIME${NC}"
echo ""

# =============================================================================
# 步骤 4: 精准 lcandy2 补丁 (核心)
# =============================================================================
echo -e "${CYAN}┌─────────────────────────────────────────────────────────────┐${NC}"
echo -e "${CYAN}│  [4/5] 执行精准 lcandy2 补丁                                │${NC}"
echo -e "${CYAN}└─────────────────────────────────────────────────────────────┘${NC}"
echo ""

# 使用 Python 执行精准补丁 (与 Windows v6.1 完全一致的逻辑)
python3 << 'PYTHON_SCRIPT'
import json
import os

CHROME_STATE = os.path.expanduser("~/Library/Application Support/Google/Chrome/Local State")
CHROME_PREFS = os.path.expanduser("~/Library/Application Support/Google/Chrome/Default/Preferences")

def get_chrome_version(data):
    """从 Local State 动态获取 Chrome 版本"""
    vpcc = data.get('variations_permanent_consistency_country')
    if vpcc and isinstance(vpcc, list) and len(vpcc) >= 1:
        version = vpcc[0]
        if version and isinstance(version, str) and '.' in version:
            return version
    return "144.0.7559.110"  # 备用

def patch_local_state():
    """精准 lcandy2 逻辑"""
    try:
        with open(CHROME_STATE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 1. 动态获取版本
        version = get_chrome_version(data)
        print(f"  ➜ 检测到 Chrome 版本: {version}")
        
        # 2. 设置国家
        data['variations_country'] = "us"
        print('  ➜ variations_country = "us"')
        
        # 3. 版本+国家一致性
        data['variations_permanent_consistency_country'] = [version, "us"]
        print(f'  ➜ variations_permanent_consistency_country = ["{version}", "us"]')
        
        # 4. 强制语言
        if 'intl' not in data: data['intl'] = {}
        data['intl']['app_locale'] = "en-US"
        print('  ➜ intl.app_locale = "en-US"')
        
        # 5. 递归开启资格
        count = [0]
        def fix_eligible(obj):
            if isinstance(obj, dict):
                for k, v in obj.items():
                    if k == 'is_glic_eligible':
                        obj[k] = True
                        count[0] += 1
                    else:
                        fix_eligible(v)
            elif isinstance(obj, list):
                for i in obj:
                    fix_eligible(i)
        fix_eligible(data)
        print(f"  ➜ 已递归设置 {count[0]} 处 is_glic_eligible = true")
        
        with open(CHROME_STATE, 'w', encoding='utf-8') as f:
            json.dump(data, f, separators=(',', ':'))
        print("  ✅ Local State 补丁完成")
        return True
    except Exception as e:
        print(f"  ❌ 失败: {e}")
        return False

def patch_preferences():
    """修复 Preferences 语言"""
    try:
        if not os.path.exists(CHROME_PREFS):
            return
        with open(CHROME_PREFS, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if 'intl' not in data: data['intl'] = {}
        data['intl']['selected_languages'] = "en-US,en"
        data['intl']['accept_languages'] = "en-US,en"
        
        with open(CHROME_PREFS, 'w', encoding='utf-8') as f:
            json.dump(data, f, separators=(',', ':'))
        print("  ✅ Preferences 语言修复完成")
    except Exception as e:
        print(f"  ⚠️  Preferences 修复失败: {e}")

patch_local_state()
patch_preferences()
PYTHON_SCRIPT

echo ""

# =============================================================================
# 步骤 4.5: macOS defaults 持久化设置
# =============================================================================
echo -e "${BLUE}  [4.5] 设置 macOS 系统级持久化...${NC}"
defaults write com.google.Chrome VariationsRestrictParameter -string "us" 2>/dev/null
echo -e "  ${GREEN}      ✅ VariationsRestrictParameter -> us${NC}"
defaults write com.google.Chrome AppleLanguages '("en-US")' 2>/dev/null
echo -e "  ${GREEN}      ✅ AppleLanguages -> en-US${NC}"
echo ""

# =============================================================================
# 步骤 5: 验证 & 完成
# =============================================================================
echo -e "${CYAN}┌─────────────────────────────────────────────────────────────┐${NC}"
echo -e "${CYAN}│  [5/5] 验证结果                                             │${NC}"
echo -e "${CYAN}└─────────────────────────────────────────────────────────────┘${NC}"
echo ""

# 检查 variations_country
if grep -q '"variations_country":"us"' "$CHROME_STATE"; then
    echo -e "  ${GREEN}✅ variations_country: us${NC}"
else
    echo -e "  ${YELLOW}⚠️  variations_country: 验证失败${NC}"
fi

# 检查 is_glic_eligible
if grep -q '"is_glic_eligible":true' "$CHROME_STATE"; then
    echo -e "  ${GREEN}✅ is_glic_eligible: true${NC}"
else
    echo -e "  ${YELLOW}⚠️  is_glic_eligible: 未找到${NC}"
fi

echo ""

# =============================================================================
# 结果总结
# =============================================================================
echo -e "${MAGENTA}╔═══════════════════════════════════════════════════════════╗${NC}"
echo -e "${MAGENTA}║                    ${GREEN}🎉 v6.2 补丁完成！${MAGENTA}                       ║${NC}"
echo -e "${MAGENTA}╚═══════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}  📋 下一步:${NC}"
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "  ${WHITE}1. 开启 VPN 并连接到美国节点${NC}"
echo -e "  ${WHITE}2. 正常启动 Chrome${NC}"
echo -e "  ${WHITE}3. 登录美区 Google 账号${NC}"
echo -e "  ${WHITE}4. Chrome 会自动从服务器获取 Gemini 配置${NC}"
echo ""
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "是否现在启动 Chrome? (y/n)"
read -p "> " -r OPEN_CHROME
if [[ "$OPEN_CHROME" =~ ^[Yy]$ ]]; then
    open -a "Google Chrome"
    echo -e "${GREEN}Chrome 已启动！${NC}"
fi

echo ""
echo -e "${GREEN}感谢使用 Gemini in Chrome Enabler v6.2!${NC}"
echo ""
read -p "按 Enter 键退出... " -r
