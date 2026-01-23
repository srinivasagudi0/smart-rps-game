import html
import os
import random
import streamlit as st

# Flexible import for both direct and package runs
try:
    from game.rock_paper_scissor import build_relationships, load_rating, play_round, save_rating
except ImportError:
    from rock_paper_scissor import build_relationships, load_rating, play_round, save_rating

RATING_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'rating.txt'))
DEFAULT_OPTIONS = ["rock", "paper", "scissors"]


def inject_styles():
    """Global styles to give the app a vivid, card-based look."""
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Clash+Grotesk:wght@500;600;700&family=Space+Mono:wght@400;700&display=swap');
        :root {
            --bg-1: #05060f;
            --bg-2: #0c1224;
            --panel: rgba(255, 255, 255, 0.05);
            --panel-strong: rgba(255, 255, 255, 0.12);
            --accent: #7c3aed;
            --accent-2: #22d3ee;
            --muted: #94a3b8;
            --text: #e5e7eb;
            --glass: rgba(255,255,255,0.08);
        }
        * { font-family: 'Clash Grotesk', 'Space Mono', system-ui, -apple-system, sans-serif; letter-spacing: 0.01em; }
        body {
            background: radial-gradient(circle at 15% 20%, rgba(124,58,237,0.22), transparent 23%),
                        radial-gradient(circle at 85% 12%, rgba(34,211,238,0.18), transparent 20%),
                        linear-gradient(135deg, var(--bg-1), var(--bg-2));
            color: var(--text);
        }
        .block-container { padding-top: 2.4rem; padding-bottom: 2.4rem; }
        .hero {
            background: linear-gradient(135deg, rgba(124,58,237,0.18), rgba(34,211,238,0.16));
            border: 1px solid rgba(255,255,255,0.08);
            padding: 1.6rem 1.8rem;
            border-radius: 18px;
            box-shadow: 0 18px 60px rgba(0,0,0,0.35);
        }
        .pill {
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            background: rgba(255,255,255,0.08);
            border-radius: 999px;
            padding: 0.35rem 0.8rem;
            font-size: 0.9rem;
            color: var(--text);
        }
        .metrics { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 0.8rem; margin-top: 1rem; }
        .metric {
            background: var(--panel);
            border: 1px solid rgba(255,255,255,0.07);
            padding: 0.85rem 1rem;
            border-radius: 12px;
            position: relative;
            overflow: hidden;
        }
        .metric::after {
            content: '';
            position: absolute;
            inset: 0;
            background: linear-gradient(125deg, rgba(124,58,237,0.12), rgba(34,211,238,0.1));
            opacity: 0.6;
        }
        .metric span { color: var(--muted); font-size: 0.85rem; position: relative; }
        .metric strong { display: block; font-size: 1.35rem; margin-top: 0.25rem; position: relative; }
        .glass {
            background: var(--panel);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 16px;
            padding: 1rem 1.15rem;
            box-shadow: 0 16px 40px rgba(0,0,0,0.35);
        }
        .status-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.6rem 0.9rem;
            border-radius: 14px;
            color: #0f172a;
            font-weight: 700;
            background: linear-gradient(135deg, #bbf7d0, #34d399);
            box-shadow: 0 10px 30px rgba(34,197,94,0.25);
        }
        .status-badge.warn { background: linear-gradient(135deg, #fed7aa, #fb923c); box-shadow: 0 10px 30px rgba(249,115,22,0.25); }
        .status-badge.info { background: linear-gradient(135deg, #bae6fd, #38bdf8); box-shadow: 0 10px 30px rgba(56,189,248,0.25); }
        .history-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 0.75rem; }
        .history-card {
            border-radius: 14px;
            padding: 0.75rem 0.9rem;
            border: 1px solid rgba(255,255,255,0.08);
            background: linear-gradient(145deg, rgba(255,255,255,0.04), rgba(255,255,255,0.02));
        }
        .history-card.win { border-color: rgba(34,197,94,0.35); }
        .history-card.draw { border-color: rgba(56,189,248,0.35); }
        .history-card.lose { border-color: rgba(248,113,113,0.4); }
        .history-card .label { color: var(--muted); font-size: 0.85rem; }
        .history-card .value { font-weight: 700; font-size: 1.1rem; }
        div.stButton > button {
            width: 100%;
            border-radius: 12px;
            border: 1px solid rgba(255,255,255,0.15);
            background: linear-gradient(135deg, rgba(124,58,237,0.22), rgba(34,211,238,0.2));
            color: var(--text);
            font-weight: 700;
            padding: 0.7rem 0.5rem;
        }
        div.stButton > button:disabled { opacity: 0.35; cursor: not-allowed; }
        .leaderboard-row {
            display: flex;
            justify-content: space-between;
            padding: 0.55rem 0.8rem;
            border-radius: 10px;
            border: 1px solid rgba(255,255,255,0.06);
            background: rgba(255,255,255,0.03);
        }
        .name-gate {
            background: var(--panel);
            border: 1px dashed rgba(255,255,255,0.2);
            border-radius: 14px;
            padding: 1rem 1.2rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def init_state():
    if "name" not in st.session_state:
        st.session_state.name = ""
    if "name_confirmed" not in st.session_state:
        st.session_state.name_confirmed = False
    if "rating" not in st.session_state:
        st.session_state.rating = 0
    if "rounds_played" not in st.session_state:
        st.session_state.rounds_played = 0
    if "options" not in st.session_state:
        st.session_state.options = DEFAULT_OPTIONS.copy()
    if "beats" not in st.session_state:
        st.session_state.beats = build_relationships(st.session_state.options)
    if "message" not in st.session_state:
        st.session_state.message = ""
    if "error" not in st.session_state:
        st.session_state.error = ""
    if "game_over" not in st.session_state:
        st.session_state.game_over = False
    if "history" not in st.session_state:
        st.session_state.history = []


def reset_round(reset_rating: bool = False, clear_history: bool = False):
    """Clear round-specific state so the user can't keep playing after a loss."""
    st.session_state.game_over = False
    st.session_state.message = ""
    if clear_history:
        st.session_state.history = []
        st.session_state.rounds_played = 0
    if reset_rating:
        st.session_state.rating = 0


def load_user_rating():
    name = st.session_state.name.lower().strip()
    if name:
        st.session_state.rating = load_rating(name, RATING_FILE)
    else:
        st.session_state.rating = 0
    reset_round(clear_history=True)


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
    reset_round(clear_history=True)


def play(user_choice: str):
    if st.session_state.game_over:
        return

    computer_choice = random.choice(st.session_state.options)
    result = play_round(user_choice, computer_choice, st.session_state.beats)

    if result == "draw":
        st.session_state.rating += 50
        st.session_state.message = f"There is a draw ({computer_choice})"
    elif result == "win":
        st.session_state.rating += 100
        st.session_state.message = f"Well done. The computer chose {computer_choice} and failed"
    else:
        st.session_state.message = f"Sorry, but the computer chose {computer_choice}. Game over!"
        st.session_state.game_over = True

    st.session_state.rounds_played += 1
    st.session_state.history.insert(
        0,
        {
            "result": result,
            "user": user_choice,
            "computer": computer_choice,
        },
    )
    st.session_state.history = st.session_state.history[:8]

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
        reset_round(reset_rating=True, clear_history=True)
        st.session_state.message = "All ratings have been cleared."
    except Exception as e:
        reset_round()
        st.session_state.message = f"Error clearing ratings: {e}"


def main():
    st.set_page_config(page_title="Rock Paper Scissors", page_icon="🪨", layout="wide")
    inject_styles()
    init_state()

    display_name = html.escape((st.session_state.name or "Anonymous").title())
    hero_html = f"""
    <div class="hero">
        <div class="pill">Arcade mode · Versus CPU</div>
        <h1 style="margin-bottom: 0.35rem;">Rock • Paper • Scissors</h1>
        <p style="color: var(--muted); max-width: 820px; margin-bottom: 1rem;">
            Quick-fire rounds with a circular ruleset. Customize the options, make your move, and climb the leaderboard.
        </p>
        <div class="metrics">
            <div class="metric"><span>Player</span><strong>{display_name}</strong></div>
            <div class="metric"><span>Rating</span><strong>{st.session_state.rating}</strong></div>
            <div class="metric"><span>Rounds this session</span><strong>{st.session_state.rounds_played}</strong></div>
            <div class="metric"><span>Options in play</span><strong>{len(st.session_state.options)}</strong></div>
        </div>
    </div>
    """
    st.markdown(hero_html, unsafe_allow_html=True)
    st.caption("Circular rules: each choice beats the next half of the list. A loss ends the run—hit restart to jump back in.")

    left, right = st.columns([1.65, 1.1], gap="large")

    with left:
        st.markdown("### Setup")
        with st.container():
            name_col, action_col = st.columns([0.7, 0.3])
            with name_col:
                name_input = st.text_input("Your name", value=st.session_state.name, placeholder="Type a nickname")
            with action_col:
                confirm_disabled = not name_input.strip()
                if st.button("Lock name", disabled=confirm_disabled):
                    st.session_state.name = name_input.lower().strip()
                    st.session_state.name_confirmed = True
                    load_user_rating()

        if not st.session_state.name_confirmed:
            st.markdown(
                """
                <div class="name-gate">
                    <strong>Step 1.</strong> Enter a name and lock it in to start playing. Ratings save under that name.
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.caption("Name locked. Rating saves automatically when you play.")

        options_text = st.text_input(
            "Options (comma-separated)",
            value=",".join(st.session_state.options),
            help="Leave blank for default rock,paper,scissors",
            disabled=not st.session_state.name_confirmed,
        )
        opt_cols = st.columns([1, 1])
        with opt_cols[0]:
            if st.button("Update options", disabled=not st.session_state.name_confirmed):
                update_options(options_text)
        with opt_cols[1]:
            if st.button("Clear All Ratings", disabled=not st.session_state.name_confirmed):
                clear_all_ratings()

        if st.session_state.error:
            st.error(st.session_state.error)

        st.markdown("### Make your move")
        if st.session_state.name_confirmed:
            cols = st.columns(len(st.session_state.options))
            for col, opt in zip(cols, st.session_state.options):
                if col.button(opt.capitalize(), disabled=st.session_state.game_over, key=f"opt-{opt}"):
                    play(opt)
            if st.session_state.game_over:
                st.warning("You lost. Click Restart to play again.")
                if st.button("Restart round"):
                    reset_round()
        else:
            st.info("Enter and lock your name to start playing.")

    with right:
        st.markdown("### Status")
        last_result = st.session_state.history[0]["result"] if st.session_state.history else None
        status_class = "status-badge"
        status_icon = "🪨"
        status_text = "Waiting for your first move"
        if st.session_state.game_over:
            status_class += " warn"
            status_icon = "💥"
            status_text = st.session_state.message or "You lost the last round."
        elif st.session_state.message:
            status_icon = "🎉" if last_result == "win" else "🤝" if last_result == "draw" else "⚠️"
            status_class += "" if last_result == "win" else " info" if last_result == "draw" else " warn"
            status_text = st.session_state.message

        st.markdown(
            f"""
            <div class="glass">
                <div class="{status_class}">
                    <span>{status_icon}</span><span>{html.escape(status_text)}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("### Recent rounds")
        if st.session_state.history:
            items = []
            for entry in st.session_state.history[:6]:
                items.append(
                    f"""
                    <div class="history-card {entry['result']}">
                        <div class="label">Result</div>
                        <div class="value">{entry['result'].title()}</div>
                        <div class="label" style="margin-top: 0.4rem;">You vs CPU</div>
                        <div class="value">{html.escape(entry['user'])} • {html.escape(entry['computer'])}</div>
                    </div>
                    """
                )
            st.markdown(f"""<div class="history-grid">{''.join(items)}</div>""", unsafe_allow_html=True)
        else:
            st.info("Play a round to see your history.")

        st.markdown("### Leaderboard (Top 10)")
        leaderboard = get_leaderboard()
        if leaderboard:
            rows = []
            for i, (user, score) in enumerate(leaderboard, 1):
                rows.append(
                    f"""
                    <div class="leaderboard-row">
                        <div>{i}. {html.escape(user)}</div>
                        <div><strong>{score}</strong></div>
                    </div>
                    """
                )
            st.markdown("".join(rows), unsafe_allow_html=True)
        else:
            st.write("No ratings yet.")


if __name__ == "__main__":
    main()
