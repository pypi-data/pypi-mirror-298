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
import threading
import logging
import bstack_utils.bstack1ll1l111_opy_ as bstack1ll111111l_opy_
from bstack_utils.helper import bstack11l1ll1l1_opy_
logger = logging.getLogger(__name__)
def bstack1l111ll11l_opy_(key_name):
  return True if key_name in threading.current_thread().__dict__.keys() else False
def bstack11l1l11l_opy_(context, *args):
    tags = getattr(args[0], bstack111l1_opy_ (u"ࠪࡸࡦ࡭ࡳࠨྼ"), [])
    bstack11llll1ll_opy_ = bstack1ll111111l_opy_.bstack1l1111l11_opy_(tags)
    threading.current_thread().isA11yTest = bstack11llll1ll_opy_
    try:
      bstack1l11l1llll_opy_ = threading.current_thread().bstackSessionDriver if bstack1l111ll11l_opy_(bstack111l1_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪ྽")) else context.browser
      if bstack1l11l1llll_opy_ and bstack1l11l1llll_opy_.session_id and bstack11llll1ll_opy_ and bstack11l1ll1l1_opy_(
              threading.current_thread(), bstack111l1_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫ྾"), None):
          threading.current_thread().isA11yTest = bstack1ll111111l_opy_.bstack11lllll1_opy_(bstack1l11l1llll_opy_, bstack11llll1ll_opy_)
    except Exception as e:
       logger.debug(bstack111l1_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡸࡦࡸࡴࠡࡣ࠴࠵ࡾࠦࡩ࡯ࠢࡥࡩ࡭ࡧࡶࡦ࠼ࠣࡿࢂ࠭྿").format(str(e)))
def bstack1ll111l1_opy_(bstack1l11l1llll_opy_):
    if bstack11l1ll1l1_opy_(threading.current_thread(), bstack111l1_opy_ (u"ࠧࡪࡵࡄ࠵࠶ࡿࡔࡦࡵࡷࠫ࿀"), None) and bstack11l1ll1l1_opy_(
      threading.current_thread(), bstack111l1_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ࿁"), None) and not bstack11l1ll1l1_opy_(threading.current_thread(), bstack111l1_opy_ (u"ࠩࡤ࠵࠶ࡿ࡟ࡴࡶࡲࡴࠬ࿂"), False):
      threading.current_thread().a11y_stop = True
      bstack1ll111111l_opy_.bstack11l1l1l11_opy_(bstack1l11l1llll_opy_, name=bstack111l1_opy_ (u"ࠥࠦ࿃"), path=bstack111l1_opy_ (u"ࠦࠧ࿄"))