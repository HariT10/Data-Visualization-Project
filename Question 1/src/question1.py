#!/usr/bin/env python

'''
question1.py
  Author(s): Simon Tenedero (1268815), Timothy Weinhardt (1236676), Harishan Thilakanathan (1274198)
  Earlier contributors(s): Deborah Stacey, Andrew Hamilton-Wright

  Project: Team Project - Question 1
  Date of Last Update: March 18, 2024.

  Functional Summary
      question1.py takes in a CSV (comma separated version) file and calculates the proportion of
      job vacancies for a given National Occupation Classification (NOC) category for each province.

      The file outputs data so that it can be redirected into a seperate file for visualizaion.

     Commandline Parameters: 3
        argv[1] = Name of the pre-processed job vacancies file
        argv[2] = Name of the pre-processed job occupancies file
        argv[3] = National Occupation Clasification Index (0-10)

     References
        Job vacancy data from https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1410032801
        Job occupancy data from https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1410042101
'''

#
#   Packages and modules
#
import sys
import csv
import re

def main(argv):

    #
    #   Check that we have been given the right number of parameters,
    #   and store the single command line argument in a variable with
    #   a better name
    #
    if len(argv) != 4:
        print("Usage: pre_process_data.py <vacancies file name> <occupations file name> <noc cateogory [0-9]>",file=sys.stderr)
        sys.exit(1)

    vacancies_filename = argv[1]
    occupations_filename = argv[2]
    noc_chosen_cateogory = argv[3]


    # Check if the NOC index paramater is an integer
    try:
        noc_chosen_cateogory = (int)(noc_chosen_cateogory)
    except ValueError as err:
        print(" Usage: pre_process_data.py <vacancies file name> <occupations file name> <noc cateogory> ", file=sys.stderr)
        sys.exit(1)

    # Create two parallel arrays to store province data
    provinces = []
    provinces_data = []

    # Create an array of each National Occupational Classification Category by name
    noc_cateogories = ["Management occupations", "Business, finance and administration occupations", "Natural and applied sciences and related occupations", "Health occupations", "Occupations in education, law and social, community and government services", "Occupations in art, culture, recreation and sport", "Sales and service occupations", "Trades, transport and equipment operators and related occupations", "Natural resources, agriculture and related production occupations", "Occupations in manufacturing and utilities"]

    # Check if the NOC index paramater is an integer from (0-10)
    if noc_chosen_cateogory < 0 or noc_chosen_cateogory > len(noc_cateogories) - 1:
        print("Please enter a valid national occupational classification cateogory [0-{}]".format(len(noc_cateogories) -1), file=sys.stderr)
        sys.exit(1)

    # Save the chosen category name in a new variable
    chosen_cateogory = noc_cateogories[noc_chosen_cateogory]

    #
    # Open the vacancy data input file.
    #
    try:
        data_fh = open(vacancies_filename, encoding="utf-8-sig")

    except IOError as err:
        print("Unable to open names file '{}' : {}".format(
                vacancies_filename, err), file=sys.stderr)
        sys.exit(1)

    #
    # Create a CSV (Comma Separated Value) reader based on this
    # open file handle.  We can use the reader in a loop iteration
    # in order to access each line in turn.
    #
    data_reader = csv.reader(data_fh)


    #   Parse each line of data from the CSV reader, which will break
    #   the lines into fields based on the comma delimiter.
    #
    #   The field for each line are stored in a different row data array
    #   for each line of the data.
    #
    #   We then take the data and assign them into a "tuple" which we
    #   can store in the provinces and province data arrays for later use
    #
    line_number = 0
    for row_data_fields in data_reader:

        if line_number != 0:

            noc_value = row_data_fields[1]

            # Since the job occupancies data set does not include teritorries, exclude them from the data
            if row_data_fields[0] != "Canada" and row_data_fields[0] != "Northwest Territories" and row_data_fields[0] != "Nunavut" and row_data_fields[0] != "Yukon":

                if re.search(chosen_cateogory, noc_value):
                    provinces.append(row_data_fields[0])
                    provinces_data.append(float(row_data_fields[2]))

        line_number += 1

    #
    # Open the occupancy data input file.
    #
    try:
        data_fh = open(occupations_filename, encoding="utf-8-sig")

    except IOError as err:
        print("Unable to open names file '{}' : {}".format(
                occupations_filename, err), file=sys.stderr)
        sys.exit(1)


    data_reader = csv.reader(data_fh)

    #   Parse each line of data from the CSV reader, which will break
    #   the lines into fields based on the comma delimiter.
    #
    #   The field for each line are stored in a different row data array
    #   for each line of the data.
    #
    #   We then take the data and calculate the proportion of job vacanies
    #   for each province in the provinces/province data arrays.
    #
    line_number = 0

    for row_data_fields in data_reader:
        if line_number != 0:

            noc_value = row_data_fields[1]

            # Once again, we are excluding territories from the data set
            if row_data_fields[0] != "Canada" or row_data_fields[0] != "Northwest Territories" or row_data_fields[0] != "Nunavut" or row_data_fields[0] != "Yukon":

                if re.search(chosen_cateogory, noc_value):

                    number_of_occupations = float(row_data_fields[2])

                    # Iterate through the provinces array and check if this line matches the province
                    for i in range(0,len(provinces)):

                        if row_data_fields[0] == provinces[i]:

                            provinces_data[i] = (provinces_data[i]) / (provinces_data[i] + (number_of_occupations * 1000))
        line_number += 1

    #
    #   Print file output, encoded as a CSV
    #
    print("Proportion of Job Vacancies for {} [{}], per province".format(chosen_cateogory, noc_chosen_cateogory))
    print("Provinces,Propotion of Job Vacancies (%)")
    for i in range(0, len(provinces)):
        print("{},{}".format(provinces[i], round(provinces_data[i]*100, 3)))
    
    #
    #   End of Function
    #

##
## Call our main function, passing the system argv as the parameter
##
main(sys.argv)

#
#   End of Script
#