import subprocess
import os
import chardet

def detect_encoding(filename):
    """检测文件编码"""
    with open(filename, "rb") as f:
        raw = f.read()
        result = chardet.detect(raw)
        return result["encoding"] or "utf-8"

def read_requirements(filename="requirements.txt"):
    """读取 requirements.txt，自动检测并修复编码"""
    packages = {}
    if not os.path.exists(filename):
        return packages

    # 检测编码
    encoding = detect_encoding(filename)
    # 重新读取文件
    try:
        with open(filename, "r", encoding=encoding) as f:
            lines = f.readlines()
    except UnicodeDecodeError:
        print(f"⚠️ 文件编码异常 ({encoding})，将尝试忽略错误读取。")
        with open(filename, "r", encoding=encoding, errors="ignore") as f:
            lines = f.readlines()

    # 解析依赖行
    for line in lines:
        line = line.strip()
        if "==" in line:
            try:
                name, version = line.split("==")
                packages[name.lower()] = version
            except ValueError:
                continue

    # 自动修复为 UTF-8 格式
    with open(filename, "w", encoding="utf-8") as f:
        for name, version in sorted(packages.items()):
            f.write(f"{name}=={version}\n")

    return packages

def get_installed_packages():
    """返回当前环境中已安装的包 {包名: 版本}"""
    result = subprocess.run(["pip", "freeze"], stdout=subprocess.PIPE, text=True)
    packages = {}
    for line in result.stdout.splitlines():
        if "==" in line:
            name, version = line.strip().split("==")
            packages[name.lower()] = version
    return packages

def write_requirements(packages, filename="requirements.txt"):
    """写入 requirements.txt"""
    with open(filename, "w", encoding="utf-8") as f:
        for name in sorted(packages.keys()):
            f.write(f"{name}=={packages[name]}\n")

def update_requirements():
    """主函数：检测、更新并自动修复 requirements.txt"""
    current = read_requirements()
    installed = get_installed_packages()
    updated = current.copy()
    updated.update(installed)

    if updated != current:
        write_requirements(updated)
        print("✅ requirements.txt 已更新并修复为 UTF-8 编码！")
        added = set(updated) - set(current)
        if added:
            print("🆕 新增包：", ", ".join(sorted(added)))
        else:
            print("🔄 已更新现有包版本。")
    else:
        print("📦 没有检测到新的依赖变化。")

if __name__ == "__main__":
    update_requirements()
