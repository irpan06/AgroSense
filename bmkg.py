import requests
import xml.etree.ElementTree as ET
# import numpy as np
# import pandas as pd

# Fungsi untuk mengunduh file XML dari URL
def download_xml(url, save_path):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
        with open(save_path, 'wb') as file:
            file.write(response.content)
        print(f"File successfully downloaded and saved as {save_path}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to download file: {e}")



def parse_weather_xml(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    humidity_data = []
    temperature_data = []
    
    for parameter in root.findall(".//parameter"):
        parameter_id = parameter.get('id')
        
        if parameter_id == 'hu':  # Kelembapan (Humidity)
            for timerange in parameter.findall('timerange'):
                datetime = timerange.get('datetime')
                value = timerange.find('value').text
                humidity_data.append({
                    'datetime': datetime,
                    'humidity': value
                })
        
        elif parameter_id == 't':  # Suhu (Temperature)
            for timerange in parameter.findall('timerange'):
                datetime = timerange.get('datetime')
                value = timerange.find('value').text
                temperature_data.append({
                    'datetime': datetime,
                    'temperature': value
                })
    
    return humidity_data, temperature_data


# URL ke file XML prediksi cuaca
xml_url = 'https://data.bmkg.go.id/DataMKG/MEWS/DigitalForecast/DigitalForecast-JawaTimur.xml'

# Path lokal untuk menyimpan file XML yang diunduh
xml_file_path = 'forecast.xml'

# Unduh file XML dari URL
download_xml(xml_url, xml_file_path)

humidity_data, temperature_data = parse_weather_xml(xml_file_path)
