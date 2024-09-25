import auto_press
import time
from auto_click.auto_click_by_point_utils import AutoClickUtils

positions = [(1125, 374), (947, 836),(947, 836)]
from moniter.moniter_keyboard_utils import MoniterKeyboardUtils

token = False


def func():
    global token
    token = True


with MoniterKeyboardUtils('esc', func) as m:
    # time.sleep(3)
    while not token:
        #     auto_press.AutoPressUtils.press_keys_together(['ctrl', 'v'])
        #     time.sleep(0.5)
        #     auto_press.AutoPressUtils.press_key('enter')
        #     time.sleep(30)
        AutoClickUtils().click_positions(positions, intervals=1)
        time.sleep(0.5)
