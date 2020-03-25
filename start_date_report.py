#!/usr/bin/env python3
import csv
import datetime
import requests

FILE_URL="http://marga.com.ar/employees-with-date.csv"

def get_start_date():
    """Interactively get the start date to query for."""

    print()
    print('Getting the first start date to query for.')
    print()
    print('The date must be greater than Jan 1st, 2018')
    year = int(input('Enter a value for the year: '))
    month = int(input('Enter a value for the month: '))
    day = int(input('Enter a value for the day: '))
    print()

    return datetime.datetime(year, month, day)

def list_newer(start_date):
    """Returns the employees that started on the given date, or the closest one."""
    file = open('employees-with-date.csv','w+')
    file.write(requests.get(FILE_URL, stream=True).content.decode("UTF-8"))
    data = file.readlines()
    file.close()
    reader = csv.reader(data[1:])

    # We want all employees that started at the same date or the closest newer
    # date. To calculate that, we go through all the data and find the
    # employees that started on the smallest date that's equal or bigger than
    # the given start date.

    sorted_list = []

    for item in reader:
        sorted_list.append(item)
        sorted_list.sort(key = sorted_list[3])

    for row in sorted_list:
        row_date = datetime.datetime.strptime(row[3], '%Y-%m-%d')

        if row_date >= start_date:
            print("Started on {} : {} {}".format(row_date.strftime("%b %d, %Y"),row[0], row[1]))

def main():
    start_date = get_start_date()
    list_newer(start_date)

if __name__ == "__main__":
    main()
