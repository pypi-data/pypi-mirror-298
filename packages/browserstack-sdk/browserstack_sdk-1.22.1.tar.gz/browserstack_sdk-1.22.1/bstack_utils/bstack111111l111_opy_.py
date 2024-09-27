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
from _pytest import fixtures
from _pytest.python import _call_with_optional_argument
from pytest import Module, Class
from bstack_utils.helper import Result, bstack1111ll111l_opy_
from browserstack_sdk.bstack1l1lll11l_opy_ import bstack1l1lllllll_opy_
def _1111111l1l_opy_(method, this, arg):
    arg_count = method.__code__.co_argcount
    if arg_count > 1:
        method(this, arg)
    else:
        method(this)
class bstack1111111ll1_opy_:
    def __init__(self, handler):
        self._1llllllllll_opy_ = {}
        self._111111111l_opy_ = {}
        self.handler = handler
        self.patch()
        pass
    def patch(self):
        pytest_version = bstack1l1lllllll_opy_.version()
        if bstack1111ll111l_opy_(pytest_version, bstack111l1_opy_ (u"ࠣ࠺࠱࠵࠳࠷ࠢᑮ")) >= 0:
            self._1llllllllll_opy_[bstack111l1_opy_ (u"ࠩࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᑯ")] = Module._register_setup_function_fixture
            self._1llllllllll_opy_[bstack111l1_opy_ (u"ࠪࡱࡴࡪࡵ࡭ࡧࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᑰ")] = Module._register_setup_module_fixture
            self._1llllllllll_opy_[bstack111l1_opy_ (u"ࠫࡨࡲࡡࡴࡵࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᑱ")] = Class._register_setup_class_fixture
            self._1llllllllll_opy_[bstack111l1_opy_ (u"ࠬࡳࡥࡵࡪࡲࡨࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᑲ")] = Class._register_setup_method_fixture
            Module._register_setup_function_fixture = self.bstack1lllllll1l1_opy_(bstack111l1_opy_ (u"࠭ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᑳ"))
            Module._register_setup_module_fixture = self.bstack1lllllll1l1_opy_(bstack111l1_opy_ (u"ࠧ࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᑴ"))
            Class._register_setup_class_fixture = self.bstack1lllllll1l1_opy_(bstack111l1_opy_ (u"ࠨࡥ࡯ࡥࡸࡹ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᑵ"))
            Class._register_setup_method_fixture = self.bstack1lllllll1l1_opy_(bstack111l1_opy_ (u"ࠩࡰࡩࡹ࡮࡯ࡥࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᑶ"))
        else:
            self._1llllllllll_opy_[bstack111l1_opy_ (u"ࠪࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᑷ")] = Module._inject_setup_function_fixture
            self._1llllllllll_opy_[bstack111l1_opy_ (u"ࠫࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᑸ")] = Module._inject_setup_module_fixture
            self._1llllllllll_opy_[bstack111l1_opy_ (u"ࠬࡩ࡬ࡢࡵࡶࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᑹ")] = Class._inject_setup_class_fixture
            self._1llllllllll_opy_[bstack111l1_opy_ (u"࠭࡭ࡦࡶ࡫ࡳࡩࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᑺ")] = Class._inject_setup_method_fixture
            Module._inject_setup_function_fixture = self.bstack1lllllll1l1_opy_(bstack111l1_opy_ (u"ࠧࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᑻ"))
            Module._inject_setup_module_fixture = self.bstack1lllllll1l1_opy_(bstack111l1_opy_ (u"ࠨ࡯ࡲࡨࡺࡲࡥࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᑼ"))
            Class._inject_setup_class_fixture = self.bstack1lllllll1l1_opy_(bstack111l1_opy_ (u"ࠩࡦࡰࡦࡹࡳࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᑽ"))
            Class._inject_setup_method_fixture = self.bstack1lllllll1l1_opy_(bstack111l1_opy_ (u"ࠪࡱࡪࡺࡨࡰࡦࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᑾ"))
    def bstack1111111111_opy_(self, bstack1111111l11_opy_, hook_type):
        meth = getattr(bstack1111111l11_opy_, hook_type, None)
        if meth is not None and fixtures.getfixturemarker(meth) is None:
            self._111111111l_opy_[hook_type] = meth
            setattr(bstack1111111l11_opy_, hook_type, self.bstack11111111l1_opy_(hook_type))
    def bstack11111111ll_opy_(self, instance, bstack1llllllll1l_opy_):
        if bstack1llllllll1l_opy_ == bstack111l1_opy_ (u"ࠦ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠢᑿ"):
            self.bstack1111111111_opy_(instance.obj, bstack111l1_opy_ (u"ࠧࡹࡥࡵࡷࡳࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࠨᒀ"))
            self.bstack1111111111_opy_(instance.obj, bstack111l1_opy_ (u"ࠨࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡨࡸࡲࡨࡺࡩࡰࡰࠥᒁ"))
        if bstack1llllllll1l_opy_ == bstack111l1_opy_ (u"ࠢ࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࠣᒂ"):
            self.bstack1111111111_opy_(instance.obj, bstack111l1_opy_ (u"ࠣࡵࡨࡸࡺࡶ࡟࡮ࡱࡧࡹࡱ࡫ࠢᒃ"))
            self.bstack1111111111_opy_(instance.obj, bstack111l1_opy_ (u"ࠤࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲࡵࡤࡶ࡮ࡨࠦᒄ"))
        if bstack1llllllll1l_opy_ == bstack111l1_opy_ (u"ࠥࡧࡱࡧࡳࡴࡡࡩ࡭ࡽࡺࡵࡳࡧࠥᒅ"):
            self.bstack1111111111_opy_(instance.obj, bstack111l1_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࡢࡧࡱࡧࡳࡴࠤᒆ"))
            self.bstack1111111111_opy_(instance.obj, bstack111l1_opy_ (u"ࠧࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡤ࡮ࡤࡷࡸࠨᒇ"))
        if bstack1llllllll1l_opy_ == bstack111l1_opy_ (u"ࠨ࡭ࡦࡶ࡫ࡳࡩࡥࡦࡪࡺࡷࡹࡷ࡫ࠢᒈ"):
            self.bstack1111111111_opy_(instance.obj, bstack111l1_opy_ (u"ࠢࡴࡧࡷࡹࡵࡥ࡭ࡦࡶ࡫ࡳࡩࠨᒉ"))
            self.bstack1111111111_opy_(instance.obj, bstack111l1_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡪࡺࡨࡰࡦࠥᒊ"))
    @staticmethod
    def bstack1111111lll_opy_(hook_type, func, args):
        if hook_type in [bstack111l1_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠ࡯ࡨࡸ࡭ࡵࡤࠨᒋ"), bstack111l1_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳࡥࡵࡪࡲࡨࠬᒌ")]:
            _1111111l1l_opy_(func, args[0], args[1])
            return
        _call_with_optional_argument(func, args[0])
    def bstack11111111l1_opy_(self, hook_type):
        def bstack1llllllll11_opy_(arg=None):
            self.handler(hook_type, bstack111l1_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࠫᒍ"))
            result = None
            exception = None
            try:
                self.bstack1111111lll_opy_(hook_type, self._111111111l_opy_[hook_type], (arg,))
                result = Result(result=bstack111l1_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬᒎ"))
            except Exception as e:
                result = Result(result=bstack111l1_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᒏ"), exception=e)
                self.handler(hook_type, bstack111l1_opy_ (u"ࠧࡢࡨࡷࡩࡷ࠭ᒐ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack111l1_opy_ (u"ࠨࡣࡩࡸࡪࡸࠧᒑ"), result)
        def bstack1lllllllll1_opy_(this, arg=None):
            self.handler(hook_type, bstack111l1_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࠩᒒ"))
            result = None
            exception = None
            try:
                self.bstack1111111lll_opy_(hook_type, self._111111111l_opy_[hook_type], (this, arg))
                result = Result(result=bstack111l1_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪᒓ"))
            except Exception as e:
                result = Result(result=bstack111l1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᒔ"), exception=e)
                self.handler(hook_type, bstack111l1_opy_ (u"ࠬࡧࡦࡵࡧࡵࠫᒕ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack111l1_opy_ (u"࠭ࡡࡧࡶࡨࡶࠬᒖ"), result)
        if hook_type in [bstack111l1_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥ࡭ࡦࡶ࡫ࡳࡩ࠭ᒗ"), bstack111l1_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡪࡺࡨࡰࡦࠪᒘ")]:
            return bstack1lllllllll1_opy_
        return bstack1llllllll11_opy_
    def bstack1lllllll1l1_opy_(self, bstack1llllllll1l_opy_):
        def bstack1lllllll1ll_opy_(this, *args, **kwargs):
            self.bstack11111111ll_opy_(this, bstack1llllllll1l_opy_)
            self._1llllllllll_opy_[bstack1llllllll1l_opy_](this, *args, **kwargs)
        return bstack1lllllll1ll_opy_