"""
main.py: druhý projekt do Engeto Online Python Akademie

author: Martina Ježková
email: jezkova.m94@gmail.com
"""

import random
import time

from colorama import Fore, Style, init
init(autoreset=True)

SEPARATOR = "-" * 60


def print_intro():
    """Display the introduction of the Bulls and Cows game."""
    print(f"""Hi there!
{SEPARATOR}
Welcome to the Bulls and Cows game! 🐂🐄

I've generated a random number with unique digits for you.
Your task is to guess it. 

📌 Rules:
- The number contains only unique digits.
- It doesn't start with 0.
- After each guess, you'll receive feedback:
    🐂 Bull → correct digit ✅ and correct position ✅
    🐄 Cow → correct digit ✅ but wrong position ❌
    🟩 green digit = Bull
    🟨 yellow digit = Cow
    🟥 red digit = the digit is not in secret number

Try to guess the number in as few attempts as possible!

🎯 Choose your difficulty:
Enter how many digits the secret number should have (1-9).
The higher the number, the more difficult the game.
{SEPARATOR}""")


def choice_difficulty() -> int:
    """User chooses the number of digits."""

    while True:
        choice = input("🟢 Enter a number from 1 to 9 to choose difficulty: ")
        if choice.isdigit() and 1 <= int(choice) <= 9:
            return int(choice)
        else:
            print("❌ Invalid choice. Please enter a number from 1 to 9.")


def generate_secret_number(length: int) -> str:
    """
    Generate secret x-digits number (x = user choice).
    All digits in secret number are unique.
    Secret number doesn't start by 0.
    """
    digits = list("0123456789")
    first_digit = random.choice(digits[1:])
    remaining = [d for d in digits if d != first_digit]
    rest_digits = random.sample(remaining, k=length - 1)

    return first_digit + "".join(rest_digits)


def get_user_guess(length: int) -> str:
    """
    Prompt the user to enter a guess with the given number of digits.
    The user guess is validated against:
     - less than required number of digits
     - more than required number of digits
     - non-digit characters
     - duplicated digits
     - leading 0
    """
    while True:
        guess = input(">>> ")

        if len(guess) < length:
            print(f"❌ The number is shorter than {length} digits.")
        elif len(guess) > length:
            print(f"❌ The number is longer than {length} digits.")
        elif not guess.isdigit():
            print(f"❌ Only numeric characters are allowed.")
        elif len(set(guess)) != length:
            print(f"❌ All digits must be unique.")
        elif guess[0] == "0":
            print(f"❌ The number cannot start with 0.")
        else:
            return guess

        print(SEPARATOR)


def evaluate_bulls_and_cows(
    secret: str, guess: str) -> tuple[int, int]:
    """Evaluate the number of bulls and cows."""
    bulls = 0
    cows = 0

    for i in range(len(secret)):
        if guess[i] == secret[i]:
            bulls += 1

        elif guess[i] in secret:
            cows += 1

    return bulls, cows


def format_duration(seconds: int) -> str:
    """Convert seconds into h m s string."""
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    return f"{h}h {m}m {s}s"


GREEN = Fore.GREEN
YELLOW = Fore.YELLOW
RED = Fore.RED
RESET = Style.RESET_ALL

def colorize_guess(secret: str, guess: str) -> str:
    """
    Color each digit of the guess based on Bulls and Cows logic.
    green color = bull (right digit and position)
    yellow color = cow (right digit and wrong position)
    red color = digit is not in the secret number
    """
    result = []
    for i, digit in enumerate(guess):
        if digit == secret[i]:
            result.append(f"{GREEN}{digit}")
        elif digit in secret:
            result.append(f"{YELLOW}{digit}")
        else:
            result.append(f"{RED}{digit}")
    return "".join(result)


def play_game(secret: str, length: int) -> tuple[int, int]:
    """
    Main game loop that asks user to guess until
    the correct number is found.

    Returns:
        attempts (int): number of guesses taken
        duration (int): total time taken in seconds
    """
    attempts = 0
    print(f"Enter a number:\n{SEPARATOR}")

    start_time = time.time()

    while True:
        guess = get_user_guess(length)
        attempts += 1

        bulls, cows = evaluate_bulls_and_cows(secret, guess)

        bull_label = "bull" if bulls in (0, 1) else "bulls"
        cow_label = "cow" if cows in (0, 1) else "cows"
        print(f"{GREEN}{bulls}{RESET} {bull_label}, "
              f"{YELLOW}{cows}{RESET} {cow_label}")
        print(f"Your guess: {colorize_guess(secret, guess)}")
        print(SEPARATOR)

        if bulls == length:
            end_time = time.time()
            duration = round(end_time - start_time)

            print(
                "🎉 Correct, you've guessed the right number"
                f"in {attempts} guesses!"
            )
            print(f"⏱️ Time taken: {format_duration(duration)}")
            print(SEPARATOR)
            print(f"That's amazing!")
            return attempts, duration


def main():
    print_intro()
    stats = []

    while True:
        length = choice_difficulty()
        secret_number = generate_secret_number(length)
        attempts, duration = play_game(secret_number, length)
        stats.append((length, attempts, duration))

        print("\n📊 Game Summary:")
        for i, (length, attempts, duration) in enumerate(stats, start=1):
            print(
            f"Game {i}: {length} digits, {attempts} guesses, "
            f"{format_duration(duration)}"
        )
        print(SEPARATOR)

        play_again = input("🔁 Do you want to play again? (y/n): ").lower()
        if play_again != "y":
            break

    print(SEPARATOR)
    print("Thanks for playing! 👋")


if __name__ == "__main__":
    main()