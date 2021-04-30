"""
In current script we create a file with all the supported cities.
"""
INPUT_FILENAME = 'city.list.json'
OUTPUT_FILENAME = 'city.txt'


def get_cities_names():
    with open(INPUT_FILENAME) as input_file:
        with open(OUTPUT_FILENAME, 'a+') as output_file:
            for line in input_file:
                if "name" in line:
                    name = line.split(" ")[-1].replace('"', '').replace(',', '')
                    output_file.write(name)


if __name__ == '__main__':
    get_cities_names()
