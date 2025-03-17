import pandas
import random


# Functions go here
def make_statement(statement, decoration):
    """Emphasises headings by adding decoration
    at the start amd end"""

    print(f"{decoration * 3} {statement} {decoration * 3}")


def string_check(question, valid_answers=('yes', 'no'), num_letters=1):
    '''Checks that users enter the full word or the first letter of a word from a list of valid responses.'''

    while True:

        response = input(question).lower()

        for item in valid_answers:

            # check if the response is the entire word
            if response == item:
                return item

            # check if it's the first letter.
            elif response == item[:num_letters]:
                return item

        print(f"please choose an option from {valid_answers}")


def instructions():
    make_statement("Instructions", "ℹ️")

    print('''
    
For each ticket holder enter ...
- Their Name
- Their Age
- The Payment method (cash / credit)

The program will record the ticket sale and calculate the 
ticket cost (and the profit).

Once you have either sold all of the tickets or entered the
exit code ('xxx'), the program will display the ticket
sales information and write the data to a text file.

It will also choose one lucky ticket holder who wins the
draw (their ticket is free)

    ''')


def not_blank(question):
    """Checks that a user response is not blank"""

    while True:
        response = input(question)

        if response != "":
            return response

        print("Sorry, this can't be blank. \n")


def int_check(question):
    error = "Please enter a valid age"
    while True:
        response = input(question).lower()

        try:
            response = int(response)
            if response == int(response):
                return response
            else:
                print(error)

        except ValueError:
            print(error)


def currency(x):
    return "${:.2f}".format(x)


# Main routine goes here

# Initialize ticket numbers
MAX_TICKETS = 5
tickets_sold = 0

# initialise variables /  non-default options for string checker
payment_ans = ('cash', 'credit')

# ticket price list
CHILD_PRICE = 7.50
ADULT_PRICE = 10.50
SENIOR_PRICE = 6.50

# Credit card surcharge (currently 5%)
CREDIT_SURCHARGE = 0.05

# lists to hold ticket details
all_names = []
all_ticket_cost = []
all_surcharges = []

mini_movie_dict = {
    'Name': all_names,
    'Ticket Price': all_ticket_cost,
    'Surcharge': all_surcharges
}

# opening statement
make_statement("Mini-Movie Fundraiser Program", "🍿")

# ask user if they want instructions,
# display instructions if user says yes
print()
want_instructions = string_check("Do you want to see the instructions? ")

if want_instructions == "yes":
    instructions()

print()

# loop to get name, age and payment type.
while tickets_sold < MAX_TICKETS:
    # ask user for their name and make sure it is not blank
    name = not_blank("Name: ")

    # if name is exit code, break out of loop
    if name == "xxx":
        break

    # ask for their age and check it is between 12 and 120
    age = int_check("Age: ")

    if age < 12:
        print(f"{name} is too young!")
        continue

    # Child ticket price ($7.50)
    elif age < 16:
        ticket_price = CHILD_PRICE

    # Adult ticket ($10.50)
    elif age < 65:
        ticket_price = ADULT_PRICE

    # Senior ticket price ($6.50)
    elif age < 121:
        ticket_price = SENIOR_PRICE

    else:
        print(f"{name} is too old!")
        continue

    # ask user for payment method (cash / credit / ca / cr)
    pay_method = string_check("Payment Method: ", payment_ans, 2)

    if pay_method == "cash":
        surcharge = 0

    # if paying by credit, calculate surcharge
    else:
        surcharge = ticket_price * CREDIT_SURCHARGE

    # add name, ticket cost and surcharge to list
    all_names.append(name)
    all_ticket_cost.append(ticket_price)
    all_surcharges.append(surcharge)

    tickets_sold +=1

# create dataframe / table from dictionary
mini_movie_frame = pandas.DataFrame(mini_movie_dict)

# Calculate the total payable for each ticket
mini_movie_frame['Total'] = mini_movie_frame['Ticket Price'] + mini_movie_frame['Surcharge']
mini_movie_frame['Profit'] = mini_movie_frame['Ticket Price'] - 5

# Work out total paid and total profit
total_paid = mini_movie_frame['Total'].sum()
total_profit = mini_movie_frame['Profit'].sum()

# choose random winner
winner = random.choice(all_names)

# find index of winner (ie: position of list)
winner_index = all_names.index(winner)
print("winner", winner, "list_position", winner_index)

# retrieve Winner Ticket Price and Profit (so we can adjust profit numbers so that the winning number is excluded)
ticket_won = mini_movie_frame.at[winner_index, 'Total']
profit_won = mini_movie_frame.at[winner_index, 'Profit']

# currency formatting (currency function)
add_dollars = ['Ticket Price', 'Surcharge', 'Total', 'Profit']
for var_item in add_dollars:
    mini_movie_frame[var_item] = mini_movie_frame[var_item].apply(currency)

# output movie frame without index
print(mini_movie_frame.to_string(index=False))

print()
print(f"Total Paid: ${total_paid:.2f}")
print(f"Total Profit: ${total_profit:.2f}")

# print winner
print(f"The lucky winner is {winner}, their ticket worth, ${ticket_won:.2f} is free!")
print(f"Total Paid is now ${total_paid - ticket_won:.2f}")
print(f"Total Profit is now ${total_profit - profit_won:.2f}")

if tickets_sold == MAX_TICKETS:
    print(f"You have sold all of the tickets (ie: {MAX_TICKETS} tickets)")
else:
    print(f"You have sold {tickets_sold} / {MAX_TICKETS} Tickets.")