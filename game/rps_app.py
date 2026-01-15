import random
import os
import streamlit as st

# Flexible import for both direct and package runs
try:
    from game.rock_paper_scissor import build_relationships, load_rating, play_round, save_rating
except ImportError:
    from rock_paper_scissor import build_relationships, load_rating, play_round, save_rating

RATING_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'rating.txt'))
DEFAULT_OPTIONS = ["rock", "paper", "scissors"]


def init_state():
    if "name" not in st.session_state:
        st.session_state.name = ""
    if "rating" not in st.session_state:
        st.session_state.rating = 0
    if "options" not in st.session_state:
        st.session_state.options = DEFAULT_OPTIONS.copy()
    if "beats" not in st.session_state:
        st.session_state.beats = build_relationships(st.session_state.options)
    if "message" not in st.session_state:
        st.session_state.message = ""
    if "error" not in st.session_state:
        st.session_state.error = ""


def load_user_rating():
    name = st.session_state.name.lower().strip()
    if name:
        st.session_state.rating = load_rating(name, RATING_FILE)
    else:
        st.session_state.rating = 0


def update_options(option_text: str):
    opts = [opt.strip() for opt in option_text.split(",") if opt.strip()]
    if not opts:
        st.session_state.options = DEFAULT_OPTIONS.copy()
        st.session_state.error = "Using default options: rock, paper, scissors."
    elif len(opts) < 3:
        st.session_state.options = DEFAULT_OPTIONS.copy()
        st.session_state.error = "Please enter at least 3 options. Using default options."
    else:
        st.session_state.options = opts
        st.session_state.error = ""
    st.session_state.beats = build_relationships(st.session_state.options)


def play(user_choice: str):
    computer_choice = random.choice(st.session_state.options)
    result = play_round(user_choice, computer_choice, st.session_state.beats)

    if result == "draw":
        st.session_state.rating += 50
        st.session_state.message = f"There is a draw ({computer_choice})"
    elif result == "win":
        st.session_state.rating += 100
        st.session_state.message = f"Well done. The computer chose {computer_choice} and failed"
    else:
        st.session_state.message = f"Sorry, but the computer chose {computer_choice}"

    name = st.session_state.name.lower().strip()
    if name:
        save_rating(name, st.session_state.rating, RATING_FILE)


def get_leaderboard():
    leaderboard = {}
    try:
        with open(RATING_FILE, "r") as file:
            for line in file:
                parts = line.strip().split()
                if len(parts) == 2:
                    user = parts[0].lower().strip()
                    score = int(parts[1])
                    # Keep only highest score for each user
                    if user not in leaderboard or score > leaderboard[user]:
                        leaderboard[user] = score
    except Exception:
        return []
    # Sort by score descending
    sorted_leaderboard = sorted(leaderboard.items(), key=lambda x: x[1], reverse=True)
    return sorted_leaderboard[:10]


def clear_all_ratings():
    try:
        with open(RATING_FILE, "w") as file:
            file.write("")
        st.session_state.rating = 0
        st.session_state.message = "All ratings have been cleared."
    except Exception as e:
        st.session_state.message = f"Error clearing ratings: {e}"


def main():
    st.set_page_config(page_title="Rock Paper Scissors", page_icon="🪨")
    init_state()

    st.title("Rock Paper Scissors")
    st.markdown("""
    Welcome to Rock Paper Scissors!
    
    **How to play:**
    - Enter your name to track your rating.
    - You can customize the options (minimum 3, comma-separated).
    - Click a button to play a round against the computer.
    - Your rating is saved automatically.
    
    **Rules:**
    - Each choice beats the next half of the list (circular logic).
    """)

    # Add clear ratings button
    if st.button("Clear All Ratings", type="primary"):
        clear_all_ratings()

    name = st.text_input("Your name", value=st.session_state.name)
    normalized_name = name.lower().strip()
    if normalized_name != st.session_state.name:
        st.session_state.name = normalized_name
        load_user_rating()

    if not st.session_state.name:
        st.warning("Please enter your name to track your rating.")

    st.write(f"Current rating: **{st.session_state.rating}**")

    options_text = st.text_input(
        "Options (comma-separated)",
        value=",".join(st.session_state.options),
        help="Leave blank for default rock,paper,scissors",
    )
    if st.button("Update options"):
        update_options(options_text)

    if st.session_state.error:
        st.error(st.session_state.error)

    st.subheader("Play a round")
    if st.session_state.name:
        cols = st.columns(len(st.session_state.options))
        for col, opt in zip(cols, st.session_state.options):
            if col.button(opt.capitalize()):
                play(opt)
    else:
        st.info("Enter your name above to start playing.")

    if st.session_state.message:
        st.info(st.session_state.message)

    st.caption("Rating saves automatically when you play. Options follow circular rules: each choice beats the next half of the list.")

    st.subheader("Leaderboard (Top 10)")
    leaderboard = get_leaderboard()
    if leaderboard:
        for i, (user, score) in enumerate(leaderboard, 1):
            st.write(f"{i}. {user}: {score}")
    else:
        st.write("No ratings yet.")


if __name__ == "__main__":
    main()
