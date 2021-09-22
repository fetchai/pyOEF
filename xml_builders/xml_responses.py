"""
<?xml version="1.0" encoding="UTF-8"?>
<response>
    <code>400</code>
    <reason>Bad Request</reason>
    <detail>agent lookup failed, 4 param(s) received</detail>
</response>
"""
import xml.etree.ElementTree as ET


def generate_error_xml(error) -> bytes:
    root = ET.Element("response")
    code = ET.SubElement(root, "code")
    code.text = "403"
    reason = ET.SubElement(root, "reason")
    reason.text = "Forbidden"
    detail = ET.SubElement(root, "detail")
    detail.text = error
    return ET.tostring(root)

"""
<?xml version="1.0" encoding="UTF-8"?>
<response>
    <encrypted>0</encrypted>
    <token>DEDC5BFDA0857F84FADC07251AB18</token>
    <page_address>oef_7CDC38925ED596873753465F764FFCFCCFBF1F47CD432FB96AE36188AA917A93</page_address>
</response>
"""


def registered_success_xml(unique_url, soef_token) -> bytes:
    root = ET.Element('response')
    encrypted = ET.SubElement(root, "encrypted")
    encrypted.text = '0'
    token = ET.SubElement(root, 'token')
    token.text = soef_token
    page_address = ET.SubElement(root, 'page_address')
    page_address.text = unique_url
    return ET.tostring(root)

"""
<?xml version="1.0" encoding="UTF-8"?>
<response>
    <code>400</code>
    <reason>Bad Request</reason>
    <detail>lobby to agent transition error</detail>
</response>"""

