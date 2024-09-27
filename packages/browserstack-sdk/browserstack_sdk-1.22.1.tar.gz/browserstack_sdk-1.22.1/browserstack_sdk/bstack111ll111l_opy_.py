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
import json
import logging
logger = logging.getLogger(__name__)
class BrowserStackSdk:
    def get_current_platform():
        bstack11l1llll_opy_ = {}
        bstack11lllll1l1_opy_ = os.environ.get(bstack111l1_opy_ (u"ࠬࡉࡕࡓࡔࡈࡒ࡙ࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡆࡄࡘࡆ࠭ග"), bstack111l1_opy_ (u"࠭ࠧඝ"))
        if not bstack11lllll1l1_opy_:
            return bstack11l1llll_opy_
        try:
            bstack11lllll11l_opy_ = json.loads(bstack11lllll1l1_opy_)
            if bstack111l1_opy_ (u"ࠢࡰࡵࠥඞ") in bstack11lllll11l_opy_:
                bstack11l1llll_opy_[bstack111l1_opy_ (u"ࠣࡱࡶࠦඟ")] = bstack11lllll11l_opy_[bstack111l1_opy_ (u"ࠤࡲࡷࠧච")]
            if bstack111l1_opy_ (u"ࠥࡳࡸࡥࡶࡦࡴࡶ࡭ࡴࡴࠢඡ") in bstack11lllll11l_opy_ or bstack111l1_opy_ (u"ࠦࡴࡹࡖࡦࡴࡶ࡭ࡴࡴࠢජ") in bstack11lllll11l_opy_:
                bstack11l1llll_opy_[bstack111l1_opy_ (u"ࠧࡵࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠣඣ")] = bstack11lllll11l_opy_.get(bstack111l1_opy_ (u"ࠨ࡯ࡴࡡࡹࡩࡷࡹࡩࡰࡰࠥඤ"), bstack11lllll11l_opy_.get(bstack111l1_opy_ (u"ࠢࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠥඥ")))
            if bstack111l1_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࠤඦ") in bstack11lllll11l_opy_ or bstack111l1_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠢට") in bstack11lllll11l_opy_:
                bstack11l1llll_opy_[bstack111l1_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠣඨ")] = bstack11lllll11l_opy_.get(bstack111l1_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࠧඩ"), bstack11lllll11l_opy_.get(bstack111l1_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠥඪ")))
            if bstack111l1_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠣණ") in bstack11lllll11l_opy_ or bstack111l1_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠣඬ") in bstack11lllll11l_opy_:
                bstack11l1llll_opy_[bstack111l1_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠤත")] = bstack11lllll11l_opy_.get(bstack111l1_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࠦථ"), bstack11lllll11l_opy_.get(bstack111l1_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠦද")))
            if bstack111l1_opy_ (u"ࠦࡩ࡫ࡶࡪࡥࡨࠦධ") in bstack11lllll11l_opy_ or bstack111l1_opy_ (u"ࠧࡪࡥࡷ࡫ࡦࡩࡓࡧ࡭ࡦࠤන") in bstack11lllll11l_opy_:
                bstack11l1llll_opy_[bstack111l1_opy_ (u"ࠨࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠥ඲")] = bstack11lllll11l_opy_.get(bstack111l1_opy_ (u"ࠢࡥࡧࡹ࡭ࡨ࡫ࠢඳ"), bstack11lllll11l_opy_.get(bstack111l1_opy_ (u"ࠣࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩࠧප")))
            if bstack111l1_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࠦඵ") in bstack11lllll11l_opy_ or bstack111l1_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠤබ") in bstack11lllll11l_opy_:
                bstack11l1llll_opy_[bstack111l1_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࡔࡡ࡮ࡧࠥභ")] = bstack11lllll11l_opy_.get(bstack111l1_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࠢම"), bstack11lllll11l_opy_.get(bstack111l1_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡏࡣࡰࡩࠧඹ")))
            if bstack111l1_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡡࡹࡩࡷࡹࡩࡰࡰࠥය") in bstack11lllll11l_opy_ or bstack111l1_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠥර") in bstack11lllll11l_opy_:
                bstack11l1llll_opy_[bstack111l1_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠦ඼")] = bstack11lllll11l_opy_.get(bstack111l1_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࡤࡼࡥࡳࡵ࡬ࡳࡳࠨල"), bstack11lllll11l_opy_.get(bstack111l1_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳࠨ඾")))
            if bstack111l1_opy_ (u"ࠧࡩࡵࡴࡶࡲࡱ࡛ࡧࡲࡪࡣࡥࡰࡪࡹࠢ඿") in bstack11lllll11l_opy_:
                bstack11l1llll_opy_[bstack111l1_opy_ (u"ࠨࡣࡶࡵࡷࡳࡲ࡜ࡡࡳ࡫ࡤࡦࡱ࡫ࡳࠣව")] = bstack11lllll11l_opy_[bstack111l1_opy_ (u"ࠢࡤࡷࡶࡸࡴࡳࡖࡢࡴ࡬ࡥࡧࡲࡥࡴࠤශ")]
        except Exception as error:
            logger.error(bstack111l1_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣ࡫ࡪࡺࡴࡪࡰࡪࠤࡨࡻࡲࡳࡧࡱࡸࠥࡶ࡬ࡢࡶࡩࡳࡷࡳࠠࡥࡣࡷࡥ࠿ࠦࠢෂ") +  str(error))
        return bstack11l1llll_opy_