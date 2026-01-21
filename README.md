# Rock Paper Scissors (CLI + Streamlit)

Play locally in a terminal or in a simple browser UI. The steps below work on any machine; replace `python3` with `python` or `py` if needed.

## Streamlit UI

1) Install once:  
   `python3 -m pip install -r game/requirements.txt`
2) Run:  
   `python3 -m streamlit run game/rps_app.py`
3) In the browser: enter a name (ratings save to `rating.txt` in the repo root), choose or update options, and click a move to play. A loss ends the round; use **Restart round** to continue.

## CLI

1) Run:  
   `python3 game/rock_paper_scissor.py`
2) Commands: `!rating` shows your score; `!exit` saves and quits. A loss ends the run—restart the script to play again.
