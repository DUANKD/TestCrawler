import requests
import json
import time
import os  # 添加 os 模块导入


class fileChecker:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Referer": "https://www.bilibili.com",
        }

    def check_duplicate_files(self, folder_path):  # 添加 self 参数
        """检查文件夹中是否存在包含-2的文件，并进行相应处理"""
        try:
            # 获取文件夹中的所有文件
            files = os.listdir(folder_path)
            # 筛选包含-2的文件
            duplicate_files = [f for f in files if "-2" in f]

            if duplicate_files:
                print(f"找到包含'-2'的文件：")
                for file in duplicate_files:
                    print(f"- {file}")
                    # 构造原始文件名（移除-2）
                    original_name = file.replace("-2", "")
                    if original_name in files:
                        # 删除原始文件
                        original_path = os.path.join(folder_path, original_name)
                        os.remove(original_path)
                        print(f"  └─ 已删除原始文件: {original_name}")

                        # 重命名-2文件
                        old_path = os.path.join(folder_path, file)
                        new_path = os.path.join(folder_path, original_name)
                        os.rename(old_path, new_path)
                        print(f"  └─ 已将 {file} 重命名为 {original_name}")
                    else:
                        print(f"  └─ 未找到对应的原始文件")
                return True
            else:
                print("未找到包含'-2'的文件")
                return False

        except Exception as e:
            print(f"处理文件时发生错误: {str(e)}")
            return False


def main():
    checker = fileChecker()

    path = 'F:\\XiaoMi\\mi_assistant_backup\\20250302_100233'
    # 测试检查重复文件
    # folder_path = input("请输入要检查的文件夹路径：")
    folder_path = path
    checker.check_duplicate_files(folder_path)

if __name__ == "__main__":
    main()