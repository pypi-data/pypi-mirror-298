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
import atexit
import os
import signal
import sys
import yaml
import requests
import logging
import threading
import socket
import datetime
import string
import random
import json
import collections.abc
import re
import multiprocessing
import traceback
import copy
import tempfile
from packaging import version
from uuid import uuid4
from browserstack.local import Local
from urllib.parse import urlparse
from dotenv import load_dotenv
from bstack_utils.constants import *
from bstack_utils.percy import *
from browserstack_sdk.bstack111ll111l_opy_ import *
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.bstack1l1111lll_opy_ import bstack1l1ll1ll11_opy_
import time
import requests
def bstack1ll111ll_opy_():
  global CONFIG
  headers = {
        bstack111l1_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩࡶ"): bstack111l1_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧࡷ"),
      }
  proxies = bstack1l11l11l_opy_(CONFIG, bstack1ll1l1l11_opy_)
  try:
    response = requests.get(bstack1ll1l1l11_opy_, headers=headers, proxies=proxies, timeout=5)
    if response.json():
      bstack1l1lll11l1_opy_ = response.json()[bstack111l1_opy_ (u"ࠬ࡮ࡵࡣࡵࠪࡸ")]
      logger.debug(bstack1l1lll1ll_opy_.format(response.json()))
      return bstack1l1lll11l1_opy_
    else:
      logger.debug(bstack1l1llllll_opy_.format(bstack111l1_opy_ (u"ࠨࡒࡦࡵࡳࡳࡳࡹࡥࠡࡌࡖࡓࡓࠦࡰࡢࡴࡶࡩࠥ࡫ࡲࡳࡱࡵࠤࠧࡹ")))
  except Exception as e:
    logger.debug(bstack1l1llllll_opy_.format(e))
def bstack11l1ll1l_opy_(hub_url):
  global CONFIG
  url = bstack111l1_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤࡺ")+  hub_url + bstack111l1_opy_ (u"ࠣ࠱ࡦ࡬ࡪࡩ࡫ࠣࡻ")
  headers = {
        bstack111l1_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡸࡾࡶࡥࠨࡼ"): bstack111l1_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ࡽ"),
      }
  proxies = bstack1l11l11l_opy_(CONFIG, url)
  try:
    start_time = time.perf_counter()
    requests.get(url, headers=headers, proxies=proxies, timeout=5)
    latency = time.perf_counter() - start_time
    logger.debug(bstack1lllll1ll1_opy_.format(hub_url, latency))
    return dict(hub_url=hub_url, latency=latency)
  except Exception as e:
    logger.debug(bstack11ll1ll1l_opy_.format(hub_url, e))
def bstack1ll11llll_opy_():
  try:
    global bstack11l1l111l_opy_
    bstack1l1lll11l1_opy_ = bstack1ll111ll_opy_()
    bstack1l1ll1l1l1_opy_ = []
    results = []
    for bstack111l11lll_opy_ in bstack1l1lll11l1_opy_:
      bstack1l1ll1l1l1_opy_.append(bstack1ll1llll1l_opy_(target=bstack11l1ll1l_opy_,args=(bstack111l11lll_opy_,)))
    for t in bstack1l1ll1l1l1_opy_:
      t.start()
    for t in bstack1l1ll1l1l1_opy_:
      results.append(t.join())
    bstack1l1ll11l_opy_ = {}
    for item in results:
      hub_url = item[bstack111l1_opy_ (u"ࠫ࡭ࡻࡢࡠࡷࡵࡰࠬࡾ")]
      latency = item[bstack111l1_opy_ (u"ࠬࡲࡡࡵࡧࡱࡧࡾ࠭ࡿ")]
      bstack1l1ll11l_opy_[hub_url] = latency
    bstack1l11l1l111_opy_ = min(bstack1l1ll11l_opy_, key= lambda x: bstack1l1ll11l_opy_[x])
    bstack11l1l111l_opy_ = bstack1l11l1l111_opy_
    logger.debug(bstack1l1lllll11_opy_.format(bstack1l11l1l111_opy_))
  except Exception as e:
    logger.debug(bstack111l1llll_opy_.format(e))
from bstack_utils.messages import *
from bstack_utils import bstack1l1ll1111_opy_
from bstack_utils.config import Config
from bstack_utils.helper import bstack11l111ll_opy_, bstack1ll1l11111_opy_, bstack1lll1l1ll_opy_, bstack11l1ll1l1_opy_, bstack1ll1l1111l_opy_, \
  Notset, bstack1l1lll1111_opy_, \
  bstack11lllll11_opy_, bstack1ll11l1l1_opy_, bstack11ll11ll1_opy_, bstack111llll11_opy_, bstack1ll1l1ll_opy_, bstack1l1llll1ll_opy_, \
  bstack1l1111l1_opy_, \
  bstack1l1111l1l_opy_, bstack111l1l11l_opy_, bstack1l11lll111_opy_, bstack1l11llll1_opy_, \
  bstack1l11lllll_opy_, bstack111ll1l1_opy_, bstack1ll11llll1_opy_, bstack1111lll11_opy_
