from xml.etree.ElementTree import Element, tostring

from defusedxml.minidom import parseString


def pretty_xml(elem: Element) -> str:
    rough = tostring(elem, encoding='unicode')
    parsed = parseString(rough)
    return parsed.toprettyxml(indent='  ')
