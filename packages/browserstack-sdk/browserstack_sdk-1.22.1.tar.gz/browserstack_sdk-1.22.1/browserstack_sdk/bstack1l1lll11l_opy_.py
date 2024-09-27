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
import multiprocessing
import os
import json
from time import sleep
import bstack_utils.bstack1ll1l111_opy_ as bstack1ll111111l_opy_
from browserstack_sdk.bstack1111l1111_opy_ import *
from bstack_utils.config import Config
from bstack_utils.messages import bstack1llll1l11l_opy_
class bstack1l1lllllll_opy_:
    def __init__(self, args, logger, bstack11l1l1111l_opy_, bstack11l1l1l1ll_opy_):
        self.args = args
        self.logger = logger
        self.bstack11l1l1111l_opy_ = bstack11l1l1111l_opy_
        self.bstack11l1l1l1ll_opy_ = bstack11l1l1l1ll_opy_
        self._prepareconfig = None
        self.Config = None
        self.runner = None
        self.bstack11ll111l1_opy_ = []
        self.bstack11l1l11ll1_opy_ = None
        self.bstack111lll1l1_opy_ = []
        self.bstack11l11lllll_opy_ = self.bstack1ll1l111l_opy_()
        self.bstack111111lll_opy_ = -1
    def bstack1l11l1ll11_opy_(self, bstack11l1l1l1l1_opy_):
        self.parse_args()
        self.bstack11l1l11l11_opy_()
        self.bstack11l1l111ll_opy_(bstack11l1l1l1l1_opy_)
    @staticmethod
    def version():
        import pytest
        return pytest.__version__
    @staticmethod
    def bstack11l1l11111_opy_():
        import importlib
        if getattr(importlib, bstack111l1_opy_ (u"ࠫ࡫࡯࡮ࡥࡡ࡯ࡳࡦࡪࡥࡳࠩ໖"), False):
            bstack11l1l1l111_opy_ = importlib.find_loader(bstack111l1_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࡤࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠧ໗"))
        else:
            bstack11l1l1l111_opy_ = importlib.util.find_spec(bstack111l1_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹࡥࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠨ໘"))
    def bstack11l1l1ll1l_opy_(self, arg):
        if arg in self.args:
            i = self.args.index(arg)
            self.args.pop(i + 1)
            self.args.pop(i)
    def parse_args(self):
        self.bstack111111lll_opy_ = -1
        if self.bstack11l1l1l1ll_opy_ and bstack111l1_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ໙") in self.bstack11l1l1111l_opy_:
            self.bstack111111lll_opy_ = int(self.bstack11l1l1111l_opy_[bstack111l1_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ໚")])
        try:
            bstack11l11llll1_opy_ = [bstack111l1_opy_ (u"ࠩ࠰࠱ࡩࡸࡩࡷࡧࡵࠫ໛"), bstack111l1_opy_ (u"ࠪ࠱࠲ࡶ࡬ࡶࡩ࡬ࡲࡸ࠭ໜ"), bstack111l1_opy_ (u"ࠫ࠲ࡶࠧໝ")]
            if self.bstack111111lll_opy_ >= 0:
                bstack11l11llll1_opy_.extend([bstack111l1_opy_ (u"ࠬ࠳࠭࡯ࡷࡰࡴࡷࡵࡣࡦࡵࡶࡩࡸ࠭ໞ"), bstack111l1_opy_ (u"࠭࠭࡯ࠩໟ")])
            for arg in bstack11l11llll1_opy_:
                self.bstack11l1l1ll1l_opy_(arg)
        except Exception as exc:
            self.logger.error(str(exc))
    def get_args(self):
        return self.args
    def bstack11l1l11l11_opy_(self):
        bstack11l1l11ll1_opy_ = [os.path.normpath(item) for item in self.args]
        self.bstack11l1l11ll1_opy_ = bstack11l1l11ll1_opy_
        return bstack11l1l11ll1_opy_
    def bstack1llll11ll_opy_(self):
        try:
            from _pytest.config import _prepareconfig
            from _pytest.config import Config
            from _pytest import runner
            self.bstack11l1l11111_opy_()
            self._prepareconfig = _prepareconfig
            self.Config = Config
            self.runner = runner
        except Exception as e:
            self.logger.warn(e, bstack1llll1l11l_opy_)
    def bstack11l1l111ll_opy_(self, bstack11l1l1l1l1_opy_):
        bstack1111ll1l1_opy_ = Config.bstack1l1ll11lll_opy_()
        if bstack11l1l1l1l1_opy_:
            self.bstack11l1l11ll1_opy_.append(bstack111l1_opy_ (u"ࠧ࠮࠯ࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ໠"))
            self.bstack11l1l11ll1_opy_.append(bstack111l1_opy_ (u"ࠨࡖࡵࡹࡪ࠭໡"))
        if bstack1111ll1l1_opy_.bstack11l1l1l11l_opy_():
            self.bstack11l1l11ll1_opy_.append(bstack111l1_opy_ (u"ࠩ࠰࠱ࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠨ໢"))
            self.bstack11l1l11ll1_opy_.append(bstack111l1_opy_ (u"ࠪࡘࡷࡻࡥࠨ໣"))
        self.bstack11l1l11ll1_opy_.append(bstack111l1_opy_ (u"ࠫ࠲ࡶࠧ໤"))
        self.bstack11l1l11ll1_opy_.append(bstack111l1_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࡤࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡴࡱࡻࡧࡪࡰࠪ໥"))
        self.bstack11l1l11ll1_opy_.append(bstack111l1_opy_ (u"࠭࠭࠮ࡦࡵ࡭ࡻ࡫ࡲࠨ໦"))
        self.bstack11l1l11ll1_opy_.append(bstack111l1_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࠧ໧"))
        if self.bstack111111lll_opy_ > 1:
            self.bstack11l1l11ll1_opy_.append(bstack111l1_opy_ (u"ࠨ࠯ࡱࠫ໨"))
            self.bstack11l1l11ll1_opy_.append(str(self.bstack111111lll_opy_))
    def bstack11l1l1lll1_opy_(self):
        bstack111lll1l1_opy_ = []
        for spec in self.bstack11ll111l1_opy_:
            bstack111ll1111_opy_ = [spec]
            bstack111ll1111_opy_ += self.bstack11l1l11ll1_opy_
            bstack111lll1l1_opy_.append(bstack111ll1111_opy_)
        self.bstack111lll1l1_opy_ = bstack111lll1l1_opy_
        return bstack111lll1l1_opy_
    def bstack1ll1l111l_opy_(self):
        try:
            from pytest_bdd import reporting
            self.bstack11l11lllll_opy_ = True
            return True
        except Exception as e:
            self.bstack11l11lllll_opy_ = False
        return self.bstack11l11lllll_opy_
    def bstack1llll1ll_opy_(self, bstack11l1l111l1_opy_, bstack1l11l1ll11_opy_):
        bstack1l11l1ll11_opy_[bstack111l1_opy_ (u"ࠩࡆࡓࡓࡌࡉࡈࠩ໩")] = self.bstack11l1l1111l_opy_
        multiprocessing.set_start_method(bstack111l1_opy_ (u"ࠪࡷࡵࡧࡷ࡯ࠩ໪"))
        bstack11ll11l11_opy_ = []
        manager = multiprocessing.Manager()
        bstack1ll111l11_opy_ = manager.list()
        if bstack111l1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ໫") in self.bstack11l1l1111l_opy_:
            for index, platform in enumerate(self.bstack11l1l1111l_opy_[bstack111l1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ໬")]):
                bstack11ll11l11_opy_.append(multiprocessing.Process(name=str(index),
                                                            target=bstack11l1l111l1_opy_,
                                                            args=(self.bstack11l1l11ll1_opy_, bstack1l11l1ll11_opy_, bstack1ll111l11_opy_)))
            bstack11l1l11lll_opy_ = len(self.bstack11l1l1111l_opy_[bstack111l1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ໭")])
        else:
            bstack11ll11l11_opy_.append(multiprocessing.Process(name=str(0),
                                                        target=bstack11l1l111l1_opy_,
                                                        args=(self.bstack11l1l11ll1_opy_, bstack1l11l1ll11_opy_, bstack1ll111l11_opy_)))
            bstack11l1l11lll_opy_ = 1
        i = 0
        for t in bstack11ll11l11_opy_:
            os.environ[bstack111l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧ໮")] = str(i)
            if bstack111l1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ໯") in self.bstack11l1l1111l_opy_:
                os.environ[bstack111l1_opy_ (u"ࠩࡆ࡙ࡗࡘࡅࡏࡖࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡊࡁࡕࡃࠪ໰")] = json.dumps(self.bstack11l1l1111l_opy_[bstack111l1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭໱")][i % bstack11l1l11lll_opy_])
            i += 1
            t.start()
        for t in bstack11ll11l11_opy_:
            t.join()
        return list(bstack1ll111l11_opy_)
    @staticmethod
    def bstack111l11ll1_opy_(driver, bstack11l1l1ll11_opy_, logger, item=None, wait=False):
        item = item or getattr(threading.current_thread(), bstack111l1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡹ࡫࡭ࠨ໲"), None)
        if item and getattr(item, bstack111l1_opy_ (u"ࠬࡥࡡ࠲࠳ࡼࡣࡹ࡫ࡳࡵࡡࡦࡥࡸ࡫ࠧ໳"), None) and not getattr(item, bstack111l1_opy_ (u"࠭࡟ࡢ࠳࠴ࡽࡤࡹࡴࡰࡲࡢࡨࡴࡴࡥࠨ໴"), False):
            logger.info(
                bstack111l1_opy_ (u"ࠢࡂࡷࡷࡳࡲࡧࡴࡦࠢࡷࡩࡸࡺࠠࡤࡣࡶࡩࠥ࡫ࡸࡦࡥࡸࡸ࡮ࡵ࡮ࠡࡪࡤࡷࠥ࡫࡮ࡥࡧࡧ࠲ࠥࡖࡲࡰࡥࡨࡷࡸ࡯࡮ࡨࠢࡩࡳࡷࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡴࡦࡵࡷ࡭ࡳ࡭ࠠࡪࡵࠣࡹࡳࡪࡥࡳࡹࡤࡽ࠳ࠨ໵"))
            bstack11l1l11l1l_opy_ = item.cls.__name__ if not item.cls is None else None
            bstack1ll111111l_opy_.bstack11l1l1l11_opy_(driver, item.name, item.path)
            item._a11y_stop_done = True
            if wait:
                sleep(2)