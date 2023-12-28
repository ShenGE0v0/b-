from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel, QTextEdit
from PyQt5.QtCore import Qt
from main import * 

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.oid_entry = QLineEdit(self)
        self.date_entry = QLineEdit(self)
        self.sessdata_entry = QLineEdit(self)
        self.result_text = QTextEdit(self)
        self.result_text.setReadOnly(True)
        self.url_entry = QLineEdit(self)  # 创建一个新的 QLineEdit 来输入 URL
        self.fetch_button = QPushButton('获取并搜索', self)  # 创建一个新的按钮来触发获取和搜索操作
        self.fetch_button.clicked.connect(self.fetch_and_search_url)  # 当按钮被点击时，调用 fetch_and_search_url 方法

        self.submit_button = QPushButton('开始爬取', self)
        self.submit_button.clicked.connect(self.generate_wordcloud)
        self.wordcloud_button = QPushButton('生成词云', self)
        self.wordcloud_button.clicked.connect(self.generate_wordcloud)
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("视频地址:"))
        layout.addWidget(self.oid_entry)
        layout.addWidget(QLabel("日期:"))
        layout.addWidget(self.date_entry)
        layout.addWidget(QLabel("Cookie:"))
        layout.addWidget(self.sessdata_entry)
        layout.addWidget(self.submit_button)
        layout.addWidget(QLabel("内容:"))
        layout.addWidget(self.result_text)
        layout.addWidget(self.wordcloud_button)
        layout.addWidget(QLabel("URL:"))
        layout.addWidget(self.url_entry)
        layout.addWidget(self.fetch_button)
    def generate_wordcloud(self):
        oid = self.oid_entry.text()
        date = self.date_entry.text()
        sessdata = self.sessdata_entry.text()
        bili = BiliBiliWordCloud(oid, date, sessdata)
        response = bili.get_response()
        modified_text = bili.modify_text(response.text)
        self.result_text.setPlainText('\n'.join(modified_text))  # 将爬取的数据显示在 result_text 文本框中
        bili.generate_wordcloud('\n'.join(modified_text))
    def fetch_and_search_url(self):
        url = self.url_entry.text()  # 从 QLineEdit 中获取 URL
        ulr = ULR()  # 创建 ULR 类的实例
        match = ulr.fetch_and_search(url)  # 通过 ULR 实例调用 fetch_and_search 方法
        if match:
            self.result_text.setPlainText(f"找到匹配项：{match.group()}")
        else:
            self.result_text.setPlainText("没有找到匹配项")
app = QApplication([])
window = MainWindow()
window.show()
app.exec_()
