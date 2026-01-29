#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GeminiEnabler Key Generator - 激活码生成器
仅限开发者使用。根据用户提供的设备 ID 生成激活码。
"""

import hashlib

SECRET_SALT = "GeminiEnabler_Safe_Salt_2026"  # 必须与主脚本一致

def generate_key(hwid: str) -> str:
    """生成激活码"""
    return hashlib.md5((hwid.strip().upper() + SECRET_SALT).encode()).hexdigest().upper()

def main():
    print("╔══════════════════════════════════════════════════╗")
    print("║        GeminiEnabler 激活码生成器 (开发者版)      ║")
    print("╚══════════════════════════════════════════════════╝")
    
    print(f"\n当前盐值: {SECRET_SALT}")
    print("请确保此盐值与 enable_gemini.py 中的 SECRET_SALT 完全一致！")
    
    while True:
        hwid = input("\n请输入用户的设备 ID (输入 q 退出): ").strip().upper()
        if hwid == 'Q':
            break
        
        if not hwid:
            continue
            
        key = generate_key(hwid)
        print(f"\n✅ 已生成激活码: {key}")
        print("-" * 40)

if __name__ == "__main__":
    main()
