filename = "retries.txt"


def write_retries(retry_amt):
    with open(filename, 'w') as file:
        file.write(str(retry_amt))


def get_retries():
    with open(filename, 'r') as file:
        for line in file:
            return int(line)
