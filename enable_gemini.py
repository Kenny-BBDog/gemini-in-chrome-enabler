#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gemini in Chrome Enabler - 一键启用 Chrome AI 功能
帮助中国区用户解锁 Gemini in Chrome、AI 历史搜索等功能
"""

import json
import os
import sys
import shutil
import platform
import subprocess
import hashlib
import uuid
from datetime import datetime
from pathlib import Path

# 尝试导入 psutil（可选依赖）
try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False


# ============== 配置常量 ==============

TARGET_COUNTRY = "us"  # 目标国家代码
TARGET_LOCALE = "en-US"  # 目标语言区域
SECRET_SALT = "GeminiEnabler_Safe_Salt_2026"  # 激活码盐值
LICENSE_FILE = ".license"

# 需要检查/修改的配置项
COUNTRY_KEYS = [
    "variations_country",
    "variations_safe_seed_permanent_consistency_country", 
    "variations_safe_seed_session_consistency_country",
]

# 需要特殊处理的配置项 (数组格式)
ARRAY_COUNTRY_KEY = "variations_permanent_consistency_country"

# GLIC 配置项
GLIC_KEY = "is_glic_eligible"

# GLIC 相关的 Chrome Flags (chrome://flags)
# 存储在 Local State 的 browser.enabled_labs_experiments 中
# 格式: "flag-name@1" 表示启用, "@2" 表示禁用
GLIC_FLAGS = [
    "glic",                      # 主开关：Gemini Live in Chrome
    "glic-actor",                # GLIC Actor
    "glic-actor-autofill",       # GLIC 自动填充
    "glic-pre-warming",          # GLIC 预热
    "glic-side-panel",           # GLIC 侧边栏
    "glic-z-order-changes",      # GLIC Z 顺序变化
    "glic-fre-pre-warming",      # GLIC FRE 预热
    "glic-button-pressed-state", # GLIC 按钮按下状态
    "glic-button-alt-label",     # GLIC 按钮替代标签
]


# ============== 颜色输出 ==============

class Color:
    """终端颜色代码"""
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    MAGENTA = "\033[95m"
    BOLD = "\033[1m"
    END = "\033[0m"


def colored(text: str, color: str) -> str:
    """为文本添加颜色"""
    if sys.platform == "win32":
        os.system("")  # 启用 Windows ANSI 支持
    return f"{color}{text}{Color.END}"


# ============== 激活与加密 (仅限打包版) ==============

def get_hwid() -> str:
    """获取硬件唯一标识符 (HWID)"""
    try:
        # 使用 MAC 地址作为简单标识
        node = uuid.getnode()
        return hashlib.sha256(str(node).encode()).hexdigest()[:16].upper()
    except Exception:
        return "UNKNOWN-DEVICE"


def verify_activation() -> bool:
    """校验激活状态"""
    # 如果不是打包运行，自动跳过验证
    if not getattr(sys, 'frozen', False):
        return True
    
    hwid = get_hwid()
    expected_code = hashlib.md5((hwid + SECRET_SALT).encode()).hexdigest().upper()
    
    # 检查本地许可证
    license_path = Path(sys.executable).parent / LICENSE_FILE
    if license_path.exists():
        try:
            with open(license_path, "r") as f:
                saved_code = f.read().strip()
                if saved_code == expected_code:
                    return True
        except Exception:
            pass

    # 提示输入激活码
    print(colored("\n🔑 程序未激活", Color.BOLD))
    print(f"   您的设备 ID: {colored(hwid, Color.CYAN)}")
    print(f"   提示: 懂技术的用户可以直接从 GitHub 拉取源码运行，无需激活码。")
    print(f"         本项目 GitHub: https://github.com/Kenny-BBDog/gemini-in-chrome-enabler")
    
    while True:
        code = input(f"\n   请输入激活码 (或输入 q 退出): ").strip().upper()
        if code == 'Q':
            sys.exit(0)
        
        if code == expected_code:
            # 保存许可证
            try:
                with open(license_path, "w") as f:
                    f.write(code)
                print(colored("   ✅ 激活成功！", Color.GREEN))
                return True
            except Exception as e:
                print(colored(f"   ⚠️ 激活成功但无法保存许可证文件: {e}", Color.YELLOW))
                return True
        else:
            print(colored("   ❌ 激活码错误，请重试或前往 GitHub 查看源码。", Color.RED))


# ============== Chrome 进程管理 ==============

def shutdown_chrome() -> set:
    """
    关闭所有 Chrome 进程
    返回被关闭的 Chrome 可执行文件路径集合
    """
    if not HAS_PSUTIL:
        return set()
    
    terminated_chromes = set()
    
    for process in psutil.process_iter(['name', 'exe']):
        try:
            proc_name = process.info['name'] or ''
            
            # 根据操作系统判断 Chrome 进程
            if sys.platform == 'darwin':
                if not proc_name.startswith('Google Chrome'):
                    continue
            elif sys.platform == 'win32':
                if proc_name.lower() != 'chrome.exe':
                    continue
            else:  # Linux
                if os.path.splitext(proc_name)[0] != 'chrome':
                    continue
            
            if not process.is_running():
                continue
            
            # 只关闭顶层进程（没有同名父进程的）
            parent = process.parent()
            if parent is not None:
                parent_name = parent.name() if parent else ''
                if parent_name == proc_name:
                    continue
            
            exe_path = process.info['exe']
            process.kill()
            if exe_path:
                terminated_chromes.add(exe_path)
                
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    
    return terminated_chromes


def restart_chrome(chrome_paths: set):
    """重启 Chrome 浏览器"""
    for chrome_path in chrome_paths:
        try:
            if sys.platform == 'win32':
                subprocess.Popen([chrome_path], 
                               stderr=subprocess.DEVNULL, 
                               stdout=subprocess.DEVNULL,
                               creationflags=subprocess.DETACHED_PROCESS)
            else:
                subprocess.Popen([chrome_path], 
                               stderr=subprocess.DEVNULL, 
                               stdout=subprocess.DEVNULL,
                               start_new_session=True)
        except Exception:
            pass


# ============== Chrome 路径检测 ==============

def get_chrome_user_data_paths() -> list[Path]:
    """
    获取所有可能的 Chrome User Data 目录路径
    支持 Windows / macOS / Linux
    """
    paths = []
    system = platform.system()
    
    if system == "Windows":
        local_app_data = os.environ.get("LOCALAPPDATA", "")
        if local_app_data:
            paths.append(Path(local_app_data) / "Google" / "Chrome" / "User Data")
            paths.append(Path(local_app_data) / "Google" / "Chrome Beta" / "User Data")
            paths.append(Path(local_app_data) / "Google" / "Chrome Dev" / "User Data")
            paths.append(Path(local_app_data) / "Google" / "Chrome SxS" / "User Data")
    
    elif system == "Darwin":  # macOS
        home = Path.home()
        paths.append(home / "Library" / "Application Support" / "Google" / "Chrome")
        paths.append(home / "Library" / "Application Support" / "Google" / "Chrome Beta")
        paths.append(home / "Library" / "Application Support" / "Google" / "Chrome Dev")
        paths.append(home / "Library" / "Application Support" / "Google" / "Chrome Canary")
    
    elif system == "Linux":
        home = Path.home()
        paths.append(home / ".config" / "google-chrome")
        paths.append(home / ".config" / "google-chrome-beta")
        paths.append(home / ".config" / "google-chrome-unstable")
    
    # 只返回存在的路径
    return [p for p in paths if p.exists()]


def get_chrome_version_name(path: Path) -> str:
    """根据路径判断 Chrome 版本名称"""
    path_str = str(path).lower()
    if "beta" in path_str:
        return "Chrome Beta"
    elif "dev" in path_str or "unstable" in path_str:
        return "Chrome Dev"
    elif "sxs" in path_str or "canary" in path_str:
        return "Chrome Canary"
    else:
        return "Chrome Stable"


def get_last_version(user_data_path: Path) -> str | None:
    """获取 Chrome 版本号"""
    last_version_file = user_data_path / "Last Version"
    if not last_version_file.exists():
        return None
    try:
        return last_version_file.read_text(encoding="utf-8").strip()
    except Exception:
        return None


# ============== 配置检查 ==============

def load_config(path: Path) -> dict | None:
    """加载配置文件"""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(colored(f"❌ 无法读取配置文件: {e}", Color.RED))
        return None


def save_config(path: Path, config: dict) -> bool:
    """保存配置文件"""
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False, separators=(",", ":"))
        return True
    except Exception as e:
        print(colored(f"❌ 无法保存配置文件: {e}", Color.RED))
        return False


def check_country_config(config: dict) -> dict:
    """检查国家相关配置"""
    results = {}
    
    for key in COUNTRY_KEYS:
        value = config.get(key, None)
        results[key] = {
            "current": value,
            "target": TARGET_COUNTRY,
            "ok": value == TARGET_COUNTRY
        }
    
    # 检查数组格式的国家配置项
    value = config.get(ARRAY_COUNTRY_KEY, None)
    if isinstance(value, list) and len(value) >= 2:
        country = value[1] if len(value) >= 2 else value[0]
        results[ARRAY_COUNTRY_KEY] = {
            "current": value,
            "target": f"[版本, {TARGET_COUNTRY}]",
            "ok": country == TARGET_COUNTRY
        }
    else:
        results[ARRAY_COUNTRY_KEY] = {
            "current": value,
            "target": f"[版本, {TARGET_COUNTRY}]",
            "ok": False
        }
    
    return results


def check_glic_config(config: dict) -> dict:
    """检查 GLIC (Gemini Live in Chrome) 配置"""
    results = {}
    
    profile_info = config.get("profile", {}).get("info_cache", {})
    
    for profile_name, profile_data in profile_info.items():
        is_eligible = profile_data.get(GLIC_KEY, False)
        results[profile_name] = {
            "current": is_eligible,
            "target": True,
            "ok": is_eligible == True
        }
    
    return results


def check_locale_config(config: dict) -> dict:
    """检查语言区域配置"""
    results = {}
    
    # 检查 Local State 中的 app_locale
    intl = config.get("intl", {})
    app_locale = intl.get("app_locale", None)
    
    results["app_locale"] = {
        "current": app_locale,
        "target": TARGET_LOCALE,
        "ok": app_locale == TARGET_LOCALE
    }
    
    return results


def check_flags_config(config: dict) -> dict:
    """检查 Chrome Flags 配置 (chrome://flags)"""
    results = {}
    
    # 获取已启用的 flags 列表
    browser = config.get("browser", {})
    enabled_flags = browser.get("enabled_labs_experiments", [])
    
    # 创建已启用 flags 的集合（只保留 flag 名称，去掉 @1/@2 后缀）
    enabled_set = set()
    for flag in enabled_flags:
        # 格式: "flag-name@1" 或 "flag-name@2"
        if "@" in flag:
            name = flag.rsplit("@", 1)[0]
            value = flag.rsplit("@", 1)[1]
            if value == "1":  # @1 表示启用
                enabled_set.add(name)
        else:
            enabled_set.add(flag)
    
    # 检查每个 GLIC flag
    missing_flags = []
    enabled_count = 0
    
    for flag in GLIC_FLAGS:
        if flag in enabled_set:
            enabled_count += 1
        else:
            missing_flags.append(flag)
    
    results["glic_flags"] = {
        "current": f"{enabled_count}/{len(GLIC_FLAGS)} 已启用",
        "target": f"{len(GLIC_FLAGS)}/{len(GLIC_FLAGS)} 全部启用",
        "ok": enabled_count == len(GLIC_FLAGS),
        "missing": missing_flags
    }
    
    return results


def check_profile_language(profile_prefs: dict) -> dict:
    """检查 Profile 的语言偏好设置"""
    results = {}
    
    # 检查 intl.accept_languages
    intl = profile_prefs.get("intl", {})
    accept_languages = intl.get("accept_languages", "")
    
    # 检查是否以 en-US 开头
    is_en_us_first = accept_languages.startswith("en-US") or accept_languages.startswith("en")
    
    results["accept_languages"] = {
        "current": accept_languages[:50] + "..." if len(accept_languages) > 50 else accept_languages,
        "target": f"以 {TARGET_LOCALE} 开头",
        "ok": is_en_us_first
    }
    
    return results


# ============== 配置修复 ==============

def backup_config(path: Path) -> Path | None:
    """备份配置文件"""
    backup_path = path.parent / f"{path.name}.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    try:
        shutil.copy2(path, backup_path)
        return backup_path
    except Exception as e:
        print(colored(f"❌ 备份失败: {e}", Color.RED))
        return None


def fix_country_config(config: dict, last_version: str = None) -> int:
    """修复国家配置"""
    fixed = 0
    
    for key in COUNTRY_KEYS:
        if config.get(key) != TARGET_COUNTRY:
            config[key] = TARGET_COUNTRY
            fixed += 1
    
    value = config.get(ARRAY_COUNTRY_KEY)
    if isinstance(value, list) and len(value) >= 2:
        need_fix = False
        if last_version and value[0] != last_version:
            value[0] = last_version
            need_fix = True
        if value[1] != TARGET_COUNTRY:
            value[1] = TARGET_COUNTRY
            need_fix = True
        if need_fix:
            fixed += 1
    elif isinstance(value, list) and len(value) == 1:
        value.append(TARGET_COUNTRY)
        fixed += 1
    
    return fixed


def fix_glic_config(config: dict) -> int:
    """修复 GLIC 配置"""
    fixed = 0
    
    profile_info = config.get("profile", {}).get("info_cache", {})
    
    for profile_name, profile_data in profile_info.items():
        if profile_data.get(GLIC_KEY) != True:
            profile_data[GLIC_KEY] = True
            fixed += 1
    
    return fixed


def fix_locale_config(config: dict) -> int:
    """修复语言区域配置"""
    fixed = 0
    
    if "intl" not in config:
        config["intl"] = {}
    
    if config["intl"].get("app_locale") != TARGET_LOCALE:
        config["intl"]["app_locale"] = TARGET_LOCALE
        fixed += 1
    
    return fixed


def fix_flags_config(config: dict) -> int:
    """修复 Chrome Flags 配置 (启用 GLIC 相关 flags)"""
    fixed = 0
    
    # 确保 browser 和 enabled_labs_experiments 存在
    if "browser" not in config:
        config["browser"] = {}
    
    enabled_flags = config["browser"].get("enabled_labs_experiments", [])
    
    # 创建已存在 flags 的字典（flag-name -> full entry）
    existing_flags = {}
    for flag in enabled_flags:
        if "@" in flag:
            name = flag.rsplit("@", 1)[0]
            existing_flags[name] = flag
        else:
            existing_flags[flag] = flag
    
    # 添加缺失的 GLIC flags
    for flag in GLIC_FLAGS:
        flag_enabled = f"{flag}@1"
        
        if flag not in existing_flags:
            # 不存在，添加
            enabled_flags.append(flag_enabled)
            fixed += 1
        elif existing_flags[flag] != flag_enabled:
            # 存在但未启用（@2 表示禁用），替换为启用
            idx = enabled_flags.index(existing_flags[flag])
            enabled_flags[idx] = flag_enabled
            fixed += 1
    
    config["browser"]["enabled_labs_experiments"] = enabled_flags
    return fixed


def fix_profile_language(profile_prefs: dict) -> int:
    """修复 Profile 的语言偏好设置"""
    fixed = 0
    
    if "intl" not in profile_prefs:
        profile_prefs["intl"] = {}
    
    current = profile_prefs["intl"].get("accept_languages", "")
    
    # 如果不是以 en-US 开头，添加 en-US 到最前面
    if not current.startswith("en-US"):
        if current:
            profile_prefs["intl"]["accept_languages"] = f"en-US,en,{current}"
        else:
            profile_prefs["intl"]["accept_languages"] = "en-US,en"
        fixed += 1
    
    return fixed


# ============== 报告打印 ==============

def print_banner():
    """打印程序横幅"""
    banner = """
╔═══════════════════════════════════════════════════════════════╗
║       Gemini in Chrome Enabler - 一键启用 Chrome AI 功能       ║
║                  https://github.com/Kenny-BBDog                ║
╚═══════════════════════════════════════════════════════════════╝
"""
    print(colored(banner, Color.CYAN))


def print_check_results(country_results: dict, glic_results: dict, 
                        locale_results: dict, lang_results: dict,
                        flags_results: dict, chrome_name: str) -> bool:
    """打印检查结果"""
    print(colored(f"\n📋 {chrome_name} 配置检查报告", Color.BOLD))
    print("=" * 60)
    
    all_ok = True
    
    # 国家配置
    print(colored("\n🌍 国家/地区配置:", Color.BLUE))
    for key, result in country_results.items():
        status = colored("✅ 正常", Color.GREEN) if result["ok"] else colored("❌ 需修复", Color.RED)
        current = result["current"]
        print(f"  {key}")
        print(f"    当前值: {current}  {status}")
        if not result["ok"]:
            all_ok = False
    
    # GLIC 配置
    print(colored("\n🤖 Gemini in Chrome (GLIC) 配置:", Color.BLUE))
    for profile, result in glic_results.items():
        status = colored("✅ 已启用", Color.GREEN) if result["ok"] else colored("❌ 未启用", Color.RED)
        print(f"  {profile}: {status}")
        if not result["ok"]:
            all_ok = False
    
    # Chrome Flags
    print(colored("\n🚩 Chrome Flags (chrome://flags):", Color.BLUE))
    for key, result in flags_results.items():
        status = colored("✅ 正常", Color.GREEN) if result["ok"] else colored("⚠️ 需启用", Color.YELLOW)
        print(f"  {key}: {result['current']}  {status}")
        if not result["ok"]:
            all_ok = False
            if result.get("missing"):
                print(f"    缺失: {', '.join(result['missing'][:3])}..." if len(result['missing']) > 3 else f"    缺失: {', '.join(result['missing'])}")
    
    # 语言配置
    print(colored("\n🌐 Chrome 语言配置:", Color.MAGENTA))
    for key, result in locale_results.items():
        status = colored("✅ 正常", Color.GREEN) if result["ok"] else colored("⚠️ 建议修改", Color.YELLOW)
        print(f"  {key}: {result['current']}  {status}")
        if not result["ok"]:
            all_ok = False
    
    # Profile 语言偏好
    if lang_results:
        print(colored("\n📝 Profile 语言偏好:", Color.MAGENTA))
        for key, result in lang_results.items():
            status = colored("✅ 正常", Color.GREEN) if result["ok"] else colored("⚠️ 建议修改", Color.YELLOW)
            print(f"  {key}: {result['current']}  {status}")
            if not result["ok"]:
                all_ok = False
    
    # 总结
    print("\n" + "=" * 60)
    if all_ok:
        print(colored("✨ 所有配置正常！请重启 Chrome 两次以激活 Gemini 功能。", Color.GREEN))
    else:
        print(colored("⚠️  发现需要修复的配置项", Color.YELLOW))
    
    # Google 账号提示
    print(colored("\n💡 提示: Google 账号的语言设置需要手动修改:", Color.CYAN))
    print("   访问 https://myaccount.google.com/personal-info")
    print("   将 Language 设置为 English (United States)")
    
    return all_ok


# ============== 主程序 ==============

def process_chrome(user_data_path: Path, fix: bool = False) -> bool:
    """处理单个 Chrome 实例"""
    chrome_name = get_chrome_version_name(user_data_path)
    local_state_path = user_data_path / "Local State"
    
    print(colored(f"\n🔍 正在检查 {chrome_name}...", Color.CYAN))
    print(f"   路径: {user_data_path}")
    
    if not local_state_path.exists():
        print(colored("   ❌ Local State 文件不存在", Color.RED))
        return False
    
    # 获取 Chrome 版本
    last_version = get_last_version(user_data_path)
    if last_version:
        print(f"   版本: {last_version}")
    
    # 加载 Local State 配置
    config = load_config(local_state_path)
    if not config:
        return False
    
    # 检查 Local State 配置
    country_results = check_country_config(config)
    glic_results = check_glic_config(config)
    locale_results = check_locale_config(config)
    flags_results = check_flags_config(config)
    
    # 检查 Default Profile 的语言偏好
    default_prefs_path = user_data_path / "Default" / "Preferences"
    lang_results = {}
    default_prefs = None
    
    if default_prefs_path.exists():
        default_prefs = load_config(default_prefs_path)
        if default_prefs:
            lang_results = check_profile_language(default_prefs)
    
    # 打印检查结果
    all_ok = print_check_results(country_results, glic_results, 
                                  locale_results, lang_results, flags_results, chrome_name)
    
    if fix and not all_ok:
        print(colored("\n🔧 正在修复配置...", Color.YELLOW))
        
        # 备份 Local State
        backup_path = backup_config(local_state_path)
        if backup_path:
            print(f"   备份 Local State: {backup_path.name}")
        
        # 修复 Local State
        country_fixed = fix_country_config(config, last_version)
        glic_fixed = fix_glic_config(config)
        locale_fixed = fix_locale_config(config)
        flags_fixed = fix_flags_config(config)
        
        if save_config(local_state_path, config):
            print(colored(f"   ✅ 已修复 {country_fixed} 个国家配置项", Color.GREEN))
            print(colored(f"   ✅ 已为 {glic_fixed} 个 Profile 启用 GLIC", Color.GREEN))
            if flags_fixed:
                print(colored(f"   ✅ 已启用 {flags_fixed} 个 Chrome Flags", Color.GREEN))
            if locale_fixed:
                print(colored(f"   ✅ 已修复语言区域设置", Color.GREEN))
        
        # 修复 Default Profile 语言偏好
        if default_prefs and default_prefs_path.exists():
            backup_config(default_prefs_path)
            lang_fixed = fix_profile_language(default_prefs)
            if lang_fixed and save_config(default_prefs_path, default_prefs):
                print(colored(f"   ✅ 已修复 Default Profile 语言偏好", Color.GREEN))
        
        return True
    
    return all_ok


def main():
    """主函数"""
    print_banner()
    
    # 激活码校验 (仅限打包版)
    if not verify_activation():
        return 1
    
    fix_mode = "--fix" in sys.argv or "-f" in sys.argv
    auto_restart = "--no-restart" not in sys.argv
    
    if fix_mode:
        print(colored("⚡ 模式: 检测 + 自动修复", Color.YELLOW))
        
        if HAS_PSUTIL:
            print(colored("🔄 将自动关闭和重启 Chrome", Color.CYAN))
        else:
            print(colored("⚠️  请确保 Chrome 已完全关闭！", Color.RED))
            print("   (安装 psutil 可启用自动关闭功能: pip install psutil)")
        
        input("\n按 Enter 继续...")
        
        # 关闭 Chrome
        terminated_chromes = set()
        if HAS_PSUTIL and auto_restart:
            terminated_chromes = shutdown_chrome()
            if terminated_chromes:
                print(colored("\n🛑 已关闭 Chrome 浏览器", Color.YELLOW))
    else:
        print(colored("👀 模式: 仅检测", Color.BLUE))
        print("   使用 --fix 参数启用自动修复模式")
    
    # 查找 Chrome
    paths = get_chrome_user_data_paths()
    
    if not paths:
        print(colored("\n❌ 未找到 Chrome 安装", Color.RED))
        print("   请确保已安装 Google Chrome")
        return 1
    
    print(colored(f"\n📂 找到 {len(paths)} 个 Chrome 安装", Color.CYAN))
    
    # 处理每个 Chrome 实例
    all_success = True
    for path in paths:
        if not process_chrome(path, fix=fix_mode):
            all_success = False
    
    # 最终提示
    if fix_mode:
        print(colored("\n" + "=" * 60, Color.CYAN))
        print(colored("🎉 修复完成！", Color.GREEN))
        
        # 重启 Chrome
        if HAS_PSUTIL and auto_restart and terminated_chromes:
            restart_chrome(terminated_chromes)
            print(colored("\n🚀 Chrome 已重新启动", Color.GREEN))
            print(colored("   请再次手动重启 Chrome 以完成激活", Color.YELLOW))
        else:
            print(colored("\n📌 下一步操作:", Color.BOLD))
            print("   1. 完全关闭 Chrome（包括后台进程）")
            print("   2. 重新打开 Chrome")
            print("   3. 再次关闭并重新打开 Chrome（重启两次）")
            print("   4. 检查地址栏旁是否出现 Gemini 图标 ✨")
        
        print(colored("\n⚠️  注意: 需要连接 VPN 到美国节点才能正常使用 Gemini", Color.YELLOW))
        print(colored("\n💡 Google 账号语言需要手动设置:", Color.CYAN))
        print("   访问 https://myaccount.google.com/personal-info")
        print("   将 Language 设置为 English (United States)")
    
    return 0 if all_success else 1


if __name__ == "__main__":
    sys.exit(main())
