from elementtree.ElementTree import XML

def parse_error(xml_str):
    error = {}
    elem = XML(xml_str)
    error['id'] = elem.attrib['id']
    error['code'] = elem.attrib['code']
    error['aux_code'] = elem.attrib['auxCode']
    error['message'] = elem.text
    
    return error