import sys
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
import markdown

class QMdView(QWidget):
    def __init__(self, filepath, parent=None):
        super(QMdView, self).__init__(parent)
        self.filepath = filepath
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    md_view = QMdView('test.md')
    md_view.show()
    sys.exit(app.exec_())