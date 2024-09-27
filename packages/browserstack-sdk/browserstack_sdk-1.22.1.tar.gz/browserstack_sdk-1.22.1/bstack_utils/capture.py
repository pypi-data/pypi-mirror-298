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
import sys
class bstack11lll1lll1_opy_:
    def __init__(self, handler):
        self._111lll11ll_opy_ = sys.stdout.write
        self._111lll1111_opy_ = sys.stderr.write
        self.handler = handler
        self._started = False
    def start(self):
        if self._started:
            return
        self._started = True
        sys.stdout.write = self.bstack111lll111l_opy_
        sys.stdout.error = self.bstack111lll11l1_opy_
    def bstack111lll111l_opy_(self, _str):
        self._111lll11ll_opy_(_str)
        if self.handler:
            self.handler({bstack111l1_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫ࿅"): bstack111l1_opy_ (u"࠭ࡉࡏࡈࡒ࿆ࠫ"), bstack111l1_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ࿇"): _str})
    def bstack111lll11l1_opy_(self, _str):
        self._111lll1111_opy_(_str)
        if self.handler:
            self.handler({bstack111l1_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧ࿈"): bstack111l1_opy_ (u"ࠩࡈࡖࡗࡕࡒࠨ࿉"), bstack111l1_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ࿊"): _str})
    def reset(self):
        if not self._started:
            return
        self._started = False
        sys.stdout.write = self._111lll11ll_opy_
        sys.stderr.write = self._111lll1111_opy_