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
import datetime
import inspect
import logging
import os
import signal
import threading
from uuid import uuid4
from bstack_utils.percy_sdk import PercySDK
import tempfile
import pytest
from packaging import version
from browserstack_sdk.__init__ import (bstack1l11l111ll_opy_, bstack11l11l1l_opy_, update, bstack1lll1ll1l1_opy_,
                                       bstack11111ll1l_opy_, bstack111ll1lll_opy_, bstack1l1ll1l1ll_opy_, bstack111111111_opy_,
                                       bstack1ll111ll11_opy_, bstack111ll1ll1_opy_, bstack1ll11l11l_opy_, bstack111111l11_opy_,
                                       bstack1l1ll1l11_opy_, getAccessibilityResults, getAccessibilityResultsSummary, perform_scan, bstack1ll11111_opy_)
from browserstack_sdk.bstack1l1lll11l_opy_ import bstack1l1lllllll_opy_
from browserstack_sdk._version import __version__
from bstack_utils import bstack1l1ll1111_opy_
from bstack_utils.capture import bstack11lll1lll1_opy_
from bstack_utils.config import Config
from bstack_utils.percy import *
from bstack_utils.constants import bstack1l1111ll1l_opy_, bstack1l11ll1l1_opy_, bstack1l11llll11_opy_, \
    bstack111l1l111_opy_
from bstack_utils.helper import bstack11l1ll1l1_opy_, bstack111111l1l1_opy_, bstack11ll1lll1l_opy_, bstack1l1llll1ll_opy_, bstack1111ll1ll1_opy_, bstack11l1l11l1_opy_, \
    bstack1111l11l11_opy_, \
    bstack111l1lll11_opy_, bstack1l1l11l1ll_opy_, bstack1l1ll11ll1_opy_, bstack111l1ll111_opy_, bstack1ll1l1ll_opy_, Notset, \
    bstack1l1lll1111_opy_, bstack11111llll1_opy_, bstack1111l1l111_opy_, Result, bstack111l1lll1l_opy_, bstack111l11ll1l_opy_, bstack11ll1ll111_opy_, \
    bstack1l11lll111_opy_, bstack1l11lllll_opy_, bstack1ll11llll1_opy_, bstack1111llllll_opy_
from bstack_utils.bstack111111l111_opy_ import bstack1111111ll1_opy_
from bstack_utils.messages import bstack1l111111_opy_, bstack11llll11l_opy_, bstack1llllll11_opy_, bstack1l11ll11l1_opy_, bstack1llll1l11l_opy_, \
    bstack1ll1111lll_opy_, bstack1l11l1ll1_opy_, bstack1l1llll111_opy_, bstack1l111l11_opy_, bstack1l1ll11l11_opy_, \
    bstack1ll111111_opy_, bstack1l11111111_opy_
from bstack_utils.proxy import bstack1l11l1ll1l_opy_, bstack1l11llll_opy_
from bstack_utils.bstack11lll1ll1_opy_ import bstack1lll11l1ll1_opy_, bstack1lll11ll111_opy_, bstack1lll11l11ll_opy_, bstack1lll11l111l_opy_, \
    bstack1lll11ll1l1_opy_, bstack1lll11l1l11_opy_, bstack1lll11l1111_opy_, bstack1ll11l111_opy_, bstack1lll11ll11l_opy_
from bstack_utils.bstack1ll1lll1l1_opy_ import bstack1llll1ll11_opy_
from bstack_utils.bstack1l1llll11l_opy_ import bstack11llll1l_opy_, bstack1l1ll111_opy_, bstack1111lll1l_opy_, \
    bstack1lll1111l1_opy_, bstack11ll111ll_opy_
from bstack_utils.bstack11lll1ll11_opy_ import bstack11lll11l11_opy_
from bstack_utils.bstack1l11l1l1ll_opy_ import bstack1lll1l11_opy_
import bstack_utils.bstack1ll1l111_opy_ as bstack1ll111111l_opy_
from bstack_utils.bstack11111l1l_opy_ import bstack11llllll11_opy_
from bstack_utils.bstack1lll11l1_opy_ import bstack1lll11l1_opy_
bstack1llll1lll1_opy_ = None
bstack1lll1l1l1l_opy_ = None
bstack1l1lll1l1_opy_ = None
bstack1l111lll1l_opy_ = None
bstack1ll11ll1_opy_ = None
bstack1l1l1ll11_opy_ = None
bstack1l11l11ll1_opy_ = None
bstack1ll1ll1l_opy_ = None
bstack1l1lll1l11_opy_ = None
bstack1ll1ll1lll_opy_ = None
bstack1l111l11l_opy_ = None
bstack1l1l111l11_opy_ = None
bstack1l111111l_opy_ = None
bstack1l111l1l_opy_ = bstack111l1_opy_ (u"ࠪࠫណ")
CONFIG = {}
bstack1l111ll111_opy_ = False
bstack11l1l111l_opy_ = bstack111l1_opy_ (u"ࠫࠬត")
bstack1111l1ll1_opy_ = bstack111l1_opy_ (u"ࠬ࠭ថ")
bstack1ll11l1l_opy_ = False
bstack1l1ll1l1l_opy_ = []
bstack1llllll1l_opy_ = bstack1l1111ll1l_opy_
bstack1ll111l1lll_opy_ = bstack111l1_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ទ")
bstack1ll11l1ll1l_opy_ = False
bstack1l111lll1_opy_ = {}
bstack11l11ll1_opy_ = False
logger = bstack1l1ll1111_opy_.get_logger(__name__, bstack1llllll1l_opy_)
store = {
    bstack111l1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫធ"): []
}
bstack1ll11l1l1ll_opy_ = False
try:
    from playwright.sync_api import (
        BrowserContext,
        Page
    )
except:
    pass
import json
_11l1lll1ll_opy_ = {}
current_test_uuid = None
def bstack1ll1llll11_opy_(page, bstack1lll1l11l1_opy_):
    try:
        page.evaluate(bstack111l1_opy_ (u"ࠣࡡࠣࡁࡃࠦࡻࡾࠤន"),
                      bstack111l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨ࡮ࡢ࡯ࡨࠦ࠿࠭ប") + json.dumps(
                          bstack1lll1l11l1_opy_) + bstack111l1_opy_ (u"ࠥࢁࢂࠨផ"))
    except Exception as e:
        print(bstack111l1_opy_ (u"ࠦࡪࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡰࡤࡱࡪࠦࡻࡾࠤព"), e)
def bstack1l1l11l1l1_opy_(page, message, level):
    try:
        page.evaluate(bstack111l1_opy_ (u"ࠧࡥࠠ࠾ࡀࠣࡿࢂࠨភ"), bstack111l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡩࡧࡴࡢࠤ࠽ࠫម") + json.dumps(
            message) + bstack111l1_opy_ (u"ࠧ࠭ࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠪយ") + json.dumps(level) + bstack111l1_opy_ (u"ࠨࡿࢀࠫរ"))
    except Exception as e:
        print(bstack111l1_opy_ (u"ࠤࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡧ࡮࡯ࡱࡷࡥࡹ࡯࡯࡯ࠢࡾࢁࠧល"), e)
def pytest_configure(config):
    bstack1111ll1l1_opy_ = Config.bstack1l1ll11lll_opy_()
    config.args = bstack1lll1l11_opy_.bstack1ll11ll1lll_opy_(config.args)
    bstack1111ll1l1_opy_.bstack1lll1l1l_opy_(bstack1ll11llll1_opy_(config.getoption(bstack111l1_opy_ (u"ࠪࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠧវ"))))
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    bstack1ll11ll1ll1_opy_ = item.config.getoption(bstack111l1_opy_ (u"ࠫࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ឝ"))
    plugins = item.config.getoption(bstack111l1_opy_ (u"ࠧࡶ࡬ࡶࡩ࡬ࡲࡸࠨឞ"))
    report = outcome.get_result()
    bstack1ll11l1l1l1_opy_(item, call, report)
    if bstack111l1_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹࡥࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡵࡲࡵࡨ࡫ࡱࠦស") not in plugins or bstack1ll1l1ll_opy_():
        return
    summary = []
    driver = getattr(item, bstack111l1_opy_ (u"ࠢࡠࡦࡵ࡭ࡻ࡫ࡲࠣហ"), None)
    page = getattr(item, bstack111l1_opy_ (u"ࠣࡡࡳࡥ࡬࡫ࠢឡ"), None)
    try:
        if (driver == None):
            driver = threading.current_thread().bstackSessionDriver
    except:
        pass
    item._driver = driver
    if (driver is not None):
        bstack1ll11l1l11l_opy_(item, report, summary, bstack1ll11ll1ll1_opy_)
    if (page is not None):
        bstack1ll11l1lll1_opy_(item, report, summary, bstack1ll11ll1ll1_opy_)
