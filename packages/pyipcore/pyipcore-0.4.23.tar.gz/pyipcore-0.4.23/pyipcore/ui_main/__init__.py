import time
from pyipcore.ui_main.ui_main import Ui_MainForm
from pyipcore.ui_main.ui_style import UiTool_StyleAdjust
from pyipcore.ipcore import IpCore, VAR_PARAM_TYPE, VAR_PORT_TYPE
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QFileDialog, QWidget, QMainWindow, QLineEdit, QCheckBox, QHBoxLayout
from pyipcore.ui_creater import GUI_IPCreator
from pyipcore.ui_utils import *
from pyipcore.ipc_utils import *
from pyipcore.ip_module_view import IpCoreView
from files3 import files
from pyverilog.vparser.parser import ParseError


class TaskWorker(QThread):
    """
    一个Worker线程，用于处理InstCode的生成。
    具体来说，它会在一个循环中，每隔dt时间，从任务队列中取出一个任务并执行。
    而任务队列中的任务目前可以理解为一个InstCode生成函数。
    """

    def __init__(self, dt=0.2):
        super().__init__()
        self._tasks = []
        self._args = []
        self._flag = True
        self._dt = dt


    def run(self):
        while self._flag:
            if len(self._tasks) > 0:
                task = self._tasks.pop(0)
                args = self._args.pop(0)
                try:
                    _ = task(*args)
                except Exception as e:
                    print(f"Error: {e.__class__.__name__}: {str(e)}")


            time.sleep(self._dt)

    def add(self, task, *args):
        self._tasks.append(task)
        self._args.append(args)

    def stop(self):
        self._flag = False

    def __bool__(self):
        return self._flag

    def __len__(self):
        return len(self._tasks)


class QInspectorContainer(QWidget):
    def __init__(self, callback, parent=None):
        super(QInspectorContainer, self).__init__(parent)
        self._layout = QVBoxLayout()
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)
        self.setLayout(self._layout)
        self._callback = callback
        self._current:QMonoInspector = None

    @property
    def current(self):
        return self._current

    @current.setter
    def current(self, value):
        self._layout.removeWidget(self._current)
        if self._current is not None:
            del self._current
        self._current = value
        if self._current is not None:
            self._current.paramChanged.connect(self._callback)
            self._layout.addWidget(self._current)

