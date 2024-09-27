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
import datetime
import threading
from bstack_utils.helper import bstack11l11l1111_opy_, bstack111llll11_opy_, get_host_info, bstack11111ll1ll_opy_, \
 bstack1ll1l1111l_opy_, bstack11l1ll1l1_opy_, bstack11ll1ll111_opy_, bstack111l1l1ll1_opy_, bstack11l1l11l1_opy_
import bstack_utils.bstack1ll1l111_opy_ as bstack1ll111111l_opy_
from bstack_utils.bstack1l11l1l1ll_opy_ import bstack1lll1l11_opy_
from bstack_utils.percy import bstack1l11l111_opy_
from bstack_utils.config import Config
bstack1111ll1l1_opy_ = Config.bstack1l1ll11lll_opy_()
logger = logging.getLogger(__name__)
percy = bstack1l11l111_opy_()
@bstack11ll1ll111_opy_(class_method=False)
def bstack1ll1l11l111_opy_(bs_config, bstack111lllll_opy_):
  try:
    data = {
        bstack111l1_opy_ (u"ࠧࡧࡱࡵࡱࡦࡺࠧᜰ"): bstack111l1_opy_ (u"ࠨ࡬ࡶࡳࡳ࠭ᜱ"),
        bstack111l1_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡢࡲࡦࡳࡥࠨᜲ"): bs_config.get(bstack111l1_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨᜳ"), bstack111l1_opy_ (u"᜴ࠫࠬ")),
        bstack111l1_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ᜵"): bs_config.get(bstack111l1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ᜶"), os.path.basename(os.path.abspath(os.getcwd()))),
        bstack111l1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ᜷"): bs_config.get(bstack111l1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ᜸")),
        bstack111l1_opy_ (u"ࠩࡧࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴࠧ᜹"): bs_config.get(bstack111l1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡆࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳ࠭᜺"), bstack111l1_opy_ (u"ࠫࠬ᜻")),
        bstack111l1_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩ᜼"): bstack11l1l11l1_opy_(),
        bstack111l1_opy_ (u"࠭ࡴࡢࡩࡶࠫ᜽"): bstack11111ll1ll_opy_(bs_config),
        bstack111l1_opy_ (u"ࠧࡩࡱࡶࡸࡤ࡯࡮ࡧࡱࠪ᜾"): get_host_info(),
        bstack111l1_opy_ (u"ࠨࡥ࡬ࡣ࡮ࡴࡦࡰࠩ᜿"): bstack111llll11_opy_(),
        bstack111l1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡴࡸࡲࡤ࡯ࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩᝀ"): os.environ.get(bstack111l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅ࡙ࡎࡒࡄࡠࡔࡘࡒࡤࡏࡄࡆࡐࡗࡍࡋࡏࡅࡓࠩᝁ")),
        bstack111l1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࡣࡹ࡫ࡳࡵࡵࡢࡶࡪࡸࡵ࡯ࠩᝂ"): os.environ.get(bstack111l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡗࡋࡒࡖࡐࠪᝃ"), False),
        bstack111l1_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴ࡟ࡤࡱࡱࡸࡷࡵ࡬ࠨᝄ"): bstack11l11l1111_opy_(),
        bstack111l1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᝅ"): bstack1ll1l111l1l_opy_(),
        bstack111l1_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡩ࡫ࡴࡢ࡫࡯ࡷࠬᝆ"): bstack1ll11lllll1_opy_(bstack111lllll_opy_),
        bstack111l1_opy_ (u"ࠩࡳࡶࡴࡪࡵࡤࡶࡢࡱࡦࡶࠧᝇ"): bstack11llllllll_opy_(bs_config, bstack111lllll_opy_.get(bstack111l1_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡵࡴࡧࡧࠫᝈ"), bstack111l1_opy_ (u"ࠫࠬᝉ"))),
        bstack111l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧᝊ"): bstack1ll1l1111l_opy_(bs_config),
    }
    return data
  except Exception as error:
    logger.error(bstack111l1_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡥࡵࡩࡦࡺࡩ࡯ࡩࠣࡴࡦࡿ࡬ࡰࡣࡧࠤ࡫ࡵࡲࠡࡖࡨࡷࡹࡎࡵࡣ࠼ࠣࠤࢀࢃࠢᝋ").format(str(error)))
    return None
def bstack1ll11lllll1_opy_(framework):
  return {
    bstack111l1_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡑࡥࡲ࡫ࠧᝌ"): framework.get(bstack111l1_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦࠩᝍ"), bstack111l1_opy_ (u"ࠩࡓࡽࡹ࡫ࡳࡵࠩᝎ")),
    bstack111l1_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᝏ"): framework.get(bstack111l1_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨᝐ")),
    bstack111l1_opy_ (u"ࠬࡹࡤ࡬ࡘࡨࡶࡸ࡯࡯࡯ࠩᝑ"): framework.get(bstack111l1_opy_ (u"࠭ࡳࡥ࡭ࡢࡺࡪࡸࡳࡪࡱࡱࠫᝒ")),
    bstack111l1_opy_ (u"ࠧ࡭ࡣࡱ࡫ࡺࡧࡧࡦࠩᝓ"): bstack111l1_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨ᝔"),
    bstack111l1_opy_ (u"ࠩࡷࡩࡸࡺࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࠩ᝕"): framework.get(bstack111l1_opy_ (u"ࠪࡸࡪࡹࡴࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪ᝖"))
  }
