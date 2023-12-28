import requests
from wordcloud import WordCloud
import matplotlib.pyplot as plt

class BiliBiliWordCloud:
    def __init__(self, oid, date, sessdata):
        self.oid = oid
        self.date = date
        self.sessdata = sessdata
        self.url = f'https://api.bilibili.com/x/v2/dm/web/history/seg.so?type=1&oid={self.oid}&date={self.date}'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36 Edg/94.0.992.31'
        }
        self.cookies = {
            'SESSDATA': self.sessdata,
        }

    def get_response(self):
        response = requests.get(self.url, headers=self.headers, cookies=self.cookies)
        return response

    def modify_text(self, text):
        lines = text.split('\n')  # 按行分割文本
        modified_lines = []
        humor_clock_count = 0  
        line_count = 0  # 用于统计行数
        for line in lines:
            try:
                post_colon = line.split(":")[1]
                result = post_colon.split("@")[0]
                modified_lines.append(result)
                if '幽默闹钟' in result:  
                    humor_clock_count += 1  
                line_count += 1  # 计数器加1
            except IndexError:
                continue  # 如果这一行没有":"或"@"，则跳过这一行
        print(f'"幽默闹钟"出现的次数: {humor_clock_count}')  
        print(f'总行数（句子数）: {line_count}')  # 打印总行数
        return modified_lines

    def generate_wordcloud(self, text, font_path='simhei.ttf'):
        # 创建词云对象
        wc = WordCloud(font_path=font_path, background_color='white', width=800, height=600)

        # 生成词云
        wc.generate(text)

        # 显示词云
        plt.imshow(wc, interpolation='bilinear')
        plt.axis('off')
        plt.show()

    def run(self):
        response = self.get_response()
        modified_text = self.modify_text(response.text)
        for line in modified_text:
            print(line)
        self.generate_wordcloud(' '.join(modified_text))

