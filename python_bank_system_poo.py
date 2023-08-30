import textwrap
from datetime import datetime
from abc import ABC, abstractmethod

class Client(ABC):
    @abstractmethod
    def perform_transaction(self, account, transaction):
        pass

class User(Client):
    def __init__(self, ssn, name, birth_date, address):
        self.ssn = ssn
        self.name = name
        self.birth_date = birth_date
        self.address = address

    def perform_transaction(self, account, transaction):
        transaction.register(account)

class Transaction(ABC):
    @property
    @abstractmethod
    def value(self):
        pass

    @abstractmethod
    def register(self, account):
        pass

class Deposit(Transaction):
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value

    def register(self, account):
        account.deposit(self.value)
        account._statement += f"Deposit:\t$ {self.value:.2f}\n"
        print("\n=== Deposit successful! ===")

class Withdrawal(Transaction):
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value

    def register(self, account):
        success = account.withdraw(self.value, limit=500, withdrawal_limit=3)
        if success:
            account._statement += f"Withdrawal:\t$ {self.value:.2f}\n"
            print("\n=== Withdrawal successful! ===")

class Account(Client):
    def __init__(self, agency, account_number, user):
        self._balance = 0
        self._agency = agency
        self._account_number = account_number
        self._user = user
        self._statement = ""
        self._num_withdrawals = 0

    def perform_transaction(self, transaction):
        transaction.register(self)

    def deposit(self, value):
        if value > 0:
            self._balance += value
        else:
            print("\n=== Operation failed! The entered value is invalid. ===")

    def withdraw(self, value, limit, withdrawal_limit):
        exceeded_balance = value > self._balance
        exceeded_limit = value > limit
        exceeded_withdrawals = self._num_withdrawals >= withdrawal_limit

        if exceeded_balance:
            print("\n=== Operation failed! You don't have enough balance. ===")
            return False
        elif exceeded_limit:
            print("\n=== Operation failed! The withdrawal amount exceeds the limit. ===")
            return False
        elif exceeded_withdrawals:
            print("\n=== Operation failed! Maximum number of withdrawals exceeded. ===")
            return False
        elif value > 0:
            self._balance -= value
            self._num_withdrawals += 1
            return True
        else:
            print("\n=== Operation failed! The entered value is invalid. ===")
            return False

    def show_statement(self):
        print("\n================ STATEMENT ================")
        print("No transactions have been made." if not self._statement else self._statement)
        print(f"\nBalance:\t$ {self._balance:.2f}")
        print("==========================================")

    def __str__(self):
        return f"""\
            Agency:\t{self._agency}
            A/C:\t\t{self._account_number}
            Holder:\t{self._user.name}
        """

def menu():
    menu_text = """\n
    ================ MENU ================
    [d]\tDeposit
    [w]\tWithdraw
    [s]\tStatement
    [na]\tNew account
    [la]\tList accounts
    [nu]\tNew user
    [q]\tQuit
    => """
    return input(textwrap.dedent(menu_text))

def create_user(users):
    ssn = input("Enter the SSN (xxx-xx-xxxx): ")
    user = filter_user(ssn, users)

    if user:
        print("\n=== A user with this SSN already exists! ===")
        return None

    name = input("Enter the full name: ")
    birth_date = input("Enter the birth date (mm-dd-yyyy): ")
    address = input("Enter the address (street, number - neighborhood - city/state abbreviation): ")

    user = User(ssn=ssn, name=name, birth_date=birth_date, address=address)
    users.append(user)

    print("\n=== User created successfully! ===")
    return user

def filter_user(ssn, users):
    filtered_users = [user for user in users if user.ssn == ssn]
    return filtered_users[0] if filtered_users else None

def main():
    users = []
    accounts = []

    while True:
        option = menu()

        if option == "d":
            if not accounts:
                print("\n=== No accounts available. Please create an account first. ===")
            else:
                value = float(input("Enter the deposit amount: "))
                transaction = Deposit(value)
                accounts[-1].perform_transaction(transaction)

        elif option == "w":
            if not accounts:
                print("\n=== No accounts available. Please create an account first. ===")
            else:
                value = float(input("Enter the withdrawal amount: "))
                transaction = Withdrawal(value)
                accounts[-1].perform_transaction(transaction)

        elif option == "s":
            if not accounts:
                print("\n=== No accounts available. Please create an account first. ===")
            else:
                accounts[-1].show_statement()

        elif option == "na":
            user = create_user(users)
            if user:
                account_number = len(accounts) + 1
                account = Account(agency="0001", account_number=account_number, user=user)
                accounts.append(account)

        elif option == "la":
            for account in accounts:
                print("=" * 100)
                print(textwrap.dedent(str(account)))

        elif option == "q":
            print("Thank you for using our services. Have a nice day!")
            break

        else:
            print("Invalid operation, please select the desired operation again.")

if __name__ == "__main__":
    main()
