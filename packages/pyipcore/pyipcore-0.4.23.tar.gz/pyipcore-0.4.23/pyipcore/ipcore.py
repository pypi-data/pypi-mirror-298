import re
import math as pymodule_math
from pyipcore.ipc_utils import *
from files3 import files

VAR_PARAM_TYPE = "param"
VAR_PORT_TYPE = 'port'


class IpCoreBuiltError(Exception):
    pass

class IpCoreModuleDefParseError(Exception):
    pass

class IpCore:
    """
    维护IP核文本
    """

    def __init__(self, dir=None, name=None, *, content=None):
        self.fdir = os.path.abspath(dir) if dir is not None else None
        self.key = name if name else None
        self.f = files(self.fdir, IPC_SUFFIX) if self.fdir is not None else None
        if self.f and not self.f[self.key]:
            raise Exception("IP core not found: {}".format(name))

        self._mono = Mono(
            "//\s*>", "\n",
            "\$", "\$",
            "/*\s*>", "\*/",
            "//\s*\[", "\]",
            "//\s*\?", '//\s*:\?', "//\s*:", "//\s*\$",
            COMMENT=r";#", CSO=r"/*\s*#", CEO=r"\*/",
            ENV=r"import math"
        )

        self._content = content
        self._built = None
        self._fmd:FirstModuleDef = None
        self._last_icode = None
        self._lefts = None
        self._rights = None
        self._separators = None

    def GetICode(self):
        """Get the instance code of the IP core."""
        return self.icode

    @staticmethod
    def FromVerilog(dir, name, vpath):
        """Trasform a Verilog file into an IP core at the same path."""
        with open(vpath, encoding='utf-8') as vf:
            content = vf.read()
        return IpCore(dir, name, content=content)

    @staticmethod
    def VerilogToIpCore(dir, name, vpath):
        """Trasform a Verilog file into an IP core at the same path."""
        f = files(dir, IPC_SUFFIX)
        with open(vpath, encoding='utf-8') as vf:
            content = vf.read()
        f[name] = content

    VERILOG_NUMBER = f"({FT.DIGIT_CHAR}+'{FT.ALPHA})?[0-9_]+"


    def build(self, **params) -> str:
        """Build the IP core with the given parameters."""
        # print("Building...")
        content = self.content
        try:
            self._built = self._mono.handle(content, **params)
        except Exception as e:
            raise IpCoreBuiltError("Failed to build the IP core. Details:\n\t{}".format(e))
        # with open('test~.v', 'w', encoding='utf-8') as f:
        #     f.write(self._built)
        # print("Parsing...")
        try:
            self._fmd = FirstModuleDef(self._built)
        except Exception as e:
            # with open('built~.v', 'w', encoding='utf-8') as f:
            #     f.write(self._built)
            raise IpCoreModuleDefParseError("Failed to parse the module definition. Details:\n\t{}".format(e))
        return self._built

    # ----------------------------------------- Following are properties -----------------------------------------

    @property
    def name(self):
        return self.fmd.name

    @property
    def author(self):
        flst = FList()
        flst.login(IPC_AUTHOR_VID, *IPC_AUTHOR_GS)
        flst.handle(self.built)
        return flst[0] if len(flst) else "Unknown"

    @property
    def content(self):
        """Return the content of the IP core."""
        return self.f[self.key] if self.f else self._content


    # 获取参数名称
    @property
    def keys(self):
        """Return the parameters of the IP core."""
        return self._mono.keys

    @property
    def dict(self):
        """Return the parameters of the IP core."""
        return self._mono.dict

    def GetInspector(self, skip_update=False, **params):
        if not skip_update:
            self._mono.handle(self.content, **params)
        w = QMonoInspector(self._mono)
        return w

    @property
    def monos(self):
        return self._mono.monos

    @property
    def types(self) -> dict:
        return self._mono.types

    @property
    def separators(self):
        if self._separators is None:
            flst = FList()
            flst.login(IPC_VIEW_VID, *IPC_VIEW_SEP)
            flst.handle(self.built)
            self._separators = flst
            return flst
        return self._separators

    @property
    def lefts(self):
        if self._lefts is None:
            flst = FList()
            flst.login(IPC_LR_VID, *IPC_LEFT_GS)
            flst.handle(self.built)
            self._lefts = flst
            return flst
        return self._lefts

    @property
    def rights(self):
        if self._rights is None:
            flst = FList()
            flst.login(IPC_LR_VID, *IPC_RIGHT_GS)
            flst.handle(self.built)
            self._rights = flst
            return flst
        return self._rights

    @property
    def icode(self):
        """
        Get the instance code of the IP core.
        * Cost lots of time.
        :return:
        """
        header = builder_info(self.author)
        pure_inst_code = self.fmd.create_module_inst_code()
        self._last_icode = header + pure_inst_code
        return self._last_icode

    @property
    def last_icode(self):
        return self._last_icode

    @property
    def raw_ports(self) -> list[Input, Output]:
        return self.fmd.ports

    @property
    def ports(self) -> list[dict]:
        return [self.fmd.ioport_to_dict(i) for i in self.fmd.ports]

    @property
    def raw_inputs(self) -> list[Input]:
        return self.fmd.inputs

    @property
    def inputs(self) -> list[dict]:
        return [self.fmd.ioport_to_dict(i) for i in self.fmd.inputs]

    @property
    def raw_outputs(self) -> list[Output]:
        return self.fmd.outputs

    @property
    def outputs(self) -> list[dict]:
        return [self.fmd.ioport_to_dict(i) for i in self.fmd.outputs]


    @property  # TODO: 解决Icode不根据param改变而更新的问题
    def built(self):
        if self._built is None:
            self.build()
        return self._built

    @property
    def fmd(self):
        if self._fmd is None:
            self.build(**self.dict)
        return self._fmd



if __name__ == '__main__':
    IpCore.VerilogToIpCore("", 'test', r'H:\FPGA_Learns\00 IPC\_raw\counter.v5.v')
    # raise
    ip = IpCore("", 'test')
    t = ip.build()
    # save to a counter~.v file
    with open('counter~.v', 'w', encoding='utf-8') as f:
        f.write(t)
    # test = "module Counter #(parameter WIDTH=16,parameter RCO_WIDTH=4"
    # txt = ip.decorate_paragraph(test, 30, 35, "WIDTH", 0)
    # print(txt)
    # txt = ip.decorate_paragraph(txt, 33, 35, "WIDTH", 0)
    print(ip.author)
    print(ip.dict)
    print(ip.types)
    print(ip.icode)
    print(ip.built)
