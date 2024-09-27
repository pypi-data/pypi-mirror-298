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
import requests
import logging
import threading
from urllib.parse import urlparse
from bstack_utils.constants import bstack11l111l11l_opy_ as bstack11l111l111_opy_
from bstack_utils.bstack1lll11l1_opy_ import bstack1lll11l1_opy_
from bstack_utils.helper import bstack11l1l11l1_opy_, bstack11ll1lll1l_opy_, bstack1ll1l1111l_opy_, bstack11l111l1ll_opy_, bstack11l11l1lll_opy_, bstack111llll11_opy_, get_host_info, bstack11l11l1111_opy_, bstack1ll1l11111_opy_, bstack11ll1ll111_opy_
from browserstack_sdk._version import __version__
logger = logging.getLogger(__name__)
@bstack11ll1ll111_opy_(class_method=False)
def _11l11111ll_opy_(driver, bstack11l1l1ll11_opy_):
  response = {}
  try:
    caps = driver.capabilities
    response = {
        bstack111l1_opy_ (u"࠭࡯ࡴࡡࡱࡥࡲ࡫ࠧ໻"): caps.get(bstack111l1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪ࠭໼"), None),
        bstack111l1_opy_ (u"ࠨࡱࡶࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ໽"): bstack11l1l1ll11_opy_.get(bstack111l1_opy_ (u"ࠩࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠬ໾"), None),
        bstack111l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡳࡧ࡭ࡦࠩ໿"): caps.get(bstack111l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩༀ"), None),
        bstack111l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠧ༁"): caps.get(bstack111l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧ༂"), None)
    }
  except Exception as error:
    logger.debug(bstack111l1_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡦࡦࡶࡦ࡬࡮ࡴࡧࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠣࡨࡪࡺࡡࡪ࡮ࡶࠤࡼ࡯ࡴࡩࠢࡨࡶࡷࡵࡲࠡ࠼ࠣࠫ༃") + str(error))
  return response
def on():
    if os.environ.get(bstack111l1_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭༄"), None) is None or os.environ[bstack111l1_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧ༅")] == bstack111l1_opy_ (u"ࠥࡲࡺࡲ࡬ࠣ༆"):
        return False
    return True
