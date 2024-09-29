import csv


__ALL__ = ['cities', 'countries', 'regions', 'states', 'subregions']


def cities():
    with open('cities.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            yield row


def countries():
    with open('countries.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            yield row


def regions():
    with open('regions.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            yield row


def states():
    with open('states.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            yield row


def subregions():
    with open('subregions.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            yield row
