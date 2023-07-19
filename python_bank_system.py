menu = """

[d] Deposit
[w] Withdraw
[s] Statement
[q] Quit

=> """

balance = 0
limit = 500
statement = ""
withdrawal_count = 0
WITHDRAWAL_LIMIT = 3

while True:

    option = input(menu)

    if option == "d":
        value = float(input("Enter the deposit amount: "))

        if value > 0:
            balance += value
            statement += f"Deposit: $ {value:.2f}\n"

        else:
            print("Operation failed! The entered value is invalid.")

    elif option == "w":
        value = float(input("Enter the withdrawal amount: "))

        exceeded_balance = value > balance

        exceeded_limit = value > limit

        exceeded_withdrawal_limit = withdrawal_count >= WITHDRAWAL_LIMIT

        if exceeded_balance:
            print("Operation failed! You don't have sufficient balance.")

        elif exceeded_limit:
            print("Operation failed! The withdrawal amount exceeds the limit.")

        elif exceeded_withdrawal_limit:
            print("Operation failed! Maximum number of withdrawals exceeded.")

        elif value > 0:
            balance -= value
            statement += f"Withdrawal: $ {value:.2f}\n"
            withdrawal_count += 1

        else:
            print("Operation failed! The entered value is invalid.")

    elif option == "s":
        print("\n=============== BANK STATEMENT ===============")
        print("No transactions have been made." if not statement else statement)
        print(f"\nBalance: $ {balance:.2f}")
        print("==============================================")

    elif option == "q":
        print("Thank you for using our services. Have a nice day!!!")
        break

    else:
        print("Invalid operation, please select the desired operation again.")