WORKER_ACTIVE_DELTA = 1.0
WORKER_DEACTIVE_DELTA = 3.0
class GUI_Main(QMainWindow):
    def __init__(self):
        super(GUI_Main, self).__init__()
        self.ui = Ui_MainForm()
        self.ui.setupUi(self)
        self._render_lock = False
        self.setWindowTitle(f"{APP_NAME} {VERSION}")
        self.load_current_size()
        self.ui.tab_sc.setCurrentIndex(0)

        # add VarItemWidget into var_layout
        self.var_widget = QInspectorContainer(self._enable_ipcore_generate_update)
        self._need_update_flag = False

        self.ui.gbox_var.layout().addWidget(self.var_widget)

        # close即退出
        self.setWindowFlag(Qt.WindowCloseButtonHint, True)

        # worker
        self.worker = TaskWorker()
        self.worker.start()
        self.worker.dt = WORKER_DEACTIVE_DELTA

        # vars
        self.ipcore = None
        self.ip_creator = None
        self.var_dict = {}

        # /// customs
        # \t = 4 spaces
        self.ui.ptxt_rc.setTabStopWidth(4 * 4)
        self.ui.ptxt_cc.setTabStopWidth(4 * 4)
        self.ui.ptxt_ic.setTabStopWidth(4 * 4)
        self.reset_signals()

        # reset ptxt to QVerilogEdit
        self.reset_ptxt_xcs()

        # style change
        UiTool_StyleAdjust.effect(self.ui)


    @property
    def params(self):
        return self.var_widget.current.params

    def reset_signals(self):
        """
        重新绑定信号槽
        :return:
        """
        self.ui.action_file_open.triggered.connect(self.open_file)
        self.ui.action_file_close.triggered.connect(self.close_file)
        self.ui.action_file_scs.triggered.connect(self.save_current_size)
        self.ui.action_file_quit.triggered.connect(self.close)
        self.ui.action_proj_export.triggered.connect(self.export_proj)
        self.ui.action_tool_creator.triggered.connect(self.open_creator)
        self.ui.action_tool_creator.triggered.connect(self.open_creator)
        self.ui.action_help_readme.triggered.connect(lambda: PopInfo("Readme", "请参考README.md"))
        self.ui.action_help_about.triggered.connect(self.show_about)


    def reset_ptxt_xcs(self):
        """
        重置代码显示区域为VerilogEditor
        """
        self.ui.horizontalLayout_3.removeWidget(self.ui.ptxt_rc)
        self.ui.ptxt_rc = QVerilogEdit(self.ui.tab_rc)
        self.ui.ptxt_rc.setReadOnly(True)
        self.ui.ptxt_rc.setObjectName("ptxt_rc")
        self.ui.horizontalLayout_3.addWidget(self.ui.ptxt_rc)
        self.ui.horizontalLayout_4.removeWidget(self.ui.ptxt_cc)
        self.ui.ptxt_cc = QVerilogEdit(self.ui.tab_cc)
        self.ui.ptxt_cc.setReadOnly(True)
        self.ui.ptxt_cc.setObjectName("ptxt_cc")
        self.ui.horizontalLayout_4.addWidget(self.ui.ptxt_cc)
        self.ui.horizontalLayout_5.removeWidget(self.ui.ptxt_ic)
        self.ui.ptxt_ic = QVerilogEdit(self.ui.tab_ic)
        self.ui.ptxt_ic.setReadOnly(True)
        self.ui.ptxt_ic.setObjectName("ptxt_ic")
        self.ui.horizontalLayout_5.addWidget(self.ui.ptxt_ic)
        self.ui.horizontalLayout_2.removeWidget(self.ui.ptxt_mv)
        self.ui.ptxt_mv = IpCoreView(self.ui.tab_mv)
        self.ui.horizontalLayout_2.addWidget(self.ui.ptxt_mv)



    def open_creator(self):
        # open as dialog
        if self.ip_creator is not None:
            # 判断是否已经被销毁
            if self.ip_creator.isVisible():
                self.ip_creator.activateWindow()
                return
            else:
                self.ip_creator = None

        self.ip_creator = GUI_IPCreator()
        self.ip_creator.show()


    def _enable_ipcore_generate_update(self, *args):
        if not len(self.worker):
            self.worker.add(self._enter_update_vars)

    def _enter_update_vars(self, *args, default=False):
        # update cc ic
        try:
            if default:
                self.ipcore.build()
            else:
                self.ipcore.build(**self.params)
        except Exception as e:
            error = f"{e.__class__.__name__}:\n{str(e)}"
            self.ui.ptxt_cc.setText(error)
            self.ui.ptxt_ic.setText(error)
            self.ui.ptxt_mv.render_error(error)
            return
        # print("finish build")
        self.ui.ptxt_cc.setText(self.ipcore.built)
        self.ui.ptxt_ic.setText(self.ipcore.icode)
        self.ui.ptxt_mv.render_ipcore(self.ipcore)
        # update inspector
        if self.var_widget.current is not None:
            self.var_widget.current.rebuildTrigger.emit(self.ipcore._mono)


    def open_file(self):
        f = files(os.getcwd(), '.prefer')
        fdir = f["last_ipc_dir"]
        fdir = os.path.abspath(fdir) if fdir else os.getcwd()
        path = QFileDialog.getOpenFileName(self, "选择IP核文件", fdir, f"IP核文件 (*{IPC_SUFFIX})")[0]
        if not path:
            return
        if not os.path.isfile(path):
            PopError("错误", "路径无效")
            return
        fdir, fnametype = os.path.split(path)
        fname = fnametype[:-len(IPC_SUFFIX)]
        f = files(fdir, IPC_SUFFIX)
        get = f[fname]
        if get is F3False:
            PopError("错误", "IPC文件不存在或无法读取")
            return

        self.ipcore = IpCore(fdir, fname)
        self.ui.ptxt_rc.setText(get)
        self.ui.ptxt_cc.setText("")
        self.ui.ptxt_ic.setText("")
        self.ui.tab_sc.setCurrentIndex(0)
        self._enter_update_vars(default=True)

        # model
        try:
            self.var_widget.current = self.ipcore.GetInspector(skip_update=True)
        except Exception as e:
            PopError(f"{e.__class__.__name__}:", str(e), 1.5)
            return

        # active worker
        self.worker.dt = WORKER_ACTIVE_DELTA

        # save last fdir
        f = files(os.getcwd(), '.prefer')
        f["last_ipc_dir"] = fdir

        PopInfo("Info", "打开成功.")

    def close_file(self):
        self.ipcore = None
        self.ui.ptxt_rc.setText("")
        self.ui.ptxt_cc.setText("")
        self.ui.ptxt_ic.setText("")
        self.var_widget.current = None
        self.ui.tab_sc.setCurrentIndex(0)

        # deactive worker
        self.worker.dt = WORKER_DEACTIVE_DELTA


    def save_current_size(self):
        f = files(os.getcwd(), '.prefer')
        f["window_size"] = self.size()


    def load_current_size(self):
        f = files(os.getcwd(), '.prefer')
        size = f["window_size"]
        if size:
            self.resize(size)

    def export_proj(self):
        if self.ipcore is None:
            PopWarn("警告", "请先打开一个IP核文件.")
            return
        f = files(os.getcwd(), '.prefer')
        fdir = f["last_export_dir"]
        fdir = os.path.abspath(fdir) if fdir else os.getcwd()
        fdir = os.path.join(fdir, self.ipcore.name)
        path = QFileDialog.getSaveFileName(self, "选择导出的verilog文件", fdir, VERILOG_TYPE)[0]
        if not path:
            return

        fdir, fnametype = os.path.split(path)

        # save ipcore.built into file
        with open(path, 'w', encoding='utf-8') as f:
            f.write(self.ipcore.built)
        PopInfo("Info", "导出成功.")

        # save last fdir
        f = files(os.getcwd(), '.prefer')
        f["last_export_dir"] = fdir


    def show_about(self):
        about_dialog = AboutDialog(self)
        about_dialog.exec_()

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    gui = GUI_Main()
    gui.show()
    sys.exit(app.exec_())
