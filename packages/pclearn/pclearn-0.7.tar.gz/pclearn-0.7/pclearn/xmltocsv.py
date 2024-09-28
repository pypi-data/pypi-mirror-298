import xml.etree.ElementTree as ET
import csv
def flatten_record(record):
    flat_record = {}    
    def flatten_element(element, parent_key=''):
        for child in element:
            key = f"{parent_key}{child.tag}" if parent_key else child.tag
            if len(child):
                flatten_element(child, key + '_')
            else:
                flat_record[key] = child.text    
    flatten_element(record)
    return flat_record
def convert_xml_to_csv(input_xml, output_csv):
    tree = ET.parse(input_xml)
    root = tree.getroot()    
    column_headers = set()
    data_rows = []    
    for record in root.findall('record'):
        flat_record = flatten_record(record)
        column_headers.update(flat_record.keys())
        data_rows.append(flat_record)    
    column_headers = sorted(column_headers)    
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(column_headers)
        for row_data in data_rows:
            row = [row_data.get(header, '') for header in column_headers]
            csv_writer.writerow(row)
input_xml = input("Enter the path of your XML file: ")
output_csv = input("Enter the name of the CSV file (without extension): ") + ".csv"
convert_xml_to_csv(input_xml, output_csv)
print(f'Converted {input_xml} to {output_csv}')























<?xml version="1.0" encoding="UTF-8"?>
<root>
    <record>
        <name>Amit Sharma</name>
        <age>28</age>
        <address>
            <city>Mumbai</city>
            <zipcode>400001</zipcode>
        </address>
    </record>
    <record>
        <name>Priya Patel</name>
        <age>32</age>
        <address>
            <city>Delhi</city>
            <zipcode>110001</zipcode>
        </address>
    </record>
    <record>
        <name>Ravi Kumar</name>
        <age>40</age>
        <address>
            <city>Bangalore</city>
            <zipcode>560001</zipcode>
        </address>
    </record>
    <record>
        <name>Neha Singh</name>
        <age>27</age>
        <address>
            <city>Kolkata</city>
            <zipcode>700001</zipcode>
        </address>
    </record>
    <record>
        <name>Suresh Reddy</name>
        <age>45</age>
        <address>
            <city>Hyderabad</city>
            <zipcode>500001</zipcode>
        </address>
    </record>
</root>
