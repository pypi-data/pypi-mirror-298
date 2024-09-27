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
from collections import deque
from bstack_utils.constants import *
class bstack1l1ll1ll11_opy_:
    def __init__(self):
        self._1lll1l11l11_opy_ = deque()
        self._1lll1l1l111_opy_ = {}
        self._1lll1l1ll11_opy_ = False
    def bstack1lll1l1l1ll_opy_(self, test_name, bstack1lll1l1lll1_opy_):
        bstack1lll1l11ll1_opy_ = self._1lll1l1l111_opy_.get(test_name, {})
        return bstack1lll1l11ll1_opy_.get(bstack1lll1l1lll1_opy_, 0)
    def bstack1lll1ll1111_opy_(self, test_name, bstack1lll1l1lll1_opy_):
        bstack1lll1l1llll_opy_ = self.bstack1lll1l1l1ll_opy_(test_name, bstack1lll1l1lll1_opy_)
        self.bstack1lll1l111ll_opy_(test_name, bstack1lll1l1lll1_opy_)
        return bstack1lll1l1llll_opy_
    def bstack1lll1l111ll_opy_(self, test_name, bstack1lll1l1lll1_opy_):
        if test_name not in self._1lll1l1l111_opy_:
            self._1lll1l1l111_opy_[test_name] = {}
        bstack1lll1l11ll1_opy_ = self._1lll1l1l111_opy_[test_name]
        bstack1lll1l1llll_opy_ = bstack1lll1l11ll1_opy_.get(bstack1lll1l1lll1_opy_, 0)
        bstack1lll1l11ll1_opy_[bstack1lll1l1lll1_opy_] = bstack1lll1l1llll_opy_ + 1
    def bstack111l1l11_opy_(self, bstack1lll1l11lll_opy_, bstack1lll1l11l1l_opy_):
        bstack1lll1l1l11l_opy_ = self.bstack1lll1ll1111_opy_(bstack1lll1l11lll_opy_, bstack1lll1l11l1l_opy_)
        bstack1lll1l1ll1l_opy_ = bstack111ll1ll1l_opy_[bstack1lll1l11l1l_opy_]
        bstack1lll1ll111l_opy_ = bstack111l1_opy_ (u"ࠦࢀࢃ࠭ࡼࡿ࠰ࡿࢂࠨᕻ").format(bstack1lll1l11lll_opy_, bstack1lll1l1ll1l_opy_, bstack1lll1l1l11l_opy_)
        self._1lll1l11l11_opy_.append(bstack1lll1ll111l_opy_)
    def bstack1lll1lll1l_opy_(self):
        return len(self._1lll1l11l11_opy_) == 0
    def bstack1llll11l1l_opy_(self):
        bstack1lll1l1l1l1_opy_ = self._1lll1l11l11_opy_.popleft()
        return bstack1lll1l1l1l1_opy_
    def capturing(self):
        return self._1lll1l1ll11_opy_
    def bstack1ll1ll1ll_opy_(self):
        self._1lll1l1ll11_opy_ = True
    def bstack11111ll11_opy_(self):
        self._1lll1l1ll11_opy_ = False