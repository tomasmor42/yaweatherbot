from Levenshtein import distance

from consts import BIG_INT


def check_closest_city(city):
    min_distance = BIG_INT
    closet_cities = []
    city = city.lower()
    with open('city.txt') as cities:
        for line in cities:
            line = line.strip('\n').lower()
            dist = distance(line, city)
            if dist < min_distance:
                min_distance = dist
                closet_cities = [line]
            elif dist == min_distance:
                closet_cities.append(line)
    return closet_cities
