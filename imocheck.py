import sys


def is_valid_imo_number(imo_number):
    # IMO numbers are 7-digit numbers
    if not (len(imo_number) == 7 and imo_number.isdigit()):
        return False

    # Calculate the check digit
    sum = 0
    for i in range(6):
        sum += int(imo_number[i]) * (7 - i)
    check_digit = sum % 10

    # Check if the check digit matches the last digit of the IMO number
    return check_digit == int(imo_number[-1])


if __name__ == "__main__":
    # Read the IMO number from the command line arguments
    if len(sys.argv) != 2:
        print("Usage: python imo_number_check.py IMO_NUMBER")
        sys.exit(1)
    imo_number = sys.argv[1]

    # Check if the IMO number is valid
    if is_valid_imo_number(imo_number):
        print("The IMO number is valid.")
    else:
        print("The IMO number is not valid.")