def bstack11llllllll_opy_(bs_config, framework):
  bstack1ll11lll11_opy_ = False
  bstack111111l1l_opy_ = False
  if bstack111l1_opy_ (u"ࠫࡦࡶࡰࠨ᝗") in bs_config:
    bstack1ll11lll11_opy_ = True
  else:
    bstack111111l1l_opy_ = True
  bstack11111l1ll_opy_ = {
    bstack111l1_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬ᝘"): bstack1lll1l11_opy_.bstack1ll1l111111_opy_(bs_config, framework),
    bstack111l1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭᝙"): bstack1ll111111l_opy_.bstack11l11l1l11_opy_(bs_config),
    bstack111l1_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠭᝚"): bs_config.get(bstack111l1_opy_ (u"ࠨࡲࡨࡶࡨࡿࠧ᝛"), False),
    bstack111l1_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶࡨࠫ᝜"): bstack111111l1l_opy_,
    bstack111l1_opy_ (u"ࠪࡥࡵࡶ࡟ࡢࡷࡷࡳࡲࡧࡴࡦࠩ᝝"): bstack1ll11lll11_opy_
  }
  return bstack11111l1ll_opy_
@bstack11ll1ll111_opy_(class_method=False)
def bstack1ll1l111l1l_opy_():
  try:
    bstack1ll11llllll_opy_ = json.loads(os.getenv(bstack111l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬ᝞"), bstack111l1_opy_ (u"ࠬࢁࡽࠨ᝟")))
    return {
        bstack111l1_opy_ (u"࠭ࡳࡦࡶࡷ࡭ࡳ࡭ࡳࠨᝠ"): bstack1ll11llllll_opy_
    }
  except Exception as error:
    logger.error(bstack111l1_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡦࡶࡪࡧࡴࡪࡰࡪࠤ࡬࡫ࡴࡠࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡠࡵࡨࡸࡹ࡯࡮ࡨࡵࠣࡪࡴࡸࠠࡕࡧࡶࡸࡍࡻࡢ࠻ࠢࠣࡿࢂࠨᝡ").format(str(error)))
    return {}
def bstack1ll1l11ll1l_opy_(array, bstack1ll1l1111l1_opy_, bstack1ll1l1111ll_opy_):
  result = {}
  for o in array:
    key = o[bstack1ll1l1111l1_opy_]
    result[key] = o[bstack1ll1l1111ll_opy_]
  return result
def bstack1ll1l1l1ll1_opy_(bstack111l1ll1_opy_=bstack111l1_opy_ (u"ࠨࠩᝢ")):
  bstack1ll1l111ll1_opy_ = bstack1ll111111l_opy_.on()
  bstack1ll1l111l11_opy_ = bstack1lll1l11_opy_.on()
  bstack1ll11llll1l_opy_ = percy.bstack1l1ll1l1_opy_()
  if bstack1ll11llll1l_opy_ and not bstack1ll1l111l11_opy_ and not bstack1ll1l111ll1_opy_:
    return bstack111l1ll1_opy_ not in [bstack111l1_opy_ (u"ࠩࡆࡆ࡙࡙ࡥࡴࡵ࡬ࡳࡳࡉࡲࡦࡣࡷࡩࡩ࠭ᝣ"), bstack111l1_opy_ (u"ࠪࡐࡴ࡭ࡃࡳࡧࡤࡸࡪࡪࠧᝤ")]
  elif bstack1ll1l111ll1_opy_ and not bstack1ll1l111l11_opy_:
    return bstack111l1ll1_opy_ not in [bstack111l1_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬᝥ"), bstack111l1_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧᝦ"), bstack111l1_opy_ (u"࠭ࡌࡰࡩࡆࡶࡪࡧࡴࡦࡦࠪᝧ")]
  return bstack1ll1l111ll1_opy_ or bstack1ll1l111l11_opy_ or bstack1ll11llll1l_opy_
@bstack11ll1ll111_opy_(class_method=False)
def bstack1ll1l1l11l1_opy_(bstack111l1ll1_opy_, test=None):
  bstack1ll1l11111l_opy_ = bstack1ll111111l_opy_.on()
  if not bstack1ll1l11111l_opy_ or bstack111l1ll1_opy_ not in [bstack111l1_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩᝨ")] or test == None:
    return None
  return {
    bstack111l1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᝩ"): bstack1ll1l11111l_opy_ and bstack11l1ll1l1_opy_(threading.current_thread(), bstack111l1_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨᝪ"), None) == True and bstack1ll111111l_opy_.bstack1l1111l11_opy_(test[bstack111l1_opy_ (u"ࠪࡸࡦ࡭ࡳࠨᝫ")])
  }