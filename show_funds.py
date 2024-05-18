import csv
counts_file = "./Counts/denomination_counts.csv"

def format_output(coin_counts, bill_counts, coin_value, total_value):
    return f'Coin Count:\t{coin_counts}\t\tBill Count:\t{bill_counts}\nCoin Values:\t{coin_value}\nTotal Value:\t{total_value}'

def get_denomination_counts():
    denominations = {}
    with open(counts_file, 'r') as file:
        reader = csv.reader(file, delimiter=",")
        next(file)
        for row in reader:
            if not row[1].isnumeric():
                continue
            denominations[row[0]] = int(row[1])
    return denominations

def get_total_value():
    coin_counts, bill_counts = 0, 0
    coin_value,  total_value = 0, 0
    with open(counts_file, 'r') as file:
        reader = csv.reader(file, delimiter=",")
        next(file)
        for row in reader:
            if not row[1].isnumeric():
                continue
                
            if denomination_to_val[row[0]] < 1 or row[0] == "Dollar Coins":
                coin_counts += int(row[1]) 
                coin_value += int(row[1])*denomination_to_val[row[0]]
            else:
                bill_counts += int(row[1])

            total_value += int(row[1])*denomination_to_val[row[0]]
    return coin_counts, bill_counts, coin_value, total_value
    
denomination_to_val = {
    "Pennies"       : 0.01,
    "Nickels"       : 0.05,
    "Dimes"         : 0.10,
    "Quarters"      : 0.25,
    "Half Dollars"  : 0.50,
    "Dollar Coins"  : 1.00,
    "Ones"          : 1.00,
    "Twos"          : 2.00,
    "Fives"         : 5.00,
    "Tens"          : 10.00,
    "Twenties"      : 20.00,
    "Fifties"       : 50.00,
    "Hundreds"      : 100.00,
}

coin_counts, bill_counts, coin_value, total_value = get_total_value()
print(format_output(coin_counts, bill_counts, coin_value, total_value))