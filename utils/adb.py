import enum
import time
import os
from typing import Union, List

from dotmap import DotMap

from utils.logger import print_and_log
from utils.system import exec_cmd
from utils.xml import find_els, str_bounds_to_xyxy

CONNECTED_DEVICES_CMD = '{} devices'
CONNECT_DEVICE_CMD = '{} connect {}'
GET_SCREEN_SIZE = '{} shell wm size'
SWIPE_CMD = '{} shell input touchscreen swipe {} {} {} {} {}'
DUMP_SCREEN_XML_CMD = '{} shell uiautomator dump && adb pull /sdcard/window_dump.xml'
TAP_AT_XY_CMD = '{} shell input tap {} {}'
ADD_TEXT = "{} shell input text '{}'"
PRESS_KEY = '{} shell input keyevent {}'

KEYCODES = DotMap({
    'DEL': 'KEYCODE_DEL',
    'MOVE_END': 'KEYCODE_MOVE_END',
    'BACK': 'KEYCODE_BACK'
})

DUMPED_XML_NAME = 'window_dump.xml'


class ADB:

    def __init__(self, adb_path: str, device_addr: str):
        self.adb_path = adb_path
        self.device_addr = device_addr
        self.screen_w, self.screen_h = self.get_screen_size()
        print('ss:', self.screen_w, self.screen_h)
        # self.screen_w, self.screen_h = 1440, 2960

    def connect_device(self, tries: int = 3) -> bool:
        """
        connects to the device
        param: device_addr ip:port
        """
        for _ in range(tries):
            exec_cmd(CONNECT_DEVICE_CMD.format(self.adb_path, self.device_addr))
            if self.device_addr in exec_cmd(CONNECTED_DEVICES_CMD.format(self.adb_path)):
                return True
            time.sleep(1)

        return False

    def get_screen_size(self):
        screen_size = exec_cmd(GET_SCREEN_SIZE.format(self.adb_path))
        print_and_log(f'screen_size: {screen_size}')
        screen_size = screen_size.split(': ')[-1].replace('\\n', '').replace('\\r', '').replace('\'', '')
        w, h = screen_size.split('x')
        return int(w), int(h)

    def get_screen_xml(self, iters: int = 5, wait_btw_each_iter: int = 1) -> Union[None, str]:
        # if os.path.exists(DUMPED_XML_NAME):
        #     os.remove(DUMPED_XML_NAME)

        for _ in range(iters):
            exec_cmd(DUMP_SCREEN_XML_CMD.format(self.adb_path))

            if not os.path.exists(DUMPED_XML_NAME):
                self.connect_device()
                continue

            with open(DUMPED_XML_NAME, 'r', encoding='utf-8') as f:
                page_src = f.read()

            if page_src == "b''" or page_src == 'b\'UI hierchary dumped to: /dev/tty\\n\'':
                self.connect_device()
            else:
                return page_src

            time.sleep(wait_btw_each_iter)

    def swipe_until_txt_is_in_screen(self, txt: str, swipe_x1: int, swipe_y1: int, swipe_x2: int, swipe_y2: int,
                                     duration: int = 500, num_swipes: int = 10):
        for _ in range(0, num_swipes):
            if self.is_text_in_screen(txt, 1, 1):
                return True
            self.swipe(swipe_x1, swipe_y1, swipe_x2, swipe_y2, duration)
        return False

    def tap_el(self, el_attr: str, el_attr_val: str, el_idx: int = 0, screen_xml: str=None):
        if screen_xml is None:
            screen_xml = self.get_screen_xml()
        
        els = find_els(screen_xml, el_attr, el_attr_val)
        if len(els) > el_idx:
            x, y, _, _ = str_bounds_to_xyxy(els[el_idx].attrib['bounds'])
            exec_cmd(TAP_AT_XY_CMD.format(self.adb_path, x, y))

    def tap_at(self, x: int, y: int):
        exec_cmd(TAP_AT_XY_CMD.format(self.adb_path, x, y))

    def add_txt(self, txt: str):
        exec_cmd(ADD_TEXT.format(self.adb_path, txt))

    def is_text_in_screen(self, txt: str, iterations: int = 5, wait_btw_each_iteration: int = 1) -> bool:
        for i in range(iterations):
            screen_xml = self.get_screen_xml()
            if txt in screen_xml:
                return True
            elif screen_xml == "b''":
                self.connect_emulator()
            time.sleep(wait_btw_each_iteration)

        return False

    def are_texts_in_screen(self, txts: List, iterations: int = 5, wait_btw_each_iteration: int = 1) -> bool:
        for _ in range(iterations):
            screen_xml = self.get_screen_xml()
            if screen_xml == "b''":
                self.connect_emulator()
            else:
                found = []
                for txt in txts:
                    if txt in screen_xml:
                        found.append(True)
                    else:
                        found.append(False)
                if sum(found) == len(found):
                    return True
                    
            time.sleep(wait_btw_each_iteration)

        return False

    def swipe(self, x1: int, y1: int, x2: int, y2: int, duration: int = 500):
        exec_cmd(SWIPE_CMD.format(self.adb_path, x1, y1, x2, y2, duration))

    def press_del_key(self, num_presses: int = 1):
        for _ in range(num_presses):
            exec_cmd(PRESS_KEY.format(self.adb_path, KEYCODES.DEL))

    def press_end_key(self, num_presses: int = 1):
        for _ in range(0, num_presses):
            exec_cmd(PRESS_KEY.format(self.adb_path, KEYCODES.MOVE_END))
    
    def press_back_key(self, num_presses: int = 1):
        for _ in range(0, num_presses):
            exec_cmd(PRESS_KEY.format(self.adb_path, KEYCODES.BACK))

    def save_screenshot(self, file_path: str):
        exec_cmd('{} exec-out screencap -p > "{}"'.format(self.adb_path, file_path))

    def remove_exiting_text(self, el_attr: str, el_attr_val: str, el_idx: int = 0):
        el = find_els(self.get_screen_xml(), el_attr, el_attr_val)[el_idx]

        el_text, el_bounds = el.attrib['text'], el.attrib['bounds']
        x, y, _, _ = str_bounds_to_xyxy(el_bounds)
        self.tap_at(x, y)
        self.press_end_key()
        self.press_del_key(len(el_text))