def bstack11l11l1l11_opy_(config):
  return config.get(bstack111l1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ༇"), False) or any([p.get(bstack111l1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ༈"), False) == True for p in config.get(bstack111l1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ༉"), [])])
def bstack1l1l111ll1_opy_(config, bstack1l111lll11_opy_):
  try:
    if not bstack1ll1l1111l_opy_(config):
      return False
    bstack111lllll1l_opy_ = config.get(bstack111l1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ༊"), False)
    if int(bstack1l111lll11_opy_) < len(config.get(bstack111l1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ་"), [])) and config[bstack111l1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ༌")][bstack1l111lll11_opy_]:
      bstack11l11l11ll_opy_ = config[bstack111l1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭།")][bstack1l111lll11_opy_].get(bstack111l1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ༎"), None)
    else:
      bstack11l11l11ll_opy_ = config.get(bstack111l1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ༏"), None)
    if bstack11l11l11ll_opy_ != None:
      bstack111lllll1l_opy_ = bstack11l11l11ll_opy_
    bstack11l1111ll1_opy_ = os.getenv(bstack111l1_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫ༐")) is not None and len(os.getenv(bstack111l1_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬ༑"))) > 0 and os.getenv(bstack111l1_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭༒")) != bstack111l1_opy_ (u"ࠩࡱࡹࡱࡲࠧ༓")
    return bstack111lllll1l_opy_ and bstack11l1111ll1_opy_
  except Exception as error:
    logger.debug(bstack111l1_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡹࡩࡷ࡯ࡦࡺ࡫ࡱ࡫ࠥࡺࡨࡦࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡶࡩࡸࡹࡩࡰࡰࠣࡻ࡮ࡺࡨࠡࡧࡵࡶࡴࡸࠠ࠻ࠢࠪ༔") + str(error))
  return False
def bstack1l1111l11_opy_(test_tags):
  bstack111llllll1_opy_ = os.getenv(bstack111l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬ༕"))
  if bstack111llllll1_opy_ is None:
    return True
  bstack111llllll1_opy_ = json.loads(bstack111llllll1_opy_)
  try:
    include_tags = bstack111llllll1_opy_[bstack111l1_opy_ (u"ࠬ࡯࡮ࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪ༖")] if bstack111l1_opy_ (u"࠭ࡩ࡯ࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫ༗") in bstack111llllll1_opy_ and isinstance(bstack111llllll1_opy_[bstack111l1_opy_ (u"ࠧࡪࡰࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩ༘ࠬ")], list) else []
    exclude_tags = bstack111llllll1_opy_[bstack111l1_opy_ (u"ࠨࡧࡻࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ༙࠭")] if bstack111l1_opy_ (u"ࠩࡨࡼࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧ༚") in bstack111llllll1_opy_ and isinstance(bstack111llllll1_opy_[bstack111l1_opy_ (u"ࠪࡩࡽࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨ༛")], list) else []
    excluded = any(tag in exclude_tags for tag in test_tags)
    included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
    return not excluded and included
  except Exception as error:
    logger.debug(bstack111l1_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡹࡥࡱ࡯ࡤࡢࡶ࡬ࡲ࡬ࠦࡴࡦࡵࡷࠤࡨࡧࡳࡦࠢࡩࡳࡷࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡢࡦࡨࡲࡶࡪࠦࡳࡤࡣࡱࡲ࡮ࡴࡧ࠯ࠢࡈࡶࡷࡵࡲࠡ࠼ࠣࠦ༜") + str(error))
  return False
def bstack111llll1ll_opy_(config, bstack11l111ll1l_opy_, bstack11l1111l11_opy_, bstack11l11l11l1_opy_):
  bstack11l1111l1l_opy_ = bstack11l111l1ll_opy_(config)
  bstack111llll1l1_opy_ = bstack11l11l1lll_opy_(config)
  if bstack11l1111l1l_opy_ is None or bstack111llll1l1_opy_ is None:
    logger.error(bstack111l1_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠࡤࡴࡨࡥࡹ࡯࡮ࡨࠢࡷࡩࡸࡺࠠࡳࡷࡱࠤ࡫ࡵࡲࠡࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱ࠾ࠥࡓࡩࡴࡵ࡬ࡲ࡬ࠦࡡࡶࡶ࡫ࡩࡳࡺࡩࡤࡣࡷ࡭ࡴࡴࠠࡵࡱ࡮ࡩࡳ࠭༝"))
    return [None, None]
  try:
    settings = json.loads(os.getenv(bstack111l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡅࡈࡉࡅࡔࡕࡌࡆࡎࡒࡉࡕ࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢ࡝ࡒࡒࠧ༞"), bstack111l1_opy_ (u"ࠧࡼࡿࠪ༟")))
    data = {
        bstack111l1_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭༠"): config[bstack111l1_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧ༡")],
        bstack111l1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭༢"): config.get(bstack111l1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ༣"), os.path.basename(os.getcwd())),
        bstack111l1_opy_ (u"ࠬࡹࡴࡢࡴࡷࡘ࡮ࡳࡥࠨ༤"): bstack11l1l11l1_opy_(),
        bstack111l1_opy_ (u"࠭ࡤࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠫ༥"): config.get(bstack111l1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡊࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࠪ༦"), bstack111l1_opy_ (u"ࠨࠩ༧")),
        bstack111l1_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩ༨"): {
            bstack111l1_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡔࡡ࡮ࡧࠪ༩"): bstack11l111ll1l_opy_,
            bstack111l1_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࡖࡦࡴࡶ࡭ࡴࡴࠧ༪"): bstack11l1111l11_opy_,
            bstack111l1_opy_ (u"ࠬࡹࡤ࡬ࡘࡨࡶࡸ࡯࡯࡯ࠩ༫"): __version__,
            bstack111l1_opy_ (u"࠭࡬ࡢࡰࡪࡹࡦ࡭ࡥࠨ༬"): bstack111l1_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧ༭"),
            bstack111l1_opy_ (u"ࠨࡶࡨࡷࡹࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨ༮"): bstack111l1_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰࠫ༯"),
            bstack111l1_opy_ (u"ࠪࡸࡪࡹࡴࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭࡙ࡩࡷࡹࡩࡰࡰࠪ༰"): bstack11l11l11l1_opy_
        },
        bstack111l1_opy_ (u"ࠫࡸ࡫ࡴࡵ࡫ࡱ࡫ࡸ࠭༱"): settings,
        bstack111l1_opy_ (u"ࠬࡼࡥࡳࡵ࡬ࡳࡳࡉ࡯࡯ࡶࡵࡳࡱ࠭༲"): bstack11l11l1111_opy_(),
        bstack111l1_opy_ (u"࠭ࡣࡪࡋࡱࡪࡴ࠭༳"): bstack111llll11_opy_(),
        bstack111l1_opy_ (u"ࠧࡩࡱࡶࡸࡎࡴࡦࡰࠩ༴"): get_host_info(),
        bstack111l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰ༵ࠪ"): bstack1ll1l1111l_opy_(config)
    }
    headers = {
        bstack111l1_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡘࡾࡶࡥࠨ༶"): bstack111l1_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ༷࠭"),
    }
    config = {
        bstack111l1_opy_ (u"ࠫࡦࡻࡴࡩࠩ༸"): (bstack11l1111l1l_opy_, bstack111llll1l1_opy_),
        bstack111l1_opy_ (u"ࠬ࡮ࡥࡢࡦࡨࡶࡸ༹࠭"): headers
    }
    response = bstack1ll1l11111_opy_(bstack111l1_opy_ (u"࠭ࡐࡐࡕࡗࠫ༺"), bstack11l111l111_opy_ + bstack111l1_opy_ (u"ࠧ࠰ࡸ࠵࠳ࡹ࡫ࡳࡵࡡࡵࡹࡳࡹࠧ༻"), data, config)
    bstack11l11111l1_opy_ = response.json()
    if bstack11l11111l1_opy_[bstack111l1_opy_ (u"ࠨࡵࡸࡧࡨ࡫ࡳࡴࠩ༼")]:
      parsed = json.loads(os.getenv(bstack111l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪ༽"), bstack111l1_opy_ (u"ࠪࡿࢂ࠭༾")))
      parsed[bstack111l1_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬ༿")] = bstack11l11111l1_opy_[bstack111l1_opy_ (u"ࠬࡪࡡࡵࡣࠪཀ")][bstack111l1_opy_ (u"࠭ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧཁ")]
      os.environ[bstack111l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨག")] = json.dumps(parsed)
      bstack1lll11l1_opy_.bstack11l11ll111_opy_(bstack11l11111l1_opy_[bstack111l1_opy_ (u"ࠨࡦࡤࡸࡦ࠭གྷ")][bstack111l1_opy_ (u"ࠩࡶࡧࡷ࡯ࡰࡵࡵࠪང")])
      bstack1lll11l1_opy_.bstack11l11l111l_opy_(bstack11l11111l1_opy_[bstack111l1_opy_ (u"ࠪࡨࡦࡺࡡࠨཅ")][bstack111l1_opy_ (u"ࠫࡨࡵ࡭࡮ࡣࡱࡨࡸ࠭ཆ")])
      bstack1lll11l1_opy_.store()
      return bstack11l11111l1_opy_[bstack111l1_opy_ (u"ࠬࡪࡡࡵࡣࠪཇ")][bstack111l1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࡚࡯࡬ࡧࡱࠫ཈")], bstack11l11111l1_opy_[bstack111l1_opy_ (u"ࠧࡥࡣࡷࡥࠬཉ")][bstack111l1_opy_ (u"ࠨ࡫ࡧࠫཊ")]
    else:
      logger.error(bstack111l1_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤࡷࡻ࡮࡯࡫ࡱ࡫ࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮࠻ࠢࠪཋ") + bstack11l11111l1_opy_[bstack111l1_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫཌ")])
      if bstack11l11111l1_opy_[bstack111l1_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬཌྷ")] == bstack111l1_opy_ (u"ࠬࡏ࡮ࡷࡣ࡯࡭ࡩࠦࡣࡰࡰࡩ࡭࡬ࡻࡲࡢࡶ࡬ࡳࡳࠦࡰࡢࡵࡶࡩࡩ࠴ࠧཎ"):
        for bstack111lllllll_opy_ in bstack11l11111l1_opy_[bstack111l1_opy_ (u"࠭ࡥࡳࡴࡲࡶࡸ࠭ཏ")]:
          logger.error(bstack111lllllll_opy_[bstack111l1_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨཐ")])
      return None, None
  except Exception as error:
    logger.error(bstack111l1_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣࡧࡷ࡫ࡡࡵ࡫ࡱ࡫ࠥࡺࡥࡴࡶࠣࡶࡺࡴࠠࡧࡱࡵࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࠺ࠡࠤད") +  str(error))
    return None, None
def bstack11l111llll_opy_():
  if os.getenv(bstack111l1_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧདྷ")) is None:
    return {
        bstack111l1_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪན"): bstack111l1_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪཔ"),
        bstack111l1_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ཕ"): bstack111l1_opy_ (u"࠭ࡂࡶ࡫࡯ࡨࠥࡩࡲࡦࡣࡷ࡭ࡴࡴࠠࡩࡣࡧࠤ࡫ࡧࡩ࡭ࡧࡧ࠲ࠬབ")
    }
  data = {bstack111l1_opy_ (u"ࠧࡦࡰࡧࡘ࡮ࡳࡥࠨབྷ"): bstack11l1l11l1_opy_()}
  headers = {
      bstack111l1_opy_ (u"ࠨࡃࡸࡸ࡭ࡵࡲࡪࡼࡤࡸ࡮ࡵ࡮ࠨམ"): bstack111l1_opy_ (u"ࠩࡅࡩࡦࡸࡥࡳࠢࠪཙ") + os.getenv(bstack111l1_opy_ (u"ࠥࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠣཚ")),
      bstack111l1_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠪཛ"): bstack111l1_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠨཛྷ")
  }
  response = bstack1ll1l11111_opy_(bstack111l1_opy_ (u"࠭ࡐࡖࡖࠪཝ"), bstack11l111l111_opy_ + bstack111l1_opy_ (u"ࠧ࠰ࡶࡨࡷࡹࡥࡲࡶࡰࡶ࠳ࡸࡺ࡯ࡱࠩཞ"), data, { bstack111l1_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡴࠩཟ"): headers })
  try:
    if response.status_code == 200:
      logger.info(bstack111l1_opy_ (u"ࠤࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ࡚ࠥࡥࡴࡶࠣࡖࡺࡴࠠ࡮ࡣࡵ࡯ࡪࡪࠠࡢࡵࠣࡧࡴࡳࡰ࡭ࡧࡷࡩࡩࠦࡡࡵࠢࠥའ") + bstack11ll1lll1l_opy_().isoformat() + bstack111l1_opy_ (u"ࠪ࡞ࠬཡ"))
      return {bstack111l1_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫར"): bstack111l1_opy_ (u"ࠬࡹࡵࡤࡥࡨࡷࡸ࠭ལ"), bstack111l1_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧཤ"): bstack111l1_opy_ (u"ࠧࠨཥ")}
    else:
      response.raise_for_status()
  except requests.RequestException as error:
    logger.error(bstack111l1_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣࡱࡦࡸ࡫ࡪࡰࡪࠤࡨࡵ࡭ࡱ࡮ࡨࡸ࡮ࡵ࡮ࠡࡱࡩࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡕࡧࡶࡸࠥࡘࡵ࡯࠼ࠣࠦས") + str(error))
    return {
        bstack111l1_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩཧ"): bstack111l1_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩཨ"),
        bstack111l1_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬཀྵ"): str(error)
    }
def bstack11111l11_opy_(caps, options, desired_capabilities={}):
  try:
    bstack11l11l1l1l_opy_ = caps.get(bstack111l1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ཪ"), {}).get(bstack111l1_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠪཫ"), caps.get(bstack111l1_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࠧཬ"), bstack111l1_opy_ (u"ࠨࠩ཭")))
    if bstack11l11l1l1l_opy_:
      logger.warn(bstack111l1_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡷࡪ࡮࡯ࠤࡷࡻ࡮ࠡࡱࡱࡰࡾࠦ࡯࡯ࠢࡇࡩࡸࡱࡴࡰࡲࠣࡦࡷࡵࡷࡴࡧࡵࡷ࠳ࠨ཮"))
      return False
    if options:
      bstack11l111lll1_opy_ = options.to_capabilities()
    elif desired_capabilities:
      bstack11l111lll1_opy_ = desired_capabilities
    else:
      bstack11l111lll1_opy_ = {}
    browser = caps.get(bstack111l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨ཯"), bstack111l1_opy_ (u"ࠫࠬ཰")).lower() or bstack11l111lll1_opy_.get(bstack111l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧཱࠪ"), bstack111l1_opy_ (u"ི࠭ࠧ")).lower()
    if browser != bstack111l1_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ཱིࠧ"):
      logger.warn(bstack111l1_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡶࡺࡴࠠࡰࡰ࡯ࡽࠥࡵ࡮ࠡࡅ࡫ࡶࡴࡳࡥࠡࡤࡵࡳࡼࡹࡥࡳࡵ࠱ུࠦ"))
      return False
    browser_version = caps.get(bstack111l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰཱུࠪ")) or caps.get(bstack111l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬྲྀ")) or bstack11l111lll1_opy_.get(bstack111l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬཷ")) or bstack11l111lll1_opy_.get(bstack111l1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ླྀ"), {}).get(bstack111l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧཹ")) or bstack11l111lll1_opy_.get(bstack111l1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨེ"), {}).get(bstack111l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰཻࠪ"))
    if browser_version and browser_version != bstack111l1_opy_ (u"ࠩ࡯ࡥࡹ࡫ࡳࡵོࠩ") and int(browser_version.split(bstack111l1_opy_ (u"ࠪ࠲ཽࠬ"))[0]) <= 98:
      logger.warn(bstack111l1_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡹ࡬ࡰࡱࠦࡲࡶࡰࠣࡳࡳࡲࡹࠡࡱࡱࠤࡈ࡮ࡲࡰ࡯ࡨࠤࡧࡸ࡯ࡸࡵࡨࡶࠥࡼࡥࡳࡵ࡬ࡳࡳࠦࡧࡳࡧࡤࡸࡪࡸࠠࡵࡪࡤࡲࠥ࠿࠸࠯ࠤཾ"))
      return False
    if not options:
      bstack111lllll11_opy_ = caps.get(bstack111l1_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪཿ")) or bstack11l111lll1_opy_.get(bstack111l1_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶྀࠫ"), {})
      if bstack111l1_opy_ (u"ࠧ࠮࠯࡫ࡩࡦࡪ࡬ࡦࡵࡶཱྀࠫ") in bstack111lllll11_opy_.get(bstack111l1_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ྂ"), []):
        logger.warn(bstack111l1_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡷࡪ࡮࡯ࠤࡳࡵࡴࠡࡴࡸࡲࠥࡵ࡮ࠡ࡮ࡨ࡫ࡦࡩࡹࠡࡪࡨࡥࡩࡲࡥࡴࡵࠣࡱࡴࡪࡥ࠯ࠢࡖࡻ࡮ࡺࡣࡩࠢࡷࡳࠥࡴࡥࡸࠢ࡫ࡩࡦࡪ࡬ࡦࡵࡶࠤࡲࡵࡤࡦࠢࡲࡶࠥࡧࡶࡰ࡫ࡧࠤࡺࡹࡩ࡯ࡩࠣ࡬ࡪࡧࡤ࡭ࡧࡶࡷࠥࡳ࡯ࡥࡧ࠱ࠦྃ"))
        return False
    return True
  except Exception as error:
    logger.debug(bstack111l1_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡹࡥࡱ࡯ࡤࡢࡶࡨࠤࡦ࠷࠱ࡺࠢࡶࡹࡵࡶ࡯ࡳࡶࠣ࠾྄ࠧ") + str(error))
    return False
def set_capabilities(caps, config):
  try:
    bstack11l111l1l1_opy_ = config.get(bstack111l1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫ྅"), {})
    bstack11l111l1l1_opy_[bstack111l1_opy_ (u"ࠬࡧࡵࡵࡪࡗࡳࡰ࡫࡮ࠨ྆")] = os.getenv(bstack111l1_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫ྇"))
    bstack11l11l1ll1_opy_ = json.loads(os.getenv(bstack111l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨྈ"), bstack111l1_opy_ (u"ࠨࡽࢀࠫྉ"))).get(bstack111l1_opy_ (u"ࠩࡶࡧࡦࡴ࡮ࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪྊ"))
    caps[bstack111l1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪྋ")] = True
    if bstack111l1_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬྌ") in caps:
      caps[bstack111l1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ྍ")][bstack111l1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ྎ")] = bstack11l111l1l1_opy_
      caps[bstack111l1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨྏ")][bstack111l1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨྐ")][bstack111l1_opy_ (u"ࠩࡶࡧࡦࡴ࡮ࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪྑ")] = bstack11l11l1ll1_opy_
    else:
      caps[bstack111l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩྒ")] = bstack11l111l1l1_opy_
      caps[bstack111l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪྒྷ")][bstack111l1_opy_ (u"ࠬࡹࡣࡢࡰࡱࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ྔ")] = bstack11l11l1ll1_opy_
  except Exception as error:
    logger.debug(bstack111l1_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡵࡨࡸࡹ࡯࡮ࡨࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷ࠳ࠦࡅࡳࡴࡲࡶ࠿ࠦࠢྕ") +  str(error))
def bstack11lllll1_opy_(driver, bstack11l111111l_opy_):
  try:
    setattr(driver, bstack111l1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡁ࠲࠳ࡼࡗ࡭ࡵࡵ࡭ࡦࡖࡧࡦࡴࠧྖ"), True)
    session = driver.session_id
    if session:
      bstack11l11ll11l_opy_ = True
      current_url = driver.current_url
      try:
        url = urlparse(current_url)
      except Exception as e:
        bstack11l11ll11l_opy_ = False
      bstack11l11ll11l_opy_ = url.scheme in [bstack111l1_opy_ (u"ࠣࡪࡷࡸࡵࠨྗ"), bstack111l1_opy_ (u"ࠤ࡫ࡸࡹࡶࡳࠣ྘")]
      if bstack11l11ll11l_opy_:
        if bstack11l111111l_opy_:
          logger.info(bstack111l1_opy_ (u"ࠥࡗࡪࡺࡵࡱࠢࡩࡳࡷࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡴࡦࡵࡷ࡭ࡳ࡭ࠠࡩࡣࡶࠤࡸࡺࡡࡳࡶࡨࡨ࠳ࠦࡁࡶࡶࡲࡱࡦࡺࡥࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨࠤࡪࡾࡥࡤࡷࡷ࡭ࡴࡴࠠࡸ࡫࡯ࡰࠥࡨࡥࡨ࡫ࡱࠤࡲࡵ࡭ࡦࡰࡷࡥࡷ࡯࡬ࡺ࠰ࠥྙ"))
      return bstack11l111111l_opy_
  except Exception as e:
    logger.error(bstack111l1_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡷࡹࡧࡲࡵ࡫ࡱ࡫ࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡶࡧࡦࡴࠠࡧࡱࡵࠤࡹ࡮ࡩࡴࠢࡷࡩࡸࡺࠠࡤࡣࡶࡩ࠿ࠦࠢྚ") + str(e))
    return False
def bstack11l1l1l11_opy_(driver, name, path):
  try:
    bstack11l1111111_opy_ = {
        bstack111l1_opy_ (u"ࠬࡺࡨࡕࡧࡶࡸࡗࡻ࡮ࡖࡷ࡬ࡨࠬྛ"): threading.current_thread().current_test_uuid,
        bstack111l1_opy_ (u"࠭ࡴࡩࡄࡸ࡭ࡱࡪࡕࡶ࡫ࡧࠫྜ"): os.environ.get(bstack111l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬྜྷ"), bstack111l1_opy_ (u"ࠨࠩྞ")),
        bstack111l1_opy_ (u"ࠩࡷ࡬ࡏࡽࡴࡕࡱ࡮ࡩࡳ࠭ྟ"): os.environ.get(bstack111l1_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫྠ"), bstack111l1_opy_ (u"ࠫࠬྡ"))
    }
    logger.debug(bstack111l1_opy_ (u"ࠬࡖࡥࡳࡨࡲࡶࡲ࡯࡮ࡨࠢࡶࡧࡦࡴࠠࡣࡧࡩࡳࡷ࡫ࠠࡴࡣࡹ࡭ࡳ࡭ࠠࡳࡧࡶࡹࡱࡺࡳࠨྡྷ"))
    logger.debug(driver.execute_async_script(bstack1lll11l1_opy_.perform_scan, {bstack111l1_opy_ (u"ࠨ࡭ࡦࡶ࡫ࡳࡩࠨྣ"): name}))
    logger.debug(driver.execute_async_script(bstack1lll11l1_opy_.bstack11l1111lll_opy_, bstack11l1111111_opy_))
    logger.info(bstack111l1_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡵࡧࡶࡸ࡮ࡴࡧࠡࡨࡲࡶࠥࡺࡨࡪࡵࠣࡸࡪࡹࡴࠡࡥࡤࡷࡪࠦࡨࡢࡵࠣࡩࡳࡪࡥࡥ࠰ࠥྤ"))
  except Exception as bstack11l111ll11_opy_:
    logger.error(bstack111l1_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡴࡨࡷࡺࡲࡴࡴࠢࡦࡳࡺࡲࡤࠡࡰࡲࡸࠥࡨࡥࠡࡲࡵࡳࡨ࡫ࡳࡴࡧࡧࠤ࡫ࡵࡲࠡࡶ࡫ࡩࠥࡺࡥࡴࡶࠣࡧࡦࡹࡥ࠻ࠢࠥྥ") + str(path) + bstack111l1_opy_ (u"ࠤࠣࡉࡷࡸ࡯ࡳࠢ࠽ࠦྦ") + str(bstack11l111ll11_opy_))