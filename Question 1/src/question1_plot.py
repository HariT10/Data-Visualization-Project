#!/usr/bin/env python3

'''
question1_plot.py
  Author(s): Simon Tenedero (1268815), Timothy Weinhardt (1236676), Harishan Thilakanathan (1274198)
  Earlier contributors(s): Andrew Hamilton-Wright

  Project: Team Project - Question 1
  Date of Last Update: March 19, 2024.

  Functional Summary
      question1_plot.py reads a CSV file and saves
      a bar plot based on the data to a PDF file.

     Commandline Parameters: 2
        sys.argv[0] = name of file to read
        sys.argv[1] = name of graphics file to create
'''

#
#   Packages and modules
#
import sys
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

def main(argv):

    #
    #   Check that we have been given the right number of parameters,
    #   and store the single command line argument in a variable with
    #   a better name
    #
    if len(argv) != 3:
        print("Usage:",
                "create_name_plot.py <data file> <graphics file>")
        sys.exit(-1)

    csv_filename = argv[1]
    graphics_filename = argv[2]

    #
    #   Open the file and save the first line in a variable.
    #   This is the title of the graph.
    #
    file = open(csv_filename, "r")
    graph_title = file.readline()

    #
    # Open the data file using "pandas", which will attempt to read
    # in the entire CSV file, excluding the first row.
    #
    try:
        csv_df = pd.read_csv(csv_filename, skiprows=1)

    except IOError as err:
        print("Unable to open source file", csv_filename,
                ": {}".format(err), file=sys.stderr)
        sys.exit(-1)

    # At this point in the file, we begin to do the plotting

    # We must get the figure before we plot to it, or nothing will show up.
    # The matplotlib "figure" is the data environment that we are drawing
    # our plot into.  The seaborn library will draw onto this figure.
    # We don't see seaborn directly refer to "fig" because it is internally
    # drawing on "the current figure" which is the same one we are
    # referencing on this line.
    fig = plt.figure()

    # This creates a lineplot using seaborn.  We simply refer to
    # the various columns of data we want in our pandas data structure.
    sns.barplot(csv_df, x = "Provinces", y = "Propotion of Job Vacancies (%)").set(title=graph_title)
    plt.xticks(rotation=45, horizontalalignment='right')

    # Now we can save the matplotlib figure that seaborn has drawn
    # for us to a file
    fig.savefig(graphics_filename, bbox_inches="tight")

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