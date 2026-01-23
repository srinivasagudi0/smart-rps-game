import random

# ------------------ Helper Functions ------------------

def load_rating(name, rating_file_path="rating.txt"):
    """Load the user's rating from rating.txt or return 0 if not found."""
    rating = 0
    try:
        with open(rating_file_path, "r") as file:
            for line in file:
                parts = line.strip().split()
                if len(parts) == 2 and parts[0] == name:
                    rating = int(parts[1])
                    break
    except FileNotFoundError:
        # If no file, just start fresh
        pass
    return rating


def save_rating(name, rating, rating_file_path="rating.txt"):
    """Save or update the user's rating in rating.txt."""
    lines = []
    found = False

    # Read existing ratings
    try:
        with open(rating_file_path, "r") as file:
            for line in file:
                parts = line.strip().split()
                if len(parts) == 2:
                    username, score = parts
                    if username == name:
                        lines.append(f"{name} {rating}\n")
                        found = True
                    else:
                        lines.append(line)
    except FileNotFoundError:
        pass

    # If new user, add their entry
    if not found:
        lines.append(f"{name} {rating}\n")

    # Write all back
    with open(rating_file_path, "w") as file:
        file.writelines(lines)


def build_relationships(options):
    """Create a dictionary of which options each one defeats (circular logic)."""
    beats = {}
    for i, option in enumerate(options):
        others = options[i + 1:] + options[:i]  # wrap-around order
        half = len(others) // 2
        # second half = beaten by 'option'
        beats[option] = others[half:]
    return beats


def play_round(user_choice, computer_choice, beats):
    """Determine round result."""
    if user_choice == computer_choice:
        return "draw"
    elif computer_choice in beats[user_choice]:
        return "win"
    else:
        return "lose"


def run_cli():
    """Run the interactive CLI game."""
    while True:
        name = input("Enter your name: ").strip()
        if name:
            break
        print("Please enter a name to start.")
    print(f"Hello, {name}")

    rating = load_rating(name)

    options_input = input().strip()
    if options_input == "":
        options = ["rock", "paper", "scissors"]
    else:
        options = [opt.strip() for opt in options_input.split(",") if opt.strip()]

    print("Okay, let's start")

    beats = build_relationships(options)

    while True:
        user_input = input().strip()

        if user_input == "!exit":
            print("Bye!")
            break
        elif user_input == "!rating":
            print(f"Your rating: {rating}")
        elif user_input in options:
            computer_choice = random.choice(options)
            result = play_round(user_input, computer_choice, beats)

            if result == "draw":
                rating += 50
                print(f"There is a draw ({computer_choice})")
            elif result == "win":
                rating += 100
                print(f"Well done. The computer chose {computer_choice} and failed")
            else:
                print(f"Sorry, but the computer chose {computer_choice}")
                print("Game over!")
                break
        else:
            print("Invalid input")

    save_rating(name, rating)


if __name__ == "__main__":
    run_cli()