from bstack_utils.bstack1llll11l_opy_ import bstack1l1ll111ll_opy_
from bstack_utils.bstack1ll1lll1l1_opy_ import bstack1llll1ll11_opy_
from bstack_utils.bstack1l1llll11l_opy_ import bstack1lll1111l1_opy_, bstack11ll111ll_opy_
from bstack_utils.bstack11111l1l_opy_ import bstack11llllll11_opy_
from bstack_utils.bstack1l11l1l1ll_opy_ import bstack1lll1l11_opy_
from bstack_utils.bstack1lll11l1_opy_ import bstack1lll11l1_opy_
from bstack_utils.proxy import bstack1l11llll_opy_, bstack1l11l11l_opy_, bstack1l11l1ll1l_opy_, bstack111lll1l_opy_
import bstack_utils.bstack1ll1l111_opy_ as bstack1ll111111l_opy_
from browserstack_sdk.bstack1l1lll11l_opy_ import *
from browserstack_sdk.bstack1111l1111_opy_ import *
from bstack_utils.bstack11lll1ll1_opy_ import bstack1ll11l111_opy_
from browserstack_sdk.bstack1l1llll1l1_opy_ import *
import bstack_utils.bstack1lllll1lll_opy_ as bstack1llllll1l1_opy_
import bstack_utils.bstack1lll1l111l_opy_ as bstack1l11l1l1_opy_
bstack1l11111ll_opy_ = bstack111l1_opy_ (u"࠭ࠠࠡ࠱࠭ࠤࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽ࠡࠬ࠲ࡠࡳࠦࠠࡪࡨࠫࡴࡦ࡭ࡥࠡ࠿ࡀࡁࠥࡼ࡯ࡪࡦࠣ࠴࠮ࠦࡻ࡝ࡰࠣࠤࠥࡺࡲࡺࡽ࡟ࡲࠥࡩ࡯࡯ࡵࡷࠤ࡫ࡹࠠ࠾ࠢࡵࡩࡶࡻࡩࡳࡧࠫࡠࠬ࡬ࡳ࡝ࠩࠬ࠿ࡡࡴࠠࠡࠢࠣࠤ࡫ࡹ࠮ࡢࡲࡳࡩࡳࡪࡆࡪ࡮ࡨࡗࡾࡴࡣࠩࡤࡶࡸࡦࡩ࡫ࡠࡲࡤࡸ࡭࠲ࠠࡋࡕࡒࡒ࠳ࡹࡴࡳ࡫ࡱ࡫࡮࡬ࡹࠩࡲࡢ࡭ࡳࡪࡥࡹࠫࠣ࠯ࠥࠨ࠺ࠣࠢ࠮ࠤࡏ࡙ࡏࡏ࠰ࡶࡸࡷ࡯࡮ࡨ࡫ࡩࡽ࠭ࡐࡓࡐࡐ࠱ࡴࡦࡸࡳࡦࠪࠫࡥࡼࡧࡩࡵࠢࡱࡩࡼࡖࡡࡨࡧ࠵࠲ࡪࡼࡡ࡭ࡷࡤࡸࡪ࠮ࠢࠩࠫࠣࡁࡃࠦࡻࡾࠤ࠯ࠤࡡ࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡧࡦࡶࡖࡩࡸࡹࡩࡰࡰࡇࡩࡹࡧࡩ࡭ࡵࠥࢁࡡ࠭ࠩࠪࠫ࡞ࠦ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠢ࡞ࠫࠣ࠯ࠥࠨࠬ࡝࡞ࡱࠦ࠮ࡢ࡮ࠡࠢࠣࠤࢂࡩࡡࡵࡥ࡫ࠬࡪࡾࠩࡼ࡞ࡱࠤࠥࠦࠠࡾ࡞ࡱࠤࠥࢃ࡜࡯ࠢࠣ࠳࠯ࠦ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࠣ࠮࠴࠭ࢀ")
bstack1l1l11llll_opy_ = bstack111l1_opy_ (u"ࠧ࡝ࡰ࠲࠮ࠥࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾ࠢ࠭࠳ࡡࡴࡣࡰࡰࡶࡸࠥࡨࡳࡵࡣࡦ࡯ࡤࡶࡡࡵࡪࠣࡁࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࡟ࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࠱ࡰࡪࡴࡧࡵࡪࠣ࠱ࠥ࠹࡝࡝ࡰࡦࡳࡳࡹࡴࠡࡤࡶࡸࡦࡩ࡫ࡠࡥࡤࡴࡸࠦ࠽ࠡࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࡛ࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻ࠴࡬ࡦࡰࡪࡸ࡭ࠦ࠭ࠡ࠳ࡠࡠࡳࡩ࡯࡯ࡵࡷࠤࡵࡥࡩ࡯ࡦࡨࡼࠥࡃࠠࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻࡡࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡲࡥ࡯ࡩࡷ࡬ࠥ࠳ࠠ࠳࡟࡟ࡲࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸࠣࡁࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡸࡲࡩࡤࡧࠫ࠴࠱ࠦࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡲࡥ࡯ࡩࡷ࡬ࠥ࠳ࠠ࠴ࠫ࡟ࡲࡨࡵ࡮ࡴࡶࠣ࡭ࡲࡶ࡯ࡳࡶࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠴ࡠࡤࡶࡸࡦࡩ࡫ࠡ࠿ࠣࡶࡪࡷࡵࡪࡴࡨࠬࠧࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤࠬ࠿ࡡࡴࡩ࡮ࡲࡲࡶࡹࡥࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶ࠷ࡣࡧࡹࡴࡢࡥ࡮࠲ࡨ࡮ࡲࡰ࡯࡬ࡹࡲ࠴࡬ࡢࡷࡱࡧ࡭ࠦ࠽ࠡࡣࡶࡽࡳࡩࠠࠩ࡮ࡤࡹࡳࡩࡨࡐࡲࡷ࡭ࡴࡴࡳࠪࠢࡀࡂࠥࢁ࡜࡯࡮ࡨࡸࠥࡩࡡࡱࡵ࠾ࡠࡳࡺࡲࡺࠢࡾࡠࡳࡩࡡࡱࡵࠣࡁࠥࡐࡓࡐࡐ࠱ࡴࡦࡸࡳࡦࠪࡥࡷࡹࡧࡣ࡬ࡡࡦࡥࡵࡹࠩ࡝ࡰࠣࠤࢂࠦࡣࡢࡶࡦ࡬࠭࡫ࡸࠪࠢࡾࡠࡳࠦࠠࠡࠢࢀࡠࡳࠦࠠࡳࡧࡷࡹࡷࡴࠠࡢࡹࡤ࡭ࡹࠦࡩ࡮ࡲࡲࡶࡹࡥࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶ࠷ࡣࡧࡹࡴࡢࡥ࡮࠲ࡨ࡮ࡲࡰ࡯࡬ࡹࡲ࠴ࡣࡰࡰࡱࡩࡨࡺࠨࡼ࡞ࡱࠤࠥࠦࠠࡸࡵࡈࡲࡩࡶ࡯ࡪࡰࡷ࠾ࠥࡦࡷࡴࡵ࠽࠳࠴ࡩࡤࡱ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࡁࡦࡥࡵࡹ࠽ࠥࡽࡨࡲࡨࡵࡤࡦࡗࡕࡍࡈࡵ࡭ࡱࡱࡱࡩࡳࡺࠨࡋࡕࡒࡒ࠳ࡹࡴࡳ࡫ࡱ࡫࡮࡬ࡹࠩࡥࡤࡴࡸ࠯ࠩࡾࡢ࠯ࡠࡳࠦࠠࠡࠢ࠱࠲࠳ࡲࡡࡶࡰࡦ࡬ࡔࡶࡴࡪࡱࡱࡷࡡࡴࠠࠡࡿࠬࡠࡳࢃ࡜࡯࠱࠭ࠤࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽ࠡࠬ࠲ࡠࡳ࠭ࢁ")
from ._version import __version__
bstack111ll11ll_opy_ = None
CONFIG = {}
bstack1l111ll1l1_opy_ = {}
bstack1lll11ll11_opy_ = {}
bstack1l1111l111_opy_ = None
bstack1l11ll1ll_opy_ = None
bstack1l1l1ll1ll_opy_ = None
bstack1l11llll1l_opy_ = -1
bstack1ll111l11l_opy_ = 0
bstack1llllll1l_opy_ = bstack1l1111ll1l_opy_
bstack11lll1111_opy_ = 1
bstack1ll11l1l_opy_ = False
bstack1l1l1l1l1_opy_ = False
bstack1l111l1l_opy_ = bstack111l1_opy_ (u"ࠨࠩࢂ")
bstack1111l1ll1_opy_ = bstack111l1_opy_ (u"ࠩࠪࢃ")
bstack1l111ll111_opy_ = False
bstack1l1l111l_opy_ = True
bstack111l111ll_opy_ = bstack111l1_opy_ (u"ࠪࠫࢄ")
bstack1l1ll1l1l_opy_ = []
bstack11l1l111l_opy_ = bstack111l1_opy_ (u"ࠫࠬࢅ")
bstack1111111ll_opy_ = False
bstack1llll1l1l1_opy_ = None
bstack1ll1llll1_opy_ = None
bstack1lll11ll1l_opy_ = None
bstack1ll111lll_opy_ = -1
bstack11l1lll11_opy_ = os.path.join(os.path.expanduser(bstack111l1_opy_ (u"ࠬࢄࠧࢆ")), bstack111l1_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ࢇ"), bstack111l1_opy_ (u"ࠧ࠯ࡴࡲࡦࡴࡺ࠭ࡳࡧࡳࡳࡷࡺ࠭ࡩࡧ࡯ࡴࡪࡸ࠮࡫ࡵࡲࡲࠬ࢈"))
bstack1l111l1111_opy_ = 0
bstack1l1l11111l_opy_ = 0
bstack1ll11111l1_opy_ = []
bstack1l11111l1_opy_ = []
bstack1l11ll111_opy_ = []
bstack1l1l1ll1l1_opy_ = []
bstack1ll11ll1l1_opy_ = bstack111l1_opy_ (u"ࠨࠩࢉ")
bstack111l111l1_opy_ = bstack111l1_opy_ (u"ࠩࠪࢊ")
bstack1l1l1l1l_opy_ = False
bstack1l1l11l11l_opy_ = False
bstack1l111lll1_opy_ = {}
bstack1llll1lll1_opy_ = None
bstack1lll1l1l1l_opy_ = None
bstack1l1l11111_opy_ = None
bstack1lllllll1l_opy_ = None
bstack1l1lll1l1l_opy_ = None
bstack1111l1l1_opy_ = None
bstack1l1lll1l1_opy_ = None
bstack1l111lll1l_opy_ = None
bstack11l1l1lll_opy_ = None
bstack1ll11ll1_opy_ = None
bstack1l1l1ll11_opy_ = None
bstack1l11l11ll1_opy_ = None
bstack1ll1ll1l_opy_ = None
bstack1l1lll1l11_opy_ = None
bstack1ll1ll1lll_opy_ = None
bstack1l111l11l_opy_ = None
bstack1l1l111l11_opy_ = None
bstack1l1l1l111_opy_ = None
bstack1l111111l_opy_ = None
bstack1l1l1l1111_opy_ = None
bstack1l1l1lll_opy_ = None
bstack11ll1lll_opy_ = None
bstack11l11ll1_opy_ = False
bstack1lllll11ll_opy_ = bstack111l1_opy_ (u"ࠥࠦࢋ")
logger = bstack1l1ll1111_opy_.get_logger(__name__, bstack1llllll1l_opy_)
bstack1111ll1l1_opy_ = Config.bstack1l1ll11lll_opy_()
percy = bstack1l11l111_opy_()
bstack1l1l111111_opy_ = bstack1l1ll1ll11_opy_()
bstack1l1111llll_opy_ = bstack1l1llll1l1_opy_()
def bstack1lll1ll1_opy_():
  global CONFIG
  global bstack1l1l1l1l_opy_
  global bstack1111ll1l1_opy_
  bstack1ll1lllll_opy_ = bstack1ll1l1111_opy_(CONFIG)
  if bstack1ll1l1111l_opy_(CONFIG):
    if (bstack111l1_opy_ (u"ࠫࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ࢌ") in bstack1ll1lllll_opy_ and str(bstack1ll1lllll_opy_[bstack111l1_opy_ (u"ࠬࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧࢍ")]).lower() == bstack111l1_opy_ (u"࠭ࡴࡳࡷࡨࠫࢎ")):
      bstack1l1l1l1l_opy_ = True
    bstack1111ll1l1_opy_.bstack1lll1l1l_opy_(bstack1ll1lllll_opy_.get(bstack111l1_opy_ (u"ࠧࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫ࢏"), False))
  else:
    bstack1l1l1l1l_opy_ = True
    bstack1111ll1l1_opy_.bstack1lll1l1l_opy_(True)
def bstack1l1l1l111l_opy_():
  from appium.version import version as appium_version
  return version.parse(appium_version)
def bstack1l1l11l1ll_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack1l111ll1_opy_():
  args = sys.argv
  for i in range(len(args)):
    if bstack111l1_opy_ (u"ࠣ࠯࠰ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡥࡲࡲ࡫࡯ࡧࡧ࡫࡯ࡩࠧ࢐") == args[i].lower() or bstack111l1_opy_ (u"ࠤ࠰࠱ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡴࡦࡪࡩࠥ࢑") == args[i].lower():
      path = args[i + 1]
      sys.argv.remove(args[i])
      sys.argv.remove(path)
      global bstack111l111ll_opy_
      bstack111l111ll_opy_ += bstack111l1_opy_ (u"ࠪ࠱࠲ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡇࡴࡴࡦࡪࡩࡉ࡭ࡱ࡫ࠠࠨ࢒") + path
      return path
  return None
bstack1ll11ll111_opy_ = re.compile(bstack111l1_opy_ (u"ࡶࠧ࠴ࠪࡀ࡞ࠧࡿ࠭࠴ࠪࡀࠫࢀ࠲࠯ࡅࠢ࢓"))
def bstack1l111l1l11_opy_(loader, node):
  value = loader.construct_scalar(node)
  for group in bstack1ll11ll111_opy_.findall(value):
    if group is not None and os.environ.get(group) is not None:
      value = value.replace(bstack111l1_opy_ (u"ࠧࠪࡻࠣ࢔") + group + bstack111l1_opy_ (u"ࠨࡽࠣ࢕"), os.environ.get(group))
  return value
def bstack11l1l1ll1_opy_():
  bstack1l111l1ll1_opy_ = bstack1l111ll1_opy_()
  if bstack1l111l1ll1_opy_ and os.path.exists(os.path.abspath(bstack1l111l1ll1_opy_)):
    fileName = bstack1l111l1ll1_opy_
  if bstack111l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡐࡐࡉࡍࡌࡥࡆࡊࡎࡈࠫ࢖") in os.environ and os.path.exists(
          os.path.abspath(os.environ[bstack111l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡑࡑࡊࡎࡍ࡟ࡇࡋࡏࡉࠬࢗ")])) and not bstack111l1_opy_ (u"ࠩࡩ࡭ࡱ࡫ࡎࡢ࡯ࡨࠫ࢘") in locals():
    fileName = os.environ[bstack111l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡆࡓࡓࡌࡉࡈࡡࡉࡍࡑࡋ࢙ࠧ")]
  if bstack111l1_opy_ (u"ࠫ࡫࡯࡬ࡦࡐࡤࡱࡪ࢚࠭") in locals():
    bstack111ll11_opy_ = os.path.abspath(fileName)
  else:
    bstack111ll11_opy_ = bstack111l1_opy_ (u"࢛ࠬ࠭")
  bstack1ll1ll11_opy_ = os.getcwd()
  bstack11l1l11ll_opy_ = bstack111l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡿ࡭࡭ࠩ࢜")
  bstack1l1l1lllll_opy_ = bstack111l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡹࡢ࡯࡯ࠫ࢝")
  while (not os.path.exists(bstack111ll11_opy_)) and bstack1ll1ll11_opy_ != bstack111l1_opy_ (u"ࠣࠤ࢞"):
    bstack111ll11_opy_ = os.path.join(bstack1ll1ll11_opy_, bstack11l1l11ll_opy_)
    if not os.path.exists(bstack111ll11_opy_):
      bstack111ll11_opy_ = os.path.join(bstack1ll1ll11_opy_, bstack1l1l1lllll_opy_)
    if bstack1ll1ll11_opy_ != os.path.dirname(bstack1ll1ll11_opy_):
      bstack1ll1ll11_opy_ = os.path.dirname(bstack1ll1ll11_opy_)
    else:
      bstack1ll1ll11_opy_ = bstack111l1_opy_ (u"ࠤࠥ࢟")
  if not os.path.exists(bstack111ll11_opy_):
    bstack11l1ll11_opy_(
      bstack1l1l1111l_opy_.format(os.getcwd()))
  try:
    with open(bstack111ll11_opy_, bstack111l1_opy_ (u"ࠪࡶࠬࢠ")) as stream:
      yaml.add_implicit_resolver(bstack111l1_opy_ (u"ࠦࠦࡶࡡࡵࡪࡨࡼࠧࢡ"), bstack1ll11ll111_opy_)
      yaml.add_constructor(bstack111l1_opy_ (u"ࠧࠧࡰࡢࡶ࡫ࡩࡽࠨࢢ"), bstack1l111l1l11_opy_)
      config = yaml.load(stream, yaml.FullLoader)
      return config
  except:
    with open(bstack111ll11_opy_, bstack111l1_opy_ (u"࠭ࡲࠨࢣ")) as stream:
      try:
        config = yaml.safe_load(stream)
        return config
      except yaml.YAMLError as exc:
        bstack11l1ll11_opy_(bstack1lll1ll11l_opy_.format(str(exc)))
def bstack1lll1llll_opy_(config):
  bstack1ll1l11lll_opy_ = bstack1ll1111ll_opy_(config)
  for option in list(bstack1ll1l11lll_opy_):
    if option.lower() in bstack111ll1l11_opy_ and option != bstack111ll1l11_opy_[option.lower()]:
      bstack1ll1l11lll_opy_[bstack111ll1l11_opy_[option.lower()]] = bstack1ll1l11lll_opy_[option]
      del bstack1ll1l11lll_opy_[option]
  return config
def bstack1lllll11l_opy_():
  global bstack1lll11ll11_opy_
  for key, bstack1ll1ll11l_opy_ in bstack11111llll_opy_.items():
    if isinstance(bstack1ll1ll11l_opy_, list):
      for var in bstack1ll1ll11l_opy_:
        if var in os.environ and os.environ[var] and str(os.environ[var]).strip():
          bstack1lll11ll11_opy_[key] = os.environ[var]
          break
    elif bstack1ll1ll11l_opy_ in os.environ and os.environ[bstack1ll1ll11l_opy_] and str(os.environ[bstack1ll1ll11l_opy_]).strip():
      bstack1lll11ll11_opy_[key] = os.environ[bstack1ll1ll11l_opy_]
  if bstack111l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࡤࡏࡄࡆࡐࡗࡍࡋࡏࡅࡓࠩࢤ") in os.environ:
    bstack1lll11ll11_opy_[bstack111l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬࢥ")] = {}
    bstack1lll11ll11_opy_[bstack111l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ࢦ")][bstack111l1_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬࢧ")] = os.environ[bstack111l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡐࡔࡉࡁࡍࡡࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗ࠭ࢨ")]
def bstack1l1111ll1_opy_():
  global bstack1l111ll1l1_opy_
  global bstack111l111ll_opy_
  for idx, val in enumerate(sys.argv):
    if idx < len(sys.argv) and bstack111l1_opy_ (u"ࠬ࠳࠭ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨࢩ").lower() == val.lower():
      bstack1l111ll1l1_opy_[bstack111l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪࢪ")] = {}
      bstack1l111ll1l1_opy_[bstack111l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫࢫ")][bstack111l1_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪࢬ")] = sys.argv[idx + 1]
      del sys.argv[idx:idx + 2]
      break
  for key, bstack1lllll1l11_opy_ in bstack1ll1l11l1_opy_.items():
    if isinstance(bstack1lllll1l11_opy_, list):
      for idx, val in enumerate(sys.argv):
        for var in bstack1lllll1l11_opy_:
          if idx < len(sys.argv) and bstack111l1_opy_ (u"ࠩ࠰࠱ࠬࢭ") + var.lower() == val.lower() and not key in bstack1l111ll1l1_opy_:
            bstack1l111ll1l1_opy_[key] = sys.argv[idx + 1]
            bstack111l111ll_opy_ += bstack111l1_opy_ (u"ࠪࠤ࠲࠳ࠧࢮ") + var + bstack111l1_opy_ (u"ࠫࠥ࠭ࢯ") + sys.argv[idx + 1]
            del sys.argv[idx:idx + 2]
            break
    else:
      for idx, val in enumerate(sys.argv):
        if idx < len(sys.argv) and bstack111l1_opy_ (u"ࠬ࠳࠭ࠨࢰ") + bstack1lllll1l11_opy_.lower() == val.lower() and not key in bstack1l111ll1l1_opy_:
          bstack1l111ll1l1_opy_[key] = sys.argv[idx + 1]
          bstack111l111ll_opy_ += bstack111l1_opy_ (u"࠭ࠠ࠮࠯ࠪࢱ") + bstack1lllll1l11_opy_ + bstack111l1_opy_ (u"ࠧࠡࠩࢲ") + sys.argv[idx + 1]
          del sys.argv[idx:idx + 2]
def bstack11l11l1l_opy_(config):
  bstack1l1ll11111_opy_ = config.keys()
  for bstack1l11l1111l_opy_, bstack1ll1llll_opy_ in bstack1111l1lll_opy_.items():
    if bstack1ll1llll_opy_ in bstack1l1ll11111_opy_:
      config[bstack1l11l1111l_opy_] = config[bstack1ll1llll_opy_]
      del config[bstack1ll1llll_opy_]
  for bstack1l11l1111l_opy_, bstack1ll1llll_opy_ in bstack1ll11ll1ll_opy_.items():
    if isinstance(bstack1ll1llll_opy_, list):
      for bstack1ll11l111l_opy_ in bstack1ll1llll_opy_:
        if bstack1ll11l111l_opy_ in bstack1l1ll11111_opy_:
          config[bstack1l11l1111l_opy_] = config[bstack1ll11l111l_opy_]
          del config[bstack1ll11l111l_opy_]
          break
    elif bstack1ll1llll_opy_ in bstack1l1ll11111_opy_:
      config[bstack1l11l1111l_opy_] = config[bstack1ll1llll_opy_]
      del config[bstack1ll1llll_opy_]
  for bstack1ll11l111l_opy_ in list(config):
    for bstack1l11l11l11_opy_ in bstack1l11l11111_opy_:
      if bstack1ll11l111l_opy_.lower() == bstack1l11l11l11_opy_.lower() and bstack1ll11l111l_opy_ != bstack1l11l11l11_opy_:
        config[bstack1l11l11l11_opy_] = config[bstack1ll11l111l_opy_]
        del config[bstack1ll11l111l_opy_]
  bstack1l1l11l1l_opy_ = [{}]
  if not config.get(bstack111l1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫࢳ")):
    config[bstack111l1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬࢴ")] = [{}]
  bstack1l1l11l1l_opy_ = config[bstack111l1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ࢵ")]
  for platform in bstack1l1l11l1l_opy_:
    for bstack1ll11l111l_opy_ in list(platform):
      for bstack1l11l11l11_opy_ in bstack1l11l11111_opy_:
        if bstack1ll11l111l_opy_.lower() == bstack1l11l11l11_opy_.lower() and bstack1ll11l111l_opy_ != bstack1l11l11l11_opy_:
          platform[bstack1l11l11l11_opy_] = platform[bstack1ll11l111l_opy_]
          del platform[bstack1ll11l111l_opy_]
  for bstack1l11l1111l_opy_, bstack1ll1llll_opy_ in bstack1ll11ll1ll_opy_.items():
    for platform in bstack1l1l11l1l_opy_:
      if isinstance(bstack1ll1llll_opy_, list):
        for bstack1ll11l111l_opy_ in bstack1ll1llll_opy_:
          if bstack1ll11l111l_opy_ in platform:
            platform[bstack1l11l1111l_opy_] = platform[bstack1ll11l111l_opy_]
            del platform[bstack1ll11l111l_opy_]
            break
      elif bstack1ll1llll_opy_ in platform:
        platform[bstack1l11l1111l_opy_] = platform[bstack1ll1llll_opy_]
        del platform[bstack1ll1llll_opy_]
  for bstack11ll1l11_opy_ in bstack1lll1l1ll1_opy_:
    if bstack11ll1l11_opy_ in config:
      if not bstack1lll1l1ll1_opy_[bstack11ll1l11_opy_] in config:
        config[bstack1lll1l1ll1_opy_[bstack11ll1l11_opy_]] = {}
      config[bstack1lll1l1ll1_opy_[bstack11ll1l11_opy_]].update(config[bstack11ll1l11_opy_])
      del config[bstack11ll1l11_opy_]
  for platform in bstack1l1l11l1l_opy_:
    for bstack11ll1l11_opy_ in bstack1lll1l1ll1_opy_:
      if bstack11ll1l11_opy_ in list(platform):
        if not bstack1lll1l1ll1_opy_[bstack11ll1l11_opy_] in platform:
          platform[bstack1lll1l1ll1_opy_[bstack11ll1l11_opy_]] = {}
        platform[bstack1lll1l1ll1_opy_[bstack11ll1l11_opy_]].update(platform[bstack11ll1l11_opy_])
        del platform[bstack11ll1l11_opy_]
  config = bstack1lll1llll_opy_(config)
  return config
def bstack1ll1ll1111_opy_(config):
  global bstack1111l1ll1_opy_
  if bstack1ll1l1111l_opy_(config) and bstack111l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨࢶ") in config and str(config[bstack111l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩࢷ")]).lower() != bstack111l1_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬࢸ"):
    if not bstack111l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫࢹ") in config:
      config[bstack111l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬࢺ")] = {}
    if not config[bstack111l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ࢻ")].get(bstack111l1_opy_ (u"ࠪࡷࡰ࡯ࡰࡃ࡫ࡱࡥࡷࡿࡉ࡯࡫ࡷ࡭ࡦࡲࡩࡴࡣࡷ࡭ࡴࡴࠧࢼ")) and not bstack111l1_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ࢽ") in config[bstack111l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩࢾ")]:
      bstack11l1l11l1_opy_ = datetime.datetime.now()
      bstack1llllllll1_opy_ = bstack11l1l11l1_opy_.strftime(bstack111l1_opy_ (u"࠭ࠥࡥࡡࠨࡦࡤࠫࡈࠦࡏࠪࢿ"))
      hostname = socket.gethostname()
      bstack11l11lll1_opy_ = bstack111l1_opy_ (u"ࠧࠨࣀ").join(random.choices(string.ascii_lowercase + string.digits, k=4))
      identifier = bstack111l1_opy_ (u"ࠨࡽࢀࡣࢀࢃ࡟ࡼࡿࠪࣁ").format(bstack1llllllll1_opy_, hostname, bstack11l11lll1_opy_)
      config[bstack111l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ࣂ")][bstack111l1_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬࣃ")] = identifier
    bstack1111l1ll1_opy_ = config[bstack111l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨࣄ")].get(bstack111l1_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࣅ"))
  return config
def bstack11ll11l1l_opy_():
  bstack11l1lll1l_opy_ =  bstack111llll11_opy_()[bstack111l1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠬࣆ")]
  return bstack11l1lll1l_opy_ if bstack11l1lll1l_opy_ else -1
def bstack111111ll1_opy_(bstack11l1lll1l_opy_):
  global CONFIG
  if not bstack111l1_opy_ (u"ࠧࠥࡽࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࡾࠩࣇ") in CONFIG[bstack111l1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪࣈ")]:
    return
  CONFIG[bstack111l1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫࣉ")] = CONFIG[bstack111l1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ࣊")].replace(
    bstack111l1_opy_ (u"ࠫࠩࢁࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࢂ࠭࣋"),
    str(bstack11l1lll1l_opy_)
  )
def bstack1l11111l1l_opy_():
  global CONFIG
  if not bstack111l1_opy_ (u"ࠬࠪࡻࡅࡃࡗࡉࡤ࡚ࡉࡎࡇࢀࠫ࣌") in CONFIG[bstack111l1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ࣍")]:
    return
  bstack11l1l11l1_opy_ = datetime.datetime.now()
  bstack1llllllll1_opy_ = bstack11l1l11l1_opy_.strftime(bstack111l1_opy_ (u"ࠧࠦࡦ࠰ࠩࡧ࠳ࠥࡉ࠼ࠨࡑࠬ࣎"))
  CONFIG[bstack111l1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴ࣏ࠪ")] = CONFIG[bstack111l1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵ࣐ࠫ")].replace(
    bstack111l1_opy_ (u"ࠪࠨࢀࡊࡁࡕࡇࡢࡘࡎࡓࡅࡾ࣑ࠩ"),
    bstack1llllllll1_opy_
  )
def bstack1lll11lll1_opy_():
  global CONFIG
  if bstack111l1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࣒࠭") in CONFIG and not bool(CONFIG[bstack111l1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸ࣓ࠧ")]):
    del CONFIG[bstack111l1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨࣔ")]
    return
  if not bstack111l1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩࣕ") in CONFIG:
    CONFIG[bstack111l1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪࣖ")] = bstack111l1_opy_ (u"ࠩࠦࠨࢀࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࢁࠬࣗ")
  if bstack111l1_opy_ (u"ࠪࠨࢀࡊࡁࡕࡇࡢࡘࡎࡓࡅࡾࠩࣘ") in CONFIG[bstack111l1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ࣙ")]:
    bstack1l11111l1l_opy_()
    os.environ[bstack111l1_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡤࡉࡏࡎࡄࡌࡒࡊࡊ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠩࣚ")] = CONFIG[bstack111l1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨࣛ")]
  if not bstack111l1_opy_ (u"ࠧࠥࡽࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࡾࠩࣜ") in CONFIG[bstack111l1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪࣝ")]:
    return
  bstack11l1lll1l_opy_ = bstack111l1_opy_ (u"ࠩࠪࣞ")
  bstack1ll111l1l1_opy_ = bstack11ll11l1l_opy_()
  if bstack1ll111l1l1_opy_ != -1:
    bstack11l1lll1l_opy_ = bstack111l1_opy_ (u"ࠪࡇࡎࠦࠧࣟ") + str(bstack1ll111l1l1_opy_)
  if bstack11l1lll1l_opy_ == bstack111l1_opy_ (u"ࠫࠬ࣠"):
    bstack11111lll_opy_ = bstack1ll11l1111_opy_(CONFIG[bstack111l1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ࣡")])
    if bstack11111lll_opy_ != -1:
      bstack11l1lll1l_opy_ = str(bstack11111lll_opy_)
  if bstack11l1lll1l_opy_:
    bstack111111ll1_opy_(bstack11l1lll1l_opy_)
    os.environ[bstack111l1_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡥࡃࡐࡏࡅࡍࡓࡋࡄࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠪ࣢")] = CONFIG[bstack111l1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࣣࠩ")]
def bstack1l1ll1lll1_opy_(bstack1lll111l1_opy_, bstack1l1l11ll1l_opy_, path):
  bstack1lll111ll1_opy_ = {
    bstack111l1_opy_ (u"ࠨ࡫ࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬࣤ"): bstack1l1l11ll1l_opy_
  }
  if os.path.exists(path):
    bstack1lll1l1l1_opy_ = json.load(open(path, bstack111l1_opy_ (u"ࠩࡵࡦࠬࣥ")))
  else:
    bstack1lll1l1l1_opy_ = {}
  bstack1lll1l1l1_opy_[bstack1lll111l1_opy_] = bstack1lll111ll1_opy_
  with open(path, bstack111l1_opy_ (u"ࠥࡻ࠰ࠨࣦ")) as outfile:
    json.dump(bstack1lll1l1l1_opy_, outfile)
def bstack1ll11l1111_opy_(bstack1lll111l1_opy_):
  bstack1lll111l1_opy_ = str(bstack1lll111l1_opy_)
  bstack1lll1lll_opy_ = os.path.join(os.path.expanduser(bstack111l1_opy_ (u"ࠫࢃ࠭ࣧ")), bstack111l1_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬࣨ"))
  try:
    if not os.path.exists(bstack1lll1lll_opy_):
      os.makedirs(bstack1lll1lll_opy_)
    file_path = os.path.join(os.path.expanduser(bstack111l1_opy_ (u"࠭ࡾࠨࣩ")), bstack111l1_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧ࣪"), bstack111l1_opy_ (u"ࠨ࠰ࡥࡹ࡮ࡲࡤ࠮ࡰࡤࡱࡪ࠳ࡣࡢࡥ࡫ࡩ࠳ࡰࡳࡰࡰࠪ࣫"))
    if not os.path.isfile(file_path):
      with open(file_path, bstack111l1_opy_ (u"ࠩࡺࠫ࣬")):
        pass
      with open(file_path, bstack111l1_opy_ (u"ࠥࡻ࠰ࠨ࣭")) as outfile:
        json.dump({}, outfile)
    with open(file_path, bstack111l1_opy_ (u"ࠫࡷ࣮࠭")) as bstack1lllll111l_opy_:
      bstack1llllll11l_opy_ = json.load(bstack1lllll111l_opy_)
    if bstack1lll111l1_opy_ in bstack1llllll11l_opy_:
      bstack1ll1ll11l1_opy_ = bstack1llllll11l_opy_[bstack1lll111l1_opy_][bstack111l1_opy_ (u"ࠬ࡯ࡤࡦࡰࡷ࡭࡫࡯ࡥࡳ࣯ࠩ")]
      bstack1ll1ll111_opy_ = int(bstack1ll1ll11l1_opy_) + 1
      bstack1l1ll1lll1_opy_(bstack1lll111l1_opy_, bstack1ll1ll111_opy_, file_path)
      return bstack1ll1ll111_opy_
    else:
      bstack1l1ll1lll1_opy_(bstack1lll111l1_opy_, 1, file_path)
      return 1
  except Exception as e:
    logger.warn(bstack1ll11l11ll_opy_.format(str(e)))
    return -1
def bstack11llll111_opy_(config):
  if not config[bstack111l1_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨࣰ")] or not config[bstack111l1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࣱࠪ")]:
    return True
  else:
    return False
def bstack11l11l1l1_opy_(config, index=0):
  global bstack1l111ll111_opy_
  bstack1l111l11l1_opy_ = {}
  caps = bstack11l1l1111_opy_ + bstack1ll111ll1_opy_
  if bstack1l111ll111_opy_:
    caps += bstack1ll1l1l111_opy_
  for key in config:
    if key in caps + [bstack111l1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࣲࠫ")]:
      continue
    bstack1l111l11l1_opy_[key] = config[key]
  if bstack111l1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬࣳ") in config:
    for bstack1l1l1llll1_opy_ in config[bstack111l1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ࣴ")][index]:
      if bstack1l1l1llll1_opy_ in caps:
        continue
      bstack1l111l11l1_opy_[bstack1l1l1llll1_opy_] = config[bstack111l1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧࣵ")][index][bstack1l1l1llll1_opy_]
  bstack1l111l11l1_opy_[bstack111l1_opy_ (u"ࠬ࡮࡯ࡴࡶࡑࡥࡲ࡫ࣶࠧ")] = socket.gethostname()
  if bstack111l1_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴࠧࣷ") in bstack1l111l11l1_opy_:
    del (bstack1l111l11l1_opy_[bstack111l1_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࠨࣸ")])
  return bstack1l111l11l1_opy_
def bstack1l1l111l1l_opy_(config):
  global bstack1l111ll111_opy_
  bstack1ll1l1lll1_opy_ = {}
  caps = bstack1ll111ll1_opy_
  if bstack1l111ll111_opy_:
    caps += bstack1ll1l1l111_opy_
  for key in caps:
    if key in config:
      bstack1ll1l1lll1_opy_[key] = config[key]
  return bstack1ll1l1lll1_opy_
def bstack1ll11l1l11_opy_(bstack1l111l11l1_opy_, bstack1ll1l1lll1_opy_):
  bstack11l1l1ll_opy_ = {}
  for key in bstack1l111l11l1_opy_.keys():
    if key in bstack1111l1lll_opy_:
      bstack11l1l1ll_opy_[bstack1111l1lll_opy_[key]] = bstack1l111l11l1_opy_[key]
    else:
      bstack11l1l1ll_opy_[key] = bstack1l111l11l1_opy_[key]
  for key in bstack1ll1l1lll1_opy_:
    if key in bstack1111l1lll_opy_:
      bstack11l1l1ll_opy_[bstack1111l1lll_opy_[key]] = bstack1ll1l1lll1_opy_[key]
    else:
      bstack11l1l1ll_opy_[key] = bstack1ll1l1lll1_opy_[key]
  return bstack11l1l1ll_opy_
def bstack1l11l111ll_opy_(config, index=0):
  global bstack1l111ll111_opy_
  caps = {}
  config = copy.deepcopy(config)
  bstack11ll111l_opy_ = bstack11l111ll_opy_(bstack11l1l1l1l_opy_, config, logger)
  bstack1ll1l1lll1_opy_ = bstack1l1l111l1l_opy_(config)
  bstack1111111l1_opy_ = bstack1ll111ll1_opy_
  bstack1111111l1_opy_ += bstack1l1l1lll1l_opy_
  bstack1ll1l1lll1_opy_ = update(bstack1ll1l1lll1_opy_, bstack11ll111l_opy_)
  if bstack1l111ll111_opy_:
    bstack1111111l1_opy_ += bstack1ll1l1l111_opy_
  if bstack111l1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࣹࠫ") in config:
    if bstack111l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࣺࠧ") in config[bstack111l1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ࣻ")][index]:
      caps[bstack111l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩࣼ")] = config[bstack111l1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨࣽ")][index][bstack111l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫࣾ")]
    if bstack111l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨࣿ") in config[bstack111l1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫऀ")][index]:
      caps[bstack111l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪँ")] = str(config[bstack111l1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ं")][index][bstack111l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬः")])
    bstack1ll1ll1ll1_opy_ = bstack11l111ll_opy_(bstack11l1l1l1l_opy_, config[bstack111l1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨऄ")][index], logger)
    bstack1111111l1_opy_ += list(bstack1ll1ll1ll1_opy_.keys())
    for bstack1l1l1lll11_opy_ in bstack1111111l1_opy_:
      if bstack1l1l1lll11_opy_ in config[bstack111l1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩअ")][index]:
        if bstack1l1l1lll11_opy_ == bstack111l1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩआ"):
          try:
            bstack1ll1ll1ll1_opy_[bstack1l1l1lll11_opy_] = str(config[bstack111l1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫइ")][index][bstack1l1l1lll11_opy_] * 1.0)
          except:
            bstack1ll1ll1ll1_opy_[bstack1l1l1lll11_opy_] = str(config[bstack111l1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬई")][index][bstack1l1l1lll11_opy_])
        else:
          bstack1ll1ll1ll1_opy_[bstack1l1l1lll11_opy_] = config[bstack111l1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭उ")][index][bstack1l1l1lll11_opy_]
        del (config[bstack111l1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧऊ")][index][bstack1l1l1lll11_opy_])
    bstack1ll1l1lll1_opy_ = update(bstack1ll1l1lll1_opy_, bstack1ll1ll1ll1_opy_)
  bstack1l111l11l1_opy_ = bstack11l11l1l1_opy_(config, index)
  for bstack1ll11l111l_opy_ in bstack1ll111ll1_opy_ + list(bstack11ll111l_opy_.keys()):
    if bstack1ll11l111l_opy_ in bstack1l111l11l1_opy_:
      bstack1ll1l1lll1_opy_[bstack1ll11l111l_opy_] = bstack1l111l11l1_opy_[bstack1ll11l111l_opy_]
      del (bstack1l111l11l1_opy_[bstack1ll11l111l_opy_])
  if bstack1l1lll1111_opy_(config):
    bstack1l111l11l1_opy_[bstack111l1_opy_ (u"ࠬࡻࡳࡦ࡙࠶ࡇࠬऋ")] = True
    caps.update(bstack1ll1l1lll1_opy_)
    caps[bstack111l1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧऌ")] = bstack1l111l11l1_opy_
  else:
    bstack1l111l11l1_opy_[bstack111l1_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉࠧऍ")] = False
    caps.update(bstack1ll11l1l11_opy_(bstack1l111l11l1_opy_, bstack1ll1l1lll1_opy_))
    if bstack111l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ऎ") in caps:
      caps[bstack111l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪए")] = caps[bstack111l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨऐ")]
      del (caps[bstack111l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩऑ")])
    if bstack111l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ऒ") in caps:
      caps[bstack111l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨओ")] = caps[bstack111l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨऔ")]
      del (caps[bstack111l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩक")])
  return caps
def bstack1l1ll11ll1_opy_():
  global bstack11l1l111l_opy_
  if bstack1l1l11l1ll_opy_() <= version.parse(bstack111l1_opy_ (u"ࠩ࠶࠲࠶࠹࠮࠱ࠩख")):
    if bstack11l1l111l_opy_ != bstack111l1_opy_ (u"ࠪࠫग"):
      return bstack111l1_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳ࠧघ") + bstack11l1l111l_opy_ + bstack111l1_opy_ (u"ࠧࡀ࠸࠱࠱ࡺࡨ࠴࡮ࡵࡣࠤङ")
    return bstack1lll1lll11_opy_
  if bstack11l1l111l_opy_ != bstack111l1_opy_ (u"࠭ࠧच"):
    return bstack111l1_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤछ") + bstack11l1l111l_opy_ + bstack111l1_opy_ (u"ࠣ࠱ࡺࡨ࠴࡮ࡵࡣࠤज")
  return bstack11l1lllll_opy_
def bstack111l1lll_opy_(options):
  return hasattr(options, bstack111l1_opy_ (u"ࠩࡶࡩࡹࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵࡻࠪझ"))
def update(d, u):
  for k, v in u.items():
    if isinstance(v, collections.abc.Mapping):
      d[k] = update(d.get(k, {}), v)
    else:
      if isinstance(v, list):
        d[k] = d.get(k, []) + v
      else:
        d[k] = v
  return d
def bstack1ll1lll1l_opy_(options, bstack111ll11l1_opy_):
  for bstack11ll1l1l1_opy_ in bstack111ll11l1_opy_:
    if bstack11ll1l1l1_opy_ in [bstack111l1_opy_ (u"ࠪࡥࡷ࡭ࡳࠨञ"), bstack111l1_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨट")]:
      continue
    if bstack11ll1l1l1_opy_ in options._experimental_options:
      options._experimental_options[bstack11ll1l1l1_opy_] = update(options._experimental_options[bstack11ll1l1l1_opy_],
                                                         bstack111ll11l1_opy_[bstack11ll1l1l1_opy_])
    else:
      options.add_experimental_option(bstack11ll1l1l1_opy_, bstack111ll11l1_opy_[bstack11ll1l1l1_opy_])
  if bstack111l1_opy_ (u"ࠬࡧࡲࡨࡵࠪठ") in bstack111ll11l1_opy_:
    for arg in bstack111ll11l1_opy_[bstack111l1_opy_ (u"࠭ࡡࡳࡩࡶࠫड")]:
      options.add_argument(arg)
    del (bstack111ll11l1_opy_[bstack111l1_opy_ (u"ࠧࡢࡴࡪࡷࠬढ")])
  if bstack111l1_opy_ (u"ࠨࡧࡻࡸࡪࡴࡳࡪࡱࡱࡷࠬण") in bstack111ll11l1_opy_:
    for ext in bstack111ll11l1_opy_[bstack111l1_opy_ (u"ࠩࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࡸ࠭त")]:
      options.add_extension(ext)
    del (bstack111ll11l1_opy_[bstack111l1_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧथ")])
def bstack1llll1l1_opy_(options, bstack1ll111l1l_opy_):
  if bstack111l1_opy_ (u"ࠫࡵࡸࡥࡧࡵࠪद") in bstack1ll111l1l_opy_:
    for bstack1lllll1ll_opy_ in bstack1ll111l1l_opy_[bstack111l1_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫध")]:
      if bstack1lllll1ll_opy_ in options._preferences:
        options._preferences[bstack1lllll1ll_opy_] = update(options._preferences[bstack1lllll1ll_opy_], bstack1ll111l1l_opy_[bstack111l1_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬन")][bstack1lllll1ll_opy_])
      else:
        options.set_preference(bstack1lllll1ll_opy_, bstack1ll111l1l_opy_[bstack111l1_opy_ (u"ࠧࡱࡴࡨࡪࡸ࠭ऩ")][bstack1lllll1ll_opy_])
  if bstack111l1_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭प") in bstack1ll111l1l_opy_:
    for arg in bstack1ll111l1l_opy_[bstack111l1_opy_ (u"ࠩࡤࡶ࡬ࡹࠧफ")]:
      options.add_argument(arg)
def bstack1lll1ll1l_opy_(options, bstack11lll11ll_opy_):
  if bstack111l1_opy_ (u"ࠪࡻࡪࡨࡶࡪࡧࡺࠫब") in bstack11lll11ll_opy_:
    options.use_webview(bool(bstack11lll11ll_opy_[bstack111l1_opy_ (u"ࠫࡼ࡫ࡢࡷ࡫ࡨࡻࠬभ")]))
  bstack1ll1lll1l_opy_(options, bstack11lll11ll_opy_)
def bstack1111llll1_opy_(options, bstack1ll1l1ll1l_opy_):
  for bstack11lllll1ll_opy_ in bstack1ll1l1ll1l_opy_:
    if bstack11lllll1ll_opy_ in [bstack111l1_opy_ (u"ࠬࡺࡥࡤࡪࡱࡳࡱࡵࡧࡺࡒࡵࡩࡻ࡯ࡥࡸࠩम"), bstack111l1_opy_ (u"࠭ࡡࡳࡩࡶࠫय")]:
      continue
    options.set_capability(bstack11lllll1ll_opy_, bstack1ll1l1ll1l_opy_[bstack11lllll1ll_opy_])
  if bstack111l1_opy_ (u"ࠧࡢࡴࡪࡷࠬर") in bstack1ll1l1ll1l_opy_:
    for arg in bstack1ll1l1ll1l_opy_[bstack111l1_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ऱ")]:
      options.add_argument(arg)
  if bstack111l1_opy_ (u"ࠩࡷࡩࡨ࡮࡮ࡰ࡮ࡲ࡫ࡾࡖࡲࡦࡸ࡬ࡩࡼ࠭ल") in bstack1ll1l1ll1l_opy_:
    options.bstack1l11llllll_opy_(bool(bstack1ll1l1ll1l_opy_[bstack111l1_opy_ (u"ࠪࡸࡪࡩࡨ࡯ࡱ࡯ࡳ࡬ࡿࡐࡳࡧࡹ࡭ࡪࡽࠧळ")]))
def bstack11llllll1l_opy_(options, bstack1ll1lll11_opy_):
  for bstack1l1l1ll1_opy_ in bstack1ll1lll11_opy_:
    if bstack1l1l1ll1_opy_ in [bstack111l1_opy_ (u"ࠫࡦࡪࡤࡪࡶ࡬ࡳࡳࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨऴ"), bstack111l1_opy_ (u"ࠬࡧࡲࡨࡵࠪव")]:
      continue
    options._options[bstack1l1l1ll1_opy_] = bstack1ll1lll11_opy_[bstack1l1l1ll1_opy_]
  if bstack111l1_opy_ (u"࠭ࡡࡥࡦ࡬ࡸ࡮ࡵ࡮ࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪश") in bstack1ll1lll11_opy_:
    for bstack1llll1l11_opy_ in bstack1ll1lll11_opy_[bstack111l1_opy_ (u"ࠧࡢࡦࡧ࡭ࡹ࡯࡯࡯ࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫष")]:
      options.bstack1l11ll111l_opy_(
        bstack1llll1l11_opy_, bstack1ll1lll11_opy_[bstack111l1_opy_ (u"ࠨࡣࡧࡨ࡮ࡺࡩࡰࡰࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬस")][bstack1llll1l11_opy_])
  if bstack111l1_opy_ (u"ࠩࡤࡶ࡬ࡹࠧह") in bstack1ll1lll11_opy_:
    for arg in bstack1ll1lll11_opy_[bstack111l1_opy_ (u"ࠪࡥࡷ࡭ࡳࠨऺ")]:
      options.add_argument(arg)
def bstack1l11l1l11l_opy_(options, caps):
  if not hasattr(options, bstack111l1_opy_ (u"ࠫࡐࡋ࡙ࠨऻ")):
    return
  if options.KEY == bstack111l1_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵ़ࠪ") and options.KEY in caps:
    bstack1ll1lll1l_opy_(options, caps[bstack111l1_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫऽ")])
  elif options.KEY == bstack111l1_opy_ (u"ࠧ࡮ࡱࡽ࠾࡫࡯ࡲࡦࡨࡲࡼࡔࡶࡴࡪࡱࡱࡷࠬा") and options.KEY in caps:
    bstack1llll1l1_opy_(options, caps[bstack111l1_opy_ (u"ࠨ࡯ࡲࡾ࠿࡬ࡩࡳࡧࡩࡳࡽࡕࡰࡵ࡫ࡲࡲࡸ࠭ि")])
  elif options.KEY == bstack111l1_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪ࠰ࡲࡴࡹ࡯࡯࡯ࡵࠪी") and options.KEY in caps:
    bstack1111llll1_opy_(options, caps[bstack111l1_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫࠱ࡳࡵࡺࡩࡰࡰࡶࠫु")])
  elif options.KEY == bstack111l1_opy_ (u"ࠫࡲࡹ࠺ࡦࡦࡪࡩࡔࡶࡴࡪࡱࡱࡷࠬू") and options.KEY in caps:
    bstack1lll1ll1l_opy_(options, caps[bstack111l1_opy_ (u"ࠬࡳࡳ࠻ࡧࡧ࡫ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ृ")])
  elif options.KEY == bstack111l1_opy_ (u"࠭ࡳࡦ࠼࡬ࡩࡔࡶࡴࡪࡱࡱࡷࠬॄ") and options.KEY in caps:
    bstack11llllll1l_opy_(options, caps[bstack111l1_opy_ (u"ࠧࡴࡧ࠽࡭ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ॅ")])
def bstack1lll1ll1l1_opy_(caps):
  global bstack1l111ll111_opy_
  if isinstance(os.environ.get(bstack111l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩॆ")), str):
    bstack1l111ll111_opy_ = eval(os.getenv(bstack111l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇࠪे")))
  if bstack1l111ll111_opy_:
    if bstack1l1l1l111l_opy_() < version.parse(bstack111l1_opy_ (u"ࠪ࠶࠳࠹࠮࠱ࠩै")):
      return None
    else:
      from appium.options.common.base import AppiumOptions
      options = AppiumOptions().load_capabilities(caps)
      return options
  else:
    browser = bstack111l1_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࠫॉ")
    if bstack111l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪॊ") in caps:
      browser = caps[bstack111l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫो")]
    elif bstack111l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨौ") in caps:
      browser = caps[bstack111l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳ्ࠩ")]
    browser = str(browser).lower()
    if browser == bstack111l1_opy_ (u"ࠩ࡬ࡴ࡭ࡵ࡮ࡦࠩॎ") or browser == bstack111l1_opy_ (u"ࠪ࡭ࡵࡧࡤࠨॏ"):
      browser = bstack111l1_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬ࠫॐ")
    if browser == bstack111l1_opy_ (u"ࠬࡹࡡ࡮ࡵࡸࡲ࡬࠭॑"):
      browser = bstack111l1_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪ॒࠭")
    if browser not in [bstack111l1_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࠧ॓"), bstack111l1_opy_ (u"ࠨࡧࡧ࡫ࡪ࠭॔"), bstack111l1_opy_ (u"ࠩ࡬ࡩࠬॕ"), bstack111l1_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫ࠪॖ"), bstack111l1_opy_ (u"ࠫ࡫࡯ࡲࡦࡨࡲࡼࠬॗ")]:
      return None
    try:
      package = bstack111l1_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࠮ࡸࡧࡥࡨࡷ࡯ࡶࡦࡴ࠱ࡿࢂ࠴࡯ࡱࡶ࡬ࡳࡳࡹࠧक़").format(browser)
      name = bstack111l1_opy_ (u"࠭ࡏࡱࡶ࡬ࡳࡳࡹࠧख़")
      browser_options = getattr(__import__(package, fromlist=[name]), name)
      options = browser_options()
      if not bstack111l1lll_opy_(options):
        return None
      for bstack1ll11l111l_opy_ in caps.keys():
        options.set_capability(bstack1ll11l111l_opy_, caps[bstack1ll11l111l_opy_])
      bstack1l11l1l11l_opy_(options, caps)
      return options
    except Exception as e:
      logger.debug(str(e))
      return None
def bstack111ll1ll1_opy_(options, bstack1lll111lll_opy_):
  if not bstack111l1lll_opy_(options):
    return
  for bstack1ll11l111l_opy_ in bstack1lll111lll_opy_.keys():
    if bstack1ll11l111l_opy_ in bstack1l1l1lll1l_opy_:
      continue
    if bstack1ll11l111l_opy_ in options._caps and type(options._caps[bstack1ll11l111l_opy_]) in [dict, list]:
      options._caps[bstack1ll11l111l_opy_] = update(options._caps[bstack1ll11l111l_opy_], bstack1lll111lll_opy_[bstack1ll11l111l_opy_])
    else:
      options.set_capability(bstack1ll11l111l_opy_, bstack1lll111lll_opy_[bstack1ll11l111l_opy_])
  bstack1l11l1l11l_opy_(options, bstack1lll111lll_opy_)
  if bstack111l1_opy_ (u"ࠧ࡮ࡱࡽ࠾ࡩ࡫ࡢࡶࡩࡪࡩࡷࡇࡤࡥࡴࡨࡷࡸ࠭ग़") in options._caps:
    if options._caps[bstack111l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ज़")] and options._caps[bstack111l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧड़")].lower() != bstack111l1_opy_ (u"ࠪࡪ࡮ࡸࡥࡧࡱࡻࠫढ़"):
      del options._caps[bstack111l1_opy_ (u"ࠫࡲࡵࡺ࠻ࡦࡨࡦࡺ࡭ࡧࡦࡴࡄࡨࡩࡸࡥࡴࡵࠪफ़")]
def bstack11l111l11_opy_(proxy_config):
  if bstack111l1_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩय़") in proxy_config:
    proxy_config[bstack111l1_opy_ (u"࠭ࡳࡴ࡮ࡓࡶࡴࡾࡹࠨॠ")] = proxy_config[bstack111l1_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫॡ")]
    del (proxy_config[bstack111l1_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬॢ")])
  if bstack111l1_opy_ (u"ࠩࡳࡶࡴࡾࡹࡕࡻࡳࡩࠬॣ") in proxy_config and proxy_config[bstack111l1_opy_ (u"ࠪࡴࡷࡵࡸࡺࡖࡼࡴࡪ࠭।")].lower() != bstack111l1_opy_ (u"ࠫࡩ࡯ࡲࡦࡥࡷࠫ॥"):
    proxy_config[bstack111l1_opy_ (u"ࠬࡶࡲࡰࡺࡼࡘࡾࡶࡥࠨ०")] = bstack111l1_opy_ (u"࠭࡭ࡢࡰࡸࡥࡱ࠭१")
  if bstack111l1_opy_ (u"ࠧࡱࡴࡲࡼࡾࡇࡵࡵࡱࡦࡳࡳ࡬ࡩࡨࡗࡵࡰࠬ२") in proxy_config:
    proxy_config[bstack111l1_opy_ (u"ࠨࡲࡵࡳࡽࡿࡔࡺࡲࡨࠫ३")] = bstack111l1_opy_ (u"ࠩࡳࡥࡨ࠭४")
  return proxy_config
def bstack1l1ll1l11_opy_(config, proxy):
  from selenium.webdriver.common.proxy import Proxy
  if not bstack111l1_opy_ (u"ࠪࡴࡷࡵࡸࡺࠩ५") in config:
    return proxy
  config[bstack111l1_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࠪ६")] = bstack11l111l11_opy_(config[bstack111l1_opy_ (u"ࠬࡶࡲࡰࡺࡼࠫ७")])
  if proxy == None:
    proxy = Proxy(config[bstack111l1_opy_ (u"࠭ࡰࡳࡱࡻࡽࠬ८")])
  return proxy
def bstack1lll1ll111_opy_(self):
  global CONFIG
  global bstack1l11l11ll1_opy_
  try:
    proxy = bstack1l11l1ll1l_opy_(CONFIG)
    if proxy:
      if proxy.endswith(bstack111l1_opy_ (u"ࠧ࠯ࡲࡤࡧࠬ९")):
        proxies = bstack1l11llll_opy_(proxy, bstack1l1ll11ll1_opy_())
        if len(proxies) > 0:
          protocol, bstack11l1111l_opy_ = proxies.popitem()
          if bstack111l1_opy_ (u"ࠣ࠼࠲࠳ࠧ॰") in bstack11l1111l_opy_:
            return bstack11l1111l_opy_
          else:
            return bstack111l1_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࠥॱ") + bstack11l1111l_opy_
      else:
        return proxy
  except Exception as e:
    logger.error(bstack111l1_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡰࡳࡱࡻࡽࠥࡻࡲ࡭ࠢ࠽ࠤࢀࢃࠢॲ").format(str(e)))
  return bstack1l11l11ll1_opy_(self)
def bstack1ll11lll1_opy_():
  global CONFIG
  return bstack111lll1l_opy_(CONFIG) and bstack1l1llll1ll_opy_() and bstack1l1l11l1ll_opy_() >= version.parse(bstack1l11ll1l1_opy_)
def bstack1l1llll1l_opy_():
  global CONFIG
  return (bstack111l1_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧॳ") in CONFIG or bstack111l1_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩॴ") in CONFIG) and bstack1l1111l1_opy_()
def bstack1ll1111ll_opy_(config):
  bstack1ll1l11lll_opy_ = {}
  if bstack111l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪॵ") in config:
    bstack1ll1l11lll_opy_ = config[bstack111l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫॶ")]
  if bstack111l1_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧॷ") in config:
    bstack1ll1l11lll_opy_ = config[bstack111l1_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨॸ")]
  proxy = bstack1l11l1ll1l_opy_(config)
  if proxy:
    if proxy.endswith(bstack111l1_opy_ (u"ࠪ࠲ࡵࡧࡣࠨॹ")) and os.path.isfile(proxy):
      bstack1ll1l11lll_opy_[bstack111l1_opy_ (u"ࠫ࠲ࡶࡡࡤ࠯ࡩ࡭ࡱ࡫ࠧॺ")] = proxy
    else:
      parsed_url = None
      if proxy.endswith(bstack111l1_opy_ (u"ࠬ࠴ࡰࡢࡥࠪॻ")):
        proxies = bstack1l11l11l_opy_(config, bstack1l1ll11ll1_opy_())
        if len(proxies) > 0:
          protocol, bstack11l1111l_opy_ = proxies.popitem()
          if bstack111l1_opy_ (u"ࠨ࠺࠰࠱ࠥॼ") in bstack11l1111l_opy_:
            parsed_url = urlparse(bstack11l1111l_opy_)
          else:
            parsed_url = urlparse(protocol + bstack111l1_opy_ (u"ࠢ࠻࠱࠲ࠦॽ") + bstack11l1111l_opy_)
      else:
        parsed_url = urlparse(proxy)
      if parsed_url and parsed_url.hostname: bstack1ll1l11lll_opy_[bstack111l1_opy_ (u"ࠨࡲࡵࡳࡽࡿࡈࡰࡵࡷࠫॾ")] = str(parsed_url.hostname)
      if parsed_url and parsed_url.port: bstack1ll1l11lll_opy_[bstack111l1_opy_ (u"ࠩࡳࡶࡴࡾࡹࡑࡱࡵࡸࠬॿ")] = str(parsed_url.port)
      if parsed_url and parsed_url.username: bstack1ll1l11lll_opy_[bstack111l1_opy_ (u"ࠪࡴࡷࡵࡸࡺࡗࡶࡩࡷ࠭ঀ")] = str(parsed_url.username)
      if parsed_url and parsed_url.password: bstack1ll1l11lll_opy_[bstack111l1_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡓࡥࡸࡹࠧঁ")] = str(parsed_url.password)
  return bstack1ll1l11lll_opy_
def bstack1ll1l1111_opy_(config):
  if bstack111l1_opy_ (u"ࠬࡺࡥࡴࡶࡆࡳࡳࡺࡥࡹࡶࡒࡴࡹ࡯࡯࡯ࡵࠪং") in config:
    return config[bstack111l1_opy_ (u"࠭ࡴࡦࡵࡷࡇࡴࡴࡴࡦࡺࡷࡓࡵࡺࡩࡰࡰࡶࠫঃ")]
  return {}
def bstack1111lll1l_opy_(caps):
  global bstack1111l1ll1_opy_
  if bstack111l1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨ঄") in caps:
    caps[bstack111l1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩঅ")][bstack111l1_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࠨআ")] = True
    if bstack1111l1ll1_opy_:
      caps[bstack111l1_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫই")][bstack111l1_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ঈ")] = bstack1111l1ll1_opy_
  else:
    caps[bstack111l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡱࡵࡣࡢ࡮ࠪউ")] = True
    if bstack1111l1ll1_opy_:
      caps[bstack111l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧঊ")] = bstack1111l1ll1_opy_
def bstack1111ll11l_opy_():
  global CONFIG
  if not bstack1ll1l1111l_opy_(CONFIG):
    return
  if bstack111l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫঋ") in CONFIG and bstack1ll11llll1_opy_(CONFIG[bstack111l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬঌ")]):
    if (
      bstack111l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭঍") in CONFIG
      and bstack1ll11llll1_opy_(CONFIG[bstack111l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧ঎")].get(bstack111l1_opy_ (u"ࠫࡸࡱࡩࡱࡄ࡬ࡲࡦࡸࡹࡊࡰ࡬ࡸ࡮ࡧ࡬ࡪࡵࡤࡸ࡮ࡵ࡮ࠨএ")))
    ):
      logger.debug(bstack111l1_opy_ (u"ࠧࡒ࡯ࡤࡣ࡯ࠤࡧ࡯࡮ࡢࡴࡼࠤࡳࡵࡴࠡࡵࡷࡥࡷࡺࡥࡥࠢࡤࡷࠥࡹ࡫ࡪࡲࡅ࡭ࡳࡧࡲࡺࡋࡱ࡭ࡹ࡯ࡡ࡭࡫ࡶࡥࡹ࡯࡯࡯ࠢ࡬ࡷࠥ࡫࡮ࡢࡤ࡯ࡩࡩࠨঐ"))
      return
    bstack1ll1l11lll_opy_ = bstack1ll1111ll_opy_(CONFIG)
    bstack11l1ll11l_opy_(CONFIG[bstack111l1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩ঑")], bstack1ll1l11lll_opy_)
def bstack11l1ll11l_opy_(key, bstack1ll1l11lll_opy_):
  global bstack111ll11ll_opy_
  logger.info(bstack1l1l1111l1_opy_)
  try:
    bstack111ll11ll_opy_ = Local()
    bstack1ll1l11l11_opy_ = {bstack111l1_opy_ (u"ࠧ࡬ࡧࡼࠫ঒"): key}
    bstack1ll1l11l11_opy_.update(bstack1ll1l11lll_opy_)
    logger.debug(bstack1lll1l111_opy_.format(str(bstack1ll1l11l11_opy_)))
    bstack111ll11ll_opy_.start(**bstack1ll1l11l11_opy_)
    if bstack111ll11ll_opy_.isRunning():
      logger.info(bstack1lll11ll_opy_)
  except Exception as e:
    bstack11l1ll11_opy_(bstack11ll1l11l_opy_.format(str(e)))
def bstack1ll1lll11l_opy_():
  global bstack111ll11ll_opy_
  if bstack111ll11ll_opy_.isRunning():
    logger.info(bstack11l11111_opy_)
    bstack111ll11ll_opy_.stop()
  bstack111ll11ll_opy_ = None
def bstack1l111llll_opy_(bstack1llll11111_opy_=[]):
  global CONFIG
  bstack1l1l111ll_opy_ = []
  bstack111l1111l_opy_ = [bstack111l1_opy_ (u"ࠨࡱࡶࠫও"), bstack111l1_opy_ (u"ࠩࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠬঔ"), bstack111l1_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧক"), bstack111l1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭খ"), bstack111l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪগ"), bstack111l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧঘ")]
  try:
    for err in bstack1llll11111_opy_:
      bstack1l11l11l1_opy_ = {}
      for k in bstack111l1111l_opy_:
        val = CONFIG[bstack111l1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪঙ")][int(err[bstack111l1_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧচ")])].get(k)
        if val:
          bstack1l11l11l1_opy_[k] = val
      if(err[bstack111l1_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨছ")] != bstack111l1_opy_ (u"ࠪࠫজ")):
        bstack1l11l11l1_opy_[bstack111l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡵࠪঝ")] = {
          err[bstack111l1_opy_ (u"ࠬࡴࡡ࡮ࡧࠪঞ")]: err[bstack111l1_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬট")]
        }
        bstack1l1l111ll_opy_.append(bstack1l11l11l1_opy_)
  except Exception as e:
    logger.debug(bstack111l1_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡩࡳࡷࡳࡡࡵࡶ࡬ࡲ࡬ࠦࡤࡢࡶࡤࠤ࡫ࡵࡲࠡࡧࡹࡩࡳࡺ࠺ࠡࠩঠ") + str(e))
  finally:
    return bstack1l1l111ll_opy_
def bstack111l1l1l1_opy_(file_name):
  bstack1ll111l111_opy_ = []
  try:
    bstack1l1l111lll_opy_ = os.path.join(tempfile.gettempdir(), file_name)
    if os.path.exists(bstack1l1l111lll_opy_):
      with open(bstack1l1l111lll_opy_) as f:
        bstack1l1ll11l1_opy_ = json.load(f)
        bstack1ll111l111_opy_ = bstack1l1ll11l1_opy_
      os.remove(bstack1l1l111lll_opy_)
    return bstack1ll111l111_opy_
  except Exception as e:
    logger.debug(bstack111l1_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡪ࡮ࡴࡤࡪࡰࡪࠤࡪࡸࡲࡰࡴࠣࡰ࡮ࡹࡴ࠻ࠢࠪড") + str(e))
    return bstack1ll111l111_opy_
def bstack1l1llll1_opy_():
  global bstack1lllll11ll_opy_
  global bstack1l1ll1l1l_opy_
  global bstack1ll11111l1_opy_
  global bstack1l11111l1_opy_
  global bstack1l11ll111_opy_
  global bstack111l111l1_opy_
  global CONFIG
  bstack1l111l1l1l_opy_ = os.environ.get(bstack111l1_opy_ (u"ࠩࡉࡖࡆࡓࡅࡘࡑࡕࡏࡤ࡛ࡓࡆࡆࠪঢ"))
  if bstack1l111l1l1l_opy_ in [bstack111l1_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩণ"), bstack111l1_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪত")]:
    bstack1ll1llllll_opy_()
  percy.shutdown()
  if bstack1lllll11ll_opy_:
    logger.warning(bstack111lllll1_opy_.format(str(bstack1lllll11ll_opy_)))
  else:
    try:
      bstack1lll1l1l1_opy_ = bstack11lllll11_opy_(bstack111l1_opy_ (u"ࠬ࠴ࡢࡴࡶࡤࡧࡰ࠳ࡣࡰࡰࡩ࡭࡬࠴ࡪࡴࡱࡱࠫথ"), logger)
      if bstack1lll1l1l1_opy_.get(bstack111l1_opy_ (u"࠭࡮ࡶࡦࡪࡩࡤࡲ࡯ࡤࡣ࡯ࠫদ")) and bstack1lll1l1l1_opy_.get(bstack111l1_opy_ (u"ࠧ࡯ࡷࡧ࡫ࡪࡥ࡬ࡰࡥࡤࡰࠬধ")).get(bstack111l1_opy_ (u"ࠨࡪࡲࡷࡹࡴࡡ࡮ࡧࠪন")):
        logger.warning(bstack111lllll1_opy_.format(str(bstack1lll1l1l1_opy_[bstack111l1_opy_ (u"ࠩࡱࡹࡩ࡭ࡥࡠ࡮ࡲࡧࡦࡲࠧ঩")][bstack111l1_opy_ (u"ࠪ࡬ࡴࡹࡴ࡯ࡣࡰࡩࠬপ")])))
    except Exception as e:
      logger.error(e)
  logger.info(bstack11ll1ll1_opy_)
  global bstack111ll11ll_opy_
  if bstack111ll11ll_opy_:
    bstack1ll1lll11l_opy_()
  try:
    for driver in bstack1l1ll1l1l_opy_:
      driver.quit()
  except Exception as e:
    pass
  logger.info(bstack11l1l1l1_opy_)
  if bstack111l111l1_opy_ == bstack111l1_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪফ"):
    bstack1l11ll111_opy_ = bstack111l1l1l1_opy_(bstack111l1_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࡣࡪࡸࡲࡰࡴࡢࡰ࡮ࡹࡴ࠯࡬ࡶࡳࡳ࠭ব"))
  if bstack111l111l1_opy_ == bstack111l1_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ভ") and len(bstack1l11111l1_opy_) == 0:
    bstack1l11111l1_opy_ = bstack111l1l1l1_opy_(bstack111l1_opy_ (u"ࠧࡱࡹࡢࡴࡾࡺࡥࡴࡶࡢࡩࡷࡸ࡯ࡳࡡ࡯࡭ࡸࡺ࠮࡫ࡵࡲࡲࠬম"))
    if len(bstack1l11111l1_opy_) == 0:
      bstack1l11111l1_opy_ = bstack111l1l1l1_opy_(bstack111l1_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡠࡲࡳࡴࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵ࠰࡭ࡷࡴࡴࠧয"))
  bstack1ll1ll111l_opy_ = bstack111l1_opy_ (u"ࠩࠪর")
  if len(bstack1ll11111l1_opy_) > 0:
    bstack1ll1ll111l_opy_ = bstack1l111llll_opy_(bstack1ll11111l1_opy_)
  elif len(bstack1l11111l1_opy_) > 0:
    bstack1ll1ll111l_opy_ = bstack1l111llll_opy_(bstack1l11111l1_opy_)
  elif len(bstack1l11ll111_opy_) > 0:
    bstack1ll1ll111l_opy_ = bstack1l111llll_opy_(bstack1l11ll111_opy_)
  elif len(bstack1l1l1ll1l1_opy_) > 0:
    bstack1ll1ll111l_opy_ = bstack1l111llll_opy_(bstack1l1l1ll1l1_opy_)
  if bool(bstack1ll1ll111l_opy_):
    bstack1l1l11ll11_opy_(bstack1ll1ll111l_opy_)
  else:
    bstack1l1l11ll11_opy_()
  bstack1ll11l1l1_opy_(bstack1l1l1ll111_opy_, logger)
  bstack1l1ll1111_opy_.bstack1111l111_opy_(CONFIG)
  if len(bstack1l11ll111_opy_) > 0:
    sys.exit(len(bstack1l11ll111_opy_))
def bstack1l111lll_opy_(bstack1l11l1l1l1_opy_, frame):
  global bstack1111ll1l1_opy_
  logger.error(bstack1l1111111_opy_)
  bstack1111ll1l1_opy_.bstack1lll11lll_opy_(bstack111l1_opy_ (u"ࠪࡷࡩࡱࡋࡪ࡮࡯ࡒࡴ࠭঱"), bstack1l11l1l1l1_opy_)
  if hasattr(signal, bstack111l1_opy_ (u"ࠫࡘ࡯ࡧ࡯ࡣ࡯ࡷࠬল")):
    bstack1111ll1l1_opy_.bstack1lll11lll_opy_(bstack111l1_opy_ (u"ࠬࡹࡤ࡬ࡍ࡬ࡰࡱ࡙ࡩࡨࡰࡤࡰࠬ঳"), signal.Signals(bstack1l11l1l1l1_opy_).name)
  else:
    bstack1111ll1l1_opy_.bstack1lll11lll_opy_(bstack111l1_opy_ (u"࠭ࡳࡥ࡭ࡎ࡭ࡱࡲࡓࡪࡩࡱࡥࡱ࠭঴"), bstack111l1_opy_ (u"ࠧࡔࡋࡊ࡙ࡓࡑࡎࡐ࡙ࡑࠫ঵"))
  bstack1l111l1l1l_opy_ = os.environ.get(bstack111l1_opy_ (u"ࠨࡈࡕࡅࡒࡋࡗࡐࡔࡎࡣ࡚࡙ࡅࡅࠩশ"))
  if bstack1l111l1l1l_opy_ == bstack111l1_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩষ"):
    bstack11llllll11_opy_.stop(bstack1111ll1l1_opy_.get_property(bstack111l1_opy_ (u"ࠪࡷࡩࡱࡋࡪ࡮࡯ࡗ࡮࡭࡮ࡢ࡮ࠪস")))
  bstack1l1llll1_opy_()
  sys.exit(1)
def bstack11l1ll11_opy_(err):
  logger.critical(bstack1llll111ll_opy_.format(str(err)))
  bstack1l1l11ll11_opy_(bstack1llll111ll_opy_.format(str(err)), True)
  atexit.unregister(bstack1l1llll1_opy_)
  bstack1ll1llllll_opy_()
  sys.exit(1)
def bstack1ll11l11l_opy_(error, message):
  logger.critical(str(error))
  logger.critical(message)
  bstack1l1l11ll11_opy_(message, True)
  atexit.unregister(bstack1l1llll1_opy_)
  bstack1ll1llllll_opy_()
  sys.exit(1)
def bstack11lllllll_opy_():
  global CONFIG
  global bstack1l111ll1l1_opy_
  global bstack1lll11ll11_opy_
  global bstack1l1l111l_opy_
  CONFIG = bstack11l1l1ll1_opy_()
  load_dotenv(CONFIG.get(bstack111l1_opy_ (u"ࠫࡪࡴࡶࡇ࡫࡯ࡩࠬহ")))
  bstack1lllll11l_opy_()
  bstack1l1111ll1_opy_()
  CONFIG = bstack11l11l1l_opy_(CONFIG)
  update(CONFIG, bstack1lll11ll11_opy_)
  update(CONFIG, bstack1l111ll1l1_opy_)
  CONFIG = bstack1ll1ll1111_opy_(CONFIG)
  bstack1l1l111l_opy_ = bstack1ll1l1111l_opy_(CONFIG)
  os.environ[bstack111l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࠨ঺")] = bstack1l1l111l_opy_.__str__()
  bstack1111ll1l1_opy_.bstack1lll11lll_opy_(bstack111l1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡳࡦࡵࡶ࡭ࡴࡴࠧ঻"), bstack1l1l111l_opy_)
  if (bstack111l1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧ়ࠪ") in CONFIG and bstack111l1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫঽ") in bstack1l111ll1l1_opy_) or (
          bstack111l1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬা") in CONFIG and bstack111l1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ি") not in bstack1lll11ll11_opy_):
    if os.getenv(bstack111l1_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡣࡈࡕࡍࡃࡋࡑࡉࡉࡥࡂࡖࡋࡏࡈࡤࡏࡄࠨী")):
      CONFIG[bstack111l1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧু")] = os.getenv(bstack111l1_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡥࡃࡐࡏࡅࡍࡓࡋࡄࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠪূ"))
    else:
      bstack1lll11lll1_opy_()
  elif (bstack111l1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪৃ") not in CONFIG and bstack111l1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪৄ") in CONFIG) or (
          bstack111l1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬ৅") in bstack1lll11ll11_opy_ and bstack111l1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭৆") not in bstack1l111ll1l1_opy_):
    del (CONFIG[bstack111l1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ে")])
  if bstack11llll111_opy_(CONFIG):
    bstack11l1ll11_opy_(bstack1l1l1111ll_opy_)
  bstack111l1l1l_opy_()
  bstack1ll11lllll_opy_()
  if bstack1l111ll111_opy_:
    CONFIG[bstack111l1_opy_ (u"ࠬࡧࡰࡱࠩৈ")] = bstack1l11lll11_opy_(CONFIG)
    logger.info(bstack1ll1l1ll1_opy_.format(CONFIG[bstack111l1_opy_ (u"࠭ࡡࡱࡲࠪ৉")]))
  if not bstack1l1l111l_opy_:
    CONFIG[bstack111l1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ৊")] = [{}]
def bstack111111l11_opy_(config, bstack1lllllll11_opy_):
  global CONFIG
  global bstack1l111ll111_opy_
  CONFIG = config
  bstack1l111ll111_opy_ = bstack1lllllll11_opy_
def bstack1ll11lllll_opy_():
  global CONFIG
  global bstack1l111ll111_opy_
  if bstack111l1_opy_ (u"ࠨࡣࡳࡴࠬো") in CONFIG:
    try:
      from appium import version
    except Exception as e:
      bstack1ll11l11l_opy_(e, bstack1l1111lll1_opy_)
    bstack1l111ll111_opy_ = True
    bstack1111ll1l1_opy_.bstack1lll11lll_opy_(bstack111l1_opy_ (u"ࠩࡤࡴࡵࡥࡡࡶࡶࡲࡱࡦࡺࡥࠨৌ"), True)
def bstack1l11lll11_opy_(config):
  bstack1lll11l11_opy_ = bstack111l1_opy_ (u"্ࠪࠫ")
  app = config[bstack111l1_opy_ (u"ࠫࡦࡶࡰࠨৎ")]
  if isinstance(app, str):
    if os.path.splitext(app)[1] in bstack111l1lll1_opy_:
      if os.path.exists(app):
        bstack1lll11l11_opy_ = bstack11l111l1l_opy_(config, app)
      elif bstack1l1l11l111_opy_(app):
        bstack1lll11l11_opy_ = app
      else:
        bstack11l1ll11_opy_(bstack11lll1l1_opy_.format(app))
    else:
      if bstack1l1l11l111_opy_(app):
        bstack1lll11l11_opy_ = app
      elif os.path.exists(app):
        bstack1lll11l11_opy_ = bstack11l111l1l_opy_(app)
      else:
        bstack11l1ll11_opy_(bstack1l1l1l1l1l_opy_)
  else:
    if len(app) > 2:
      bstack11l1ll11_opy_(bstack1l1lll111_opy_)
    elif len(app) == 2:
      if bstack111l1_opy_ (u"ࠬࡶࡡࡵࡪࠪ৏") in app and bstack111l1_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲࡥࡩࡥࠩ৐") in app:
        if os.path.exists(app[bstack111l1_opy_ (u"ࠧࡱࡣࡷ࡬ࠬ৑")]):
          bstack1lll11l11_opy_ = bstack11l111l1l_opy_(config, app[bstack111l1_opy_ (u"ࠨࡲࡤࡸ࡭࠭৒")], app[bstack111l1_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡡ࡬ࡨࠬ৓")])
        else:
          bstack11l1ll11_opy_(bstack11lll1l1_opy_.format(app))
      else:
        bstack11l1ll11_opy_(bstack1l1lll111_opy_)
    else:
      for key in app:
        if key in bstack1l1lllll1l_opy_:
          if key == bstack111l1_opy_ (u"ࠪࡴࡦࡺࡨࠨ৔"):
            if os.path.exists(app[key]):
              bstack1lll11l11_opy_ = bstack11l111l1l_opy_(config, app[key])
            else:
              bstack11l1ll11_opy_(bstack11lll1l1_opy_.format(app))
          else:
            bstack1lll11l11_opy_ = app[key]
        else:
          bstack11l1ll11_opy_(bstack11111111_opy_)
  return bstack1lll11l11_opy_
def bstack1l1l11l111_opy_(bstack1lll11l11_opy_):
  import re
  bstack1ll1l1l1_opy_ = re.compile(bstack111l1_opy_ (u"ࡶࠧࡤ࡛ࡢ࠯ࡽࡅ࠲ࡠ࠰࠮࠻࡟ࡣ࠳ࡢ࠭࡞ࠬࠧࠦ৕"))
  bstack1llllll111_opy_ = re.compile(bstack111l1_opy_ (u"ࡷࠨ࡞࡜ࡣ࠰ࡾࡆ࠳࡚࠱࠯࠼ࡠࡤ࠴࡜࠮࡟࠭࠳ࡠࡧ࠭ࡻࡃ࠰࡞࠵࠳࠹࡝ࡡ࠱ࡠ࠲ࡣࠪࠥࠤ৖"))
  if bstack111l1_opy_ (u"࠭ࡢࡴ࠼࠲࠳ࠬৗ") in bstack1lll11l11_opy_ or re.fullmatch(bstack1ll1l1l1_opy_, bstack1lll11l11_opy_) or re.fullmatch(bstack1llllll111_opy_, bstack1lll11l11_opy_):
    return True
  else:
    return False
def bstack11l111l1l_opy_(config, path, bstack11lll111_opy_=None):
  import requests
  from requests_toolbelt.multipart.encoder import MultipartEncoder
  import hashlib
  md5_hash = hashlib.md5(open(os.path.abspath(path), bstack111l1_opy_ (u"ࠧࡳࡤࠪ৘")).read()).hexdigest()
  bstack1llll111l1_opy_ = bstack1l1ll11ll_opy_(md5_hash)
  bstack1lll11l11_opy_ = None
  if bstack1llll111l1_opy_:
    logger.info(bstack1l1l1ll11l_opy_.format(bstack1llll111l1_opy_, md5_hash))
    return bstack1llll111l1_opy_
  bstack1ll111ll1l_opy_ = MultipartEncoder(
    fields={
      bstack111l1_opy_ (u"ࠨࡨ࡬ࡰࡪ࠭৙"): (os.path.basename(path), open(os.path.abspath(path), bstack111l1_opy_ (u"ࠩࡵࡦࠬ৚")), bstack111l1_opy_ (u"ࠪࡸࡪࡾࡴ࠰ࡲ࡯ࡥ࡮ࡴࠧ৛")),
      bstack111l1_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡣ࡮ࡪࠧড়"): bstack11lll111_opy_
    }
  )
  response = requests.post(bstack1ll11111ll_opy_, data=bstack1ll111ll1l_opy_,
                           headers={bstack111l1_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡔࡺࡲࡨࠫঢ়"): bstack1ll111ll1l_opy_.content_type},
                           auth=(config[bstack111l1_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨ৞")], config[bstack111l1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪয়")]))
  try:
    res = json.loads(response.text)
    bstack1lll11l11_opy_ = res[bstack111l1_opy_ (u"ࠨࡣࡳࡴࡤࡻࡲ࡭ࠩৠ")]
    logger.info(bstack11lllllll1_opy_.format(bstack1lll11l11_opy_))
    bstack11111l11l_opy_(md5_hash, bstack1lll11l11_opy_)
  except ValueError as err:
    bstack11l1ll11_opy_(bstack11lll1ll_opy_.format(str(err)))
  return bstack1lll11l11_opy_
def bstack111l1l1l_opy_(framework_name=None, args=None):
  global CONFIG
  global bstack11lll1111_opy_
  bstack11l1llll_opy_ = 1
  bstack11llllll1_opy_ = 1
  if bstack111l1_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩৡ") in CONFIG:
    bstack11llllll1_opy_ = CONFIG[bstack111l1_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪৢ")]
  else:
    bstack11llllll1_opy_ = bstack111l1l1ll_opy_(framework_name, args) or 1
  if bstack111l1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧৣ") in CONFIG:
    bstack11l1llll_opy_ = len(CONFIG[bstack111l1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ৤")])
  bstack11lll1111_opy_ = int(bstack11llllll1_opy_) * int(bstack11l1llll_opy_)
def bstack111l1l1ll_opy_(framework_name, args):
  if framework_name == bstack1111ll1ll_opy_ and args and bstack111l1_opy_ (u"࠭࠭࠮ࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠫ৥") in args:
      bstack1ll1111l1_opy_ = args.index(bstack111l1_opy_ (u"ࠧ࠮࠯ࡳࡶࡴࡩࡥࡴࡵࡨࡷࠬ০"))
      return int(args[bstack1ll1111l1_opy_ + 1]) or 1
  return 1
def bstack1l1ll11ll_opy_(md5_hash):
  bstack1ll1lll1_opy_ = os.path.join(os.path.expanduser(bstack111l1_opy_ (u"ࠨࢀࠪ১")), bstack111l1_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩ২"), bstack111l1_opy_ (u"ࠪࡥࡵࡶࡕࡱ࡮ࡲࡥࡩࡓࡄ࠶ࡊࡤࡷ࡭࠴ࡪࡴࡱࡱࠫ৩"))
  if os.path.exists(bstack1ll1lll1_opy_):
    bstack1l111ll1l_opy_ = json.load(open(bstack1ll1lll1_opy_, bstack111l1_opy_ (u"ࠫࡷࡨࠧ৪")))
    if md5_hash in bstack1l111ll1l_opy_:
      bstack1l11ll1l1l_opy_ = bstack1l111ll1l_opy_[md5_hash]
      bstack1llll11ll1_opy_ = datetime.datetime.now()
      bstack1lll1l1l11_opy_ = datetime.datetime.strptime(bstack1l11ll1l1l_opy_[bstack111l1_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨ৫")], bstack111l1_opy_ (u"࠭ࠥࡥ࠱ࠨࡱ࠴࡙ࠫࠡࠧࡋ࠾ࠪࡓ࠺ࠦࡕࠪ৬"))
      if (bstack1llll11ll1_opy_ - bstack1lll1l1l11_opy_).days > 30:
        return None
      elif version.parse(str(__version__)) > version.parse(bstack1l11ll1l1l_opy_[bstack111l1_opy_ (u"ࠧࡴࡦ࡮ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ৭")]):
        return None
      return bstack1l11ll1l1l_opy_[bstack111l1_opy_ (u"ࠨ࡫ࡧࠫ৮")]
  else:
    return None
def bstack11111l11l_opy_(md5_hash, bstack1lll11l11_opy_):
  bstack1lll1lll_opy_ = os.path.join(os.path.expanduser(bstack111l1_opy_ (u"ࠩࢁࠫ৯")), bstack111l1_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪৰ"))
  if not os.path.exists(bstack1lll1lll_opy_):
    os.makedirs(bstack1lll1lll_opy_)
  bstack1ll1lll1_opy_ = os.path.join(os.path.expanduser(bstack111l1_opy_ (u"ࠫࢃ࠭ৱ")), bstack111l1_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬ৲"), bstack111l1_opy_ (u"࠭ࡡࡱࡲࡘࡴࡱࡵࡡࡥࡏࡇ࠹ࡍࡧࡳࡩ࠰࡭ࡷࡴࡴࠧ৳"))
  bstack1l1ll1ll_opy_ = {
    bstack111l1_opy_ (u"ࠧࡪࡦࠪ৴"): bstack1lll11l11_opy_,
    bstack111l1_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫ৵"): datetime.datetime.strftime(datetime.datetime.now(), bstack111l1_opy_ (u"ࠩࠨࡨ࠴ࠫ࡭࠰ࠧ࡜ࠤࠪࡎ࠺ࠦࡏ࠽ࠩࡘ࠭৶")),
    bstack111l1_opy_ (u"ࠪࡷࡩࡱ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ৷"): str(__version__)
  }
  if os.path.exists(bstack1ll1lll1_opy_):
    bstack1l111ll1l_opy_ = json.load(open(bstack1ll1lll1_opy_, bstack111l1_opy_ (u"ࠫࡷࡨࠧ৸")))
  else:
    bstack1l111ll1l_opy_ = {}
  bstack1l111ll1l_opy_[md5_hash] = bstack1l1ll1ll_opy_
  with open(bstack1ll1lll1_opy_, bstack111l1_opy_ (u"ࠧࡽࠫࠣ৹")) as outfile:
    json.dump(bstack1l111ll1l_opy_, outfile)
def bstack1l1ll1l1ll_opy_(self):
  return
def bstack111111111_opy_(self):
  return
def bstack1ll111ll11_opy_(self):
  global bstack1ll1ll1l_opy_
  bstack1ll1ll1l_opy_(self)
def bstack1111ll1l_opy_():
  global bstack1lll11ll1l_opy_
  bstack1lll11ll1l_opy_ = True
def bstack1l11lll11l_opy_(self):
  global bstack1l111l1l_opy_
  global bstack1l1111l111_opy_
  global bstack1lll1l1l1l_opy_
  try:
    if bstack111l1_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭৺") in bstack1l111l1l_opy_ and self.session_id != None and bstack11l1ll1l1_opy_(threading.current_thread(), bstack111l1_opy_ (u"ࠧࡵࡧࡶࡸࡘࡺࡡࡵࡷࡶࠫ৻"), bstack111l1_opy_ (u"ࠨࠩৼ")) != bstack111l1_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪ৽"):
      bstack1l111lllll_opy_ = bstack111l1_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪ৾") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack111l1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ৿")
      if bstack1l111lllll_opy_ == bstack111l1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ਀"):
        bstack1l11lllll_opy_(logger)
      if self != None:
        bstack1lll1111l1_opy_(self, bstack1l111lllll_opy_, bstack111l1_opy_ (u"࠭ࠬࠡࠩਁ").join(threading.current_thread().bstackTestErrorMessages))
    threading.current_thread().testStatus = bstack111l1_opy_ (u"ࠧࠨਂ")
    if bstack111l1_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨਃ") in bstack1l111l1l_opy_ and getattr(threading.current_thread(), bstack111l1_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ਄"), None):
      bstack1l1lllllll_opy_.bstack111l11ll1_opy_(self, bstack1l111lll1_opy_, logger, wait=True)
    if bstack111l1_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪਅ") in bstack1l111l1l_opy_:
      if not threading.currentThread().behave_test_status:
        bstack1lll1111l1_opy_(self, bstack111l1_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠦਆ"))
      bstack1l11l1l1_opy_.bstack1ll111l1_opy_(self)
  except Exception as e:
    logger.debug(bstack111l1_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡱࡦࡸ࡫ࡪࡰࡪࠤࡸࡺࡡࡵࡷࡶ࠾ࠥࠨਇ") + str(e))
  bstack1lll1l1l1l_opy_(self)
  self.session_id = None
def bstack1ll11ll11_opy_(self, *args, **kwargs):
  try:
    from selenium.webdriver.remote.remote_connection import RemoteConnection
    from bstack_utils.helper import bstack1l11l1ll_opy_
    global bstack1l111l1l_opy_
    command_executor = kwargs.get(bstack111l1_opy_ (u"࠭ࡣࡰ࡯ࡰࡥࡳࡪ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳࠩਈ"), bstack111l1_opy_ (u"ࠧࠨਉ"))
    bstack111llll1_opy_ = False
    if type(command_executor) == str and bstack111l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠫਊ") in command_executor:
      bstack111llll1_opy_ = True
    elif isinstance(command_executor, RemoteConnection) and bstack111l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱࠬ਋") in str(getattr(command_executor, bstack111l1_opy_ (u"ࠪࡣࡺࡸ࡬ࠨ਌"), bstack111l1_opy_ (u"ࠫࠬ਍"))):
      bstack111llll1_opy_ = True
    else:
      return bstack1llll1lll1_opy_(self, *args, **kwargs)
    if bstack111llll1_opy_:
      if kwargs.get(bstack111l1_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡸ࠭਎")):
        kwargs[bstack111l1_opy_ (u"࠭࡯ࡱࡶ࡬ࡳࡳࡹࠧਏ")] = bstack1l11l1ll_opy_(kwargs[bstack111l1_opy_ (u"ࠧࡰࡲࡷ࡭ࡴࡴࡳࠨਐ")], bstack1l111l1l_opy_)
      elif kwargs.get(bstack111l1_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨ਑")):
        kwargs[bstack111l1_opy_ (u"ࠩࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩ਒")] = bstack1l11l1ll_opy_(kwargs[bstack111l1_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪਓ")], bstack1l111l1l_opy_)
  except Exception as e:
    logger.error(bstack111l1_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡫࡮ࠡࡲࡵࡳࡨ࡫ࡳࡴ࡫ࡱ࡫࡙ࠥࡄࡌࠢࡦࡥࡵࡹ࠺ࠡࡽࢀࠦਔ").format(str(e)))
  return bstack1llll1lll1_opy_(self, *args, **kwargs)
def bstack11ll1llll_opy_(self, command_executor=bstack111l1_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࠳࠴࠷࠲࠸࠰࠳࠲࠵࠴࠱࠻࠶࠷࠸࠹ࠨਕ"), *args, **kwargs):
  bstack1l1111ll11_opy_ = bstack1ll11ll11_opy_(self, command_executor=command_executor, *args, **kwargs)
  if not bstack1lll1l11_opy_.on():
    return bstack1l1111ll11_opy_
  try:
    logger.debug(bstack111l1_opy_ (u"࠭ࡃࡰ࡯ࡰࡥࡳࡪࠠࡆࡺࡨࡧࡺࡺ࡯ࡳࠢࡺ࡬ࡪࡴࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣ࡭ࡸࠦࡦࡢ࡮ࡶࡩࠥ࠳ࠠࡼࡿࠪਖ").format(str(command_executor)))
    logger.debug(bstack111l1_opy_ (u"ࠧࡉࡷࡥࠤ࡚ࡘࡌࠡ࡫ࡶࠤ࠲ࠦࡻࡾࠩਗ").format(str(command_executor._url)))
    from selenium.webdriver.remote.remote_connection import RemoteConnection
    if isinstance(command_executor, RemoteConnection) and bstack111l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠫਘ") in command_executor._url:
      bstack1111ll1l1_opy_.bstack1lll11lll_opy_(bstack111l1_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡶࡩࡸࡹࡩࡰࡰࠪਙ"), True)
  except:
    pass
  if (isinstance(command_executor, str) and bstack111l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠭ਚ") in command_executor):
    bstack1111ll1l1_opy_.bstack1lll11lll_opy_(bstack111l1_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠬਛ"), True)
  threading.current_thread().bstackSessionDriver = self
  bstack11llllll11_opy_.bstack111lll111_opy_(self)
  return bstack1l1111ll11_opy_
def bstack1ll11111_opy_(args):
  return bstack111l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷ࠭ਜ") in str(args)
def bstack1l1llllll1_opy_(self, driver_command, *args, **kwargs):
  global bstack1l1l1l1111_opy_
  global bstack11l11ll1_opy_
  bstack1lll1ll11_opy_ = bstack11l1ll1l1_opy_(threading.current_thread(), bstack111l1_opy_ (u"࠭ࡩࡴࡃ࠴࠵ࡾ࡚ࡥࡴࡶࠪਝ"), None) and bstack11l1ll1l1_opy_(
          threading.current_thread(), bstack111l1_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭ਞ"), None)
  bstack1l111l111_opy_ = getattr(self, bstack111l1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡂ࠳࠴ࡽࡘ࡮࡯ࡶ࡮ࡧࡗࡨࡧ࡮ࠨਟ"), None) != None and getattr(self, bstack111l1_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡃ࠴࠵ࡾ࡙ࡨࡰࡷ࡯ࡨࡘࡩࡡ࡯ࠩਠ"), None) == True
  if not bstack11l11ll1_opy_ and bstack1l1l111l_opy_ and bstack111l1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪਡ") in CONFIG and CONFIG[bstack111l1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫਢ")] == True and bstack1lll11l1_opy_.bstack1l1l11l11_opy_(driver_command) and (bstack1l111l111_opy_ or bstack1lll1ll11_opy_) and not bstack1ll11111_opy_(args):
    try:
      bstack11l11ll1_opy_ = True
      logger.debug(bstack111l1_opy_ (u"ࠬࡖࡥࡳࡨࡲࡶࡲ࡯࡮ࡨࠢࡶࡧࡦࡴࠠࡧࡱࡵࠤࢀࢃࠧਣ").format(driver_command))
      logger.debug(perform_scan(self, driver_command=driver_command))
    except Exception as err:
      logger.debug(bstack111l1_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡳࡩࡷ࡬࡯ࡳ࡯ࠣࡷࡨࡧ࡮ࠡࡽࢀࠫਤ").format(str(err)))
    bstack11l11ll1_opy_ = False
  response = bstack1l1l1l1111_opy_(self, driver_command, *args, **kwargs)
  if (bstack111l1_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ਥ") in str(bstack1l111l1l_opy_).lower() or bstack111l1_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨਦ") in str(bstack1l111l1l_opy_).lower()) and bstack1lll1l11_opy_.on():
    try:
      if driver_command == bstack111l1_opy_ (u"ࠩࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹ࠭ਧ"):
        bstack11llllll11_opy_.bstack11ll11l1_opy_({
            bstack111l1_opy_ (u"ࠪ࡭ࡲࡧࡧࡦࠩਨ"): response[bstack111l1_opy_ (u"ࠫࡻࡧ࡬ࡶࡧࠪ਩")],
            bstack111l1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬਪ"): bstack11llllll11_opy_.current_test_uuid() if bstack11llllll11_opy_.current_test_uuid() else bstack1lll1l11_opy_.current_hook_uuid()
        })
    except:
      pass
  return response
def bstack1lllll1l1l_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
  global CONFIG
  global bstack1l1111l111_opy_
  global bstack1l11llll1l_opy_
  global bstack1l1l1ll1ll_opy_
  global bstack1ll11l1l_opy_
  global bstack1l1l1l1l1_opy_
  global bstack1l111l1l_opy_
  global bstack1llll1lll1_opy_
  global bstack1l1ll1l1l_opy_
  global bstack1ll111lll_opy_
  global bstack1l111lll1_opy_
  CONFIG[bstack111l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨਫ")] = str(bstack1l111l1l_opy_) + str(__version__)
  command_executor = bstack1l1ll11ll1_opy_()
  logger.debug(bstack1l11ll11l1_opy_.format(command_executor))
  proxy = bstack1l1ll1l11_opy_(CONFIG, proxy)
  bstack1l111lll11_opy_ = 0 if bstack1l11llll1l_opy_ < 0 else bstack1l11llll1l_opy_
  try:
    if bstack1ll11l1l_opy_ is True:
      bstack1l111lll11_opy_ = int(multiprocessing.current_process().name)
    elif bstack1l1l1l1l1_opy_ is True:
      bstack1l111lll11_opy_ = int(threading.current_thread().name)
  except:
    bstack1l111lll11_opy_ = 0
  bstack1lll111lll_opy_ = bstack1l11l111ll_opy_(CONFIG, bstack1l111lll11_opy_)
  logger.debug(bstack1l1llll111_opy_.format(str(bstack1lll111lll_opy_)))
  if bstack111l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫਬ") in CONFIG and bstack1ll11llll1_opy_(CONFIG[bstack111l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬਭ")]):
    bstack1111lll1l_opy_(bstack1lll111lll_opy_)
  if bstack1ll111111l_opy_.bstack1l1l111ll1_opy_(CONFIG, bstack1l111lll11_opy_) and bstack1ll111111l_opy_.bstack11111l11_opy_(bstack1lll111lll_opy_, options, desired_capabilities):
    threading.current_thread().a11yPlatform = True
    bstack1ll111111l_opy_.set_capabilities(bstack1lll111lll_opy_, CONFIG)
  if desired_capabilities:
    bstack1l1l1111_opy_ = bstack11l11l1l_opy_(desired_capabilities)
    bstack1l1l1111_opy_[bstack111l1_opy_ (u"ࠩࡸࡷࡪ࡝࠳ࡄࠩਮ")] = bstack1l1lll1111_opy_(CONFIG)
    bstack1l11l11l1l_opy_ = bstack1l11l111ll_opy_(bstack1l1l1111_opy_)
    if bstack1l11l11l1l_opy_:
      bstack1lll111lll_opy_ = update(bstack1l11l11l1l_opy_, bstack1lll111lll_opy_)
    desired_capabilities = None
  if options:
    bstack111ll1ll1_opy_(options, bstack1lll111lll_opy_)
  if not options:
    options = bstack1lll1ll1l1_opy_(bstack1lll111lll_opy_)
  bstack1l111lll1_opy_ = CONFIG.get(bstack111l1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ਯ"))[bstack1l111lll11_opy_]
  if proxy and bstack1l1l11l1ll_opy_() >= version.parse(bstack111l1_opy_ (u"ࠫ࠹࠴࠱࠱࠰࠳ࠫਰ")):
    options.proxy(proxy)
  if options and bstack1l1l11l1ll_opy_() >= version.parse(bstack111l1_opy_ (u"ࠬ࠹࠮࠹࠰࠳ࠫ਱")):
    desired_capabilities = None
  if (
          not options and not desired_capabilities
  ) or (
          bstack1l1l11l1ll_opy_() < version.parse(bstack111l1_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬਲ")) and not desired_capabilities
  ):
    desired_capabilities = {}
    desired_capabilities.update(bstack1lll111lll_opy_)
  logger.info(bstack1llllll11_opy_)
  if bstack1l1l11l1ll_opy_() >= version.parse(bstack111l1_opy_ (u"ࠧ࠵࠰࠴࠴࠳࠶ࠧਲ਼")):
    bstack1llll1lll1_opy_(self, command_executor=command_executor,
              options=options, keep_alive=keep_alive, file_detector=file_detector)
  elif bstack1l1l11l1ll_opy_() >= version.parse(bstack111l1_opy_ (u"ࠨ࠵࠱࠼࠳࠶ࠧ਴")):
    bstack1llll1lll1_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities, options=options,
              browser_profile=browser_profile, proxy=proxy,
              keep_alive=keep_alive, file_detector=file_detector)
  elif bstack1l1l11l1ll_opy_() >= version.parse(bstack111l1_opy_ (u"ࠩ࠵࠲࠺࠹࠮࠱ࠩਵ")):
    bstack1llll1lll1_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities,
              browser_profile=browser_profile, proxy=proxy,
              keep_alive=keep_alive, file_detector=file_detector)
  else:
    bstack1llll1lll1_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities,
              browser_profile=browser_profile, proxy=proxy,
              keep_alive=keep_alive)
  try:
    bstack1lll1llll1_opy_ = bstack111l1_opy_ (u"ࠪࠫਸ਼")
    if bstack1l1l11l1ll_opy_() >= version.parse(bstack111l1_opy_ (u"ࠫ࠹࠴࠰࠯࠲ࡥ࠵ࠬ਷")):
      bstack1lll1llll1_opy_ = self.caps.get(bstack111l1_opy_ (u"ࠧࡵࡰࡵ࡫ࡰࡥࡱࡎࡵࡣࡗࡵࡰࠧਸ"))
    else:
      bstack1lll1llll1_opy_ = self.capabilities.get(bstack111l1_opy_ (u"ࠨ࡯ࡱࡶ࡬ࡱࡦࡲࡈࡶࡤࡘࡶࡱࠨਹ"))
    if bstack1lll1llll1_opy_:
      bstack1l11lll111_opy_(bstack1lll1llll1_opy_)
      if bstack1l1l11l1ll_opy_() <= version.parse(bstack111l1_opy_ (u"ࠧ࠴࠰࠴࠷࠳࠶ࠧ਺")):
        self.command_executor._url = bstack111l1_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤ਻") + bstack11l1l111l_opy_ + bstack111l1_opy_ (u"ࠤ࠽࠼࠵࠵ࡷࡥ࠱࡫ࡹࡧࠨ਼")
      else:
        self.command_executor._url = bstack111l1_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࠧ਽") + bstack1lll1llll1_opy_ + bstack111l1_opy_ (u"ࠦ࠴ࡽࡤ࠰ࡪࡸࡦࠧਾ")
      logger.debug(bstack11llll11l_opy_.format(bstack1lll1llll1_opy_))
    else:
      logger.debug(bstack1l111111_opy_.format(bstack111l1_opy_ (u"ࠧࡕࡰࡵ࡫ࡰࡥࡱࠦࡈࡶࡤࠣࡲࡴࡺࠠࡧࡱࡸࡲࡩࠨਿ")))
  except Exception as e:
    logger.debug(bstack1l111111_opy_.format(e))
  if bstack111l1_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬੀ") in bstack1l111l1l_opy_:
    bstack1l11lll1_opy_(bstack1l11llll1l_opy_, bstack1ll111lll_opy_)
  bstack1l1111l111_opy_ = self.session_id
  if bstack111l1_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧੁ") in bstack1l111l1l_opy_ or bstack111l1_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨੂ") in bstack1l111l1l_opy_ or bstack111l1_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ੃") in bstack1l111l1l_opy_:
    threading.current_thread().bstackSessionId = self.session_id
    threading.current_thread().bstackSessionDriver = self
    threading.current_thread().bstackTestErrorMessages = []
    bstack11llllll11_opy_.bstack111lll111_opy_(self)
  bstack1l1ll1l1l_opy_.append(self)
  if bstack111l1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭੄") in CONFIG and bstack111l1_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ੅") in CONFIG[bstack111l1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ੆")][bstack1l111lll11_opy_]:
    bstack1l1l1ll1ll_opy_ = CONFIG[bstack111l1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩੇ")][bstack1l111lll11_opy_][bstack111l1_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬੈ")]
  logger.debug(bstack1l1ll11l11_opy_.format(bstack1l1111l111_opy_))
try:
  try:
    import Browser
    from subprocess import Popen
    def bstack1l11l111l1_opy_(self, args, bufsize=-1, executable=None,
              stdin=None, stdout=None, stderr=None,
              preexec_fn=None, close_fds=True,
              shell=False, cwd=None, env=None, universal_newlines=None,
              startupinfo=None, creationflags=0,
              restore_signals=True, start_new_session=False,
              pass_fds=(), *, user=None, group=None, extra_groups=None,
              encoding=None, errors=None, text=None, umask=-1, pipesize=-1):
      global CONFIG
      global bstack1111111ll_opy_
      if(bstack111l1_opy_ (u"ࠣ࡫ࡱࡨࡪࡾ࠮࡫ࡵࠥ੉") in args[1]):
        with open(os.path.join(os.path.expanduser(bstack111l1_opy_ (u"ࠩࢁࠫ੊")), bstack111l1_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪੋ"), bstack111l1_opy_ (u"ࠫ࠳ࡹࡥࡴࡵ࡬ࡳࡳ࡯ࡤࡴ࠰ࡷࡼࡹ࠭ੌ")), bstack111l1_opy_ (u"ࠬࡽ੍ࠧ")) as fp:
          fp.write(bstack111l1_opy_ (u"ࠨࠢ੎"))
        if(not os.path.exists(os.path.join(os.path.dirname(args[1]), bstack111l1_opy_ (u"ࠢࡪࡰࡧࡩࡽࡥࡢࡴࡶࡤࡧࡰ࠴ࡪࡴࠤ੏")))):
          with open(args[1], bstack111l1_opy_ (u"ࠨࡴࠪ੐")) as f:
            lines = f.readlines()
            index = next((i for i, line in enumerate(lines) if bstack111l1_opy_ (u"ࠩࡤࡷࡾࡴࡣࠡࡨࡸࡲࡨࡺࡩࡰࡰࠣࡣࡳ࡫ࡷࡑࡣࡪࡩ࠭ࡩ࡯࡯ࡶࡨࡼࡹ࠲ࠠࡱࡣࡪࡩࠥࡃࠠࡷࡱ࡬ࡨࠥ࠶ࠩࠨੑ") in line), None)
            if index is not None:
                lines.insert(index+2, bstack1l11111ll_opy_)
            lines.insert(1, bstack1l1l11llll_opy_)
            f.seek(0)
            with open(os.path.join(os.path.dirname(args[1]), bstack111l1_opy_ (u"ࠥ࡭ࡳࡪࡥࡹࡡࡥࡷࡹࡧࡣ࡬࠰࡭ࡷࠧ੒")), bstack111l1_opy_ (u"ࠫࡼ࠭੓")) as bstack1l1l1ll1l_opy_:
              bstack1l1l1ll1l_opy_.writelines(lines)
        CONFIG[bstack111l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧ੔")] = str(bstack1l111l1l_opy_) + str(__version__)
        bstack1l111lll11_opy_ = 0 if bstack1l11llll1l_opy_ < 0 else bstack1l11llll1l_opy_
        try:
          if bstack1ll11l1l_opy_ is True:
            bstack1l111lll11_opy_ = int(multiprocessing.current_process().name)
          elif bstack1l1l1l1l1_opy_ is True:
            bstack1l111lll11_opy_ = int(threading.current_thread().name)
        except:
          bstack1l111lll11_opy_ = 0
        CONFIG[bstack111l1_opy_ (u"ࠨࡵࡴࡧ࡚࠷ࡈࠨ੕")] = False
        CONFIG[bstack111l1_opy_ (u"ࠢࡪࡵࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨ੖")] = True
        bstack1lll111lll_opy_ = bstack1l11l111ll_opy_(CONFIG, bstack1l111lll11_opy_)
        logger.debug(bstack1l1llll111_opy_.format(str(bstack1lll111lll_opy_)))
        if CONFIG.get(bstack111l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬ੗")):
          bstack1111lll1l_opy_(bstack1lll111lll_opy_)
        if bstack111l1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ੘") in CONFIG and bstack111l1_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨਖ਼") in CONFIG[bstack111l1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧਗ਼")][bstack1l111lll11_opy_]:
          bstack1l1l1ll1ll_opy_ = CONFIG[bstack111l1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨਜ਼")][bstack1l111lll11_opy_][bstack111l1_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫੜ")]
        args.append(os.path.join(os.path.expanduser(bstack111l1_opy_ (u"ࠧࡿࠩ੝")), bstack111l1_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨਫ਼"), bstack111l1_opy_ (u"ࠩ࠱ࡷࡪࡹࡳࡪࡱࡱ࡭ࡩࡹ࠮ࡵࡺࡷࠫ੟")))
        args.append(str(threading.get_ident()))
        args.append(json.dumps(bstack1lll111lll_opy_))
        args[1] = os.path.join(os.path.dirname(args[1]), bstack111l1_opy_ (u"ࠥ࡭ࡳࡪࡥࡹࡡࡥࡷࡹࡧࡣ࡬࠰࡭ࡷࠧ੠"))
      bstack1111111ll_opy_ = True
      return bstack1ll1ll1lll_opy_(self, args, bufsize=bufsize, executable=executable,
                    stdin=stdin, stdout=stdout, stderr=stderr,
                    preexec_fn=preexec_fn, close_fds=close_fds,
                    shell=shell, cwd=cwd, env=env, universal_newlines=universal_newlines,
                    startupinfo=startupinfo, creationflags=creationflags,
                    restore_signals=restore_signals, start_new_session=start_new_session,
                    pass_fds=pass_fds, user=user, group=group, extra_groups=extra_groups,
                    encoding=encoding, errors=errors, text=text, umask=umask, pipesize=pipesize)
  except Exception as e:
    pass
  import playwright._impl._api_structures
  import playwright._impl._helper
  def bstack1111l11l1_opy_(self,
        executablePath = None,
        channel = None,
        args = None,
        ignoreDefaultArgs = None,
        handleSIGINT = None,
        handleSIGTERM = None,
        handleSIGHUP = None,
        timeout = None,
        env = None,
        headless = None,
        devtools = None,
        proxy = None,
        downloadsPath = None,
        slowMo = None,
        tracesDir = None,
        chromiumSandbox = None,
        firefoxUserPrefs = None
        ):
    global CONFIG
    global bstack1l11llll1l_opy_
    global bstack1l1l1ll1ll_opy_
    global bstack1ll11l1l_opy_
    global bstack1l1l1l1l1_opy_
    global bstack1l111l1l_opy_
    CONFIG[bstack111l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭੡")] = str(bstack1l111l1l_opy_) + str(__version__)
    bstack1l111lll11_opy_ = 0 if bstack1l11llll1l_opy_ < 0 else bstack1l11llll1l_opy_
    try:
      if bstack1ll11l1l_opy_ is True:
        bstack1l111lll11_opy_ = int(multiprocessing.current_process().name)
      elif bstack1l1l1l1l1_opy_ is True:
        bstack1l111lll11_opy_ = int(threading.current_thread().name)
    except:
      bstack1l111lll11_opy_ = 0
    CONFIG[bstack111l1_opy_ (u"ࠧ࡯ࡳࡑ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠦ੢")] = True
    bstack1lll111lll_opy_ = bstack1l11l111ll_opy_(CONFIG, bstack1l111lll11_opy_)
    logger.debug(bstack1l1llll111_opy_.format(str(bstack1lll111lll_opy_)))
    if CONFIG.get(bstack111l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪ੣")):
      bstack1111lll1l_opy_(bstack1lll111lll_opy_)
    if bstack111l1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ੤") in CONFIG and bstack111l1_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭੥") in CONFIG[bstack111l1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ੦")][bstack1l111lll11_opy_]:
      bstack1l1l1ll1ll_opy_ = CONFIG[bstack111l1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭੧")][bstack1l111lll11_opy_][bstack111l1_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ੨")]
    import urllib
    import json
    bstack1lll1111_opy_ = bstack111l1_opy_ (u"ࠬࡽࡳࡴ࠼࠲࠳ࡨࡪࡰ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࡀࡥࡤࡴࡸࡃࠧ੩") + urllib.parse.quote(json.dumps(bstack1lll111lll_opy_))
    browser = self.connect(bstack1lll1111_opy_)
    return browser
except Exception as e:
    pass
def bstack1l1ll1lll_opy_():
    global bstack1111111ll_opy_
    global bstack1l111l1l_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        from bstack_utils.helper import bstack111lll1ll_opy_
        if not bstack1l1l111l_opy_:
          global bstack11ll1lll_opy_
          if not bstack11ll1lll_opy_:
            from bstack_utils.helper import bstack11lll111l_opy_, bstack1l111l1ll_opy_
            bstack11ll1lll_opy_ = bstack11lll111l_opy_()
            bstack1l111l1ll_opy_(bstack1l111l1l_opy_)
          BrowserType.connect = bstack111lll1ll_opy_
          return
        BrowserType.launch = bstack1111l11l1_opy_
        bstack1111111ll_opy_ = True
    except Exception as e:
        pass
    try:
      import Browser
      from subprocess import Popen
      Popen.__init__ = bstack1l11l111l1_opy_
      bstack1111111ll_opy_ = True
    except Exception as e:
      pass
def bstack1ll1llll11_opy_(context, bstack1lll1l11l1_opy_):
  try:
    context.page.evaluate(bstack111l1_opy_ (u"ࠨ࡟ࠡ࠿ࡁࠤࢀࢃࠢ੪"), bstack111l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡳࡧ࡭ࡦࠤ࠽ࠫ੫")+ json.dumps(bstack1lll1l11l1_opy_) + bstack111l1_opy_ (u"ࠣࡿࢀࠦ੬"))
  except Exception as e:
    logger.debug(bstack111l1_opy_ (u"ࠤࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡹࡥࡴࡵ࡬ࡳࡳࠦ࡮ࡢ࡯ࡨࠤࢀࢃࠢ੭"), e)
def bstack1l1l11l1l1_opy_(context, message, level):
  try:
    context.page.evaluate(bstack111l1_opy_ (u"ࠥࡣࠥࡃ࠾ࠡࡽࢀࠦ੮"), bstack111l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡧࡥࡹࡧࠢ࠻ࠩ੯") + json.dumps(message) + bstack111l1_opy_ (u"ࠬ࠲ࠢ࡭ࡧࡹࡩࡱࠨ࠺ࠨੰ") + json.dumps(level) + bstack111l1_opy_ (u"࠭ࡽࡾࠩੱ"))
  except Exception as e:
    logger.debug(bstack111l1_opy_ (u"ࠢࡦࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࡥࡳࡴ࡯ࡵࡣࡷ࡭ࡴࡴࠠࡼࡿࠥੲ"), e)
def bstack1l11111lll_opy_(self, url):
  global bstack1l1lll1l11_opy_
  try:
    bstack1l1ll111_opy_(url)
  except Exception as err:
    logger.debug(bstack1l111l11_opy_.format(str(err)))
  try:
    bstack1l1lll1l11_opy_(self, url)
  except Exception as e:
    try:
      bstack1l1l11ll1_opy_ = str(e)
      if any(err_msg in bstack1l1l11ll1_opy_ for err_msg in bstack1l11llll11_opy_):
        bstack1l1ll111_opy_(url, True)
    except Exception as err:
      logger.debug(bstack1l111l11_opy_.format(str(err)))
    raise e
def bstack111llll1l_opy_(self):
  global bstack1ll1llll1_opy_
  bstack1ll1llll1_opy_ = self
  return
def bstack1l1llll11_opy_(self):
  global bstack1llll1l1l1_opy_
  bstack1llll1l1l1_opy_ = self
  return
def bstack1l1l1l11_opy_(test_name, bstack1ll11l1ll1_opy_):
  global CONFIG
  if percy.bstack1l1ll1l1_opy_() == bstack111l1_opy_ (u"ࠣࡶࡵࡹࡪࠨੳ"):
    bstack11lll1l1l_opy_ = os.path.relpath(bstack1ll11l1ll1_opy_, start=os.getcwd())
    suite_name, _ = os.path.splitext(bstack11lll1l1l_opy_)
    bstack1llllll1ll_opy_ = suite_name + bstack111l1_opy_ (u"ࠤ࠰ࠦੴ") + test_name
    threading.current_thread().percySessionName = bstack1llllll1ll_opy_
def bstack1ll1l11ll1_opy_(self, test, *args, **kwargs):
  global bstack1l1l11111_opy_
  test_name = None
  bstack1ll11l1ll1_opy_ = None
  if test:
    test_name = str(test.name)
    bstack1ll11l1ll1_opy_ = str(test.source)
  bstack1l1l1l11_opy_(test_name, bstack1ll11l1ll1_opy_)
  bstack1l1l11111_opy_(self, test, *args, **kwargs)
def bstack11ll11lll_opy_(driver, bstack1llllll1ll_opy_):
  if not bstack1l1l1l1l_opy_ and bstack1llllll1ll_opy_:
      bstack1l1l11lll1_opy_ = {
          bstack111l1_opy_ (u"ࠪࡥࡨࡺࡩࡰࡰࠪੵ"): bstack111l1_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬ੶"),
          bstack111l1_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨ੷"): {
              bstack111l1_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ੸"): bstack1llllll1ll_opy_
          }
      }
      bstack111llllll_opy_ = bstack111l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࢁࠬ੹").format(json.dumps(bstack1l1l11lll1_opy_))
      driver.execute_script(bstack111llllll_opy_)
  if bstack1l11ll1ll_opy_:
      bstack1111l11ll_opy_ = {
          bstack111l1_opy_ (u"ࠨࡣࡦࡸ࡮ࡵ࡮ࠨ੺"): bstack111l1_opy_ (u"ࠩࡤࡲࡳࡵࡴࡢࡶࡨࠫ੻"),
          bstack111l1_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭੼"): {
              bstack111l1_opy_ (u"ࠫࡩࡧࡴࡢࠩ੽"): bstack1llllll1ll_opy_ + bstack111l1_opy_ (u"ࠬࠦࡰࡢࡵࡶࡩࡩࠧࠧ੾"),
              bstack111l1_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬ੿"): bstack111l1_opy_ (u"ࠧࡪࡰࡩࡳࠬ઀")
          }
      }
      if bstack1l11ll1ll_opy_.status == bstack111l1_opy_ (u"ࠨࡒࡄࡗࡘ࠭ઁ"):
          bstack1l1l1l11ll_opy_ = bstack111l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࢃࠧં").format(json.dumps(bstack1111l11ll_opy_))
          driver.execute_script(bstack1l1l1l11ll_opy_)
          bstack1lll1111l1_opy_(driver, bstack111l1_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪઃ"))
      elif bstack1l11ll1ll_opy_.status == bstack111l1_opy_ (u"ࠫࡋࡇࡉࡍࠩ઄"):
          reason = bstack111l1_opy_ (u"ࠧࠨઅ")
          bstack1llll1111_opy_ = bstack1llllll1ll_opy_ + bstack111l1_opy_ (u"࠭ࠠࡧࡣ࡬ࡰࡪࡪࠧઆ")
          if bstack1l11ll1ll_opy_.message:
              reason = str(bstack1l11ll1ll_opy_.message)
              bstack1llll1111_opy_ = bstack1llll1111_opy_ + bstack111l1_opy_ (u"ࠧࠡࡹ࡬ࡸ࡭ࠦࡥࡳࡴࡲࡶ࠿ࠦࠧઇ") + reason
          bstack1111l11ll_opy_[bstack111l1_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫઈ")] = {
              bstack111l1_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨઉ"): bstack111l1_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩઊ"),
              bstack111l1_opy_ (u"ࠫࡩࡧࡴࡢࠩઋ"): bstack1llll1111_opy_
          }
          bstack1l1l1l11ll_opy_ = bstack111l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࡿࠪઌ").format(json.dumps(bstack1111l11ll_opy_))
          driver.execute_script(bstack1l1l1l11ll_opy_)
          bstack1lll1111l1_opy_(driver, bstack111l1_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ઍ"), reason)
          bstack111ll1l1_opy_(reason, str(bstack1l11ll1ll_opy_), str(bstack1l11llll1l_opy_), logger)
def bstack11l111lll_opy_(driver, test):
  if percy.bstack1l1ll1l1_opy_() == bstack111l1_opy_ (u"ࠢࡵࡴࡸࡩࠧ઎") and percy.bstack11llll11_opy_() == bstack111l1_opy_ (u"ࠣࡶࡨࡷࡹࡩࡡࡴࡧࠥએ"):
      bstack111l11l11_opy_ = bstack11l1ll1l1_opy_(threading.current_thread(), bstack111l1_opy_ (u"ࠩࡳࡩࡷࡩࡹࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬઐ"), None)
      bstack11l1l111_opy_(driver, bstack111l11l11_opy_, test)
  if bstack11l1ll1l1_opy_(threading.current_thread(), bstack111l1_opy_ (u"ࠪ࡭ࡸࡇ࠱࠲ࡻࡗࡩࡸࡺࠧઑ"), None) and bstack11l1ll1l1_opy_(
          threading.current_thread(), bstack111l1_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ઒"), None):
      logger.info(bstack111l1_opy_ (u"ࠧࡇࡵࡵࡱࡰࡥࡹ࡫ࠠࡵࡧࡶࡸࠥࡩࡡࡴࡧࠣࡩࡽ࡫ࡣࡶࡶ࡬ࡳࡳࠦࡨࡢࡵࠣࡩࡳࡪࡥࡥ࠰ࠣࡔࡷࡵࡣࡦࡵࡶ࡭ࡳ࡭ࠠࡧࡱࡵࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡹ࡫ࡳࡵ࡫ࡱ࡫ࠥ࡯ࡳࠡࡷࡱࡨࡪࡸࡷࡢࡻ࠱ࠤࠧઓ"))
      bstack1ll111111l_opy_.bstack11l1l1l11_opy_(driver, name=test.name, path=test.source)
def bstack1l11ll1l11_opy_(test, bstack1llllll1ll_opy_):
    try:
      data = {}
      if test:
        data[bstack111l1_opy_ (u"࠭࡮ࡢ࡯ࡨࠫઔ")] = bstack1llllll1ll_opy_
      if bstack1l11ll1ll_opy_:
        if bstack1l11ll1ll_opy_.status == bstack111l1_opy_ (u"ࠧࡑࡃࡖࡗࠬક"):
          data[bstack111l1_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨખ")] = bstack111l1_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩગ")
        elif bstack1l11ll1ll_opy_.status == bstack111l1_opy_ (u"ࠪࡊࡆࡏࡌࠨઘ"):
          data[bstack111l1_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫઙ")] = bstack111l1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬચ")
          if bstack1l11ll1ll_opy_.message:
            data[bstack111l1_opy_ (u"࠭ࡲࡦࡣࡶࡳࡳ࠭છ")] = str(bstack1l11ll1ll_opy_.message)
      user = CONFIG[bstack111l1_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩજ")]
      key = CONFIG[bstack111l1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫઝ")]
      url = bstack111l1_opy_ (u"ࠩ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡿࢂࡀࡻࡾࡂࡤࡴ࡮࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡤࡹࡹࡵ࡭ࡢࡶࡨ࠳ࡸ࡫ࡳࡴ࡫ࡲࡲࡸ࠵ࡻࡾ࠰࡭ࡷࡴࡴࠧઞ").format(user, key, bstack1l1111l111_opy_)
      headers = {
        bstack111l1_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩટ"): bstack111l1_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧઠ"),
      }
      if bool(data):
        requests.put(url, json=data, headers=headers)
    except Exception as e:
      logger.error(bstack1l1ll111l1_opy_.format(str(e)))
def bstack1lllll1l1_opy_(test, bstack1llllll1ll_opy_):
  global CONFIG
  global bstack1llll1l1l1_opy_
  global bstack1ll1llll1_opy_
  global bstack1l1111l111_opy_
  global bstack1l11ll1ll_opy_
  global bstack1l1l1ll1ll_opy_
  global bstack1lllllll1l_opy_
  global bstack1l1lll1l1l_opy_
  global bstack1111l1l1_opy_
  global bstack1l1l1lll_opy_
  global bstack1l1ll1l1l_opy_
  global bstack1l111lll1_opy_
  try:
    if not bstack1l1111l111_opy_:
      with open(os.path.join(os.path.expanduser(bstack111l1_opy_ (u"ࠬࢄࠧડ")), bstack111l1_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ઢ"), bstack111l1_opy_ (u"ࠧ࠯ࡵࡨࡷࡸ࡯࡯࡯࡫ࡧࡷ࠳ࡺࡸࡵࠩણ"))) as f:
        bstack1l1l11lll_opy_ = json.loads(bstack111l1_opy_ (u"ࠣࡽࠥત") + f.read().strip() + bstack111l1_opy_ (u"ࠩࠥࡼࠧࡀࠠࠣࡻࠥࠫથ") + bstack111l1_opy_ (u"ࠥࢁࠧદ"))
        bstack1l1111l111_opy_ = bstack1l1l11lll_opy_[str(threading.get_ident())]
  except:
    pass
  if bstack1l1ll1l1l_opy_:
    for driver in bstack1l1ll1l1l_opy_:
      if bstack1l1111l111_opy_ == driver.session_id:
        if test:
          bstack11l111lll_opy_(driver, test)
        bstack11ll11lll_opy_(driver, bstack1llllll1ll_opy_)
  elif bstack1l1111l111_opy_:
    bstack1l11ll1l11_opy_(test, bstack1llllll1ll_opy_)
  if bstack1llll1l1l1_opy_:
    bstack1l1lll1l1l_opy_(bstack1llll1l1l1_opy_)
  if bstack1ll1llll1_opy_:
    bstack1111l1l1_opy_(bstack1ll1llll1_opy_)
  if bstack1lll11ll1l_opy_:
    bstack1l1l1lll_opy_()
def bstack1l111ll11_opy_(self, test, *args, **kwargs):
  bstack1llllll1ll_opy_ = None
  if test:
    bstack1llllll1ll_opy_ = str(test.name)
  bstack1lllll1l1_opy_(test, bstack1llllll1ll_opy_)
  bstack1lllllll1l_opy_(self, test, *args, **kwargs)
def bstack111l1ll1l_opy_(self, parent, test, skip_on_failure=None, rpa=False):
  global bstack1l1lll1l1_opy_
  global CONFIG
  global bstack1l1ll1l1l_opy_
  global bstack1l1111l111_opy_
  bstack1l11l1llll_opy_ = None
  try:
    if bstack11l1ll1l1_opy_(threading.current_thread(), bstack111l1_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪધ"), None):
      try:
        if not bstack1l1111l111_opy_:
          with open(os.path.join(os.path.expanduser(bstack111l1_opy_ (u"ࠬࢄࠧન")), bstack111l1_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭઩"), bstack111l1_opy_ (u"ࠧ࠯ࡵࡨࡷࡸ࡯࡯࡯࡫ࡧࡷ࠳ࡺࡸࡵࠩપ"))) as f:
            bstack1l1l11lll_opy_ = json.loads(bstack111l1_opy_ (u"ࠣࡽࠥફ") + f.read().strip() + bstack111l1_opy_ (u"ࠩࠥࡼࠧࡀࠠࠣࡻࠥࠫબ") + bstack111l1_opy_ (u"ࠥࢁࠧભ"))
            bstack1l1111l111_opy_ = bstack1l1l11lll_opy_[str(threading.get_ident())]
      except:
        pass
      if bstack1l1ll1l1l_opy_:
        for driver in bstack1l1ll1l1l_opy_:
          if bstack1l1111l111_opy_ == driver.session_id:
            bstack1l11l1llll_opy_ = driver
    bstack11llll1ll_opy_ = bstack1ll111111l_opy_.bstack1l1111l11_opy_(test.tags)
    if bstack1l11l1llll_opy_:
      threading.current_thread().isA11yTest = bstack1ll111111l_opy_.bstack11lllll1_opy_(bstack1l11l1llll_opy_, bstack11llll1ll_opy_)
    else:
      threading.current_thread().isA11yTest = bstack11llll1ll_opy_
  except:
    pass
  bstack1l1lll1l1_opy_(self, parent, test, skip_on_failure=skip_on_failure, rpa=rpa)
  global bstack1l11ll1ll_opy_
  bstack1l11ll1ll_opy_ = self._test
def bstack1l11l1l11_opy_():
  global bstack11l1lll11_opy_
  try:
    if os.path.exists(bstack11l1lll11_opy_):
      os.remove(bstack11l1lll11_opy_)
  except Exception as e:
    logger.debug(bstack111l1_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡤࡦ࡮ࡨࡸ࡮ࡴࡧࠡࡴࡲࡦࡴࡺࠠࡳࡧࡳࡳࡷࡺࠠࡧ࡫࡯ࡩ࠿ࠦࠧમ") + str(e))
def bstack1lll1lll1_opy_():
  global bstack11l1lll11_opy_
  bstack1lll1l1l1_opy_ = {}
  try:
    if not os.path.isfile(bstack11l1lll11_opy_):
      with open(bstack11l1lll11_opy_, bstack111l1_opy_ (u"ࠬࡽࠧય")):
        pass
      with open(bstack11l1lll11_opy_, bstack111l1_opy_ (u"ࠨࡷࠬࠤર")) as outfile:
        json.dump({}, outfile)
    if os.path.exists(bstack11l1lll11_opy_):
      bstack1lll1l1l1_opy_ = json.load(open(bstack11l1lll11_opy_, bstack111l1_opy_ (u"ࠧࡳࡤࠪ઱")))
  except Exception as e:
    logger.debug(bstack111l1_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡶࡪࡧࡤࡪࡰࡪࠤࡷࡵࡢࡰࡶࠣࡶࡪࡶ࡯ࡳࡶࠣࡪ࡮ࡲࡥ࠻ࠢࠪલ") + str(e))
  finally:
    return bstack1lll1l1l1_opy_
def bstack1l11lll1_opy_(platform_index, item_index):
  global bstack11l1lll11_opy_
  try:
    bstack1lll1l1l1_opy_ = bstack1lll1lll1_opy_()
    bstack1lll1l1l1_opy_[item_index] = platform_index
    with open(bstack11l1lll11_opy_, bstack111l1_opy_ (u"ࠤࡺ࠯ࠧળ")) as outfile:
      json.dump(bstack1lll1l1l1_opy_, outfile)
  except Exception as e:
    logger.debug(bstack111l1_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡽࡲࡪࡶ࡬ࡲ࡬ࠦࡴࡰࠢࡵࡳࡧࡵࡴࠡࡴࡨࡴࡴࡸࡴࠡࡨ࡬ࡰࡪࡀࠠࠨ઴") + str(e))
def bstack1ll1ll11ll_opy_(bstack1lllll1111_opy_):
  global CONFIG
  bstack1lll11llll_opy_ = bstack111l1_opy_ (u"ࠫࠬવ")
  if not bstack111l1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨશ") in CONFIG:
    logger.info(bstack111l1_opy_ (u"࠭ࡎࡰࠢࡳࡰࡦࡺࡦࡰࡴࡰࡷࠥࡶࡡࡴࡵࡨࡨࠥࡻ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡩࡨࡲࡪࡸࡡࡵࡧࠣࡶࡪࡶ࡯ࡳࡶࠣࡪࡴࡸࠠࡓࡱࡥࡳࡹࠦࡲࡶࡰࠪષ"))
  try:
    platform = CONFIG[bstack111l1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪસ")][bstack1lllll1111_opy_]
    if bstack111l1_opy_ (u"ࠨࡱࡶࠫહ") in platform:
      bstack1lll11llll_opy_ += str(platform[bstack111l1_opy_ (u"ࠩࡲࡷࠬ઺")]) + bstack111l1_opy_ (u"ࠪ࠰ࠥ࠭઻")
    if bstack111l1_opy_ (u"ࠫࡴࡹࡖࡦࡴࡶ࡭ࡴࡴ઼ࠧ") in platform:
      bstack1lll11llll_opy_ += str(platform[bstack111l1_opy_ (u"ࠬࡵࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠨઽ")]) + bstack111l1_opy_ (u"࠭ࠬࠡࠩા")
    if bstack111l1_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠫિ") in platform:
      bstack1lll11llll_opy_ += str(platform[bstack111l1_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩࠬી")]) + bstack111l1_opy_ (u"ࠩ࠯ࠤࠬુ")
    if bstack111l1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬૂ") in platform:
      bstack1lll11llll_opy_ += str(platform[bstack111l1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ૃ")]) + bstack111l1_opy_ (u"ࠬ࠲ࠠࠨૄ")
    if bstack111l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫૅ") in platform:
      bstack1lll11llll_opy_ += str(platform[bstack111l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬ૆")]) + bstack111l1_opy_ (u"ࠨ࠮ࠣࠫે")
    if bstack111l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪૈ") in platform:
      bstack1lll11llll_opy_ += str(platform[bstack111l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫૉ")]) + bstack111l1_opy_ (u"ࠫ࠱ࠦࠧ૊")
  except Exception as e:
    logger.debug(bstack111l1_opy_ (u"࡙ࠬ࡯࡮ࡧࠣࡩࡷࡸ࡯ࡳࠢ࡬ࡲࠥ࡭ࡥ࡯ࡧࡵࡥࡹ࡯࡮ࡨࠢࡳࡰࡦࡺࡦࡰࡴࡰࠤࡸࡺࡲࡪࡰࡪࠤ࡫ࡵࡲࠡࡴࡨࡴࡴࡸࡴࠡࡩࡨࡲࡪࡸࡡࡵ࡫ࡲࡲࠬો") + str(e))
  finally:
    if bstack1lll11llll_opy_[len(bstack1lll11llll_opy_) - 2:] == bstack111l1_opy_ (u"࠭ࠬࠡࠩૌ"):
      bstack1lll11llll_opy_ = bstack1lll11llll_opy_[:-2]
    return bstack1lll11llll_opy_
def bstack111l11111_opy_(path, bstack1lll11llll_opy_):
  try:
    import xml.etree.ElementTree as ET
    bstack1ll1l111ll_opy_ = ET.parse(path)
    bstack1lll111l_opy_ = bstack1ll1l111ll_opy_.getroot()
    bstack1l11l1l1l_opy_ = None
    for suite in bstack1lll111l_opy_.iter(bstack111l1_opy_ (u"ࠧࡴࡷ࡬ࡸࡪ્࠭")):
      if bstack111l1_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨ૎") in suite.attrib:
        suite.attrib[bstack111l1_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ૏")] += bstack111l1_opy_ (u"ࠪࠤࠬૐ") + bstack1lll11llll_opy_
        bstack1l11l1l1l_opy_ = suite
    bstack11l11111l_opy_ = None
    for robot in bstack1lll111l_opy_.iter(bstack111l1_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪ૑")):
      bstack11l11111l_opy_ = robot
    bstack11l11llll_opy_ = len(bstack11l11111l_opy_.findall(bstack111l1_opy_ (u"ࠬࡹࡵࡪࡶࡨࠫ૒")))
    if bstack11l11llll_opy_ == 1:
      bstack11l11111l_opy_.remove(bstack11l11111l_opy_.findall(bstack111l1_opy_ (u"࠭ࡳࡶ࡫ࡷࡩࠬ૓"))[0])
      bstack11l11ll11_opy_ = ET.Element(bstack111l1_opy_ (u"ࠧࡴࡷ࡬ࡸࡪ࠭૔"), attrib={bstack111l1_opy_ (u"ࠨࡰࡤࡱࡪ࠭૕"): bstack111l1_opy_ (u"ࠩࡖࡹ࡮ࡺࡥࡴࠩ૖"), bstack111l1_opy_ (u"ࠪ࡭ࡩ࠭૗"): bstack111l1_opy_ (u"ࠫࡸ࠶ࠧ૘")})
      bstack11l11111l_opy_.insert(1, bstack11l11ll11_opy_)
      bstack1l1l1l1lll_opy_ = None
      for suite in bstack11l11111l_opy_.iter(bstack111l1_opy_ (u"ࠬࡹࡵࡪࡶࡨࠫ૙")):
        bstack1l1l1l1lll_opy_ = suite
      bstack1l1l1l1lll_opy_.append(bstack1l11l1l1l_opy_)
      bstack1l1ll11l1l_opy_ = None
      for status in bstack1l11l1l1l_opy_.iter(bstack111l1_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭૚")):
        bstack1l1ll11l1l_opy_ = status
      bstack1l1l1l1lll_opy_.append(bstack1l1ll11l1l_opy_)
    bstack1ll1l111ll_opy_.write(path)
  except Exception as e:
    logger.debug(bstack111l1_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡳࡥࡷࡹࡩ࡯ࡩࠣࡻ࡭࡯࡬ࡦࠢࡪࡩࡳ࡫ࡲࡢࡶ࡬ࡲ࡬ࠦࡲࡰࡤࡲࡸࠥࡸࡥࡱࡱࡵࡸࠬ૛") + str(e))
def bstack1l11lll1l_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name):
  global bstack1l1l1l111_opy_
  global CONFIG
  if bstack111l1_opy_ (u"ࠣࡲࡼࡸ࡭ࡵ࡮ࡱࡣࡷ࡬ࠧ૜") in options:
    del options[bstack111l1_opy_ (u"ࠤࡳࡽࡹ࡮࡯࡯ࡲࡤࡸ࡭ࠨ૝")]
  bstack1lll111ll1_opy_ = bstack1lll1lll1_opy_()
  for bstack11l11l111_opy_ in bstack1lll111ll1_opy_.keys():
    path = os.path.join(os.getcwd(), bstack111l1_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࡡࡵࡩࡸࡻ࡬ࡵࡵࠪ૞"), str(bstack11l11l111_opy_), bstack111l1_opy_ (u"ࠫࡴࡻࡴࡱࡷࡷ࠲ࡽࡳ࡬ࠨ૟"))
    bstack111l11111_opy_(path, bstack1ll1ll11ll_opy_(bstack1lll111ll1_opy_[bstack11l11l111_opy_]))
  bstack1l11l1l11_opy_()
  return bstack1l1l1l111_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name)
def bstack1ll1l1l11l_opy_(self, ff_profile_dir):
  global bstack1l111lll1l_opy_
  if not ff_profile_dir:
    return None
  return bstack1l111lll1l_opy_(self, ff_profile_dir)
def bstack11ll11ll_opy_(datasources, opts_for_run, outs_dir, pabot_args, suite_group):
  from pabot.pabot import QueueItem
  global CONFIG
  global bstack1111l1ll1_opy_
  bstack1ll1ll1l1_opy_ = []
  if bstack111l1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨૠ") in CONFIG:
    bstack1ll1ll1l1_opy_ = CONFIG[bstack111l1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩૡ")]
  return [
    QueueItem(
      datasources,
      outs_dir,
      opts_for_run,
      suite,
      pabot_args[bstack111l1_opy_ (u"ࠢࡤࡱࡰࡱࡦࡴࡤࠣૢ")],
      pabot_args[bstack111l1_opy_ (u"ࠣࡸࡨࡶࡧࡵࡳࡦࠤૣ")],
      argfile,
      pabot_args.get(bstack111l1_opy_ (u"ࠤ࡫࡭ࡻ࡫ࠢ૤")),
      pabot_args[bstack111l1_opy_ (u"ࠥࡴࡷࡵࡣࡦࡵࡶࡩࡸࠨ૥")],
      platform[0],
      bstack1111l1ll1_opy_
    )
    for suite in suite_group
    for argfile in pabot_args[bstack111l1_opy_ (u"ࠦࡦࡸࡧࡶ࡯ࡨࡲࡹ࡬ࡩ࡭ࡧࡶࠦ૦")] or [(bstack111l1_opy_ (u"ࠧࠨ૧"), None)]
    for platform in enumerate(bstack1ll1ll1l1_opy_)
  ]
def bstack111l11l1_opy_(self, datasources, outs_dir, options,
                        execution_item, command, verbose, argfile,
                        hive=None, processes=0, platform_index=0, bstack1llll1lll_opy_=bstack111l1_opy_ (u"࠭ࠧ૨")):
  global bstack1ll11ll1_opy_
  self.platform_index = platform_index
  self.bstack1lll1ll1ll_opy_ = bstack1llll1lll_opy_
  bstack1ll11ll1_opy_(self, datasources, outs_dir, options,
                      execution_item, command, verbose, argfile, hive, processes)
def bstack11l1llll1_opy_(caller_id, datasources, is_last, item, outs_dir):
  global bstack1l1l1ll11_opy_
  global bstack111l111ll_opy_
  bstack11ll1ll11_opy_ = copy.deepcopy(item)
  if not bstack111l1_opy_ (u"ࠧࡷࡣࡵ࡭ࡦࡨ࡬ࡦࠩ૩") in item.options:
    bstack11ll1ll11_opy_.options[bstack111l1_opy_ (u"ࠨࡸࡤࡶ࡮ࡧࡢ࡭ࡧࠪ૪")] = []
  bstack1ll11l11_opy_ = bstack11ll1ll11_opy_.options[bstack111l1_opy_ (u"ࠩࡹࡥࡷ࡯ࡡࡣ࡮ࡨࠫ૫")].copy()
  for v in bstack11ll1ll11_opy_.options[bstack111l1_opy_ (u"ࠪࡺࡦࡸࡩࡢࡤ࡯ࡩࠬ૬")]:
    if bstack111l1_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡔࡑࡇࡔࡇࡑࡕࡑࡎࡔࡄࡆ࡚ࠪ૭") in v:
      bstack1ll11l11_opy_.remove(v)
    if bstack111l1_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡈࡒࡉࡂࡔࡊࡗࠬ૮") in v:
      bstack1ll11l11_opy_.remove(v)
    if bstack111l1_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡊࡅࡇࡎࡒࡇࡆࡒࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔࠪ૯") in v:
      bstack1ll11l11_opy_.remove(v)
  bstack1ll11l11_opy_.insert(0, bstack111l1_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑࡐࡍࡃࡗࡊࡔࡘࡍࡊࡐࡇࡉ࡝ࡀࡻࡾࠩ૰").format(bstack11ll1ll11_opy_.platform_index))
  bstack1ll11l11_opy_.insert(0, bstack111l1_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡅࡇࡉࡐࡔࡉࡁࡍࡋࡇࡉࡓ࡚ࡉࡇࡋࡈࡖ࠿ࢁࡽࠨ૱").format(bstack11ll1ll11_opy_.bstack1lll1ll1ll_opy_))
  bstack11ll1ll11_opy_.options[bstack111l1_opy_ (u"ࠩࡹࡥࡷ࡯ࡡࡣ࡮ࡨࠫ૲")] = bstack1ll11l11_opy_
  if bstack111l111ll_opy_:
    bstack11ll1ll11_opy_.options[bstack111l1_opy_ (u"ࠪࡺࡦࡸࡩࡢࡤ࡯ࡩࠬ૳")].insert(0, bstack111l1_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡇࡑࡏࡁࡓࡉࡖ࠾ࢀࢃࠧ૴").format(bstack111l111ll_opy_))
  return bstack1l1l1ll11_opy_(caller_id, datasources, is_last, bstack11ll1ll11_opy_, outs_dir)
def bstack11ll1111l_opy_(command, item_index):
  if bstack1111ll1l1_opy_.get_property(bstack111l1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡹࡥࡴࡵ࡬ࡳࡳ࠭૵")):
    os.environ[bstack111l1_opy_ (u"࠭ࡃࡖࡔࡕࡉࡓ࡚࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡇࡅ࡙ࡇࠧ૶")] = json.dumps(CONFIG[bstack111l1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ૷")][item_index % bstack1ll111l11l_opy_])
  global bstack111l111ll_opy_
  if bstack111l111ll_opy_:
    command[0] = command[0].replace(bstack111l1_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧ૸"), bstack111l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠮ࡵࡧ࡯ࠥࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱࠦ࠭࠮ࡤࡶࡸࡦࡩ࡫ࡠ࡫ࡷࡩࡲࡥࡩ࡯ࡦࡨࡼࠥ࠭ૹ") + str(
      item_index) + bstack111l1_opy_ (u"ࠪࠤࠬૺ") + bstack111l111ll_opy_, 1)
  else:
    command[0] = command[0].replace(bstack111l1_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪૻ"),
                                    bstack111l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠱ࡸࡪ࡫ࠡࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠢ࠰࠱ࡧࡹࡴࡢࡥ࡮ࡣ࡮ࡺࡥ࡮ࡡ࡬ࡲࡩ࡫ࡸࠡࠩૼ") + str(item_index), 1)
def bstack1l111111l1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index):
  global bstack11l1l1lll_opy_
  bstack11ll1111l_opy_(command, item_index)
  return bstack11l1l1lll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
def bstack1lll11l111_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir):
  global bstack11l1l1lll_opy_
  bstack11ll1111l_opy_(command, item_index)
  return bstack11l1l1lll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir)
def bstack1l11ll1111_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout):
  global bstack11l1l1lll_opy_
  bstack11ll1111l_opy_(command, item_index)
  return bstack11l1l1lll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
def is_driver_active(driver):
  return True if driver and driver.session_id else False
def bstack1llll11l11_opy_(self, runner, quiet=False, capture=True):
  global bstack1l111l1lll_opy_
  bstack1l1lllll_opy_ = bstack1l111l1lll_opy_(self, runner, quiet=quiet, capture=capture)
  if self.exception:
    if not hasattr(runner, bstack111l1_opy_ (u"࠭ࡥࡹࡥࡨࡴࡹ࡯࡯࡯ࡡࡤࡶࡷ࠭૽")):
      runner.exception_arr = []
    if not hasattr(runner, bstack111l1_opy_ (u"ࠧࡦࡺࡦࡣࡹࡸࡡࡤࡧࡥࡥࡨࡱ࡟ࡢࡴࡵࠫ૾")):
      runner.exc_traceback_arr = []
    runner.exception = self.exception
    runner.exc_traceback = self.exc_traceback
    runner.exception_arr.append(self.exception)
    runner.exc_traceback_arr.append(self.exc_traceback)
  return bstack1l1lllll_opy_
def bstack1l1ll1l111_opy_(runner, hook_name, context, element, bstack1l111l111l_opy_, *args):
  try:
    if runner.hooks.get(hook_name):
      bstack1l1111llll_opy_.bstack11lll1l11_opy_(hook_name, element)
    bstack1l111l111l_opy_(runner, hook_name, context, *args)
    if runner.hooks.get(hook_name):
      bstack1l1111llll_opy_.bstack11111lll1_opy_(element)
      if hook_name not in [bstack111l1_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࡠࡣ࡯ࡰࠬ૿"), bstack111l1_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡣ࡯ࡰࠬ଀")] and args and hasattr(args[0], bstack111l1_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࡡࡰࡩࡸࡹࡡࡨࡧࠪଁ")):
        args[0].error_message = bstack111l1_opy_ (u"ࠫࠬଂ")
  except Exception as e:
    logger.debug(bstack111l1_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡪࡤࡲࡩࡲࡥࠡࡪࡲࡳࡰࡹࠠࡪࡰࠣࡦࡪ࡮ࡡࡷࡧ࠽ࠤࢀࢃࠧଃ").format(str(e)))
def bstack1lllllllll_opy_(runner, name, context, bstack1l111l111l_opy_, *args):
    if runner.hooks.get(bstack111l1_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡡ࡭࡮ࠥ଄")).__name__ != bstack111l1_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡢ࡮࡯ࡣࡩ࡫ࡦࡢࡷ࡯ࡸࡤ࡮࡯ࡰ࡭ࠥଅ"):
      bstack1l1ll1l111_opy_(runner, name, context, runner, bstack1l111l111l_opy_, *args)
    try:
      threading.current_thread().bstackSessionDriver if bstack1l111ll11l_opy_(bstack111l1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡔࡧࡶࡷ࡮ࡵ࡮ࡅࡴ࡬ࡺࡪࡸࠧଆ")) else context.browser
      runner.driver_initialised = bstack111l1_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡤࡰࡱࠨଇ")
    except Exception as e:
      logger.debug(bstack111l1_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡶࠣࡨࡷ࡯ࡶࡦࡴࠣ࡭ࡳ࡯ࡴࡪࡣ࡯࡭ࡸ࡫ࠠࡢࡶࡷࡶ࡮ࡨࡵࡵࡧ࠽ࠤࢀࢃࠧଈ").format(str(e)))
def bstack1l1111l11l_opy_(runner, name, context, bstack1l111l111l_opy_, *args):
    bstack1l1ll1l111_opy_(runner, name, context, context.feature, bstack1l111l111l_opy_, *args)
    try:
      if not bstack1l1l1l1l_opy_:
        bstack1l11l1llll_opy_ = threading.current_thread().bstackSessionDriver if bstack1l111ll11l_opy_(bstack111l1_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪଉ")) else context.browser
        if is_driver_active(bstack1l11l1llll_opy_):
          if runner.driver_initialised is None: runner.driver_initialised = bstack111l1_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤ࡬ࡥࡢࡶࡸࡶࡪࠨଊ")
          bstack1lll1l11l1_opy_ = str(runner.feature.name)
          bstack1ll1llll11_opy_(context, bstack1lll1l11l1_opy_)
          bstack1l11l1llll_opy_.execute_script(bstack111l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡲࡦࡳࡥࠣ࠼ࠣࠫଋ") + json.dumps(bstack1lll1l11l1_opy_) + bstack111l1_opy_ (u"ࠧࡾࡿࠪଌ"))
    except Exception as e:
      logger.debug(bstack111l1_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸ࡫ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡱࡥࡲ࡫ࠠࡪࡰࠣࡦࡪ࡬࡯ࡳࡧࠣࡪࡪࡧࡴࡶࡴࡨ࠾ࠥࢁࡽࠨ଍").format(str(e)))
def bstack1ll1l1lll_opy_(runner, name, context, bstack1l111l111l_opy_, *args):
    bstack1l1111llll_opy_.start_test(context)
    bstack1l1ll1l111_opy_(runner, name, context, context.scenario, bstack1l111l111l_opy_, *args)
def bstack1l11l1lll_opy_(runner, name, context, bstack1l111l111l_opy_, *args):
    if len(context.scenario.tags) == 0: bstack1l1111llll_opy_.start_test(context)
    bstack1l1ll1l111_opy_(runner, name, context, context.scenario, bstack1l111l111l_opy_, *args)
    threading.current_thread().a11y_stop = False
    bstack1l11l1l1_opy_.bstack11l1l11l_opy_(context, *args)
    try:
      bstack1l11l1llll_opy_ = bstack11l1ll1l1_opy_(threading.current_thread(), bstack111l1_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨ଎"), context.browser)
      if is_driver_active(bstack1l11l1llll_opy_):
        bstack11llllll11_opy_.bstack111lll111_opy_(bstack11l1ll1l1_opy_(threading.current_thread(), bstack111l1_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩଏ"), {}))
        if runner.driver_initialised is None: runner.driver_initialised = bstack111l1_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴࠨଐ")
        if (not bstack1l1l1l1l_opy_):
          scenario_name = args[0].name
          feature_name = bstack1lll1l11l1_opy_ = str(runner.feature.name)
          bstack1lll1l11l1_opy_ = feature_name + bstack111l1_opy_ (u"ࠬࠦ࠭ࠡࠩ଑") + scenario_name
          if runner.driver_initialised == bstack111l1_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠣ଒"):
            bstack1ll1llll11_opy_(context, bstack1lll1l11l1_opy_)
            bstack1l11l1llll_opy_.execute_script(bstack111l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡳࡧ࡭ࡦࠤ࠽ࠤࠬଓ") + json.dumps(bstack1lll1l11l1_opy_) + bstack111l1_opy_ (u"ࠨࡿࢀࠫଔ"))
    except Exception as e:
      logger.debug(bstack111l1_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡥࡵࠢࡶࡩࡸࡹࡩࡰࡰࠣࡲࡦࡳࡥࠡ࡫ࡱࠤࡧ࡫ࡦࡰࡴࡨࠤࡸࡩࡥ࡯ࡣࡵ࡭ࡴࡀࠠࡼࡿࠪକ").format(str(e)))
def bstack1111lllll_opy_(runner, name, context, bstack1l111l111l_opy_, *args):
    bstack1l1ll1l111_opy_(runner, name, context, args[0], bstack1l111l111l_opy_, *args)
    try:
      bstack1l11l1llll_opy_ = threading.current_thread().bstackSessionDriver if bstack1l111ll11l_opy_(bstack111l1_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩଖ")) else context.browser
      if is_driver_active(bstack1l11l1llll_opy_):
        if runner.driver_initialised is None: runner.driver_initialised = bstack111l1_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡸࡺࡥࡱࠤଗ")
        bstack1l1111llll_opy_.bstack1ll1l111l1_opy_(args[0])
        if runner.driver_initialised == bstack111l1_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡹࡴࡦࡲࠥଘ"):
          feature_name = bstack1lll1l11l1_opy_ = str(runner.feature.name)
          bstack1lll1l11l1_opy_ = feature_name + bstack111l1_opy_ (u"࠭ࠠ࠮ࠢࠪଙ") + context.scenario.name
          bstack1l11l1llll_opy_.execute_script(bstack111l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡳࡧ࡭ࡦࠤ࠽ࠤࠬଚ") + json.dumps(bstack1lll1l11l1_opy_) + bstack111l1_opy_ (u"ࠨࡿࢀࠫଛ"))
    except Exception as e:
      logger.debug(bstack111l1_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡥࡵࠢࡶࡩࡸࡹࡩࡰࡰࠣࡲࡦࡳࡥࠡ࡫ࡱࠤࡧ࡫ࡦࡰࡴࡨࠤࡸࡺࡥࡱ࠼ࠣࡿࢂ࠭ଜ").format(str(e)))
def bstack1l1111ll_opy_(runner, name, context, bstack1l111l111l_opy_, *args):
  bstack1l1111llll_opy_.bstack1ll111l1ll_opy_(args[0])
  try:
    bstack11ll11111_opy_ = args[0].status.name
    bstack1l11l1llll_opy_ = threading.current_thread().bstackSessionDriver if bstack111l1_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩଝ") in threading.current_thread().__dict__.keys() else context.browser
    if is_driver_active(bstack1l11l1llll_opy_):
      if runner.driver_initialised is None:
        runner.driver_initialised  = bstack111l1_opy_ (u"ࠫ࡮ࡴࡳࡵࡧࡳࠫଞ")
        feature_name = bstack1lll1l11l1_opy_ = str(runner.feature.name)
        bstack1lll1l11l1_opy_ = feature_name + bstack111l1_opy_ (u"ࠬࠦ࠭ࠡࠩଟ") + context.scenario.name
        bstack1l11l1llll_opy_.execute_script(bstack111l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡲࡦࡳࡥࠣ࠼ࠣࠫଠ") + json.dumps(bstack1lll1l11l1_opy_) + bstack111l1_opy_ (u"ࠧࡾࡿࠪଡ"))
    if str(bstack11ll11111_opy_).lower() == bstack111l1_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨଢ"):
      bstack1ll11l1l1l_opy_ = bstack111l1_opy_ (u"ࠩࠪଣ")
      bstack1l1l1lll1_opy_ = bstack111l1_opy_ (u"ࠪࠫତ")
      bstack1llll11l1_opy_ = bstack111l1_opy_ (u"ࠫࠬଥ")
      try:
        import traceback
        bstack1ll11l1l1l_opy_ = runner.exception.__class__.__name__
        bstack11ll1lll1_opy_ = traceback.format_tb(runner.exc_traceback)
        bstack1l1l1lll1_opy_ = bstack111l1_opy_ (u"ࠬࠦࠧଦ").join(bstack11ll1lll1_opy_)
        bstack1llll11l1_opy_ = bstack11ll1lll1_opy_[-1]
      except Exception as e:
        logger.debug(bstack11111111l_opy_.format(str(e)))
      bstack1ll11l1l1l_opy_ += bstack1llll11l1_opy_
      bstack1l1l11l1l1_opy_(context, json.dumps(str(args[0].name) + bstack111l1_opy_ (u"ࠨࠠ࠮ࠢࡉࡥ࡮ࡲࡥࡥࠣ࡟ࡲࠧଧ") + str(bstack1l1l1lll1_opy_)),
                          bstack111l1_opy_ (u"ࠢࡦࡴࡵࡳࡷࠨନ"))
      if runner.driver_initialised == bstack111l1_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡵࡷࡩࡵࠨ଩"):
        bstack11ll111ll_opy_(getattr(context, bstack111l1_opy_ (u"ࠩࡳࡥ࡬࡫ࠧପ"), None), bstack111l1_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥଫ"), bstack1ll11l1l1l_opy_)
        bstack1l11l1llll_opy_.execute_script(bstack111l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡧࡥࡹࡧࠢ࠻ࠩବ") + json.dumps(str(args[0].name) + bstack111l1_opy_ (u"ࠧࠦ࠭ࠡࡈࡤ࡭ࡱ࡫ࡤࠢ࡞ࡱࠦଭ") + str(bstack1l1l1lll1_opy_)) + bstack111l1_opy_ (u"࠭ࠬࠡࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠣࠦࡪࡸࡲࡰࡴࠥࢁࢂ࠭ମ"))
      if runner.driver_initialised == bstack111l1_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡴࡶࡨࡴࠧଯ"):
        bstack1lll1111l1_opy_(bstack1l11l1llll_opy_, bstack111l1_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨର"), bstack111l1_opy_ (u"ࠤࡖࡧࡪࡴࡡࡳ࡫ࡲࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡼ࡯ࡴࡩ࠼ࠣࡠࡳࠨ଱") + str(bstack1ll11l1l1l_opy_))
    else:
      bstack1l1l11l1l1_opy_(context, bstack111l1_opy_ (u"ࠥࡔࡦࡹࡳࡦࡦࠤࠦଲ"), bstack111l1_opy_ (u"ࠦ࡮ࡴࡦࡰࠤଳ"))
      if runner.driver_initialised == bstack111l1_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡹࡴࡦࡲࠥ଴"):
        bstack11ll111ll_opy_(getattr(context, bstack111l1_opy_ (u"࠭ࡰࡢࡩࡨࠫଵ"), None), bstack111l1_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢଶ"))
      bstack1l11l1llll_opy_.execute_script(bstack111l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡤࡢࡶࡤࠦ࠿࠭ଷ") + json.dumps(str(args[0].name) + bstack111l1_opy_ (u"ࠤࠣ࠱ࠥࡖࡡࡴࡵࡨࡨࠦࠨସ")) + bstack111l1_opy_ (u"ࠪ࠰ࠥࠨ࡬ࡦࡸࡨࡰࠧࡀࠠࠣ࡫ࡱࡪࡴࠨࡽࡾࠩହ"))
      if runner.driver_initialised == bstack111l1_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡸࡺࡥࡱࠤ଺"):
        bstack1lll1111l1_opy_(bstack1l11l1llll_opy_, bstack111l1_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧ଻"))
  except Exception as e:
    logger.debug(bstack111l1_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡰࡥࡷࡱࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡵࡷࡥࡹࡻࡳࠡ࡫ࡱࠤࡦ࡬ࡴࡦࡴࠣࡷࡹ࡫ࡰ࠻ࠢࡾࢁ଼ࠬ").format(str(e)))
  bstack1l1ll1l111_opy_(runner, name, context, args[0], bstack1l111l111l_opy_, *args)
def bstack1ll1111ll1_opy_(runner, name, context, bstack1l111l111l_opy_, *args):
  bstack1l1111llll_opy_.end_test(args[0])
  try:
    bstack1l1lll1l_opy_ = args[0].status.name
    bstack1l11l1llll_opy_ = bstack11l1ll1l1_opy_(threading.current_thread(), bstack111l1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭ଽ"), context.browser)
    bstack1l11l1l1_opy_.bstack1ll111l1_opy_(bstack1l11l1llll_opy_)
    if str(bstack1l1lll1l_opy_).lower() == bstack111l1_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨା"):
      bstack1ll11l1l1l_opy_ = bstack111l1_opy_ (u"ࠩࠪି")
      bstack1l1l1lll1_opy_ = bstack111l1_opy_ (u"ࠪࠫୀ")
      bstack1llll11l1_opy_ = bstack111l1_opy_ (u"ࠫࠬୁ")
      try:
        import traceback
        bstack1ll11l1l1l_opy_ = runner.exception.__class__.__name__
        bstack11ll1lll1_opy_ = traceback.format_tb(runner.exc_traceback)
        bstack1l1l1lll1_opy_ = bstack111l1_opy_ (u"ࠬࠦࠧୂ").join(bstack11ll1lll1_opy_)
        bstack1llll11l1_opy_ = bstack11ll1lll1_opy_[-1]
      except Exception as e:
        logger.debug(bstack11111111l_opy_.format(str(e)))
      bstack1ll11l1l1l_opy_ += bstack1llll11l1_opy_
      bstack1l1l11l1l1_opy_(context, json.dumps(str(args[0].name) + bstack111l1_opy_ (u"ࠨࠠ࠮ࠢࡉࡥ࡮ࡲࡥࡥࠣ࡟ࡲࠧୃ") + str(bstack1l1l1lll1_opy_)),
                          bstack111l1_opy_ (u"ࠢࡦࡴࡵࡳࡷࠨୄ"))
      if runner.driver_initialised == bstack111l1_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡵࡦࡩࡳࡧࡲࡪࡱࠥ୅") or runner.driver_initialised == bstack111l1_opy_ (u"ࠩ࡬ࡲࡸࡺࡥࡱࠩ୆"):
        bstack11ll111ll_opy_(getattr(context, bstack111l1_opy_ (u"ࠪࡴࡦ࡭ࡥࠨେ"), None), bstack111l1_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦୈ"), bstack1ll11l1l1l_opy_)
        bstack1l11l1llll_opy_.execute_script(bstack111l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡨࡦࡺࡡࠣ࠼ࠪ୉") + json.dumps(str(args[0].name) + bstack111l1_opy_ (u"ࠨࠠ࠮ࠢࡉࡥ࡮ࡲࡥࡥࠣ࡟ࡲࠧ୊") + str(bstack1l1l1lll1_opy_)) + bstack111l1_opy_ (u"ࠧ࠭ࠢࠥࡰࡪࡼࡥ࡭ࠤ࠽ࠤࠧ࡫ࡲࡳࡱࡵࠦࢂࢃࠧୋ"))
      if runner.driver_initialised == bstack111l1_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡵࡦࡩࡳࡧࡲࡪࡱࠥୌ") or runner.driver_initialised == bstack111l1_opy_ (u"ࠩ࡬ࡲࡸࡺࡥࡱ୍ࠩ"):
        bstack1lll1111l1_opy_(bstack1l11l1llll_opy_, bstack111l1_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ୎"), bstack111l1_opy_ (u"ࠦࡘࡩࡥ࡯ࡣࡵ࡭ࡴࠦࡦࡢ࡫࡯ࡩࡩࠦࡷࡪࡶ࡫࠾ࠥࡢ࡮ࠣ୏") + str(bstack1ll11l1l1l_opy_))
    else:
      bstack1l1l11l1l1_opy_(context, bstack111l1_opy_ (u"ࠧࡖࡡࡴࡵࡨࡨࠦࠨ୐"), bstack111l1_opy_ (u"ࠨࡩ࡯ࡨࡲࠦ୑"))
      if runner.driver_initialised == bstack111l1_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡴࡥࡨࡲࡦࡸࡩࡰࠤ୒") or runner.driver_initialised == bstack111l1_opy_ (u"ࠨ࡫ࡱࡷࡹ࡫ࡰࠨ୓"):
        bstack11ll111ll_opy_(getattr(context, bstack111l1_opy_ (u"ࠩࡳࡥ࡬࡫ࠧ୔"), None), bstack111l1_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥ୕"))
      bstack1l11l1llll_opy_.execute_script(bstack111l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡧࡥࡹࡧࠢ࠻ࠩୖ") + json.dumps(str(args[0].name) + bstack111l1_opy_ (u"ࠧࠦ࠭ࠡࡒࡤࡷࡸ࡫ࡤࠢࠤୗ")) + bstack111l1_opy_ (u"࠭ࠬࠡࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠣࠦ࡮ࡴࡦࡰࠤࢀࢁࠬ୘"))
      if runner.driver_initialised == bstack111l1_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡴࡥࡨࡲࡦࡸࡩࡰࠤ୙") or runner.driver_initialised == bstack111l1_opy_ (u"ࠨ࡫ࡱࡷࡹ࡫ࡰࠨ୚"):
        bstack1lll1111l1_opy_(bstack1l11l1llll_opy_, bstack111l1_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠤ୛"))
  except Exception as e:
    logger.debug(bstack111l1_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦ࡭ࡢࡴ࡮ࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡹࡴࡢࡶࡸࡷࠥ࡯࡮ࠡࡣࡩࡸࡪࡸࠠࡧࡧࡤࡸࡺࡸࡥ࠻ࠢࡾࢁࠬଡ଼").format(str(e)))
  bstack1l1ll1l111_opy_(runner, name, context, context.scenario, bstack1l111l111l_opy_, *args)
  if len(context.scenario.tags) == 0: threading.current_thread().current_test_uuid = None
def bstack11111ll1_opy_(runner, name, context, bstack1l111l111l_opy_, *args):
    bstack1l1ll1l111_opy_(runner, name, context, context.scenario, bstack1l111l111l_opy_, *args)
    threading.current_thread().current_test_uuid = None
def bstack1111l111l_opy_(runner, name, context, bstack1l111l111l_opy_, *args):
    try:
      bstack1l11l1llll_opy_ = bstack11l1ll1l1_opy_(threading.current_thread(), bstack111l1_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪଢ଼"), context.browser)
      if context.failed is True:
        bstack1lll1l11ll_opy_ = []
        bstack1ll1lll1ll_opy_ = []
        bstack1ll1111111_opy_ = []
        bstack11ll1l111_opy_ = bstack111l1_opy_ (u"ࠬ࠭୞")
        try:
          import traceback
          for exc in runner.exception_arr:
            bstack1lll1l11ll_opy_.append(exc.__class__.__name__)
          for exc_tb in runner.exc_traceback_arr:
            bstack11ll1lll1_opy_ = traceback.format_tb(exc_tb)
            bstack1l1111111l_opy_ = bstack111l1_opy_ (u"࠭ࠠࠨୟ").join(bstack11ll1lll1_opy_)
            bstack1ll1lll1ll_opy_.append(bstack1l1111111l_opy_)
            bstack1ll1111111_opy_.append(bstack11ll1lll1_opy_[-1])
        except Exception as e:
          logger.debug(bstack11111111l_opy_.format(str(e)))
        bstack1ll11l1l1l_opy_ = bstack111l1_opy_ (u"ࠧࠨୠ")
        for i in range(len(bstack1lll1l11ll_opy_)):
          bstack1ll11l1l1l_opy_ += bstack1lll1l11ll_opy_[i] + bstack1ll1111111_opy_[i] + bstack111l1_opy_ (u"ࠨ࡞ࡱࠫୡ")
        bstack11ll1l111_opy_ = bstack111l1_opy_ (u"ࠩࠣࠫୢ").join(bstack1ll1lll1ll_opy_)
        if runner.driver_initialised in [bstack111l1_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡪࡪࡧࡴࡶࡴࡨࠦୣ"), bstack111l1_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡦࡲ࡬ࠣ୤")]:
          bstack1l1l11l1l1_opy_(context, bstack11ll1l111_opy_, bstack111l1_opy_ (u"ࠧ࡫ࡲࡳࡱࡵࠦ୥"))
          bstack11ll111ll_opy_(getattr(context, bstack111l1_opy_ (u"࠭ࡰࡢࡩࡨࠫ୦"), None), bstack111l1_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢ୧"), bstack1ll11l1l1l_opy_)
          bstack1l11l1llll_opy_.execute_script(bstack111l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡤࡢࡶࡤࠦ࠿࠭୨") + json.dumps(bstack11ll1l111_opy_) + bstack111l1_opy_ (u"ࠩ࠯ࠤࠧࡲࡥࡷࡧ࡯ࠦ࠿ࠦࠢࡦࡴࡵࡳࡷࠨࡽࡾࠩ୩"))
          bstack1lll1111l1_opy_(bstack1l11l1llll_opy_, bstack111l1_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥ୪"), bstack111l1_opy_ (u"ࠦࡘࡵ࡭ࡦࠢࡶࡧࡪࡴࡡࡳ࡫ࡲࡷࠥ࡬ࡡࡪ࡮ࡨࡨ࠿ࠦ࡜࡯ࠤ୫") + str(bstack1ll11l1l1l_opy_))
          bstack1111ll11_opy_ = bstack1l11llll1_opy_(bstack11ll1l111_opy_, runner.feature.name, logger)
          if (bstack1111ll11_opy_ != None):
            bstack1l1l1ll1l1_opy_.append(bstack1111ll11_opy_)
      else:
        if runner.driver_initialised in [bstack111l1_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤ࡬ࡥࡢࡶࡸࡶࡪࠨ୬"), bstack111l1_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡡ࡭࡮ࠥ୭")]:
          bstack1l1l11l1l1_opy_(context, bstack111l1_opy_ (u"ࠢࡇࡧࡤࡸࡺࡸࡥ࠻ࠢࠥ୮") + str(runner.feature.name) + bstack111l1_opy_ (u"ࠣࠢࡳࡥࡸࡹࡥࡥࠣࠥ୯"), bstack111l1_opy_ (u"ࠤ࡬ࡲ࡫ࡵࠢ୰"))
          bstack11ll111ll_opy_(getattr(context, bstack111l1_opy_ (u"ࠪࡴࡦ࡭ࡥࠨୱ"), None), bstack111l1_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠦ୲"))
          bstack1l11l1llll_opy_.execute_script(bstack111l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡨࡦࡺࡡࠣ࠼ࠪ୳") + json.dumps(bstack111l1_opy_ (u"ࠨࡆࡦࡣࡷࡹࡷ࡫࠺ࠡࠤ୴") + str(runner.feature.name) + bstack111l1_opy_ (u"ࠢࠡࡲࡤࡷࡸ࡫ࡤࠢࠤ୵")) + bstack111l1_opy_ (u"ࠨ࠮ࠣࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠥࠨࡩ࡯ࡨࡲࠦࢂࢃࠧ୶"))
          bstack1lll1111l1_opy_(bstack1l11l1llll_opy_, bstack111l1_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ୷"))
          bstack1111ll11_opy_ = bstack1l11llll1_opy_(bstack11ll1l111_opy_, runner.feature.name, logger)
          if (bstack1111ll11_opy_ != None):
            bstack1l1l1ll1l1_opy_.append(bstack1111ll11_opy_)
    except Exception as e:
      logger.debug(bstack111l1_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦ࡭ࡢࡴ࡮ࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡹࡴࡢࡶࡸࡷࠥ࡯࡮ࠡࡣࡩࡸࡪࡸࠠࡧࡧࡤࡸࡺࡸࡥ࠻ࠢࡾࢁࠬ୸").format(str(e)))
    bstack1l1ll1l111_opy_(runner, name, context, context.feature, bstack1l111l111l_opy_, *args)
def bstack1llll11lll_opy_(self, name, context, *args):
  if bstack1l1l111l_opy_:
    platform_index = int(threading.current_thread()._name) % bstack1ll111l11l_opy_
    bstack1l11l11ll_opy_ = CONFIG[bstack111l1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ୹")][platform_index]
    os.environ[bstack111l1_opy_ (u"ࠬࡉࡕࡓࡔࡈࡒ࡙ࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡆࡄࡘࡆ࠭୺")] = json.dumps(bstack1l11l11ll_opy_)
  global bstack1l111l111l_opy_
  if not hasattr(self, bstack111l1_opy_ (u"࠭ࡤࡳ࡫ࡹࡩࡷࡥࡩ࡯࡫ࡷ࡭ࡦࡲࡩࡴࡧࡧࠫ୻")):
    self.driver_initialised = None
  bstack1l1lll11ll_opy_ = {
      bstack111l1_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫࡟ࡢ࡮࡯ࠫ୼"): bstack1lllllllll_opy_,
      bstack111l1_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࡠࡨࡨࡥࡹࡻࡲࡦࠩ୽"): bstack1l1111l11l_opy_,
      bstack111l1_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࡡࡷࡥ࡬࠭୾"): bstack1ll1l1lll_opy_,
      bstack111l1_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬ୿"): bstack1l11l1lll_opy_,
      bstack111l1_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࡣࡸࡺࡥࡱࠩ஀"): bstack1111lllll_opy_,
      bstack111l1_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣࡸࡺࡥࡱࠩ஁"): bstack1l1111ll_opy_,
      bstack111l1_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤࡹࡣࡦࡰࡤࡶ࡮ࡵࠧஂ"): bstack1ll1111ll1_opy_,
      bstack111l1_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡴࡢࡩࠪஃ"): bstack11111ll1_opy_,
      bstack111l1_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡧࡧࡤࡸࡺࡸࡥࠨ஄"): bstack1111l111l_opy_,
      bstack111l1_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡣ࡯ࡰࠬஅ"): lambda *args: bstack1l1ll1l111_opy_(*args, self)
  }
  handler = bstack1l1lll11ll_opy_.get(name, bstack1l111l111l_opy_)
  handler(self, name, context, bstack1l111l111l_opy_, *args)
  if name in [bstack111l1_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡩࡩࡦࡺࡵࡳࡧࠪஆ"), bstack111l1_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬஇ"), bstack111l1_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣࡦࡲ࡬ࠨஈ")]:
    try:
      bstack1l11l1llll_opy_ = threading.current_thread().bstackSessionDriver if bstack1l111ll11l_opy_(bstack111l1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬஉ")) else context.browser
      bstack1111l1l11_opy_ = (
        (name == bstack111l1_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡡ࡭࡮ࠪஊ") and self.driver_initialised == bstack111l1_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡣ࡯ࡰࠧ஋")) or
        (name == bstack111l1_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡨࡨࡥࡹࡻࡲࡦࠩ஌") and self.driver_initialised == bstack111l1_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡪࡪࡧࡴࡶࡴࡨࠦ஍")) or
        (name == bstack111l1_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬஎ") and self.driver_initialised in [bstack111l1_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡹࡣࡦࡰࡤࡶ࡮ࡵࠢஏ"), bstack111l1_opy_ (u"ࠨࡩ࡯ࡵࡷࡩࡵࠨஐ")]) or
        (name == bstack111l1_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡳࡵࡧࡳࠫ஑") and self.driver_initialised == bstack111l1_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡵࡷࡩࡵࠨஒ"))
      )
      if bstack1111l1l11_opy_:
        self.driver_initialised = None
        bstack1l11l1llll_opy_.quit()
    except Exception:
      pass
def bstack11111ll1l_opy_(config, startdir):
  return bstack111l1_opy_ (u"ࠤࡧࡶ࡮ࡼࡥࡳ࠼ࠣࡿ࠵ࢃࠢஓ").format(bstack111l1_opy_ (u"ࠥࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠤஔ"))
notset = Notset()
def bstack111l1ll11_opy_(self, name: str, default=notset, skip: bool = False):
  global bstack1l111l11l_opy_
  if str(name).lower() == bstack111l1_opy_ (u"ࠫࡩࡸࡩࡷࡧࡵࠫக"):
    return bstack111l1_opy_ (u"ࠧࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠦ஖")
  else:
    return bstack1l111l11l_opy_(self, name, default, skip)
def bstack1llll1ll1_opy_(item, when):
  global bstack1l1l111l11_opy_
  try:
    bstack1l1l111l11_opy_(item, when)
  except Exception as e:
    pass
def bstack111ll1lll_opy_():
  return
def bstack11llll1l_opy_(type, name, status, reason, bstack1l111l11ll_opy_, bstack1lll11l11l_opy_):
  bstack1l1l11lll1_opy_ = {
    bstack111l1_opy_ (u"࠭ࡡࡤࡶ࡬ࡳࡳ࠭஗"): type,
    bstack111l1_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪ஘"): {}
  }
  if type == bstack111l1_opy_ (u"ࠨࡣࡱࡲࡴࡺࡡࡵࡧࠪங"):
    bstack1l1l11lll1_opy_[bstack111l1_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬச")][bstack111l1_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩ஛")] = bstack1l111l11ll_opy_
    bstack1l1l11lll1_opy_[bstack111l1_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧஜ")][bstack111l1_opy_ (u"ࠬࡪࡡࡵࡣࠪ஝")] = json.dumps(str(bstack1lll11l11l_opy_))
  if type == bstack111l1_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧஞ"):
    bstack1l1l11lll1_opy_[bstack111l1_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪட")][bstack111l1_opy_ (u"ࠨࡰࡤࡱࡪ࠭஠")] = name
  if type == bstack111l1_opy_ (u"ࠩࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠬ஡"):
    bstack1l1l11lll1_opy_[bstack111l1_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭஢")][bstack111l1_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫண")] = status
    if status == bstack111l1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬத"):
      bstack1l1l11lll1_opy_[bstack111l1_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩ஥")][bstack111l1_opy_ (u"ࠧࡳࡧࡤࡷࡴࡴࠧ஦")] = json.dumps(str(reason))
  bstack111llllll_opy_ = bstack111l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࢂ࠭஧").format(json.dumps(bstack1l1l11lll1_opy_))
  return bstack111llllll_opy_
def bstack11l111111_opy_(driver_command, response):
    if driver_command == bstack111l1_opy_ (u"ࠩࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹ࠭ந"):
        bstack11llllll11_opy_.bstack11ll11l1_opy_({
            bstack111l1_opy_ (u"ࠪ࡭ࡲࡧࡧࡦࠩன"): response[bstack111l1_opy_ (u"ࠫࡻࡧ࡬ࡶࡧࠪப")],
            bstack111l1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ஫"): bstack11llllll11_opy_.current_test_uuid()
        })
def bstack1ll11l1ll_opy_(item, call, rep):
  global bstack1l111111l_opy_
  global bstack1l1ll1l1l_opy_
  global bstack1l1l1l1l_opy_
  name = bstack111l1_opy_ (u"࠭ࠧ஬")
  try:
    if rep.when == bstack111l1_opy_ (u"ࠧࡤࡣ࡯ࡰࠬ஭"):
      bstack1l1111l111_opy_ = threading.current_thread().bstackSessionId
      try:
        if not bstack1l1l1l1l_opy_:
          name = str(rep.nodeid)
          bstack11lll11l_opy_ = bstack11llll1l_opy_(bstack111l1_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩம"), name, bstack111l1_opy_ (u"ࠩࠪய"), bstack111l1_opy_ (u"ࠪࠫர"), bstack111l1_opy_ (u"ࠫࠬற"), bstack111l1_opy_ (u"ࠬ࠭ல"))
          threading.current_thread().bstack1llllllll_opy_ = name
          for driver in bstack1l1ll1l1l_opy_:
            if bstack1l1111l111_opy_ == driver.session_id:
              driver.execute_script(bstack11lll11l_opy_)
      except Exception as e:
        logger.debug(bstack111l1_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡵࡨࡸࡹ࡯࡮ࡨࠢࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠠࡧࡱࡵࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡵࡨࡷࡸ࡯࡯࡯࠼ࠣࡿࢂ࠭ள").format(str(e)))
      try:
        bstack1ll11l111_opy_(rep.outcome.lower())
        if rep.outcome.lower() != bstack111l1_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨழ"):
          status = bstack111l1_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨவ") if rep.outcome.lower() == bstack111l1_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩஶ") else bstack111l1_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪஷ")
          reason = bstack111l1_opy_ (u"ࠫࠬஸ")
          if status == bstack111l1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬஹ"):
            reason = rep.longrepr.reprcrash.message
            if (not threading.current_thread().bstackTestErrorMessages):
              threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(reason)
          level = bstack111l1_opy_ (u"࠭ࡩ࡯ࡨࡲࠫ஺") if status == bstack111l1_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧ஻") else bstack111l1_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧ஼")
          data = name + bstack111l1_opy_ (u"ࠩࠣࡴࡦࡹࡳࡦࡦࠤࠫ஽") if status == bstack111l1_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪா") else name + bstack111l1_opy_ (u"ࠫࠥ࡬ࡡࡪ࡮ࡨࡨࠦࠦࠧி") + reason
          bstack1l11l111l_opy_ = bstack11llll1l_opy_(bstack111l1_opy_ (u"ࠬࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠧீ"), bstack111l1_opy_ (u"࠭ࠧு"), bstack111l1_opy_ (u"ࠧࠨூ"), bstack111l1_opy_ (u"ࠨࠩ௃"), level, data)
          for driver in bstack1l1ll1l1l_opy_:
            if bstack1l1111l111_opy_ == driver.session_id:
              driver.execute_script(bstack1l11l111l_opy_)
      except Exception as e:
        logger.debug(bstack111l1_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡣࡰࡰࡷࡩࡽࡺࠠࡧࡱࡵࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡵࡨࡷࡸ࡯࡯࡯࠼ࠣࡿࢂ࠭௄").format(str(e)))
  except Exception as e:
    logger.debug(bstack111l1_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥ࡭ࡥࡵࡶ࡬ࡲ࡬ࠦࡳࡵࡣࡷࡩࠥ࡯࡮ࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡺࡥࡴࡶࠣࡷࡹࡧࡴࡶࡵ࠽ࠤࢀࢃࠧ௅").format(str(e)))
  bstack1l111111l_opy_(item, call, rep)
def bstack11l1l111_opy_(driver, bstack1lll111111_opy_, test=None):
  global bstack1l11llll1l_opy_
  if test != None:
    bstack1ll11l1lll_opy_ = getattr(test, bstack111l1_opy_ (u"ࠫࡳࡧ࡭ࡦࠩெ"), None)
    bstack1l1ll1l11l_opy_ = getattr(test, bstack111l1_opy_ (u"ࠬࡻࡵࡪࡦࠪே"), None)
    PercySDK.screenshot(driver, bstack1lll111111_opy_, bstack1ll11l1lll_opy_=bstack1ll11l1lll_opy_, bstack1l1ll1l11l_opy_=bstack1l1ll1l11l_opy_, bstack11l1lll1_opy_=bstack1l11llll1l_opy_)
  else:
    PercySDK.screenshot(driver, bstack1lll111111_opy_)
def bstack1lll1l1111_opy_(driver):
  if bstack1l1l111111_opy_.bstack1lll1lll1l_opy_() is True or bstack1l1l111111_opy_.capturing() is True:
    return
  bstack1l1l111111_opy_.bstack1ll1ll1ll_opy_()
  while not bstack1l1l111111_opy_.bstack1lll1lll1l_opy_():
    bstack1l1ll1111l_opy_ = bstack1l1l111111_opy_.bstack1llll11l1l_opy_()
    bstack11l1l111_opy_(driver, bstack1l1ll1111l_opy_)
  bstack1l1l111111_opy_.bstack11111ll11_opy_()
def bstack11l11l1ll_opy_(sequence, driver_command, response = None, bstack11ll1l1l_opy_ = None, args = None):
    try:
      if sequence != bstack111l1_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪ࠭ை"):
        return
      if percy.bstack1l1ll1l1_opy_() == bstack111l1_opy_ (u"ࠢࡧࡣ࡯ࡷࡪࠨ௉"):
        return
      bstack1l1ll1111l_opy_ = bstack11l1ll1l1_opy_(threading.current_thread(), bstack111l1_opy_ (u"ࠨࡲࡨࡶࡨࡿࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫொ"), None)
      for command in bstack1lllllll1_opy_:
        if command == driver_command:
          for driver in bstack1l1ll1l1l_opy_:
            bstack1lll1l1111_opy_(driver)
      bstack11ll1111_opy_ = percy.bstack11llll11_opy_()
      if driver_command in bstack1lll1l1lll_opy_[bstack11ll1111_opy_]:
        bstack1l1l111111_opy_.bstack111l1l11_opy_(bstack1l1ll1111l_opy_, driver_command)
    except Exception as e:
      pass
def bstack111l1111_opy_(framework_name):
  if bstack1111ll1l1_opy_.get_property(bstack111l1_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡰࡳࡩࡥࡣࡢ࡮࡯ࡩࡩ࠭ோ")):
      return
  bstack1111ll1l1_opy_.bstack1lll11lll_opy_(bstack111l1_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡱࡴࡪ࡟ࡤࡣ࡯ࡰࡪࡪࠧௌ"), True)
  global bstack1l111l1l_opy_
  global bstack1111111ll_opy_
  global bstack1l1l11l11l_opy_
  bstack1l111l1l_opy_ = framework_name
  logger.info(bstack1l11111111_opy_.format(bstack1l111l1l_opy_.split(bstack111l1_opy_ (u"ࠫ࠲்࠭"))[0]))
  bstack1lll1ll1_opy_()
  try:
    from selenium import webdriver
    from selenium.webdriver.common.service import Service
    from selenium.webdriver.remote.webdriver import WebDriver
    if bstack1l1l111l_opy_:
      Service.start = bstack1l1ll1l1ll_opy_
      Service.stop = bstack111111111_opy_
      webdriver.Remote.get = bstack1l11111lll_opy_
      WebDriver.close = bstack1ll111ll11_opy_
      WebDriver.quit = bstack1l11lll11l_opy_
      webdriver.Remote.__init__ = bstack1lllll1l1l_opy_
      WebDriver.getAccessibilityResults = getAccessibilityResults
      WebDriver.get_accessibility_results = getAccessibilityResults
      WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
      WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
      WebDriver.performScan = perform_scan
      WebDriver.perform_scan = perform_scan
    if not bstack1l1l111l_opy_:
        webdriver.Remote.__init__ = bstack11ll1llll_opy_
    WebDriver.execute = bstack1l1llllll1_opy_
    bstack1111111ll_opy_ = True
  except Exception as e:
    pass
  try:
    if bstack1l1l111l_opy_:
      from QWeb.keywords import browser
      browser.close_browser = bstack1111ll1l_opy_
  except Exception as e:
    pass
  bstack1l1ll1lll_opy_()
  if not bstack1111111ll_opy_:
    bstack1ll11l11l_opy_(bstack111l1_opy_ (u"ࠧࡖࡡࡤ࡭ࡤ࡫ࡪࡹࠠ࡯ࡱࡷࠤ࡮ࡴࡳࡵࡣ࡯ࡰࡪࡪࠢ௎"), bstack1ll111111_opy_)
  if bstack1ll11lll1_opy_():
    try:
      from selenium.webdriver.remote.remote_connection import RemoteConnection
      RemoteConnection._get_proxy_url = bstack1lll1ll111_opy_
    except Exception as e:
      logger.error(bstack1ll1111lll_opy_.format(str(e)))
  if bstack1l1llll1l_opy_():
    bstack1l1111l1l_opy_(CONFIG, logger)
  if (bstack111l1_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬ௏") in str(framework_name).lower()):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        if percy.bstack1l1ll1l1_opy_() == bstack111l1_opy_ (u"ࠢࡵࡴࡸࡩࠧௐ"):
          bstack1llll1ll11_opy_(bstack11l11l1ll_opy_)
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        WebDriverCreator._get_ff_profile = bstack1ll1l1l11l_opy_
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCache.close = bstack1l1llll11_opy_
      except Exception as e:
        logger.warn(bstack11lll11l1_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import ApplicationCache
        ApplicationCache.close = bstack111llll1l_opy_
      except Exception as e:
        logger.debug(bstack1l1l11ll_opy_ + str(e))
    except Exception as e:
      bstack1ll11l11l_opy_(e, bstack11lll11l1_opy_)
    Output.start_test = bstack1ll1l11ll1_opy_
    Output.end_test = bstack1l111ll11_opy_
    TestStatus.__init__ = bstack111l1ll1l_opy_
    QueueItem.__init__ = bstack111l11l1_opy_
    pabot._create_items = bstack11ll11ll_opy_
    try:
      from pabot import __version__ as bstack1l111ll1ll_opy_
      if version.parse(bstack1l111ll1ll_opy_) >= version.parse(bstack111l1_opy_ (u"ࠨ࠴࠱࠵࠺࠴࠰ࠨ௑")):
        pabot._run = bstack1l11ll1111_opy_
      elif version.parse(bstack1l111ll1ll_opy_) >= version.parse(bstack111l1_opy_ (u"ࠩ࠵࠲࠶࠹࠮࠱ࠩ௒")):
        pabot._run = bstack1lll11l111_opy_
      else:
        pabot._run = bstack1l111111l1_opy_
    except Exception as e:
      pabot._run = bstack1l111111l1_opy_
    pabot._create_command_for_execution = bstack11l1llll1_opy_
    pabot._report_results = bstack1l11lll1l_opy_
  if bstack111l1_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪ௓") in str(framework_name).lower():
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1ll11l11l_opy_(e, bstack1ll1l1l1l_opy_)
    Runner.run_hook = bstack1llll11lll_opy_
    Step.run = bstack1llll11l11_opy_
  if bstack111l1_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ௔") in str(framework_name).lower():
    if not bstack1l1l111l_opy_:
      return
    try:
      if percy.bstack1l1ll1l1_opy_() == bstack111l1_opy_ (u"ࠧࡺࡲࡶࡧࠥ௕"):
          bstack1llll1ll11_opy_(bstack11l11l1ll_opy_)
      from pytest_selenium import pytest_selenium
      from _pytest.config import Config
      pytest_selenium.pytest_report_header = bstack11111ll1l_opy_
      from pytest_selenium.drivers import browserstack
      browserstack.pytest_selenium_runtest_makereport = bstack111ll1lll_opy_
      Config.getoption = bstack111l1ll11_opy_
    except Exception as e:
      pass
    try:
      from pytest_bdd import reporting
      reporting.runtest_makereport = bstack1ll11l1ll_opy_
    except Exception as e:
      pass
def bstack11ll1l1ll_opy_():
  global CONFIG
  if bstack111l1_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭௖") in CONFIG and int(CONFIG[bstack111l1_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧௗ")]) > 1:
    logger.warn(bstack11l111ll1_opy_)
def bstack1ll11lll_opy_(arg, bstack1l11l1ll11_opy_, bstack1ll111l111_opy_=None):
  global CONFIG
  global bstack11l1l111l_opy_
  global bstack1l111ll111_opy_
  global bstack1l1l111l_opy_
  global bstack1111ll1l1_opy_
  bstack1l111l1l1l_opy_ = bstack111l1_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ௘")
  if bstack1l11l1ll11_opy_ and isinstance(bstack1l11l1ll11_opy_, str):
    bstack1l11l1ll11_opy_ = eval(bstack1l11l1ll11_opy_)
  CONFIG = bstack1l11l1ll11_opy_[bstack111l1_opy_ (u"ࠩࡆࡓࡓࡌࡉࡈࠩ௙")]
  bstack11l1l111l_opy_ = bstack1l11l1ll11_opy_[bstack111l1_opy_ (u"ࠪࡌ࡚ࡈ࡟ࡖࡔࡏࠫ௚")]
  bstack1l111ll111_opy_ = bstack1l11l1ll11_opy_[bstack111l1_opy_ (u"ࠫࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭௛")]
  bstack1l1l111l_opy_ = bstack1l11l1ll11_opy_[bstack111l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࠨ௜")]
  bstack1111ll1l1_opy_.bstack1lll11lll_opy_(bstack111l1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡳࡦࡵࡶ࡭ࡴࡴࠧ௝"), bstack1l1l111l_opy_)
  os.environ[bstack111l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࠩ௞")] = bstack1l111l1l1l_opy_
  os.environ[bstack111l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡑࡑࡊࡎࡍࠧ௟")] = json.dumps(CONFIG)
  os.environ[bstack111l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡊࡘࡆࡤ࡛ࡒࡍࠩ௠")] = bstack11l1l111l_opy_
  os.environ[bstack111l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡌࡗࡤࡇࡐࡑࡡࡄ࡙࡙ࡕࡍࡂࡖࡈࠫ௡")] = str(bstack1l111ll111_opy_)
  os.environ[bstack111l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔ࡞࡚ࡅࡔࡖࡢࡔࡑ࡛ࡇࡊࡐࠪ௢")] = str(True)
  if bstack11ll11ll1_opy_(arg, [bstack111l1_opy_ (u"ࠬ࠳࡮ࠨ௣"), bstack111l1_opy_ (u"࠭࠭࠮ࡰࡸࡱࡵࡸ࡯ࡤࡧࡶࡷࡪࡹࠧ௤")]) != -1:
    os.environ[bstack111l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐ࡚ࡖࡈࡗ࡙ࡥࡐࡂࡔࡄࡐࡑࡋࡌࠨ௥")] = str(True)
  if len(sys.argv) <= 1:
    logger.critical(bstack1l1lll1ll1_opy_)
    return
  bstack1lllll11_opy_()
  global bstack11lll1111_opy_
  global bstack1l11llll1l_opy_
  global bstack1111l1ll1_opy_
  global bstack111l111ll_opy_
  global bstack1l11111l1_opy_
  global bstack1l1l11l11l_opy_
  global bstack1ll11l1l_opy_
  arg.append(bstack111l1_opy_ (u"ࠣ࠯࡚ࠦ௦"))
  arg.append(bstack111l1_opy_ (u"ࠤ࡬࡫ࡳࡵࡲࡦ࠼ࡐࡳࡩࡻ࡬ࡦࠢࡤࡰࡷ࡫ࡡࡥࡻࠣ࡭ࡲࡶ࡯ࡳࡶࡨࡨ࠿ࡶࡹࡵࡧࡶࡸ࠳ࡖࡹࡵࡧࡶࡸ࡜ࡧࡲ࡯࡫ࡱ࡫ࠧ௧"))
  arg.append(bstack111l1_opy_ (u"ࠥ࠱࡜ࠨ௨"))
  arg.append(bstack111l1_opy_ (u"ࠦ࡮࡭࡮ࡰࡴࡨ࠾࡙࡮ࡥࠡࡪࡲࡳࡰ࡯࡭ࡱ࡮ࠥ௩"))
  global bstack1llll1lll1_opy_
  global bstack1lll1l1l1l_opy_
  global bstack1l1l1l1111_opy_
  global bstack1l1lll1l1_opy_
  global bstack1l111lll1l_opy_
  global bstack1ll11ll1_opy_
  global bstack1l1l1ll11_opy_
  global bstack1ll1ll1l_opy_
  global bstack1l1lll1l11_opy_
  global bstack1l11l11ll1_opy_
  global bstack1l111l11l_opy_
  global bstack1l1l111l11_opy_
  global bstack1l111111l_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack1llll1lll1_opy_ = webdriver.Remote.__init__
    bstack1lll1l1l1l_opy_ = WebDriver.quit
    bstack1ll1ll1l_opy_ = WebDriver.close
    bstack1l1lll1l11_opy_ = WebDriver.get
    bstack1l1l1l1111_opy_ = WebDriver.execute
  except Exception as e:
    pass
  if bstack111lll1l_opy_(CONFIG) and bstack1l1llll1ll_opy_():
    if bstack1l1l11l1ll_opy_() < version.parse(bstack1l11ll1l1_opy_):
      logger.error(bstack1l11l1ll1_opy_.format(bstack1l1l11l1ll_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        bstack1l11l11ll1_opy_ = RemoteConnection._get_proxy_url
      except Exception as e:
        logger.error(bstack1ll1111lll_opy_.format(str(e)))
  try:
    from _pytest.config import Config
    bstack1l111l11l_opy_ = Config.getoption
    from _pytest import runner
    bstack1l1l111l11_opy_ = runner._update_current_test_var
  except Exception as e:
    logger.warn(e, bstack1llll1l11l_opy_)
  try:
    from pytest_bdd import reporting
    bstack1l111111l_opy_ = reporting.runtest_makereport
  except Exception as e:
    logger.debug(bstack111l1_opy_ (u"ࠬࡖ࡬ࡦࡣࡶࡩࠥ࡯࡮ࡴࡶࡤࡰࡱࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡸࡴࠦࡲࡶࡰࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡵࡧࡶࡸࡸ࠭௪"))
  bstack1111l1ll1_opy_ = CONFIG.get(bstack111l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪ௫"), {}).get(bstack111l1_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ௬"))
  bstack1ll11l1l_opy_ = True
  bstack111l1111_opy_(bstack111l1l111_opy_)
  os.environ[bstack111l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡖࡕࡈࡖࡓࡇࡍࡆࠩ௭")] = CONFIG[bstack111l1_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫ௮")]
  os.environ[bstack111l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄࡇࡈࡋࡓࡔࡡࡎࡉ࡞࠭௯")] = CONFIG[bstack111l1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧ௰")]
  os.environ[bstack111l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࠨ௱")] = bstack1l1l111l_opy_.__str__()
  from _pytest.config import main as bstack11l1ll111_opy_
  bstack1l11l1111_opy_ = []
  try:
    bstack1lll11111_opy_ = bstack11l1ll111_opy_(arg)
    if bstack111l1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡥࡳࡴࡲࡶࡤࡲࡩࡴࡶࠪ௲") in multiprocessing.current_process().__dict__.keys():
      for bstack1ll111lll1_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack1l11l1111_opy_.append(bstack1ll111lll1_opy_)
    try:
      bstack11l111l1_opy_ = (bstack1l11l1111_opy_, int(bstack1lll11111_opy_))
      bstack1ll111l111_opy_.append(bstack11l111l1_opy_)
    except:
      bstack1ll111l111_opy_.append((bstack1l11l1111_opy_, bstack1lll11111_opy_))
  except Exception as e:
    logger.error(traceback.format_exc())
    bstack1l11l1111_opy_.append({bstack111l1_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ௳"): bstack111l1_opy_ (u"ࠨࡒࡵࡳࡨ࡫ࡳࡴࠢࠪ௴") + os.environ.get(bstack111l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩ௵")), bstack111l1_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩ௶"): traceback.format_exc(), bstack111l1_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪ௷"): int(os.environ.get(bstack111l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬ௸")))})
    bstack1ll111l111_opy_.append((bstack1l11l1111_opy_, 1))
def bstack1lll1111l_opy_(arg):
  global bstack1l1l11111l_opy_
  bstack111l1111_opy_(bstack1l11ll11_opy_)
  os.environ[bstack111l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧ௹")] = str(bstack1l111ll111_opy_)
  from behave.__main__ import main as bstack1111ll111_opy_
  status_code = bstack1111ll111_opy_(arg)
  if status_code != 0:
    bstack1l1l11111l_opy_ = status_code
def bstack11llllll_opy_():
  logger.info(bstack11lllll1l_opy_)
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument(bstack111l1_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭௺"), help=bstack111l1_opy_ (u"ࠨࡉࡨࡲࡪࡸࡡࡵࡧࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡦࡳࡳ࡬ࡩࡨࠩ௻"))
  parser.add_argument(bstack111l1_opy_ (u"ࠩ࠰ࡹࠬ௼"), bstack111l1_opy_ (u"ࠪ࠱࠲ࡻࡳࡦࡴࡱࡥࡲ࡫ࠧ௽"), help=bstack111l1_opy_ (u"ࠫ࡞ࡵࡵࡳࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡷࡶࡩࡷࡴࡡ࡮ࡧࠪ௾"))
  parser.add_argument(bstack111l1_opy_ (u"ࠬ࠳࡫ࠨ௿"), bstack111l1_opy_ (u"࠭࠭࠮࡭ࡨࡽࠬఀ"), help=bstack111l1_opy_ (u"࡚ࠧࡱࡸࡶࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡦࡩࡣࡦࡵࡶࠤࡰ࡫ࡹࠨఁ"))
  parser.add_argument(bstack111l1_opy_ (u"ࠨ࠯ࡩࠫం"), bstack111l1_opy_ (u"ࠩ࠰࠱࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧః"), help=bstack111l1_opy_ (u"ࠪ࡝ࡴࡻࡲࠡࡶࡨࡷࡹࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩఄ"))
  bstack11l11lll_opy_ = parser.parse_args()
  try:
    bstack111l11ll_opy_ = bstack111l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱࡫ࡪࡴࡥࡳ࡫ࡦ࠲ࡾࡳ࡬࠯ࡵࡤࡱࡵࡲࡥࠨఅ")
    if bstack11l11lll_opy_.framework and bstack11l11lll_opy_.framework not in (bstack111l1_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬఆ"), bstack111l1_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠹ࠧఇ")):
      bstack111l11ll_opy_ = bstack111l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡦࡳࡣࡰࡩࡼࡵࡲ࡬࠰ࡼࡱࡱ࠴ࡳࡢ࡯ࡳࡰࡪ࠭ఈ")
    bstack111lll11l_opy_ = os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack111l11ll_opy_)
    bstack1l1lll11_opy_ = open(bstack111lll11l_opy_, bstack111l1_opy_ (u"ࠨࡴࠪఉ"))
    bstack1ll1l11l_opy_ = bstack1l1lll11_opy_.read()
    bstack1l1lll11_opy_.close()
    if bstack11l11lll_opy_.username:
      bstack1ll1l11l_opy_ = bstack1ll1l11l_opy_.replace(bstack111l1_opy_ (u"ࠩ࡜ࡓ࡚ࡘ࡟ࡖࡕࡈࡖࡓࡇࡍࡆࠩఊ"), bstack11l11lll_opy_.username)
    if bstack11l11lll_opy_.key:
      bstack1ll1l11l_opy_ = bstack1ll1l11l_opy_.replace(bstack111l1_opy_ (u"ࠪ࡝ࡔ࡛ࡒࡠࡃࡆࡇࡊ࡙ࡓࡠࡍࡈ࡝ࠬఋ"), bstack11l11lll_opy_.key)
    if bstack11l11lll_opy_.framework:
      bstack1ll1l11l_opy_ = bstack1ll1l11l_opy_.replace(bstack111l1_opy_ (u"ࠫ࡞ࡕࡕࡓࡡࡉࡖࡆࡓࡅࡘࡑࡕࡏࠬఌ"), bstack11l11lll_opy_.framework)
    file_name = bstack111l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡾࡳ࡬ࠨ఍")
    file_path = os.path.abspath(file_name)
    bstack1l1l1l1l11_opy_ = open(file_path, bstack111l1_opy_ (u"࠭ࡷࠨఎ"))
    bstack1l1l1l1l11_opy_.write(bstack1ll1l11l_opy_)
    bstack1l1l1l1l11_opy_.close()
    logger.info(bstack1l1lll1lll_opy_)
    try:
      os.environ[bstack111l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࠩఏ")] = bstack11l11lll_opy_.framework if bstack11l11lll_opy_.framework != None else bstack111l1_opy_ (u"ࠣࠤఐ")
      config = yaml.safe_load(bstack1ll1l11l_opy_)
      config[bstack111l1_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩ఑")] = bstack111l1_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰ࠰ࡷࡪࡺࡵࡱࠩఒ")
      bstack1lllll11l1_opy_(bstack1ll1l11l1l_opy_, config)
    except Exception as e:
      logger.debug(bstack1l11ll1ll1_opy_.format(str(e)))
  except Exception as e:
    logger.error(bstack1ll1l11ll_opy_.format(str(e)))
def bstack1lllll11l1_opy_(bstack111l1ll1_opy_, config, bstack1l11lllll1_opy_={}):
  global bstack1l1l111l_opy_
  global bstack111l111l1_opy_
  global bstack1111ll1l1_opy_
  if not config:
    return
  bstack11lll1lll_opy_ = bstack1lll111ll_opy_ if not bstack1l1l111l_opy_ else (
    bstack1l111l1l1_opy_ if bstack111l1_opy_ (u"ࠫࡦࡶࡰࠨఓ") in config else bstack1l11111l11_opy_)
  bstack1ll11lll11_opy_ = False
  bstack111111l1l_opy_ = False
  if bstack1l1l111l_opy_ is True:
      if bstack111l1_opy_ (u"ࠬࡧࡰࡱࠩఔ") in config:
          bstack1ll11lll11_opy_ = True
      else:
          bstack111111l1l_opy_ = True
  bstack11111l1ll_opy_ = bstack1llllll1l1_opy_.bstack11llllllll_opy_(config, bstack111l111l1_opy_)
  data = {
    bstack111l1_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨక"): config[bstack111l1_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩఖ")],
    bstack111l1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫగ"): config[bstack111l1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬఘ")],
    bstack111l1_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧఙ"): bstack111l1ll1_opy_,
    bstack111l1_opy_ (u"ࠫࡩ࡫ࡴࡦࡥࡷࡩࡩࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨచ"): os.environ.get(bstack111l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡋࡘࡁࡎࡇ࡚ࡓࡗࡑࠧఛ"), bstack111l111l1_opy_),
    bstack111l1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨజ"): bstack1ll11ll1l1_opy_,
    bstack111l1_opy_ (u"ࠧࡰࡲࡷ࡭ࡲࡧ࡬ࡠࡪࡸࡦࡤࡻࡲ࡭ࠩఝ"): bstack111l1l11l_opy_(),
    bstack111l1_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡱࡴࡲࡴࡪࡸࡴࡪࡧࡶࠫఞ"): {
      bstack111l1_opy_ (u"ࠩ࡯ࡥࡳ࡭ࡵࡢࡩࡨࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧట"): str(config[bstack111l1_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪఠ")]) if bstack111l1_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫడ") in config else bstack111l1_opy_ (u"ࠧࡻ࡮࡬ࡰࡲࡻࡳࠨఢ"),
      bstack111l1_opy_ (u"࠭࡬ࡢࡰࡪࡹࡦ࡭ࡥࡗࡧࡵࡷ࡮ࡵ࡮ࠨణ"): sys.version,
      bstack111l1_opy_ (u"ࠧࡳࡧࡩࡩࡷࡸࡥࡳࠩత"): bstack1l11lll1l1_opy_(os.getenv(bstack111l1_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࠥథ"), bstack111l1_opy_ (u"ࠤࠥద"))),
      bstack111l1_opy_ (u"ࠪࡰࡦࡴࡧࡶࡣࡪࡩࠬధ"): bstack111l1_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫన"),
      bstack111l1_opy_ (u"ࠬࡶࡲࡰࡦࡸࡧࡹ࠭఩"): bstack11lll1lll_opy_,
      bstack111l1_opy_ (u"࠭ࡰࡳࡱࡧࡹࡨࡺ࡟࡮ࡣࡳࠫప"): bstack11111l1ll_opy_,
      bstack111l1_opy_ (u"ࠧࡵࡧࡶࡸ࡭ࡻࡢࡠࡷࡸ࡭ࡩ࠭ఫ"): os.environ[bstack111l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭బ")],
      bstack111l1_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯࡛࡫ࡲࡴ࡫ࡲࡲࠬభ"): bstack1l1ll111ll_opy_(os.environ.get(bstack111l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡉࡖࡆࡓࡅࡘࡑࡕࡏࠬమ"), bstack111l111l1_opy_)),
      bstack111l1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧయ"): config[bstack111l1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨర")] if config[bstack111l1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩఱ")] else bstack111l1_opy_ (u"ࠢࡶࡰ࡮ࡲࡴࡽ࡮ࠣల"),
      bstack111l1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪళ"): str(config[bstack111l1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫఴ")]) if bstack111l1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬవ") in config else bstack111l1_opy_ (u"ࠦࡺࡴ࡫࡯ࡱࡺࡲࠧశ"),
      bstack111l1_opy_ (u"ࠬࡵࡳࠨష"): sys.platform,
      bstack111l1_opy_ (u"࠭ࡨࡰࡵࡷࡲࡦࡳࡥࠨస"): socket.gethostname(),
      bstack111l1_opy_ (u"ࠧࡴࡦ࡮ࡖࡺࡴࡉࡥࠩహ"): bstack1111ll1l1_opy_.get_property(bstack111l1_opy_ (u"ࠨࡵࡧ࡯ࡗࡻ࡮ࡊࡦࠪ఺"))
    }
  }
  if not bstack1111ll1l1_opy_.get_property(bstack111l1_opy_ (u"ࠩࡶࡨࡰࡑࡩ࡭࡮ࡖ࡭࡬ࡴࡡ࡭ࠩ఻")) is None:
    data[bstack111l1_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡳࡶࡴࡶࡥࡳࡶ࡬ࡩࡸ఼࠭")][bstack111l1_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡓࡥࡵࡣࡧࡥࡹࡧࠧఽ")] = {
      bstack111l1_opy_ (u"ࠬࡸࡥࡢࡵࡲࡲࠬా"): bstack111l1_opy_ (u"࠭ࡵࡴࡧࡵࡣࡰ࡯࡬࡭ࡧࡧࠫి"),
      bstack111l1_opy_ (u"ࠧࡴ࡫ࡪࡲࡦࡲࠧీ"): bstack1111ll1l1_opy_.get_property(bstack111l1_opy_ (u"ࠨࡵࡧ࡯ࡐ࡯࡬࡭ࡕ࡬࡫ࡳࡧ࡬ࠨు")),
      bstack111l1_opy_ (u"ࠩࡶ࡭࡬ࡴࡡ࡭ࡐࡸࡱࡧ࡫ࡲࠨూ"): bstack1111ll1l1_opy_.get_property(bstack111l1_opy_ (u"ࠪࡷࡩࡱࡋࡪ࡮࡯ࡒࡴ࠭ృ"))
    }
  if bstack111l1ll1_opy_ == bstack1ll11l11l1_opy_:
    data[bstack111l1_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡴࡷࡵࡰࡦࡴࡷ࡭ࡪࡹࠧౄ")][bstack111l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡇࡴࡴࡦࡪࡩࠪ౅")] = bstack1111lll11_opy_(config)
    data[bstack111l1_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡶࡲࡰࡲࡨࡶࡹ࡯ࡥࡴࠩె")][bstack111l1_opy_ (u"ࠧࡪࡵࡓࡩࡷࡩࡹࡂࡷࡷࡳࡊࡴࡡࡣ࡮ࡨࡨࠬే")] = percy.bstack111ll1l1l_opy_
    data[bstack111l1_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡱࡴࡲࡴࡪࡸࡴࡪࡧࡶࠫై")][bstack111l1_opy_ (u"ࠩࡳࡩࡷࡩࡹࡃࡷ࡬ࡰࡩࡏࡤࠨ౉")] = percy.bstack11l1111ll_opy_
  update(data[bstack111l1_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡳࡶࡴࡶࡥࡳࡶ࡬ࡩࡸ࠭ొ")], bstack1l11lllll1_opy_)
  try:
    response = bstack1ll1l11111_opy_(bstack111l1_opy_ (u"ࠫࡕࡕࡓࡕࠩో"), bstack1lll1l1ll_opy_(bstack111lll11_opy_), data, {
      bstack111l1_opy_ (u"ࠬࡧࡵࡵࡪࠪౌ"): (config[bstack111l1_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨ్")], config[bstack111l1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪ౎")])
    })
    if response:
      logger.debug(bstack1ll1l1l1ll_opy_.format(bstack111l1ll1_opy_, str(response.json())))
  except Exception as e:
    logger.debug(bstack1ll1111l_opy_.format(str(e)))
def bstack1l11lll1l1_opy_(framework):
  return bstack111l1_opy_ (u"ࠣࡽࢀ࠱ࡵࡿࡴࡩࡱࡱࡥ࡬࡫࡮ࡵ࠱ࡾࢁࠧ౏").format(str(framework), __version__) if framework else bstack111l1_opy_ (u"ࠤࡳࡽࡹ࡮࡯࡯ࡣࡪࡩࡳࡺ࠯ࡼࡿࠥ౐").format(
    __version__)
def bstack1lllll11_opy_():
  global CONFIG
  global bstack1llllll1l_opy_
  if bool(CONFIG):
    return
  try:
    bstack11lllllll_opy_()
    logger.debug(bstack1ll1lll111_opy_.format(str(CONFIG)))
    bstack1llllll1l_opy_ = bstack1l1ll1111_opy_.bstack1l11ll11ll_opy_(CONFIG, bstack1llllll1l_opy_)
    bstack1lll1ll1_opy_()
  except Exception as e:
    logger.error(bstack111l1_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡶࡸࡴ࠱ࠦࡥࡳࡴࡲࡶ࠿ࠦࠢ౑") + str(e))
    sys.exit(1)
  sys.excepthook = bstack1l1ll1ll1_opy_
  atexit.register(bstack1l1llll1_opy_)
  signal.signal(signal.SIGINT, bstack1l111lll_opy_)
  signal.signal(signal.SIGTERM, bstack1l111lll_opy_)
def bstack1l1ll1ll1_opy_(exctype, value, traceback):
  global bstack1l1ll1l1l_opy_
  try:
    for driver in bstack1l1ll1l1l_opy_:
      bstack1lll1111l1_opy_(driver, bstack111l1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ౒"), bstack111l1_opy_ (u"࡙ࠧࡥࡴࡵ࡬ࡳࡳࠦࡦࡢ࡫࡯ࡩࡩࠦࡷࡪࡶ࡫࠾ࠥࡢ࡮ࠣ౓") + str(value))
  except Exception:
    pass
  bstack1l1l11ll11_opy_(value, True)
  sys.__excepthook__(exctype, value, traceback)
  sys.exit(1)
def bstack1l1l11ll11_opy_(message=bstack111l1_opy_ (u"࠭ࠧ౔"), bstack1ll1ll1l11_opy_ = False):
  global CONFIG
  bstack1l11111ll1_opy_ = bstack111l1_opy_ (u"ࠧࡨ࡮ࡲࡦࡦࡲࡅࡹࡥࡨࡴࡹ࡯࡯࡯ౕࠩ") if bstack1ll1ll1l11_opy_ else bstack111l1_opy_ (u"ࠨࡧࡵࡶࡴࡸౖࠧ")
  try:
    if message:
      bstack1l11lllll1_opy_ = {
        bstack1l11111ll1_opy_ : str(message)
      }
      bstack1lllll11l1_opy_(bstack1ll11l11l1_opy_, CONFIG, bstack1l11lllll1_opy_)
    else:
      bstack1lllll11l1_opy_(bstack1ll11l11l1_opy_, CONFIG)
  except Exception as e:
    logger.debug(bstack1lll11ll1_opy_.format(str(e)))
def bstack1l1ll1ll1l_opy_(bstack1lll1l11l_opy_, size):
  bstack1l1l1l11l1_opy_ = []
  while len(bstack1lll1l11l_opy_) > size:
    bstack1l1lll111l_opy_ = bstack1lll1l11l_opy_[:size]
    bstack1l1l1l11l1_opy_.append(bstack1l1lll111l_opy_)
    bstack1lll1l11l_opy_ = bstack1lll1l11l_opy_[size:]
  bstack1l1l1l11l1_opy_.append(bstack1lll1l11l_opy_)
  return bstack1l1l1l11l1_opy_
def bstack1l11lll1ll_opy_(args):
  if bstack111l1_opy_ (u"ࠩ࠰ࡱࠬ౗") in args and bstack111l1_opy_ (u"ࠪࡴࡩࡨࠧౘ") in args:
    return True
  return False
def run_on_browserstack(bstack11l1ll1ll_opy_=None, bstack1ll111l111_opy_=None, bstack1111l1l1l_opy_=False):
  global CONFIG
  global bstack11l1l111l_opy_
  global bstack1l111ll111_opy_
  global bstack111l111l1_opy_
  global bstack1111ll1l1_opy_
  bstack1l111l1l1l_opy_ = bstack111l1_opy_ (u"ࠫࠬౙ")
  bstack1ll11l1l1_opy_(bstack1l1l1ll111_opy_, logger)
  if bstack11l1ll1ll_opy_ and isinstance(bstack11l1ll1ll_opy_, str):
    bstack11l1ll1ll_opy_ = eval(bstack11l1ll1ll_opy_)
  if bstack11l1ll1ll_opy_:
    CONFIG = bstack11l1ll1ll_opy_[bstack111l1_opy_ (u"ࠬࡉࡏࡏࡈࡌࡋࠬౚ")]
    bstack11l1l111l_opy_ = bstack11l1ll1ll_opy_[bstack111l1_opy_ (u"࠭ࡈࡖࡄࡢ࡙ࡗࡒࠧ౛")]
    bstack1l111ll111_opy_ = bstack11l1ll1ll_opy_[bstack111l1_opy_ (u"ࠧࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩ౜")]
    bstack1111ll1l1_opy_.bstack1lll11lll_opy_(bstack111l1_opy_ (u"ࠨࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇࠪౝ"), bstack1l111ll111_opy_)
    bstack1l111l1l1l_opy_ = bstack111l1_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩ౞")
  bstack1111ll1l1_opy_.bstack1lll11lll_opy_(bstack111l1_opy_ (u"ࠪࡷࡩࡱࡒࡶࡰࡌࡨࠬ౟"), uuid4().__str__())
  logger.debug(bstack111l1_opy_ (u"ࠫࡸࡪ࡫ࡓࡷࡱࡍࡩࡃࠧౠ") + bstack1111ll1l1_opy_.get_property(bstack111l1_opy_ (u"ࠬࡹࡤ࡬ࡔࡸࡲࡎࡪࠧౡ")))
  if not bstack1111l1l1l_opy_:
    if len(sys.argv) <= 1:
      logger.critical(bstack1l1lll1ll1_opy_)
      return
    if sys.argv[1] == bstack111l1_opy_ (u"࠭࠭࠮ࡸࡨࡶࡸ࡯࡯࡯ࠩౢ") or sys.argv[1] == bstack111l1_opy_ (u"ࠧ࠮ࡸࠪౣ"):
      logger.info(bstack111l1_opy_ (u"ࠨࡄࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡑࡻࡷ࡬ࡴࡴࠠࡔࡆࡎࠤࡻࢁࡽࠨ౤").format(__version__))
      return
    if sys.argv[1] == bstack111l1_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨ౥"):
      bstack11llllll_opy_()
      return
  args = sys.argv
  bstack1lllll11_opy_()
  global bstack11lll1111_opy_
  global bstack1ll111l11l_opy_
  global bstack1ll11l1l_opy_
  global bstack1l1l1l1l1_opy_
  global bstack1l11llll1l_opy_
  global bstack1111l1ll1_opy_
  global bstack111l111ll_opy_
  global bstack1ll11111l1_opy_
  global bstack1l11111l1_opy_
  global bstack1l1l11l11l_opy_
  global bstack1l111l1111_opy_
  bstack1ll111l11l_opy_ = len(CONFIG.get(bstack111l1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭౦"), []))
  if not bstack1l111l1l1l_opy_:
    if args[1] == bstack111l1_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫ౧") or args[1] == bstack111l1_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲ࠸࠭౨"):
      bstack1l111l1l1l_opy_ = bstack111l1_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭౩")
      args = args[2:]
    elif args[1] == bstack111l1_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭౪"):
      bstack1l111l1l1l_opy_ = bstack111l1_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧ౫")
      args = args[2:]
    elif args[1] == bstack111l1_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨ౬"):
      bstack1l111l1l1l_opy_ = bstack111l1_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩ౭")
      args = args[2:]
    elif args[1] == bstack111l1_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬ౮"):
      bstack1l111l1l1l_opy_ = bstack111l1_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱ࠭౯")
      args = args[2:]
    elif args[1] == bstack111l1_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭౰"):
      bstack1l111l1l1l_opy_ = bstack111l1_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ౱")
      args = args[2:]
    elif args[1] == bstack111l1_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨ౲"):
      bstack1l111l1l1l_opy_ = bstack111l1_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩ౳")
      args = args[2:]
    else:
      if not bstack111l1_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭౴") in CONFIG or str(CONFIG[bstack111l1_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧ౵")]).lower() in [bstack111l1_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬ౶"), bstack111l1_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠹ࠧ౷")]:
        bstack1l111l1l1l_opy_ = bstack111l1_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧ౸")
        args = args[1:]
      elif str(CONFIG[bstack111l1_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫ౹")]).lower() == bstack111l1_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ౺"):
        bstack1l111l1l1l_opy_ = bstack111l1_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩ౻")
        args = args[1:]
      elif str(CONFIG[bstack111l1_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧ౼")]).lower() == bstack111l1_opy_ (u"ࠬࡶࡡࡣࡱࡷࠫ౽"):
        bstack1l111l1l1l_opy_ = bstack111l1_opy_ (u"࠭ࡰࡢࡤࡲࡸࠬ౾")
        args = args[1:]
      elif str(CONFIG[bstack111l1_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪ౿")]).lower() == bstack111l1_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨಀ"):
        bstack1l111l1l1l_opy_ = bstack111l1_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩಁ")
        args = args[1:]
      elif str(CONFIG[bstack111l1_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ಂ")]).lower() == bstack111l1_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫಃ"):
        bstack1l111l1l1l_opy_ = bstack111l1_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬ಄")
        args = args[1:]
      else:
        os.environ[bstack111l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࠨಅ")] = bstack1l111l1l1l_opy_
        bstack11l1ll11_opy_(bstack1111llll_opy_)
  os.environ[bstack111l1_opy_ (u"ࠧࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࡢ࡙ࡘࡋࡄࠨಆ")] = bstack1l111l1l1l_opy_
  bstack111l111l1_opy_ = bstack1l111l1l1l_opy_
  global bstack1ll1ll1lll_opy_
  global bstack11ll1lll_opy_
  if bstack11l1ll1ll_opy_:
    try:
      os.environ[bstack111l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࠪಇ")] = bstack1l111l1l1l_opy_
      bstack1lllll11l1_opy_(bstack1l1l1llll_opy_, CONFIG)
    except Exception as e:
      logger.debug(bstack111111l1_opy_.format(str(e)))
  global bstack1llll1lll1_opy_
  global bstack1lll1l1l1l_opy_
  global bstack1l1l11111_opy_
  global bstack1lllllll1l_opy_
  global bstack1111l1l1_opy_
  global bstack1l1lll1l1l_opy_
  global bstack1l1lll1l1_opy_
  global bstack1l111lll1l_opy_
  global bstack11l1l1lll_opy_
  global bstack1ll11ll1_opy_
  global bstack1l1l1ll11_opy_
  global bstack1ll1ll1l_opy_
  global bstack1l111l111l_opy_
  global bstack1l111l1lll_opy_
  global bstack1l1lll1l11_opy_
  global bstack1l11l11ll1_opy_
  global bstack1l111l11l_opy_
  global bstack1l1l111l11_opy_
  global bstack1l1l1l111_opy_
  global bstack1l111111l_opy_
  global bstack1l1l1l1111_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack1llll1lll1_opy_ = webdriver.Remote.__init__
    bstack1lll1l1l1l_opy_ = WebDriver.quit
    bstack1ll1ll1l_opy_ = WebDriver.close
    bstack1l1lll1l11_opy_ = WebDriver.get
    bstack1l1l1l1111_opy_ = WebDriver.execute
  except Exception as e:
    pass
  try:
    import Browser
    from subprocess import Popen
    bstack1ll1ll1lll_opy_ = Popen.__init__
  except Exception as e:
    pass
  try:
    from bstack_utils.helper import bstack11lll111l_opy_
    bstack11ll1lll_opy_ = bstack11lll111l_opy_()
  except Exception as e:
    pass
  try:
    global bstack1l1l1lll_opy_
    from QWeb.keywords import browser
    bstack1l1l1lll_opy_ = browser.close_browser
  except Exception as e:
    pass
  if bstack111lll1l_opy_(CONFIG) and bstack1l1llll1ll_opy_():
    if bstack1l1l11l1ll_opy_() < version.parse(bstack1l11ll1l1_opy_):
      logger.error(bstack1l11l1ll1_opy_.format(bstack1l1l11l1ll_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        bstack1l11l11ll1_opy_ = RemoteConnection._get_proxy_url
      except Exception as e:
        logger.error(bstack1ll1111lll_opy_.format(str(e)))
  if not CONFIG.get(bstack111l1_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧࡄࡹࡹࡵࡃࡢࡲࡷࡹࡷ࡫ࡌࡰࡩࡶࠫಈ"), False) and not bstack11l1ll1ll_opy_:
    logger.info(bstack1l1l1l11l_opy_)
  if bstack1l111l1l1l_opy_ != bstack111l1_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪಉ") or (bstack1l111l1l1l_opy_ == bstack111l1_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫಊ") and not bstack11l1ll1ll_opy_):
    bstack1ll11llll_opy_()
  if (bstack1l111l1l1l_opy_ in [bstack111l1_opy_ (u"ࠬࡶࡡࡣࡱࡷࠫಋ"), bstack111l1_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬಌ"), bstack111l1_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠳ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠨ಍")]):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCreator._get_ff_profile = bstack1ll1l1l11l_opy_
        bstack1l1lll1l1l_opy_ = WebDriverCache.close
      except Exception as e:
        logger.warn(bstack11lll11l1_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import ApplicationCache
        bstack1111l1l1_opy_ = ApplicationCache.close
      except Exception as e:
        logger.debug(bstack1l1l11ll_opy_ + str(e))
    except Exception as e:
      bstack1ll11l11l_opy_(e, bstack11lll11l1_opy_)
    if bstack1l111l1l1l_opy_ != bstack111l1_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠩಎ"):
      bstack1l11l1l11_opy_()
    bstack1l1l11111_opy_ = Output.start_test
    bstack1lllllll1l_opy_ = Output.end_test
    bstack1l1lll1l1_opy_ = TestStatus.__init__
    bstack11l1l1lll_opy_ = pabot._run
    bstack1ll11ll1_opy_ = QueueItem.__init__
    bstack1l1l1ll11_opy_ = pabot._create_command_for_execution
    bstack1l1l1l111_opy_ = pabot._report_results
  if bstack1l111l1l1l_opy_ == bstack111l1_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩಏ"):
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1ll11l11l_opy_(e, bstack1ll1l1l1l_opy_)
    bstack1l111l111l_opy_ = Runner.run_hook
    bstack1l111l1lll_opy_ = Step.run
  if bstack1l111l1l1l_opy_ == bstack111l1_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪಐ"):
    try:
      from _pytest.config import Config
      bstack1l111l11l_opy_ = Config.getoption
      from _pytest import runner
      bstack1l1l111l11_opy_ = runner._update_current_test_var
    except Exception as e:
      logger.warn(e, bstack1llll1l11l_opy_)
    try:
      from pytest_bdd import reporting
      bstack1l111111l_opy_ = reporting.runtest_makereport
    except Exception as e:
      logger.debug(bstack111l1_opy_ (u"ࠫࡕࡲࡥࡢࡵࡨࠤ࡮ࡴࡳࡵࡣ࡯ࡰࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡷࡳࠥࡸࡵ࡯ࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡴࡦࡵࡷࡷࠬ಑"))
  try:
    framework_name = bstack111l1_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫಒ") if bstack1l111l1l1l_opy_ in [bstack111l1_opy_ (u"࠭ࡰࡢࡤࡲࡸࠬಓ"), bstack111l1_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ಔ"), bstack111l1_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠩಕ")] else bstack1lll111l1l_opy_(bstack1l111l1l1l_opy_)
    bstack111lllll_opy_ = {
      bstack111l1_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࠪಖ"): bstack111l1_opy_ (u"ࠪࡿ࠵ࢃ࠭ࡤࡷࡦࡹࡲࡨࡥࡳࠩಗ").format(framework_name) if bstack1l111l1l1l_opy_ == bstack111l1_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫಘ") and bstack1ll1l1ll_opy_() else framework_name,
      bstack111l1_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩಙ"): bstack1l1ll111ll_opy_(framework_name),
      bstack111l1_opy_ (u"࠭ࡳࡥ࡭ࡢࡺࡪࡸࡳࡪࡱࡱࠫಚ"): __version__,
      bstack111l1_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡹࡸ࡫ࡤࠨಛ"): bstack1l111l1l1l_opy_
    }
    if bstack1l111l1l1l_opy_ in bstack1l11ll11l_opy_:
      if bstack1l1l111l_opy_ and bstack111l1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨಜ") in CONFIG and CONFIG[bstack111l1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩಝ")] == True:
        if bstack111l1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪಞ") in CONFIG:
          os.environ[bstack111l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬಟ")] = os.getenv(bstack111l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭ಠ"), json.dumps(CONFIG[bstack111l1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ಡ")]))
          CONFIG[bstack111l1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧಢ")].pop(bstack111l1_opy_ (u"ࠨ࡫ࡱࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭ಣ"), None)
          CONFIG[bstack111l1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩತ")].pop(bstack111l1_opy_ (u"ࠪࡩࡽࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨಥ"), None)
        bstack111lllll_opy_[bstack111l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫದ")] = {
          bstack111l1_opy_ (u"ࠬࡴࡡ࡮ࡧࠪಧ"): bstack111l1_opy_ (u"࠭ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠨನ"),
          bstack111l1_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࠨ಩"): str(bstack1l1l11l1ll_opy_())
        }
    if bstack1l111l1l1l_opy_ not in [bstack111l1_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠩಪ")]:
      bstack111l111l_opy_ = bstack11llllll11_opy_.launch(CONFIG, bstack111lllll_opy_)
  except Exception as e:
    logger.debug(bstack1111l1ll_opy_.format(bstack111l1_opy_ (u"ࠩࡗࡩࡸࡺࡈࡶࡤࠪಫ"), str(e)))
  if bstack1l111l1l1l_opy_ == bstack111l1_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪಬ"):
    bstack1ll11l1l_opy_ = True
    if bstack11l1ll1ll_opy_ and bstack1111l1l1l_opy_:
      bstack1111l1ll1_opy_ = CONFIG.get(bstack111l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨಭ"), {}).get(bstack111l1_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧಮ"))
      bstack111l1111_opy_(bstack1l11111l_opy_)
    elif bstack11l1ll1ll_opy_:
      bstack1111l1ll1_opy_ = CONFIG.get(bstack111l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪಯ"), {}).get(bstack111l1_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩರ"))
      global bstack1l1ll1l1l_opy_
      try:
        if bstack1l11lll1ll_opy_(bstack11l1ll1ll_opy_[bstack111l1_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫಱ")]) and multiprocessing.current_process().name == bstack111l1_opy_ (u"ࠩ࠳ࠫಲ"):
          bstack11l1ll1ll_opy_[bstack111l1_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ಳ")].remove(bstack111l1_opy_ (u"ࠫ࠲ࡳࠧ಴"))
          bstack11l1ll1ll_opy_[bstack111l1_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨವ")].remove(bstack111l1_opy_ (u"࠭ࡰࡥࡤࠪಶ"))
          bstack11l1ll1ll_opy_[bstack111l1_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪಷ")] = bstack11l1ll1ll_opy_[bstack111l1_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫಸ")][0]
          with open(bstack11l1ll1ll_opy_[bstack111l1_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬಹ")], bstack111l1_opy_ (u"ࠪࡶࠬ಺")) as f:
            bstack1l11l11lll_opy_ = f.read()
          bstack11111l1l1_opy_ = bstack111l1_opy_ (u"ࠦࠧࠨࡦࡳࡱࡰࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡷࡩࡱࠠࡪ࡯ࡳࡳࡷࡺࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡩ࡯࡫ࡷ࡭ࡦࡲࡩࡻࡧ࠾ࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢ࡭ࡳ࡯ࡴࡪࡣ࡯࡭ࡿ࡫ࠨࡼࡿࠬ࠿ࠥ࡬ࡲࡰ࡯ࠣࡴࡩࡨࠠࡪ࡯ࡳࡳࡷࡺࠠࡑࡦࡥ࠿ࠥࡵࡧࡠࡦࡥࠤࡂࠦࡐࡥࡤ࠱ࡨࡴࡥࡢࡳࡧࡤ࡯ࡀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡧࡩ࡫ࠦ࡭ࡰࡦࡢࡦࡷ࡫ࡡ࡬ࠪࡶࡩࡱ࡬ࠬࠡࡣࡵ࡫࠱ࠦࡴࡦ࡯ࡳࡳࡷࡧࡲࡺࠢࡀࠤ࠵࠯࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡴࡳࡻ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡦࡸࡧࠡ࠿ࠣࡷࡹࡸࠨࡪࡰࡷࠬࡦࡸࡧࠪ࠭࠴࠴࠮ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡪࡾࡣࡦࡲࡷࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡢࡵࠣࡩ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡰࡢࡵࡶࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡲ࡫ࡤࡪࡢࠩࡵࡨࡰ࡫࠲ࡡࡳࡩ࠯ࡸࡪࡳࡰࡰࡴࡤࡶࡾ࠯ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡔࡩࡨ࠮ࡥࡱࡢࡦࠥࡃࠠ࡮ࡱࡧࡣࡧࡸࡥࡢ࡭ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡐࡥࡤ࠱ࡨࡴࡥࡢࡳࡧࡤ࡯ࠥࡃࠠ࡮ࡱࡧࡣࡧࡸࡥࡢ࡭ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡐࡥࡤࠫ࠭࠳ࡹࡥࡵࡡࡷࡶࡦࡩࡥࠩࠫ࡟ࡲࠧࠨࠢ಻").format(str(bstack11l1ll1ll_opy_))
          bstack1ll11lll1l_opy_ = bstack11111l1l1_opy_ + bstack1l11l11lll_opy_
          bstack1ll1l1ll11_opy_ = bstack11l1ll1ll_opy_[bstack111l1_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨ಼")] + bstack111l1_opy_ (u"࠭࡟ࡣࡵࡷࡥࡨࡱ࡟ࡵࡧࡰࡴ࠳ࡶࡹࠨಽ")
          with open(bstack1ll1l1ll11_opy_, bstack111l1_opy_ (u"ࠧࡸࠩಾ")):
            pass
          with open(bstack1ll1l1ll11_opy_, bstack111l1_opy_ (u"ࠣࡹ࠮ࠦಿ")) as f:
            f.write(bstack1ll11lll1l_opy_)
          import subprocess
          bstack11l11l11_opy_ = subprocess.run([bstack111l1_opy_ (u"ࠤࡳࡽࡹ࡮࡯࡯ࠤೀ"), bstack1ll1l1ll11_opy_])
          if os.path.exists(bstack1ll1l1ll11_opy_):
            os.unlink(bstack1ll1l1ll11_opy_)
          os._exit(bstack11l11l11_opy_.returncode)
        else:
          if bstack1l11lll1ll_opy_(bstack11l1ll1ll_opy_[bstack111l1_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ು")]):
            bstack11l1ll1ll_opy_[bstack111l1_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧೂ")].remove(bstack111l1_opy_ (u"ࠬ࠳࡭ࠨೃ"))
            bstack11l1ll1ll_opy_[bstack111l1_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩೄ")].remove(bstack111l1_opy_ (u"ࠧࡱࡦࡥࠫ೅"))
            bstack11l1ll1ll_opy_[bstack111l1_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫೆ")] = bstack11l1ll1ll_opy_[bstack111l1_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬೇ")][0]
          bstack111l1111_opy_(bstack1l11111l_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(bstack11l1ll1ll_opy_[bstack111l1_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ೈ")])))
          sys.argv = sys.argv[2:]
          mod_globals = globals()
          mod_globals[bstack111l1_opy_ (u"ࠫࡤࡥ࡮ࡢ࡯ࡨࡣࡤ࠭೉")] = bstack111l1_opy_ (u"ࠬࡥ࡟࡮ࡣ࡬ࡲࡤࡥࠧೊ")
          mod_globals[bstack111l1_opy_ (u"࠭࡟ࡠࡨ࡬ࡰࡪࡥ࡟ࠨೋ")] = os.path.abspath(bstack11l1ll1ll_opy_[bstack111l1_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪೌ")])
          exec(open(bstack11l1ll1ll_opy_[bstack111l1_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨ್ࠫ")]).read(), mod_globals)
      except BaseException as e:
        try:
          traceback.print_exc()
          logger.error(bstack111l1_opy_ (u"ࠩࡆࡥࡺ࡭ࡨࡵࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲ࠿ࠦࡻࡾࠩ೎").format(str(e)))
          for driver in bstack1l1ll1l1l_opy_:
            bstack1ll111l111_opy_.append({
              bstack111l1_opy_ (u"ࠪࡲࡦࡳࡥࠨ೏"): bstack11l1ll1ll_opy_[bstack111l1_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧ೐")],
              bstack111l1_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫ೑"): str(e),
              bstack111l1_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬ೒"): multiprocessing.current_process().name
            })
            bstack1lll1111l1_opy_(driver, bstack111l1_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ೓"), bstack111l1_opy_ (u"ࠣࡕࡨࡷࡸ࡯࡯࡯ࠢࡩࡥ࡮ࡲࡥࡥࠢࡺ࡭ࡹ࡮࠺ࠡ࡞ࡱࠦ೔") + str(e))
        except Exception:
          pass
      finally:
        try:
          for driver in bstack1l1ll1l1l_opy_:
            driver.quit()
        except Exception as e:
          pass
    else:
      percy.init(bstack1l111ll111_opy_, CONFIG, logger)
      bstack1111ll11l_opy_()
      bstack11ll1l1ll_opy_()
      bstack1l11l1ll11_opy_ = {
        bstack111l1_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬೕ"): args[0],
        bstack111l1_opy_ (u"ࠪࡇࡔࡔࡆࡊࡉࠪೖ"): CONFIG,
        bstack111l1_opy_ (u"ࠫࡍ࡛ࡂࡠࡗࡕࡐࠬ೗"): bstack11l1l111l_opy_,
        bstack111l1_opy_ (u"ࠬࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧ೘"): bstack1l111ll111_opy_
      }
      percy.bstack1ll1l1l1l1_opy_()
      if bstack111l1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ೙") in CONFIG:
        bstack11ll11l11_opy_ = []
        manager = multiprocessing.Manager()
        bstack1ll111l11_opy_ = manager.list()
        if bstack1l11lll1ll_opy_(args):
          for index, platform in enumerate(CONFIG[bstack111l1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ೚")]):
            if index == 0:
              bstack1l11l1ll11_opy_[bstack111l1_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫ೛")] = args
            bstack11ll11l11_opy_.append(multiprocessing.Process(name=str(index),
                                                       target=run_on_browserstack,
                                                       args=(bstack1l11l1ll11_opy_, bstack1ll111l11_opy_)))
        else:
          for index, platform in enumerate(CONFIG[bstack111l1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ೜")]):
            bstack11ll11l11_opy_.append(multiprocessing.Process(name=str(index),
                                                       target=run_on_browserstack,
                                                       args=(bstack1l11l1ll11_opy_, bstack1ll111l11_opy_)))
        for t in bstack11ll11l11_opy_:
          t.start()
        for t in bstack11ll11l11_opy_:
          t.join()
        bstack1ll11111l1_opy_ = list(bstack1ll111l11_opy_)
      else:
        if bstack1l11lll1ll_opy_(args):
          bstack1l11l1ll11_opy_[bstack111l1_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ೝ")] = args
          test = multiprocessing.Process(name=str(0),
                                         target=run_on_browserstack, args=(bstack1l11l1ll11_opy_,))
          test.start()
          test.join()
        else:
          bstack111l1111_opy_(bstack1l11111l_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(args[0])))
          mod_globals = globals()
          mod_globals[bstack111l1_opy_ (u"ࠫࡤࡥ࡮ࡢ࡯ࡨࡣࡤ࠭ೞ")] = bstack111l1_opy_ (u"ࠬࡥ࡟࡮ࡣ࡬ࡲࡤࡥࠧ೟")
          mod_globals[bstack111l1_opy_ (u"࠭࡟ࡠࡨ࡬ࡰࡪࡥ࡟ࠨೠ")] = os.path.abspath(args[0])
          sys.argv = sys.argv[2:]
          exec(open(args[0]).read(), mod_globals)
  elif bstack1l111l1l1l_opy_ == bstack111l1_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭ೡ") or bstack1l111l1l1l_opy_ == bstack111l1_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧೢ"):
    percy.init(bstack1l111ll111_opy_, CONFIG, logger)
    percy.bstack1ll1l1l1l1_opy_()
    try:
      from pabot import pabot
    except Exception as e:
      bstack1ll11l11l_opy_(e, bstack11lll11l1_opy_)
    bstack1111ll11l_opy_()
    bstack111l1111_opy_(bstack1111ll1ll_opy_)
    if bstack1l1l111l_opy_:
      bstack111l1l1l_opy_(bstack1111ll1ll_opy_, args)
      if bstack111l1_opy_ (u"ࠩ࠰࠱ࡵࡸ࡯ࡤࡧࡶࡷࡪࡹࠧೣ") in args:
        i = args.index(bstack111l1_opy_ (u"ࠪ࠱࠲ࡶࡲࡰࡥࡨࡷࡸ࡫ࡳࠨ೤"))
        args.pop(i)
        args.pop(i)
      if bstack111l1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ೥") not in CONFIG:
        CONFIG[bstack111l1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ೦")] = [{}]
        bstack1ll111l11l_opy_ = 1
      if bstack11lll1111_opy_ == 0:
        bstack11lll1111_opy_ = 1
      args.insert(0, str(bstack11lll1111_opy_))
      args.insert(0, str(bstack111l1_opy_ (u"࠭࠭࠮ࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠫ೧")))
    if bstack11llllll11_opy_.on():
      try:
        from robot.run import USAGE
        from robot.utils import ArgumentParser
        from pabot.arguments import _parse_pabot_args
        bstack1lll1lllll_opy_, pabot_args = _parse_pabot_args(args)
        opts, bstack1llll1l1ll_opy_ = ArgumentParser(
            USAGE,
            auto_pythonpath=False,
            auto_argumentfile=True,
            env_options=bstack111l1_opy_ (u"ࠢࡓࡑࡅࡓ࡙ࡥࡏࡑࡖࡌࡓࡓ࡙ࠢ೨"),
        ).parse_args(bstack1lll1lllll_opy_)
        bstack1111lll1_opy_ = args.index(bstack1lll1lllll_opy_[0]) if len(bstack1lll1lllll_opy_) > 0 else len(args)
        args.insert(bstack1111lll1_opy_, str(bstack111l1_opy_ (u"ࠨ࠯࠰ࡰ࡮ࡹࡴࡦࡰࡨࡶࠬ೩")))
        args.insert(bstack1111lll1_opy_ + 1, str(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack111l1_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡵࡳࡧࡵࡴࡠ࡮࡬ࡷࡹ࡫࡮ࡦࡴ࠱ࡴࡾ࠭೪"))))
        if bstack1ll11llll1_opy_(os.environ.get(bstack111l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡕࡉࡗ࡛ࡎࠨ೫"))) and str(os.environ.get(bstack111l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡖࡊࡘࡕࡏࡡࡗࡉࡘ࡚ࡓࠨ೬"), bstack111l1_opy_ (u"ࠬࡴࡵ࡭࡮ࠪ೭"))) != bstack111l1_opy_ (u"࠭࡮ࡶ࡮࡯ࠫ೮"):
          for bstack11l11ll1l_opy_ in bstack1llll1l1ll_opy_:
            args.remove(bstack11l11ll1l_opy_)
          bstack1l11ll1lll_opy_ = os.environ.get(bstack111l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡒࡆࡔࡘࡒࡤ࡚ࡅࡔࡖࡖࠫ೯")).split(bstack111l1_opy_ (u"ࠨ࠮ࠪ೰"))
          for bstack1l1l1l1ll1_opy_ in bstack1l11ll1lll_opy_:
            args.append(bstack1l1l1l1ll1_opy_)
      except Exception as e:
        logger.error(bstack111l1_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡢࡶࡷࡥࡨ࡮ࡩ࡯ࡩࠣࡰ࡮ࡹࡴࡦࡰࡨࡶࠥ࡬࡯ࡳࠢࡒࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺ࠰ࠣࡉࡷࡸ࡯ࡳࠢ࠰ࠤࠧೱ").format(e))
    pabot.main(args)
  elif bstack1l111l1l1l_opy_ == bstack111l1_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫೲ"):
    try:
      from robot import run_cli
    except Exception as e:
      bstack1ll11l11l_opy_(e, bstack11lll11l1_opy_)
    for a in args:
      if bstack111l1_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡔࡑࡇࡔࡇࡑࡕࡑࡎࡔࡄࡆ࡚ࠪೳ") in a:
        bstack1l11llll1l_opy_ = int(a.split(bstack111l1_opy_ (u"ࠬࡀࠧ೴"))[1])
      if bstack111l1_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡊࡅࡇࡎࡒࡇࡆࡒࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔࠪ೵") in a:
        bstack1111l1ll1_opy_ = str(a.split(bstack111l1_opy_ (u"ࠧ࠻ࠩ೶"))[1])
      if bstack111l1_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡄࡎࡌࡅࡗࡍࡓࠨ೷") in a:
        bstack111l111ll_opy_ = str(a.split(bstack111l1_opy_ (u"ࠩ࠽ࠫ೸"))[1])
    bstack111ll111_opy_ = None
    if bstack111l1_opy_ (u"ࠪ࠱࠲ࡨࡳࡵࡣࡦ࡯ࡤ࡯ࡴࡦ࡯ࡢ࡭ࡳࡪࡥࡹࠩ೹") in args:
      i = args.index(bstack111l1_opy_ (u"ࠫ࠲࠳ࡢࡴࡶࡤࡧࡰࡥࡩࡵࡧࡰࡣ࡮ࡴࡤࡦࡺࠪ೺"))
      args.pop(i)
      bstack111ll111_opy_ = args.pop(i)
    if bstack111ll111_opy_ is not None:
      global bstack1ll111lll_opy_
      bstack1ll111lll_opy_ = bstack111ll111_opy_
    bstack111l1111_opy_(bstack1111ll1ll_opy_)
    run_cli(args)
    if bstack111l1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵࠩ೻") in multiprocessing.current_process().__dict__.keys():
      for bstack1ll111lll1_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack1ll111l111_opy_.append(bstack1ll111lll1_opy_)
  elif bstack1l111l1l1l_opy_ == bstack111l1_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭೼"):
    percy.init(bstack1l111ll111_opy_, CONFIG, logger)
    percy.bstack1ll1l1l1l1_opy_()
    bstack1llll111_opy_ = bstack1l1lllllll_opy_(args, logger, CONFIG, bstack1l1l111l_opy_)
    bstack1llll111_opy_.bstack1llll11ll_opy_()
    bstack1111ll11l_opy_()
    bstack1l1l1l1l1_opy_ = True
    bstack1l1l11l11l_opy_ = bstack1llll111_opy_.bstack1ll1l111l_opy_()
    bstack1llll111_opy_.bstack1l11l1ll11_opy_(bstack1l1l1l1l_opy_)
    bstack1ll11ll1l_opy_ = bstack1llll111_opy_.bstack1llll1ll_opy_(bstack1ll11lll_opy_, {
      bstack111l1_opy_ (u"ࠧࡉࡗࡅࡣ࡚ࡘࡌࠨ೽"): bstack11l1l111l_opy_,
      bstack111l1_opy_ (u"ࠨࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇࠪ೾"): bstack1l111ll111_opy_,
      bstack111l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡘࡘࡔࡓࡁࡕࡋࡒࡒࠬ೿"): bstack1l1l111l_opy_
    })
    try:
      bstack1l11l1111_opy_, bstack1ll11111l_opy_ = map(list, zip(*bstack1ll11ll1l_opy_))
      bstack1l11111l1_opy_ = bstack1l11l1111_opy_[0]
      for status_code in bstack1ll11111l_opy_:
        if status_code != 0:
          bstack1l111l1111_opy_ = status_code
          break
    except Exception as e:
      logger.debug(bstack111l1_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡢࡸࡨࠤࡪࡸࡲࡰࡴࡶࠤࡦࡴࡤࠡࡵࡷࡥࡹࡻࡳࠡࡥࡲࡨࡪ࠴ࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࠾ࠥࢁࡽࠣഀ").format(str(e)))
  elif bstack1l111l1l1l_opy_ == bstack111l1_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫഁ"):
    try:
      from behave.__main__ import main as bstack1111ll111_opy_
      from behave.configuration import Configuration
    except Exception as e:
      bstack1ll11l11l_opy_(e, bstack1ll1l1l1l_opy_)
    bstack1111ll11l_opy_()
    bstack1l1l1l1l1_opy_ = True
    bstack111111lll_opy_ = 1
    if bstack111l1_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬം") in CONFIG:
      bstack111111lll_opy_ = CONFIG[bstack111l1_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭ഃ")]
    if bstack111l1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪഄ") in CONFIG:
      bstack1l1ll111l_opy_ = int(bstack111111lll_opy_) * int(len(CONFIG[bstack111l1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫഅ")]))
    else:
      bstack1l1ll111l_opy_ = int(bstack111111lll_opy_)
    config = Configuration(args)
    bstack1l111111ll_opy_ = config.paths
    if len(bstack1l111111ll_opy_) == 0:
      import glob
      pattern = bstack111l1_opy_ (u"ࠩ࠭࠮࠴࠰࠮ࡧࡧࡤࡸࡺࡸࡥࠨആ")
      bstack1llll1l1l_opy_ = glob.glob(pattern, recursive=True)
      args.extend(bstack1llll1l1l_opy_)
      config = Configuration(args)
      bstack1l111111ll_opy_ = config.paths
    bstack11ll111l1_opy_ = [os.path.normpath(item) for item in bstack1l111111ll_opy_]
    bstack1lll11111l_opy_ = [os.path.normpath(item) for item in args]
    bstack1l11ll1l_opy_ = [item for item in bstack1lll11111l_opy_ if item not in bstack11ll111l1_opy_]
    import platform as pf
    if pf.system().lower() == bstack111l1_opy_ (u"ࠪࡻ࡮ࡴࡤࡰࡹࡶࠫഇ"):
      from pathlib import PureWindowsPath, PurePosixPath
      bstack11ll111l1_opy_ = [str(PurePosixPath(PureWindowsPath(bstack1l11l1lll1_opy_)))
                    for bstack1l11l1lll1_opy_ in bstack11ll111l1_opy_]
    bstack111lll1l1_opy_ = []
    for spec in bstack11ll111l1_opy_:
      bstack111ll1111_opy_ = []
      bstack111ll1111_opy_ += bstack1l11ll1l_opy_
      bstack111ll1111_opy_.append(spec)
      bstack111lll1l1_opy_.append(bstack111ll1111_opy_)
    execution_items = []
    for bstack111ll1111_opy_ in bstack111lll1l1_opy_:
      if bstack111l1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧഈ") in CONFIG:
        for index, _ in enumerate(CONFIG[bstack111l1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨഉ")]):
          item = {}
          item[bstack111l1_opy_ (u"࠭ࡡࡳࡩࠪഊ")] = bstack111l1_opy_ (u"ࠧࠡࠩഋ").join(bstack111ll1111_opy_)
          item[bstack111l1_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧഌ")] = index
          execution_items.append(item)
      else:
        item = {}
        item[bstack111l1_opy_ (u"ࠩࡤࡶ࡬࠭഍")] = bstack111l1_opy_ (u"ࠪࠤࠬഎ").join(bstack111ll1111_opy_)
        item[bstack111l1_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪഏ")] = 0
        execution_items.append(item)
    bstack111ll1ll_opy_ = bstack1l1ll1ll1l_opy_(execution_items, bstack1l1ll111l_opy_)
    for execution_item in bstack111ll1ll_opy_:
      bstack11ll11l11_opy_ = []
      for item in execution_item:
        bstack11ll11l11_opy_.append(bstack1ll1llll1l_opy_(name=str(item[bstack111l1_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫഐ")]),
                                             target=bstack1lll1111l_opy_,
                                             args=(item[bstack111l1_opy_ (u"࠭ࡡࡳࡩࠪ഑")],)))
      for t in bstack11ll11l11_opy_:
        t.start()
      for t in bstack11ll11l11_opy_:
        t.join()
  else:
    bstack11l1ll11_opy_(bstack1111llll_opy_)
  if not bstack11l1ll1ll_opy_:
    bstack1ll1llllll_opy_()
  bstack1l1ll1111_opy_.bstack1l111llll1_opy_()
def browserstack_initialize(bstack1l1l111l1_opy_=None):
  run_on_browserstack(bstack1l1l111l1_opy_, None, True)
def bstack1ll1llllll_opy_():
  global CONFIG
  global bstack111l111l1_opy_
  global bstack1l111l1111_opy_
  global bstack1l1l11111l_opy_
  global bstack1111ll1l1_opy_
  bstack11llllll11_opy_.stop()
  bstack1lll1l11_opy_.bstack11llll1l1_opy_()
  [bstack111l11l1l_opy_, bstack1llll1ll1l_opy_] = get_build_link()
  if bstack111l11l1l_opy_ is not None and bstack11ll11l1l_opy_() != -1:
    sessions = bstack1lll11l1ll_opy_(bstack111l11l1l_opy_)
    bstack1ll1111l1l_opy_(sessions, bstack1llll1ll1l_opy_)
  if bstack111l111l1_opy_ == bstack111l1_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧഒ") and bstack1l111l1111_opy_ != 0:
    sys.exit(bstack1l111l1111_opy_)
  if bstack111l111l1_opy_ == bstack111l1_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨഓ") and bstack1l1l11111l_opy_ != 0:
    sys.exit(bstack1l1l11111l_opy_)
def bstack1lll111l1l_opy_(bstack1ll11ll11l_opy_):
  if bstack1ll11ll11l_opy_:
    return bstack1ll11ll11l_opy_.capitalize()
  else:
    return bstack111l1_opy_ (u"ࠩࠪഔ")
def bstack11l1111l1_opy_(bstack1ll1lllll1_opy_):
  if bstack111l1_opy_ (u"ࠪࡲࡦࡳࡥࠨക") in bstack1ll1lllll1_opy_ and bstack1ll1lllll1_opy_[bstack111l1_opy_ (u"ࠫࡳࡧ࡭ࡦࠩഖ")] != bstack111l1_opy_ (u"ࠬ࠭ഗ"):
    return bstack1ll1lllll1_opy_[bstack111l1_opy_ (u"࠭࡮ࡢ࡯ࡨࠫഘ")]
  else:
    bstack1llllll1ll_opy_ = bstack111l1_opy_ (u"ࠢࠣങ")
    if bstack111l1_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࠨച") in bstack1ll1lllll1_opy_ and bstack1ll1lllll1_opy_[bstack111l1_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࠩഛ")] != None:
      bstack1llllll1ll_opy_ += bstack1ll1lllll1_opy_[bstack111l1_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࠪജ")] + bstack111l1_opy_ (u"ࠦ࠱ࠦࠢഝ")
      if bstack1ll1lllll1_opy_[bstack111l1_opy_ (u"ࠬࡵࡳࠨഞ")] == bstack111l1_opy_ (u"ࠨࡩࡰࡵࠥട"):
        bstack1llllll1ll_opy_ += bstack111l1_opy_ (u"ࠢࡪࡑࡖࠤࠧഠ")
      bstack1llllll1ll_opy_ += (bstack1ll1lllll1_opy_[bstack111l1_opy_ (u"ࠨࡱࡶࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬഡ")] or bstack111l1_opy_ (u"ࠩࠪഢ"))
      return bstack1llllll1ll_opy_
    else:
      bstack1llllll1ll_opy_ += bstack1lll111l1l_opy_(bstack1ll1lllll1_opy_[bstack111l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࠫണ")]) + bstack111l1_opy_ (u"ࠦࠥࠨത") + (
              bstack1ll1lllll1_opy_[bstack111l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠧഥ")] or bstack111l1_opy_ (u"࠭ࠧദ")) + bstack111l1_opy_ (u"ࠢ࠭ࠢࠥധ")
      if bstack1ll1lllll1_opy_[bstack111l1_opy_ (u"ࠨࡱࡶࠫന")] == bstack111l1_opy_ (u"ࠤ࡚࡭ࡳࡪ࡯ࡸࡵࠥഩ"):
        bstack1llllll1ll_opy_ += bstack111l1_opy_ (u"࡛ࠥ࡮ࡴࠠࠣപ")
      bstack1llllll1ll_opy_ += bstack1ll1lllll1_opy_[bstack111l1_opy_ (u"ࠫࡴࡹ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨഫ")] or bstack111l1_opy_ (u"ࠬ࠭ബ")
      return bstack1llllll1ll_opy_
def bstack1lllll111_opy_(bstack1llll111l_opy_):
  if bstack1llll111l_opy_ == bstack111l1_opy_ (u"ࠨࡤࡰࡰࡨࠦഭ"):
    return bstack111l1_opy_ (u"ࠧ࠽ࡶࡧࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࠣࡷࡹࡿ࡬ࡦ࠿ࠥࡧࡴࡲ࡯ࡳ࠼ࡪࡶࡪ࡫࡮࠼ࠤࡁࡀ࡫ࡵ࡮ࡵࠢࡦࡳࡱࡵࡲ࠾ࠤࡪࡶࡪ࡫࡮ࠣࡀࡆࡳࡲࡶ࡬ࡦࡶࡨࡨࡁ࠵ࡦࡰࡰࡷࡂࡁ࠵ࡴࡥࡀࠪമ")
  elif bstack1llll111l_opy_ == bstack111l1_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣയ"):
    return bstack111l1_opy_ (u"ࠩ࠿ࡸࡩࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࠥࡹࡴࡺ࡮ࡨࡁࠧࡩ࡯࡭ࡱࡵ࠾ࡷ࡫ࡤ࠼ࠤࡁࡀ࡫ࡵ࡮ࡵࠢࡦࡳࡱࡵࡲ࠾ࠤࡵࡩࡩࠨ࠾ࡇࡣ࡬ࡰࡪࡪ࠼࠰ࡨࡲࡲࡹࡄ࠼࠰ࡶࡧࡂࠬര")
  elif bstack1llll111l_opy_ == bstack111l1_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥറ"):
    return bstack111l1_opy_ (u"ࠫࡁࡺࡤࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨࠠࡴࡶࡼࡰࡪࡃࠢࡤࡱ࡯ࡳࡷࡀࡧࡳࡧࡨࡲࡀࠨ࠾࠽ࡨࡲࡲࡹࠦࡣࡰ࡮ࡲࡶࡂࠨࡧࡳࡧࡨࡲࠧࡄࡐࡢࡵࡶࡩࡩࡂ࠯ࡧࡱࡱࡸࡃࡂ࠯ࡵࡦࡁࠫല")
  elif bstack1llll111l_opy_ == bstack111l1_opy_ (u"ࠧ࡫ࡲࡳࡱࡵࠦള"):
    return bstack111l1_opy_ (u"࠭࠼ࡵࡦࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࠢࡶࡸࡾࡲࡥ࠾ࠤࡦࡳࡱࡵࡲ࠻ࡴࡨࡨࡀࠨ࠾࠽ࡨࡲࡲࡹࠦࡣࡰ࡮ࡲࡶࡂࠨࡲࡦࡦࠥࡂࡊࡸࡲࡰࡴ࠿࠳࡫ࡵ࡮ࡵࡀ࠿࠳ࡹࡪ࠾ࠨഴ")
  elif bstack1llll111l_opy_ == bstack111l1_opy_ (u"ࠢࡵ࡫ࡰࡩࡴࡻࡴࠣവ"):
    return bstack111l1_opy_ (u"ࠨ࠾ࡷࡨࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࠤࡸࡺࡹ࡭ࡧࡀࠦࡨࡵ࡬ࡰࡴ࠽ࠧࡪ࡫ࡡ࠴࠴࠹࠿ࠧࡄ࠼ࡧࡱࡱࡸࠥࡩ࡯࡭ࡱࡵࡁࠧࠩࡥࡦࡣ࠶࠶࠻ࠨ࠾ࡕ࡫ࡰࡩࡴࡻࡴ࠽࠱ࡩࡳࡳࡺ࠾࠽࠱ࡷࡨࡃ࠭ശ")
  elif bstack1llll111l_opy_ == bstack111l1_opy_ (u"ࠤࡵࡹࡳࡴࡩ࡯ࡩࠥഷ"):
    return bstack111l1_opy_ (u"ࠪࡀࡹࡪࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࠦࡳࡵࡻ࡯ࡩࡂࠨࡣࡰ࡮ࡲࡶ࠿ࡨ࡬ࡢࡥ࡮࠿ࠧࡄ࠼ࡧࡱࡱࡸࠥࡩ࡯࡭ࡱࡵࡁࠧࡨ࡬ࡢࡥ࡮ࠦࡃࡘࡵ࡯ࡰ࡬ࡲ࡬ࡂ࠯ࡧࡱࡱࡸࡃࡂ࠯ࡵࡦࡁࠫസ")
  else:
    return bstack111l1_opy_ (u"ࠫࡁࡺࡤࠡࡣ࡯࡭࡬ࡴ࠽ࠣࡥࡨࡲࡹ࡫ࡲࠣࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢࠡࡵࡷࡽࡱ࡫࠽ࠣࡥࡲࡰࡴࡸ࠺ࡣ࡮ࡤࡧࡰࡁࠢ࠿࠾ࡩࡳࡳࡺࠠࡤࡱ࡯ࡳࡷࡃࠢࡣ࡮ࡤࡧࡰࠨ࠾ࠨഹ") + bstack1lll111l1l_opy_(
      bstack1llll111l_opy_) + bstack111l1_opy_ (u"ࠬࡂ࠯ࡧࡱࡱࡸࡃࡂ࠯ࡵࡦࡁࠫഺ")
def bstack1l1ll1llll_opy_(session):
  return bstack111l1_opy_ (u"࠭࠼ࡵࡴࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡶࡴࡽࠢ࠿࠾ࡷࡨࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠣࡷࡪࡹࡳࡪࡱࡱ࠱ࡳࡧ࡭ࡦࠤࡁࡀࡦࠦࡨࡳࡧࡩࡁࠧࢁࡽࠣࠢࡷࡥࡷ࡭ࡥࡵ࠿ࠥࡣࡧࡲࡡ࡯࡭ࠥࡂࢀࢃ࠼࠰ࡣࡁࡀ࠴ࡺࡤ࠿ࡽࢀࡿࢂࡂࡴࡥࠢࡤࡰ࡮࡭࡮࠾ࠤࡦࡩࡳࡺࡥࡳࠤࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࡀࡾࢁࡁ࠵ࡴࡥࡀ࠿ࡸࡩࠦࡡ࡭࡫ࡪࡲࡂࠨࡣࡦࡰࡷࡩࡷࠨࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࡄࡻࡾ࠾࠲ࡸࡩࡄ࠼ࡵࡦࠣࡥࡱ࡯ࡧ࡯࠿ࠥࡧࡪࡴࡴࡦࡴࠥࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࡁࡿࢂࡂ࠯ࡵࡦࡁࡀࡹࡪࠠࡢ࡮࡬࡫ࡳࡃࠢࡤࡧࡱࡸࡪࡸࠢࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨ࠾ࡼࡿ࠿࠳ࡹࡪ࠾࠽࠱ࡷࡶࡃ഻࠭").format(
    session[bstack111l1_opy_ (u"ࠧࡱࡷࡥࡰ࡮ࡩ࡟ࡶࡴ࡯഼ࠫ")], bstack11l1111l1_opy_(session), bstack1lllll111_opy_(session[bstack111l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡴࡶࡤࡸࡺࡹࠧഽ")]),
    bstack1lllll111_opy_(session[bstack111l1_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩാ")]),
    bstack1lll111l1l_opy_(session[bstack111l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࠫി")] or session[bstack111l1_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࠫീ")] or bstack111l1_opy_ (u"ࠬ࠭ു")) + bstack111l1_opy_ (u"ࠨࠠࠣൂ") + (session[bstack111l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠩൃ")] or bstack111l1_opy_ (u"ࠨࠩൄ")),
    session[bstack111l1_opy_ (u"ࠩࡲࡷࠬ൅")] + bstack111l1_opy_ (u"ࠥࠤࠧെ") + session[bstack111l1_opy_ (u"ࠫࡴࡹ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨേ")], session[bstack111l1_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴࠧൈ")] or bstack111l1_opy_ (u"࠭ࠧ൉"),
    session[bstack111l1_opy_ (u"ࠧࡤࡴࡨࡥࡹ࡫ࡤࡠࡣࡷࠫൊ")] if session[bstack111l1_opy_ (u"ࠨࡥࡵࡩࡦࡺࡥࡥࡡࡤࡸࠬോ")] else bstack111l1_opy_ (u"ࠩࠪൌ"))
def bstack1ll1111l1l_opy_(sessions, bstack1llll1ll1l_opy_):
  try:
    bstack111111ll_opy_ = bstack111l1_opy_ (u"്ࠥࠦ")
    if not os.path.exists(bstack1llll1l111_opy_):
      os.mkdir(bstack1llll1l111_opy_)
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack111l1_opy_ (u"ࠫࡦࡹࡳࡦࡶࡶ࠳ࡷ࡫ࡰࡰࡴࡷ࠲࡭ࡺ࡭࡭ࠩൎ")), bstack111l1_opy_ (u"ࠬࡸࠧ൏")) as f:
      bstack111111ll_opy_ = f.read()
    bstack111111ll_opy_ = bstack111111ll_opy_.replace(bstack111l1_opy_ (u"࠭ࡻࠦࡔࡈࡗ࡚ࡒࡔࡔࡡࡆࡓ࡚ࡔࡔࠦࡿࠪ൐"), str(len(sessions)))
    bstack111111ll_opy_ = bstack111111ll_opy_.replace(bstack111l1_opy_ (u"ࠧࡼࠧࡅ࡙ࡎࡒࡄࡠࡗࡕࡐࠪࢃࠧ൑"), bstack1llll1ll1l_opy_)
    bstack111111ll_opy_ = bstack111111ll_opy_.replace(bstack111l1_opy_ (u"ࠨࡽࠨࡆ࡚ࡏࡌࡅࡡࡑࡅࡒࡋࠥࡾࠩ൒"),
                                              sessions[0].get(bstack111l1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡰࡤࡱࡪ࠭൓")) if sessions[0] else bstack111l1_opy_ (u"ࠪࠫൔ"))
    with open(os.path.join(bstack1llll1l111_opy_, bstack111l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠰ࡶࡪࡶ࡯ࡳࡶ࠱࡬ࡹࡳ࡬ࠨൕ")), bstack111l1_opy_ (u"ࠬࡽࠧൖ")) as stream:
      stream.write(bstack111111ll_opy_.split(bstack111l1_opy_ (u"࠭ࡻࠦࡕࡈࡗࡘࡏࡏࡏࡕࡢࡈࡆ࡚ࡁࠦࡿࠪൗ"))[0])
      for session in sessions:
        stream.write(bstack1l1ll1llll_opy_(session))
      stream.write(bstack111111ll_opy_.split(bstack111l1_opy_ (u"ࠧࡼࠧࡖࡉࡘ࡙ࡉࡐࡐࡖࡣࡉࡇࡔࡂࠧࢀࠫ൘"))[1])
    logger.info(bstack111l1_opy_ (u"ࠨࡉࡨࡲࡪࡸࡡࡵࡧࡧࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡦࡺ࡯࡬ࡥࠢࡤࡶࡹ࡯ࡦࡢࡥࡷࡷࠥࡧࡴࠡࡽࢀࠫ൙").format(bstack1llll1l111_opy_));
  except Exception as e:
    logger.debug(bstack11111l111_opy_.format(str(e)))
def bstack1lll11l1ll_opy_(bstack111l11l1l_opy_):
  global CONFIG
  try:
    host = bstack111l1_opy_ (u"ࠩࡤࡴ࡮࠳ࡣ࡭ࡱࡸࡨࠬ൚") if bstack111l1_opy_ (u"ࠪࡥࡵࡶࠧ൛") in CONFIG else bstack111l1_opy_ (u"ࠫࡦࡶࡩࠨ൜")
    user = CONFIG[bstack111l1_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧ൝")]
    key = CONFIG[bstack111l1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩ൞")]
    bstack1l1111l1l1_opy_ = bstack111l1_opy_ (u"ࠧࡢࡲࡳ࠱ࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭ൟ") if bstack111l1_opy_ (u"ࠨࡣࡳࡴࠬൠ") in CONFIG else bstack111l1_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶࡨࠫൡ")
    url = bstack111l1_opy_ (u"ࠪ࡬ࡹࡺࡰࡴ࠼࠲࠳ࢀࢃ࠺ࡼࡿࡃࡿࢂ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡾࢁ࠴ࡨࡵࡪ࡮ࡧࡷ࠴ࢁࡽ࠰ࡵࡨࡷࡸ࡯࡯࡯ࡵ࠱࡮ࡸࡵ࡮ࠨൢ").format(user, key, host, bstack1l1111l1l1_opy_,
                                                                                bstack111l11l1l_opy_)
    headers = {
      bstack111l1_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲ࡺࡹࡱࡧࠪൣ"): bstack111l1_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠨ൤"),
    }
    proxies = bstack1l11l11l_opy_(CONFIG, url)
    response = requests.get(url, headers=headers, proxies=proxies)
    if response.json():
      return list(map(lambda session: session[bstack111l1_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢࡷࡪࡹࡳࡪࡱࡱࠫ൥")], response.json()))
  except Exception as e:
    logger.debug(bstack1l1l11l1_opy_.format(str(e)))
def get_build_link():
  global CONFIG
  global bstack1ll11ll1l1_opy_
  try:
    if bstack111l1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪ൦") in CONFIG:
      host = bstack111l1_opy_ (u"ࠨࡣࡳ࡭࠲ࡩ࡬ࡰࡷࡧࠫ൧") if bstack111l1_opy_ (u"ࠩࡤࡴࡵ࠭൨") in CONFIG else bstack111l1_opy_ (u"ࠪࡥࡵ࡯ࠧ൩")
      user = CONFIG[bstack111l1_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭൪")]
      key = CONFIG[bstack111l1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨ൫")]
      bstack1l1111l1l1_opy_ = bstack111l1_opy_ (u"࠭ࡡࡱࡲ࠰ࡥࡺࡺ࡯࡮ࡣࡷࡩࠬ൬") if bstack111l1_opy_ (u"ࠧࡢࡲࡳࠫ൭") in CONFIG else bstack111l1_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵࡧࠪ൮")
      url = bstack111l1_opy_ (u"ࠩ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡿࢂࡀࡻࡾࡂࡾࢁ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡽࢀ࠳ࡧࡻࡩ࡭ࡦࡶ࠲࡯ࡹ࡯࡯ࠩ൯").format(user, key, host, bstack1l1111l1l1_opy_)
      headers = {
        bstack111l1_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩ൰"): bstack111l1_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧ൱"),
      }
      if bstack111l1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ൲") in CONFIG:
        params = {bstack111l1_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ൳"): CONFIG[bstack111l1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪ൴")], bstack111l1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡪࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ൵"): CONFIG[bstack111l1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ൶")]}
      else:
        params = {bstack111l1_opy_ (u"ࠪࡲࡦࡳࡥࠨ൷"): CONFIG[bstack111l1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ൸")]}
      proxies = bstack1l11l11l_opy_(CONFIG, url)
      response = requests.get(url, params=params, headers=headers, proxies=proxies)
      if response.json():
        bstack1111111l_opy_ = response.json()[0][bstack111l1_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡࡥࡹ࡮ࡲࡤࠨ൹")]
        if bstack1111111l_opy_:
          bstack1llll1ll1l_opy_ = bstack1111111l_opy_[bstack111l1_opy_ (u"࠭ࡰࡶࡤ࡯࡭ࡨࡥࡵࡳ࡮ࠪൺ")].split(bstack111l1_opy_ (u"ࠧࡱࡷࡥࡰ࡮ࡩ࠭ࡣࡷ࡬ࡰࡩ࠭ൻ"))[0] + bstack111l1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡳ࠰ࠩർ") + bstack1111111l_opy_[
            bstack111l1_opy_ (u"ࠩ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬൽ")]
          logger.info(bstack1ll111llll_opy_.format(bstack1llll1ll1l_opy_))
          bstack1ll11ll1l1_opy_ = bstack1111111l_opy_[bstack111l1_opy_ (u"ࠪ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭ൾ")]
          bstack11l11l11l_opy_ = CONFIG[bstack111l1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧൿ")]
          if bstack111l1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ඀") in CONFIG:
            bstack11l11l11l_opy_ += bstack111l1_opy_ (u"࠭ࠠࠨඁ") + CONFIG[bstack111l1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩං")]
          if bstack11l11l11l_opy_ != bstack1111111l_opy_[bstack111l1_opy_ (u"ࠨࡰࡤࡱࡪ࠭ඃ")]:
            logger.debug(bstack1lll11l1l1_opy_.format(bstack1111111l_opy_[bstack111l1_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ඄")], bstack11l11l11l_opy_))
          return [bstack1111111l_opy_[bstack111l1_opy_ (u"ࠪ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭අ")], bstack1llll1ll1l_opy_]
    else:
      logger.warn(bstack1111l11l_opy_)
  except Exception as e:
    logger.debug(bstack1l1111l1ll_opy_.format(str(e)))
  return [None, None]
def bstack1l1ll111_opy_(url, bstack111ll11l_opy_=False):
  global CONFIG
  global bstack1lllll11ll_opy_
  if not bstack1lllll11ll_opy_:
    hostname = bstack1l1lllll1_opy_(url)
    is_private = bstack1llll1llll_opy_(hostname)
    if (bstack111l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨආ") in CONFIG and not bstack1ll11llll1_opy_(CONFIG[bstack111l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩඇ")])) and (is_private or bstack111ll11l_opy_):
      bstack1lllll11ll_opy_ = hostname
def bstack1l1lllll1_opy_(url):
  return urlparse(url).hostname
def bstack1llll1llll_opy_(hostname):
  for bstack1l1l1l1ll_opy_ in bstack1llll1111l_opy_:
    regex = re.compile(bstack1l1l1l1ll_opy_)
    if regex.match(hostname):
      return True
  return False
def bstack1l111ll11l_opy_(key_name):
  return True if key_name in threading.current_thread().__dict__.keys() else False
def getAccessibilityResults(driver):
  global CONFIG
  global bstack1l11llll1l_opy_
  bstack1lll111l11_opy_ = not (bstack11l1ll1l1_opy_(threading.current_thread(), bstack111l1_opy_ (u"࠭ࡩࡴࡃ࠴࠵ࡾ࡚ࡥࡴࡶࠪඈ"), None) and bstack11l1ll1l1_opy_(
          threading.current_thread(), bstack111l1_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭ඉ"), None))
  bstack1lll11l1l_opy_ = getattr(driver, bstack111l1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡂ࠳࠴ࡽࡘ࡮࡯ࡶ࡮ࡧࡗࡨࡧ࡮ࠨඊ"), None) != True
  if not bstack1ll111111l_opy_.bstack1l1l111ll1_opy_(CONFIG, bstack1l11llll1l_opy_) or (bstack1lll11l1l_opy_ and bstack1lll111l11_opy_):
    logger.warning(bstack111l1_opy_ (u"ࠤࡑࡳࡹࠦࡡ࡯ࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡳࡦࡵࡶ࡭ࡴࡴࠬࠡࡥࡤࡲࡳࡵࡴࠡࡴࡨࡸࡷ࡯ࡥࡷࡧࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡶࡪࡹࡵ࡭ࡶࡶ࠲ࠧඋ"))
    return {}
  try:
    logger.debug(bstack111l1_opy_ (u"ࠪࡔࡪࡸࡦࡰࡴࡰ࡭ࡳ࡭ࠠࡴࡥࡤࡲࠥࡨࡥࡧࡱࡵࡩࠥ࡭ࡥࡵࡶ࡬ࡲ࡬ࠦࡲࡦࡵࡸࡰࡹࡹࠧඌ"))
    logger.debug(perform_scan(driver))
    results = driver.execute_async_script(bstack1lll11l1_opy_.bstack1lll1111ll_opy_)
    return results
  except Exception:
    logger.error(bstack111l1_opy_ (u"ࠦࡓࡵࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡳࡧࡶࡹࡱࡺࡳࠡࡹࡨࡶࡪࠦࡦࡰࡷࡱࡨ࠳ࠨඍ"))
    return {}
def getAccessibilityResultsSummary(driver):
  global CONFIG
  global bstack1l11llll1l_opy_
  bstack1lll111l11_opy_ = not (bstack11l1ll1l1_opy_(threading.current_thread(), bstack111l1_opy_ (u"ࠬ࡯ࡳࡂ࠳࠴ࡽ࡙࡫ࡳࡵࠩඎ"), None) and bstack11l1ll1l1_opy_(
          threading.current_thread(), bstack111l1_opy_ (u"࠭ࡡ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬඏ"), None))
  bstack1lll11l1l_opy_ = getattr(driver, bstack111l1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡁ࠲࠳ࡼࡗ࡭ࡵࡵ࡭ࡦࡖࡧࡦࡴࠧඐ"), None) != True
  if not bstack1ll111111l_opy_.bstack1l1l111ll1_opy_(CONFIG, bstack1l11llll1l_opy_) or (bstack1lll11l1l_opy_ and bstack1lll111l11_opy_):
    logger.warning(bstack111l1_opy_ (u"ࠣࡐࡲࡸࠥࡧ࡮ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡹࡥࡴࡵ࡬ࡳࡳ࠲ࠠࡤࡣࡱࡲࡴࡺࠠࡳࡧࡷࡶ࡮࡫ࡶࡦࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡵࡩࡸࡻ࡬ࡵࡵࠣࡷࡺࡳ࡭ࡢࡴࡼ࠲ࠧඑ"))
    return {}
  try:
    logger.debug(bstack111l1_opy_ (u"ࠩࡓࡩࡷ࡬࡯ࡳ࡯࡬ࡲ࡬ࠦࡳࡤࡣࡱࠤࡧ࡫ࡦࡰࡴࡨࠤ࡬࡫ࡴࡵ࡫ࡱ࡫ࠥࡸࡥࡴࡷ࡯ࡸࡸࠦࡳࡶ࡯ࡰࡥࡷࡿࠧඒ"))
    logger.debug(perform_scan(driver))
    bstack1ll1111l11_opy_ = driver.execute_async_script(bstack1lll11l1_opy_.bstack1ll1ll1l1l_opy_)
    return bstack1ll1111l11_opy_
  except Exception:
    logger.error(bstack111l1_opy_ (u"ࠥࡒࡴࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡳࡶ࡯ࡰࡥࡷࡿࠠࡸࡣࡶࠤ࡫ࡵࡵ࡯ࡦ࠱ࠦඓ"))
    return {}
def perform_scan(driver, *args, **kwargs):
  global CONFIG
  global bstack1l11llll1l_opy_
  bstack1lll111l11_opy_ = not (bstack11l1ll1l1_opy_(threading.current_thread(), bstack111l1_opy_ (u"ࠫ࡮ࡹࡁ࠲࠳ࡼࡘࡪࡹࡴࠨඔ"), None) and bstack11l1ll1l1_opy_(
          threading.current_thread(), bstack111l1_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫඕ"), None))
  bstack1lll11l1l_opy_ = getattr(driver, bstack111l1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡇ࠱࠲ࡻࡖ࡬ࡴࡻ࡬ࡥࡕࡦࡥࡳ࠭ඖ"), None) != True
  if not bstack1ll111111l_opy_.bstack1l1l111ll1_opy_(CONFIG, bstack1l11llll1l_opy_) or (bstack1lll11l1l_opy_ and bstack1lll111l11_opy_):
    logger.warning(bstack111l1_opy_ (u"ࠢࡏࡱࡷࠤࡦࡴࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠱ࠦࡣࡢࡰࡱࡳࡹࠦࡲࡶࡰࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡷࡨࡧ࡮࠯ࠤ඗"))
    return {}
  try:
    bstack1ll1l1llll_opy_ = driver.execute_async_script(bstack1lll11l1_opy_.perform_scan, {bstack111l1_opy_ (u"ࠨ࡯ࡨࡸ࡭ࡵࡤࠨ඘"): kwargs.get(bstack111l1_opy_ (u"ࠩࡧࡶ࡮ࡼࡥࡳࡡࡦࡳࡲࡳࡡ࡯ࡦࠪ඙"), None) or bstack111l1_opy_ (u"ࠪࠫක")})
    return bstack1ll1l1llll_opy_
  except Exception:
    logger.error(bstack111l1_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡳࡷࡱࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡸࡩࡡ࡯࠰ࠥඛ"))
    return {}