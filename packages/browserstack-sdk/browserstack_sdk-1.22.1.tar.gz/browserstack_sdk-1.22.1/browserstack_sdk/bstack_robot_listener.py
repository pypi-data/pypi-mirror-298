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
import threading
from uuid import uuid4
from itertools import zip_longest
from collections import OrderedDict
from robot.libraries.BuiltIn import BuiltIn
from browserstack_sdk.bstack11ll11l1ll_opy_ import RobotHandler
from bstack_utils.capture import bstack11lll1lll1_opy_
from bstack_utils.bstack11lll1ll11_opy_ import bstack11ll11111l_opy_, bstack11lll11l1l_opy_, bstack11lll11l11_opy_
from bstack_utils.bstack1l11l1l1ll_opy_ import bstack1lll1l11_opy_
from bstack_utils.bstack11111l1l_opy_ import bstack11llllll11_opy_
from bstack_utils.constants import *
from bstack_utils.helper import bstack11l1ll1l1_opy_, bstack11l1l11l1_opy_, Result, \
    bstack11ll1ll111_opy_, bstack11ll1lll1l_opy_
class bstack_robot_listener:
    ROBOT_LISTENER_API_VERSION = 2
    store = {
        bstack111l1_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧช"): [],
        bstack111l1_opy_ (u"ࠫ࡬ࡲ࡯ࡣࡣ࡯ࡣ࡭ࡵ࡯࡬ࡵࠪซ"): [],
        bstack111l1_opy_ (u"ࠬࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡴࠩฌ"): []
    }
    bstack11ll11l11l_opy_ = []
    bstack11ll11ll1l_opy_ = []
    @staticmethod
    def bstack11llll11l1_opy_(log):
        if not (log[bstack111l1_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧญ")] and log[bstack111l1_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨฎ")].strip()):
            return
        active = bstack1lll1l11_opy_.bstack11lll1l1ll_opy_()
        log = {
            bstack111l1_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧฏ"): log[bstack111l1_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨฐ")],
            bstack111l1_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭ฑ"): bstack11ll1lll1l_opy_().isoformat() + bstack111l1_opy_ (u"ࠫ࡟࠭ฒ"),
            bstack111l1_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ณ"): log[bstack111l1_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧด")],
        }
        if active:
            if active[bstack111l1_opy_ (u"ࠧࡵࡻࡳࡩࠬต")] == bstack111l1_opy_ (u"ࠨࡪࡲࡳࡰ࠭ถ"):
                log[bstack111l1_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩท")] = active[bstack111l1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪธ")]
            elif active[bstack111l1_opy_ (u"ࠫࡹࡿࡰࡦࠩน")] == bstack111l1_opy_ (u"ࠬࡺࡥࡴࡶࠪบ"):
                log[bstack111l1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ป")] = active[bstack111l1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧผ")]
        bstack11llllll11_opy_.bstack1111l111_opy_([log])
    def __init__(self):
        self.messages = Messages()
        self._11ll1l1l11_opy_ = None
        self._11ll1l1111_opy_ = None
        self._11l1lll1ll_opy_ = OrderedDict()
        self.bstack11lll1ll1l_opy_ = bstack11lll1lll1_opy_(self.bstack11llll11l1_opy_)
    @bstack11ll1ll111_opy_(class_method=True)
    def start_suite(self, name, attrs):
        self.messages.bstack11ll1ll1l1_opy_()
        if not self._11l1lll1ll_opy_.get(attrs.get(bstack111l1_opy_ (u"ࠨ࡫ࡧࠫฝ")), None):
            self._11l1lll1ll_opy_[attrs.get(bstack111l1_opy_ (u"ࠩ࡬ࡨࠬพ"))] = {}
        bstack11l1llllll_opy_ = bstack11lll11l11_opy_(
                bstack11l1lll1l1_opy_=attrs.get(bstack111l1_opy_ (u"ࠪ࡭ࡩ࠭ฟ")),
                name=name,
                bstack11lll11ll1_opy_=bstack11l1l11l1_opy_(),
                file_path=os.path.relpath(attrs[bstack111l1_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫภ")], start=os.getcwd()) if attrs.get(bstack111l1_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬม")) != bstack111l1_opy_ (u"࠭ࠧย") else bstack111l1_opy_ (u"ࠧࠨร"),
                framework=bstack111l1_opy_ (u"ࠨࡔࡲࡦࡴࡺࠧฤ")
            )
        threading.current_thread().current_suite_id = attrs.get(bstack111l1_opy_ (u"ࠩ࡬ࡨࠬล"), None)
        self._11l1lll1ll_opy_[attrs.get(bstack111l1_opy_ (u"ࠪ࡭ࡩ࠭ฦ"))][bstack111l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧว")] = bstack11l1llllll_opy_
    @bstack11ll1ll111_opy_(class_method=True)
    def end_suite(self, name, attrs):
        messages = self.messages.bstack11l1ll1ll1_opy_()
        self._11l1llll1l_opy_(messages)
        for bstack11ll1ll1ll_opy_ in self.bstack11ll11l11l_opy_:
            bstack11ll1ll1ll_opy_[bstack111l1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴࠧศ")][bstack111l1_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬษ")].extend(self.store[bstack111l1_opy_ (u"ࠧࡨ࡮ࡲࡦࡦࡲ࡟ࡩࡱࡲ࡯ࡸ࠭ส")])
            bstack11llllll11_opy_.bstack11ll1l11ll_opy_(bstack11ll1ll1ll_opy_)
        self.bstack11ll11l11l_opy_ = []
        self.store[bstack111l1_opy_ (u"ࠨࡩ࡯ࡳࡧࡧ࡬ࡠࡪࡲࡳࡰࡹࠧห")] = []
    @bstack11ll1ll111_opy_(class_method=True)
    def start_test(self, name, attrs):
        self.bstack11lll1ll1l_opy_.start()
        if not self._11l1lll1ll_opy_.get(attrs.get(bstack111l1_opy_ (u"ࠩ࡬ࡨࠬฬ")), None):
            self._11l1lll1ll_opy_[attrs.get(bstack111l1_opy_ (u"ࠪ࡭ࡩ࠭อ"))] = {}
        driver = bstack11l1ll1l1_opy_(threading.current_thread(), bstack111l1_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪฮ"), None)
        bstack11lll1ll11_opy_ = bstack11lll11l11_opy_(
            bstack11l1lll1l1_opy_=attrs.get(bstack111l1_opy_ (u"ࠬ࡯ࡤࠨฯ")),
            name=name,
            bstack11lll11ll1_opy_=bstack11l1l11l1_opy_(),
            file_path=os.path.relpath(attrs[bstack111l1_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭ะ")], start=os.getcwd()),
            scope=RobotHandler.bstack11ll11llll_opy_(attrs.get(bstack111l1_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧั"), None)),
            framework=bstack111l1_opy_ (u"ࠨࡔࡲࡦࡴࡺࠧา"),
            tags=attrs[bstack111l1_opy_ (u"ࠩࡷࡥ࡬ࡹࠧำ")],
            hooks=self.store[bstack111l1_opy_ (u"ࠪ࡫ࡱࡵࡢࡢ࡮ࡢ࡬ࡴࡵ࡫ࡴࠩิ")],
            bstack11l1ll11l1_opy_=bstack11llllll11_opy_.bstack11l1llll11_opy_(driver) if driver and driver.session_id else {},
            meta={},
            code=bstack111l1_opy_ (u"ࠦࢀࢃࠠ࡝ࡰࠣࡿࢂࠨี").format(bstack111l1_opy_ (u"ࠧࠦࠢึ").join(attrs[bstack111l1_opy_ (u"࠭ࡴࡢࡩࡶࠫื")]), name) if attrs[bstack111l1_opy_ (u"ࠧࡵࡣࡪࡷุࠬ")] else name
        )
        self._11l1lll1ll_opy_[attrs.get(bstack111l1_opy_ (u"ࠨ࡫ࡧูࠫ"))][bstack111l1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥฺࠬ")] = bstack11lll1ll11_opy_
        threading.current_thread().current_test_uuid = bstack11lll1ll11_opy_.bstack11ll1l111l_opy_()
        threading.current_thread().current_test_id = attrs.get(bstack111l1_opy_ (u"ࠪ࡭ࡩ࠭฻"), None)
        self.bstack11lllll111_opy_(bstack111l1_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬ฼"), bstack11lll1ll11_opy_)
    @bstack11ll1ll111_opy_(class_method=True)
    def end_test(self, name, attrs):
        self.bstack11lll1ll1l_opy_.reset()
        bstack11ll11l1l1_opy_ = bstack11l1lll11l_opy_.get(attrs.get(bstack111l1_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬ฽")), bstack111l1_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧ฾"))
        self._11l1lll1ll_opy_[attrs.get(bstack111l1_opy_ (u"ࠧࡪࡦࠪ฿"))][bstack111l1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫเ")].stop(time=bstack11l1l11l1_opy_(), duration=int(attrs.get(bstack111l1_opy_ (u"ࠩࡨࡰࡦࡶࡳࡦࡦࡷ࡭ࡲ࡫ࠧแ"), bstack111l1_opy_ (u"ࠪ࠴ࠬโ"))), result=Result(result=bstack11ll11l1l1_opy_, exception=attrs.get(bstack111l1_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬใ")), bstack11lll111l1_opy_=[attrs.get(bstack111l1_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ไ"))]))
        self.bstack11lllll111_opy_(bstack111l1_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨๅ"), self._11l1lll1ll_opy_[attrs.get(bstack111l1_opy_ (u"ࠧࡪࡦࠪๆ"))][bstack111l1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫ็")], True)
        self.store[bstack111l1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡸ่࠭")] = []
        threading.current_thread().current_test_uuid = None
        threading.current_thread().current_test_id = None
    @bstack11ll1ll111_opy_(class_method=True)
    def start_keyword(self, name, attrs):
        self.messages.bstack11ll1ll1l1_opy_()
        current_test_id = bstack11l1ll1l1_opy_(threading.current_thread(), bstack111l1_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡨ้ࠬ"), None)
        bstack11lll1111l_opy_ = current_test_id if bstack11l1ll1l1_opy_(threading.current_thread(), bstack111l1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡩ๊࠭"), None) else bstack11l1ll1l1_opy_(threading.current_thread(), bstack111l1_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡳࡶ࡫ࡷࡩࡤ࡯ࡤࠨ๋"), None)
        if attrs.get(bstack111l1_opy_ (u"࠭ࡴࡺࡲࡨࠫ์"), bstack111l1_opy_ (u"ࠧࠨํ")).lower() in [bstack111l1_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧ๎"), bstack111l1_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫ๏")]:
            hook_type = bstack11ll111l1l_opy_(attrs.get(bstack111l1_opy_ (u"ࠪࡸࡾࡶࡥࠨ๐")), bstack11l1ll1l1_opy_(threading.current_thread(), bstack111l1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨ๑"), None))
            hook_name = bstack111l1_opy_ (u"ࠬࢁࡽࠨ๒").format(attrs.get(bstack111l1_opy_ (u"࠭࡫ࡸࡰࡤࡱࡪ࠭๓"), bstack111l1_opy_ (u"ࠧࠨ๔")))
            if hook_type in [bstack111l1_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡃࡏࡐࠬ๕"), bstack111l1_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡃࡏࡐࠬ๖")]:
                hook_name = bstack111l1_opy_ (u"ࠪ࡟ࢀࢃ࡝ࠡࡽࢀࠫ๗").format(bstack11ll11lll1_opy_.get(hook_type), attrs.get(bstack111l1_opy_ (u"ࠫࡰࡽ࡮ࡢ࡯ࡨࠫ๘"), bstack111l1_opy_ (u"ࠬ࠭๙")))
            bstack11ll111ll1_opy_ = bstack11lll11l1l_opy_(
                bstack11l1lll1l1_opy_=bstack11lll1111l_opy_ + bstack111l1_opy_ (u"࠭࠭ࠨ๚") + attrs.get(bstack111l1_opy_ (u"ࠧࡵࡻࡳࡩࠬ๛"), bstack111l1_opy_ (u"ࠨࠩ๜")).lower(),
                name=hook_name,
                bstack11lll11ll1_opy_=bstack11l1l11l1_opy_(),
                file_path=os.path.relpath(attrs.get(bstack111l1_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩ๝")), start=os.getcwd()),
                framework=bstack111l1_opy_ (u"ࠪࡖࡴࡨ࡯ࡵࠩ๞"),
                tags=attrs[bstack111l1_opy_ (u"ࠫࡹࡧࡧࡴࠩ๟")],
                scope=RobotHandler.bstack11ll11llll_opy_(attrs.get(bstack111l1_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬ๠"), None)),
                hook_type=hook_type,
                meta={}
            )
            threading.current_thread().current_hook_uuid = bstack11ll111ll1_opy_.bstack11ll1l111l_opy_()
            threading.current_thread().current_hook_id = bstack11lll1111l_opy_ + bstack111l1_opy_ (u"࠭࠭ࠨ๡") + attrs.get(bstack111l1_opy_ (u"ࠧࡵࡻࡳࡩࠬ๢"), bstack111l1_opy_ (u"ࠨࠩ๣")).lower()
            self.store[bstack111l1_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭๤")] = [bstack11ll111ll1_opy_.bstack11ll1l111l_opy_()]
            if bstack11l1ll1l1_opy_(threading.current_thread(), bstack111l1_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧ๥"), None):
                self.store[bstack111l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱࡳࠨ๦")].append(bstack11ll111ll1_opy_.bstack11ll1l111l_opy_())
            else:
                self.store[bstack111l1_opy_ (u"ࠬ࡭࡬ࡰࡤࡤࡰࡤ࡮࡯ࡰ࡭ࡶࠫ๧")].append(bstack11ll111ll1_opy_.bstack11ll1l111l_opy_())
            if bstack11lll1111l_opy_:
                self._11l1lll1ll_opy_[bstack11lll1111l_opy_ + bstack111l1_opy_ (u"࠭࠭ࠨ๨") + attrs.get(bstack111l1_opy_ (u"ࠧࡵࡻࡳࡩࠬ๩"), bstack111l1_opy_ (u"ࠨࠩ๪")).lower()] = { bstack111l1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ๫"): bstack11ll111ll1_opy_ }
            bstack11llllll11_opy_.bstack11lllll111_opy_(bstack111l1_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫ๬"), bstack11ll111ll1_opy_)
        else:
            bstack11lll11lll_opy_ = {
                bstack111l1_opy_ (u"ࠫ࡮ࡪࠧ๭"): uuid4().__str__(),
                bstack111l1_opy_ (u"ࠬࡺࡥࡹࡶࠪ๮"): bstack111l1_opy_ (u"࠭ࡻࡾࠢࡾࢁࠬ๯").format(attrs.get(bstack111l1_opy_ (u"ࠧ࡬ࡹࡱࡥࡲ࡫ࠧ๰")), attrs.get(bstack111l1_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭๱"), bstack111l1_opy_ (u"ࠩࠪ๲"))) if attrs.get(bstack111l1_opy_ (u"ࠪࡥࡷ࡭ࡳࠨ๳"), []) else attrs.get(bstack111l1_opy_ (u"ࠫࡰࡽ࡮ࡢ࡯ࡨࠫ๴")),
                bstack111l1_opy_ (u"ࠬࡹࡴࡦࡲࡢࡥࡷ࡭ࡵ࡮ࡧࡱࡸࠬ๵"): attrs.get(bstack111l1_opy_ (u"࠭ࡡࡳࡩࡶࠫ๶"), []),
                bstack111l1_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫ๷"): bstack11l1l11l1_opy_(),
                bstack111l1_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ๸"): bstack111l1_opy_ (u"ࠩࡳࡩࡳࡪࡩ࡯ࡩࠪ๹"),
                bstack111l1_opy_ (u"ࠪࡨࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠨ๺"): attrs.get(bstack111l1_opy_ (u"ࠫࡩࡵࡣࠨ๻"), bstack111l1_opy_ (u"ࠬ࠭๼"))
            }
            if attrs.get(bstack111l1_opy_ (u"࠭࡬ࡪࡤࡱࡥࡲ࡫ࠧ๽"), bstack111l1_opy_ (u"ࠧࠨ๾")) != bstack111l1_opy_ (u"ࠨࠩ๿"):
                bstack11lll11lll_opy_[bstack111l1_opy_ (u"ࠩ࡮ࡩࡾࡽ࡯ࡳࡦࠪ຀")] = attrs.get(bstack111l1_opy_ (u"ࠪࡰ࡮ࡨ࡮ࡢ࡯ࡨࠫກ"))
            if not self.bstack11ll11ll1l_opy_:
                self._11l1lll1ll_opy_[self._11ll1llll1_opy_()][bstack111l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧຂ")].add_step(bstack11lll11lll_opy_)
                threading.current_thread().current_step_uuid = bstack11lll11lll_opy_[bstack111l1_opy_ (u"ࠬ࡯ࡤࠨ຃")]
            self.bstack11ll11ll1l_opy_.append(bstack11lll11lll_opy_)
    @bstack11ll1ll111_opy_(class_method=True)
    def end_keyword(self, name, attrs):
        messages = self.messages.bstack11l1ll1ll1_opy_()
        self._11l1llll1l_opy_(messages)
        current_test_id = bstack11l1ll1l1_opy_(threading.current_thread(), bstack111l1_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡤࠨຄ"), None)
        bstack11lll1111l_opy_ = current_test_id if current_test_id else bstack11l1ll1l1_opy_(threading.current_thread(), bstack111l1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡵࡸ࡭ࡹ࡫࡟ࡪࡦࠪ຅"), None)
        bstack11l1ll1lll_opy_ = bstack11l1lll11l_opy_.get(attrs.get(bstack111l1_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨຆ")), bstack111l1_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪງ"))
        bstack11ll11ll11_opy_ = attrs.get(bstack111l1_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫຈ"))
        if bstack11l1ll1lll_opy_ != bstack111l1_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬຉ") and not attrs.get(bstack111l1_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ຊ")) and self._11ll1l1l11_opy_:
            bstack11ll11ll11_opy_ = self._11ll1l1l11_opy_
        bstack11llll1lll_opy_ = Result(result=bstack11l1ll1lll_opy_, exception=bstack11ll11ll11_opy_, bstack11lll111l1_opy_=[bstack11ll11ll11_opy_])
        if attrs.get(bstack111l1_opy_ (u"࠭ࡴࡺࡲࡨࠫ຋"), bstack111l1_opy_ (u"ࠧࠨຌ")).lower() in [bstack111l1_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧຍ"), bstack111l1_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫຎ")]:
            bstack11lll1111l_opy_ = current_test_id if current_test_id else bstack11l1ll1l1_opy_(threading.current_thread(), bstack111l1_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡸࡻࡩࡵࡧࡢ࡭ࡩ࠭ຏ"), None)
            if bstack11lll1111l_opy_:
                bstack11lll1l111_opy_ = bstack11lll1111l_opy_ + bstack111l1_opy_ (u"ࠦ࠲ࠨຐ") + attrs.get(bstack111l1_opy_ (u"ࠬࡺࡹࡱࡧࠪຑ"), bstack111l1_opy_ (u"࠭ࠧຒ")).lower()
                self._11l1lll1ll_opy_[bstack11lll1l111_opy_][bstack111l1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪຓ")].stop(time=bstack11l1l11l1_opy_(), duration=int(attrs.get(bstack111l1_opy_ (u"ࠨࡧ࡯ࡥࡵࡹࡥࡥࡶ࡬ࡱࡪ࠭ດ"), bstack111l1_opy_ (u"ࠩ࠳ࠫຕ"))), result=bstack11llll1lll_opy_)
                bstack11llllll11_opy_.bstack11lllll111_opy_(bstack111l1_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬຖ"), self._11l1lll1ll_opy_[bstack11lll1l111_opy_][bstack111l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧທ")])
        else:
            bstack11lll1111l_opy_ = current_test_id if current_test_id else bstack11l1ll1l1_opy_(threading.current_thread(), bstack111l1_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣ࡮ࡪࠧຘ"), None)
            if bstack11lll1111l_opy_ and len(self.bstack11ll11ll1l_opy_) == 1:
                current_step_uuid = bstack11l1ll1l1_opy_(threading.current_thread(), bstack111l1_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡴࡶࡨࡴࡤࡻࡵࡪࡦࠪນ"), None)
                self._11l1lll1ll_opy_[bstack11lll1111l_opy_][bstack111l1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪບ")].bstack11llll11ll_opy_(current_step_uuid, duration=int(attrs.get(bstack111l1_opy_ (u"ࠨࡧ࡯ࡥࡵࡹࡥࡥࡶ࡬ࡱࡪ࠭ປ"), bstack111l1_opy_ (u"ࠩ࠳ࠫຜ"))), result=bstack11llll1lll_opy_)
            else:
                self.bstack11l1lll111_opy_(attrs)
            self.bstack11ll11ll1l_opy_.pop()
    def log_message(self, message):
        try:
            if message.get(bstack111l1_opy_ (u"ࠪ࡬ࡹࡳ࡬ࠨຝ"), bstack111l1_opy_ (u"ࠫࡳࡵࠧພ")) == bstack111l1_opy_ (u"ࠬࡿࡥࡴࠩຟ"):
                return
            self.messages.push(message)
            bstack11ll11l111_opy_ = []
            if bstack1lll1l11_opy_.bstack11lll1l1ll_opy_():
                bstack11ll11l111_opy_.append({
                    bstack111l1_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩຠ"): bstack11l1l11l1_opy_(),
                    bstack111l1_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨມ"): message.get(bstack111l1_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩຢ")),
                    bstack111l1_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨຣ"): message.get(bstack111l1_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩ຤")),
                    **bstack1lll1l11_opy_.bstack11lll1l1ll_opy_()
                })
                if len(bstack11ll11l111_opy_) > 0:
                    bstack11llllll11_opy_.bstack1111l111_opy_(bstack11ll11l111_opy_)
        except Exception as err:
            pass
    def close(self):
        bstack11llllll11_opy_.bstack11l1ll11ll_opy_()
    def bstack11l1lll111_opy_(self, bstack11ll1111l1_opy_):
        if not bstack1lll1l11_opy_.bstack11lll1l1ll_opy_():
            return
        kwname = bstack111l1_opy_ (u"ࠫࢀࢃࠠࡼࡿࠪລ").format(bstack11ll1111l1_opy_.get(bstack111l1_opy_ (u"ࠬࡱࡷ࡯ࡣࡰࡩࠬ຦")), bstack11ll1111l1_opy_.get(bstack111l1_opy_ (u"࠭ࡡࡳࡩࡶࠫວ"), bstack111l1_opy_ (u"ࠧࠨຨ"))) if bstack11ll1111l1_opy_.get(bstack111l1_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ຩ"), []) else bstack11ll1111l1_opy_.get(bstack111l1_opy_ (u"ࠩ࡮ࡻࡳࡧ࡭ࡦࠩສ"))
        error_message = bstack111l1_opy_ (u"ࠥ࡯ࡼࡴࡡ࡮ࡧ࠽ࠤࡡࠨࡻ࠱ࡿ࡟ࠦࠥࢂࠠࡴࡶࡤࡸࡺࡹ࠺ࠡ࡞ࠥࡿ࠶ࢃ࡜ࠣࠢࡿࠤࡪࡾࡣࡦࡲࡷ࡭ࡴࡴ࠺ࠡ࡞ࠥࡿ࠷ࢃ࡜ࠣࠤຫ").format(kwname, bstack11ll1111l1_opy_.get(bstack111l1_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫຬ")), str(bstack11ll1111l1_opy_.get(bstack111l1_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ອ"))))
        bstack11ll1lllll_opy_ = bstack111l1_opy_ (u"ࠨ࡫ࡸࡰࡤࡱࡪࡀࠠ࡝ࠤࡾ࠴ࢂࡢࠢࠡࡾࠣࡷࡹࡧࡴࡶࡵ࠽ࠤࡡࠨࡻ࠲ࡿ࡟ࠦࠧຮ").format(kwname, bstack11ll1111l1_opy_.get(bstack111l1_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧຯ")))
        bstack11lll11111_opy_ = error_message if bstack11ll1111l1_opy_.get(bstack111l1_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩະ")) else bstack11ll1lllll_opy_
        bstack11ll111lll_opy_ = {
            bstack111l1_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬັ"): self.bstack11ll11ll1l_opy_[-1].get(bstack111l1_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧາ"), bstack11l1l11l1_opy_()),
            bstack111l1_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬຳ"): bstack11lll11111_opy_,
            bstack111l1_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫິ"): bstack111l1_opy_ (u"࠭ࡅࡓࡔࡒࡖࠬີ") if bstack11ll1111l1_opy_.get(bstack111l1_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧຶ")) == bstack111l1_opy_ (u"ࠨࡈࡄࡍࡑ࠭ື") else bstack111l1_opy_ (u"ࠩࡌࡒࡋࡕຸࠧ"),
            **bstack1lll1l11_opy_.bstack11lll1l1ll_opy_()
        }
        bstack11llllll11_opy_.bstack1111l111_opy_([bstack11ll111lll_opy_])
    def _11ll1llll1_opy_(self):
        for bstack11l1lll1l1_opy_ in reversed(self._11l1lll1ll_opy_):
            bstack11ll1l1ll1_opy_ = bstack11l1lll1l1_opy_
            data = self._11l1lll1ll_opy_[bstack11l1lll1l1_opy_][bstack111l1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦູ࠭")]
            if isinstance(data, bstack11lll11l1l_opy_):
                if not bstack111l1_opy_ (u"ࠫࡊࡇࡃࡉ຺ࠩ") in data.bstack11l1ll111l_opy_():
                    return bstack11ll1l1ll1_opy_
            else:
                return bstack11ll1l1ll1_opy_
    def _11l1llll1l_opy_(self, messages):
        try:
            bstack11ll1ll11l_opy_ = BuiltIn().get_variable_value(bstack111l1_opy_ (u"ࠧࠪࡻࡍࡑࡊࠤࡑࡋࡖࡆࡎࢀࠦົ")) in (bstack11ll1l1lll_opy_.DEBUG, bstack11ll1l1lll_opy_.TRACE)
            for message, bstack11ll1l1l1l_opy_ in zip_longest(messages, messages[1:]):
                name = message.get(bstack111l1_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧຼ"))
                level = message.get(bstack111l1_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ຽ"))
                if level == bstack11ll1l1lll_opy_.FAIL:
                    self._11ll1l1l11_opy_ = name or self._11ll1l1l11_opy_
                    self._11ll1l1111_opy_ = bstack11ll1l1l1l_opy_.get(bstack111l1_opy_ (u"ࠣ࡯ࡨࡷࡸࡧࡧࡦࠤ຾")) if bstack11ll1ll11l_opy_ and bstack11ll1l1l1l_opy_ else self._11ll1l1111_opy_
        except:
            pass
    @classmethod
    def bstack11lllll111_opy_(self, event: str, bstack11l1ll1l1l_opy_: bstack11ll11111l_opy_, bstack11l1ll1l11_opy_=False):
        if event == bstack111l1_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫ຿"):
            bstack11l1ll1l1l_opy_.set(hooks=self.store[bstack111l1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡪࡲࡳࡰࡹࠧເ")])
        if event == bstack111l1_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡱࡩࡱࡲࡨࡨࠬແ"):
            event = bstack111l1_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧໂ")
        if bstack11l1ll1l11_opy_:
            bstack11ll111l11_opy_ = {
                bstack111l1_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪໃ"): event,
                bstack11l1ll1l1l_opy_.bstack11ll111111_opy_(): bstack11l1ll1l1l_opy_.bstack11l1ll1111_opy_(event)
            }
            self.bstack11ll11l11l_opy_.append(bstack11ll111l11_opy_)
        else:
            bstack11llllll11_opy_.bstack11lllll111_opy_(event, bstack11l1ll1l1l_opy_)
class Messages:
    def __init__(self):
        self._11ll1111ll_opy_ = []
    def bstack11ll1ll1l1_opy_(self):
        self._11ll1111ll_opy_.append([])
    def bstack11l1ll1ll1_opy_(self):
        return self._11ll1111ll_opy_.pop() if self._11ll1111ll_opy_ else list()
    def push(self, message):
        self._11ll1111ll_opy_[-1].append(message) if self._11ll1111ll_opy_ else self._11ll1111ll_opy_.append([message])
class bstack11ll1l1lll_opy_:
    FAIL = bstack111l1_opy_ (u"ࠧࡇࡃࡌࡐࠬໄ")
    ERROR = bstack111l1_opy_ (u"ࠨࡇࡕࡖࡔࡘࠧ໅")
    WARNING = bstack111l1_opy_ (u"࡚ࠩࡅࡗࡔࠧໆ")
    bstack11ll1l11l1_opy_ = bstack111l1_opy_ (u"ࠪࡍࡓࡌࡏࠨ໇")
    DEBUG = bstack111l1_opy_ (u"ࠫࡉࡋࡂࡖࡉ່ࠪ")
    TRACE = bstack111l1_opy_ (u"࡚ࠬࡒࡂࡅࡈ້ࠫ")
    bstack11l1l1llll_opy_ = [FAIL, ERROR]
def bstack11l1lllll1_opy_(bstack11ll1lll11_opy_):
    if not bstack11ll1lll11_opy_:
        return None
    if bstack11ll1lll11_opy_.get(bstack111l1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢ໊ࠩ"), None):
        return getattr(bstack11ll1lll11_opy_[bstack111l1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣ໋ࠪ")], bstack111l1_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭໌"), None)
    return bstack11ll1lll11_opy_.get(bstack111l1_opy_ (u"ࠩࡸࡹ࡮ࡪࠧໍ"), None)
def bstack11ll111l1l_opy_(hook_type, current_test_uuid):
    if hook_type.lower() not in [bstack111l1_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩ໎"), bstack111l1_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭໏")]:
        return
    if hook_type.lower() == bstack111l1_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫ໐"):
        if current_test_uuid is None:
            return bstack111l1_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡁࡍࡎࠪ໑")
        else:
            return bstack111l1_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡆࡃࡆࡌࠬ໒")
    elif hook_type.lower() == bstack111l1_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪ໓"):
        if current_test_uuid is None:
            return bstack111l1_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡃࡏࡐࠬ໔")
        else:
            return bstack111l1_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡈࡅࡈࡎࠧ໕")