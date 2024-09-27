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
import sys
import logging
import tarfile
import io
import os
import requests
import re
from requests_toolbelt.multipart.encoder import MultipartEncoder
from bstack_utils.constants import bstack111l1lllll_opy_, bstack111ll111ll_opy_
import tempfile
import json
bstack1lllll1ll11_opy_ = os.path.join(tempfile.gettempdir(), bstack111l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡦࡨࡦࡺ࡭࠮࡭ࡱࡪࠫᒙ"))
def get_logger(name=__name__, level=None):
  logger = logging.getLogger(name)
  if level:
    logging.basicConfig(
      level=level,
      format=bstack111l1_opy_ (u"ࠪࡠࡳࠫࠨࡢࡵࡦࡸ࡮ࡳࡥࠪࡵࠣ࡟ࠪ࠮࡮ࡢ࡯ࡨ࠭ࡸࡣ࡛ࠦࠪ࡯ࡩࡻ࡫࡬࡯ࡣࡰࡩ࠮ࡹ࡝ࠡ࠯ࠣࠩ࠭ࡳࡥࡴࡵࡤ࡫ࡪ࠯ࡳࠨᒚ"),
      datefmt=bstack111l1_opy_ (u"ࠫࠪࡎ࠺ࠦࡏ࠽ࠩࡘ࠭ᒛ"),
      stream=sys.stdout
    )
  return logger
def bstack1lllll1llll_opy_():
  global bstack1lllll1ll11_opy_
  if os.path.exists(bstack1lllll1ll11_opy_):
    os.remove(bstack1lllll1ll11_opy_)
def bstack1l111llll1_opy_():
  for handler in logging.getLogger().handlers:
    logging.getLogger().removeHandler(handler)
def bstack1l11ll11ll_opy_(config, log_level):
  bstack1lllllll11l_opy_ = log_level
  if bstack111l1_opy_ (u"ࠬࡲ࡯ࡨࡎࡨࡺࡪࡲࠧᒜ") in config and config[bstack111l1_opy_ (u"࠭࡬ࡰࡩࡏࡩࡻ࡫࡬ࠨᒝ")] in bstack111l1lllll_opy_:
    bstack1lllllll11l_opy_ = bstack111l1lllll_opy_[config[bstack111l1_opy_ (u"ࠧ࡭ࡱࡪࡐࡪࡼࡥ࡭ࠩᒞ")]]
  if config.get(bstack111l1_opy_ (u"ࠨࡦ࡬ࡷࡦࡨ࡬ࡦࡃࡸࡸࡴࡉࡡࡱࡶࡸࡶࡪࡒ࡯ࡨࡵࠪᒟ"), False):
    logging.getLogger().setLevel(bstack1lllllll11l_opy_)
    return bstack1lllllll11l_opy_
  global bstack1lllll1ll11_opy_
  bstack1l111llll1_opy_()
  bstack1llllll1lll_opy_ = logging.Formatter(
    fmt=bstack111l1_opy_ (u"ࠩ࡟ࡲࠪ࠮ࡡࡴࡥࡷ࡭ࡲ࡫ࠩࡴࠢ࡞ࠩ࠭ࡴࡡ࡮ࡧࠬࡷࡢࡡࠥࠩ࡮ࡨࡺࡪࡲ࡮ࡢ࡯ࡨ࠭ࡸࡣࠠ࠮ࠢࠨࠬࡲ࡫ࡳࡴࡣࡪࡩ࠮ࡹࠧᒠ"),
    datefmt=bstack111l1_opy_ (u"ࠪࠩࡍࡀࠥࡎ࠼ࠨࡗࠬᒡ")
  )
  bstack1llllll1l11_opy_ = logging.StreamHandler(sys.stdout)
  file_handler = logging.FileHandler(bstack1lllll1ll11_opy_)
  file_handler.setFormatter(bstack1llllll1lll_opy_)
  bstack1llllll1l11_opy_.setFormatter(bstack1llllll1lll_opy_)
  file_handler.setLevel(logging.DEBUG)
  bstack1llllll1l11_opy_.setLevel(log_level)
  file_handler.addFilter(lambda r: r.name != bstack111l1_opy_ (u"ࠫࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࠴ࡷࡦࡤࡧࡶ࡮ࡼࡥࡳ࠰ࡵࡩࡲࡵࡴࡦ࠰ࡵࡩࡲࡵࡴࡦࡡࡦࡳࡳࡴࡥࡤࡶ࡬ࡳࡳ࠭ᒢ"))
  logging.getLogger().setLevel(logging.DEBUG)
  bstack1llllll1l11_opy_.setLevel(bstack1lllllll11l_opy_)
  logging.getLogger().addHandler(bstack1llllll1l11_opy_)
  logging.getLogger().addHandler(file_handler)
  return bstack1lllllll11l_opy_
def bstack1lllll1lll1_opy_(config):
  try:
    bstack1lllllll111_opy_ = set(bstack111ll111ll_opy_)
    bstack1llllll1111_opy_ = bstack111l1_opy_ (u"ࠬ࠭ᒣ")
    with open(bstack111l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡿ࡭࡭ࠩᒤ")) as bstack1lllll1ll1l_opy_:
      bstack1llllll11l1_opy_ = bstack1lllll1ll1l_opy_.read()
      bstack1llllll1111_opy_ = re.sub(bstack111l1_opy_ (u"ࡲࠨࡠࠫࡠࡸ࠱ࠩࡀࠥ࠱࠮ࠩࡢ࡮ࠨᒥ"), bstack111l1_opy_ (u"ࠨࠩᒦ"), bstack1llllll11l1_opy_, flags=re.M)
      bstack1llllll1111_opy_ = re.sub(
        bstack111l1_opy_ (u"ࡴࠪࡢ࠭ࡢࡳࠬࠫࡂࠬࠬᒧ") + bstack111l1_opy_ (u"ࠪࢀࠬᒨ").join(bstack1lllllll111_opy_) + bstack111l1_opy_ (u"ࠫ࠮࠴ࠪࠥࠩᒩ"),
        bstack111l1_opy_ (u"ࡷ࠭࡜࠳࠼ࠣ࡟ࡗࡋࡄࡂࡅࡗࡉࡉࡣࠧᒪ"),
        bstack1llllll1111_opy_, flags=re.M | re.I
      )
    def bstack1llllll11ll_opy_(dic):
      bstack1llllll1l1l_opy_ = {}
      for key, value in dic.items():
        if key in bstack1lllllll111_opy_:
          bstack1llllll1l1l_opy_[key] = bstack111l1_opy_ (u"࡛࠭ࡓࡇࡇࡅࡈ࡚ࡅࡅ࡟ࠪᒫ")
        else:
          if isinstance(value, dict):
            bstack1llllll1l1l_opy_[key] = bstack1llllll11ll_opy_(value)
          else:
            bstack1llllll1l1l_opy_[key] = value
      return bstack1llllll1l1l_opy_
    bstack1llllll1l1l_opy_ = bstack1llllll11ll_opy_(config)
    return {
      bstack111l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡹ࡮࡮ࠪᒬ"): bstack1llllll1111_opy_,
      bstack111l1_opy_ (u"ࠨࡨ࡬ࡲࡦࡲࡣࡰࡰࡩ࡭࡬࠴ࡪࡴࡱࡱࠫᒭ"): json.dumps(bstack1llllll1l1l_opy_)
    }
  except Exception as e:
    return {}
def bstack1111l111_opy_(config):
  global bstack1lllll1ll11_opy_
  try:
    if config.get(bstack111l1_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧࡄࡹࡹࡵࡃࡢࡲࡷࡹࡷ࡫ࡌࡰࡩࡶࠫᒮ"), False):
      return
    uuid = os.getenv(bstack111l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨᒯ"))
    if not uuid or uuid == bstack111l1_opy_ (u"ࠫࡳࡻ࡬࡭ࠩᒰ"):
      return
    bstack1llllll111l_opy_ = [bstack111l1_opy_ (u"ࠬࡸࡥࡲࡷ࡬ࡶࡪࡳࡥ࡯ࡶࡶ࠲ࡹࡾࡴࠨᒱ"), bstack111l1_opy_ (u"࠭ࡐࡪࡲࡩ࡭ࡱ࡫ࠧᒲ"), bstack111l1_opy_ (u"ࠧࡱࡻࡳࡶࡴࡰࡥࡤࡶ࠱ࡸࡴࡳ࡬ࠨᒳ"), bstack1lllll1ll11_opy_]
    bstack1l111llll1_opy_()
    logging.shutdown()
    output_file = os.path.join(tempfile.gettempdir(), bstack111l1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠮࡮ࡲ࡫ࡸ࠳ࠧᒴ") + uuid + bstack111l1_opy_ (u"ࠩ࠱ࡸࡦࡸ࠮ࡨࡼࠪᒵ"))
    with tarfile.open(output_file, bstack111l1_opy_ (u"ࠥࡻ࠿࡭ࡺࠣᒶ")) as archive:
      for file in filter(lambda f: os.path.exists(f), bstack1llllll111l_opy_):
        try:
          archive.add(file,  arcname=os.path.basename(file))
        except:
          pass
      for name, data in bstack1lllll1lll1_opy_(config).items():
        tarinfo = tarfile.TarInfo(name)
        bstack1llllll1ll1_opy_ = data.encode()
        tarinfo.size = len(bstack1llllll1ll1_opy_)
        archive.addfile(tarinfo, io.BytesIO(bstack1llllll1ll1_opy_))
    bstack1ll111ll1l_opy_ = MultipartEncoder(
      fields= {
        bstack111l1_opy_ (u"ࠫࡩࡧࡴࡢࠩᒷ"): (os.path.basename(output_file), open(os.path.abspath(output_file), bstack111l1_opy_ (u"ࠬࡸࡢࠨᒸ")), bstack111l1_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳ࡽ࠳ࡧࡻ࡫ࡳࠫᒹ")),
        bstack111l1_opy_ (u"ࠧࡤ࡮࡬ࡩࡳࡺࡂࡶ࡫࡯ࡨ࡚ࡻࡩࡥࠩᒺ"): uuid
      }
    )
    response = requests.post(
      bstack111l1_opy_ (u"ࠣࡪࡷࡸࡵࡹ࠺࠰࠱ࡸࡴࡱࡵࡡࡥ࠯ࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡩ࡬ࡪࡧࡱࡸ࠲ࡲ࡯ࡨࡵ࠲ࡹࡵࡲ࡯ࡢࡦࠥᒻ"),
      data=bstack1ll111ll1l_opy_,
      headers={bstack111l1_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡘࡾࡶࡥࠨᒼ"): bstack1ll111ll1l_opy_.content_type},
      auth=(config[bstack111l1_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬᒽ")], config[bstack111l1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧᒾ")])
    )
    os.remove(output_file)
    if response.status_code != 200:
      get_logger().debug(bstack111l1_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤࡺࡶ࡬ࡰࡣࡧࠤࡱࡵࡧࡴ࠼ࠣࠫᒿ") + response.status_code)
  except Exception as e:
    get_logger().debug(bstack111l1_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡹࡥ࡯ࡦ࡬ࡲ࡬ࠦ࡬ࡰࡩࡶ࠾ࠬᓀ") + str(e))
  finally:
    try:
      bstack1lllll1llll_opy_()
    except:
      pass