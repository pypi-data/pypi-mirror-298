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
import os
import logging
from uuid import uuid4
from bstack_utils.bstack11lll1ll11_opy_ import bstack11lll11l1l_opy_, bstack11lll11l11_opy_
from bstack_utils.bstack1l11l1l1ll_opy_ import bstack1lll1l11_opy_
from bstack_utils.helper import bstack11l1ll1l1_opy_, bstack11l1l11l1_opy_, Result
from bstack_utils.bstack11111l1l_opy_ import bstack11llllll11_opy_
from bstack_utils.capture import bstack11lll1lll1_opy_
from bstack_utils.constants import *
logger = logging.getLogger(__name__)
class bstack1l1llll1l1_opy_:
    def __init__(self):
        self.bstack11lll1ll1l_opy_ = bstack11lll1lll1_opy_(self.bstack11llll11l1_opy_)
        self.tests = {}
    @staticmethod
    def bstack11llll11l1_opy_(log):
        if not (log[bstack111l1_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪස")] and log[bstack111l1_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫහ")].strip()):
            return
        active = bstack1lll1l11_opy_.bstack11lll1l1ll_opy_()
        log = {
            bstack111l1_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪළ"): log[bstack111l1_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫෆ")],
            bstack111l1_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩ෇"): bstack11l1l11l1_opy_(),
            bstack111l1_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ෈"): log[bstack111l1_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ෉")],
        }
        if active:
            if active[bstack111l1_opy_ (u"ࠩࡷࡽࡵ࡫්ࠧ")] == bstack111l1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࠨ෋"):
                log[bstack111l1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ෌")] = active[bstack111l1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ෍")]
            elif active[bstack111l1_opy_ (u"࠭ࡴࡺࡲࡨࠫ෎")] == bstack111l1_opy_ (u"ࠧࡵࡧࡶࡸࠬා"):
                log[bstack111l1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨැ")] = active[bstack111l1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩෑ")]
        bstack11llllll11_opy_.bstack1111l111_opy_([log])
    def start_test(self, attrs):
        bstack11llll1l1l_opy_ = uuid4().__str__()
        self.tests[bstack11llll1l1l_opy_] = {}
        self.bstack11lll1ll1l_opy_.start()
        bstack11lll1ll11_opy_ = bstack11lll11l11_opy_(
            name=attrs.scenario.name,
            uuid=bstack11llll1l1l_opy_,
            bstack11lll11ll1_opy_=bstack11l1l11l1_opy_(),
            file_path=attrs.feature.filename,
            result=bstack111l1_opy_ (u"ࠥࡴࡪࡴࡤࡪࡰࡪࠦි"),
            framework=bstack111l1_opy_ (u"ࠫࡇ࡫ࡨࡢࡸࡨࠫී"),
            scope=[attrs.feature.name],
            meta={},
            tags=attrs.scenario.tags
        )
        self.tests[bstack11llll1l1l_opy_][bstack111l1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨු")] = bstack11lll1ll11_opy_
        threading.current_thread().current_test_uuid = bstack11llll1l1l_opy_
        bstack11llllll11_opy_.bstack11lllll111_opy_(bstack111l1_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧ෕"), bstack11lll1ll11_opy_)
    def end_test(self, attrs):
        bstack11lll1llll_opy_ = {
            bstack111l1_opy_ (u"ࠢ࡯ࡣࡰࡩࠧූ"): attrs.feature.name,
            bstack111l1_opy_ (u"ࠣࡦࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳࠨ෗"): attrs.feature.description
        }
        current_test_uuid = threading.current_thread().current_test_uuid
        bstack11lll1ll11_opy_ = self.tests[current_test_uuid][bstack111l1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬෘ")]
        meta = {
            bstack111l1_opy_ (u"ࠥࡪࡪࡧࡴࡶࡴࡨࠦෙ"): bstack11lll1llll_opy_,
            bstack111l1_opy_ (u"ࠦࡸࡺࡥࡱࡵࠥේ"): bstack11lll1ll11_opy_.meta.get(bstack111l1_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫෛ"), []),
            bstack111l1_opy_ (u"ࠨࡳࡤࡧࡱࡥࡷ࡯࡯ࠣො"): {
                bstack111l1_opy_ (u"ࠢ࡯ࡣࡰࡩࠧෝ"): attrs.feature.scenarios[0].name if len(attrs.feature.scenarios) else None
            }
        }
        bstack11lll1ll11_opy_.bstack11llll1ll1_opy_(meta)
        bstack11lll1l11l_opy_, exception = self._11lll111ll_opy_(attrs)
        bstack11llll1lll_opy_ = Result(result=attrs.status.name, exception=exception, bstack11lll111l1_opy_=[bstack11lll1l11l_opy_])
        self.tests[threading.current_thread().current_test_uuid][bstack111l1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫෞ")].stop(time=bstack11l1l11l1_opy_(), duration=int(attrs.duration)*1000, result=bstack11llll1lll_opy_)
        bstack11llllll11_opy_.bstack11lllll111_opy_(bstack111l1_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫෟ"), self.tests[threading.current_thread().current_test_uuid][bstack111l1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭෠")])
    def bstack1ll1l111l1_opy_(self, attrs):
        bstack11lll11lll_opy_ = {
            bstack111l1_opy_ (u"ࠫ࡮ࡪࠧ෡"): uuid4().__str__(),
            bstack111l1_opy_ (u"ࠬࡱࡥࡺࡹࡲࡶࡩ࠭෢"): attrs.keyword,
            bstack111l1_opy_ (u"࠭ࡳࡵࡧࡳࡣࡦࡸࡧࡶ࡯ࡨࡲࡹ࠭෣"): [],
            bstack111l1_opy_ (u"ࠧࡵࡧࡻࡸࠬ෤"): attrs.name,
            bstack111l1_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬ෥"): bstack11l1l11l1_opy_(),
            bstack111l1_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ෦"): bstack111l1_opy_ (u"ࠪࡴࡪࡴࡤࡪࡰࡪࠫ෧"),
            bstack111l1_opy_ (u"ࠫࡩ࡫ࡳࡤࡴ࡬ࡴࡹ࡯࡯࡯ࠩ෨"): bstack111l1_opy_ (u"ࠬ࠭෩")
        }
        self.tests[threading.current_thread().current_test_uuid][bstack111l1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ෪")].add_step(bstack11lll11lll_opy_)
        threading.current_thread().current_step_uuid = bstack11lll11lll_opy_[bstack111l1_opy_ (u"ࠧࡪࡦࠪ෫")]
    def bstack1ll111l1ll_opy_(self, attrs):
        current_test_id = bstack11l1ll1l1_opy_(threading.current_thread(), bstack111l1_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬ෬"), None)
        current_step_uuid = bstack11l1ll1l1_opy_(threading.current_thread(), bstack111l1_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡷࡹ࡫ࡰࡠࡷࡸ࡭ࡩ࠭෭"), None)
        bstack11lll1l11l_opy_, exception = self._11lll111ll_opy_(attrs)
        bstack11llll1lll_opy_ = Result(result=attrs.status.name, exception=exception, bstack11lll111l1_opy_=[bstack11lll1l11l_opy_])
        self.tests[current_test_id][bstack111l1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭෮")].bstack11llll11ll_opy_(current_step_uuid, duration=int(attrs.duration)*1000, result=bstack11llll1lll_opy_)
        threading.current_thread().current_step_uuid = None
    def bstack11lll1l11_opy_(self, name, attrs):
        bstack11llll1111_opy_ = uuid4().__str__()
        self.tests[bstack11llll1111_opy_] = {}
        self.bstack11lll1ll1l_opy_.start()
        scopes = []
        if name in [bstack111l1_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡦࡲ࡬ࠣ෯"), bstack111l1_opy_ (u"ࠧࡧࡦࡵࡧࡵࡣࡦࡲ࡬ࠣ෰")]:
            file_path = os.path.join(attrs.config.base_dir, attrs.config.environment_file)
            scopes = [attrs.config.environment_file]
        elif name in [bstack111l1_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡦࡦࡣࡷࡹࡷ࡫ࠢ෱"), bstack111l1_opy_ (u"ࠢࡢࡨࡷࡩࡷࡥࡦࡦࡣࡷࡹࡷ࡫ࠢෲ")]:
            file_path = attrs.filename
            scopes = [attrs.name]
        else:
            file_path = attrs.filename
            scopes = [attrs.feature.name]
        hook_data = bstack11lll11l1l_opy_(
            name=name,
            uuid=bstack11llll1111_opy_,
            bstack11lll11ll1_opy_=bstack11l1l11l1_opy_(),
            file_path=file_path,
            framework=bstack111l1_opy_ (u"ࠣࡄࡨ࡬ࡦࡼࡥࠣෳ"),
            scope=scopes,
            result=bstack111l1_opy_ (u"ࠤࡳࡩࡳࡪࡩ࡯ࡩࠥ෴"),
            hook_type=name
        )
        self.tests[bstack11llll1111_opy_][bstack111l1_opy_ (u"ࠥࡸࡪࡹࡴࡠࡦࡤࡸࡦࠨ෵")] = hook_data
        current_test_id = bstack11l1ll1l1_opy_(threading.current_thread(), bstack111l1_opy_ (u"ࠦࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠣ෶"), None)
        if current_test_id:
            hook_data.bstack11lll1l1l1_opy_(current_test_id)
        if name == bstack111l1_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡧ࡬࡭ࠤ෷"):
            threading.current_thread().before_all_hook_uuid = bstack11llll1111_opy_
        threading.current_thread().current_hook_uuid = bstack11llll1111_opy_
        bstack11llllll11_opy_.bstack11lllll111_opy_(bstack111l1_opy_ (u"ࠨࡈࡰࡱ࡮ࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠢ෸"), hook_data)
    def bstack11111lll1_opy_(self, attrs):
        bstack11lll1l111_opy_ = bstack11l1ll1l1_opy_(threading.current_thread(), bstack111l1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫ෹"), None)
        hook_data = self.tests[bstack11lll1l111_opy_][bstack111l1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫ෺")]
        status = bstack111l1_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠤ෻")
        exception = None
        bstack11lll1l11l_opy_ = None
        if hook_data.name == bstack111l1_opy_ (u"ࠥࡥ࡫ࡺࡥࡳࡡࡤࡰࡱࠨ෼"):
            self.bstack11lll1ll1l_opy_.reset()
            bstack11llll1l11_opy_ = self.tests[bstack11l1ll1l1_opy_(threading.current_thread(), bstack111l1_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࡣࡦࡲ࡬ࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫ෽"), None)][bstack111l1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ෾")].result.result
            if bstack11llll1l11_opy_ == bstack111l1_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨ෿"):
                if attrs.hook_failures == 1:
                    status = bstack111l1_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢ฀")
                elif attrs.hook_failures == 2:
                    status = bstack111l1_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣก")
            elif attrs.bstack11llll111l_opy_:
                status = bstack111l1_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤข")
            threading.current_thread().before_all_hook_uuid = None
        else:
            if hook_data.name == bstack111l1_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࡢࡥࡱࡲࠧฃ") and attrs.hook_failures == 1:
                status = bstack111l1_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦค")
            elif hasattr(attrs, bstack111l1_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࡣࡲ࡫ࡳࡴࡣࡪࡩࠬฅ")) and attrs.error_message:
                status = bstack111l1_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨฆ")
            bstack11lll1l11l_opy_, exception = self._11lll111ll_opy_(attrs)
        bstack11llll1lll_opy_ = Result(result=status, exception=exception, bstack11lll111l1_opy_=[bstack11lll1l11l_opy_])
        hook_data.stop(time=bstack11l1l11l1_opy_(), duration=0, result=bstack11llll1lll_opy_)
        bstack11llllll11_opy_.bstack11lllll111_opy_(bstack111l1_opy_ (u"ࠧࡉࡱࡲ࡯ࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩง"), self.tests[bstack11lll1l111_opy_][bstack111l1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫจ")])
        threading.current_thread().current_hook_uuid = None
    def _11lll111ll_opy_(self, attrs):
        try:
            import traceback
            bstack11ll1lll1_opy_ = traceback.format_tb(attrs.exc_traceback)
            bstack11lll1l11l_opy_ = bstack11ll1lll1_opy_[-1] if bstack11ll1lll1_opy_ else None
            exception = attrs.exception
        except Exception:
            logger.debug(bstack111l1_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡱࡦࡧࡺࡸࡲࡦࡦࠣࡻ࡭࡯࡬ࡦࠢࡪࡩࡹࡺࡩ࡯ࡩࠣࡧࡺࡹࡴࡰ࡯ࠣࡸࡷࡧࡣࡦࡤࡤࡧࡰࠨฉ"))
            bstack11lll1l11l_opy_ = None
            exception = None
        return bstack11lll1l11l_opy_, exception