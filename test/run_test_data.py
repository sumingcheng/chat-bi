#!/usr/bin/env python3
"""
测试数据生成运行脚本
使用方法: python run_test_data.py
"""
import subprocess
import sys
import os

def check_faker_installed():
    """检查 faker 是否已安装"""
    try:
        import faker
        print("✅ Faker 依赖已安装")
        return True
    except ImportError:
        return False

def install_dependencies():
    """安装必要的依赖"""
    print("📦 检查并安装依赖...")
    
    # 先检查是否已经安装
    if check_faker_installed():
        return True
    
    print("🔍 尝试安装 faker 依赖...")
    
    # 尝试使用 uv
    try:
        subprocess.check_call([sys.executable.replace("python.exe", "uv"), "add", "faker>=30.5.0"])
        print("✅ 通过 uv 安装 Faker 依赖完成")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass
    
    # 回退到 pip
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "faker>=30.5.0"])
        print("✅ 通过 pip 安装 Faker 依赖完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 安装依赖失败: {e}")
        print("💡 请手动安装: uv add faker 或 pip install faker")
        return False

def run_data_generation():
    """运行测试数据生成"""
    print("🚀 开始运行测试数据生成脚本...")
    try:
        # 使用相对路径调用同目录下的脚本
        script_path = os.path.join(os.path.dirname(__file__), "generate_test_data.py")
        result = subprocess.run([sys.executable, script_path], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ 测试数据生成成功!")
            print("\n📊 输出:")
            print(result.stdout)
        else:
            print("❌ 测试数据生成失败!")
            print(f"错误信息: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ 运行失败: {e}")
        return False
    return True

def main():
    """主函数"""
    print("="*60)
    print("🎯 Chat-BI 测试数据生成工具")
    print("="*60)
    
    # 检查是否在test目录或项目根目录
    current_dir = os.path.dirname(__file__)
    generate_script = os.path.join(current_dir, "generate_test_data.py")
    
    if not os.path.exists(generate_script):
        print("❌ 找不到 generate_test_data.py 文件")
        print("💡 请确保在 test 目录中运行此脚本")
        sys.exit(1)
    
    # 检查并安装依赖
    if not install_dependencies():
        print("❌ 依赖检查失败")
        print("💡 如果你已经安装了 faker，可以直接运行: python test/generate_test_data.py")
        sys.exit(1)
    
    # 运行数据生成
    if not run_data_generation():
        print("❌ 测试数据生成失败")
        sys.exit(1)
    
    print("\n" + "="*60)
    print("🎉 测试数据生成完成!")
    print("📝 现在可以使用以下方式查看数据:")
    print("   - API接口: http://localhost:13000/docs")
    print("   - 数据库: 使用MySQL客户端连接查看")
    print("="*60)

if __name__ == "__main__":
    main() 