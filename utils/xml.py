import re
from typing import Union, List

import lxml.etree as ET

from utils.logger import print_and_log


def find_els(xml: str, node_attr: str, node_attr_val: str):    
    root = ET.fromstring(xml.encode())
    xpath = f".//node[@{node_attr}='{node_attr_val}']"
    return root.findall(xpath)


def find_els_by_xpath(xml: str, xpath: str):
    root = ET.fromstring(xml.encode())
    return root.findall(xpath)


def get_el_attrib_val(xml: str, el_attr: str, el_attr_val, attr_to_get: str, el_idx: int = 0) -> Union[None, str]:
    els = find_els(xml, el_attr, el_attr_val)
    if len(els) > el_idx:
        return els[el_idx].attrib.get(attr_to_get, None)


def get_text_xyxy(self, text: str) -> List[int]:
    bounds = get_el_attrib_val(self.adb.get_screen_xml(), 'text', text, 'bounds')
    return str_bounds_to_xyxy(bounds)


def str_bounds_to_xyxy(bounds: str):
    min_x, min_y = bounds.split('][')[0].split(',')
    max_x, max_y = bounds.split('][')[1].split(',')
    min_x = min_x.replace('[', '')
    max_y = max_y.replace(']', '')
    return int(min_x), int(min_y), int(max_x), int(max_y)


def el_to_str(el: ET) -> str:
    return ET.tostring(el, encoding='unicode')
