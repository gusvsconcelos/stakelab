import json
import os
import random
import sys


def load_json(filename):
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        return []


def save_json(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def menu():
    print("Welcome to StakeLab\n")

    print("1.Sign Up")
    print("2.Deposit")
    print("3.New Bet")
    print("4.Bet History")
    print("5.User Data")
    print("6.Clear History")
    print("7.Exit")

    try:
        user_choice = int(input("\nChoose an option from the menu: "))
    except ValueError:
        print("Invalid input. Please enter a number.")
        return

    if user_choice == 1:
        clear_screen()
        sign_up()
    elif user_choice == 2:
        clear_screen()
        deposit()
    elif user_choice == 3:
        clear_screen()
        new_bet()
    elif user_choice == 4:
        clear_screen()
        show_bet_history()
    elif user_choice == 5:
        clear_screen()
        display_user_info()
    elif user_choice == 6:
        clear_screen()
        clear_history()
    elif user_choice == 7:
        clear_screen()
        exit_program()
    else:
        print("Invalid choice. Please select a valid option.")
        input("\nPress ENTER to return to the menu...")


def new_bet():
    user_data = load_json("userdata.json")
    bet_history = load_json("bethistory.json")

    balance = user_data["Balance"]

    match = str(input("Enter the match: "))
    match_date = str(input("Enter the match date: "))
    match_market = str(input("Enter the betting market: "))

    try:
        odds = float(input("Enter the odds: "))
        stake = float(input("Enter your stake: "))
    except ValueError:
        print("Invalid input. Please enter a number.")
        input("\nPress ENTER to return to the menu...")
        return

    if stake > balance:
        print("Insufficient balance for this bet.")
        input("\nPress ENTER to return to the menu...")
        return

    result = ("Lost", "Won")[random.choice([True, False])]
    balance += stake * odds if result == "Won" else -stake

    user_data["Balance"] = balance

    print(f"\nBet result: {result}")
    print(f"Return: {stake * odds if result == 'Won' else '-' + str(stake)}")
    print(f"Updated balance: {balance}")

    bet = {
        "User": user_data["Name"],
        "Match": match,
        "Date": match_date,
        "Market": match_market,
        "Odds": odds,
        "Stake": stake,
        "Result": result,
        "Balance": balance,
    }

    bet_history.append(bet)

    save_json("bethistory.json", bet_history)
    save_json("userdata.json", user_data)

    input("\nPress ENTER to return to the menu...")


def deposit():
    user_data = load_json("userdata.json")

    try:
        deposit_value = float(input("Enter deposit amount: "))
    except ValueError:
        print("Invalid input. Please enter a number.")
        input("\nPress ENTER to return to the menu...")
        return

    user_data["Balance"] += deposit_value

    print(f"Successfully added {deposit_value} to your balance!")

    save_json("userdata.json", user_data)

    input("\nPress ENTER to return to the menu...")


def display_user_info():
    data = load_json("userdata.json")
    print(json.dumps(data, indent=4))

    input("\nPress ENTER to return to the menu...")


def show_bet_history():
    data = load_json("bethistory.json")
    print(json.dumps(data, indent=4))

    input("\nPress ENTER to return to the menu...")


def clear_history():
    data = load_json("bethistory.json")

    user_confirmation = str(
        input("Are you sure you want to clear your history? [y/N] ").upper()
    )

    if user_confirmation == "Y":
        data = []

        save_json("bethistory.json", data)

        print("Your betting history has been cleared.")
        input("\nPress ENTER to return to the menu...")
    else:
        clear_screen()


def sign_up():
    user_name = str(input("Enter your name: "))

    try:
        user_balance = float(input("Enter your initial deposit amount: "))
    except ValueError:
        print("Invalid input. Please enter a number.")
        input("\nPress ENTER to return to the menu...")
        return

    user_data = {"Name": user_name, "Balance": user_balance}

    save_json("userdata.json", user_data)


def exit_program():
    user_confirmation = str(input("Are you sure you want to exit? [y/N] ").upper())

    if user_confirmation == "Y":
        sys.exit()
    else:
        clear_screen()
        menu()


def main():
    while True:
        clear_screen()
        menu()


if __name__ == "__main__":
    main()
