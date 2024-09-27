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
import json
import os
import threading
from bstack_utils.config import Config
from bstack_utils.helper import bstack1111l11l1l_opy_, bstack1l1lllll1_opy_, bstack11l1ll1l1_opy_, bstack1llll1llll_opy_, \
    bstack1111lll1l1_opy_
def bstack1l1llll1_opy_(bstack1ll1lllll1l_opy_):
    for driver in bstack1ll1lllll1l_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1lll1111l1_opy_(driver, status, reason=bstack111l1_opy_ (u"ࠬ࠭ᗗ")):
    bstack1111ll1l1_opy_ = Config.bstack1l1ll11lll_opy_()
    if bstack1111ll1l1_opy_.bstack11l1l1l11l_opy_():
        return
    bstack11lll11l_opy_ = bstack11llll1l_opy_(bstack111l1_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠩᗘ"), bstack111l1_opy_ (u"ࠧࠨᗙ"), status, reason, bstack111l1_opy_ (u"ࠨࠩᗚ"), bstack111l1_opy_ (u"ࠩࠪᗛ"))
    driver.execute_script(bstack11lll11l_opy_)
def bstack11ll111ll_opy_(page, status, reason=bstack111l1_opy_ (u"ࠪࠫᗜ")):
    try:
        if page is None:
            return
        bstack1111ll1l1_opy_ = Config.bstack1l1ll11lll_opy_()
        if bstack1111ll1l1_opy_.bstack11l1l1l11l_opy_():
            return
        bstack11lll11l_opy_ = bstack11llll1l_opy_(bstack111l1_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠧᗝ"), bstack111l1_opy_ (u"ࠬ࠭ᗞ"), status, reason, bstack111l1_opy_ (u"࠭ࠧᗟ"), bstack111l1_opy_ (u"ࠧࠨᗠ"))
        page.evaluate(bstack111l1_opy_ (u"ࠣࡡࠣࡁࡃࠦࡻࡾࠤᗡ"), bstack11lll11l_opy_)
    except Exception as e:
        print(bstack111l1_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡵࡨࡸࡹ࡯࡮ࡨࠢࡶࡩࡸࡹࡩࡰࡰࠣࡷࡹࡧࡴࡶࡵࠣࡪࡴࡸࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࢀࢃࠢᗢ"), e)
def bstack11llll1l_opy_(type, name, status, reason, bstack1l111l11ll_opy_, bstack1lll11l11l_opy_):
    bstack1l1l11lll1_opy_ = {
        bstack111l1_opy_ (u"ࠪࡥࡨࡺࡩࡰࡰࠪᗣ"): type,
        bstack111l1_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧᗤ"): {}
    }
    if type == bstack111l1_opy_ (u"ࠬࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠧᗥ"):
        bstack1l1l11lll1_opy_[bstack111l1_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩᗦ")][bstack111l1_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ᗧ")] = bstack1l111l11ll_opy_
        bstack1l1l11lll1_opy_[bstack111l1_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫᗨ")][bstack111l1_opy_ (u"ࠩࡧࡥࡹࡧࠧᗩ")] = json.dumps(str(bstack1lll11l11l_opy_))
    if type == bstack111l1_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫᗪ"):
        bstack1l1l11lll1_opy_[bstack111l1_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧᗫ")][bstack111l1_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᗬ")] = name
    if type == bstack111l1_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠩᗭ"):
        bstack1l1l11lll1_opy_[bstack111l1_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪᗮ")][bstack111l1_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨᗯ")] = status
        if status == bstack111l1_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᗰ") and str(reason) != bstack111l1_opy_ (u"ࠥࠦᗱ"):
            bstack1l1l11lll1_opy_[bstack111l1_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧᗲ")][bstack111l1_opy_ (u"ࠬࡸࡥࡢࡵࡲࡲࠬᗳ")] = json.dumps(str(reason))
    bstack111llllll_opy_ = bstack111l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠫᗴ").format(json.dumps(bstack1l1l11lll1_opy_))
    return bstack111llllll_opy_
def bstack1l1ll111_opy_(url, config, logger, bstack111ll11l_opy_=False):
    hostname = bstack1l1lllll1_opy_(url)
    is_private = bstack1llll1llll_opy_(hostname)
    try:
        if is_private or bstack111ll11l_opy_:
            file_path = bstack1111l11l1l_opy_(bstack111l1_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧᗵ"), bstack111l1_opy_ (u"ࠨ࠰ࡥࡷࡹࡧࡣ࡬࠯ࡦࡳࡳ࡬ࡩࡨ࠰࡭ࡷࡴࡴࠧᗶ"), logger)
            if os.environ.get(bstack111l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡎࡒࡇࡆࡒ࡟ࡏࡑࡗࡣࡘࡋࡔࡠࡇࡕࡖࡔࡘࠧᗷ")) and eval(
                    os.environ.get(bstack111l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡏࡓࡈࡇࡌࡠࡐࡒࡘࡤ࡙ࡅࡕࡡࡈࡖࡗࡕࡒࠨᗸ"))):
                return
            if (bstack111l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨᗹ") in config and not config[bstack111l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩᗺ")]):
                os.environ[bstack111l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡒࡏࡄࡃࡏࡣࡓࡕࡔࡠࡕࡈࡘࡤࡋࡒࡓࡑࡕࠫᗻ")] = str(True)
                bstack1ll1llll1l1_opy_ = {bstack111l1_opy_ (u"ࠧࡩࡱࡶࡸࡳࡧ࡭ࡦࠩᗼ"): hostname}
                bstack1111lll1l1_opy_(bstack111l1_opy_ (u"ࠨ࠰ࡥࡷࡹࡧࡣ࡬࠯ࡦࡳࡳ࡬ࡩࡨ࠰࡭ࡷࡴࡴࠧᗽ"), bstack111l1_opy_ (u"ࠩࡱࡹࡩ࡭ࡥࡠ࡮ࡲࡧࡦࡲࠧᗾ"), bstack1ll1llll1l1_opy_, logger)
    except Exception as e:
        pass
def bstack1111lll1l_opy_(caps, bstack1ll1llll1ll_opy_):
    if bstack111l1_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫᗿ") in caps:
        caps[bstack111l1_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬᘀ")][bstack111l1_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࠫᘁ")] = True
        if bstack1ll1llll1ll_opy_:
            caps[bstack111l1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧᘂ")][bstack111l1_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩᘃ")] = bstack1ll1llll1ll_opy_
    else:
        caps[bstack111l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡭ࡱࡦࡥࡱ࠭ᘄ")] = True
        if bstack1ll1llll1ll_opy_:
            caps[bstack111l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪᘅ")] = bstack1ll1llll1ll_opy_
def bstack1lll11l1l1l_opy_(bstack11ll11l1l1_opy_):
    bstack1ll1lllll11_opy_ = bstack11l1ll1l1_opy_(threading.current_thread(), bstack111l1_opy_ (u"ࠪࡸࡪࡹࡴࡔࡶࡤࡸࡺࡹࠧᘆ"), bstack111l1_opy_ (u"ࠫࠬᘇ"))
    if bstack1ll1lllll11_opy_ == bstack111l1_opy_ (u"ࠬ࠭ᘈ") or bstack1ll1lllll11_opy_ == bstack111l1_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧᘉ"):
        threading.current_thread().testStatus = bstack11ll11l1l1_opy_
    else:
        if bstack11ll11l1l1_opy_ == bstack111l1_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᘊ"):
            threading.current_thread().testStatus = bstack11ll11l1l1_opy_