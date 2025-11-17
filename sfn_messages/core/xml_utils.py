from xml.dom import minidom
from xml.etree.ElementTree import tostring, Element

def pretty_xml(elem: Element) -> str:
    rough = tostring(elem, encoding='unicode')
    parsed = minidom.parseString(rough)
    return parsed.toprettyxml(indent='  ')
