from pyipcore.ui_main.creator_page.fileitem import *


class QIpcInfoCollector(QWidget):  # 子组件，收集IP核文本信息
    """
    name: str  # IP核别名
    author: str  # IP核作者
    brand: str  # FPGA芯片品牌
    model: str  # FPGA芯片型号
    board: str  # IP核所适用开发板
    group: str  # IP核所属组别
    都不是必须的，可以为空，默认None
    """


class QIpCoreCreator(QWidget):
    ...
if __name__ == '__main__':
    app = QApplication(sys.argv)
    md_view = QMdView('test.md')
    md_view.show()
    sys.exit(app.exec_())