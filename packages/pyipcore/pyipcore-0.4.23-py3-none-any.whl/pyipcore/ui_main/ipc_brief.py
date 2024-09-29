from pyipcore.ui_main.creator_page.fileitem import *
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
from PyQt5.QtGui import QFontDatabase
import markdown
import sys
import os

class QMdView(QWidget):
    def __init__(self, filepath, parent=None, *, fontsize=18, fontfamily="Microsoft YaHei UI"):
        super(QMdView, self).__init__(parent)
        self.filepath = filepath
        # 获取全局设置
        defaultSettings = QWebEngineSettings.globalSettings()

        # 设置默认字体大小
        defaultSettings.setFontSize(QWebEngineSettings.DefaultFontSize, fontsize)

        # 设置特定字体系列
        fontDatabase = QFontDatabase()
        standardFont = fontDatabase.font(fontfamily, "Regular", fontsize)
        defaultSettings.setFontFamily(QWebEngineSettings.StandardFont, standardFont.family())

        # 初始化UI
        self.initUI()


    def initUI(self):
        # 设置布局
        layout = QVBoxLayout(self)

        # 创建QWebEngineView对象
        self.web_view = QWebEngineView()
        layout.addWidget(self.web_view)

        # 加载并显示Markdown文件
        self.load_md_file()


    def load_md_file(self):
        # 将Markdown文件转换为HTML
        markdown_html = self.convert_md_to_html(self.filepath)

        # 使用QWebEngineView显示HTML内容
        self.web_view.setHtml(markdown_html)

    def convert_md_to_html(self, filepath):
        # 读取Markdown文件内容
        with open(filepath, 'r', encoding='utf-8') as file:
            markdown_content = file.read()

        # 使用markdown库将Markdown转换为HTML
        html_content = markdown.markdown(markdown_content)

        return html_content