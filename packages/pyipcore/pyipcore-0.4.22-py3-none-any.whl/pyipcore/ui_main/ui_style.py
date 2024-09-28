from pyipcore.ui_utils import *

print(LT_JLCYELLOW)
class UiTool_StyleAdjust:
    # Static class
    @classmethod
    def effect(cls, ui):
        """
        Adjust the style of the UI.
        """
        # 设置样式表
        ui.tab_sc.setStyleSheet("""
            QTabBar::tab {
                color: %s;
            }
            QTabBar::tab:selected {
                color: %s;
                background-color: %s;
            }
        """ % (DARK_DODGERBLUE.name(QColor.HexArgb),
               DARK_DODGERBLUE.darker().name(QColor.HexArgb),
               LT_JLCYELLOW.name(QColor.HexArgb)
               ))