def bstack1ll11l1l11l_opy_(item, report, summary, bstack1ll11ll1ll1_opy_):
    if report.when == bstack111l1_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨអ") and report.skipped:
        bstack1lll11ll11l_opy_(report)
    if report.when in [bstack111l1_opy_ (u"ࠥࡷࡪࡺࡵࡱࠤឣ"), bstack111l1_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࠨឤ")]:
        return
    if not bstack1111ll1ll1_opy_():
        return
    try:
        if (str(bstack1ll11ll1ll1_opy_).lower() != bstack111l1_opy_ (u"ࠬࡺࡲࡶࡧࠪឥ")):
            item._driver.execute_script(
                bstack111l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡲࡦࡳࡥࠣ࠼ࠣࠫឦ") + json.dumps(
                    report.nodeid) + bstack111l1_opy_ (u"ࠧࡾࡿࠪឧ"))
        os.environ[bstack111l1_opy_ (u"ࠨࡒ࡜ࡘࡊ࡙ࡔࡠࡖࡈࡗ࡙ࡥࡎࡂࡏࡈࠫឨ")] = report.nodeid
    except Exception as e:
        summary.append(
            bstack111l1_opy_ (u"ࠤ࡚ࡅࡗࡔࡉࡏࡉ࠽ࠤࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠ࡮ࡣࡵ࡯ࠥࡹࡥࡴࡵ࡬ࡳࡳࠦ࡮ࡢ࡯ࡨ࠾ࠥࢁ࠰ࡾࠤឩ").format(e)
        )
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack111l1_opy_ (u"ࠥࡻࡦࡹࡸࡧࡣ࡬ࡰࠧឪ")))
    bstack1ll11l1l1l_opy_ = bstack111l1_opy_ (u"ࠦࠧឫ")
    bstack1lll11ll11l_opy_(report)
    if not passed:
        try:
            bstack1ll11l1l1l_opy_ = report.longrepr.reprcrash
        except Exception as e:
            summary.append(
                bstack111l1_opy_ (u"ࠧ࡝ࡁࡓࡐࡌࡒࡌࡀࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡨࡪࡺࡥࡳ࡯࡬ࡲࡪࠦࡦࡢ࡫࡯ࡹࡷ࡫ࠠࡳࡧࡤࡷࡴࡴ࠺ࠡࡽ࠳ࢁࠧឬ").format(e)
            )
        try:
            if (threading.current_thread().bstackTestErrorMessages == None):
                threading.current_thread().bstackTestErrorMessages = []
        except Exception as e:
            threading.current_thread().bstackTestErrorMessages = []
        threading.current_thread().bstackTestErrorMessages.append(str(bstack1ll11l1l1l_opy_))
    if not report.skipped:
        passed = report.passed or (report.failed and hasattr(report, bstack111l1_opy_ (u"ࠨࡷࡢࡵࡻࡪࡦ࡯࡬ࠣឭ")))
        bstack1ll11l1l1l_opy_ = bstack111l1_opy_ (u"ࠢࠣឮ")
        if not passed:
            try:
                bstack1ll11l1l1l_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack111l1_opy_ (u"࡙ࠣࡄࡖࡓࡏࡎࡈ࠼ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡤࡦࡶࡨࡶࡲ࡯࡮ࡦࠢࡩࡥ࡮ࡲࡵࡳࡧࠣࡶࡪࡧࡳࡰࡰ࠽ࠤࢀ࠶ࡽࠣឯ").format(e)
                )
            try:
                if (threading.current_thread().bstackTestErrorMessages == None):
                    threading.current_thread().bstackTestErrorMessages = []
            except Exception as e:
                threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(str(bstack1ll11l1l1l_opy_))
        try:
            if passed:
                item._driver.execute_script(
                    bstack111l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡰࡪࡼࡥ࡭ࠤ࠽ࠤࠧ࡯࡮ࡧࡱࠥ࠰ࠥࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࡪࡡࡵࡣࠥ࠾ࠥ࠭ឰ")
                    + json.dumps(bstack111l1_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠤࠦឱ"))
                    + bstack111l1_opy_ (u"ࠦࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡽ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࢃࠢឲ")
                )
            else:
                item._driver.execute_script(
                    bstack111l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ࠯ࠤࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠨ࡬ࡦࡸࡨࡰࠧࡀࠠࠣࡧࡵࡶࡴࡸࠢ࠭ࠢ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤࡧࡥࡹࡧࠢ࠻ࠢࠪឳ")
                    + json.dumps(str(bstack1ll11l1l1l_opy_))
                    + bstack111l1_opy_ (u"ࠨ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡿ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡾࠤ឴")
                )
        except Exception as e:
            summary.append(bstack111l1_opy_ (u"ࠢࡘࡃࡕࡒࡎࡔࡇ࠻ࠢࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡧ࡮࡯ࡱࡷࡥࡹ࡫࠺ࠡࡽ࠳ࢁࠧ឵").format(e))
def bstack1ll11ll1111_opy_(test_name, error_message):
    try:
        bstack1ll11l111ll_opy_ = []
        bstack1l111lll11_opy_ = os.environ.get(bstack111l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨា"), bstack111l1_opy_ (u"ࠩ࠳ࠫិ"))
        bstack1111ll11_opy_ = {bstack111l1_opy_ (u"ࠪࡲࡦࡳࡥࠨី"): test_name, bstack111l1_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪឹ"): error_message, bstack111l1_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫឺ"): bstack1l111lll11_opy_}
        bstack1ll111lll1l_opy_ = os.path.join(tempfile.gettempdir(), bstack111l1_opy_ (u"࠭ࡰࡸࡡࡳࡽࡹ࡫ࡳࡵࡡࡨࡶࡷࡵࡲࡠ࡮࡬ࡷࡹ࠴ࡪࡴࡱࡱࠫុ"))
        if os.path.exists(bstack1ll111lll1l_opy_):
            with open(bstack1ll111lll1l_opy_) as f:
                bstack1ll11l111ll_opy_ = json.load(f)
        bstack1ll11l111ll_opy_.append(bstack1111ll11_opy_)
        with open(bstack1ll111lll1l_opy_, bstack111l1_opy_ (u"ࠧࡸࠩូ")) as f:
            json.dump(bstack1ll11l111ll_opy_, f)
    except Exception as e:
        logger.debug(bstack111l1_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡴࡪࡸࡳࡪࡵࡷ࡭ࡳ࡭ࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡵࡿࡴࡦࡵࡷࠤࡪࡸࡲࡰࡴࡶ࠾ࠥ࠭ួ") + str(e))
def bstack1ll11l1lll1_opy_(item, report, summary, bstack1ll11ll1ll1_opy_):
    if report.when in [bstack111l1_opy_ (u"ࠤࡶࡩࡹࡻࡰࠣើ"), bstack111l1_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࠧឿ")]:
        return
    if (str(bstack1ll11ll1ll1_opy_).lower() != bstack111l1_opy_ (u"ࠫࡹࡸࡵࡦࠩៀ")):
        bstack1ll1llll11_opy_(item._page, report.nodeid)
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack111l1_opy_ (u"ࠧࡽࡡࡴࡺࡩࡥ࡮ࡲࠢេ")))
    bstack1ll11l1l1l_opy_ = bstack111l1_opy_ (u"ࠨࠢែ")
    bstack1lll11ll11l_opy_(report)
    if not report.skipped:
        if not passed:
            try:
                bstack1ll11l1l1l_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack111l1_opy_ (u"ࠢࡘࡃࡕࡒࡎࡔࡇ࠻ࠢࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡪࡥࡵࡧࡵࡱ࡮ࡴࡥࠡࡨࡤ࡭ࡱࡻࡲࡦࠢࡵࡩࡦࡹ࡯࡯࠼ࠣࡿ࠵ࢃࠢៃ").format(e)
                )
        try:
            if passed:
                bstack11ll111ll_opy_(getattr(item, bstack111l1_opy_ (u"ࠨࡡࡳࡥ࡬࡫ࠧោ"), None), bstack111l1_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠤៅ"))
            else:
                error_message = bstack111l1_opy_ (u"ࠪࠫំ")
                if bstack1ll11l1l1l_opy_:
                    bstack1l1l11l1l1_opy_(item._page, str(bstack1ll11l1l1l_opy_), bstack111l1_opy_ (u"ࠦࡪࡸࡲࡰࡴࠥះ"))
                    bstack11ll111ll_opy_(getattr(item, bstack111l1_opy_ (u"ࠬࡥࡰࡢࡩࡨࠫៈ"), None), bstack111l1_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨ៉"), str(bstack1ll11l1l1l_opy_))
                    error_message = str(bstack1ll11l1l1l_opy_)
                else:
                    bstack11ll111ll_opy_(getattr(item, bstack111l1_opy_ (u"ࠧࡠࡲࡤ࡫ࡪ࠭៊"), None), bstack111l1_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣ់"))
                bstack1ll11ll1111_opy_(report.nodeid, error_message)
        except Exception as e:
            summary.append(bstack111l1_opy_ (u"ࠤ࡚ࡅࡗࡔࡉࡏࡉ࠽ࠤࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡶࡲࡧࡥࡹ࡫ࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡵࡷࡥࡹࡻࡳ࠻ࠢࡾ࠴ࢂࠨ៌").format(e))
try:
    from typing import Generator
    import pytest_playwright.pytest_playwright as p
    @pytest.fixture
    def page(context: BrowserContext, request: pytest.FixtureRequest) -> Generator[Page, None, None]:
        page = context.new_page()
        request.node._page = page
        yield page
except:
    pass
def pytest_addoption(parser):
    parser.addoption(bstack111l1_opy_ (u"ࠥ࠱࠲ࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢ៍"), default=bstack111l1_opy_ (u"ࠦࡋࡧ࡬ࡴࡧࠥ៎"), help=bstack111l1_opy_ (u"ࠧࡇࡵࡵࡱࡰࡥࡹ࡯ࡣࠡࡵࡨࡸࠥࡹࡥࡴࡵ࡬ࡳࡳࠦ࡮ࡢ࡯ࡨࠦ៏"))
    parser.addoption(bstack111l1_opy_ (u"ࠨ࠭࠮ࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠧ័"), default=bstack111l1_opy_ (u"ࠢࡇࡣ࡯ࡷࡪࠨ៑"), help=bstack111l1_opy_ (u"ࠣࡃࡸࡸࡴࡳࡡࡵ࡫ࡦࠤࡸ࡫ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡱࡥࡲ࡫្ࠢ"))
    try:
        import pytest_selenium.pytest_selenium
    except:
        parser.addoption(bstack111l1_opy_ (u"ࠤ࠰࠱ࡩࡸࡩࡷࡧࡵࠦ៓"), action=bstack111l1_opy_ (u"ࠥࡷࡹࡵࡲࡦࠤ។"), default=bstack111l1_opy_ (u"ࠦࡨ࡮ࡲࡰ࡯ࡨࠦ៕"),
                         help=bstack111l1_opy_ (u"ࠧࡊࡲࡪࡸࡨࡶࠥࡺ࡯ࠡࡴࡸࡲࠥࡺࡥࡴࡶࡶࠦ៖"))
def bstack11llll11l1_opy_(log):
    if not (log[bstack111l1_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧៗ")] and log[bstack111l1_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ៘")].strip()):
        return
    active = bstack11lll1l1ll_opy_()
    log = {
        bstack111l1_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧ៙"): log[bstack111l1_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨ៚")],
        bstack111l1_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭៛"): bstack11ll1lll1l_opy_().isoformat() + bstack111l1_opy_ (u"ࠫ࡟࠭ៜ"),
        bstack111l1_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭៝"): log[bstack111l1_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ៞")],
    }
    if active:
        if active[bstack111l1_opy_ (u"ࠧࡵࡻࡳࡩࠬ៟")] == bstack111l1_opy_ (u"ࠨࡪࡲࡳࡰ࠭០"):
            log[bstack111l1_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ១")] = active[bstack111l1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ២")]
        elif active[bstack111l1_opy_ (u"ࠫࡹࡿࡰࡦࠩ៣")] == bstack111l1_opy_ (u"ࠬࡺࡥࡴࡶࠪ៤"):
            log[bstack111l1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭៥")] = active[bstack111l1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ៦")]
    bstack11llllll11_opy_.bstack1111l111_opy_([log])
def bstack11lll1l1ll_opy_():
    if len(store[bstack111l1_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬ៧")]) > 0 and store[bstack111l1_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭៨")][-1]:
        return {
            bstack111l1_opy_ (u"ࠪࡸࡾࡶࡥࠨ៩"): bstack111l1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩ៪"),
            bstack111l1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ៫"): store[bstack111l1_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪ៬")][-1]
        }
    if store.get(bstack111l1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫ៭"), None):
        return {
            bstack111l1_opy_ (u"ࠨࡶࡼࡴࡪ࠭៮"): bstack111l1_opy_ (u"ࠩࡷࡩࡸࡺࠧ៯"),
            bstack111l1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ៰"): store[bstack111l1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨ៱")]
        }
    return None
