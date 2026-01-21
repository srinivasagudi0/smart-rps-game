# Rock Paper Scissors (CLI + Streamlit)

Play the existing CLI game or a simple Streamlit UI.

## Quick start (Streamlit)

```bash
cd /Users/srinivasagudi/PyCharmMiscProject
python -m streamlit run game/rps_app.py
```

- Enter your name to load/save rating in `rating.txt` (created beside the repo root).
- Optionally set custom options (comma-separated). Blank restores `rock,paper,scissors`.
- Click a choice to play; rating updates per round and persists when a name is set.
- A loss ends the round; click **Restart round** to play again.

## CLI

```bash
cd /Users/srinivasagudi/PyCharmMiscProject
python game/rock_paper_scissor.py
```

Controls: `!rating` shows rating, `!exit` saves & quits. A loss ends the game automatically; restart the script to play again.
