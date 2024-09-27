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
import os
class RobotHandler():
    def __init__(self, args, logger, bstack11l1l1111l_opy_, bstack11l1l1l1ll_opy_):
        self.args = args
        self.logger = logger
        self.bstack11l1l1111l_opy_ = bstack11l1l1111l_opy_
        self.bstack11l1l1l1ll_opy_ = bstack11l1l1l1ll_opy_
    @staticmethod
    def version():
        import robot
        return robot.__version__
    @staticmethod
    def bstack11ll11llll_opy_(bstack11l11ll1ll_opy_):
        bstack11l11lll1l_opy_ = []
        if bstack11l11ll1ll_opy_:
            tokens = str(os.path.basename(bstack11l11ll1ll_opy_)).split(bstack111l1_opy_ (u"ࠣࡡࠥ໶"))
            camelcase_name = bstack111l1_opy_ (u"ࠤࠣࠦ໷").join(t.title() for t in tokens)
            suite_name, bstack11l11ll1l1_opy_ = os.path.splitext(camelcase_name)
            bstack11l11lll1l_opy_.append(suite_name)
        return bstack11l11lll1l_opy_
    @staticmethod
    def bstack11l11lll11_opy_(typename):
        if bstack111l1_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࠨ໸") in typename:
            return bstack111l1_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࡅࡳࡴࡲࡶࠧ໹")
        return bstack111l1_opy_ (u"࡛ࠧ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡆࡴࡵࡳࡷࠨ໺")