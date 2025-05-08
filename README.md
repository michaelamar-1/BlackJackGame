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

1. [Demo](#demo)  
2. [Features](#features)  
3. [Installation](#installation)  
4. [Usage](#usage)  
5. [Configuration](#configuration)  
6. [Running Tests](#running-tests)  
7. [Project Structure](#project-structure)  
8. [Contributing](#contributing)  
9. [License](#license)

---

## Demo

![Blackjack Screenshot](./assets/demo.png)

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
