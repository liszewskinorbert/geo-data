import csv
import re


def clean_data(line):
    # Podziel linię na pola za pomocą średnika
    fields = line.split(';')

    # Usuń spacje na początku i na końcu każdego pola
    cleaned_fields = [field.strip().replace('\xa0', '') for field in fields]

    for i in range(len(cleaned_fields)):
        # Usuń "ul. " oraz wszystko przed tym w polu
        index_ul = cleaned_fields[i].find("ul. ")
        if index_ul != -1:
            cleaned_fields[i] = cleaned_fields[i][index_ul + len("ul. "):].strip()

        # Sprawdź, czy ostatnie trzy znaki to cyfra, spacja i litera
        if len(cleaned_fields[i]) >= 3 and cleaned_fields[i][-3].isdigit() and cleaned_fields[i][-2] == ' ':
            cleaned_fields[i] = cleaned_fields[i][:-2] + cleaned_fields[i][-1]  # Usunięcie spacji

    return cleaned_fields


def is_postal_code(field):
    # Sprawdza, czy pole ma format dwie cyfry, dowolny znak, trzy cyfry
    return re.match(r'^\d{2}.\d{3}$', field) is not None


def is_city(field):
    # Sprawdza, czy pole nie zawiera cyfr
    return not any(char.isdigit() for char in field)


def main():
    filename = input("Podaj nazwę pliku CSV: ")
    records = []

    try:
        with open(filename, mode='r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for line in reader:
                # Oczyszczanie danych
                cleaned_fields = clean_data(';'.join(line))
                data_dict = {}

                # Przydzielanie pól do odpowiednich kluczy
                for field in cleaned_fields:
                    if is_postal_code(field):
                        data_dict['kod pocztowy'] = field
                    elif is_city(field):
                        data_dict['miejscowość'] = field
                    else:
                        data_dict['adres'] = field

                # Dodanie rekordu do listy
                records.append(data_dict)

        # Zapisanie oczyszczonych danych do pliku tekstowego
        with open('oczyszczone_dane.txt', mode='w', encoding='utf-8') as outfile:
            for record in records:
                # Przygotowanie linii do zapisu
                line = f"{record.get('adres', '')}, {record.get('kod pocztowy', '')} {record.get('miejscowość', '')}, Polska\n"
                outfile.write(line)

        print("Dane zostały zapisane do pliku 'oczyszczone_dane.txt'.")

    except FileNotFoundError:
        print("Plik nie został znaleziony.")
    except Exception as e:
        print(f"Wystąpił błąd: {e}")


if __name__ == "__main__":
    main()
