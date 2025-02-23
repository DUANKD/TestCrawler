import requests
import json
import time

class BilibiliCrawler:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Referer': 'https://www.bilibili.com'
        }
        
    def get_video_info(self, bvid):
        """获取视频信息"""
        url = f'https://api.bilibili.com/x/web-interface/view?bvid={bvid}'
        
        try:
            response = requests.get(url, headers=self.headers)
            data = response.json()
            
            if data['code'] == 0:
                video_data = data['data']
                info = {
                    '标题': video_data['title'],
                    '作者': video_data['owner']['name'],
                    '播放量': video_data['stat']['view'],
                    '点赞数': video_data['stat']['like'],
                    '投币数': video_data['stat']['coin'],
                    '收藏数': video_data['stat']['favorite'],
                    '发布时间': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(video_data['pubdate']))
                }
                return info
            else:
                return f"错误: {data['message']}"
                
        except Exception as e:
            return f"发生错误: {str(e)}"

def main():
    crawler = BilibiliCrawler()
    
    # 测试视频BV号
    bv_id = input("请输入视频BV号（例如：BV1xx411c7mD）：")
    
    # 获取视频信息
    info = crawler.get_video_info(bv_id)
    
    # 打印结果
    if isinstance(info, dict):
        print("\n视频信息：")
        for key, value in info.items():
            print(f"{key}: {value}")
    else:
        print(info)

if __name__ == "__main__":
    main()