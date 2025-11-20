from xml.etree import ElementTree as ET

from defusedxml.ElementTree import fromstring
from pydantic import ValidationError


def extract_missing_fields(exc: ValidationError) -> set[str]:
    return {str(err['loc'][0]) for err in exc.errors() if err['type'] == 'missing'}


def normalize_xml(xml: str) -> str:
    root = fromstring(xml)

    def _strip_ws(elem: ET.Element) -> None:
        if elem.text is not None and elem.text.strip() == '':
            elem.text = None
        if elem.tail is not None and elem.tail.strip() == '':
            elem.tail = None
        for child in elem:
            _strip_ws(child)

    _strip_ws(root)
    return ET.tostring(root, encoding='unicode')
