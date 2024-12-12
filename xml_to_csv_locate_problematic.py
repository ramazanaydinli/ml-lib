import xml.etree.ElementTree as ET
import os





def xml_to_csv(path):
    xml_list = []
    for xml_file in glob.glob(path + "/*.xml"):
        print(f"Processing: {xml_file}")  # Log the file being processed
        try:
            tree = ET.parse(xml_file)
            root = tree.getroot()
            # Continue processing...
        except ET.ParseError as e:
            print(f"Error parsing {xml_file}: {e}")
            continue
    return pd.DataFrame(xml_list)