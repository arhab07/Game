import random
def spin_row():
    spin=['❤️','💜','💙','🖤','💛']
    return [random.choice(spin) for _ in range(3)]
def print_row(row):
    row = " || ".join(row)
    return row
def get_payout(row,bet):
    if row[0]==row[1]==row[2]:
        if row[0]== "💛":
            return bet * 5
        elif row[0]== "💜":
            return bet * 10
        elif row[0]=="💙":
            return bet * 15
        elif row[0]=="🖤":
            return bet * 20
        elif row[0]=="❤️":
            return bet * 50
    return 0
