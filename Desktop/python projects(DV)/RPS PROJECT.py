import random
import time

# ANSI color codes for console text
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"

# ASCII art for each move
rock_art = """
    _______
---'   ____)
      (_____)
      (_____)
      (____)
---.__(___)
"""

paper_art = """
    _______
---'   ____)____
          ______)
          _______)
         _______)
---.__________)
"""

scissors_art = """
    _______
---'   ____)____
          ______)
       __________)
      (____)
---.__(___)
"""

art = {"rock": rock_art, "paper": paper_art, "scissors": scissors_art}

print(CYAN + "=====================================")
print("     ROCK  PAPER  SCISSORS")
print("=====================================" + RESET)
print("Type Rock/Paper/Scissors (or just r/p/s) or 'end' to quit\n")

wins = 0
losses = 0
draws = 0

while True:
    user_input = input("Your move: ")

    if user_input.lower() == "end":
        print("\nGame over. Thanks for playing!")
        break

    user_input = user_input.lower()

    # allow short forms r, p, s along with full words
    if user_input == "r":
        user_choice = "rock"
    elif user_input == "p":
        user_choice = "paper"
    elif user_input == "s":
        user_choice = "scissors"
    else:
        user_choice = user_input

    if user_choice != "rock" and user_choice != "paper" and user_choice != "scissors":
        print(RED + "Invalid input. Type rock, paper, scissors (or r/p/s)." + RESET)
        continue

    # suspense before revealing the computer's move
    print("Rock...")
    time.sleep(0.4)
    print("Paper...")
    time.sleep(0.4)
    print("Scissors...")
    time.sleep(0.4)
    print("Shoot!\n")

    computer_choice = random.choice(["rock", "paper", "scissors"])

    print("You chose:")
    print(art[user_choice])
    print("Computer chose:")
    print(art[computer_choice])

    if user_choice == computer_choice:
        print(YELLOW + "It's a tie!" + RESET)
        draws = draws + 1

    elif user_choice == "rock" and computer_choice == "scissors":
        print(GREEN + "You win! Rock smashes Scissors." + RESET)
        wins = wins + 1

    elif user_choice == "paper" and computer_choice == "rock":
        print(GREEN + "You win! Paper covers Rock." + RESET)
        wins = wins + 1

    elif user_choice == "scissors" and computer_choice == "paper":
        print(GREEN + "You win! Scissors cuts Paper." + RESET)
        wins = wins + 1

    else:
        print(RED + "You lose! " + computer_choice.capitalize() + " beats " + user_choice.capitalize() + RESET)
        losses = losses + 1

    print(CYAN + "Score -> Wins: " + str(wins) + "  Losses: " + str(losses) + "  Draws: " + str(draws) + RESET)
    print("-------------------------------------\n")

print("\nFinal Score")
print("Wins:", wins)
print("Losses:", losses)
print("Draws:", draws)