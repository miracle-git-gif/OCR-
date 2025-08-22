import os
import sys
import requests
import json
from concurrent.futures import ThreadPoolExecutor
from PIL import Image
import io

# 配置参数
API_ENDPOINT = "http://127.0.0.1:8000/file_parse"  # 替换为实际API地址
API_KEY = "your-api-key"                           # 替换为你的API密钥
FOLDER_PATH = "./files_to_process"                 # 要处理的文件夹路径
MAX_WORKERS = 1                                    # 最大并发线程数
OUT_PATH = "./test999"
MAX_SIZE = (2048, 2048)                            # 最大图片尺寸（宽高）

if len(sys.argv) == 3:
    FOLDER_PATH = sys.argv[1]
    OUT_PATH = sys.argv[2]      
    print("文件目录", FOLDER_PATH)
    print("导出目录", OUT_PATH)
else:
    print("请传递两个参数 格式为 python script.py <文件目录> <导出目录>")
    exit()

def downscale_image(image_path, max_size=MAX_SIZE):
    """对图片进行降质（缩小尺寸）"""
    try:
        img = Image.open(image_path)
        img.thumbnail(max_size, Image.Resampling.LANCZOS)
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='JPEG', quality=85)
        img_bytes.seek(0)
        return img_bytes
    except Exception as e:
        print(f"降质图片失败 {image_path}: {e}")
        return None

def process_file(file_path):
    """处理单个文件的函数"""
    try:
        img_bytes = downscale_image(file_path)
        if img_bytes is None:
            return None

        files = {'files': (os.path.basename(file_path), img_bytes, 'image/jpeg')}
        headers = {'Authorization': f'Bearer {API_KEY}'}
        
        response = requests.post(
            API_ENDPOINT,
            files=files,
            data={'output_dir': OUT_PATH},
            # headers=headers,
            timeout=3000
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"成功处理 {file_path}: {json.dumps(result, indent=2)}")
            return result
        else:
            print(f"处理失败 {file_path}: {response.text}")
            return None
            
    except Exception as e:
        print(f"处理 {file_path} 时出错: {str(e)}")
        return None

def batch_process_files():
    """批量处理文件夹中的所有文件"""
    if not os.path.exists(FOLDER_PATH):
        print(f"文件夹不存在: {FOLDER_PATH}")
        return
        
    file_list = [
        os.path.join(FOLDER_PATH, f) 
        for f in os.listdir(FOLDER_PATH) 
        if os.path.isfile(os.path.join(FOLDER_PATH, f))
    ]
    
    if not file_list:
        print("文件夹中没有可处理的文件")
        return
        
    print(f"开始批量处理 {len(file_list)} 个文件...")
    
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        results = list(executor.map(process_file, file_list))
    
    print("\n处理完成！")
    return [r for r in results if r is not None]

if __name__ == "__main__":
    batch_process_files()
