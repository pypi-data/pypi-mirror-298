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
import sys
import json
import time
import shutil
import tempfile
import requests
import subprocess
from threading import Thread
from os.path import expanduser
from bstack_utils.constants import *
from requests.auth import HTTPBasicAuth
from bstack_utils.helper import bstack1lll1l1ll_opy_, bstack1ll1l11111_opy_
class bstack1l11l111_opy_:
  working_dir = os.getcwd()
  bstack1lllllll11_opy_ = False
  config = {}
  binary_path = bstack111l1_opy_ (u"ࠨࠩᔈ")
  bstack1llll1ll1l1_opy_ = bstack111l1_opy_ (u"ࠩࠪᔉ")
  bstack1l1l111111_opy_ = False
  bstack1lllll11l11_opy_ = None
  bstack1llll1111l1_opy_ = {}
  bstack1lll1ll11l1_opy_ = 300
  bstack1llll1l111l_opy_ = False
  logger = None
  bstack1llll1l1111_opy_ = False
  bstack111ll1l1l_opy_ = False
  bstack11l1111ll_opy_ = None
  bstack1llll11l1l1_opy_ = bstack111l1_opy_ (u"ࠪࠫᔊ")
  bstack1lll1lll1ll_opy_ = {
    bstack111l1_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࠫᔋ") : 1,
    bstack111l1_opy_ (u"ࠬ࡬ࡩࡳࡧࡩࡳࡽ࠭ᔌ") : 2,
    bstack111l1_opy_ (u"࠭ࡥࡥࡩࡨࠫᔍ") : 3,
    bstack111l1_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯ࠧᔎ") : 4
  }
  def __init__(self) -> None: pass
  def bstack1lll1ll1l1l_opy_(self):
    bstack1llll1111ll_opy_ = bstack111l1_opy_ (u"ࠨࠩᔏ")
    bstack1llll111ll1_opy_ = sys.platform
    bstack1lllll11ll1_opy_ = bstack111l1_opy_ (u"ࠩࡳࡩࡷࡩࡹࠨᔐ")
    if re.match(bstack111l1_opy_ (u"ࠥࡨࡦࡸࡷࡪࡰࡿࡱࡦࡩࠠࡰࡵࠥᔑ"), bstack1llll111ll1_opy_) != None:
      bstack1llll1111ll_opy_ = bstack111ll11l11_opy_ + bstack111l1_opy_ (u"ࠦ࠴ࡶࡥࡳࡥࡼ࠱ࡴࡹࡸ࠯ࡼ࡬ࡴࠧᔒ")
      self.bstack1llll11l1l1_opy_ = bstack111l1_opy_ (u"ࠬࡳࡡࡤࠩᔓ")
    elif re.match(bstack111l1_opy_ (u"ࠨ࡭ࡴࡹ࡬ࡲࢁࡳࡳࡺࡵࡿࡱ࡮ࡴࡧࡸࡾࡦࡽ࡬ࡽࡩ࡯ࡾࡥࡧࡨࡽࡩ࡯ࡾࡺ࡭ࡳࡩࡥࡽࡧࡰࡧࢁࡽࡩ࡯࠵࠵ࠦᔔ"), bstack1llll111ll1_opy_) != None:
      bstack1llll1111ll_opy_ = bstack111ll11l11_opy_ + bstack111l1_opy_ (u"ࠢ࠰ࡲࡨࡶࡨࡿ࠭ࡸ࡫ࡱ࠲ࡿ࡯ࡰࠣᔕ")
      bstack1lllll11ll1_opy_ = bstack111l1_opy_ (u"ࠣࡲࡨࡶࡨࡿ࠮ࡦࡺࡨࠦᔖ")
      self.bstack1llll11l1l1_opy_ = bstack111l1_opy_ (u"ࠩࡺ࡭ࡳ࠭ᔗ")
    else:
      bstack1llll1111ll_opy_ = bstack111ll11l11_opy_ + bstack111l1_opy_ (u"ࠥ࠳ࡵ࡫ࡲࡤࡻ࠰ࡰ࡮ࡴࡵࡹ࠰ࡽ࡭ࡵࠨᔘ")
      self.bstack1llll11l1l1_opy_ = bstack111l1_opy_ (u"ࠫࡱ࡯࡮ࡶࡺࠪᔙ")
    return bstack1llll1111ll_opy_, bstack1lllll11ll1_opy_
  def bstack1llll11ll11_opy_(self):
    try:
      bstack1llll1ll1ll_opy_ = [os.path.join(expanduser(bstack111l1_opy_ (u"ࠧࢄࠢᔚ")), bstack111l1_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ᔛ")), self.working_dir, tempfile.gettempdir()]
      for path in bstack1llll1ll1ll_opy_:
        if(self.bstack1llll11111l_opy_(path)):
          return path
      raise bstack111l1_opy_ (u"ࠢࡖࡰࡤࡰࡧ࡫ࠠࡵࡱࠣࡨࡴࡽ࡮࡭ࡱࡤࡨࠥࡶࡥࡳࡥࡼࠤࡧ࡯࡮ࡢࡴࡼࠦᔜ")
    except Exception as e:
      self.logger.error(bstack111l1_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤ࡫࡯࡮ࡥࠢࡤࡺࡦ࡯࡬ࡢࡤ࡯ࡩࠥࡶࡡࡵࡪࠣࡪࡴࡸࠠࡱࡧࡵࡧࡾࠦࡤࡰࡹࡱࡰࡴࡧࡤ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࠳ࠠࡼࡿࠥᔝ").format(e))
  def bstack1llll11111l_opy_(self, path):
    try:
      if not os.path.exists(path):
        os.makedirs(path)
      return True
    except:
      return False
  def bstack1llll111111_opy_(self, bstack1llll1111ll_opy_, bstack1lllll11ll1_opy_):
    try:
      bstack1llll1l11ll_opy_ = self.bstack1llll11ll11_opy_()
      bstack1lllll11l1l_opy_ = os.path.join(bstack1llll1l11ll_opy_, bstack111l1_opy_ (u"ࠩࡳࡩࡷࡩࡹ࠯ࡼ࡬ࡴࠬᔞ"))
      bstack1lllll1111l_opy_ = os.path.join(bstack1llll1l11ll_opy_, bstack1lllll11ll1_opy_)
      if os.path.exists(bstack1lllll1111l_opy_):
        self.logger.info(bstack111l1_opy_ (u"ࠥࡔࡪࡸࡣࡺࠢࡥ࡭ࡳࡧࡲࡺࠢࡩࡳࡺࡴࡤࠡ࡫ࡱࠤࢀࢃࠬࠡࡵ࡮࡭ࡵࡶࡩ࡯ࡩࠣࡨࡴࡽ࡮࡭ࡱࡤࡨࠧᔟ").format(bstack1lllll1111l_opy_))
        return bstack1lllll1111l_opy_
      if os.path.exists(bstack1lllll11l1l_opy_):
        self.logger.info(bstack111l1_opy_ (u"ࠦࡕ࡫ࡲࡤࡻࠣࡾ࡮ࡶࠠࡧࡱࡸࡲࡩࠦࡩ࡯ࠢࡾࢁ࠱ࠦࡵ࡯ࡼ࡬ࡴࡵ࡯࡮ࡨࠤᔠ").format(bstack1lllll11l1l_opy_))
        return self.bstack1llll1lll11_opy_(bstack1lllll11l1l_opy_, bstack1lllll11ll1_opy_)
      self.logger.info(bstack111l1_opy_ (u"ࠧࡊ࡯ࡸࡰ࡯ࡳࡦࡪࡩ࡯ࡩࠣࡴࡪࡸࡣࡺࠢࡥ࡭ࡳࡧࡲࡺࠢࡩࡶࡴࡳࠠࡼࡿࠥᔡ").format(bstack1llll1111ll_opy_))
      response = bstack1ll1l11111_opy_(bstack111l1_opy_ (u"࠭ࡇࡆࡖࠪᔢ"), bstack1llll1111ll_opy_, {}, {})
      if response.status_code == 200:
        with open(bstack1lllll11l1l_opy_, bstack111l1_opy_ (u"ࠧࡸࡤࠪᔣ")) as file:
          file.write(response.content)
        self.logger.info(bstack111l1_opy_ (u"ࠣࡆࡲࡻࡳࡲ࡯ࡢࡦࡨࡨࠥࡶࡥࡳࡥࡼࠤࡧ࡯࡮ࡢࡴࡼࠤࡦࡴࡤࠡࡵࡤࡺࡪࡪࠠࡢࡶࠣࡿࢂࠨᔤ").format(bstack1lllll11l1l_opy_))
        return self.bstack1llll1lll11_opy_(bstack1lllll11l1l_opy_, bstack1lllll11ll1_opy_)
      else:
        raise(bstack111l1_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࠠࡵࡪࡨࠤ࡫࡯࡬ࡦ࠰ࠣࡗࡹࡧࡴࡶࡵࠣࡧࡴࡪࡥ࠻ࠢࡾࢁࠧᔥ").format(response.status_code))
    except Exception as e:
      self.logger.error(bstack111l1_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡤࡰࡹࡱࡰࡴࡧࡤࠡࡲࡨࡶࡨࡿࠠࡣ࡫ࡱࡥࡷࡿ࠺ࠡࡽࢀࠦᔦ").format(e))
  def bstack1llll1lllll_opy_(self, bstack1llll1111ll_opy_, bstack1lllll11ll1_opy_):
    try:
      retry = 2
      bstack1lllll1111l_opy_ = None
      bstack1lll1lll1l1_opy_ = False
      while retry > 0:
        bstack1lllll1111l_opy_ = self.bstack1llll111111_opy_(bstack1llll1111ll_opy_, bstack1lllll11ll1_opy_)
        bstack1lll1lll1l1_opy_ = self.bstack1llll1l1l11_opy_(bstack1llll1111ll_opy_, bstack1lllll11ll1_opy_, bstack1lllll1111l_opy_)
        if bstack1lll1lll1l1_opy_:
          break
        retry -= 1
      return bstack1lllll1111l_opy_, bstack1lll1lll1l1_opy_
    except Exception as e:
      self.logger.error(bstack111l1_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡨࡧࡷࠤࡵ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻࠣࡴࡦࡺࡨࠣᔧ").format(e))
    return bstack1lllll1111l_opy_, False
  def bstack1llll1l1l11_opy_(self, bstack1llll1111ll_opy_, bstack1lllll11ll1_opy_, bstack1lllll1111l_opy_, bstack1lll1ll1l11_opy_ = 0):
    if bstack1lll1ll1l11_opy_ > 1:
      return False
    if bstack1lllll1111l_opy_ == None or os.path.exists(bstack1lllll1111l_opy_) == False:
      self.logger.warn(bstack111l1_opy_ (u"ࠧࡖࡥࡳࡥࡼࠤࡵࡧࡴࡩࠢࡱࡳࡹࠦࡦࡰࡷࡱࡨ࠱ࠦࡲࡦࡶࡵࡽ࡮ࡴࡧࠡࡦࡲࡻࡳࡲ࡯ࡢࡦࠥᔨ"))
      return False
    bstack1llll1ll111_opy_ = bstack111l1_opy_ (u"ࠨ࡞࠯ࠬࡃࡴࡪࡸࡣࡺ࡞࠲ࡧࡱ࡯ࠠ࡝ࡦ࠱ࡠࡩ࠱࠮࡝ࡦ࠮ࠦᔩ")
    command = bstack111l1_opy_ (u"ࠧࡼࡿࠣ࠱࠲ࡼࡥࡳࡵ࡬ࡳࡳ࠭ᔪ").format(bstack1lllll1111l_opy_)
    bstack1llll1llll1_opy_ = subprocess.check_output(command, shell=True, text=True)
    if re.match(bstack1llll1ll111_opy_, bstack1llll1llll1_opy_) != None:
      return True
    else:
      self.logger.error(bstack111l1_opy_ (u"ࠣࡒࡨࡶࡨࡿࠠࡷࡧࡵࡷ࡮ࡵ࡮ࠡࡥ࡫ࡩࡨࡱࠠࡧࡣ࡬ࡰࡪࡪࠢᔫ"))
      return False
  def bstack1llll1lll11_opy_(self, bstack1lllll11l1l_opy_, bstack1lllll11ll1_opy_):
    try:
      working_dir = os.path.dirname(bstack1lllll11l1l_opy_)
      shutil.unpack_archive(bstack1lllll11l1l_opy_, working_dir)
      bstack1lllll1111l_opy_ = os.path.join(working_dir, bstack1lllll11ll1_opy_)
      os.chmod(bstack1lllll1111l_opy_, 0o755)
      return bstack1lllll1111l_opy_
    except Exception as e:
      self.logger.error(bstack111l1_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡻ࡮ࡻ࡫ࡳࠤࡵ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻࠥᔬ"))
  def bstack1llll1ll11l_opy_(self):
    try:
      bstack1llll1l1lll_opy_ = self.config.get(bstack111l1_opy_ (u"ࠪࡴࡪࡸࡣࡺࠩᔭ"))
      bstack1llll1ll11l_opy_ = bstack1llll1l1lll_opy_ or (bstack1llll1l1lll_opy_ is None and self.bstack1lllllll11_opy_)
      if not bstack1llll1ll11l_opy_ or self.config.get(bstack111l1_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧᔮ"), None) not in bstack111ll11l1l_opy_:
        return False
      self.bstack1l1l111111_opy_ = True
      return True
    except Exception as e:
      self.logger.error(bstack111l1_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡦࡨࡸࡪࡩࡴࠡࡲࡨࡶࡨࡿࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࢀࢃࠢᔯ").format(e))
  def bstack1llll1l1l1l_opy_(self):
    try:
      bstack1llll1l1l1l_opy_ = self.bstack1llll11l1ll_opy_
      return bstack1llll1l1l1l_opy_
    except Exception as e:
      self.logger.error(bstack111l1_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡧࡩࡹ࡫ࡣࡵࠢࡳࡩࡷࡩࡹࠡࡥࡤࡴࡹࡻࡲࡦࠢࡰࡳࡩ࡫ࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࢀࢃࠢᔰ").format(e))
  def init(self, bstack1lllllll11_opy_, config, logger):
    self.bstack1lllllll11_opy_ = bstack1lllllll11_opy_
    self.config = config
    self.logger = logger
    if not self.bstack1llll1ll11l_opy_():
      return
    self.bstack1llll1111l1_opy_ = config.get(bstack111l1_opy_ (u"ࠧࡱࡧࡵࡧࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ᔱ"), {})
    self.bstack1llll11l1ll_opy_ = config.get(bstack111l1_opy_ (u"ࠨࡲࡨࡶࡨࡿࡃࡢࡲࡷࡹࡷ࡫ࡍࡰࡦࡨࠫᔲ"))
    try:
      bstack1llll1111ll_opy_, bstack1lllll11ll1_opy_ = self.bstack1lll1ll1l1l_opy_()
      bstack1lllll1111l_opy_, bstack1lll1lll1l1_opy_ = self.bstack1llll1lllll_opy_(bstack1llll1111ll_opy_, bstack1lllll11ll1_opy_)
      if bstack1lll1lll1l1_opy_:
        self.binary_path = bstack1lllll1111l_opy_
        thread = Thread(target=self.bstack1lll1llll11_opy_)
        thread.start()
      else:
        self.bstack1llll1l1111_opy_ = True
        self.logger.error(bstack111l1_opy_ (u"ࠤࡌࡲࡻࡧ࡬ࡪࡦࠣࡴࡪࡸࡣࡺࠢࡳࡥࡹ࡮ࠠࡧࡱࡸࡲࡩࠦ࠭ࠡࡽࢀ࠰࡛ࠥ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡵࡷࡥࡷࡺࠠࡑࡧࡵࡧࡾࠨᔳ").format(bstack1lllll1111l_opy_))
    except Exception as e:
      self.logger.error(bstack111l1_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡵࡣࡵࡸࠥࡶࡥࡳࡥࡼ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡽࢀࠦᔴ").format(e))
  def bstack1llll11lll1_opy_(self):
    try:
      logfile = os.path.join(self.working_dir, bstack111l1_opy_ (u"ࠫࡱࡵࡧࠨᔵ"), bstack111l1_opy_ (u"ࠬࡶࡥࡳࡥࡼ࠲ࡱࡵࡧࠨᔶ"))
      os.makedirs(os.path.dirname(logfile)) if not os.path.exists(os.path.dirname(logfile)) else None
      self.logger.debug(bstack111l1_opy_ (u"ࠨࡐࡶࡵ࡫࡭ࡳ࡭ࠠࡱࡧࡵࡧࡾࠦ࡬ࡰࡩࡶࠤࡦࡺࠠࡼࡿࠥᔷ").format(logfile))
      self.bstack1llll1ll1l1_opy_ = logfile
    except Exception as e:
      self.logger.error(bstack111l1_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡷࡪࡺࠠࡱࡧࡵࡧࡾࠦ࡬ࡰࡩࠣࡴࡦࡺࡨ࠭ࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࢁࡽࠣᔸ").format(e))
  def bstack1lll1llll11_opy_(self):
    bstack1lllll11111_opy_ = self.bstack1lll1ll1ll1_opy_()
    if bstack1lllll11111_opy_ == None:
      self.bstack1llll1l1111_opy_ = True
      self.logger.error(bstack111l1_opy_ (u"ࠣࡒࡨࡶࡨࡿࠠࡵࡱ࡮ࡩࡳࠦ࡮ࡰࡶࠣࡪࡴࡻ࡮ࡥ࠮ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡵࡣࡵࡸࠥࡶࡥࡳࡥࡼࠦᔹ"))
      return False
    command_args = [bstack111l1_opy_ (u"ࠤࡤࡴࡵࡀࡥࡹࡧࡦ࠾ࡸࡺࡡࡳࡶࠥᔺ") if self.bstack1lllllll11_opy_ else bstack111l1_opy_ (u"ࠪࡩࡽ࡫ࡣ࠻ࡵࡷࡥࡷࡺࠧᔻ")]
    bstack1lll1llllll_opy_ = self.bstack1llll111l11_opy_()
    if bstack1lll1llllll_opy_ != None:
      command_args.append(bstack111l1_opy_ (u"ࠦ࠲ࡩࠠࡼࡿࠥᔼ").format(bstack1lll1llllll_opy_))
    env = os.environ.copy()
    env[bstack111l1_opy_ (u"ࠧࡖࡅࡓࡅ࡜ࡣ࡙ࡕࡋࡆࡐࠥᔽ")] = bstack1lllll11111_opy_
    env[bstack111l1_opy_ (u"ࠨࡔࡉࡡࡅ࡙ࡎࡒࡄࡠࡗࡘࡍࡉࠨᔾ")] = os.environ.get(bstack111l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬᔿ"), bstack111l1_opy_ (u"ࠨࠩᕀ"))
    bstack1llll1l1ll1_opy_ = [self.binary_path]
    self.bstack1llll11lll1_opy_()
    self.bstack1lllll11l11_opy_ = self.bstack1lllll111l1_opy_(bstack1llll1l1ll1_opy_ + command_args, env)
    self.logger.debug(bstack111l1_opy_ (u"ࠤࡖࡸࡦࡸࡴࡪࡰࡪࠤࡍ࡫ࡡ࡭ࡶ࡫ࠤࡈ࡮ࡥࡤ࡭ࠥᕁ"))
    bstack1lll1ll1l11_opy_ = 0
    while self.bstack1lllll11l11_opy_.poll() == None:
      bstack1llll1l11l1_opy_ = self.bstack1llll11l111_opy_()
      if bstack1llll1l11l1_opy_:
        self.logger.debug(bstack111l1_opy_ (u"ࠥࡌࡪࡧ࡬ࡵࡪࠣࡇ࡭࡫ࡣ࡬ࠢࡶࡹࡨࡩࡥࡴࡵࡩࡹࡱࠨᕂ"))
        self.bstack1llll1l111l_opy_ = True
        return True
      bstack1lll1ll1l11_opy_ += 1
      self.logger.debug(bstack111l1_opy_ (u"ࠦࡍ࡫ࡡ࡭ࡶ࡫ࠤࡈ࡮ࡥࡤ࡭ࠣࡖࡪࡺࡲࡺࠢ࠰ࠤࢀࢃࠢᕃ").format(bstack1lll1ll1l11_opy_))
      time.sleep(2)
    self.logger.error(bstack111l1_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡷࡥࡷࡺࠠࡱࡧࡵࡧࡾ࠲ࠠࡉࡧࡤࡰࡹ࡮ࠠࡄࡪࡨࡧࡰࠦࡆࡢ࡫࡯ࡩࡩࠦࡡࡧࡶࡨࡶࠥࢁࡽࠡࡣࡷࡸࡪࡳࡰࡵࡵࠥᕄ").format(bstack1lll1ll1l11_opy_))
    self.bstack1llll1l1111_opy_ = True
    return False
  def bstack1llll11l111_opy_(self, bstack1lll1ll1l11_opy_ = 0):
    if bstack1lll1ll1l11_opy_ > 10:
      return False
    try:
      bstack1lll1lll111_opy_ = os.environ.get(bstack111l1_opy_ (u"࠭ࡐࡆࡔࡆ࡝ࡤ࡙ࡅࡓࡘࡈࡖࡤࡇࡄࡅࡔࡈࡗࡘ࠭ᕅ"), bstack111l1_opy_ (u"ࠧࡩࡶࡷࡴ࠿࠵࠯࡭ࡱࡦࡥࡱ࡮࡯ࡴࡶ࠽࠹࠸࠹࠸ࠨᕆ"))
      bstack1lllll111ll_opy_ = bstack1lll1lll111_opy_ + bstack111ll11ll1_opy_
      response = requests.get(bstack1lllll111ll_opy_)
      data = response.json()
      self.bstack11l1111ll_opy_ = getattr(data.get(bstack111l1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࠧᕇ"), {}), bstack111l1_opy_ (u"ࠩ࡬ࡨࠬᕈ"), None)
      return True
    except:
      self.logger.debug(bstack111l1_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡲࡧࡨࡻࡲࡳࡧࡧࠤࡼ࡮ࡩ࡭ࡧࠣࡴࡷࡵࡣࡦࡵࡶ࡭ࡳ࡭ࠠࡩࡧࡤࡰࡹ࡮ࠠࡤࡪࡨࡧࡰࠦࡲࡦࡵࡳࡳࡳࡹࡥࠣᕉ"))
      return False
  def bstack1lll1ll1ll1_opy_(self):
    bstack1lll1llll1l_opy_ = bstack111l1_opy_ (u"ࠫࡦࡶࡰࠨᕊ") if self.bstack1lllllll11_opy_ else bstack111l1_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡫ࠧᕋ")
    bstack1lll1lllll1_opy_ = bstack111l1_opy_ (u"ࠨࡵ࡯ࡦࡨࡪ࡮ࡴࡥࡥࠤᕌ") if self.config.get(bstack111l1_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠭ᕍ")) is None else True
    bstack11111l111l_opy_ = bstack111l1_opy_ (u"ࠣࡣࡳ࡭࠴ࡧࡰࡱࡡࡳࡩࡷࡩࡹ࠰ࡩࡨࡸࡤࡶࡲࡰ࡬ࡨࡧࡹࡥࡴࡰ࡭ࡨࡲࡄࡴࡡ࡮ࡧࡀࡿࢂࠬࡴࡺࡲࡨࡁࢀࢃࠦࡱࡧࡵࡧࡾࡃࡻࡾࠤᕎ").format(self.config[bstack111l1_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧᕏ")], bstack1lll1llll1l_opy_, bstack1lll1lllll1_opy_)
    if self.bstack1llll11l1ll_opy_:
      bstack11111l111l_opy_ += bstack111l1_opy_ (u"ࠥࠪࡵ࡫ࡲࡤࡻࡢࡧࡦࡶࡴࡶࡴࡨࡣࡲࡵࡤࡦ࠿ࡾࢁࠧᕐ").format(self.bstack1llll11l1ll_opy_)
    uri = bstack1lll1l1ll_opy_(bstack11111l111l_opy_)
    try:
      response = bstack1ll1l11111_opy_(bstack111l1_opy_ (u"ࠫࡌࡋࡔࠨᕑ"), uri, {}, {bstack111l1_opy_ (u"ࠬࡧࡵࡵࡪࠪᕒ"): (self.config[bstack111l1_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨᕓ")], self.config[bstack111l1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪᕔ")])})
      if response.status_code == 200:
        data = response.json()
        self.bstack1l1l111111_opy_ = data.get(bstack111l1_opy_ (u"ࠨࡵࡸࡧࡨ࡫ࡳࡴࠩᕕ"))
        self.bstack1llll11l1ll_opy_ = data.get(bstack111l1_opy_ (u"ࠩࡳࡩࡷࡩࡹࡠࡥࡤࡴࡹࡻࡲࡦࡡࡰࡳࡩ࡫ࠧᕖ"))
        os.environ[bstack111l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡉࡗࡉ࡙ࠨᕗ")] = str(self.bstack1l1l111111_opy_)
        os.environ[bstack111l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡊࡘࡃ࡚ࡡࡆࡅࡕ࡚ࡕࡓࡇࡢࡑࡔࡊࡅࠨᕘ")] = str(self.bstack1llll11l1ll_opy_)
        if bstack1lll1lllll1_opy_ == bstack111l1_opy_ (u"ࠧࡻ࡮ࡥࡧࡩ࡭ࡳ࡫ࡤࠣᕙ") and str(self.bstack1l1l111111_opy_).lower() == bstack111l1_opy_ (u"ࠨࡴࡳࡷࡨࠦᕚ"):
          self.bstack111ll1l1l_opy_ = True
        if bstack111l1_opy_ (u"ࠢࡵࡱ࡮ࡩࡳࠨᕛ") in data:
          return data[bstack111l1_opy_ (u"ࠣࡶࡲ࡯ࡪࡴࠢᕜ")]
        else:
          raise bstack111l1_opy_ (u"ࠩࡗࡳࡰ࡫࡮ࠡࡐࡲࡸࠥࡌ࡯ࡶࡰࡧࠤ࠲ࠦࡻࡾࠩᕝ").format(data)
      else:
        raise bstack111l1_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡦࡦࡶࡦ࡬ࠥࡶࡥࡳࡥࡼࠤࡹࡵ࡫ࡦࡰ࠯ࠤࡗ࡫ࡳࡱࡱࡱࡷࡪࠦࡳࡵࡣࡷࡹࡸࠦ࠭ࠡࡽࢀ࠰ࠥࡘࡥࡴࡲࡲࡲࡸ࡫ࠠࡃࡱࡧࡽࠥ࠳ࠠࡼࡿࠥᕞ").format(response.status_code, response.json())
    except Exception as e:
      self.logger.error(bstack111l1_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡧࡷ࡫ࡡࡵ࡫ࡱ࡫ࠥࡶࡥࡳࡥࡼࠤࡵࡸ࡯࡫ࡧࡦࡸࠧᕟ").format(e))
  def bstack1llll111l11_opy_(self):
    bstack1llll11llll_opy_ = os.path.join(tempfile.gettempdir(), bstack111l1_opy_ (u"ࠧࡶࡥࡳࡥࡼࡇࡴࡴࡦࡪࡩ࠱࡮ࡸࡵ࡮ࠣᕠ"))
    try:
      if bstack111l1_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴࠧᕡ") not in self.bstack1llll1111l1_opy_:
        self.bstack1llll1111l1_opy_[bstack111l1_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࠨᕢ")] = 2
      with open(bstack1llll11llll_opy_, bstack111l1_opy_ (u"ࠨࡹࠪᕣ")) as fp:
        json.dump(self.bstack1llll1111l1_opy_, fp)
      return bstack1llll11llll_opy_
    except Exception as e:
      self.logger.error(bstack111l1_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡩࡲࡦࡣࡷࡩࠥࡶࡥࡳࡥࡼࠤࡨࡵ࡮ࡧ࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡻࡾࠤᕤ").format(e))
  def bstack1lllll111l1_opy_(self, cmd, env = os.environ.copy()):
    try:
      if self.bstack1llll11l1l1_opy_ == bstack111l1_opy_ (u"ࠪࡻ࡮ࡴࠧᕥ"):
        bstack1llll11l11l_opy_ = [bstack111l1_opy_ (u"ࠫࡨࡳࡤ࠯ࡧࡻࡩࠬᕦ"), bstack111l1_opy_ (u"ࠬ࠵ࡣࠨᕧ")]
        cmd = bstack1llll11l11l_opy_ + cmd
      cmd = bstack111l1_opy_ (u"࠭ࠠࠨᕨ").join(cmd)
      self.logger.debug(bstack111l1_opy_ (u"ࠢࡓࡷࡱࡲ࡮ࡴࡧࠡࡽࢀࠦᕩ").format(cmd))
      with open(self.bstack1llll1ll1l1_opy_, bstack111l1_opy_ (u"ࠣࡣࠥᕪ")) as bstack1llll11ll1l_opy_:
        process = subprocess.Popen(cmd, shell=True, stdout=bstack1llll11ll1l_opy_, text=True, stderr=bstack1llll11ll1l_opy_, env=env, universal_newlines=True)
      return process
    except Exception as e:
      self.bstack1llll1l1111_opy_ = True
      self.logger.error(bstack111l1_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡴࡢࡴࡷࠤࡵ࡫ࡲࡤࡻࠣࡻ࡮ࡺࡨࠡࡥࡰࡨࠥ࠳ࠠࡼࡿ࠯ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴ࠺ࠡࡽࢀࠦᕫ").format(cmd, e))
  def shutdown(self):
    try:
      if self.bstack1llll1l111l_opy_:
        self.logger.info(bstack111l1_opy_ (u"ࠥࡗࡹࡵࡰࡱ࡫ࡱ࡫ࠥࡖࡥࡳࡥࡼࠦᕬ"))
        cmd = [self.binary_path, bstack111l1_opy_ (u"ࠦࡪࡾࡥࡤ࠼ࡶࡸࡴࡶࠢᕭ")]
        self.bstack1lllll111l1_opy_(cmd)
        self.bstack1llll1l111l_opy_ = False
    except Exception as e:
      self.logger.error(bstack111l1_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡷࡳࡵࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡸ࡫ࡷ࡬ࠥࡩ࡯࡮࡯ࡤࡲࡩࠦ࠭ࠡࡽࢀ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮࠻ࠢࡾࢁࠧᕮ").format(cmd, e))
  def bstack1ll1l1l1l1_opy_(self):
    if not self.bstack1l1l111111_opy_:
      return
    try:
      bstack1lll1lll11l_opy_ = 0
      while not self.bstack1llll1l111l_opy_ and bstack1lll1lll11l_opy_ < self.bstack1lll1ll11l1_opy_:
        if self.bstack1llll1l1111_opy_:
          self.logger.info(bstack111l1_opy_ (u"ࠨࡐࡦࡴࡦࡽࠥࡹࡥࡵࡷࡳࠤ࡫ࡧࡩ࡭ࡧࡧࠦᕯ"))
          return
        time.sleep(1)
        bstack1lll1lll11l_opy_ += 1
      os.environ[bstack111l1_opy_ (u"ࠧࡑࡇࡕࡇ࡞ࡥࡂࡆࡕࡗࡣࡕࡒࡁࡕࡈࡒࡖࡒ࠭ᕰ")] = str(self.bstack1lll1ll1lll_opy_())
      self.logger.info(bstack111l1_opy_ (u"ࠣࡒࡨࡶࡨࡿࠠࡴࡧࡷࡹࡵࠦࡣࡰ࡯ࡳࡰࡪࡺࡥࡥࠤᕱ"))
    except Exception as e:
      self.logger.error(bstack111l1_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡹࡥࡵࡷࡳࠤࡵ࡫ࡲࡤࡻ࠯ࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡼࡿࠥᕲ").format(e))
  def bstack1lll1ll1lll_opy_(self):
    if self.bstack1lllllll11_opy_:
      return
    try:
      bstack1llll111l1l_opy_ = [platform[bstack111l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨᕳ")].lower() for platform in self.config.get(bstack111l1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧᕴ"), [])]
      bstack1llll111lll_opy_ = sys.maxsize
      bstack1lll1ll11ll_opy_ = bstack111l1_opy_ (u"ࠬ࠭ᕵ")
      for browser in bstack1llll111l1l_opy_:
        if browser in self.bstack1lll1lll1ll_opy_:
          bstack1llll1lll1l_opy_ = self.bstack1lll1lll1ll_opy_[browser]
        if bstack1llll1lll1l_opy_ < bstack1llll111lll_opy_:
          bstack1llll111lll_opy_ = bstack1llll1lll1l_opy_
          bstack1lll1ll11ll_opy_ = browser
      return bstack1lll1ll11ll_opy_
    except Exception as e:
      self.logger.error(bstack111l1_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡩ࡭ࡳࡪࠠࡣࡧࡶࡸࠥࡶ࡬ࡢࡶࡩࡳࡷࡳࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࢀࢃࠢᕶ").format(e))
  @classmethod
  def bstack1l1ll1l1_opy_(self):
    return os.getenv(bstack111l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡆࡔࡆ࡝ࠬᕷ"), bstack111l1_opy_ (u"ࠨࡈࡤࡰࡸ࡫ࠧᕸ")).lower()
  @classmethod
  def bstack11llll11_opy_(self):
    return os.getenv(bstack111l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡈࡖࡈ࡟࡟ࡄࡃࡓࡘ࡚ࡘࡅࡠࡏࡒࡈࡊ࠭ᕹ"), bstack111l1_opy_ (u"ࠪࠫᕺ"))