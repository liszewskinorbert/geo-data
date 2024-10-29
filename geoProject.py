import csv
import time
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

def read_addresses(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        addresses = [line.strip() for line in file.readlines()]
    return addresses

def geocode_address(address):
    geolocator = Nominatim(user_agent="your_custom_user_agent@example.com")  # Użyj swojego identyfikatora
    try:
        location = geolocator.geocode(address, timeout=10)
        if location:
            return (location.latitude, location.longitude)
        else:
            return None
    except (GeocoderTimedOut, GeocoderServiceError) as e:
        print(f"Błąd geokodowania dla adresu '{address}': {e}")
        return None

def write_results(results, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Adres', 'Szerokość', 'Długość'])
        for address, coords in results.items():
            if coords:
                writer.writerow([address, coords[0], coords[1]])
            else:
                writer.writerow([address, 'Brak danych', 'Brak danych'])

def main():
    input_file = 'oczyszczone_dane.txt'  # Plik wejściowy z danymi
    output_file = 'wyniki.csv'  # Plik wyjściowy z wynikami

    addresses = read_addresses(input_file)
    results = {}

    for address in addresses:
        # Zmiana adresu na format, który Nominatim rozumie
        address_formatted = address.replace(',', '').strip()
        coords = geocode_address(address_formatted)
        results[address] = coords
        time.sleep(2)  # Wstrzymanie wykonania na 2 sekundy

    write_results(results, output_file)
    print(f"Wyniki zostały zapisane do pliku: {output_file}")

if __name__ == '__main__':
    main()
