import sys
import os

# 获取当前脚本所在目录（testpath.py 的目录：drawing-api/scripts/crud_generate）
current_script_dir = os.path.dirname(os.path.abspath(__file__))

# 计算项目根路径（drawing-api 目录）
project_root = os.path.dirname(os.path.dirname(current_script_dir))

# 将项目根路径加入 sys.path（确保优先级，可放最前面）
sys.path.insert(0, project_root)

# 验证路径是否正确
print("项目根路径:", project_root)  # 应输出: E:\218AiProject\Drawing-Recognition-PC\drawing-api

# 测试导入
try:
    from application.settings import BASE_DIR
    print("导入成功！BASE_DIR =", BASE_DIR)
except ModuleNotFoundError as e:
    print("导入失败:", e)
    # 额外调试：检查 application 包是否存在
    app_path = os.path.join(project_root, "application")
    if not os.path.exists(app_path):
        print(f"错误：{app_path} 目录不存在！")
    elif not os.path.isfile(os.path.join(app_path, "__init__.py")):
        print(f"错误：{app_path} 缺少 __init__.py 文件！")