import textwrap


def menu():
    menu = """\n
    ================ MENU ================
    [d]\tDeposit
    [w]\tWithdraw
    [s]\tStatement
    [na]\tNew account
    [la]\tList accounts
    [nu]\tNew user
    [q]\tQuit
    => """
    return input(textwrap.dedent(menu))


def deposit(balance, value, statement, /):
    if value > 0:
        balance += value
        statement += f"Deposit:\t$ {value:.2f}\n"
        print("\n=== Deposit successful! ===")
    else:
        print("\n=== Operation failed! The entered value is invalid. ===")

    return balance, statement


def withdraw(*, balance, value, statement, limit, num_withdrawals, withdrawal_limit):
    exceeded_balance = value > balance
    exceeded_limit = value > limit
    exceeded_withdrawals = num_withdrawals >= withdrawal_limit

    if exceeded_balance:
        print("\n=== Operation failed! You don't have enough balance. ===")

    elif exceeded_limit:
        print("\n=== Operation failed! The withdrawal amount exceeds the limit. ===")

    elif exceeded_withdrawals:
        print("\n=== Operation failed! Maximum number of withdrawals exceeded. ===")

    elif value > 0:
        balance -= value
        statement += f"Withdrawal:\t$ {value:.2f}\n"
        num_withdrawals += 1
        print("\n=== Withdrawal successful! ===")

    else:
        print("\n=== Operation failed! The entered value is invalid. ===")

    return balance, statement


def show_statement(balance, /, *, statement):
    print("\n================ STATEMENT ================")
    print("No transactions have been made." if not statement else statement)
    print(f"\nBalance:\t$ {balance:.2f}")
    print("==========================================")


def create_user(users):
    ssn = input("Enter the SSN (xxx-xx-xxxx): ")
    user = filter_user(ssn, users)

    if user:
        print("\n=== A user with this SSN already exists! ===")
        return

    name = input("Enter the full name: ")
    birth_date = input("Enter the birth date (mm-dd-yyyy): ")
    address = input("Enter the address (street, number - neighborhood - city/state abbreviation): ")

    users.append({"name": name, "birth_date": birth_date, "ssn": ssn, "address": address})

    print("=== User created successfully! ===")


def filter_user(ssn, users):
    filtered_users = [user for user in users if user["ssn"] == ssn]
    return filtered_users[0] if filtered_users else None


def create_account(agency, account_number, users):
    ssn = input("Enter the user's SSN (xxx-xx-xxxx): ")
    user = filter_user(ssn, users)

    if user:
        print("\n=== Account created successfully! ===")
        return {"agency": agency, "account_number": account_number, "user": user}

    print("\n=== User not found, account creation process terminated! ===")


def list_accounts(accounts):
    for account in accounts:
        line = f"""\
            Agency:\t{account['agency']}
            A/C:\t\t{account['account_number']}
            Holder:\t{account['user']['name']}
        """
        print("=" * 100)
        print(textwrap.dedent(line))


def main():
    WITHDRAWAL_LIMIT = 3
    AGENCY = "0001"

    balance = 0
    limit = 500
    statement = ""
    num_withdrawals = 0
    users = []
    accounts = []

    while True:
        option = menu()

        if option == "d":
            value = float(input("Enter the deposit amount: "))

            balance, statement = deposit(balance, value, statement)

        elif option == "w":
            value = float(input("Enter the withdrawal amount: "))

            balance, statement = withdraw(
                balance=balance,
                value=value,
                statement=statement,
                limit=limit,
                num_withdrawals=num_withdrawals,
                withdrawal_limit=WITHDRAWAL_LIMIT,
            )

        elif option == "s":
            show_statement(balance, statement=statement)

        elif option == "nu":
            create_user(users)

        elif option == "na":
            account_number = len(accounts) + 1
            account = create_account(AGENCY, account_number, users)

            if account:
                accounts.append(account)

        elif option == "la":
            list_accounts(accounts)

        elif option == "q":
            print("Thank you for using our services. Have a nice day!")
            break

        else:
            print("Invalid operation, please select the desired operation again.")

main()
