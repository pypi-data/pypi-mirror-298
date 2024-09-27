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
from urllib.parse import urlparse
from bstack_utils.config import Config
from bstack_utils.messages import bstack1lllll11lll_opy_
bstack1111ll1l1_opy_ = Config.bstack1l1ll11lll_opy_()
def bstack1lll11lll11_opy_(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
def bstack1lll1l111l1_opy_(bstack1lll11lllll_opy_, bstack1lll1l1111l_opy_):
    from pypac import get_pac
    from pypac import PACSession
    from pypac.parser import PACFile
    import socket
    if os.path.isfile(bstack1lll11lllll_opy_):
        with open(bstack1lll11lllll_opy_) as f:
            pac = PACFile(f.read())
    elif bstack1lll11lll11_opy_(bstack1lll11lllll_opy_):
        pac = get_pac(url=bstack1lll11lllll_opy_)
    else:
        raise Exception(bstack111l1_opy_ (u"ࠬࡖࡡࡤࠢࡩ࡭ࡱ࡫ࠠࡥࡱࡨࡷࠥࡴ࡯ࡵࠢࡨࡼ࡮ࡹࡴ࠻ࠢࡾࢁࠬᕼ").format(bstack1lll11lllll_opy_))
    session = PACSession(pac)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((bstack111l1_opy_ (u"ࠨ࠸࠯࠺࠱࠼࠳࠾ࠢᕽ"), 80))
        bstack1lll11llll1_opy_ = s.getsockname()[0]
        s.close()
    except:
        bstack1lll11llll1_opy_ = bstack111l1_opy_ (u"ࠧ࠱࠰࠳࠲࠵࠴࠰ࠨᕾ")
    proxy_url = session.get_pac().find_proxy_for_url(bstack1lll1l1111l_opy_, bstack1lll11llll1_opy_)
    return proxy_url
def bstack111lll1l_opy_(config):
    return bstack111l1_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫᕿ") in config or bstack111l1_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭ᖀ") in config
def bstack1l11l1ll1l_opy_(config):
    if not bstack111lll1l_opy_(config):
        return
    if config.get(bstack111l1_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭ᖁ")):
        return config.get(bstack111l1_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧᖂ"))
    if config.get(bstack111l1_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩᖃ")):
        return config.get(bstack111l1_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪᖄ"))
def bstack1l11l11l_opy_(config, bstack1lll1l1111l_opy_):
    proxy = bstack1l11l1ll1l_opy_(config)
    proxies = {}
    if config.get(bstack111l1_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪᖅ")) or config.get(bstack111l1_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬᖆ")):
        if proxy.endswith(bstack111l1_opy_ (u"ࠩ࠱ࡴࡦࡩࠧᖇ")):
            proxies = bstack1l11llll_opy_(proxy, bstack1lll1l1111l_opy_)
        else:
            proxies = {
                bstack111l1_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩᖈ"): proxy
            }
    bstack1111ll1l1_opy_.bstack1lll11lll_opy_(bstack111l1_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡖࡩࡹࡺࡩ࡯ࡩࡶࠫᖉ"), proxies)
    return proxies
def bstack1l11llll_opy_(bstack1lll11lllll_opy_, bstack1lll1l1111l_opy_):
    proxies = {}
    global bstack1lll11lll1l_opy_
    if bstack111l1_opy_ (u"ࠬࡖࡁࡄࡡࡓࡖࡔ࡞࡙ࠨᖊ") in globals():
        return bstack1lll11lll1l_opy_
    try:
        proxy = bstack1lll1l111l1_opy_(bstack1lll11lllll_opy_, bstack1lll1l1111l_opy_)
        if bstack111l1_opy_ (u"ࠨࡄࡊࡔࡈࡇ࡙ࠨᖋ") in proxy:
            proxies = {}
        elif bstack111l1_opy_ (u"ࠢࡉࡖࡗࡔࠧᖌ") in proxy or bstack111l1_opy_ (u"ࠣࡊࡗࡘࡕ࡙ࠢᖍ") in proxy or bstack111l1_opy_ (u"ࠤࡖࡓࡈࡑࡓࠣᖎ") in proxy:
            bstack1lll1l11111_opy_ = proxy.split(bstack111l1_opy_ (u"ࠥࠤࠧᖏ"))
            if bstack111l1_opy_ (u"ࠦ࠿࠵࠯ࠣᖐ") in bstack111l1_opy_ (u"ࠧࠨᖑ").join(bstack1lll1l11111_opy_[1:]):
                proxies = {
                    bstack111l1_opy_ (u"࠭ࡨࡵࡶࡳࡷࠬᖒ"): bstack111l1_opy_ (u"ࠢࠣᖓ").join(bstack1lll1l11111_opy_[1:])
                }
            else:
                proxies = {
                    bstack111l1_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧᖔ"): str(bstack1lll1l11111_opy_[0]).lower() + bstack111l1_opy_ (u"ࠤ࠽࠳࠴ࠨᖕ") + bstack111l1_opy_ (u"ࠥࠦᖖ").join(bstack1lll1l11111_opy_[1:])
                }
        elif bstack111l1_opy_ (u"ࠦࡕࡘࡏ࡙࡛ࠥᖗ") in proxy:
            bstack1lll1l11111_opy_ = proxy.split(bstack111l1_opy_ (u"ࠧࠦࠢᖘ"))
            if bstack111l1_opy_ (u"ࠨ࠺࠰࠱ࠥᖙ") in bstack111l1_opy_ (u"ࠢࠣᖚ").join(bstack1lll1l11111_opy_[1:]):
                proxies = {
                    bstack111l1_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧᖛ"): bstack111l1_opy_ (u"ࠤࠥᖜ").join(bstack1lll1l11111_opy_[1:])
                }
            else:
                proxies = {
                    bstack111l1_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩᖝ"): bstack111l1_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳ࠧᖞ") + bstack111l1_opy_ (u"ࠧࠨᖟ").join(bstack1lll1l11111_opy_[1:])
                }
        else:
            proxies = {
                bstack111l1_opy_ (u"࠭ࡨࡵࡶࡳࡷࠬᖠ"): proxy
            }
    except Exception as e:
        print(bstack111l1_opy_ (u"ࠢࡴࡱࡰࡩࠥ࡫ࡲࡳࡱࡵࠦᖡ"), bstack1lllll11lll_opy_.format(bstack1lll11lllll_opy_, str(e)))
    bstack1lll11lll1l_opy_ = proxies
    return proxies