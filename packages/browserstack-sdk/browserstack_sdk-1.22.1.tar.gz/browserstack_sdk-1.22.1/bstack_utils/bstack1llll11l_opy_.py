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
from browserstack_sdk.bstack1l1lll11l_opy_ import bstack1l1lllllll_opy_
from browserstack_sdk.bstack11ll11l1ll_opy_ import RobotHandler
def bstack1l1ll111ll_opy_(framework):
    if framework.lower() == bstack111l1_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪኢ"):
        return bstack1l1lllllll_opy_.version()
    elif framework.lower() == bstack111l1_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪኣ"):
        return RobotHandler.version()
    elif framework.lower() == bstack111l1_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬኤ"):
        import behave
        return behave.__version__
    else:
        return bstack111l1_opy_ (u"࠭ࡵ࡯࡭ࡱࡳࡼࡴࠧእ")