bstack11lll1ll1l_opy_ = bstack11lll1lll1_opy_(bstack11llll11l1_opy_)
def pytest_runtest_call(item):
    try:
        global CONFIG
        global bstack1ll11l1ll1l_opy_
        item._1ll11l11111_opy_ = True
        bstack11llll1ll_opy_ = bstack1ll111111l_opy_.bstack1l1111l11_opy_(bstack111l1lll11_opy_(item.own_markers))
        item._a11y_test_case = bstack11llll1ll_opy_
        if bstack1ll11l1ll1l_opy_:
            driver = getattr(item, bstack111l1_opy_ (u"ࠬࡥࡤࡳ࡫ࡹࡩࡷ࠭៲"), None)
            item._a11y_started = bstack1ll111111l_opy_.bstack11lllll1_opy_(driver, bstack11llll1ll_opy_)
        if not bstack11llllll11_opy_.on() or bstack1ll111l1lll_opy_ != bstack111l1_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭៳"):
            return
        global current_test_uuid, bstack11lll1ll1l_opy_
        bstack11lll1ll1l_opy_.start()
        bstack11ll1lll11_opy_ = {
            bstack111l1_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ៴"): uuid4().__str__(),
            bstack111l1_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬ៵"): bstack11ll1lll1l_opy_().isoformat() + bstack111l1_opy_ (u"ࠩ࡝ࠫ៶")
        }
        current_test_uuid = bstack11ll1lll11_opy_[bstack111l1_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ៷")]
        store[bstack111l1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨ៸")] = bstack11ll1lll11_opy_[bstack111l1_opy_ (u"ࠬࡻࡵࡪࡦࠪ៹")]
        threading.current_thread().current_test_uuid = current_test_uuid
        _11l1lll1ll_opy_[item.nodeid] = {**_11l1lll1ll_opy_[item.nodeid], **bstack11ll1lll11_opy_}
        bstack1ll11l11lll_opy_(item, _11l1lll1ll_opy_[item.nodeid], bstack111l1_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧ៺"))
    except Exception as err:
        print(bstack111l1_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹࡥࡲࡶࡰࡷࡩࡸࡺ࡟ࡤࡣ࡯ࡰ࠿ࠦࡻࡾࠩ៻"), str(err))
def pytest_runtest_setup(item):
    global bstack1ll11l1l1ll_opy_
    threading.current_thread().percySessionName = item.nodeid
    if bstack111l1ll111_opy_():
        atexit.register(bstack1l1llll1_opy_)
        if not bstack1ll11l1l1ll_opy_:
            try:
                bstack1ll11ll111l_opy_ = [signal.SIGINT, signal.SIGTERM]
                if not bstack1111llllll_opy_():
                    bstack1ll11ll111l_opy_.extend([signal.SIGHUP, signal.SIGQUIT])
                for s in bstack1ll11ll111l_opy_:
                    signal.signal(s, bstack1ll111ll11l_opy_)
                bstack1ll11l1l1ll_opy_ = True
            except Exception as e:
                logger.debug(
                    bstack111l1_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡪࡰࠣࡶࡪ࡭ࡩࡴࡶࡨࡶࠥࡹࡩࡨࡰࡤࡰࠥ࡮ࡡ࡯ࡦ࡯ࡩࡷࡹ࠺ࠡࠤ៼") + str(e))
        try:
            item.config.hook.pytest_selenium_runtest_makereport = bstack1lll11l1ll1_opy_
        except Exception as err:
            threading.current_thread().testStatus = bstack111l1_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ៽")
    try:
        if not bstack11llllll11_opy_.on():
            return
        bstack11lll1ll1l_opy_.start()
        uuid = uuid4().__str__()
        bstack11ll1lll11_opy_ = {
            bstack111l1_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ៾"): uuid,
            bstack111l1_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨ៿"): bstack11ll1lll1l_opy_().isoformat() + bstack111l1_opy_ (u"ࠬࡠࠧ᠀"),
            bstack111l1_opy_ (u"࠭ࡴࡺࡲࡨࠫ᠁"): bstack111l1_opy_ (u"ࠧࡩࡱࡲ࡯ࠬ᠂"),
            bstack111l1_opy_ (u"ࠨࡪࡲࡳࡰࡥࡴࡺࡲࡨࠫ᠃"): bstack111l1_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡈࡅࡈࡎࠧ᠄"),
            bstack111l1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡰࡤࡱࡪ࠭᠅"): bstack111l1_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪ᠆")
        }
        threading.current_thread().current_hook_uuid = uuid
        threading.current_thread().current_test_item = item
        store[bstack111l1_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡺࡥ࡮ࠩ᠇")] = item
        store[bstack111l1_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪ᠈")] = [uuid]
        if not _11l1lll1ll_opy_.get(item.nodeid, None):
            _11l1lll1ll_opy_[item.nodeid] = {bstack111l1_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭᠉"): [], bstack111l1_opy_ (u"ࠨࡨ࡬ࡼࡹࡻࡲࡦࡵࠪ᠊"): []}
        _11l1lll1ll_opy_[item.nodeid][bstack111l1_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨ᠋")].append(bstack11ll1lll11_opy_[bstack111l1_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ᠌")])
        _11l1lll1ll_opy_[item.nodeid + bstack111l1_opy_ (u"ࠫ࠲ࡹࡥࡵࡷࡳࠫ᠍")] = bstack11ll1lll11_opy_
        bstack1ll11l111l1_opy_(item, bstack11ll1lll11_opy_, bstack111l1_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭᠎"))
    except Exception as err:
        print(bstack111l1_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸࡤࡸࡵ࡯ࡶࡨࡷࡹࡥࡳࡦࡶࡸࡴ࠿ࠦࡻࡾࠩ᠏"), str(err))
def pytest_runtest_teardown(item):
    try:
        global bstack1l111lll1_opy_
        bstack1l111lll11_opy_ = 0
        if bstack1ll11l1l_opy_ is True:
            bstack1l111lll11_opy_ = int(os.environ.get(bstack111l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧ᠐")))
        if bstack1l11l111_opy_.bstack1l1ll1l1_opy_() == bstack111l1_opy_ (u"ࠣࡶࡵࡹࡪࠨ᠑"):
            if bstack1l11l111_opy_.bstack11llll11_opy_() == bstack111l1_opy_ (u"ࠤࡷࡩࡸࡺࡣࡢࡵࡨࠦ᠒"):
                bstack1ll11l11l11_opy_ = bstack11l1ll1l1_opy_(threading.current_thread(), bstack111l1_opy_ (u"ࠪࡴࡪࡸࡣࡺࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭᠓"), None)
                bstack111l11l11_opy_ = bstack1ll11l11l11_opy_ + bstack111l1_opy_ (u"ࠦ࠲ࡺࡥࡴࡶࡦࡥࡸ࡫ࠢ᠔")
                driver = getattr(item, bstack111l1_opy_ (u"ࠬࡥࡤࡳ࡫ࡹࡩࡷ࠭᠕"), None)
                bstack1ll11l1lll_opy_ = getattr(item, bstack111l1_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ᠖"), None)
                bstack1l1ll1l11l_opy_ = getattr(item, bstack111l1_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ᠗"), None)
                PercySDK.screenshot(driver, bstack111l11l11_opy_, bstack1ll11l1lll_opy_=bstack1ll11l1lll_opy_, bstack1l1ll1l11l_opy_=bstack1l1ll1l11l_opy_, bstack11l1lll1_opy_=bstack1l111lll11_opy_)
        if getattr(item, bstack111l1_opy_ (u"ࠨࡡࡤ࠵࠶ࡿ࡟ࡴࡶࡤࡶࡹ࡫ࡤࠨ᠘"), False):
            bstack1l1lllllll_opy_.bstack111l11ll1_opy_(getattr(item, bstack111l1_opy_ (u"ࠩࡢࡨࡷ࡯ࡶࡦࡴࠪ᠙"), None), bstack1l111lll1_opy_, logger, item)
        if not bstack11llllll11_opy_.on():
            return
        bstack11ll1lll11_opy_ = {
            bstack111l1_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ᠚"): uuid4().__str__(),
            bstack111l1_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨ᠛"): bstack11ll1lll1l_opy_().isoformat() + bstack111l1_opy_ (u"ࠬࡠࠧ᠜"),
            bstack111l1_opy_ (u"࠭ࡴࡺࡲࡨࠫ᠝"): bstack111l1_opy_ (u"ࠧࡩࡱࡲ࡯ࠬ᠞"),
            bstack111l1_opy_ (u"ࠨࡪࡲࡳࡰࡥࡴࡺࡲࡨࠫ᠟"): bstack111l1_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡇࡄࡇࡍ࠭ᠠ"),
            bstack111l1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡰࡤࡱࡪ࠭ᠡ"): bstack111l1_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭ᠢ")
        }
        _11l1lll1ll_opy_[item.nodeid + bstack111l1_opy_ (u"ࠬ࠳ࡴࡦࡣࡵࡨࡴࡽ࡮ࠨᠣ")] = bstack11ll1lll11_opy_
        bstack1ll11l111l1_opy_(item, bstack11ll1lll11_opy_, bstack111l1_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧᠤ"))
    except Exception as err:
        print(bstack111l1_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹࡥࡲࡶࡰࡷࡩࡸࡺ࡟ࡵࡧࡤࡶࡩࡵࡷ࡯࠼ࠣࡿࢂ࠭ᠥ"), str(err))
@pytest.hookimpl(hookwrapper=True)
def pytest_fixture_setup(fixturedef, request):
    if not bstack11llllll11_opy_.on():
        yield
        return
    start_time = datetime.datetime.now()
    if bstack1lll11l111l_opy_(fixturedef.argname):
        store[bstack111l1_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡰࡳࡩࡻ࡬ࡦࡡ࡬ࡸࡪࡳࠧᠦ")] = request.node
    elif bstack1lll11ll1l1_opy_(fixturedef.argname):
        store[bstack111l1_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡧࡱࡧࡳࡴࡡ࡬ࡸࡪࡳࠧᠧ")] = request.node
    outcome = yield
    try:
        fixture = {
            bstack111l1_opy_ (u"ࠪࡲࡦࡳࡥࠨᠨ"): fixturedef.argname,
            bstack111l1_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫᠩ"): bstack1111l11l11_opy_(outcome),
            bstack111l1_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴࠧᠪ"): (datetime.datetime.now() - start_time).total_seconds() * 1000
        }
        current_test_item = store[bstack111l1_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡴࡦ࡯ࠪᠫ")]
        if not _11l1lll1ll_opy_.get(current_test_item.nodeid, None):
            _11l1lll1ll_opy_[current_test_item.nodeid] = {bstack111l1_opy_ (u"ࠧࡧ࡫ࡻࡸࡺࡸࡥࡴࠩᠬ"): []}
        _11l1lll1ll_opy_[current_test_item.nodeid][bstack111l1_opy_ (u"ࠨࡨ࡬ࡼࡹࡻࡲࡦࡵࠪᠭ")].append(fixture)
    except Exception as err:
        logger.debug(bstack111l1_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡼࡸࡪࡹࡴࡠࡨ࡬ࡼࡹࡻࡲࡦࡡࡶࡩࡹࡻࡰ࠻ࠢࡾࢁࠬᠮ"), str(err))
if bstack1ll1l1ll_opy_() and bstack11llllll11_opy_.on():
    def pytest_bdd_before_step(request, step):
        try:
            _11l1lll1ll_opy_[request.node.nodeid][bstack111l1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ᠯ")].bstack1ll1l111l1_opy_(id(step))
        except Exception as err:
            print(bstack111l1_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶࡢࡦࡩࡪ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡴࡶࡨࡴ࠿ࠦࡻࡾࠩᠰ"), str(err))
    def pytest_bdd_step_error(request, step, exception):
        try:
            _11l1lll1ll_opy_[request.node.nodeid][bstack111l1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨᠱ")].bstack11llll11ll_opy_(id(step), Result.failed(exception=exception))
        except Exception as err:
            print(bstack111l1_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸࡤࡨࡤࡥࡡࡶࡸࡪࡶ࡟ࡦࡴࡵࡳࡷࡀࠠࡼࡿࠪᠲ"), str(err))
    def pytest_bdd_after_step(request, step):
        try:
            bstack11lll1ll11_opy_: bstack11lll11l11_opy_ = _11l1lll1ll_opy_[request.node.nodeid][bstack111l1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪᠳ")]
            bstack11lll1ll11_opy_.bstack11llll11ll_opy_(id(step), Result.passed())
        except Exception as err:
            print(bstack111l1_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࡟ࡣࡦࡧࡣࡸࡺࡥࡱࡡࡨࡶࡷࡵࡲ࠻ࠢࡾࢁࠬᠴ"), str(err))
    def pytest_bdd_before_scenario(request, feature, scenario):
        global bstack1ll111l1lll_opy_
        try:
            if not bstack11llllll11_opy_.on() or bstack1ll111l1lll_opy_ != bstack111l1_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩ࠭ᠵ"):
                return
            global bstack11lll1ll1l_opy_
            bstack11lll1ll1l_opy_.start()
            driver = bstack11l1ll1l1_opy_(threading.current_thread(), bstack111l1_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩᠶ"), None)
            if not _11l1lll1ll_opy_.get(request.node.nodeid, None):
                _11l1lll1ll_opy_[request.node.nodeid] = {}
            bstack11lll1ll11_opy_ = bstack11lll11l11_opy_.bstack1ll1lll1111_opy_(
                scenario, feature, request.node,
                name=bstack1lll11l1l11_opy_(request.node, scenario),
                bstack11lll11ll1_opy_=bstack11l1l11l1_opy_(),
                file_path=feature.filename,
                scope=[feature.name],
                framework=bstack111l1_opy_ (u"ࠫࡕࡿࡴࡦࡵࡷ࠱ࡨࡻࡣࡶ࡯ࡥࡩࡷ࠭ᠷ"),
                tags=bstack1lll11l1111_opy_(feature, scenario),
                bstack11l1ll11l1_opy_=bstack11llllll11_opy_.bstack11l1llll11_opy_(driver) if driver and driver.session_id else {}
            )
            _11l1lll1ll_opy_[request.node.nodeid][bstack111l1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨᠸ")] = bstack11lll1ll11_opy_
            bstack1ll11l1ll11_opy_(bstack11lll1ll11_opy_.uuid)
            bstack11llllll11_opy_.bstack11lllll111_opy_(bstack111l1_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧᠹ"), bstack11lll1ll11_opy_)
        except Exception as err:
            print(bstack111l1_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹࡥࡢࡥࡦࡢࡦࡪ࡬࡯ࡳࡧࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳ࠿ࠦࡻࡾࠩᠺ"), str(err))
def bstack1ll111llll1_opy_(bstack11llll1111_opy_):
    if bstack11llll1111_opy_ in store[bstack111l1_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬᠻ")]:
        store[bstack111l1_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭ᠼ")].remove(bstack11llll1111_opy_)
def bstack1ll11l1ll11_opy_(bstack11llll1l1l_opy_):
    store[bstack111l1_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧᠽ")] = bstack11llll1l1l_opy_
    threading.current_thread().current_test_uuid = bstack11llll1l1l_opy_
@bstack11llllll11_opy_.bstack1ll1l11llll_opy_
def bstack1ll11l1l1l1_opy_(item, call, report):
    global bstack1ll111l1lll_opy_
    bstack1llll11ll1_opy_ = bstack11l1l11l1_opy_()
    if hasattr(report, bstack111l1_opy_ (u"ࠫࡸࡺ࡯ࡱࠩᠾ")):
        bstack1llll11ll1_opy_ = bstack111l1lll1l_opy_(report.stop)
    elif hasattr(report, bstack111l1_opy_ (u"ࠬࡹࡴࡢࡴࡷࠫᠿ")):
        bstack1llll11ll1_opy_ = bstack111l1lll1l_opy_(report.start)
    try:
        if getattr(report, bstack111l1_opy_ (u"࠭ࡷࡩࡧࡱࠫᡀ"), bstack111l1_opy_ (u"ࠧࠨᡁ")) == bstack111l1_opy_ (u"ࠨࡥࡤࡰࡱ࠭ᡂ"):
            bstack11lll1ll1l_opy_.reset()
        if getattr(report, bstack111l1_opy_ (u"ࠩࡺ࡬ࡪࡴࠧᡃ"), bstack111l1_opy_ (u"ࠪࠫᡄ")) == bstack111l1_opy_ (u"ࠫࡨࡧ࡬࡭ࠩᡅ"):
            if bstack1ll111l1lll_opy_ == bstack111l1_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬᡆ"):
                _11l1lll1ll_opy_[item.nodeid][bstack111l1_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫᡇ")] = bstack1llll11ll1_opy_
                bstack1ll11l11lll_opy_(item, _11l1lll1ll_opy_[item.nodeid], bstack111l1_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩᡈ"), report, call)
                store[bstack111l1_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬᡉ")] = None
            elif bstack1ll111l1lll_opy_ == bstack111l1_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠨᡊ"):
                bstack11lll1ll11_opy_ = _11l1lll1ll_opy_[item.nodeid][bstack111l1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ᡋ")]
                bstack11lll1ll11_opy_.set(hooks=_11l1lll1ll_opy_[item.nodeid].get(bstack111l1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪᡌ"), []))
                exception, bstack11lll111l1_opy_ = None, None
                if call.excinfo:
                    exception = call.excinfo.value
                    bstack11lll111l1_opy_ = [call.excinfo.exconly(), getattr(report, bstack111l1_opy_ (u"ࠬࡲ࡯࡯ࡩࡵࡩࡵࡸࡴࡦࡺࡷࠫᡍ"), bstack111l1_opy_ (u"࠭ࠧᡎ"))]
                bstack11lll1ll11_opy_.stop(time=bstack1llll11ll1_opy_, result=Result(result=getattr(report, bstack111l1_opy_ (u"ࠧࡰࡷࡷࡧࡴࡳࡥࠨᡏ"), bstack111l1_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨᡐ")), exception=exception, bstack11lll111l1_opy_=bstack11lll111l1_opy_))
                bstack11llllll11_opy_.bstack11lllll111_opy_(bstack111l1_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫᡑ"), _11l1lll1ll_opy_[item.nodeid][bstack111l1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ᡒ")])
        elif getattr(report, bstack111l1_opy_ (u"ࠫࡼ࡮ࡥ࡯ࠩᡓ"), bstack111l1_opy_ (u"ࠬ࠭ᡔ")) in [bstack111l1_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬᡕ"), bstack111l1_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࠩᡖ")]:
            bstack11lll1l111_opy_ = item.nodeid + bstack111l1_opy_ (u"ࠨ࠯ࠪᡗ") + getattr(report, bstack111l1_opy_ (u"ࠩࡺ࡬ࡪࡴࠧᡘ"), bstack111l1_opy_ (u"ࠪࠫᡙ"))
            if getattr(report, bstack111l1_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬᡚ"), False):
                hook_type = bstack111l1_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡋࡁࡄࡊࠪᡛ") if getattr(report, bstack111l1_opy_ (u"࠭ࡷࡩࡧࡱࠫᡜ"), bstack111l1_opy_ (u"ࠧࠨᡝ")) == bstack111l1_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧᡞ") else bstack111l1_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡇࡄࡇࡍ࠭ᡟ")
                _11l1lll1ll_opy_[bstack11lll1l111_opy_] = {
                    bstack111l1_opy_ (u"ࠪࡹࡺ࡯ࡤࠨᡠ"): uuid4().__str__(),
                    bstack111l1_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨᡡ"): bstack1llll11ll1_opy_,
                    bstack111l1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡸࡾࡶࡥࠨᡢ"): hook_type
                }
            _11l1lll1ll_opy_[bstack11lll1l111_opy_][bstack111l1_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫᡣ")] = bstack1llll11ll1_opy_
            bstack1ll111llll1_opy_(_11l1lll1ll_opy_[bstack11lll1l111_opy_][bstack111l1_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᡤ")])
            bstack1ll11l111l1_opy_(item, _11l1lll1ll_opy_[bstack11lll1l111_opy_], bstack111l1_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪᡥ"), report, call)
            if getattr(report, bstack111l1_opy_ (u"ࠩࡺ࡬ࡪࡴࠧᡦ"), bstack111l1_opy_ (u"ࠪࠫᡧ")) == bstack111l1_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪᡨ"):
                if getattr(report, bstack111l1_opy_ (u"ࠬࡵࡵࡵࡥࡲࡱࡪ࠭ᡩ"), bstack111l1_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ᡪ")) == bstack111l1_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᡫ"):
                    bstack11ll1lll11_opy_ = {
                        bstack111l1_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᡬ"): uuid4().__str__(),
                        bstack111l1_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭ᡭ"): bstack11l1l11l1_opy_(),
                        bstack111l1_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᡮ"): bstack11l1l11l1_opy_()
                    }
                    _11l1lll1ll_opy_[item.nodeid] = {**_11l1lll1ll_opy_[item.nodeid], **bstack11ll1lll11_opy_}
                    bstack1ll11l11lll_opy_(item, _11l1lll1ll_opy_[item.nodeid], bstack111l1_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬᡯ"))
                    bstack1ll11l11lll_opy_(item, _11l1lll1ll_opy_[item.nodeid], bstack111l1_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧᡰ"), report, call)
    except Exception as err:
        print(bstack111l1_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥ࡮ࡡ࡯ࡦ࡯ࡩࡤࡵ࠱࠲ࡻࡢࡸࡪࡹࡴࡠࡧࡹࡩࡳࡺ࠺ࠡࡽࢀࠫᡱ"), str(err))
def bstack1ll11l1llll_opy_(test, bstack11ll1lll11_opy_, result=None, call=None, bstack111l1ll1_opy_=None, outcome=None):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    bstack11lll1ll11_opy_ = {
        bstack111l1_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᡲ"): bstack11ll1lll11_opy_[bstack111l1_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᡳ")],
        bstack111l1_opy_ (u"ࠩࡷࡽࡵ࡫ࠧᡴ"): bstack111l1_opy_ (u"ࠪࡸࡪࡹࡴࠨᡵ"),
        bstack111l1_opy_ (u"ࠫࡳࡧ࡭ࡦࠩᡶ"): test.name,
        bstack111l1_opy_ (u"ࠬࡨ࡯ࡥࡻࠪᡷ"): {
            bstack111l1_opy_ (u"࠭࡬ࡢࡰࡪࠫᡸ"): bstack111l1_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧ᡹"),
            bstack111l1_opy_ (u"ࠨࡥࡲࡨࡪ࠭᡺"): inspect.getsource(test.obj)
        },
        bstack111l1_opy_ (u"ࠩ࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭᡻"): test.name,
        bstack111l1_opy_ (u"ࠪࡷࡨࡵࡰࡦࠩ᡼"): test.name,
        bstack111l1_opy_ (u"ࠫࡸࡩ࡯ࡱࡧࡶࠫ᡽"): bstack1lll1l11_opy_.bstack11ll11llll_opy_(test),
        bstack111l1_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨ᡾"): file_path,
        bstack111l1_opy_ (u"࠭࡬ࡰࡥࡤࡸ࡮ࡵ࡮ࠨ᡿"): file_path,
        bstack111l1_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧᢀ"): bstack111l1_opy_ (u"ࠨࡲࡨࡲࡩ࡯࡮ࡨࠩᢁ"),
        bstack111l1_opy_ (u"ࠩࡹࡧࡤ࡬ࡩ࡭ࡧࡳࡥࡹ࡮ࠧᢂ"): file_path,
        bstack111l1_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧᢃ"): bstack11ll1lll11_opy_[bstack111l1_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨᢄ")],
        bstack111l1_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨᢅ"): bstack111l1_opy_ (u"࠭ࡐࡺࡶࡨࡷࡹ࠭ᢆ"),
        bstack111l1_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳࡒࡦࡴࡸࡲࡕࡧࡲࡢ࡯ࠪᢇ"): {
            bstack111l1_opy_ (u"ࠨࡴࡨࡶࡺࡴ࡟࡯ࡣࡰࡩࠬᢈ"): test.nodeid
        },
        bstack111l1_opy_ (u"ࠩࡷࡥ࡬ࡹࠧᢉ"): bstack111l1lll11_opy_(test.own_markers)
    }
    if bstack111l1ll1_opy_ in [bstack111l1_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡰ࡯ࡰࡱࡧࡧࠫᢊ"), bstack111l1_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ᢋ")]:
        bstack11lll1ll11_opy_[bstack111l1_opy_ (u"ࠬࡳࡥࡵࡣࠪᢌ")] = {
            bstack111l1_opy_ (u"࠭ࡦࡪࡺࡷࡹࡷ࡫ࡳࠨᢍ"): bstack11ll1lll11_opy_.get(bstack111l1_opy_ (u"ࠧࡧ࡫ࡻࡸࡺࡸࡥࡴࠩᢎ"), [])
        }
    if bstack111l1ll1_opy_ == bstack111l1_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕ࡮࡭ࡵࡶࡥࡥࠩᢏ"):
        bstack11lll1ll11_opy_[bstack111l1_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩᢐ")] = bstack111l1_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫᢑ")
        bstack11lll1ll11_opy_[bstack111l1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪᢒ")] = bstack11ll1lll11_opy_[bstack111l1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫᢓ")]
        bstack11lll1ll11_opy_[bstack111l1_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫᢔ")] = bstack11ll1lll11_opy_[bstack111l1_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬᢕ")]
    if result:
        bstack11lll1ll11_opy_[bstack111l1_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨᢖ")] = result.outcome
        bstack11lll1ll11_opy_[bstack111l1_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࡣ࡮ࡴ࡟࡮ࡵࠪᢗ")] = result.duration * 1000
        bstack11lll1ll11_opy_[bstack111l1_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᢘ")] = bstack11ll1lll11_opy_[bstack111l1_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩᢙ")]
        if result.failed:
            bstack11lll1ll11_opy_[bstack111l1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪࡥࡴࡺࡲࡨࠫᢚ")] = bstack11llllll11_opy_.bstack11l11lll11_opy_(call.excinfo.typename)
            bstack11lll1ll11_opy_[bstack111l1_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫ࠧᢛ")] = bstack11llllll11_opy_.bstack1ll1l11l11l_opy_(call.excinfo, result)
        bstack11lll1ll11_opy_[bstack111l1_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭ᢜ")] = bstack11ll1lll11_opy_[bstack111l1_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧᢝ")]
    if outcome:
        bstack11lll1ll11_opy_[bstack111l1_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩᢞ")] = bstack1111l11l11_opy_(outcome)
        bstack11lll1ll11_opy_[bstack111l1_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࡤ࡯࡮ࡠ࡯ࡶࠫᢟ")] = 0
        bstack11lll1ll11_opy_[bstack111l1_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩᢠ")] = bstack11ll1lll11_opy_[bstack111l1_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪᢡ")]
        if bstack11lll1ll11_opy_[bstack111l1_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ᢢ")] == bstack111l1_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᢣ"):
            bstack11lll1ll11_opy_[bstack111l1_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࡡࡷࡽࡵ࡫ࠧᢤ")] = bstack111l1_opy_ (u"ࠩࡘࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࡊࡸࡲࡰࡴࠪᢥ")  # bstack1ll11l11ll1_opy_
            bstack11lll1ll11_opy_[bstack111l1_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࠫᢦ")] = [{bstack111l1_opy_ (u"ࠫࡧࡧࡣ࡬ࡶࡵࡥࡨ࡫ࠧᢧ"): [bstack111l1_opy_ (u"ࠬࡹ࡯࡮ࡧࠣࡩࡷࡸ࡯ࡳࠩᢨ")]}]
        bstack11lll1ll11_opy_[bstack111l1_opy_ (u"࠭ࡨࡰࡱ࡮ࡷᢩࠬ")] = bstack11ll1lll11_opy_[bstack111l1_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭ᢪ")]
    return bstack11lll1ll11_opy_
def bstack1ll111lll11_opy_(test, bstack11ll111ll1_opy_, bstack111l1ll1_opy_, result, call, outcome, bstack1ll11ll11l1_opy_):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    hook_type = bstack11ll111ll1_opy_[bstack111l1_opy_ (u"ࠨࡪࡲࡳࡰࡥࡴࡺࡲࡨࠫ᢫")]
    hook_name = bstack11ll111ll1_opy_[bstack111l1_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟࡯ࡣࡰࡩࠬ᢬")]
    hook_data = {
        bstack111l1_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ᢭"): bstack11ll111ll1_opy_[bstack111l1_opy_ (u"ࠫࡺࡻࡩࡥࠩ᢮")],
        bstack111l1_opy_ (u"ࠬࡺࡹࡱࡧࠪ᢯"): bstack111l1_opy_ (u"࠭ࡨࡰࡱ࡮ࠫᢰ"),
        bstack111l1_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᢱ"): bstack111l1_opy_ (u"ࠨࡽࢀࠫᢲ").format(bstack1lll11ll111_opy_(hook_name)),
        bstack111l1_opy_ (u"ࠩࡥࡳࡩࡿࠧᢳ"): {
            bstack111l1_opy_ (u"ࠪࡰࡦࡴࡧࠨᢴ"): bstack111l1_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫᢵ"),
            bstack111l1_opy_ (u"ࠬࡩ࡯ࡥࡧࠪᢶ"): None
        },
        bstack111l1_opy_ (u"࠭ࡳࡤࡱࡳࡩࠬᢷ"): test.name,
        bstack111l1_opy_ (u"ࠧࡴࡥࡲࡴࡪࡹࠧᢸ"): bstack1lll1l11_opy_.bstack11ll11llll_opy_(test, hook_name),
        bstack111l1_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫᢹ"): file_path,
        bstack111l1_opy_ (u"ࠩ࡯ࡳࡨࡧࡴࡪࡱࡱࠫᢺ"): file_path,
        bstack111l1_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪᢻ"): bstack111l1_opy_ (u"ࠫࡵ࡫࡮ࡥ࡫ࡱ࡫ࠬᢼ"),
        bstack111l1_opy_ (u"ࠬࡼࡣࡠࡨ࡬ࡰࡪࡶࡡࡵࡪࠪᢽ"): file_path,
        bstack111l1_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪᢾ"): bstack11ll111ll1_opy_[bstack111l1_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫᢿ")],
        bstack111l1_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫᣀ"): bstack111l1_opy_ (u"ࠩࡓࡽࡹ࡫ࡳࡵ࠯ࡦࡹࡨࡻ࡭ࡣࡧࡵࠫᣁ") if bstack1ll111l1lll_opy_ == bstack111l1_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠧᣂ") else bstack111l1_opy_ (u"ࠫࡕࡿࡴࡦࡵࡷࠫᣃ"),
        bstack111l1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡸࡾࡶࡥࠨᣄ"): hook_type
    }
    bstack1ll1lll1l1l_opy_ = bstack11l1lllll1_opy_(_11l1lll1ll_opy_.get(test.nodeid, None))
    if bstack1ll1lll1l1l_opy_:
        hook_data[bstack111l1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠ࡫ࡧࠫᣅ")] = bstack1ll1lll1l1l_opy_
    if result:
        hook_data[bstack111l1_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧᣆ")] = result.outcome
        hook_data[bstack111l1_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࡢ࡭ࡳࡥ࡭ࡴࠩᣇ")] = result.duration * 1000
        hook_data[bstack111l1_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧᣈ")] = bstack11ll111ll1_opy_[bstack111l1_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᣉ")]
        if result.failed:
            hook_data[bstack111l1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࡤࡺࡹࡱࡧࠪᣊ")] = bstack11llllll11_opy_.bstack11l11lll11_opy_(call.excinfo.typename)
            hook_data[bstack111l1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭ᣋ")] = bstack11llllll11_opy_.bstack1ll1l11l11l_opy_(call.excinfo, result)
    if outcome:
        hook_data[bstack111l1_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ᣌ")] = bstack1111l11l11_opy_(outcome)
        hook_data[bstack111l1_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࡡ࡬ࡲࡤࡳࡳࠨᣍ")] = 100
        hook_data[bstack111l1_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ᣎ")] = bstack11ll111ll1_opy_[bstack111l1_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧᣏ")]
        if hook_data[bstack111l1_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪᣐ")] == bstack111l1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᣑ"):
            hook_data[bstack111l1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪࡥࡴࡺࡲࡨࠫᣒ")] = bstack111l1_opy_ (u"࠭ࡕ࡯ࡪࡤࡲࡩࡲࡥࡥࡇࡵࡶࡴࡸࠧᣓ")  # bstack1ll11l11ll1_opy_
            hook_data[bstack111l1_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࠨᣔ")] = [{bstack111l1_opy_ (u"ࠨࡤࡤࡧࡰࡺࡲࡢࡥࡨࠫᣕ"): [bstack111l1_opy_ (u"ࠩࡶࡳࡲ࡫ࠠࡦࡴࡵࡳࡷ࠭ᣖ")]}]
    if bstack1ll11ll11l1_opy_:
        hook_data[bstack111l1_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪᣗ")] = bstack1ll11ll11l1_opy_.result
        hook_data[bstack111l1_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳࡥࡩ࡯ࡡࡰࡷࠬᣘ")] = bstack11111llll1_opy_(bstack11ll111ll1_opy_[bstack111l1_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩᣙ")], bstack11ll111ll1_opy_[bstack111l1_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫᣚ")])
        hook_data[bstack111l1_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬᣛ")] = bstack11ll111ll1_opy_[bstack111l1_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ᣜ")]
        if hook_data[bstack111l1_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩᣝ")] == bstack111l1_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪᣞ"):
            hook_data[bstack111l1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࡤࡺࡹࡱࡧࠪᣟ")] = bstack11llllll11_opy_.bstack11l11lll11_opy_(bstack1ll11ll11l1_opy_.exception_type)
            hook_data[bstack111l1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭ᣠ")] = [{bstack111l1_opy_ (u"࠭ࡢࡢࡥ࡮ࡸࡷࡧࡣࡦࠩᣡ"): bstack1111l1l111_opy_(bstack1ll11ll11l1_opy_.exception)}]
    return hook_data
def bstack1ll11l11lll_opy_(test, bstack11ll1lll11_opy_, bstack111l1ll1_opy_, result=None, call=None, outcome=None):
    bstack11lll1ll11_opy_ = bstack1ll11l1llll_opy_(test, bstack11ll1lll11_opy_, result, call, bstack111l1ll1_opy_, outcome)
    driver = getattr(test, bstack111l1_opy_ (u"ࠧࡠࡦࡵ࡭ࡻ࡫ࡲࠨᣢ"), None)
    if bstack111l1ll1_opy_ == bstack111l1_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩᣣ") and driver:
        bstack11lll1ll11_opy_[bstack111l1_opy_ (u"ࠩ࡬ࡲࡹ࡫ࡧࡳࡣࡷ࡭ࡴࡴࡳࠨᣤ")] = bstack11llllll11_opy_.bstack11l1llll11_opy_(driver)
    if bstack111l1ll1_opy_ == bstack111l1_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡰ࡯ࡰࡱࡧࡧࠫᣥ"):
        bstack111l1ll1_opy_ = bstack111l1_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ᣦ")
    bstack11ll111l11_opy_ = {
        bstack111l1_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩᣧ"): bstack111l1ll1_opy_,
        bstack111l1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࠨᣨ"): bstack11lll1ll11_opy_
    }
    bstack11llllll11_opy_.bstack11ll1l11ll_opy_(bstack11ll111l11_opy_)
def bstack1ll11l111l1_opy_(test, bstack11ll1lll11_opy_, bstack111l1ll1_opy_, result=None, call=None, outcome=None, bstack1ll11ll11l1_opy_=None):
    hook_data = bstack1ll111lll11_opy_(test, bstack11ll1lll11_opy_, bstack111l1ll1_opy_, result, call, outcome, bstack1ll11ll11l1_opy_)
    bstack11ll111l11_opy_ = {
        bstack111l1_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫᣩ"): bstack111l1ll1_opy_,
        bstack111l1_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࠪᣪ"): hook_data
    }
    bstack11llllll11_opy_.bstack11ll1l11ll_opy_(bstack11ll111l11_opy_)
def bstack11l1lllll1_opy_(bstack11ll1lll11_opy_):
    if not bstack11ll1lll11_opy_:
        return None
    if bstack11ll1lll11_opy_.get(bstack111l1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬᣫ"), None):
        return getattr(bstack11ll1lll11_opy_[bstack111l1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ᣬ")], bstack111l1_opy_ (u"ࠫࡺࡻࡩࡥࠩᣭ"), None)
    return bstack11ll1lll11_opy_.get(bstack111l1_opy_ (u"ࠬࡻࡵࡪࡦࠪᣮ"), None)
@pytest.fixture(autouse=True)
def second_fixture(caplog, request):
    yield
    try:
        if not bstack11llllll11_opy_.on():
            return
        places = [bstack111l1_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬᣯ"), bstack111l1_opy_ (u"ࠧࡤࡣ࡯ࡰࠬᣰ"), bstack111l1_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪᣱ")]
        bstack11ll11l111_opy_ = []
        for bstack1ll11l1l111_opy_ in places:
            records = caplog.get_records(bstack1ll11l1l111_opy_)
            bstack1ll11ll1l1l_opy_ = bstack111l1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᣲ") if bstack1ll11l1l111_opy_ == bstack111l1_opy_ (u"ࠪࡧࡦࡲ࡬ࠨᣳ") else bstack111l1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᣴ")
            bstack1ll11ll1l11_opy_ = request.node.nodeid + (bstack111l1_opy_ (u"ࠬ࠭ᣵ") if bstack1ll11l1l111_opy_ == bstack111l1_opy_ (u"࠭ࡣࡢ࡮࡯ࠫ᣶") else bstack111l1_opy_ (u"ࠧ࠮ࠩ᣷") + bstack1ll11l1l111_opy_)
            bstack11llll1l1l_opy_ = bstack11l1lllll1_opy_(_11l1lll1ll_opy_.get(bstack1ll11ll1l11_opy_, None))
            if not bstack11llll1l1l_opy_:
                continue
            for record in records:
                if bstack111l11ll1l_opy_(record.message):
                    continue
                bstack11ll11l111_opy_.append({
                    bstack111l1_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫ᣸"): bstack111111l1l1_opy_(record.created).isoformat() + bstack111l1_opy_ (u"ࠩ࡝ࠫ᣹"),
                    bstack111l1_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩ᣺"): record.levelname,
                    bstack111l1_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ᣻"): record.message,
                    bstack1ll11ll1l1l_opy_: bstack11llll1l1l_opy_
                })
        if len(bstack11ll11l111_opy_) > 0:
            bstack11llllll11_opy_.bstack1111l111_opy_(bstack11ll11l111_opy_)
    except Exception as err:
        print(bstack111l1_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡸ࡫ࡣࡰࡰࡧࡣ࡫࡯ࡸࡵࡷࡵࡩ࠿ࠦࡻࡾࠩ᣼"), str(err))
def bstack11l111111_opy_(sequence, driver_command, response=None, driver = None, args = None):
    global bstack11l11ll1_opy_
    bstack1lll1ll11_opy_ = bstack11l1ll1l1_opy_(threading.current_thread(), bstack111l1_opy_ (u"࠭ࡩࡴࡃ࠴࠵ࡾ࡚ࡥࡴࡶࠪ᣽"), None) and bstack11l1ll1l1_opy_(
            threading.current_thread(), bstack111l1_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭᣾"), None)
    bstack1l111l111_opy_ = getattr(driver, bstack111l1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡂ࠳࠴ࡽࡘ࡮࡯ࡶ࡮ࡧࡗࡨࡧ࡮ࠨ᣿"), None) != None and getattr(driver, bstack111l1_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡃ࠴࠵ࡾ࡙ࡨࡰࡷ࡯ࡨࡘࡩࡡ࡯ࠩᤀ"), None) == True
    if sequence == bstack111l1_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࠪᤁ") and driver != None:
      if not bstack11l11ll1_opy_ and bstack1111ll1ll1_opy_() and bstack111l1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᤂ") in CONFIG and CONFIG[bstack111l1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᤃ")] == True and bstack1lll11l1_opy_.bstack1l1l11l11_opy_(driver_command) and (bstack1l111l111_opy_ or bstack1lll1ll11_opy_) and not bstack1ll11111_opy_(args):
        try:
          bstack11l11ll1_opy_ = True
          logger.debug(bstack111l1_opy_ (u"࠭ࡐࡦࡴࡩࡳࡷࡳࡩ࡯ࡩࠣࡷࡨࡧ࡮ࠡࡨࡲࡶࠥࢁࡽࠨᤄ").format(driver_command))
          logger.debug(perform_scan(driver, driver_command=driver_command))
        except Exception as err:
          logger.debug(bstack111l1_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡴࡪࡸࡦࡰࡴࡰࠤࡸࡩࡡ࡯ࠢࡾࢁࠬᤅ").format(str(err)))
        bstack11l11ll1_opy_ = False
    if sequence == bstack111l1_opy_ (u"ࠨࡣࡩࡸࡪࡸࠧᤆ"):
        if driver_command == bstack111l1_opy_ (u"ࠩࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹ࠭ᤇ"):
            bstack11llllll11_opy_.bstack11ll11l1_opy_({
                bstack111l1_opy_ (u"ࠪ࡭ࡲࡧࡧࡦࠩᤈ"): response[bstack111l1_opy_ (u"ࠫࡻࡧ࡬ࡶࡧࠪᤉ")],
                bstack111l1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᤊ"): store[bstack111l1_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪᤋ")]
            })
def bstack1l1llll1_opy_():
    global bstack1l1ll1l1l_opy_
    bstack1l1ll1111_opy_.bstack1l111llll1_opy_()
    logging.shutdown()
    bstack11llllll11_opy_.bstack11l1ll11ll_opy_()
    for driver in bstack1l1ll1l1l_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1ll111ll11l_opy_(*args):
    global bstack1l1ll1l1l_opy_
    bstack11llllll11_opy_.bstack11l1ll11ll_opy_()
    for driver in bstack1l1ll1l1l_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack11ll1llll_opy_(self, *args, **kwargs):
    bstack1l1111ll11_opy_ = bstack1llll1lll1_opy_(self, *args, **kwargs)
    bstack11llllll11_opy_.bstack111lll111_opy_(self)
    return bstack1l1111ll11_opy_
def bstack111l1111_opy_(framework_name):
    from bstack_utils.config import Config
    bstack1111ll1l1_opy_ = Config.bstack1l1ll11lll_opy_()
    if bstack1111ll1l1_opy_.get_property(bstack111l1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟࡮ࡱࡧࡣࡨࡧ࡬࡭ࡧࡧࠫᤌ")):
        return
    bstack1111ll1l1_opy_.bstack1lll11lll_opy_(bstack111l1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠ࡯ࡲࡨࡤࡩࡡ࡭࡮ࡨࡨࠬᤍ"), True)
    global bstack1l111l1l_opy_
    global bstack1111111ll_opy_
    bstack1l111l1l_opy_ = framework_name
    logger.info(bstack1l11111111_opy_.format(bstack1l111l1l_opy_.split(bstack111l1_opy_ (u"ࠩ࠰ࠫᤎ"))[0]))
    try:
        from selenium import webdriver
        from selenium.webdriver.common.service import Service
        from selenium.webdriver.remote.webdriver import WebDriver
        if bstack1111ll1ll1_opy_():
            Service.start = bstack1l1ll1l1ll_opy_
            Service.stop = bstack111111111_opy_
            webdriver.Remote.__init__ = bstack1lllll1l1l_opy_
            webdriver.Remote.get = bstack1l11111lll_opy_
            if not isinstance(os.getenv(bstack111l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓ࡝࡙ࡋࡓࡕࡡࡓࡅࡗࡇࡌࡍࡇࡏࠫᤏ")), str):
                return
            WebDriver.close = bstack1ll111ll11_opy_
            WebDriver.quit = bstack1l11lll11l_opy_
            WebDriver.getAccessibilityResults = getAccessibilityResults
            WebDriver.get_accessibility_results = getAccessibilityResults
            WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
            WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
            WebDriver.performScan = perform_scan
            WebDriver.perform_scan = perform_scan
        if not bstack1111ll1ll1_opy_() and bstack11llllll11_opy_.on():
            webdriver.Remote.__init__ = bstack11ll1llll_opy_
        bstack1111111ll_opy_ = True
    except Exception as e:
        pass
    bstack1l1ll1lll_opy_()
    if os.environ.get(bstack111l1_opy_ (u"ࠫࡘࡋࡌࡆࡐࡌ࡙ࡒࡥࡏࡓࡡࡓࡐࡆ࡟ࡗࡓࡋࡊࡌ࡙ࡥࡉࡏࡕࡗࡅࡑࡒࡅࡅࠩᤐ")):
        bstack1111111ll_opy_ = eval(os.environ.get(bstack111l1_opy_ (u"࡙ࠬࡅࡍࡇࡑࡍ࡚ࡓ࡟ࡐࡔࡢࡔࡑࡇ࡙ࡘࡔࡌࡋࡍ࡚࡟ࡊࡐࡖࡘࡆࡒࡌࡆࡆࠪᤑ")))
    if not bstack1111111ll_opy_:
        bstack1ll11l11l_opy_(bstack111l1_opy_ (u"ࠨࡐࡢࡥ࡮ࡥ࡬࡫ࡳࠡࡰࡲࡸࠥ࡯࡮ࡴࡶࡤࡰࡱ࡫ࡤࠣᤒ"), bstack1ll111111_opy_)
    if bstack1ll11lll1_opy_():
        try:
            from selenium.webdriver.remote.remote_connection import RemoteConnection
            RemoteConnection._get_proxy_url = bstack1lll1ll111_opy_
        except Exception as e:
            logger.error(bstack1ll1111lll_opy_.format(str(e)))
    if bstack111l1_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧᤓ") in str(framework_name).lower():
        if not bstack1111ll1ll1_opy_():
            return
        try:
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
def bstack1l11lll11l_opy_(self):
    global bstack1l111l1l_opy_
    global bstack1l1111l111_opy_
    global bstack1lll1l1l1l_opy_
    try:
        if bstack111l1_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨᤔ") in bstack1l111l1l_opy_ and self.session_id != None and bstack11l1ll1l1_opy_(threading.current_thread(), bstack111l1_opy_ (u"ࠩࡷࡩࡸࡺࡓࡵࡣࡷࡹࡸ࠭ᤕ"), bstack111l1_opy_ (u"ࠪࠫᤖ")) != bstack111l1_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬᤗ"):
            bstack1l111lllll_opy_ = bstack111l1_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬᤘ") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack111l1_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᤙ")
            bstack1l11lllll_opy_(logger, True)
            if self != None:
                bstack1lll1111l1_opy_(self, bstack1l111lllll_opy_, bstack111l1_opy_ (u"ࠧ࠭ࠢࠪᤚ").join(threading.current_thread().bstackTestErrorMessages))
        item = store.get(bstack111l1_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡪࡶࡨࡱࠬᤛ"), None)
        if item is not None and bstack1ll11l1ll1l_opy_:
            bstack1l1lllllll_opy_.bstack111l11ll1_opy_(self, bstack1l111lll1_opy_, logger, item)
        threading.current_thread().testStatus = bstack111l1_opy_ (u"ࠩࠪᤜ")
    except Exception as e:
        logger.debug(bstack111l1_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡ࡯ࡤࡶࡰ࡯࡮ࡨࠢࡶࡸࡦࡺࡵࡴ࠼ࠣࠦᤝ") + str(e))
    bstack1lll1l1l1l_opy_(self)
    self.session_id = None
def bstack1lllll1l1l_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
    global CONFIG
    global bstack1l1111l111_opy_
    global bstack1l1l1ll1ll_opy_
    global bstack1ll11l1l_opy_
    global bstack1l111l1l_opy_
    global bstack1llll1lll1_opy_
    global bstack1l1ll1l1l_opy_
    global bstack11l1l111l_opy_
    global bstack1111l1ll1_opy_
    global bstack1ll11l1ll1l_opy_
    global bstack1l111lll1_opy_
    CONFIG[bstack111l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭ᤞ")] = str(bstack1l111l1l_opy_) + str(__version__)
    command_executor = bstack1l1ll11ll1_opy_(bstack11l1l111l_opy_)
    logger.debug(bstack1l11ll11l1_opy_.format(command_executor))
    proxy = bstack1l1ll1l11_opy_(CONFIG, proxy)
    bstack1l111lll11_opy_ = 0
    try:
        if bstack1ll11l1l_opy_ is True:
            bstack1l111lll11_opy_ = int(os.environ.get(bstack111l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬ᤟")))
    except:
        bstack1l111lll11_opy_ = 0
    bstack1lll111lll_opy_ = bstack1l11l111ll_opy_(CONFIG, bstack1l111lll11_opy_)
    logger.debug(bstack1l1llll111_opy_.format(str(bstack1lll111lll_opy_)))
    bstack1l111lll1_opy_ = CONFIG.get(bstack111l1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩᤠ"))[bstack1l111lll11_opy_]
    if bstack111l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫᤡ") in CONFIG and CONFIG[bstack111l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬᤢ")]:
        bstack1111lll1l_opy_(bstack1lll111lll_opy_, bstack1111l1ll1_opy_)
    if bstack1ll111111l_opy_.bstack1l1l111ll1_opy_(CONFIG, bstack1l111lll11_opy_) and bstack1ll111111l_opy_.bstack11111l11_opy_(bstack1lll111lll_opy_, options, desired_capabilities):
        bstack1ll11l1ll1l_opy_ = True
        bstack1ll111111l_opy_.set_capabilities(bstack1lll111lll_opy_, CONFIG)
    if desired_capabilities:
        bstack1l1l1111_opy_ = bstack11l11l1l_opy_(desired_capabilities)
        bstack1l1l1111_opy_[bstack111l1_opy_ (u"ࠩࡸࡷࡪ࡝࠳ࡄࠩᤣ")] = bstack1l1lll1111_opy_(CONFIG)
        bstack1l11l11l1l_opy_ = bstack1l11l111ll_opy_(bstack1l1l1111_opy_)
        if bstack1l11l11l1l_opy_:
            bstack1lll111lll_opy_ = update(bstack1l11l11l1l_opy_, bstack1lll111lll_opy_)
        desired_capabilities = None
    if options:
        bstack111ll1ll1_opy_(options, bstack1lll111lll_opy_)
    if not options:
        options = bstack1lll1ll1l1_opy_(bstack1lll111lll_opy_)
    if proxy and bstack1l1l11l1ll_opy_() >= version.parse(bstack111l1_opy_ (u"ࠪ࠸࠳࠷࠰࠯࠲ࠪᤤ")):
        options.proxy(proxy)
    if options and bstack1l1l11l1ll_opy_() >= version.parse(bstack111l1_opy_ (u"ࠫ࠸࠴࠸࠯࠲ࠪᤥ")):
        desired_capabilities = None
    if (
            not options and not desired_capabilities
    ) or (
            bstack1l1l11l1ll_opy_() < version.parse(bstack111l1_opy_ (u"ࠬ࠹࠮࠹࠰࠳ࠫᤦ")) and not desired_capabilities
    ):
        desired_capabilities = {}
        desired_capabilities.update(bstack1lll111lll_opy_)
    logger.info(bstack1llllll11_opy_)
    if bstack1l1l11l1ll_opy_() >= version.parse(bstack111l1_opy_ (u"࠭࠴࠯࠳࠳࠲࠵࠭ᤧ")):
        bstack1llll1lll1_opy_(self, command_executor=command_executor,
                  options=options, keep_alive=keep_alive, file_detector=file_detector)
    elif bstack1l1l11l1ll_opy_() >= version.parse(bstack111l1_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭ᤨ")):
        bstack1llll1lll1_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities, options=options,
                  browser_profile=browser_profile, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    elif bstack1l1l11l1ll_opy_() >= version.parse(bstack111l1_opy_ (u"ࠨ࠴࠱࠹࠸࠴࠰ࠨᤩ")):
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
        bstack1lll1llll1_opy_ = bstack111l1_opy_ (u"ࠩࠪᤪ")
        if bstack1l1l11l1ll_opy_() >= version.parse(bstack111l1_opy_ (u"ࠪ࠸࠳࠶࠮࠱ࡤ࠴ࠫᤫ")):
            bstack1lll1llll1_opy_ = self.caps.get(bstack111l1_opy_ (u"ࠦࡴࡶࡴࡪ࡯ࡤࡰࡍࡻࡢࡖࡴ࡯ࠦ᤬"))
        else:
            bstack1lll1llll1_opy_ = self.capabilities.get(bstack111l1_opy_ (u"ࠧࡵࡰࡵ࡫ࡰࡥࡱࡎࡵࡣࡗࡵࡰࠧ᤭"))
        if bstack1lll1llll1_opy_:
            bstack1l11lll111_opy_(bstack1lll1llll1_opy_)
            if bstack1l1l11l1ll_opy_() <= version.parse(bstack111l1_opy_ (u"࠭࠳࠯࠳࠶࠲࠵࠭᤮")):
                self.command_executor._url = bstack111l1_opy_ (u"ࠢࡩࡶࡷࡴ࠿࠵࠯ࠣ᤯") + bstack11l1l111l_opy_ + bstack111l1_opy_ (u"ࠣ࠼࠻࠴࠴ࡽࡤ࠰ࡪࡸࡦࠧᤰ")
            else:
                self.command_executor._url = bstack111l1_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲ࠦᤱ") + bstack1lll1llll1_opy_ + bstack111l1_opy_ (u"ࠥ࠳ࡼࡪ࠯ࡩࡷࡥࠦᤲ")
            logger.debug(bstack11llll11l_opy_.format(bstack1lll1llll1_opy_))
        else:
            logger.debug(bstack1l111111_opy_.format(bstack111l1_opy_ (u"ࠦࡔࡶࡴࡪ࡯ࡤࡰࠥࡎࡵࡣࠢࡱࡳࡹࠦࡦࡰࡷࡱࡨࠧᤳ")))
    except Exception as e:
        logger.debug(bstack1l111111_opy_.format(e))
    bstack1l1111l111_opy_ = self.session_id
    if bstack111l1_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬᤴ") in bstack1l111l1l_opy_:
        threading.current_thread().bstackSessionId = self.session_id
        threading.current_thread().bstackSessionDriver = self
        threading.current_thread().bstackTestErrorMessages = []
        item = store.get(bstack111l1_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡴࡦ࡯ࠪᤵ"), None)
        if item:
            bstack1ll11l1111l_opy_ = getattr(item, bstack111l1_opy_ (u"ࠧࡠࡶࡨࡷࡹࡥࡣࡢࡵࡨࡣࡸࡺࡡࡳࡶࡨࡨࠬᤶ"), False)
            if not getattr(item, bstack111l1_opy_ (u"ࠨࡡࡧࡶ࡮ࡼࡥࡳࠩᤷ"), None) and bstack1ll11l1111l_opy_:
                setattr(store[bstack111l1_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡷࡩࡲ࠭ᤸ")], bstack111l1_opy_ (u"ࠪࡣࡩࡸࡩࡷࡧࡵ᤹ࠫ"), self)
        bstack11llllll11_opy_.bstack111lll111_opy_(self)
    bstack1l1ll1l1l_opy_.append(self)
    if bstack111l1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ᤺") in CONFIG and bstack111l1_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧ᤻ࠪ") in CONFIG[bstack111l1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ᤼")][bstack1l111lll11_opy_]:
        bstack1l1l1ll1ll_opy_ = CONFIG[bstack111l1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ᤽")][bstack1l111lll11_opy_][bstack111l1_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭᤾")]
    logger.debug(bstack1l1ll11l11_opy_.format(bstack1l1111l111_opy_))
def bstack1l11111lll_opy_(self, url):
    global bstack1l1lll1l11_opy_
    global CONFIG
    try:
        bstack1l1ll111_opy_(url, CONFIG, logger)
    except Exception as err:
        logger.debug(bstack1l111l11_opy_.format(str(err)))
    try:
        bstack1l1lll1l11_opy_(self, url)
    except Exception as e:
        try:
            bstack1l1l11ll1_opy_ = str(e)
            if any(err_msg in bstack1l1l11ll1_opy_ for err_msg in bstack1l11llll11_opy_):
                bstack1l1ll111_opy_(url, CONFIG, logger, True)
        except Exception as err:
            logger.debug(bstack1l111l11_opy_.format(str(err)))
        raise e
def bstack1llll1ll1_opy_(item, when):
    global bstack1l1l111l11_opy_
    try:
        bstack1l1l111l11_opy_(item, when)
    except Exception as e:
        pass
def bstack1ll11l1ll_opy_(item, call, rep):
    global bstack1l111111l_opy_
    global bstack1l1ll1l1l_opy_
    name = bstack111l1_opy_ (u"ࠩࠪ᤿")
    try:
        if rep.when == bstack111l1_opy_ (u"ࠪࡧࡦࡲ࡬ࠨ᥀"):
            bstack1l1111l111_opy_ = threading.current_thread().bstackSessionId
            bstack1ll11ll1ll1_opy_ = item.config.getoption(bstack111l1_opy_ (u"ࠫࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭᥁"))
            try:
                if (str(bstack1ll11ll1ll1_opy_).lower() != bstack111l1_opy_ (u"ࠬࡺࡲࡶࡧࠪ᥂")):
                    name = str(rep.nodeid)
                    bstack11lll11l_opy_ = bstack11llll1l_opy_(bstack111l1_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ᥃"), name, bstack111l1_opy_ (u"ࠧࠨ᥄"), bstack111l1_opy_ (u"ࠨࠩ᥅"), bstack111l1_opy_ (u"ࠩࠪ᥆"), bstack111l1_opy_ (u"ࠪࠫ᥇"))
                    os.environ[bstack111l1_opy_ (u"ࠫࡕ࡟ࡔࡆࡕࡗࡣ࡙ࡋࡓࡕࡡࡑࡅࡒࡋࠧ᥈")] = name
                    for driver in bstack1l1ll1l1l_opy_:
                        if bstack1l1111l111_opy_ == driver.session_id:
                            driver.execute_script(bstack11lll11l_opy_)
            except Exception as e:
                logger.debug(bstack111l1_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠦࡦࡰࡴࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡴࡧࡶࡷ࡮ࡵ࡮࠻ࠢࡾࢁࠬ᥉").format(str(e)))
            try:
                bstack1ll11l111_opy_(rep.outcome.lower())
                if rep.outcome.lower() != bstack111l1_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧ᥊"):
                    status = bstack111l1_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ᥋") if rep.outcome.lower() == bstack111l1_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ᥌") else bstack111l1_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ᥍")
                    reason = bstack111l1_opy_ (u"ࠪࠫ᥎")
                    if status == bstack111l1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ᥏"):
                        reason = rep.longrepr.reprcrash.message
                        if (not threading.current_thread().bstackTestErrorMessages):
                            threading.current_thread().bstackTestErrorMessages = []
                        threading.current_thread().bstackTestErrorMessages.append(reason)
                    level = bstack111l1_opy_ (u"ࠬ࡯࡮ࡧࡱࠪᥐ") if status == bstack111l1_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ᥑ") else bstack111l1_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ᥒ")
                    data = name + bstack111l1_opy_ (u"ࠨࠢࡳࡥࡸࡹࡥࡥࠣࠪᥓ") if status == bstack111l1_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩᥔ") else name + bstack111l1_opy_ (u"ࠪࠤ࡫ࡧࡩ࡭ࡧࡧࠥࠥ࠭ᥕ") + reason
                    bstack1l11l111l_opy_ = bstack11llll1l_opy_(bstack111l1_opy_ (u"ࠫࡦࡴ࡮ࡰࡶࡤࡸࡪ࠭ᥖ"), bstack111l1_opy_ (u"ࠬ࠭ᥗ"), bstack111l1_opy_ (u"࠭ࠧᥘ"), bstack111l1_opy_ (u"ࠧࠨᥙ"), level, data)
                    for driver in bstack1l1ll1l1l_opy_:
                        if bstack1l1111l111_opy_ == driver.session_id:
                            driver.execute_script(bstack1l11l111l_opy_)
            except Exception as e:
                logger.debug(bstack111l1_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡷࡪࡺࡴࡪࡰࡪࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡩ࡯࡯ࡶࡨࡼࡹࠦࡦࡰࡴࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡴࡧࡶࡷ࡮ࡵ࡮࠻ࠢࡾࢁࠬᥚ").format(str(e)))
    except Exception as e:
        logger.debug(bstack111l1_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤ࡬࡫ࡴࡵ࡫ࡱ࡫ࠥࡹࡴࡢࡶࡨࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡹ࡫ࡳࡵࠢࡶࡸࡦࡺࡵࡴ࠼ࠣࡿࢂ࠭ᥛ").format(str(e)))
    bstack1l111111l_opy_(item, call, rep)
notset = Notset()
def bstack111l1ll11_opy_(self, name: str, default=notset, skip: bool = False):
    global bstack1l111l11l_opy_
    if str(name).lower() == bstack111l1_opy_ (u"ࠪࡨࡷ࡯ࡶࡦࡴࠪᥜ"):
        return bstack111l1_opy_ (u"ࠦࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠥᥝ")
    else:
        return bstack1l111l11l_opy_(self, name, default, skip)
def bstack1lll1ll111_opy_(self):
    global CONFIG
    global bstack1l11l11ll1_opy_
    try:
        proxy = bstack1l11l1ll1l_opy_(CONFIG)
        if proxy:
            if proxy.endswith(bstack111l1_opy_ (u"ࠬ࠴ࡰࡢࡥࠪᥞ")):
                proxies = bstack1l11llll_opy_(proxy, bstack1l1ll11ll1_opy_())
                if len(proxies) > 0:
                    protocol, bstack11l1111l_opy_ = proxies.popitem()
                    if bstack111l1_opy_ (u"ࠨ࠺࠰࠱ࠥᥟ") in bstack11l1111l_opy_:
                        return bstack11l1111l_opy_
                    else:
                        return bstack111l1_opy_ (u"ࠢࡩࡶࡷࡴ࠿࠵࠯ࠣᥠ") + bstack11l1111l_opy_
            else:
                return proxy
    except Exception as e:
        logger.error(bstack111l1_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡪࡰࠣࡷࡪࡺࡴࡪࡰࡪࠤࡵࡸ࡯ࡹࡻࠣࡹࡷࡲࠠ࠻ࠢࡾࢁࠧᥡ").format(str(e)))
    return bstack1l11l11ll1_opy_(self)
def bstack1ll11lll1_opy_():
    return (bstack111l1_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬᥢ") in CONFIG or bstack111l1_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧᥣ") in CONFIG) and bstack1l1llll1ll_opy_() and bstack1l1l11l1ll_opy_() >= version.parse(
        bstack1l11ll1l1_opy_)
def bstack1111l11l1_opy_(self,
               executablePath=None,
               channel=None,
               args=None,
               ignoreDefaultArgs=None,
               handleSIGINT=None,
               handleSIGTERM=None,
               handleSIGHUP=None,
               timeout=None,
               env=None,
               headless=None,
               devtools=None,
               proxy=None,
               downloadsPath=None,
               slowMo=None,
               tracesDir=None,
               chromiumSandbox=None,
               firefoxUserPrefs=None
               ):
    global CONFIG
    global bstack1l1l1ll1ll_opy_
    global bstack1ll11l1l_opy_
    global bstack1l111l1l_opy_
    CONFIG[bstack111l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭ᥤ")] = str(bstack1l111l1l_opy_) + str(__version__)
    bstack1l111lll11_opy_ = 0
    try:
        if bstack1ll11l1l_opy_ is True:
            bstack1l111lll11_opy_ = int(os.environ.get(bstack111l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬᥥ")))
    except:
        bstack1l111lll11_opy_ = 0
    CONFIG[bstack111l1_opy_ (u"ࠨࡩࡴࡒ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠧᥦ")] = True
    bstack1lll111lll_opy_ = bstack1l11l111ll_opy_(CONFIG, bstack1l111lll11_opy_)
    logger.debug(bstack1l1llll111_opy_.format(str(bstack1lll111lll_opy_)))
    if CONFIG.get(bstack111l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫᥧ")):
        bstack1111lll1l_opy_(bstack1lll111lll_opy_, bstack1111l1ll1_opy_)
    if bstack111l1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫᥨ") in CONFIG and bstack111l1_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧᥩ") in CONFIG[bstack111l1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ᥪ")][bstack1l111lll11_opy_]:
        bstack1l1l1ll1ll_opy_ = CONFIG[bstack111l1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧᥫ")][bstack1l111lll11_opy_][bstack111l1_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪᥬ")]
    import urllib
    import json
    bstack1lll1111_opy_ = bstack111l1_opy_ (u"࠭ࡷࡴࡵ࠽࠳࠴ࡩࡤࡱ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࡁࡦࡥࡵࡹ࠽ࠨᥭ") + urllib.parse.quote(json.dumps(bstack1lll111lll_opy_))
    browser = self.connect(bstack1lll1111_opy_)
    return browser
def bstack1l1ll1lll_opy_():
    global bstack1111111ll_opy_
    global bstack1l111l1l_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        from bstack_utils.helper import bstack111lll1ll_opy_
        if not bstack1111ll1ll1_opy_():
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
def bstack1ll111ll1ll_opy_():
    global CONFIG
    global bstack1l111ll111_opy_
    global bstack11l1l111l_opy_
    global bstack1111l1ll1_opy_
    global bstack1ll11l1l_opy_
    global bstack1llllll1l_opy_
    CONFIG = json.loads(os.environ.get(bstack111l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡐࡐࡉࡍࡌ࠭᥮")))
    bstack1l111ll111_opy_ = eval(os.environ.get(bstack111l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩ᥯")))
    bstack11l1l111l_opy_ = os.environ.get(bstack111l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡊࡘࡆࡤ࡛ࡒࡍࠩᥰ"))
    bstack111111l11_opy_(CONFIG, bstack1l111ll111_opy_)
    bstack1llllll1l_opy_ = bstack1l1ll1111_opy_.bstack1l11ll11ll_opy_(CONFIG, bstack1llllll1l_opy_)
    global bstack1llll1lll1_opy_
    global bstack1lll1l1l1l_opy_
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
    except Exception as e:
        pass
    if (bstack111l1_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭ᥱ") in CONFIG or bstack111l1_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨᥲ") in CONFIG) and bstack1l1llll1ll_opy_():
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
        logger.debug(bstack111l1_opy_ (u"ࠬࡖ࡬ࡦࡣࡶࡩࠥ࡯࡮ࡴࡶࡤࡰࡱࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡸࡴࠦࡲࡶࡰࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡵࡧࡶࡸࡸ࠭ᥳ"))
    bstack1111l1ll1_opy_ = CONFIG.get(bstack111l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪᥴ"), {}).get(bstack111l1_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ᥵"))
    bstack1ll11l1l_opy_ = True
    bstack111l1111_opy_(bstack111l1l111_opy_)
if (bstack111l1ll111_opy_()):
    bstack1ll111ll1ll_opy_()
@bstack11ll1ll111_opy_(class_method=False)
def bstack1ll111lllll_opy_(hook_name, event, bstack1ll11ll11ll_opy_=None):
    if hook_name not in [bstack111l1_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࠩ᥶"), bstack111l1_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠭᥷"), bstack111l1_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡰࡳࡩࡻ࡬ࡦࠩ᥸"), bstack111l1_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡰࡦࡸࡰࡪ࠭᥹"), bstack111l1_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡨࡲࡡࡴࡵࠪ᥺"), bstack111l1_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡥ࡯ࡥࡸࡹࠧ᥻"), bstack111l1_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥ࡭ࡦࡶ࡫ࡳࡩ࠭᥼"), bstack111l1_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡪࡺࡨࡰࡦࠪ᥽")]:
        return
    node = store[bstack111l1_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡷࡩࡲ࠭᥾")]
    if hook_name in [bstack111l1_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡰࡳࡩࡻ࡬ࡦࠩ᥿"), bstack111l1_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡰࡦࡸࡰࡪ࠭ᦀ")]:
        node = store[bstack111l1_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥ࡭ࡰࡦࡸࡰࡪࡥࡩࡵࡧࡰࠫᦁ")]
    elif hook_name in [bstack111l1_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡩ࡬ࡢࡵࡶࠫᦂ"), bstack111l1_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡦࡰࡦࡹࡳࠨᦃ")]:
        node = store[bstack111l1_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡦࡰࡦࡹࡳࡠ࡫ࡷࡩࡲ࠭ᦄ")]
    if event == bstack111l1_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࠩᦅ"):
        hook_type = bstack1lll11l11ll_opy_(hook_name)
        uuid = uuid4().__str__()
        bstack11ll111ll1_opy_ = {
            bstack111l1_opy_ (u"ࠪࡹࡺ࡯ࡤࠨᦆ"): uuid,
            bstack111l1_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨᦇ"): bstack11l1l11l1_opy_(),
            bstack111l1_opy_ (u"ࠬࡺࡹࡱࡧࠪᦈ"): bstack111l1_opy_ (u"࠭ࡨࡰࡱ࡮ࠫᦉ"),
            bstack111l1_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡺࡹࡱࡧࠪᦊ"): hook_type,
            bstack111l1_opy_ (u"ࠨࡪࡲࡳࡰࡥ࡮ࡢ࡯ࡨࠫᦋ"): hook_name
        }
        store[bstack111l1_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭ᦌ")].append(uuid)
        bstack1ll111ll1l1_opy_ = node.nodeid
        if hook_type == bstack111l1_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡉࡆࡉࡈࠨᦍ"):
            if not _11l1lll1ll_opy_.get(bstack1ll111ll1l1_opy_, None):
                _11l1lll1ll_opy_[bstack1ll111ll1l1_opy_] = {bstack111l1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪᦎ"): []}
            _11l1lll1ll_opy_[bstack1ll111ll1l1_opy_][bstack111l1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫᦏ")].append(bstack11ll111ll1_opy_[bstack111l1_opy_ (u"࠭ࡵࡶ࡫ࡧࠫᦐ")])
        _11l1lll1ll_opy_[bstack1ll111ll1l1_opy_ + bstack111l1_opy_ (u"ࠧ࠮ࠩᦑ") + hook_name] = bstack11ll111ll1_opy_
        bstack1ll11l111l1_opy_(node, bstack11ll111ll1_opy_, bstack111l1_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩᦒ"))
    elif event == bstack111l1_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࠨᦓ"):
        bstack11lll1l111_opy_ = node.nodeid + bstack111l1_opy_ (u"ࠪ࠱ࠬᦔ") + hook_name
        _11l1lll1ll_opy_[bstack11lll1l111_opy_][bstack111l1_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩᦕ")] = bstack11l1l11l1_opy_()
        bstack1ll111llll1_opy_(_11l1lll1ll_opy_[bstack11lll1l111_opy_][bstack111l1_opy_ (u"ࠬࡻࡵࡪࡦࠪᦖ")])
        bstack1ll11l111l1_opy_(node, _11l1lll1ll_opy_[bstack11lll1l111_opy_], bstack111l1_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨᦗ"), bstack1ll11ll11l1_opy_=bstack1ll11ll11ll_opy_)
def bstack1ll11l11l1l_opy_():
    global bstack1ll111l1lll_opy_
    if bstack1ll1l1ll_opy_():
        bstack1ll111l1lll_opy_ = bstack111l1_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠫᦘ")
    else:
        bstack1ll111l1lll_opy_ = bstack111l1_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨᦙ")
@bstack11llllll11_opy_.bstack1ll1l11llll_opy_
def bstack1ll111ll111_opy_():
    bstack1ll11l11l1l_opy_()
    if bstack1l1llll1ll_opy_():
        bstack1llll1ll11_opy_(bstack11l111111_opy_)
    try:
        bstack1111111ll1_opy_(bstack1ll111lllll_opy_)
    except Exception as e:
        logger.debug(bstack111l1_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡪࡲࡳࡰࡹࠠࡱࡣࡷࡧ࡭ࡀࠠࡼࡿࠥᦚ").format(e))
bstack1ll111ll111_opy_()