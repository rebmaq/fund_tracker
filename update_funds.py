import struct
import csv
from datetime import datetime
from show_funds import get_denomination_counts

counts_file = "./Counts/denomination_counts.csv"
transaction_history_file= "./Counts/ledger.log"
FORMAT = "20s15s?i"

def serialize_update(timestamp, operation, denomination, amount):
    timestamp_bytes = timestamp.encode('utf-8')[:20].ljust(20, b'\0')
    denomination_bytes = denomination.encode('utf-8')[:15].ljust(15, b'\0')
    return struct.pack(FORMAT, timestamp_bytes, denomination_bytes, operation, amount)

def deserialize_update(binary_data):
    timestamp_bytes, denomination_bytes, operation, amount = struct.unpack(FORMAT, binary_data)
    timestamp = timestamp_bytes.decode('utf-8').strip('\0')
    denomination = denomination_bytes.decode('utf-8').strip('\0')
    return timestamp, denomination, operation, amount

def view_ledger():
     with open(transaction_history_file, 'rb') as file:  
        while chunk := file.read(struct.calcsize(FORMAT)):
            yield deserialize_update(chunk)

def print_ledger():
    for event in view_ledger():
        print(event)

def update_funds(updates):
    new_counts = get_denomination_counts()
    for update in updates:
        operation, denomination, amount = update
        
        if denomination not in new_counts:
            raise ValueError(f'Denomination {denomination} not found in the funds CSV.')

        if operation == 1:
            new_counts[denomination] += amount
        else:
            new_counts[denomination] -= amount
        
        if new_counts[denomination] < 0:
                raise ValueError(f'Balance is negative for {denomination}\nNo changes have been made to the CSV.')
    
    order = ["Pennies", "Nickels", "Dimes", "Quarters", "Half Dollars", "Dollar Coins", "Ones", "Twos", "Fives", "Tens", "Twenties", "Fifties", "Hundreds"]
    
    with open(counts_file, 'w', newline="") as file:
        writer = csv.writer(file, delimiter=",")
        writer.writerow(["Denomination", "Count"])
        for i in order:
            writer.writerow([i, new_counts[i]])

    with open(transaction_history_file, "ab") as file:
        for operation, denomination, amount in updates:
            transaction_log = serialize_update(datetime.now().isoformat(), operation, denomination, amount)
            file.write(transaction_log)

try:    
    update_funds([[1, "Twos", 3]])
    print_ledger()
except ValueError as e:
    print(e)