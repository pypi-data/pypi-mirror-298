import xml.etree.ElementTree as ET
import csv

def flatten_record(record):
    """ Flatten a nested XML record into a flat dictionary. """
    flat_record = {}
    
    def flatten_element(element, parent_key=''):
        """ Recursive function to flatten nested XML elements. """
        for child in element:
            key = f"{parent_key}{child.tag}" if parent_key else child.tag
            if len(child):
                flatten_element(child, key + '_')
            else:
                flat_record[key] = child.text
    
    flatten_element(record)
    return flat_record

def xml_to_csv(xml_file, csv_file):
    # Parse the XML file
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    # Collect headers and records
    headers = set()
    records = []
    
    for record in root.findall('record'):
        flat_record = flatten_record(record)
        headers.update(flat_record.keys())
        records.append(flat_record)
    
    headers = sorted(headers)
    
    # Write data to CSV file
    with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(headers)
        for record in records:
            row = [record.get(header, '') for header in headers]
            csvwriter.writerow(row)

# Define the XML and CSV file paths
xml_file = input("Enter the path of your XML file: ")
csv_file = input("Enter the name of the CSV file (without extension): ") + ".csv"

# Convert XML to CSV
xml_to_csv(xml_file, csv_file)
print(f'Converted {xml_file} to {csv_file}')
