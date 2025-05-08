# BlackJackGame

A terminal-based Python implementation of the classic card game Blackjack, enhanced with:
- **Automatic Blackjack detection**  
- **Split-hand support** when a pair is dealt  
- **Double-down option**  
- **Sound effects** on each card dealt  
- **Statistics tracking** (wins, losses, pushes)  
- **Rich console UI** via [Rich](https://github.com/Textualize/rich)

---

## Table of Contents

1. [Features](#features)  
2. [Installation](#installation)  
3. [Usage](#usage)  
4. [Configuration](#configuration)   
5. [Project Structure](#project-structure)  

---

## Features

- **Automatic Blackjack win** on an Ace + 10-value card  
- **Split Hand**: if initial two cards are a pair, play two hands independently  
- **Double Down**: double your bet and receive exactly one more card  
- **Card-dealing sound** (“card.wav”) on each draw  
- **Persistent stats**: track total games, win/loss/push counts, and win rate  
- **Colored console UI**: clear, colored card display and panels via Rich

---

## Installation

1. **Clone the repo**  
   ```bash
   git clone https://github.com/michaelamar-1/BlackJackGame.git
   cd BlackJackGame
2. (Optional) Create and activate a virtual environment

## Usage
Ensure card.wav sits in the project root (or update the path in play_card_sound()).
Run the game:
python blackjack.py
Follow the on-screen prompts to:
- Place your bet
- Hit or stand
- Split pairs when available
- Double down on favorable hands
After each round, your statistics (wins/losses/pushes) will display and persist.

## Configuration
Sound file
By default, card.wav is loaded from the project root. To use your own .wav file, replace card.wav or update the path argument in play_card_sound().
Starting bankroll
Edit the initial bankroll variable in blackjack.py to set how many chips you start with.

## Project Structure
BlackJackGame/
├── card.wav              # Deal-sound effect
├── blackjack.py          # Main game loop & user interaction
├── Deck.py               # Deck and card-drawing logic
├── Player.py             # Player hand, score calculation, actions
├── Stats.py              # Persistent stats storage and display
├── requirements.txt      # `pygame`, `rich`
└── README.md             # You are here!


