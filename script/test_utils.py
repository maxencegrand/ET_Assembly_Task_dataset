import sys
import traceback

from test.utils.test_position import test_position
from test.utils.test_device import test_device
from test.utils.test_state import test_state
from test.utils.test_block import test_block
from test.utils.test_event import test_event


test_position()
test_block()
test_event()
test_device()
test_state()
