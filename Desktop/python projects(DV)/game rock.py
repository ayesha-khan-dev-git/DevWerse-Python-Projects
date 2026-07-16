"""
Rock, Paper, Scissors — Streak Edition
----------------------------------------
A console-based Rock, Paper, Scissors game with a twist:
it tracks your win/loss streak and total score across rounds,
and reacts differently depending on how the match is going.

Rules implemented:
- random module picks the computer's move
- infinite while loop keeps the game running
- typing 'end' (any case: End, END, end...) instantly stops the game
- if/elif/else determines the winner each round
- each round prints both choices and a clear result
"""

import random

# Moves mapped to what they beat, plus a flavor verb for the win message
MOVES = {
    "rock": {"beats": "scissors", "verb": "smashes"},
    "paper": {"beats": "rock", "verb": "covers"},
    "scissors": {"beats": "paper", "verb": "cuts"},
}

CHOICES_DISPLAY = "Rock, Paper, Scissors"


def get_computer_choice():
    """Randomly select the computer's move."""
    return random.choice(list(MOVES.keys()))


def decide_winner(user, computer):
    """
    Return 'user', 'computer', or 'tie' based on standard rules.
    Uses if/elif/else as required.
    """
    if user == computer:
        return "tie"
    elif MOVES[user]["beats"] == computer:
        return "user"
    else:
        return "computer"


def streak_message(streak):
    """A little unique flavor based on the current win/loss streak."""
    if streak >= 3:
        return f"🔥 You're on a {streak}-win streak! Unstoppable!"
    elif streak <= -3:
        return f"❄️ Cold streak: {abs(streak)} losses in a row. Shake it off!"
    return ""


def print_banner():
    print("=" * 45)
    print("   ROCK · PAPER · SCISSORS — STREAK EDITION")
    print("=" * 45)
    print("Type 'end' (any case) at any time to quit.\n")


def main():
    print_banner()

    user_score = 0
    computer_score = 0
    ties = 0
    streak = 0  # positive = user winning streak, negative = losing streak
    rounds_played = 0

    while True:
        raw_input_value = input(
            f"Enter your move ({CHOICES_DISPLAY}) or type 'end' to stop: "
        ).strip()

        # Case-insensitive check for the exit command
        if raw_input_value.lower() == "end":
            print("\nGame over. Thanks for playing!")
            break

        user_choice = raw_input_value.lower()

        if user_choice not in MOVES:
            print(f"⚠️  '{raw_input_value}' isn't a valid move. Try Rock, Paper, or Scissors.\n")
            continue

        computer_choice = get_computer_choice()
        rounds_played += 1

        print(f"Computer chose: {computer_choice.capitalize()}")

        result = decide_winner(user_choice, computer_choice)

        if result == "tie":
            print(f"It's a tie! Both chose {user_choice.capitalize()}.")
            ties += 1
            streak = 0
        elif result == "user":
            verb = MOVES[user_choice]["verb"]
            print(f"You win! {user_choice.capitalize()} {verb} {computer_choice.capitalize()}.")
            user_score += 1
            streak = streak + 1 if streak >= 0 else 1
        else:
            verb = MOVES[computer_choice]["verb"]
            print(f"Computer wins! {computer_choice.capitalize()} {verb} {user_choice.capitalize()}.")
            computer_score += 1
            streak = streak - 1 if streak <= 0 else -1

        flavor = streak_message(streak)
        if flavor:
            print(flavor)

        print(f"Score → You: {user_score} | Computer: {computer_score} | Ties: {ties}\n")

    # End-of-game summary
    print("-" * 45)
    print(f"Rounds played: {rounds_played}")
    print(f"Final Score → You: {user_score} | Computer: {computer_score} | Ties: {ties}")
    if user_score > computer_score:
        print("🏆 You won the match overall! Great job.")
    elif computer_score > user_score:
        print("🤖 The computer won the match overall. Rematch soon?")
    else:
        print("🤝 The match ended in an overall tie!")
    print("-" * 45)


if __name__ == "__main__":
    main()