# coding: UTF-8
import sys
bstack1111ll_opy_ = sys.version_info [0] == 2
bstack111ll1l_opy_ = 2048
bstack11l1ll1_opy_ = 7
def bstack111l1_opy_ (bstack1llllll_opy_):
    global bstack11111l_opy_
    bstack1111ll1_opy_ = ord (bstack1llllll_opy_ [-1])
    bstack11l11l1_opy_ = bstack1llllll_opy_ [:-1]
    bstack1llllll1_opy_ = bstack1111ll1_opy_ % len (bstack11l11l1_opy_)
    bstack1l111l1_opy_ = bstack11l11l1_opy_ [:bstack1llllll1_opy_] + bstack11l11l1_opy_ [bstack1llllll1_opy_:]
    if bstack1111ll_opy_:
        bstackl_opy_ = unicode () .join ([unichr (ord (char) - bstack111ll1l_opy_ - (bstack1lll1ll_opy_ + bstack1111ll1_opy_) % bstack11l1ll1_opy_) for bstack1lll1ll_opy_, char in enumerate (bstack1l111l1_opy_)])
    else:
        bstackl_opy_ = str () .join ([chr (ord (char) - bstack111ll1l_opy_ - (bstack1lll1ll_opy_ + bstack1111ll1_opy_) % bstack11l1ll1_opy_) for bstack1lll1ll_opy_, char in enumerate (bstack1l111l1_opy_)])
    return eval (bstackl_opy_)
class bstack1llll1ll11_opy_:
    def __init__(self, handler):
        self._1lll1111111_opy_ = None
        self.handler = handler
        self._1ll1lllllll_opy_ = self.bstack1ll1llllll1_opy_()
        self.patch()
    def patch(self):
        self._1lll1111111_opy_ = self._1ll1lllllll_opy_.execute
        self._1ll1lllllll_opy_.execute = self.bstack1lll111111l_opy_()
    def bstack1lll111111l_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            self.handler(bstack111l1_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࠥᗕ"), driver_command, None, this, args)
            response = self._1lll1111111_opy_(this, driver_command, *args, **kwargs)
            self.handler(bstack111l1_opy_ (u"ࠦࡦ࡬ࡴࡦࡴࠥᗖ"), driver_command, response)
            return response
        return execute
    def reset(self):
        self._1ll1lllllll_opy_.execute = self._1lll1111111_opy_
    @staticmethod
    def bstack1ll1llllll1_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver