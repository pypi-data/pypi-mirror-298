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
import re
from bstack_utils.bstack1l1llll11l_opy_ import bstack1lll11l1l1l_opy_
def bstack1lll11l1lll_opy_(fixture_name):
    if fixture_name.startswith(bstack111l1_opy_ (u"ࠨࡡࡻࡹࡳ࡯ࡴࡠࡵࡨࡸࡺࡶ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᖢ")):
        return bstack111l1_opy_ (u"ࠩࡶࡩࡹࡻࡰ࠮ࡨࡸࡲࡨࡺࡩࡰࡰࠪᖣ")
    elif fixture_name.startswith(bstack111l1_opy_ (u"ࠪࡣࡽࡻ࡮ࡪࡶࡢࡷࡪࡺࡵࡱࡡࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᖤ")):
        return bstack111l1_opy_ (u"ࠫࡸ࡫ࡴࡶࡲ࠰ࡱࡴࡪࡵ࡭ࡧࠪᖥ")
    elif fixture_name.startswith(bstack111l1_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᖦ")):
        return bstack111l1_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮࠮ࡨࡸࡲࡨࡺࡩࡰࡰࠪᖧ")
    elif fixture_name.startswith(bstack111l1_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᖨ")):
        return bstack111l1_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰ࠰ࡱࡴࡪࡵ࡭ࡧࠪᖩ")
def bstack1lll111llll_opy_(fixture_name):
    return bool(re.match(bstack111l1_opy_ (u"ࠩࡡࡣࡽࡻ࡮ࡪࡶࡢࠬࡸ࡫ࡴࡶࡲࡿࡸࡪࡧࡲࡥࡱࡺࡲ࠮ࡥࠨࡧࡷࡱࡧࡹ࡯࡯࡯ࡾࡰࡳࡩࡻ࡬ࡦࠫࡢࡪ࡮ࡾࡴࡶࡴࡨࡣ࠳࠰ࠧᖪ"), fixture_name))
def bstack1lll11l111l_opy_(fixture_name):
    return bool(re.match(bstack111l1_opy_ (u"ࠪࡢࡤࡾࡵ࡯࡫ࡷࡣ࠭ࡹࡥࡵࡷࡳࢀࡹ࡫ࡡࡳࡦࡲࡻࡳ࠯࡟࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠ࠰࠭ࠫᖫ"), fixture_name))
def bstack1lll11ll1l1_opy_(fixture_name):
    return bool(re.match(bstack111l1_opy_ (u"ࠫࡣࡥࡸࡶࡰ࡬ࡸࡤ࠮ࡳࡦࡶࡸࡴࢁࡺࡥࡢࡴࡧࡳࡼࡴࠩࡠࡥ࡯ࡥࡸࡹ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠ࠰࠭ࠫᖬ"), fixture_name))
def bstack1lll111lll1_opy_(fixture_name):
    if fixture_name.startswith(bstack111l1_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡹࡥࡵࡷࡳࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᖭ")):
        return bstack111l1_opy_ (u"࠭ࡳࡦࡶࡸࡴ࠲࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧᖮ"), bstack111l1_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡆࡃࡆࡌࠬᖯ")
    elif fixture_name.startswith(bstack111l1_opy_ (u"ࠨࡡࡻࡹࡳ࡯ࡴࡠࡵࡨࡸࡺࡶ࡟࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᖰ")):
        return bstack111l1_opy_ (u"ࠩࡶࡩࡹࡻࡰ࠮࡯ࡲࡨࡺࡲࡥࠨᖱ"), bstack111l1_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡅࡑࡒࠧᖲ")
    elif fixture_name.startswith(bstack111l1_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᖳ")):
        return bstack111l1_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࠭ࡧࡷࡱࡧࡹ࡯࡯࡯ࠩᖴ"), bstack111l1_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡋࡁࡄࡊࠪᖵ")
    elif fixture_name.startswith(bstack111l1_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᖶ")):
        return bstack111l1_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰ࠰ࡱࡴࡪࡵ࡭ࡧࠪᖷ"), bstack111l1_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡃࡏࡐࠬᖸ")
    return None, None
def bstack1lll11ll111_opy_(hook_name):
    if hook_name in [bstack111l1_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩᖹ"), bstack111l1_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭ᖺ")]:
        return hook_name.capitalize()
    return hook_name
def bstack1lll11l11ll_opy_(hook_name):
    if hook_name in [bstack111l1_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠭ᖻ"), bstack111l1_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡳࡥࡵࡪࡲࡨࠬᖼ")]:
        return bstack111l1_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡆࡃࡆࡌࠬᖽ")
    elif hook_name in [bstack111l1_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟࡮ࡱࡧࡹࡱ࡫ࠧᖾ"), bstack111l1_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠࡥ࡯ࡥࡸࡹࠧᖿ")]:
        return bstack111l1_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡅࡑࡒࠧᗀ")
    elif hook_name in [bstack111l1_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠨᗁ"), bstack111l1_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡧࡷ࡬ࡴࡪࠧᗂ")]:
        return bstack111l1_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡋࡁࡄࡊࠪᗃ")
    elif hook_name in [bstack111l1_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡳࡩࡻ࡬ࡦࠩᗄ"), bstack111l1_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡧࡱࡧࡳࡴࠩᗅ")]:
        return bstack111l1_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡃࡏࡐࠬᗆ")
    return hook_name
def bstack1lll11l1l11_opy_(node, scenario):
    if hasattr(node, bstack111l1_opy_ (u"ࠪࡧࡦࡲ࡬ࡴࡲࡨࡧࠬᗇ")):
        parts = node.nodeid.rsplit(bstack111l1_opy_ (u"ࠦࡠࠨᗈ"))
        params = parts[-1]
        return bstack111l1_opy_ (u"ࠧࢁࡽࠡ࡝ࡾࢁࠧᗉ").format(scenario.name, params)
    return scenario.name
def bstack1lll11ll1ll_opy_(node):
    try:
        examples = []
        if hasattr(node, bstack111l1_opy_ (u"࠭ࡣࡢ࡮࡯ࡷࡵ࡫ࡣࠨᗊ")):
            examples = list(node.callspec.params[bstack111l1_opy_ (u"ࠧࡠࡲࡼࡸࡪࡹࡴࡠࡤࡧࡨࡤ࡫ࡸࡢ࡯ࡳࡰࡪ࠭ᗋ")].values())
        return examples
    except:
        return []
def bstack1lll11l1111_opy_(feature, scenario):
    return list(feature.tags) + list(scenario.tags)
def bstack1lll11ll11l_opy_(report):
    try:
        status = bstack111l1_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᗌ")
        if report.passed or (report.failed and hasattr(report, bstack111l1_opy_ (u"ࠤࡺࡥࡸࡾࡦࡢ࡫࡯ࠦᗍ"))):
            status = bstack111l1_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪᗎ")
        elif report.skipped:
            status = bstack111l1_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬᗏ")
        bstack1lll11l1l1l_opy_(status)
    except:
        pass
def bstack1ll11l111_opy_(status):
    try:
        bstack1lll11l11l1_opy_ = bstack111l1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᗐ")
        if status == bstack111l1_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ᗑ"):
            bstack1lll11l11l1_opy_ = bstack111l1_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧᗒ")
        elif status == bstack111l1_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩᗓ"):
            bstack1lll11l11l1_opy_ = bstack111l1_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪᗔ")
        bstack1lll11l1l1l_opy_(bstack1lll11l11l1_opy_)
    except:
        pass
def bstack1lll11l1ll1_opy_(item=None, report=None, summary=None, extra=None):
    return