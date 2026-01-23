A customizable, extensible Rock Paper Scissors engine built with Python. Unlike traditional versions, this "Smart" edition supports dynamic rule sets (like Rock-Paper-Scissors-Lizard-Spock) using circular logic, tracks persistent user ratings, and offers both a modern Web UI and a classic CLI.

---

## ✨ Key Features

-   **🧠 Smart Circular Logic**: Input any number of options (e.g., `rock,paper,scissors,lizard,spock`), and the game automatically builds a balanced circular relationship where each choice beats exactly half of the others.
-   **🎨 Modern Web UI**: A sleek, card-based interface built with **Streamlit**, featuring custom CSS, glassmorphism effects, and real-time history tracking.
-   **⌨️ Classic CLI**: A lightweight command-line version for quick sessions.
-   **📈 Persistent Scoring**: All ratings are saved to `rating.txt`, allowing players to build their scores over multiple sessions.
-   **🏆 Leaderboard**: Tracks top performers across the application.

---

## 🚀 Quick Start

### 1. Installation

First, clone the repository and install the dependencies:

```bash
git clone https://github.com/srinivasagudi0/smart-rps-game.git
cd smart-rps-game
pip install -r requirements.txt
```

### 2. Run the Web App (Recommended)
Experience the game with a modern graphical interface:

```bash
streamlit run rps_app.py
```
*Once running, navigate to the URL provided in your terminal (usually `http://localhost:8501`).*

### 3. Run the CLI Version
For a classic terminal-based experience:

```bash
python rock_paper_scissor.py
```

---

## 🧠 How the "Smart" Logic Works

The game uses a **Circular Win Condition** algorithm. When you provide a list of options:
1.  The options are arranged in a circle.
2.  For any chosen option, it **wins** against the half of the list that follows it in the circle.
3.  It **loses** against the half of the list that precedes it.

**Example (5 options):**
If you play with `rock, gun, lightning, devil, dragon`:
-   `rock` beats `devil` and `dragon`.
-   `rock` loses to `gun` and `lightning`.

---

## 📊 Scoring System

-   **Win**: +100 points
-   **Draw**: +50 points
-   **Loss**: 0 points (and the round ends!)

Scores are automatically saved to `rating.txt` associated with your username.

---

## 🛠️ Project Structure

```text
.
├── rps_app.py              # Streamlit Web Application (Frontend)
├── rock_paper_scissor.py   # Core Logic & CLI Implementation
├── rating.txt              # Persistent score storage
├── requirements.txt        # Project dependencies
└── README.md               # Documentation
```

---

## 🤝 Contributing

Contributions are welcome! If you have ideas for new features (like AI patterns or global leaderboards), feel free to:
1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

---

**Created by [srinivasagudi0](https://github.com/srinivasagudi0)**
