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
import re
bstack1111l1lll_opy_ = {
	bstack111l1_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫ࿐"): bstack111l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡸࡷࡪࡸࠧ࿑"),
  bstack111l1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧ࿒"): bstack111l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡰ࡫ࡹࠨ࿓"),
  bstack111l1_opy_ (u"࠭࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠩ࿔"): bstack111l1_opy_ (u"ࠧࡰࡵࡢࡺࡪࡸࡳࡪࡱࡱࠫ࿕"),
  bstack111l1_opy_ (u"ࠨࡷࡶࡩ࡜࠹ࡃࠨ࿖"): bstack111l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡷࡶࡩࡤࡽ࠳ࡤࠩ࿗"),
  bstack111l1_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨ࿘"): bstack111l1_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࠬ࿙"),
  bstack111l1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ࿚"): bstack111l1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࠬ࿛"),
  bstack111l1_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬ࿜"): bstack111l1_opy_ (u"ࠨࡰࡤࡱࡪ࠭࿝"),
  bstack111l1_opy_ (u"ࠩࡧࡩࡧࡻࡧࠨ࿞"): bstack111l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡧࡩࡧࡻࡧࠨ࿟"),
  bstack111l1_opy_ (u"ࠫࡨࡵ࡮ࡴࡱ࡯ࡩࡑࡵࡧࡴࠩ࿠"): bstack111l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡮ࡴࡱ࡯ࡩࠬ࿡"),
  bstack111l1_opy_ (u"࠭࡮ࡦࡶࡺࡳࡷࡱࡌࡰࡩࡶࠫ࿢"): bstack111l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡮ࡦࡶࡺࡳࡷࡱࡌࡰࡩࡶࠫ࿣"),
  bstack111l1_opy_ (u"ࠨࡣࡳࡴ࡮ࡻ࡭ࡍࡱࡪࡷࠬ࿤"): bstack111l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡳࡴ࡮ࡻ࡭ࡍࡱࡪࡷࠬ࿥"),
  bstack111l1_opy_ (u"ࠪࡺ࡮ࡪࡥࡰࠩ࿦"): bstack111l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡺ࡮ࡪࡥࡰࠩ࿧"),
  bstack111l1_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳࡌࡰࡩࡶࠫ࿨"): bstack111l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡹࡥ࡭ࡧࡱ࡭ࡺࡳࡌࡰࡩࡶࠫ࿩"),
  bstack111l1_opy_ (u"ࠧࡵࡧ࡯ࡩࡲ࡫ࡴࡳࡻࡏࡳ࡬ࡹࠧ࿪"): bstack111l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡵࡧ࡯ࡩࡲ࡫ࡴࡳࡻࡏࡳ࡬ࡹࠧ࿫"),
  bstack111l1_opy_ (u"ࠩࡪࡩࡴࡒ࡯ࡤࡣࡷ࡭ࡴࡴࠧ࿬"): bstack111l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡪࡩࡴࡒ࡯ࡤࡣࡷ࡭ࡴࡴࠧ࿭"),
  bstack111l1_opy_ (u"ࠫࡹ࡯࡭ࡦࡼࡲࡲࡪ࠭࿮"): bstack111l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡹ࡯࡭ࡦࡼࡲࡲࡪ࠭࿯"),
  bstack111l1_opy_ (u"࠭ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨ࿰"): bstack111l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ࿱"),
  bstack111l1_opy_ (u"ࠨ࡯ࡤࡷࡰࡉ࡯࡮࡯ࡤࡲࡩࡹࠧ࿲"): bstack111l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡯ࡤࡷࡰࡉ࡯࡮࡯ࡤࡲࡩࡹࠧ࿳"),
  bstack111l1_opy_ (u"ࠪ࡭ࡩࡲࡥࡕ࡫ࡰࡩࡴࡻࡴࠨ࿴"): bstack111l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱࡭ࡩࡲࡥࡕ࡫ࡰࡩࡴࡻࡴࠨ࿵"),
  bstack111l1_opy_ (u"ࠬࡳࡡࡴ࡭ࡅࡥࡸ࡯ࡣࡂࡷࡷ࡬ࠬ࿶"): bstack111l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡳࡡࡴ࡭ࡅࡥࡸ࡯ࡣࡂࡷࡷ࡬ࠬ࿷"),
  bstack111l1_opy_ (u"ࠧࡴࡧࡱࡨࡐ࡫ࡹࡴࠩ࿸"): bstack111l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡴࡧࡱࡨࡐ࡫ࡹࡴࠩ࿹"),
  bstack111l1_opy_ (u"ࠩࡤࡹࡹࡵࡗࡢ࡫ࡷࠫ࿺"): bstack111l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡹࡹࡵࡗࡢ࡫ࡷࠫ࿻"),
  bstack111l1_opy_ (u"ࠫ࡭ࡵࡳࡵࡵࠪ࿼"): bstack111l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲࡭ࡵࡳࡵࡵࠪ࿽"),
  bstack111l1_opy_ (u"࠭ࡢࡧࡥࡤࡧ࡭࡫ࠧ࿾"): bstack111l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡧࡥࡤࡧ࡭࡫ࠧ࿿"),
  bstack111l1_opy_ (u"ࠨࡹࡶࡐࡴࡩࡡ࡭ࡕࡸࡴࡵࡵࡲࡵࠩက"): bstack111l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡹࡶࡐࡴࡩࡡ࡭ࡕࡸࡴࡵࡵࡲࡵࠩခ"),
  bstack111l1_opy_ (u"ࠪࡨ࡮ࡹࡡࡣ࡮ࡨࡇࡴࡸࡳࡓࡧࡶࡸࡷ࡯ࡣࡵ࡫ࡲࡲࡸ࠭ဂ"): bstack111l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡨ࡮ࡹࡡࡣ࡮ࡨࡇࡴࡸࡳࡓࡧࡶࡸࡷ࡯ࡣࡵ࡫ࡲࡲࡸ࠭ဃ"),
  bstack111l1_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡓࡧ࡭ࡦࠩင"): bstack111l1_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪ࠭စ"),
  bstack111l1_opy_ (u"ࠧࡳࡧࡤࡰࡒࡵࡢࡪ࡮ࡨࠫဆ"): bstack111l1_opy_ (u"ࠨࡴࡨࡥࡱࡥ࡭ࡰࡤ࡬ࡰࡪ࠭ဇ"),
  bstack111l1_opy_ (u"ࠩࡤࡴࡵ࡯ࡵ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩဈ"): bstack111l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡴࡵ࡯ࡵ࡮ࡡࡹࡩࡷࡹࡩࡰࡰࠪဉ"),
  bstack111l1_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡒࡪࡺࡷࡰࡴ࡮ࠫည"): bstack111l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡻࡳࡵࡱࡰࡒࡪࡺࡷࡰࡴ࡮ࠫဋ"),
  bstack111l1_opy_ (u"࠭࡮ࡦࡶࡺࡳࡷࡱࡐࡳࡱࡩ࡭ࡱ࡫ࠧဌ"): bstack111l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡮ࡦࡶࡺࡳࡷࡱࡐࡳࡱࡩ࡭ࡱ࡫ࠧဍ"),
  bstack111l1_opy_ (u"ࠨࡣࡦࡧࡪࡶࡴࡊࡰࡶࡩࡨࡻࡲࡦࡅࡨࡶࡹࡹࠧဎ"): bstack111l1_opy_ (u"ࠩࡤࡧࡨ࡫ࡰࡵࡕࡶࡰࡈ࡫ࡲࡵࡵࠪဏ"),
  bstack111l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬတ"): bstack111l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬထ"),
  bstack111l1_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬဒ"): bstack111l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡹ࡯ࡶࡴࡦࡩࠬဓ"),
  bstack111l1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩန"): bstack111l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩပ"),
  bstack111l1_opy_ (u"ࠩ࡫ࡳࡸࡺࡎࡢ࡯ࡨࠫဖ"): bstack111l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡫ࡳࡸࡺࡎࡢ࡯ࡨࠫဗ"),
  bstack111l1_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡗ࡮ࡳࠧဘ"): bstack111l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡪࡴࡡࡣ࡮ࡨࡗ࡮ࡳࠧမ"),
  bstack111l1_opy_ (u"࠭ࡳࡪ࡯ࡒࡴࡹ࡯࡯࡯ࡵࠪယ"): bstack111l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡳࡪ࡯ࡒࡴࡹ࡯࡯࡯ࡵࠪရ"),
  bstack111l1_opy_ (u"ࠨࡷࡳࡰࡴࡧࡤࡎࡧࡧ࡭ࡦ࠭လ"): bstack111l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡷࡳࡰࡴࡧࡤࡎࡧࡧ࡭ࡦ࠭ဝ")
}
bstack111ll1111l_opy_ = [
  bstack111l1_opy_ (u"ࠪࡳࡸ࠭သ"),
  bstack111l1_opy_ (u"ࠫࡴࡹࡖࡦࡴࡶ࡭ࡴࡴࠧဟ"),
  bstack111l1_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳࡖࡦࡴࡶ࡭ࡴࡴࠧဠ"),
  bstack111l1_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫအ"),
  bstack111l1_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠫဢ"),
  bstack111l1_opy_ (u"ࠨࡴࡨࡥࡱࡓ࡯ࡣ࡫࡯ࡩࠬဣ"),
  bstack111l1_opy_ (u"ࠩࡤࡴࡵ࡯ࡵ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩဤ"),
]
bstack11111llll_opy_ = {
  bstack111l1_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬဥ"): [bstack111l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢ࡙ࡘࡋࡒࡏࡃࡐࡉࠬဦ"), bstack111l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡚࡙ࡅࡓࡡࡑࡅࡒࡋࠧဧ")],
  bstack111l1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩဨ"): bstack111l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡄࡅࡈࡗࡘࡥࡋࡆ࡛ࠪဩ"),
  bstack111l1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫဪ"): bstack111l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡘࡍࡑࡊ࡟ࡏࡃࡐࡉࠬါ"),
  bstack111l1_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨာ"): bstack111l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡗࡕࡊࡆࡅࡗࡣࡓࡇࡍࡆࠩိ"),
  bstack111l1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧီ"): bstack111l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡈࡕࡊࡎࡇࡣࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒࠨု"),
  bstack111l1_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧူ"): bstack111l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡃࡕࡅࡑࡒࡅࡍࡕࡢࡔࡊࡘ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࠩေ"),
  bstack111l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ဲ"): bstack111l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡏࡓࡈࡇࡌࠨဳ"),
  bstack111l1_opy_ (u"ࠫࡷ࡫ࡲࡶࡰࡗࡩࡸࡺࡳࠨဴ"): bstack111l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡗࡋࡒࡖࡐࡢࡘࡊ࡙ࡔࡔࠩဵ"),
  bstack111l1_opy_ (u"࠭ࡡࡱࡲࠪံ"): [bstack111l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡑࡒࡢࡍࡉ့࠭"), bstack111l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡒࡓࠫး")],
  bstack111l1_opy_ (u"ࠩ࡯ࡳ࡬ࡒࡥࡷࡧ࡯္ࠫ"): bstack111l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡖࡈࡐࡥࡌࡐࡉࡏࡉ࡛ࡋࡌࠨ်"),
  bstack111l1_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨျ"): bstack111l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࠨြ"),
  bstack111l1_opy_ (u"࠭ࡴࡦࡵࡷࡓࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪွ"): bstack111l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡔࡈࡓࡆࡔ࡙ࡅࡇࡏࡌࡊࡖ࡜ࠫှ")
}
bstack1ll1l11l1_opy_ = {
  bstack111l1_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪဿ"): [bstack111l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡷࡶࡩࡷࡥ࡮ࡢ࡯ࡨࠫ၀"), bstack111l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡸࡷࡪࡸࡎࡢ࡯ࡨࠫ၁")],
  bstack111l1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧ၂"): [bstack111l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶࡣࡰ࡫ࡹࠨ၃"), bstack111l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨ၄")],
  bstack111l1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪ၅"): bstack111l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪ၆"),
  bstack111l1_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧ၇"): bstack111l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧ၈"),
  bstack111l1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭၉"): bstack111l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭၊"),
  bstack111l1_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭။"): [bstack111l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡰࡱࡲࠪ၌"), bstack111l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ၍")],
  bstack111l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭၎"): bstack111l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡯ࡳࡨࡧ࡬ࠨ၏"),
  bstack111l1_opy_ (u"ࠫࡷ࡫ࡲࡶࡰࡗࡩࡸࡺࡳࠨၐ"): bstack111l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡷ࡫ࡲࡶࡰࡗࡩࡸࡺࡳࠨၑ"),
  bstack111l1_opy_ (u"࠭ࡡࡱࡲࠪၒ"): bstack111l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡱࡲࠪၓ"),
  bstack111l1_opy_ (u"ࠨ࡮ࡲ࡫ࡑ࡫ࡶࡦ࡮ࠪၔ"): bstack111l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡮ࡲ࡫ࡑ࡫ࡶࡦ࡮ࠪၕ"),
  bstack111l1_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧၖ"): bstack111l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧၗ")
}
bstack1ll11ll1ll_opy_ = {
  bstack111l1_opy_ (u"ࠬࡵࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠨၘ"): bstack111l1_opy_ (u"࠭࡯ࡴࡡࡹࡩࡷࡹࡩࡰࡰࠪၙ"),
  bstack111l1_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩၚ"): [bstack111l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡡࡹࡩࡷࡹࡩࡰࡰࠪၛ"), bstack111l1_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬၜ")],
  bstack111l1_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨၝ"): bstack111l1_opy_ (u"ࠫࡳࡧ࡭ࡦࠩၞ"),
  bstack111l1_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡓࡧ࡭ࡦࠩၟ"): bstack111l1_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪ࠭ၠ"),
  bstack111l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬၡ"): [bstack111l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࠩၢ"), bstack111l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡲࡦࡳࡥࠨၣ")],
  bstack111l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫၤ"): bstack111l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ၥ"),
  bstack111l1_opy_ (u"ࠬࡸࡥࡢ࡮ࡐࡳࡧ࡯࡬ࡦࠩၦ"): bstack111l1_opy_ (u"࠭ࡲࡦࡣ࡯ࡣࡲࡵࡢࡪ࡮ࡨࠫၧ"),
  bstack111l1_opy_ (u"ࠧࡢࡲࡳ࡭ࡺࡳࡖࡦࡴࡶ࡭ࡴࡴࠧၨ"): [bstack111l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡲࡳ࡭ࡺࡳ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨၩ"), bstack111l1_opy_ (u"ࠩࡤࡴࡵ࡯ࡵ࡮ࡡࡹࡩࡷࡹࡩࡰࡰࠪၪ")],
  bstack111l1_opy_ (u"ࠪࡥࡨࡩࡥࡱࡶࡌࡲࡸ࡫ࡣࡶࡴࡨࡇࡪࡸࡴࡴࠩၫ"): [bstack111l1_opy_ (u"ࠫࡦࡩࡣࡦࡲࡷࡗࡸࡲࡃࡦࡴࡷࡷࠬၬ"), bstack111l1_opy_ (u"ࠬࡧࡣࡤࡧࡳࡸࡘࡹ࡬ࡄࡧࡵࡸࠬၭ")]
}
bstack1ll111ll1_opy_ = [
  bstack111l1_opy_ (u"࠭ࡡࡤࡥࡨࡴࡹࡏ࡮ࡴࡧࡦࡹࡷ࡫ࡃࡦࡴࡷࡷࠬၮ"),
  bstack111l1_opy_ (u"ࠧࡱࡣࡪࡩࡑࡵࡡࡥࡕࡷࡶࡦࡺࡥࡨࡻࠪၯ"),
  bstack111l1_opy_ (u"ࠨࡲࡵࡳࡽࡿࠧၰ"),
  bstack111l1_opy_ (u"ࠩࡶࡩࡹ࡝ࡩ࡯ࡦࡲࡻࡗ࡫ࡣࡵࠩၱ"),
  bstack111l1_opy_ (u"ࠪࡸ࡮ࡳࡥࡰࡷࡷࡷࠬၲ"),
  bstack111l1_opy_ (u"ࠫࡸࡺࡲࡪࡥࡷࡊ࡮ࡲࡥࡊࡰࡷࡩࡷࡧࡣࡵࡣࡥ࡭ࡱ࡯ࡴࡺࠩၳ"),
  bstack111l1_opy_ (u"ࠬࡻ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡑࡴࡲࡱࡵࡺࡂࡦࡪࡤࡺ࡮ࡵࡲࠨၴ"),
  bstack111l1_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫၵ"),
  bstack111l1_opy_ (u"ࠧ࡮ࡱࡽ࠾࡫࡯ࡲࡦࡨࡲࡼࡔࡶࡴࡪࡱࡱࡷࠬၶ"),
  bstack111l1_opy_ (u"ࠨ࡯ࡶ࠾ࡪࡪࡧࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩၷ"),
  bstack111l1_opy_ (u"ࠩࡶࡩ࠿࡯ࡥࡐࡲࡷ࡭ࡴࡴࡳࠨၸ"),
  bstack111l1_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫࠱ࡳࡵࡺࡩࡰࡰࡶࠫၹ"),
]
bstack11l1l1111_opy_ = [
  bstack111l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨၺ"),
  bstack111l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩၻ"),
  bstack111l1_opy_ (u"࠭࡬ࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬၼ"),
  bstack111l1_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧၽ"),
  bstack111l1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫၾ"),
  bstack111l1_opy_ (u"ࠩ࡯ࡳ࡬ࡒࡥࡷࡧ࡯ࠫၿ"),
  bstack111l1_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭ႀ"),
  bstack111l1_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨႁ"),
  bstack111l1_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨႂ"),
  bstack111l1_opy_ (u"࠭ࡴࡦࡵࡷࡇࡴࡴࡴࡦࡺࡷࡓࡵࡺࡩࡰࡰࡶࠫႃ"),
  bstack111l1_opy_ (u"ࠧࡵࡧࡶࡸࡔࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫႄ"),
  bstack111l1_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡗࡣࡵ࡭ࡦࡨ࡬ࡦࡵࠪႅ"),
  bstack111l1_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡖࡤ࡫ࠬႆ"),
  bstack111l1_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧႇ"),
  bstack111l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ႈ"),
  bstack111l1_opy_ (u"ࠬࡸࡥࡳࡷࡱࡘࡪࡹࡴࡴࠩႉ"),
  bstack111l1_opy_ (u"࠭ࡃࡖࡕࡗࡓࡒࡥࡔࡂࡉࡢ࠵ࠬႊ"),
  bstack111l1_opy_ (u"ࠧࡄࡗࡖࡘࡔࡓ࡟ࡕࡃࡊࡣ࠷࠭ႋ"),
  bstack111l1_opy_ (u"ࠨࡅࡘࡗ࡙ࡕࡍࡠࡖࡄࡋࡤ࠹ࠧႌ"),
  bstack111l1_opy_ (u"ࠩࡆ࡙ࡘ࡚ࡏࡎࡡࡗࡅࡌࡥ࠴ࠨႍ"),
  bstack111l1_opy_ (u"ࠪࡇ࡚࡙ࡔࡐࡏࡢࡘࡆࡍ࡟࠶ࠩႎ"),
  bstack111l1_opy_ (u"ࠫࡈ࡛ࡓࡕࡑࡐࡣ࡙ࡇࡇࡠ࠸ࠪႏ"),
  bstack111l1_opy_ (u"ࠬࡉࡕࡔࡖࡒࡑࡤ࡚ࡁࡈࡡ࠺ࠫ႐"),
  bstack111l1_opy_ (u"࠭ࡃࡖࡕࡗࡓࡒࡥࡔࡂࡉࡢ࠼ࠬ႑"),
  bstack111l1_opy_ (u"ࠧࡄࡗࡖࡘࡔࡓ࡟ࡕࡃࡊࡣ࠾࠭႒"),
  bstack111l1_opy_ (u"ࠨࡲࡨࡶࡨࡿࠧ႓"),
  bstack111l1_opy_ (u"ࠩࡳࡩࡷࡩࡹࡐࡲࡷ࡭ࡴࡴࡳࠨ႔"),
  bstack111l1_opy_ (u"ࠪࡴࡪࡸࡣࡺࡅࡤࡴࡹࡻࡲࡦࡏࡲࡨࡪ࠭႕"),
  bstack111l1_opy_ (u"ࠫࡩ࡯ࡳࡢࡤ࡯ࡩࡆࡻࡴࡰࡅࡤࡴࡹࡻࡲࡦࡎࡲ࡫ࡸ࠭႖")
]
bstack111ll1l111_opy_ = [
  bstack111l1_opy_ (u"ࠬࡻࡰ࡭ࡱࡤࡨࡒ࡫ࡤࡪࡣࠪ႗"),
  bstack111l1_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨ႘"),
  bstack111l1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪ႙"),
  bstack111l1_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ႚ"),
  bstack111l1_opy_ (u"ࠩࡷࡩࡸࡺࡐࡳ࡫ࡲࡶ࡮ࡺࡹࠨႛ"),
  bstack111l1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ႜ"),
  bstack111l1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡗࡥ࡬࠭ႝ"),
  bstack111l1_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠪ႞"),
  bstack111l1_opy_ (u"࠭ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨ႟"),
  bstack111l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬႠ"),
  bstack111l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩႡ"),
  bstack111l1_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࠨႢ"),
  bstack111l1_opy_ (u"ࠪࡳࡸ࠭Ⴃ"),
  bstack111l1_opy_ (u"ࠫࡴࡹࡖࡦࡴࡶ࡭ࡴࡴࠧႤ"),
  bstack111l1_opy_ (u"ࠬ࡮࡯ࡴࡶࡶࠫႥ"),
  bstack111l1_opy_ (u"࠭ࡡࡶࡶࡲ࡛ࡦ࡯ࡴࠨႦ"),
  bstack111l1_opy_ (u"ࠧࡳࡧࡪ࡭ࡴࡴࠧႧ"),
  bstack111l1_opy_ (u"ࠨࡶ࡬ࡱࡪࢀ࡯࡯ࡧࠪႨ"),
  bstack111l1_opy_ (u"ࠩࡰࡥࡨ࡮ࡩ࡯ࡧࠪႩ"),
  bstack111l1_opy_ (u"ࠪࡶࡪࡹ࡯࡭ࡷࡷ࡭ࡴࡴࠧႪ"),
  bstack111l1_opy_ (u"ࠫ࡮ࡪ࡬ࡦࡖ࡬ࡱࡪࡵࡵࡵࠩႫ"),
  bstack111l1_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡔࡸࡩࡦࡰࡷࡥࡹ࡯࡯࡯ࠩႬ"),
  bstack111l1_opy_ (u"࠭ࡶࡪࡦࡨࡳࠬႭ"),
  bstack111l1_opy_ (u"ࠧ࡯ࡱࡓࡥ࡬࡫ࡌࡰࡣࡧࡘ࡮ࡳࡥࡰࡷࡷࠫႮ"),
  bstack111l1_opy_ (u"ࠨࡤࡩࡧࡦࡩࡨࡦࠩႯ"),
  bstack111l1_opy_ (u"ࠩࡧࡩࡧࡻࡧࠨႰ"),
  bstack111l1_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡖࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࡹࠧႱ"),
  bstack111l1_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡗࡪࡴࡤࡌࡧࡼࡷࠬႲ"),
  bstack111l1_opy_ (u"ࠬࡸࡥࡢ࡮ࡐࡳࡧ࡯࡬ࡦࠩႳ"),
  bstack111l1_opy_ (u"࠭࡮ࡰࡒ࡬ࡴࡪࡲࡩ࡯ࡧࠪႴ"),
  bstack111l1_opy_ (u"ࠧࡤࡪࡨࡧࡰ࡛ࡒࡍࠩႵ"),
  bstack111l1_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪႶ"),
  bstack111l1_opy_ (u"ࠩࡤࡧࡨ࡫ࡰࡵࡅࡲࡳࡰ࡯ࡥࡴࠩႷ"),
  bstack111l1_opy_ (u"ࠪࡧࡦࡶࡴࡶࡴࡨࡇࡷࡧࡳࡩࠩႸ"),
  bstack111l1_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠨႹ"),
  bstack111l1_opy_ (u"ࠬࡧࡰࡱ࡫ࡸࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬႺ"),
  bstack111l1_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰ࡙ࡩࡷࡹࡩࡰࡰࠪႻ"),
  bstack111l1_opy_ (u"ࠧ࡯ࡱࡅࡰࡦࡴ࡫ࡑࡱ࡯ࡰ࡮ࡴࡧࠨႼ"),
  bstack111l1_opy_ (u"ࠨ࡯ࡤࡷࡰ࡙ࡥ࡯ࡦࡎࡩࡾࡹࠧႽ"),
  bstack111l1_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡎࡲ࡫ࡸ࠭Ⴞ"),
  bstack111l1_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡌࡨࠬႿ"),
  bstack111l1_opy_ (u"ࠫࡩ࡫ࡤࡪࡥࡤࡸࡪࡪࡄࡦࡸ࡬ࡧࡪ࠭Ⴠ"),
  bstack111l1_opy_ (u"ࠬ࡮ࡥࡢࡦࡨࡶࡕࡧࡲࡢ࡯ࡶࠫჁ"),
  bstack111l1_opy_ (u"࠭ࡰࡩࡱࡱࡩࡓࡻ࡭ࡣࡧࡵࠫჂ"),
  bstack111l1_opy_ (u"ࠧ࡯ࡧࡷࡻࡴࡸ࡫ࡍࡱࡪࡷࠬჃ"),
  bstack111l1_opy_ (u"ࠨࡰࡨࡸࡼࡵࡲ࡬ࡎࡲ࡫ࡸࡕࡰࡵ࡫ࡲࡲࡸ࠭Ⴤ"),
  bstack111l1_opy_ (u"ࠩࡦࡳࡳࡹ࡯࡭ࡧࡏࡳ࡬ࡹࠧჅ"),
  bstack111l1_opy_ (u"ࠪࡹࡸ࡫ࡗ࠴ࡅࠪ჆"),
  bstack111l1_opy_ (u"ࠫࡦࡶࡰࡪࡷࡰࡐࡴ࡭ࡳࠨჇ"),
  bstack111l1_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡇ࡯࡯࡮ࡧࡷࡶ࡮ࡩࠧ჈"),
  bstack111l1_opy_ (u"࠭ࡶࡪࡦࡨࡳ࡛࠸ࠧ჉"),
  bstack111l1_opy_ (u"ࠧ࡮࡫ࡧࡗࡪࡹࡳࡪࡱࡱࡍࡳࡹࡴࡢ࡮࡯ࡅࡵࡶࡳࠨ჊"),
  bstack111l1_opy_ (u"ࠨࡧࡶࡴࡷ࡫ࡳࡴࡱࡖࡩࡷࡼࡥࡳࠩ჋"),
  bstack111l1_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰࡐࡴ࡭ࡳࠨ჌"),
  bstack111l1_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱࡈࡪࡰࠨჍ"),
  bstack111l1_opy_ (u"ࠫࡹ࡫࡬ࡦ࡯ࡨࡸࡷࡿࡌࡰࡩࡶࠫ჎"),
  bstack111l1_opy_ (u"ࠬࡹࡹ࡯ࡥࡗ࡭ࡲ࡫ࡗࡪࡶ࡫ࡒ࡙ࡖࠧ჏"),
  bstack111l1_opy_ (u"࠭ࡧࡦࡱࡏࡳࡨࡧࡴࡪࡱࡱࠫა"),
  bstack111l1_opy_ (u"ࠧࡨࡲࡶࡐࡴࡩࡡࡵ࡫ࡲࡲࠬბ"),
  bstack111l1_opy_ (u"ࠨࡰࡨࡸࡼࡵࡲ࡬ࡒࡵࡳ࡫࡯࡬ࡦࠩგ"),
  bstack111l1_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡐࡨࡸࡼࡵࡲ࡬ࠩდ"),
  bstack111l1_opy_ (u"ࠪࡪࡴࡸࡣࡦࡅ࡫ࡥࡳ࡭ࡥࡋࡣࡵࠫე"),
  bstack111l1_opy_ (u"ࠫࡽࡳࡳࡋࡣࡵࠫვ"),
  bstack111l1_opy_ (u"ࠬࡾ࡭ࡹࡌࡤࡶࠬზ"),
  bstack111l1_opy_ (u"࠭࡭ࡢࡵ࡮ࡇࡴࡳ࡭ࡢࡰࡧࡷࠬთ"),
  bstack111l1_opy_ (u"ࠧ࡮ࡣࡶ࡯ࡇࡧࡳࡪࡥࡄࡹࡹ࡮ࠧი"),
  bstack111l1_opy_ (u"ࠨࡹࡶࡐࡴࡩࡡ࡭ࡕࡸࡴࡵࡵࡲࡵࠩკ"),
  bstack111l1_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧࡆࡳࡷࡹࡒࡦࡵࡷࡶ࡮ࡩࡴࡪࡱࡱࡷࠬლ"),
  bstack111l1_opy_ (u"ࠪࡥࡵࡶࡖࡦࡴࡶ࡭ࡴࡴࠧმ"),
  bstack111l1_opy_ (u"ࠫࡦࡩࡣࡦࡲࡷࡍࡳࡹࡥࡤࡷࡵࡩࡈ࡫ࡲࡵࡵࠪნ"),
  bstack111l1_opy_ (u"ࠬࡸࡥࡴ࡫ࡪࡲࡆࡶࡰࠨო"),
  bstack111l1_opy_ (u"࠭ࡤࡪࡵࡤࡦࡱ࡫ࡁ࡯࡫ࡰࡥࡹ࡯࡯࡯ࡵࠪპ"),
  bstack111l1_opy_ (u"ࠧࡤࡣࡱࡥࡷࡿࠧჟ"),
  bstack111l1_opy_ (u"ࠨࡨ࡬ࡶࡪ࡬࡯ࡹࠩრ"),
  bstack111l1_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࠩს"),
  bstack111l1_opy_ (u"ࠪ࡭ࡪ࠭ტ"),
  bstack111l1_opy_ (u"ࠫࡪࡪࡧࡦࠩუ"),
  bstack111l1_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭ࠬფ"),
  bstack111l1_opy_ (u"࠭ࡱࡶࡧࡸࡩࠬქ"),
  bstack111l1_opy_ (u"ࠧࡪࡰࡷࡩࡷࡴࡡ࡭ࠩღ"),
  bstack111l1_opy_ (u"ࠨࡣࡳࡴࡘࡺ࡯ࡳࡧࡆࡳࡳ࡬ࡩࡨࡷࡵࡥࡹ࡯࡯࡯ࠩყ"),
  bstack111l1_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡅࡤࡱࡪࡸࡡࡊ࡯ࡤ࡫ࡪࡏ࡮࡫ࡧࡦࡸ࡮ࡵ࡮ࠨშ"),
  bstack111l1_opy_ (u"ࠪࡲࡪࡺࡷࡰࡴ࡮ࡐࡴ࡭ࡳࡆࡺࡦࡰࡺࡪࡥࡉࡱࡶࡸࡸ࠭ჩ"),
  bstack111l1_opy_ (u"ࠫࡳ࡫ࡴࡸࡱࡵ࡯ࡑࡵࡧࡴࡋࡱࡧࡱࡻࡤࡦࡊࡲࡷࡹࡹࠧც"),
  bstack111l1_opy_ (u"ࠬࡻࡰࡥࡣࡷࡩࡆࡶࡰࡔࡧࡷࡸ࡮ࡴࡧࡴࠩძ"),
  bstack111l1_opy_ (u"࠭ࡲࡦࡵࡨࡶࡻ࡫ࡄࡦࡸ࡬ࡧࡪ࠭წ"),
  bstack111l1_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧჭ"),
  bstack111l1_opy_ (u"ࠨࡵࡨࡲࡩࡑࡥࡺࡵࠪხ"),
  bstack111l1_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡒࡤࡷࡸࡩ࡯ࡥࡧࠪჯ"),
  bstack111l1_opy_ (u"ࠪࡹࡵࡪࡡࡵࡧࡌࡳࡸࡊࡥࡷ࡫ࡦࡩࡘ࡫ࡴࡵ࡫ࡱ࡫ࡸ࠭ჰ"),
  bstack111l1_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡅࡺࡪࡩࡰࡋࡱ࡮ࡪࡩࡴࡪࡱࡱࠫჱ"),
  bstack111l1_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡆࡶࡰ࡭ࡧࡓࡥࡾ࠭ჲ"),
  bstack111l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࠧჳ"),
  bstack111l1_opy_ (u"ࠧࡸࡦ࡬ࡳࡘ࡫ࡲࡷ࡫ࡦࡩࠬჴ"),
  bstack111l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪჵ"),
  bstack111l1_opy_ (u"ࠩࡳࡶࡪࡼࡥ࡯ࡶࡆࡶࡴࡹࡳࡔ࡫ࡷࡩ࡙ࡸࡡࡤ࡭࡬ࡲ࡬࠭ჶ"),
  bstack111l1_opy_ (u"ࠪ࡬࡮࡭ࡨࡄࡱࡱࡸࡷࡧࡳࡵࠩჷ"),
  bstack111l1_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡔࡷ࡫ࡦࡦࡴࡨࡲࡨ࡫ࡳࠨჸ"),
  bstack111l1_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡘ࡯࡭ࠨჹ"),
  bstack111l1_opy_ (u"࠭ࡳࡪ࡯ࡒࡴࡹ࡯࡯࡯ࡵࠪჺ"),
  bstack111l1_opy_ (u"ࠧࡳࡧࡰࡳࡻ࡫ࡉࡐࡕࡄࡴࡵ࡙ࡥࡵࡶ࡬ࡲ࡬ࡹࡌࡰࡥࡤࡰ࡮ࢀࡡࡵ࡫ࡲࡲࠬ჻"),
  bstack111l1_opy_ (u"ࠨࡪࡲࡷࡹࡔࡡ࡮ࡧࠪჼ"),
  bstack111l1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫჽ"),
  bstack111l1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࠬჾ"),
  bstack111l1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡔࡡ࡮ࡧࠪჿ"),
  bstack111l1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠧᄀ"),
  bstack111l1_opy_ (u"࠭ࡰࡢࡩࡨࡐࡴࡧࡤࡔࡶࡵࡥࡹ࡫ࡧࡺࠩᄁ"),
  bstack111l1_opy_ (u"ࠧࡱࡴࡲࡼࡾ࠭ᄂ"),
  bstack111l1_opy_ (u"ࠨࡶ࡬ࡱࡪࡵࡵࡵࡵࠪᄃ"),
  bstack111l1_opy_ (u"ࠩࡸࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࡕࡸ࡯࡮ࡲࡷࡆࡪ࡮ࡡࡷ࡫ࡲࡶࠬᄄ")
]
bstack111ll1l11_opy_ = {
  bstack111l1_opy_ (u"ࠪࡺࠬᄅ"): bstack111l1_opy_ (u"ࠫࡻ࠭ᄆ"),
  bstack111l1_opy_ (u"ࠬ࡬ࠧᄇ"): bstack111l1_opy_ (u"࠭ࡦࠨᄈ"),
  bstack111l1_opy_ (u"ࠧࡧࡱࡵࡧࡪ࠭ᄉ"): bstack111l1_opy_ (u"ࠨࡨࡲࡶࡨ࡫ࠧᄊ"),
  bstack111l1_opy_ (u"ࠩࡲࡲࡱࡿࡡࡶࡶࡲࡱࡦࡺࡥࠨᄋ"): bstack111l1_opy_ (u"ࠪࡳࡳࡲࡹࡂࡷࡷࡳࡲࡧࡴࡦࠩᄌ"),
  bstack111l1_opy_ (u"ࠫ࡫ࡵࡲࡤࡧ࡯ࡳࡨࡧ࡬ࠨᄍ"): bstack111l1_opy_ (u"ࠬ࡬࡯ࡳࡥࡨࡰࡴࡩࡡ࡭ࠩᄎ"),
  bstack111l1_opy_ (u"࠭ࡰࡳࡱࡻࡽ࡭ࡵࡳࡵࠩᄏ"): bstack111l1_opy_ (u"ࠧࡱࡴࡲࡼࡾࡎ࡯ࡴࡶࠪᄐ"),
  bstack111l1_opy_ (u"ࠨࡲࡵࡳࡽࡿࡰࡰࡴࡷࠫᄑ"): bstack111l1_opy_ (u"ࠩࡳࡶࡴࡾࡹࡑࡱࡵࡸࠬᄒ"),
  bstack111l1_opy_ (u"ࠪࡴࡷࡵࡸࡺࡷࡶࡩࡷ࠭ᄓ"): bstack111l1_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡘࡷࡪࡸࠧᄔ"),
  bstack111l1_opy_ (u"ࠬࡶࡲࡰࡺࡼࡴࡦࡹࡳࠨᄕ"): bstack111l1_opy_ (u"࠭ࡰࡳࡱࡻࡽࡕࡧࡳࡴࠩᄖ"),
  bstack111l1_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡶࡲࡰࡺࡼ࡬ࡴࡹࡴࠨᄗ"): bstack111l1_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡐࡳࡱࡻࡽࡍࡵࡳࡵࠩᄘ"),
  bstack111l1_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡱࡴࡲࡼࡾࡶ࡯ࡳࡶࠪᄙ"): bstack111l1_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡒࡵࡳࡽࡿࡐࡰࡴࡷࠫᄚ"),
  bstack111l1_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡳࡶࡴࡾࡹࡶࡵࡨࡶࠬᄛ"): bstack111l1_opy_ (u"ࠬ࠳࡬ࡰࡥࡤࡰࡕࡸ࡯ࡹࡻࡘࡷࡪࡸࠧᄜ"),
  bstack111l1_opy_ (u"࠭࠭࡭ࡱࡦࡥࡱࡶࡲࡰࡺࡼࡹࡸ࡫ࡲࠨᄝ"): bstack111l1_opy_ (u"ࠧ࠮࡮ࡲࡧࡦࡲࡐࡳࡱࡻࡽ࡚ࡹࡥࡳࠩᄞ"),
  bstack111l1_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡰࡳࡱࡻࡽࡵࡧࡳࡴࠩᄟ"): bstack111l1_opy_ (u"ࠩ࠰ࡰࡴࡩࡡ࡭ࡒࡵࡳࡽࡿࡐࡢࡵࡶࠫᄠ"),
  bstack111l1_opy_ (u"ࠪ࠱ࡱࡵࡣࡢ࡮ࡳࡶࡴࡾࡹࡱࡣࡶࡷࠬᄡ"): bstack111l1_opy_ (u"ࠫ࠲ࡲ࡯ࡤࡣ࡯ࡔࡷࡵࡸࡺࡒࡤࡷࡸ࠭ᄢ"),
  bstack111l1_opy_ (u"ࠬࡨࡩ࡯ࡣࡵࡽࡵࡧࡴࡩࠩᄣ"): bstack111l1_opy_ (u"࠭ࡢࡪࡰࡤࡶࡾࡶࡡࡵࡪࠪᄤ"),
  bstack111l1_opy_ (u"ࠧࡱࡣࡦࡪ࡮ࡲࡥࠨᄥ"): bstack111l1_opy_ (u"ࠨ࠯ࡳࡥࡨ࠳ࡦࡪ࡮ࡨࠫᄦ"),
  bstack111l1_opy_ (u"ࠩࡳࡥࡨ࠳ࡦࡪ࡮ࡨࠫᄧ"): bstack111l1_opy_ (u"ࠪ࠱ࡵࡧࡣ࠮ࡨ࡬ࡰࡪ࠭ᄨ"),
  bstack111l1_opy_ (u"ࠫ࠲ࡶࡡࡤ࠯ࡩ࡭ࡱ࡫ࠧᄩ"): bstack111l1_opy_ (u"ࠬ࠳ࡰࡢࡥ࠰ࡪ࡮ࡲࡥࠨᄪ"),
  bstack111l1_opy_ (u"࠭࡬ࡰࡩࡩ࡭ࡱ࡫ࠧᄫ"): bstack111l1_opy_ (u"ࠧ࡭ࡱࡪࡪ࡮ࡲࡥࠨᄬ"),
  bstack111l1_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪᄭ"): bstack111l1_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫᄮ"),
}
bstack111ll11l11_opy_ = bstack111l1_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳࡬࡯ࡴࡩࡷࡥ࠲ࡨࡵ࡭࠰ࡲࡨࡶࡨࡿ࠯ࡤ࡮࡬࠳ࡷ࡫࡬ࡦࡣࡶࡩࡸ࠵࡬ࡢࡶࡨࡷࡹ࠵ࡤࡰࡹࡱࡰࡴࡧࡤࠣᄯ")
bstack111ll11ll1_opy_ = bstack111l1_opy_ (u"ࠦ࠴ࡶࡥࡳࡥࡼ࠳࡭࡫ࡡ࡭ࡶ࡫ࡧ࡭࡫ࡣ࡬ࠤᄰ")
bstack11l1lllll_opy_ = bstack111l1_opy_ (u"ࠬ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡨࡶࡤ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡷࡥ࠱࡫ࡹࡧ࠭ᄱ")
bstack1lll1lll11_opy_ = bstack111l1_opy_ (u"࠭ࡨࡵࡶࡳ࠾࠴࠵ࡨࡶࡤ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲࡀ࠸࠱࠱ࡺࡨ࠴࡮ࡵࡣࠩᄲ")
bstack1ll1l1l11_opy_ = bstack111l1_opy_ (u"ࠧࡩࡶࡷࡴࡸࡀ࠯࠰ࡪࡸࡦ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡰࡨࡼࡹࡥࡨࡶࡤࡶࠫᄳ")
bstack111l1lllll_opy_ = {
  bstack111l1_opy_ (u"ࠨࡥࡵ࡭ࡹ࡯ࡣࡢ࡮ࠪᄴ"): 50,
  bstack111l1_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨᄵ"): 40,
  bstack111l1_opy_ (u"ࠪࡻࡦࡸ࡮ࡪࡰࡪࠫᄶ"): 30,
  bstack111l1_opy_ (u"ࠫ࡮ࡴࡦࡰࠩᄷ"): 20,
  bstack111l1_opy_ (u"ࠬࡪࡥࡣࡷࡪࠫᄸ"): 10
}
bstack1l1111ll1l_opy_ = bstack111l1lllll_opy_[bstack111l1_opy_ (u"࠭ࡩ࡯ࡨࡲࠫᄹ")]
bstack1l11111l_opy_ = bstack111l1_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴ࠭ࡱࡻࡷ࡬ࡴࡴࡡࡨࡧࡱࡸ࠴࠭ᄺ")
bstack1111ll1ll_opy_ = bstack111l1_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡱࡻࡷ࡬ࡴࡴࡡࡨࡧࡱࡸ࠴࠭ᄻ")
bstack1l11ll11_opy_ = bstack111l1_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦ࠯ࡳࡽࡹ࡮࡯࡯ࡣࡪࡩࡳࡺ࠯ࠨᄼ")
bstack111l1l111_opy_ = bstack111l1_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶ࠰ࡴࡾࡺࡨࡰࡰࡤ࡫ࡪࡴࡴ࠰ࠩᄽ")
bstack1llll1l11l_opy_ = bstack111l1_opy_ (u"ࠫࡕࡲࡥࡢࡵࡨࠤ࡮ࡴࡳࡵࡣ࡯ࡰࠥࡶࡹࡵࡧࡶࡸࠥࡧ࡮ࡥࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡶࡩࡱ࡫࡮ࡪࡷࡰࠤࡵࡧࡣ࡬ࡣࡪࡩࡸ࠴ࠠࡡࡲ࡬ࡴࠥ࡯࡮ࡴࡶࡤࡰࡱࠦࡰࡺࡶࡨࡷࡹࠦࡰࡺࡶࡨࡷࡹ࠳ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡡࠩᄾ")
bstack111ll111l1_opy_ = [bstack111l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡚࡙ࡅࡓࡐࡄࡑࡊ࠭ᄿ"), bstack111l1_opy_ (u"࡙࠭ࡐࡗࡕࡣ࡚࡙ࡅࡓࡐࡄࡑࡊ࠭ᅀ")]
bstack111ll11111_opy_ = [bstack111l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡄࡅࡈࡗࡘࡥࡋࡆ࡛ࠪᅁ"), bstack111l1_opy_ (u"ࠨ࡛ࡒ࡙ࡗࡥࡁࡄࡅࡈࡗࡘࡥࡋࡆ࡛ࠪᅂ")]
bstack11l1l1l1l_opy_ = re.compile(bstack111l1_opy_ (u"ࠩࡡ࡟ࡡࡢࡷ࠮࡟࠮࠾࠳࠰ࠤࠨᅃ"))
bstack1ll1l1l111_opy_ = [
  bstack111l1_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࡎࡢ࡯ࡨࠫᅄ"),
  bstack111l1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᅅ"),
  bstack111l1_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡓࡧ࡭ࡦࠩᅆ"),
  bstack111l1_opy_ (u"࠭࡮ࡦࡹࡆࡳࡲࡳࡡ࡯ࡦࡗ࡭ࡲ࡫࡯ࡶࡶࠪᅇ"),
  bstack111l1_opy_ (u"ࠧࡢࡲࡳࠫᅈ"),
  bstack111l1_opy_ (u"ࠨࡷࡧ࡭ࡩ࠭ᅉ"),
  bstack111l1_opy_ (u"ࠩ࡯ࡥࡳ࡭ࡵࡢࡩࡨࠫᅊ"),
  bstack111l1_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡧࠪᅋ"),
  bstack111l1_opy_ (u"ࠫࡴࡸࡩࡦࡰࡷࡥࡹ࡯࡯࡯ࠩᅌ"),
  bstack111l1_opy_ (u"ࠬࡧࡵࡵࡱ࡚ࡩࡧࡼࡩࡦࡹࠪᅍ"),
  bstack111l1_opy_ (u"࠭࡮ࡰࡔࡨࡷࡪࡺࠧᅎ"), bstack111l1_opy_ (u"ࠧࡧࡷ࡯ࡰࡗ࡫ࡳࡦࡶࠪᅏ"),
  bstack111l1_opy_ (u"ࠨࡥ࡯ࡩࡦࡸࡓࡺࡵࡷࡩࡲࡌࡩ࡭ࡧࡶࠫᅐ"),
  bstack111l1_opy_ (u"ࠩࡨࡺࡪࡴࡴࡕ࡫ࡰ࡭ࡳ࡭ࡳࠨᅑ"),
  bstack111l1_opy_ (u"ࠪࡩࡳࡧࡢ࡭ࡧࡓࡩࡷ࡬࡯ࡳ࡯ࡤࡲࡨ࡫ࡌࡰࡩࡪ࡭ࡳ࡭ࠧᅒ"),
  bstack111l1_opy_ (u"ࠫࡴࡺࡨࡦࡴࡄࡴࡵࡹࠧᅓ"),
  bstack111l1_opy_ (u"ࠬࡶࡲࡪࡰࡷࡔࡦ࡭ࡥࡔࡱࡸࡶࡨ࡫ࡏ࡯ࡈ࡬ࡲࡩࡌࡡࡪ࡮ࡸࡶࡪ࠭ᅔ"),
  bstack111l1_opy_ (u"࠭ࡡࡱࡲࡄࡧࡹ࡯ࡶࡪࡶࡼࠫᅕ"), bstack111l1_opy_ (u"ࠧࡢࡲࡳࡔࡦࡩ࡫ࡢࡩࡨࠫᅖ"), bstack111l1_opy_ (u"ࠨࡣࡳࡴ࡜ࡧࡩࡵࡃࡦࡸ࡮ࡼࡩࡵࡻࠪᅗ"), bstack111l1_opy_ (u"ࠩࡤࡴࡵ࡝ࡡࡪࡶࡓࡥࡨࡱࡡࡨࡧࠪᅘ"), bstack111l1_opy_ (u"ࠪࡥࡵࡶࡗࡢ࡫ࡷࡈࡺࡸࡡࡵ࡫ࡲࡲࠬᅙ"),
  bstack111l1_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡖࡪࡧࡤࡺࡖ࡬ࡱࡪࡵࡵࡵࠩᅚ"),
  bstack111l1_opy_ (u"ࠬࡧ࡬࡭ࡱࡺࡘࡪࡹࡴࡑࡣࡦ࡯ࡦ࡭ࡥࡴࠩᅛ"),
  bstack111l1_opy_ (u"࠭ࡡ࡯ࡦࡵࡳ࡮ࡪࡃࡰࡸࡨࡶࡦ࡭ࡥࠨᅜ"), bstack111l1_opy_ (u"ࠧࡢࡰࡧࡶࡴ࡯ࡤࡄࡱࡹࡩࡷࡧࡧࡦࡇࡱࡨࡎࡴࡴࡦࡰࡷࠫᅝ"),
  bstack111l1_opy_ (u"ࠨࡣࡱࡨࡷࡵࡩࡥࡆࡨࡺ࡮ࡩࡥࡓࡧࡤࡨࡾ࡚ࡩ࡮ࡧࡲࡹࡹ࠭ᅞ"),
  bstack111l1_opy_ (u"ࠩࡤࡨࡧࡖ࡯ࡳࡶࠪᅟ"),
  bstack111l1_opy_ (u"ࠪࡥࡳࡪࡲࡰ࡫ࡧࡈࡪࡼࡩࡤࡧࡖࡳࡨࡱࡥࡵࠩᅠ"),
  bstack111l1_opy_ (u"ࠫࡦࡴࡤࡳࡱ࡬ࡨࡎࡴࡳࡵࡣ࡯ࡰ࡙࡯࡭ࡦࡱࡸࡸࠬᅡ"),
  bstack111l1_opy_ (u"ࠬࡧ࡮ࡥࡴࡲ࡭ࡩࡏ࡮ࡴࡶࡤࡰࡱࡖࡡࡵࡪࠪᅢ"),
  bstack111l1_opy_ (u"࠭ࡡࡷࡦࠪᅣ"), bstack111l1_opy_ (u"ࠧࡢࡸࡧࡐࡦࡻ࡮ࡤࡪࡗ࡭ࡲ࡫࡯ࡶࡶࠪᅤ"), bstack111l1_opy_ (u"ࠨࡣࡹࡨࡗ࡫ࡡࡥࡻࡗ࡭ࡲ࡫࡯ࡶࡶࠪᅥ"), bstack111l1_opy_ (u"ࠩࡤࡺࡩࡇࡲࡨࡵࠪᅦ"),
  bstack111l1_opy_ (u"ࠪࡹࡸ࡫ࡋࡦࡻࡶࡸࡴࡸࡥࠨᅧ"), bstack111l1_opy_ (u"ࠫࡰ࡫ࡹࡴࡶࡲࡶࡪࡖࡡࡵࡪࠪᅨ"), bstack111l1_opy_ (u"ࠬࡱࡥࡺࡵࡷࡳࡷ࡫ࡐࡢࡵࡶࡻࡴࡸࡤࠨᅩ"),
  bstack111l1_opy_ (u"࠭࡫ࡦࡻࡄࡰ࡮ࡧࡳࠨᅪ"), bstack111l1_opy_ (u"ࠧ࡬ࡧࡼࡔࡦࡹࡳࡸࡱࡵࡨࠬᅫ"),
  bstack111l1_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࡥࡴ࡬ࡺࡪࡸࡅࡹࡧࡦࡹࡹࡧࡢ࡭ࡧࠪᅬ"), bstack111l1_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࡦࡵ࡭ࡻ࡫ࡲࡂࡴࡪࡷࠬᅭ"), bstack111l1_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࡧࡶ࡮ࡼࡥࡳࡇࡻࡩࡨࡻࡴࡢࡤ࡯ࡩࡉ࡯ࡲࠨᅮ"), bstack111l1_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࡨࡷ࡯ࡶࡦࡴࡆ࡬ࡷࡵ࡭ࡦࡏࡤࡴࡵ࡯࡮ࡨࡈ࡬ࡰࡪ࠭ᅯ"), bstack111l1_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡩࡸࡩࡷࡧࡵ࡙ࡸ࡫ࡓࡺࡵࡷࡩࡲࡋࡸࡦࡥࡸࡸࡦࡨ࡬ࡦࠩᅰ"),
  bstack111l1_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪࡪࡲࡪࡸࡨࡶࡕࡵࡲࡵࠩᅱ"), bstack111l1_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࡤࡳ࡫ࡹࡩࡷࡖ࡯ࡳࡶࡶࠫᅲ"),
  bstack111l1_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࡥࡴ࡬ࡺࡪࡸࡄࡪࡵࡤࡦࡱ࡫ࡂࡶ࡫࡯ࡨࡈ࡮ࡥࡤ࡭ࠪᅳ"),
  bstack111l1_opy_ (u"ࠩࡤࡹࡹࡵࡗࡦࡤࡹ࡭ࡪࡽࡔࡪ࡯ࡨࡳࡺࡺࠧᅴ"),
  bstack111l1_opy_ (u"ࠪ࡭ࡳࡺࡥ࡯ࡶࡄࡧࡹ࡯࡯࡯ࠩᅵ"), bstack111l1_opy_ (u"ࠫ࡮ࡴࡴࡦࡰࡷࡇࡦࡺࡥࡨࡱࡵࡽࠬᅶ"), bstack111l1_opy_ (u"ࠬ࡯࡮ࡵࡧࡱࡸࡋࡲࡡࡨࡵࠪᅷ"), bstack111l1_opy_ (u"࠭࡯ࡱࡶ࡬ࡳࡳࡧ࡬ࡊࡰࡷࡩࡳࡺࡁࡳࡩࡸࡱࡪࡴࡴࡴࠩᅸ"),
  bstack111l1_opy_ (u"ࠧࡥࡱࡱࡸࡘࡺ࡯ࡱࡃࡳࡴࡔࡴࡒࡦࡵࡨࡸࠬᅹ"),
  bstack111l1_opy_ (u"ࠨࡷࡱ࡭ࡨࡵࡤࡦࡍࡨࡽࡧࡵࡡࡳࡦࠪᅺ"), bstack111l1_opy_ (u"ࠩࡵࡩࡸ࡫ࡴࡌࡧࡼࡦࡴࡧࡲࡥࠩᅻ"),
  bstack111l1_opy_ (u"ࠪࡲࡴ࡙ࡩࡨࡰࠪᅼ"),
  bstack111l1_opy_ (u"ࠫ࡮࡭࡮ࡰࡴࡨ࡙ࡳ࡯࡭ࡱࡱࡵࡸࡦࡴࡴࡗ࡫ࡨࡻࡸ࠭ᅽ"),
  bstack111l1_opy_ (u"ࠬࡪࡩࡴࡣࡥࡰࡪࡇ࡮ࡥࡴࡲ࡭ࡩ࡝ࡡࡵࡥ࡫ࡩࡷࡹࠧᅾ"),
  bstack111l1_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᅿ"),
  bstack111l1_opy_ (u"ࠧࡳࡧࡦࡶࡪࡧࡴࡦࡅ࡫ࡶࡴࡳࡥࡅࡴ࡬ࡺࡪࡸࡓࡦࡵࡶ࡭ࡴࡴࡳࠨᆀ"),
  bstack111l1_opy_ (u"ࠨࡰࡤࡸ࡮ࡼࡥࡘࡧࡥࡗࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࠧᆁ"),
  bstack111l1_opy_ (u"ࠩࡤࡲࡩࡸ࡯ࡪࡦࡖࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࡖࡡࡵࡪࠪᆂ"),
  bstack111l1_opy_ (u"ࠪࡲࡪࡺࡷࡰࡴ࡮ࡗࡵ࡫ࡥࡥࠩᆃ"),
  bstack111l1_opy_ (u"ࠫ࡬ࡶࡳࡆࡰࡤࡦࡱ࡫ࡤࠨᆄ"),
  bstack111l1_opy_ (u"ࠬ࡯ࡳࡉࡧࡤࡨࡱ࡫ࡳࡴࠩᆅ"),
  bstack111l1_opy_ (u"࠭ࡡࡥࡤࡈࡼࡪࡩࡔࡪ࡯ࡨࡳࡺࡺࠧᆆ"),
  bstack111l1_opy_ (u"ࠧ࡭ࡱࡦࡥࡱ࡫ࡓࡤࡴ࡬ࡴࡹ࠭ᆇ"),
  bstack111l1_opy_ (u"ࠨࡵ࡮࡭ࡵࡊࡥࡷ࡫ࡦࡩࡎࡴࡩࡵ࡫ࡤࡰ࡮ࢀࡡࡵ࡫ࡲࡲࠬᆈ"),
  bstack111l1_opy_ (u"ࠩࡤࡹࡹࡵࡇࡳࡣࡱࡸࡕ࡫ࡲ࡮࡫ࡶࡷ࡮ࡵ࡮ࡴࠩᆉ"),
  bstack111l1_opy_ (u"ࠪࡥࡳࡪࡲࡰ࡫ࡧࡒࡦࡺࡵࡳࡣ࡯ࡓࡷ࡯ࡥ࡯ࡶࡤࡸ࡮ࡵ࡮ࠨᆊ"),
  bstack111l1_opy_ (u"ࠫࡸࡿࡳࡵࡧࡰࡔࡴࡸࡴࠨᆋ"),
  bstack111l1_opy_ (u"ࠬࡸࡥ࡮ࡱࡷࡩࡆࡪࡢࡉࡱࡶࡸࠬᆌ"),
  bstack111l1_opy_ (u"࠭ࡳ࡬࡫ࡳ࡙ࡳࡲ࡯ࡤ࡭ࠪᆍ"), bstack111l1_opy_ (u"ࠧࡶࡰ࡯ࡳࡨࡱࡔࡺࡲࡨࠫᆎ"), bstack111l1_opy_ (u"ࠨࡷࡱࡰࡴࡩ࡫ࡌࡧࡼࠫᆏ"),
  bstack111l1_opy_ (u"ࠩࡤࡹࡹࡵࡌࡢࡷࡱࡧ࡭࠭ᆐ"),
  bstack111l1_opy_ (u"ࠪࡷࡰ࡯ࡰࡍࡱࡪࡧࡦࡺࡃࡢࡲࡷࡹࡷ࡫ࠧᆑ"),
  bstack111l1_opy_ (u"ࠫࡺࡴࡩ࡯ࡵࡷࡥࡱࡲࡏࡵࡪࡨࡶࡕࡧࡣ࡬ࡣࡪࡩࡸ࠭ᆒ"),
  bstack111l1_opy_ (u"ࠬࡪࡩࡴࡣࡥࡰࡪ࡝ࡩ࡯ࡦࡲࡻࡆࡴࡩ࡮ࡣࡷ࡭ࡴࡴࠧᆓ"),
  bstack111l1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨ࡙ࡵ࡯࡭ࡵ࡙ࡩࡷࡹࡩࡰࡰࠪᆔ"),
  bstack111l1_opy_ (u"ࠧࡦࡰࡩࡳࡷࡩࡥࡂࡲࡳࡍࡳࡹࡴࡢ࡮࡯ࠫᆕ"),
  bstack111l1_opy_ (u"ࠨࡧࡱࡷࡺࡸࡥࡘࡧࡥࡺ࡮࡫ࡷࡴࡊࡤࡺࡪࡖࡡࡨࡧࡶࠫᆖ"), bstack111l1_opy_ (u"ࠩࡺࡩࡧࡼࡩࡦࡹࡇࡩࡻࡺ࡯ࡰ࡮ࡶࡔࡴࡸࡴࠨᆗ"), bstack111l1_opy_ (u"ࠪࡩࡳࡧࡢ࡭ࡧ࡚ࡩࡧࡼࡩࡦࡹࡇࡩࡹࡧࡩ࡭ࡵࡆࡳࡱࡲࡥࡤࡶ࡬ࡳࡳ࠭ᆘ"),
  bstack111l1_opy_ (u"ࠫࡷ࡫࡭ࡰࡶࡨࡅࡵࡶࡳࡄࡣࡦ࡬ࡪࡒࡩ࡮࡫ࡷࠫᆙ"),
  bstack111l1_opy_ (u"ࠬࡩࡡ࡭ࡧࡱࡨࡦࡸࡆࡰࡴࡰࡥࡹ࠭ᆚ"),
  bstack111l1_opy_ (u"࠭ࡢࡶࡰࡧࡰࡪࡏࡤࠨᆛ"),
  bstack111l1_opy_ (u"ࠧ࡭ࡣࡸࡲࡨ࡮ࡔࡪ࡯ࡨࡳࡺࡺࠧᆜ"),
  bstack111l1_opy_ (u"ࠨ࡮ࡲࡧࡦࡺࡩࡰࡰࡖࡩࡷࡼࡩࡤࡧࡶࡉࡳࡧࡢ࡭ࡧࡧࠫᆝ"), bstack111l1_opy_ (u"ࠩ࡯ࡳࡨࡧࡴࡪࡱࡱࡗࡪࡸࡶࡪࡥࡨࡷࡆࡻࡴࡩࡱࡵ࡭ࡿ࡫ࡤࠨᆞ"),
  bstack111l1_opy_ (u"ࠪࡥࡺࡺ࡯ࡂࡥࡦࡩࡵࡺࡁ࡭ࡧࡵࡸࡸ࠭ᆟ"), bstack111l1_opy_ (u"ࠫࡦࡻࡴࡰࡆ࡬ࡷࡲ࡯ࡳࡴࡃ࡯ࡩࡷࡺࡳࠨᆠ"),
  bstack111l1_opy_ (u"ࠬࡴࡡࡵ࡫ࡹࡩࡎࡴࡳࡵࡴࡸࡱࡪࡴࡴࡴࡎ࡬ࡦࠬᆡ"),
  bstack111l1_opy_ (u"࠭࡮ࡢࡶ࡬ࡺࡪ࡝ࡥࡣࡖࡤࡴࠬᆢ"),
  bstack111l1_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯ࡉ࡯࡫ࡷ࡭ࡦࡲࡕࡳ࡮ࠪᆣ"), bstack111l1_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩࡂ࡮࡯ࡳࡼࡖ࡯ࡱࡷࡳࡷࠬᆤ"), bstack111l1_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪࡋࡪࡲࡴࡸࡥࡇࡴࡤࡹࡩ࡝ࡡࡳࡰ࡬ࡲ࡬࠭ᆥ"), bstack111l1_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫ࡒࡴࡪࡴࡌࡪࡰ࡮ࡷࡎࡴࡂࡢࡥ࡮࡫ࡷࡵࡵ࡯ࡦࠪᆦ"),
  bstack111l1_opy_ (u"ࠫࡰ࡫ࡥࡱࡍࡨࡽࡈ࡮ࡡࡪࡰࡶࠫᆧ"),
  bstack111l1_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯࡭ࡿࡧࡢ࡭ࡧࡖࡸࡷ࡯࡮ࡨࡵࡇ࡭ࡷ࠭ᆨ"),
  bstack111l1_opy_ (u"࠭ࡰࡳࡱࡦࡩࡸࡹࡁࡳࡩࡸࡱࡪࡴࡴࡴࠩᆩ"),
  bstack111l1_opy_ (u"ࠧࡪࡰࡷࡩࡷࡑࡥࡺࡆࡨࡰࡦࡿࠧᆪ"),
  bstack111l1_opy_ (u"ࠨࡵ࡫ࡳࡼࡏࡏࡔࡎࡲ࡫ࠬᆫ"),
  bstack111l1_opy_ (u"ࠩࡶࡩࡳࡪࡋࡦࡻࡖࡸࡷࡧࡴࡦࡩࡼࠫᆬ"),
  bstack111l1_opy_ (u"ࠪࡻࡪࡨ࡫ࡪࡶࡕࡩࡸࡶ࡯࡯ࡵࡨࡘ࡮ࡳࡥࡰࡷࡷࠫᆭ"), bstack111l1_opy_ (u"ࠫࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࡘࡣ࡬ࡸ࡙࡯࡭ࡦࡱࡸࡸࠬᆮ"),
  bstack111l1_opy_ (u"ࠬࡸࡥ࡮ࡱࡷࡩࡉ࡫ࡢࡶࡩࡓࡶࡴࡾࡹࠨᆯ"),
  bstack111l1_opy_ (u"࠭ࡥ࡯ࡣࡥࡰࡪࡇࡳࡺࡰࡦࡉࡽ࡫ࡣࡶࡶࡨࡊࡷࡵ࡭ࡉࡶࡷࡴࡸ࠭ᆰ"),
  bstack111l1_opy_ (u"ࠧࡴ࡭࡬ࡴࡑࡵࡧࡄࡣࡳࡸࡺࡸࡥࠨᆱ"),
  bstack111l1_opy_ (u"ࠨࡹࡨࡦࡰ࡯ࡴࡅࡧࡥࡹ࡬ࡖࡲࡰࡺࡼࡔࡴࡸࡴࠨᆲ"),
  bstack111l1_opy_ (u"ࠩࡩࡹࡱࡲࡃࡰࡰࡷࡩࡽࡺࡌࡪࡵࡷࠫᆳ"),
  bstack111l1_opy_ (u"ࠪࡻࡦ࡯ࡴࡇࡱࡵࡅࡵࡶࡓࡤࡴ࡬ࡴࡹ࠭ᆴ"),
  bstack111l1_opy_ (u"ࠫࡼ࡫ࡢࡷ࡫ࡨࡻࡈࡵ࡮࡯ࡧࡦࡸࡗ࡫ࡴࡳ࡫ࡨࡷࠬᆵ"),
  bstack111l1_opy_ (u"ࠬࡧࡰࡱࡐࡤࡱࡪ࠭ᆶ"),
  bstack111l1_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲ࡙ࡓࡍࡅࡨࡶࡹ࠭ᆷ"),
  bstack111l1_opy_ (u"ࠧࡵࡣࡳ࡛࡮ࡺࡨࡔࡪࡲࡶࡹࡖࡲࡦࡵࡶࡈࡺࡸࡡࡵ࡫ࡲࡲࠬᆸ"),
  bstack111l1_opy_ (u"ࠨࡵࡦࡥࡱ࡫ࡆࡢࡥࡷࡳࡷ࠭ᆹ"),
  bstack111l1_opy_ (u"ࠩࡺࡨࡦࡒ࡯ࡤࡣ࡯ࡔࡴࡸࡴࠨᆺ"),
  bstack111l1_opy_ (u"ࠪࡷ࡭ࡵࡷ࡙ࡥࡲࡨࡪࡒ࡯ࡨࠩᆻ"),
  bstack111l1_opy_ (u"ࠫ࡮ࡵࡳࡊࡰࡶࡸࡦࡲ࡬ࡑࡣࡸࡷࡪ࠭ᆼ"),
  bstack111l1_opy_ (u"ࠬࡾࡣࡰࡦࡨࡇࡴࡴࡦࡪࡩࡉ࡭ࡱ࡫ࠧᆽ"),
  bstack111l1_opy_ (u"࠭࡫ࡦࡻࡦ࡬ࡦ࡯࡮ࡑࡣࡶࡷࡼࡵࡲࡥࠩᆾ"),
  bstack111l1_opy_ (u"ࠧࡶࡵࡨࡔࡷ࡫ࡢࡶ࡫࡯ࡸ࡜ࡊࡁࠨᆿ"),
  bstack111l1_opy_ (u"ࠨࡲࡵࡩࡻ࡫࡮ࡵ࡙ࡇࡅࡆࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴࠩᇀ"),
  bstack111l1_opy_ (u"ࠩࡺࡩࡧࡊࡲࡪࡸࡨࡶࡆ࡭ࡥ࡯ࡶࡘࡶࡱ࠭ᇁ"),
  bstack111l1_opy_ (u"ࠪ࡯ࡪࡿࡣࡩࡣ࡬ࡲࡕࡧࡴࡩࠩᇂ"),
  bstack111l1_opy_ (u"ࠫࡺࡹࡥࡏࡧࡺ࡛ࡉࡇࠧᇃ"),
  bstack111l1_opy_ (u"ࠬࡽࡤࡢࡎࡤࡹࡳࡩࡨࡕ࡫ࡰࡩࡴࡻࡴࠨᇄ"), bstack111l1_opy_ (u"࠭ࡷࡥࡣࡆࡳࡳࡴࡥࡤࡶ࡬ࡳࡳ࡚ࡩ࡮ࡧࡲࡹࡹ࠭ᇅ"),
  bstack111l1_opy_ (u"ࠧࡹࡥࡲࡨࡪࡕࡲࡨࡋࡧࠫᇆ"), bstack111l1_opy_ (u"ࠨࡺࡦࡳࡩ࡫ࡓࡪࡩࡱ࡭ࡳ࡭ࡉࡥࠩᇇ"),
  bstack111l1_opy_ (u"ࠩࡸࡴࡩࡧࡴࡦࡦ࡚ࡈࡆࡈࡵ࡯ࡦ࡯ࡩࡎࡪࠧᇈ"),
  bstack111l1_opy_ (u"ࠪࡶࡪࡹࡥࡵࡑࡱࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡲࡵࡑࡱࡰࡾ࠭ᇉ"),
  bstack111l1_opy_ (u"ࠫࡨࡵ࡭࡮ࡣࡱࡨ࡙࡯࡭ࡦࡱࡸࡸࡸ࠭ᇊ"),
  bstack111l1_opy_ (u"ࠬࡽࡤࡢࡕࡷࡥࡷࡺࡵࡱࡔࡨࡸࡷ࡯ࡥࡴࠩᇋ"), bstack111l1_opy_ (u"࠭ࡷࡥࡣࡖࡸࡦࡸࡴࡶࡲࡕࡩࡹࡸࡹࡊࡰࡷࡩࡷࡼࡡ࡭ࠩᇌ"),
  bstack111l1_opy_ (u"ࠧࡤࡱࡱࡲࡪࡩࡴࡉࡣࡵࡨࡼࡧࡲࡦࡍࡨࡽࡧࡵࡡࡳࡦࠪᇍ"),
  bstack111l1_opy_ (u"ࠨ࡯ࡤࡼ࡙ࡿࡰࡪࡰࡪࡊࡷ࡫ࡱࡶࡧࡱࡧࡾ࠭ᇎ"),
  bstack111l1_opy_ (u"ࠩࡶ࡭ࡲࡶ࡬ࡦࡋࡶ࡚࡮ࡹࡩࡣ࡮ࡨࡇ࡭࡫ࡣ࡬ࠩᇏ"),
  bstack111l1_opy_ (u"ࠪࡹࡸ࡫ࡃࡢࡴࡷ࡬ࡦ࡭ࡥࡔࡵ࡯ࠫᇐ"),
  bstack111l1_opy_ (u"ࠫࡸ࡮࡯ࡶ࡮ࡧ࡙ࡸ࡫ࡓࡪࡰࡪࡰࡪࡺ࡯࡯ࡖࡨࡷࡹࡓࡡ࡯ࡣࡪࡩࡷ࠭ᇑ"),
  bstack111l1_opy_ (u"ࠬࡹࡴࡢࡴࡷࡍ࡜ࡊࡐࠨᇒ"),
  bstack111l1_opy_ (u"࠭ࡡ࡭࡮ࡲࡻ࡙ࡵࡵࡤࡪࡌࡨࡊࡴࡲࡰ࡮࡯ࠫᇓ"),
  bstack111l1_opy_ (u"ࠧࡪࡩࡱࡳࡷ࡫ࡈࡪࡦࡧࡩࡳࡇࡰࡪࡒࡲࡰ࡮ࡩࡹࡆࡴࡵࡳࡷ࠭ᇔ"),
  bstack111l1_opy_ (u"ࠨ࡯ࡲࡧࡰࡒ࡯ࡤࡣࡷ࡭ࡴࡴࡁࡱࡲࠪᇕ"),
  bstack111l1_opy_ (u"ࠩ࡯ࡳ࡬ࡩࡡࡵࡈࡲࡶࡲࡧࡴࠨᇖ"), bstack111l1_opy_ (u"ࠪࡰࡴ࡭ࡣࡢࡶࡉ࡭ࡱࡺࡥࡳࡕࡳࡩࡨࡹࠧᇗ"),
  bstack111l1_opy_ (u"ࠫࡦࡲ࡬ࡰࡹࡇࡩࡱࡧࡹࡂࡦࡥࠫᇘ"),
  bstack111l1_opy_ (u"ࠬࡪࡩࡴࡣࡥࡰࡪࡏࡤࡍࡱࡦࡥࡹࡵࡲࡂࡷࡷࡳࡨࡵ࡭ࡱ࡮ࡨࡸ࡮ࡵ࡮ࠨᇙ")
]
bstack1ll11111ll_opy_ = bstack111l1_opy_ (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡢࡲ࡬࠱ࡨࡲ࡯ࡶࡦ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡡࡱࡲ࠰ࡥࡺࡺ࡯࡮ࡣࡷࡩ࠴ࡻࡰ࡭ࡱࡤࡨࠬᇚ")
bstack111l1lll1_opy_ = [bstack111l1_opy_ (u"ࠧ࠯ࡣࡳ࡯ࠬᇛ"), bstack111l1_opy_ (u"ࠨ࠰ࡤࡥࡧ࠭ᇜ"), bstack111l1_opy_ (u"ࠩ࠱࡭ࡵࡧࠧᇝ")]
bstack1l1lllll1l_opy_ = [bstack111l1_opy_ (u"ࠪ࡭ࡩ࠭ᇞ"), bstack111l1_opy_ (u"ࠫࡵࡧࡴࡩࠩᇟ"), bstack111l1_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡤ࡯ࡤࠨᇠ"), bstack111l1_opy_ (u"࠭ࡳࡩࡣࡵࡩࡦࡨ࡬ࡦࡡ࡬ࡨࠬᇡ")]
bstack1lll1l1ll1_opy_ = {
  bstack111l1_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᇢ"): bstack111l1_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᇣ"),
  bstack111l1_opy_ (u"ࠩࡩ࡭ࡷ࡫ࡦࡰࡺࡒࡴࡹ࡯࡯࡯ࡵࠪᇤ"): bstack111l1_opy_ (u"ࠪࡱࡴࢀ࠺ࡧ࡫ࡵࡩ࡫ࡵࡸࡐࡲࡷ࡭ࡴࡴࡳࠨᇥ"),
  bstack111l1_opy_ (u"ࠫࡪࡪࡧࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᇦ"): bstack111l1_opy_ (u"ࠬࡳࡳ࠻ࡧࡧ࡫ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᇧ"),
  bstack111l1_opy_ (u"࠭ࡩࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᇨ"): bstack111l1_opy_ (u"ࠧࡴࡧ࠽࡭ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᇩ"),
  bstack111l1_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩࡐࡲࡷ࡭ࡴࡴࡳࠨᇪ"): bstack111l1_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪ࠰ࡲࡴࡹ࡯࡯࡯ࡵࠪᇫ")
}
bstack1l1l1lll1l_opy_ = [
  bstack111l1_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᇬ"),
  bstack111l1_opy_ (u"ࠫࡲࡵࡺ࠻ࡨ࡬ࡶࡪ࡬࡯ࡹࡑࡳࡸ࡮ࡵ࡮ࡴࠩᇭ"),
  bstack111l1_opy_ (u"ࠬࡳࡳ࠻ࡧࡧ࡫ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᇮ"),
  bstack111l1_opy_ (u"࠭ࡳࡦ࠼࡬ࡩࡔࡶࡴࡪࡱࡱࡷࠬᇯ"),
  bstack111l1_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯࠮ࡰࡲࡷ࡭ࡴࡴࡳࠨᇰ"),
]
bstack1l11l11111_opy_ = bstack11l1l1111_opy_ + bstack111ll1l111_opy_ + bstack1ll1l1l111_opy_
bstack1llll1111l_opy_ = [
  bstack111l1_opy_ (u"ࠨࡠ࡯ࡳࡨࡧ࡬ࡩࡱࡶࡸࠩ࠭ᇱ"),
  bstack111l1_opy_ (u"ࠩࡡࡦࡸ࠳࡬ࡰࡥࡤࡰ࠳ࡩ࡯࡮ࠦࠪᇲ"),
  bstack111l1_opy_ (u"ࠪࡢ࠶࠸࠷࠯ࠩᇳ"),
  bstack111l1_opy_ (u"ࠫࡣ࠷࠰࠯ࠩᇴ"),
  bstack111l1_opy_ (u"ࠬࡤ࠱࠸࠴࠱࠵ࡠ࠼࠭࠺࡟࠱ࠫᇵ"),
  bstack111l1_opy_ (u"࠭࡞࠲࠹࠵࠲࠷ࡡ࠰࠮࠻ࡠ࠲ࠬᇶ"),
  bstack111l1_opy_ (u"ࠧ࡟࠳࠺࠶࠳࠹࡛࠱࠯࠴ࡡ࠳࠭ᇷ"),
  bstack111l1_opy_ (u"ࠨࡠ࠴࠽࠷࠴࠱࠷࠺࠱ࠫᇸ")
]
bstack111ll1l11l_opy_ = bstack111l1_opy_ (u"ࠩ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡥࡵ࡯࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯ࠪᇹ")
bstack111lll11_opy_ = bstack111l1_opy_ (u"ࠪࡷࡩࡱ࠯ࡷ࠳࠲ࡩࡻ࡫࡮ࡵࠩᇺ")
bstack1l11111l11_opy_ = [ bstack111l1_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭ᇻ") ]
bstack1l111l1l1_opy_ = [ bstack111l1_opy_ (u"ࠬࡧࡰࡱ࠯ࡤࡹࡹࡵ࡭ࡢࡶࡨࠫᇼ") ]
bstack1lll111ll_opy_ = [ bstack111l1_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭ᇽ") ]
bstack1ll1l11l1l_opy_ = bstack111l1_opy_ (u"ࠧࡔࡆࡎࡗࡪࡺࡵࡱࠩᇾ")
bstack1l1l1llll_opy_ = bstack111l1_opy_ (u"ࠨࡕࡇࡏ࡙࡫ࡳࡵࡃࡷࡸࡪࡳࡰࡵࡧࡧࠫᇿ")
bstack1ll11l11l1_opy_ = bstack111l1_opy_ (u"ࠩࡖࡈࡐ࡚ࡥࡴࡶࡖࡹࡨࡩࡥࡴࡵࡩࡹࡱ࠭ሀ")
bstack1l11ll1l1_opy_ = bstack111l1_opy_ (u"ࠪ࠸࠳࠶࠮࠱ࠩሁ")
bstack1l11llll11_opy_ = [
  bstack111l1_opy_ (u"ࠫࡊࡘࡒࡠࡈࡄࡍࡑࡋࡄࠨሂ"),
  bstack111l1_opy_ (u"ࠬࡋࡒࡓࡡࡗࡍࡒࡋࡄࡠࡑࡘࡘࠬሃ"),
  bstack111l1_opy_ (u"࠭ࡅࡓࡔࡢࡆࡑࡕࡃࡌࡇࡇࡣࡇ࡟࡟ࡄࡎࡌࡉࡓ࡚ࠧሄ"),
  bstack111l1_opy_ (u"ࠧࡆࡔࡕࡣࡓࡋࡔࡘࡑࡕࡏࡤࡉࡈࡂࡐࡊࡉࡉ࠭ህ"),
  bstack111l1_opy_ (u"ࠨࡇࡕࡖࡤ࡙ࡏࡄࡍࡈࡘࡤࡔࡏࡕࡡࡆࡓࡓࡔࡅࡄࡖࡈࡈࠬሆ"),
  bstack111l1_opy_ (u"ࠩࡈࡖࡗࡥࡃࡐࡐࡑࡉࡈ࡚ࡉࡐࡐࡢࡇࡑࡕࡓࡆࡆࠪሇ"),
  bstack111l1_opy_ (u"ࠪࡉࡗࡘ࡟ࡄࡑࡑࡒࡊࡉࡔࡊࡑࡑࡣࡗࡋࡓࡆࡖࠪለ"),
  bstack111l1_opy_ (u"ࠫࡊࡘࡒࡠࡅࡒࡒࡓࡋࡃࡕࡋࡒࡒࡤࡘࡅࡇࡗࡖࡉࡉ࠭ሉ"),
  bstack111l1_opy_ (u"ࠬࡋࡒࡓࡡࡆࡓࡓࡔࡅࡄࡖࡌࡓࡓࡥࡁࡃࡑࡕࡘࡊࡊࠧሊ"),
  bstack111l1_opy_ (u"࠭ࡅࡓࡔࡢࡇࡔࡔࡎࡆࡅࡗࡍࡔࡔ࡟ࡇࡃࡌࡐࡊࡊࠧላ"),
  bstack111l1_opy_ (u"ࠧࡆࡔࡕࡣࡓࡇࡍࡆࡡࡑࡓ࡙ࡥࡒࡆࡕࡒࡐ࡛ࡋࡄࠨሌ"),
  bstack111l1_opy_ (u"ࠨࡇࡕࡖࡤࡇࡄࡅࡔࡈࡗࡘࡥࡉࡏࡘࡄࡐࡎࡊࠧል"),
  bstack111l1_opy_ (u"ࠩࡈࡖࡗࡥࡁࡅࡆࡕࡉࡘ࡙࡟ࡖࡐࡕࡉࡆࡉࡈࡂࡄࡏࡉࠬሎ"),
  bstack111l1_opy_ (u"ࠪࡉࡗࡘ࡟ࡕࡗࡑࡒࡊࡒ࡟ࡄࡑࡑࡒࡊࡉࡔࡊࡑࡑࡣࡋࡇࡉࡍࡇࡇࠫሏ"),
  bstack111l1_opy_ (u"ࠫࡊࡘࡒࡠࡅࡒࡒࡓࡋࡃࡕࡋࡒࡒࡤ࡚ࡉࡎࡇࡇࡣࡔ࡛ࡔࠨሐ"),
  bstack111l1_opy_ (u"ࠬࡋࡒࡓࡡࡖࡓࡈࡑࡓࡠࡅࡒࡒࡓࡋࡃࡕࡋࡒࡒࡤࡌࡁࡊࡎࡈࡈࠬሑ"),
  bstack111l1_opy_ (u"࠭ࡅࡓࡔࡢࡗࡔࡉࡋࡔࡡࡆࡓࡓࡔࡅࡄࡖࡌࡓࡓࡥࡈࡐࡕࡗࡣ࡚ࡔࡒࡆࡃࡆࡌࡆࡈࡌࡆࠩሒ"),
  bstack111l1_opy_ (u"ࠧࡆࡔࡕࡣࡕࡘࡏ࡙࡛ࡢࡇࡔࡔࡎࡆࡅࡗࡍࡔࡔ࡟ࡇࡃࡌࡐࡊࡊࠧሓ"),
  bstack111l1_opy_ (u"ࠨࡇࡕࡖࡤࡔࡁࡎࡇࡢࡒࡔ࡚࡟ࡓࡇࡖࡓࡑ࡜ࡅࡅࠩሔ"),
  bstack111l1_opy_ (u"ࠩࡈࡖࡗࡥࡎࡂࡏࡈࡣࡗࡋࡓࡐࡎࡘࡘࡎࡕࡎࡠࡈࡄࡍࡑࡋࡄࠨሕ"),
  bstack111l1_opy_ (u"ࠪࡉࡗࡘ࡟ࡎࡃࡑࡈࡆ࡚ࡏࡓ࡛ࡢࡔࡗࡕࡘ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡࡉࡅࡎࡒࡅࡅࠩሖ"),
]
bstack1llll1l111_opy_ = bstack111l1_opy_ (u"ࠫ࠳࠵ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠲ࡧࡲࡵ࡫ࡩࡥࡨࡺࡳ࠰ࠩሗ")
bstack1l1l1ll111_opy_ = os.path.join(os.path.expanduser(bstack111l1_opy_ (u"ࠬࢄࠧመ")), bstack111l1_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ሙ"), bstack111l1_opy_ (u"ࠧ࠯ࡤࡶࡸࡦࡩ࡫࠮ࡥࡲࡲ࡫࡯ࡧ࠯࡬ࡶࡳࡳ࠭ሚ"))
bstack11l111l11l_opy_ = bstack111l1_opy_ (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡧࡰࡪࠩማ")
bstack111ll1l1ll_opy_ = [ bstack111l1_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩሜ"), bstack111l1_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩም"), bstack111l1_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪሞ"), bstack111l1_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬሟ")]
bstack1l11ll11l_opy_ = [ bstack111l1_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ሠ"), bstack111l1_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ሡ"), bstack111l1_opy_ (u"ࠨࡲࡤࡦࡴࡺࠧሢ"), bstack111l1_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩሣ") ]
bstack11l1lll11l_opy_ = {
  bstack111l1_opy_ (u"ࠪࡔࡆ࡙ࡓࠨሤ"): bstack111l1_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫሥ"),
  bstack111l1_opy_ (u"ࠬࡌࡁࡊࡎࠪሦ"): bstack111l1_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ሧ"),
  bstack111l1_opy_ (u"ࠧࡔࡍࡌࡔࠬረ"): bstack111l1_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩሩ")
}
bstack1lllllll1_opy_ = [
  bstack111l1_opy_ (u"ࠤࡪࡩࡹࠨሪ"),
  bstack111l1_opy_ (u"ࠥ࡫ࡴࡈࡡࡤ࡭ࠥራ"),
  bstack111l1_opy_ (u"ࠦ࡬ࡵࡆࡰࡴࡺࡥࡷࡪࠢሬ"),
  bstack111l1_opy_ (u"ࠧࡸࡥࡧࡴࡨࡷ࡭ࠨር"),
  bstack111l1_opy_ (u"ࠨࡣ࡭࡫ࡦ࡯ࡊࡲࡥ࡮ࡧࡱࡸࠧሮ"),
  bstack111l1_opy_ (u"ࠢࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࠦሯ"),
  bstack111l1_opy_ (u"ࠣࡵࡸࡦࡲ࡯ࡴࡆ࡮ࡨࡱࡪࡴࡴࠣሰ"),
  bstack111l1_opy_ (u"ࠤࡶࡩࡳࡪࡋࡦࡻࡶࡘࡴࡋ࡬ࡦ࡯ࡨࡲࡹࠨሱ"),
  bstack111l1_opy_ (u"ࠥࡷࡪࡴࡤࡌࡧࡼࡷ࡙ࡵࡁࡤࡶ࡬ࡺࡪࡋ࡬ࡦ࡯ࡨࡲࡹࠨሲ"),
  bstack111l1_opy_ (u"ࠦࡨࡲࡥࡢࡴࡈࡰࡪࡳࡥ࡯ࡶࠥሳ"),
  bstack111l1_opy_ (u"ࠧࡧࡣࡵ࡫ࡲࡲࡸࠨሴ"),
  bstack111l1_opy_ (u"ࠨࡥࡹࡧࡦࡹࡹ࡫ࡓࡤࡴ࡬ࡴࡹࠨስ"),
  bstack111l1_opy_ (u"ࠢࡦࡺࡨࡧࡺࡺࡥࡂࡵࡼࡲࡨ࡙ࡣࡳ࡫ࡳࡸࠧሶ"),
  bstack111l1_opy_ (u"ࠣࡥ࡯ࡳࡸ࡫ࠢሷ"),
  bstack111l1_opy_ (u"ࠤࡴࡹ࡮ࡺࠢሸ"),
  bstack111l1_opy_ (u"ࠥࡴࡪࡸࡦࡰࡴࡰࡘࡴࡻࡣࡩࡃࡦࡸ࡮ࡵ࡮ࠣሹ"),
  bstack111l1_opy_ (u"ࠦࡵ࡫ࡲࡧࡱࡵࡱࡒࡻ࡬ࡵ࡫ࡗࡳࡺࡩࡨࠣሺ"),
  bstack111l1_opy_ (u"ࠧࡹࡨࡢ࡭ࡨࠦሻ"),
  bstack111l1_opy_ (u"ࠨࡣ࡭ࡱࡶࡩࡆࡶࡰࠣሼ")
]
bstack111ll1ll11_opy_ = [
  bstack111l1_opy_ (u"ࠢࡤ࡮࡬ࡧࡰࠨሽ"),
  bstack111l1_opy_ (u"ࠣࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠧሾ"),
  bstack111l1_opy_ (u"ࠤࡤࡹࡹࡵࠢሿ"),
  bstack111l1_opy_ (u"ࠥࡱࡦࡴࡵࡢ࡮ࠥቀ"),
  bstack111l1_opy_ (u"ࠦࡹ࡫ࡳࡵࡥࡤࡷࡪࠨቁ")
]
bstack1lll1l1lll_opy_ = {
  bstack111l1_opy_ (u"ࠧࡩ࡬ࡪࡥ࡮ࠦቂ"): [bstack111l1_opy_ (u"ࠨࡣ࡭࡫ࡦ࡯ࡊࡲࡥ࡮ࡧࡱࡸࠧቃ")],
  bstack111l1_opy_ (u"ࠢࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࠦቄ"): [bstack111l1_opy_ (u"ࠣࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠧቅ")],
  bstack111l1_opy_ (u"ࠤࡤࡹࡹࡵࠢቆ"): [bstack111l1_opy_ (u"ࠥࡷࡪࡴࡤࡌࡧࡼࡷ࡙ࡵࡅ࡭ࡧࡰࡩࡳࡺࠢቇ"), bstack111l1_opy_ (u"ࠦࡸ࡫࡮ࡥࡍࡨࡽࡸ࡚࡯ࡂࡥࡷ࡭ࡻ࡫ࡅ࡭ࡧࡰࡩࡳࡺࠢቈ"), bstack111l1_opy_ (u"ࠧࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࠤ቉"), bstack111l1_opy_ (u"ࠨࡣ࡭࡫ࡦ࡯ࡊࡲࡥ࡮ࡧࡱࡸࠧቊ")],
  bstack111l1_opy_ (u"ࠢ࡮ࡣࡱࡹࡦࡲࠢቋ"): [bstack111l1_opy_ (u"ࠣ࡯ࡤࡲࡺࡧ࡬ࠣቌ")],
  bstack111l1_opy_ (u"ࠤࡷࡩࡸࡺࡣࡢࡵࡨࠦቍ"): [bstack111l1_opy_ (u"ࠥࡸࡪࡹࡴࡤࡣࡶࡩࠧ቎")],
}
bstack111ll1ll1l_opy_ = {
  bstack111l1_opy_ (u"ࠦࡨࡲࡩࡤ࡭ࡈࡰࡪࡳࡥ࡯ࡶࠥ቏"): bstack111l1_opy_ (u"ࠧࡩ࡬ࡪࡥ࡮ࠦቐ"),
  bstack111l1_opy_ (u"ࠨࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠥቑ"): bstack111l1_opy_ (u"ࠢࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࠦቒ"),
  bstack111l1_opy_ (u"ࠣࡵࡨࡲࡩࡑࡥࡺࡵࡗࡳࡊࡲࡥ࡮ࡧࡱࡸࠧቓ"): bstack111l1_opy_ (u"ࠤࡶࡩࡳࡪࡋࡦࡻࡶࠦቔ"),
  bstack111l1_opy_ (u"ࠥࡷࡪࡴࡤࡌࡧࡼࡷ࡙ࡵࡁࡤࡶ࡬ࡺࡪࡋ࡬ࡦ࡯ࡨࡲࡹࠨቕ"): bstack111l1_opy_ (u"ࠦࡸ࡫࡮ࡥࡍࡨࡽࡸࠨቖ"),
  bstack111l1_opy_ (u"ࠧࡺࡥࡴࡶࡦࡥࡸ࡫ࠢ቗"): bstack111l1_opy_ (u"ࠨࡴࡦࡵࡷࡧࡦࡹࡥࠣቘ")
}
bstack11ll11lll1_opy_ = {
  bstack111l1_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡂࡎࡏࠫ቙"): bstack111l1_opy_ (u"ࠨࡕࡸ࡭ࡹ࡫ࠠࡔࡧࡷࡹࡵ࠭ቚ"),
  bstack111l1_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡃࡏࡐࠬቛ"): bstack111l1_opy_ (u"ࠪࡗࡺ࡯ࡴࡦࠢࡗࡩࡦࡸࡤࡰࡹࡱࠫቜ"),
  bstack111l1_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡊࡇࡃࡉࠩቝ"): bstack111l1_opy_ (u"࡚ࠬࡥࡴࡶࠣࡗࡪࡺࡵࡱࠩ቞"),
  bstack111l1_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡋࡁࡄࡊࠪ቟"): bstack111l1_opy_ (u"ࠧࡕࡧࡶࡸ࡚ࠥࡥࡢࡴࡧࡳࡼࡴࠧበ")
}
bstack111ll11lll_opy_ = 65536
bstack111l1llll1_opy_ = bstack111l1_opy_ (u"ࠨ࠰࠱࠲ࡠ࡚ࡒࡖࡐࡆࡅ࡙ࡋࡄ࡞ࠩቡ")
bstack111ll111ll_opy_ = [
      bstack111l1_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫቢ"), bstack111l1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ባ"), bstack111l1_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧቤ"), bstack111l1_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩብ"), bstack111l1_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲ࡜ࡡࡳ࡫ࡤࡦࡱ࡫ࡳࠨቦ"),
      bstack111l1_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡛ࡳࡦࡴࠪቧ"), bstack111l1_opy_ (u"ࠨࡲࡵࡳࡽࡿࡐࡢࡵࡶࠫቨ"), bstack111l1_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡑࡴࡲࡼࡾ࡛ࡳࡦࡴࠪቩ"), bstack111l1_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡒࡵࡳࡽࡿࡐࡢࡵࡶࠫቪ"),
      bstack111l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡹࡸ࡫ࡲࡏࡣࡰࡩࠬቫ"), bstack111l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧቬ"), bstack111l1_opy_ (u"࠭ࡡࡶࡶ࡫ࡘࡴࡱࡥ࡯ࠩቭ")
    ]
