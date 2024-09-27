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
class bstack111lll1l1l_opy_(object):
  bstack1lll1lll_opy_ = os.path.join(os.path.expanduser(bstack111l1_opy_ (u"ࠪࢂࠬྦྷ")), bstack111l1_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫྨ"))
  bstack111lll1l11_opy_ = os.path.join(bstack1lll1lll_opy_, bstack111l1_opy_ (u"ࠬࡩ࡯࡮࡯ࡤࡲࡩࡹ࠮࡫ࡵࡲࡲࠬྩ"))
  bstack111llll11l_opy_ = None
  perform_scan = None
  bstack1lll1111ll_opy_ = None
  bstack1ll1ll1l1l_opy_ = None
  bstack11l1111lll_opy_ = None
  def __new__(cls):
    if not hasattr(cls, bstack111l1_opy_ (u"࠭ࡩ࡯ࡵࡷࡥࡳࡩࡥࠨྪ")):
      cls.instance = super(bstack111lll1l1l_opy_, cls).__new__(cls)
      cls.instance.bstack111llll111_opy_()
    return cls.instance
  def bstack111llll111_opy_(self):
    try:
      with open(self.bstack111lll1l11_opy_, bstack111l1_opy_ (u"ࠧࡳࠩྫ")) as bstack1lllll111l_opy_:
        bstack111lll1ll1_opy_ = bstack1lllll111l_opy_.read()
        data = json.loads(bstack111lll1ll1_opy_)
        if bstack111l1_opy_ (u"ࠨࡥࡲࡱࡲࡧ࡮ࡥࡵࠪྫྷ") in data:
          self.bstack11l11l111l_opy_(data[bstack111l1_opy_ (u"ࠩࡦࡳࡲࡳࡡ࡯ࡦࡶࠫྭ")])
        if bstack111l1_opy_ (u"ࠪࡷࡨࡸࡩࡱࡶࡶࠫྮ") in data:
          self.bstack11l11ll111_opy_(data[bstack111l1_opy_ (u"ࠫࡸࡩࡲࡪࡲࡷࡷࠬྯ")])
    except:
      pass
  def bstack11l11ll111_opy_(self, scripts):
    if scripts != None:
      self.perform_scan = scripts[bstack111l1_opy_ (u"ࠬࡹࡣࡢࡰࠪྰ")]
      self.bstack1lll1111ll_opy_ = scripts[bstack111l1_opy_ (u"࠭ࡧࡦࡶࡕࡩࡸࡻ࡬ࡵࡵࠪྱ")]
      self.bstack1ll1ll1l1l_opy_ = scripts[bstack111l1_opy_ (u"ࠧࡨࡧࡷࡖࡪࡹࡵ࡭ࡶࡶࡗࡺࡳ࡭ࡢࡴࡼࠫྲ")]
      self.bstack11l1111lll_opy_ = scripts[bstack111l1_opy_ (u"ࠨࡵࡤࡺࡪࡘࡥࡴࡷ࡯ࡸࡸ࠭ླ")]
  def bstack11l11l111l_opy_(self, bstack111llll11l_opy_):
    if bstack111llll11l_opy_ != None and len(bstack111llll11l_opy_) != 0:
      self.bstack111llll11l_opy_ = bstack111llll11l_opy_
  def store(self):
    try:
      with open(self.bstack111lll1l11_opy_, bstack111l1_opy_ (u"ࠩࡺࠫྴ")) as file:
        json.dump({
          bstack111l1_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࡷࠧྵ"): self.bstack111llll11l_opy_,
          bstack111l1_opy_ (u"ࠦࡸࡩࡲࡪࡲࡷࡷࠧྶ"): {
            bstack111l1_opy_ (u"ࠧࡹࡣࡢࡰࠥྷ"): self.perform_scan,
            bstack111l1_opy_ (u"ࠨࡧࡦࡶࡕࡩࡸࡻ࡬ࡵࡵࠥྸ"): self.bstack1lll1111ll_opy_,
            bstack111l1_opy_ (u"ࠢࡨࡧࡷࡖࡪࡹࡵ࡭ࡶࡶࡗࡺࡳ࡭ࡢࡴࡼࠦྐྵ"): self.bstack1ll1ll1l1l_opy_,
            bstack111l1_opy_ (u"ࠣࡵࡤࡺࡪࡘࡥࡴࡷ࡯ࡸࡸࠨྺ"): self.bstack11l1111lll_opy_
          }
        }, file)
    except:
      pass
  def bstack1l1l11l11_opy_(self, bstack111lll1lll_opy_):
    try:
      return any(command.get(bstack111l1_opy_ (u"ࠩࡱࡥࡲ࡫ࠧྻ")) == bstack111lll1lll_opy_ for command in self.bstack111llll11l_opy_)
    except:
      return False
bstack1lll11l1_opy_ = bstack111lll1l1l_opy_()