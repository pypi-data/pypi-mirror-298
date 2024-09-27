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
import logging
import os
import threading
from bstack_utils.helper import bstack1ll11llll1_opy_
from bstack_utils.constants import bstack111ll1l1ll_opy_
logger = logging.getLogger(__name__)
class bstack1lll1l11_opy_:
    bstack1lll111ll1l_opy_ = None
    @classmethod
    def bstack11llll1l1_opy_(cls):
        if cls.on():
            logger.info(
                bstack111l1_opy_ (u"࡛ࠫ࡯ࡳࡪࡶࠣ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡣࡷ࡬ࡰࡩࡹ࠯ࡼࡿࠣࡸࡴࠦࡶࡪࡧࡺࠤࡧࡻࡩ࡭ࡦࠣࡶࡪࡶ࡯ࡳࡶ࠯ࠤ࡮ࡴࡳࡪࡩ࡫ࡸࡸ࠲ࠠࡢࡰࡧࠤࡲࡧ࡮ࡺࠢࡰࡳࡷ࡫ࠠࡥࡧࡥࡹ࡬࡭ࡩ࡯ࡩࠣ࡭ࡳ࡬࡯ࡳ࡯ࡤࡸ࡮ࡵ࡮ࠡࡣ࡯ࡰࠥࡧࡴࠡࡱࡱࡩࠥࡶ࡬ࡢࡥࡨࠥࡡࡴࠧᝬ").format(os.environ[bstack111l1_opy_ (u"ࠧࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡅ࡙ࡎࡒࡄࡠࡊࡄࡗࡍࡋࡄࡠࡋࡇࠦ᝭")]))
    @classmethod
    def on(cls):
        if os.environ.get(bstack111l1_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡎ࡜࡚ࠧᝮ"), None) is None or os.environ[bstack111l1_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡏ࡝ࡔࠨᝯ")] == bstack111l1_opy_ (u"ࠣࡰࡸࡰࡱࠨᝰ"):
            return False
        return True
    @classmethod
    def bstack1ll1l111111_opy_(cls, bs_config, framework=bstack111l1_opy_ (u"ࠤࠥ᝱")):
        if framework == bstack111l1_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪᝲ"):
            return bstack1ll11llll1_opy_(bs_config.get(bstack111l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡑࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨᝳ")))
        bstack1ll11lll111_opy_ = framework in bstack111ll1l1ll_opy_
        return bstack1ll11llll1_opy_(bs_config.get(bstack111l1_opy_ (u"ࠬࡺࡥࡴࡶࡒࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩ᝴"), bstack1ll11lll111_opy_))
    @classmethod
    def bstack1ll11lll1l1_opy_(cls, framework):
        return framework in bstack111ll1l1ll_opy_
    @classmethod
    def bstack1ll1ll111ll_opy_(cls, bs_config, framework):
        return cls.bstack1ll1l111111_opy_(bs_config, framework) is True and cls.bstack1ll11lll1l1_opy_(framework)
    @staticmethod
    def current_hook_uuid():
        return getattr(threading.current_thread(), bstack111l1_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪ᝵"), None)
    @staticmethod
    def bstack11lll1l1ll_opy_():
        if getattr(threading.current_thread(), bstack111l1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫ᝶"), None):
            return {
                bstack111l1_opy_ (u"ࠨࡶࡼࡴࡪ࠭᝷"): bstack111l1_opy_ (u"ࠩࡷࡩࡸࡺࠧ᝸"),
                bstack111l1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ᝹"): getattr(threading.current_thread(), bstack111l1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨ᝺"), None)
            }
        if getattr(threading.current_thread(), bstack111l1_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩ᝻"), None):
            return {
                bstack111l1_opy_ (u"࠭ࡴࡺࡲࡨࠫ᝼"): bstack111l1_opy_ (u"ࠧࡩࡱࡲ࡯ࠬ᝽"),
                bstack111l1_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ᝾"): getattr(threading.current_thread(), bstack111l1_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭᝿"), None)
            }
        return None
    @staticmethod
    def bstack1ll11lll1ll_opy_(func):
        def wrap(*args, **kwargs):
            if bstack1lll1l11_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def bstack11ll11llll_opy_(test, hook_name=None):
        bstack1ll11llll11_opy_ = test.parent
        if hook_name in [bstack111l1_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡦࡰࡦࡹࡳࠨក"), bstack111l1_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡣ࡭ࡣࡶࡷࠬខ"), bstack111l1_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࠫគ"), bstack111l1_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡲࡨࡺࡲࡥࠨឃ")]:
            bstack1ll11llll11_opy_ = test
        scope = []
        while bstack1ll11llll11_opy_ is not None:
            scope.append(bstack1ll11llll11_opy_.name)
            bstack1ll11llll11_opy_ = bstack1ll11llll11_opy_.parent
        scope.reverse()
        return scope[2:]
    @staticmethod
    def bstack1ll11lll11l_opy_(hook_type):
        if hook_type == bstack111l1_opy_ (u"ࠢࡃࡇࡉࡓࡗࡋ࡟ࡆࡃࡆࡌࠧង"):
            return bstack111l1_opy_ (u"ࠣࡕࡨࡸࡺࡶࠠࡩࡱࡲ࡯ࠧច")
        elif hook_type == bstack111l1_opy_ (u"ࠤࡄࡊ࡙ࡋࡒࡠࡇࡄࡇࡍࠨឆ"):
            return bstack111l1_opy_ (u"ࠥࡘࡪࡧࡲࡥࡱࡺࡲࠥ࡮࡯ࡰ࡭ࠥជ")
    @staticmethod
    def bstack1ll11ll1lll_opy_(bstack11ll111l1_opy_):
        try:
            if not bstack1lll1l11_opy_.on():
                return bstack11ll111l1_opy_
            if os.environ.get(bstack111l1_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡖࡊࡘࡕࡏࠤឈ"), None) == bstack111l1_opy_ (u"ࠧࡺࡲࡶࡧࠥញ"):
                tests = os.environ.get(bstack111l1_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡘࡅࡓࡗࡑࡣ࡙ࡋࡓࡕࡕࠥដ"), None)
                if tests is None or tests == bstack111l1_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧឋ"):
                    return bstack11ll111l1_opy_
                bstack11ll111l1_opy_ = tests.split(bstack111l1_opy_ (u"ࠨ࠮ࠪឌ"))
                return bstack11ll111l1_opy_
        except Exception as exc:
            print(bstack111l1_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡴࡨࡶࡺࡴࠠࡩࡣࡱࡨࡱ࡫ࡲ࠻ࠢࠥឍ"), str(exc))
        return bstack11ll111l1_opy_