bstack111ll1l1l1_opy_= {
  bstack111l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫቮ"): bstack111l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬቯ"),
  bstack111l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ተ"): bstack111l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧቱ"),
  bstack111l1_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪቲ"): bstack111l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩታ"),
  bstack111l1_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭ቴ"): bstack111l1_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧት"),
  bstack111l1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫቶ"): bstack111l1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬቷ"),
  bstack111l1_opy_ (u"ࠪࡰࡴ࡭ࡌࡦࡸࡨࡰࠬቸ"): bstack111l1_opy_ (u"ࠫࡱࡵࡧࡍࡧࡹࡩࡱ࠭ቹ"),
  bstack111l1_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨቺ"): bstack111l1_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩቻ"),
  bstack111l1_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫቼ"): bstack111l1_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬች"),
  bstack111l1_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬቾ"): bstack111l1_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ቿ"),
  bstack111l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡅࡲࡲࡹ࡫ࡸࡵࡑࡳࡸ࡮ࡵ࡮ࡴࠩኀ"): bstack111l1_opy_ (u"ࠬࡺࡥࡴࡶࡆࡳࡳࡺࡥࡹࡶࡒࡴࡹ࡯࡯࡯ࡵࠪኁ"),
  bstack111l1_opy_ (u"࠭ࡴࡦࡵࡷࡓࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪኂ"): bstack111l1_opy_ (u"ࠧࡵࡧࡶࡸࡔࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫኃ"),
  bstack111l1_opy_ (u"ࠨࡶࡨࡷࡹࡕࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬኄ"): bstack111l1_opy_ (u"ࠩࡷࡩࡸࡺࡏࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ኅ"),
  bstack111l1_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯࡙ࡥࡷ࡯ࡡࡣ࡮ࡨࡷࠬኆ"): bstack111l1_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰ࡚ࡦࡸࡩࡢࡤ࡯ࡩࡸ࠭ኇ"),
  bstack111l1_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩኈ"): bstack111l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨ኉"),
  bstack111l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩኊ"): bstack111l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪኋ"),
  bstack111l1_opy_ (u"ࠩࡵࡩࡷࡻ࡮ࡕࡧࡶࡸࡸ࠭ኌ"): bstack111l1_opy_ (u"ࠪࡶࡪࡸࡵ࡯ࡖࡨࡷࡹࡹࠧኍ"),
  bstack111l1_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࠪ኎"): bstack111l1_opy_ (u"ࠬࡶࡥࡳࡥࡼࠫ኏"),
  bstack111l1_opy_ (u"࠭ࡰࡦࡴࡦࡽࡔࡶࡴࡪࡱࡱࡷࠬነ"): bstack111l1_opy_ (u"ࠧࡱࡧࡵࡧࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ኑ"),
  bstack111l1_opy_ (u"ࠨࡲࡨࡶࡨࡿࡃࡢࡲࡷࡹࡷ࡫ࡍࡰࡦࡨࠫኒ"): bstack111l1_opy_ (u"ࠩࡳࡩࡷࡩࡹࡄࡣࡳࡸࡺࡸࡥࡎࡱࡧࡩࠬና"),
  bstack111l1_opy_ (u"ࠪࡨ࡮ࡹࡡࡣ࡮ࡨࡅࡺࡺ࡯ࡄࡣࡳࡸࡺࡸࡥࡍࡱࡪࡷࠬኔ"): bstack111l1_opy_ (u"ࠫࡩ࡯ࡳࡢࡤ࡯ࡩࡆࡻࡴࡰࡅࡤࡴࡹࡻࡲࡦࡎࡲ࡫ࡸ࠭ን"),
  bstack111l1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬኖ"): bstack111l1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ኗ"),
  bstack111l1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧኘ"): bstack111l1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨኙ"),
  bstack111l1_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭ኚ"): bstack111l1_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧኛ"),
  bstack111l1_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࡐࡲࡷ࡭ࡴࡴࡳࠨኜ"): bstack111l1_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩኝ"),
  bstack111l1_opy_ (u"࠭ࡰࡳࡱࡻࡽࡘ࡫ࡴࡵ࡫ࡱ࡫ࡸ࠭ኞ"): bstack111l1_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡙ࡥࡵࡶ࡬ࡲ࡬ࡹࠧኟ")
}
bstack111ll11l1l_opy_ = [bstack111l1_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨአ"), bstack111l1_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨኡ")]