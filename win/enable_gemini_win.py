import os
import json
import winreg
import time
from pathlib import Path

# =============================================================================
#  Chrome Gemini AI 解锁 (v6.2 精准 lcandy2 版)
#  动态版本检测 + 纯净逻辑
# =============================================================================

TARGET_COUNTRY = "us"
TARGET_LOCALE = "en-US"

def get_chrome_version_from_local_state(data):
    """从 Local State 读取 Chrome 版本 (与 lcandy2 一致)"""
    # 尝试从现有的 variations_permanent_consistency_country 获取版本
    vpcc = data.get('variations_permanent_consistency_country')
    if vpcc and isinstance(vpcc, list) and len(vpcc) >= 1:
        version = vpcc[0]
        if version and isinstance(version, str) and '.' in version:
            return version
    
    # 备用：尝试从 user_experience_metrics 获取
    uem = data.get('user_experience_metrics', {})
    if 'stability' in uem:
        stats = uem.get('stability', {})
        if 'stats_version' in stats:
            return stats['stats_version']
    
    # 最终备用：使用默认版本
    return "144.0.7559.110"

def cleanup_registry():
    """清理注册表策略"""
    print("🧹 [1/4] 清理注册表策略...")
    paths = [r"SOFTWARE\Policies\Google\Chrome"]
    for path in paths:
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, path, 0, winreg.KEY_ALL_ACCESS)
            while True:
                try:
                    name = winreg.EnumValue(key, 0)[0]
                    winreg.DeleteValue(key, name)
                    print(f"    ➜ 已删除: {name}")
                except OSError:
                    break
            winreg.CloseKey(key)
        except: pass
    print("    ✅ 完成")

def patch_lcandy2_exact(path):
    """精准对齐 lcandy2 逻辑"""
    print(f"\n💉 [2/4] 执行 lcandy2 精准补丁...")
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 1. 动态获取 Chrome 版本 (lcandy2 方式)
        version = get_chrome_version_from_local_state(data)
        print(f"    ➜ 检测到 Chrome 版本: {version}")
        
        # 2. 设置国家 (lcandy2 核心)
        data['variations_country'] = TARGET_COUNTRY
        print(f"    ➜ variations_country = \"{TARGET_COUNTRY}\"")
        
        # 3. 版本+国家一致性 (lcandy2 核心)
        data['variations_permanent_consistency_country'] = [version, TARGET_COUNTRY]
        print(f"    ➜ variations_permanent_consistency_country = [\"{version}\", \"{TARGET_COUNTRY}\"]")
        
        # 4. 强制语言 (解决中文问题)
        if 'intl' not in data: data['intl'] = {}
        data['intl']['app_locale'] = TARGET_LOCALE
        print(f"    ➜ intl.app_locale = \"{TARGET_LOCALE}\"")
        
        # 5. 递归开启资格 (lcandy2 核心)
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
        print(f"    ➜ 已递归设置 {count[0]} 处 is_glic_eligible = true")

        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, separators=(',', ':'))
        print("    ✅ Local State 补丁完成")
        return True
    except Exception as e:
        print(f"    ❌ 失败: {e}")
        return False

def patch_preferences(path):
    """修复 Preferences 语言"""
    print(f"\n💉 [3/4] 修复 Preferences 语言...")
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if 'intl' not in data: data['intl'] = {}
        data['intl']['selected_languages'] = "en-US,en"
        data['intl']['accept_languages'] = "en-US,en"
        print(f"    ➜ selected_languages = \"en-US,en\"")

        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, separators=(',', ':'))
        print("    ✅ 完成")
        return True
    except Exception as e:
        print(f"    ❌ 失败: {e}")
        return False

def main():
    print("=" * 60)
    print("   Gemini 解锁 (v6.1 精准 lcandy2 版)")
    print("   动态版本检测 + 纯净逻辑")
    print("=" * 60)
    
    chrome_data = Path(os.getenv('LOCALAPPDATA')) / "Google/Chrome/User Data"
    local_state = chrome_data / "Local State"
    preferences = chrome_data / "Default" / "Preferences"
    
    print("\n🚀 正在关闭 Chrome...")
    os.system("taskkill /F /IM chrome.exe /T >nul 2>&1")
    time.sleep(1)
    
    cleanup_registry()
    
    if local_state.exists():
        patch_lcandy2_exact(local_state)
    else:
        print("    ⚠️ Local State 不存在，请先启动一次 Chrome")
    
    if preferences.exists():
        patch_preferences(preferences)
    
    print("\n" + "=" * 60)
    print("🎉 [4/4] 补丁完成！")
    print("=" * 60)
    print("\n💡 下一步:")
    print("    1. 开启美国 VPN")
    print("    2. 正常启动 Chrome")
    print("    3. 登录美区 Google 账号")
    print("    4. Chrome 会自动从服务器获取 Gemini 配置")
    print("\n⚠️ 如果界面仍是中文:")
    print("    chrome.exe --lang=en-US")
    
    os.system("pause")

if __name__ == "__main__":
    main()
