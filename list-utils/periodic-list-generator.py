'''

Generate a list of all the items of a periodic input.
For example for monthly input generate an item for each month

'''

### Module(s) importation ###
import argparse
import calendar
import locale

### Functions ###

def get_arguments():
    """ Define CLI parameters and then get user supplied arguments """

    # Define a new parser to parse the command line in Python
    parser = argparse.ArgumentParser(description="item list generator")

    # Define arguments coming from the command line
    parser.add_argument("periodicity",
                        help="periodicity of the item : daily, weekly, monthly, quaterly", type=str)
    parser.add_argument("-t", "--text_output",
                        help="text to add to period", type=str)
    parser.add_argument("-p", "--position", required=False,
                        help="position of the text : append, prepend")
    parser.add_argument("-l", "--locale", required=False,
                        help="Language for periodicity : fr_FR")

    # parsing user supplied command line arguments
    args = parser.parse_args()

    if not args.locale is None:
        print(str(args.locale))
        locale.setlocale(locale.LC_ALL, str(args.locale))

    if args.periodicity == 'monthly':
        for month in range(1, 13):
            print(args.text_output, calendar.month_name[month])


### Parametrage ###

############
### MAIN ###
############

if __name__ == "__main__":
    arguments = get_arguments()