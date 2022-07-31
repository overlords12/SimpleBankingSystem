import random as rm
import sqlite3

storage = {}
# Global Variables
conn = sqlite3.connect('card.s3db')
cur = conn.cursor()


def menu():
    while True:
        print("1. Create an account\n2. Log into account\n0. Exit")
        input_ = int(input())
        if input_ == 0:
            exit()
        if input_ == 1:
            create_account()
        if input_ == 2:
            load_account()


def create_account():
    rm.seed()
    print()
    while True:
        verification = ''.join(["{}".format(rm.randint(0, 9)) for _ in range(0, 9)])
        account_number = "400000" + verification + "5"
        password = str(rm.randint(1111, 9999))

        if 0 in sql_exec("SELECT COUNT(number) FROM card WHERE {} = number"
                         .format(account_number), 'one') and luhn(account_number):
            print("Your card number: ")
            print(account_number)
            print("Your card PIN: ")
            print(password)
            print("\n")
            sql_exec("INSERT INTO card VALUES ({}, {}, {}, {})".format("'" + account_number + "'",
                                                                       account_number, password, 0), "")
            break


def load_account():
    print("\nEnter your card number: ")
    card_number = input()
    print("Enter your card PIN: ")
    card_pin = input()
    print("\n")
    if type(sql_exec("SElECT pin FROM card WHERE number = {}".format(card_number), "one")) == type(None):
        print("Wrong card number or PIN!")
    else:
        if card_pin in sql_exec("SElECT pin FROM card WHERE number = {}".format(card_number), "one"):
            print("You have successfully logged in!\n")
            account_options(card_number)
        else:
            print("Wrong card number or PIN!")


def account_options(card_number):
    while True:
        print("1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit\n")
        input_ = int(input())
        if input_ == 0:
            exit()
        if input_ == 1:
            balance = sql_exec("SELECT balance FROM card WHERE number = {}".format(card_number), "one")[0]
            print("Balance: ", balance, "\n")
        if input_ == 2:
            income = input("Add amount of income: ")
            add_income(card_number, income)
            print("Income was added!")
        if input_ == 3:
            transfer(card_number)
        if input_ == 4:
            sql_exec("DELETE FROM card WHERE number = {}".format(card_number), "no")
            print("The account has been closed!")
        if input_ == 5:
            print("You have successfully logged out!\n")
            break


def luhn(verification_):
    # Drop the last digit: already done
    last = verification_[-1]
    verification_ = verification_[:15]
    # multiply odd * 2
    verification_ = [int(i) for i in verification_]
    verification_ = [i * 2 if j % 2 == 0 else i for j, i in enumerate(verification_)]
    # Subtract 9 from numbers over 9:
    verification_ = [i - 9 if i > 9 else i for i in verification_]
    # add al numbers
    verification_ = sum(verification_) + int(last[0])
    if verification_ % 10 == 0:
        return True
    else:
        return False


def sql_exec(query, return_it):
    cur.execute(query)
    conn.commit()
    if return_it == 'all':
        fetched = cur.fetchall()
        return fetched
    elif return_it == 'one':
        fetched = cur.fetchone()
        return fetched
    else:
        pass


def add_income(card_number, income):
    balance = sql_exec("SELECT balance FROM card WHERE number = {}".format(card_number), "one")[0]
    balance = int(balance) + int(income)
    sql_exec("UPDATE card SET balance = {} WHERE  number = {}"
             .format(balance, card_number), "no")


def transfer(card_number):
    card_transfer = input("Enter card number: \n")
    if card_transfer == card_number:
        print("You can't transfer money to the same account!: ")
    elif not luhn(card_transfer):
        print("Probably you made a mistake in the card number. Please try again!\n")
    elif sql_exec("SELECT COUNT(number) FROM card WHERE number = {}".format(card_transfer), "one")[0] != 1:
        print("Such a card does not exist.\n")
    else:
        transfer_value = int(input("Enter how much money you want to transfer: \n"))
        balance = sql_exec("SELECT balance FROM card WHERE number = {}".format(card_number), "one")[0]
        if balance < transfer_value:
            print("Not enough money! \n")
        elif balance > transfer_value:
            add_income(card_number, int(transfer_value) * -1)
            add_income(card_transfer, transfer_value)
            print("Success!")


sql_exec(''' CREATE TABLE IF NOT EXISTS card 
(id INTEGER, number TEXT, pin TEXT, balance INTEGER DEFAULT 0 ) ''', "no")

#  4000007801835155  1963 other 4000005927888025 8153
menu()
