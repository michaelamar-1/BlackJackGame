from pygame import mixer
from rich.console import Console
from rich.panel import Panel
from Deck import Deck
from Player import Player
from Stats import update_stats, print_stats
console = Console()


def play_card_sound():
    """
    Play the card-dealing sound effect.
    :return: None
    """
    mixer.init()
    mixer.music.load('card.wav')
    mixer.music.play()


def get_card_display(card):
    """
    Return a Rich-formatted string for a single playing card.
    :param card: tuple (rank, suit), e.g. ('A', '♥️')
    :return: str Rich markup, e.g. "[red]A♥️[/red]"
    """
    rank, suit = card
    color = "red" if suit in ['♥️', '♦️'] else "white"
    return f"[{color}]{rank}{suit}[/{color}]"


def show_hand(player, reveal_all=True, is_blackjack=False, title="Your hand"):
    """
    Render a player's hand as a Rich Panel, showing soft/hard totals or hiding the dealer hole card.
    :param player: Player instance (has .hand list of cards)
    :param reveal_all: bool, if False hides the dealer's second card
    :param is_blackjack: bool, if True forces score to "21" and appends "(Blackjack!)"
    :param title: str, panel title
    :return: Panel object
    """
    if not reveal_all:
        first = get_card_display(player.hand[0])
        return Panel(f"{first}, [?]", title=title, border_style="magenta")

    hard, aces = 0, 0
    for rank, _ in player.hand:
        if rank.isdigit():
            hard += int(rank)
        elif rank in ['J', 'Q', 'K']:
            hard += 10
        else:  # Ace
            hard += 1
            aces += 1

    if is_blackjack:
        score = "21"
    elif aces and hard + 10 <= 21:
        score = f"{hard}/{hard + 10}"
    else:
        score = str(hard)

    label = " (Blackjack!)" if is_blackjack else ""
    cards = ", ".join(get_card_display(c) for c in player.hand)
    style = "cyan" if title.startswith("Your") else "magenta"
    return Panel(f"{cards}{label}", title=f"{title} ({score})", border_style=style)


def is_blackjack(hand):
    """
    Check if a two-card hand is a natural blackjack (Ace + 10-value).
    :param hand: list of card tuples
    :return: bool
    """
    if len(hand) == 2:
        ranks = [c[0] for c in hand]
        return 'A' in ranks and any(r in ['10', 'J', 'Q', 'K'] for r in ranks)
    return False


def card_value(card):
    """
    Return the Blackjack point value of a single card.
    :param card: tuple (rank, suit)
    :return: int 1–11
    """
    rank, _ = card
    if rank.isdigit():
        return int(rank)
    if rank in ['J', 'Q', 'K']:
        return 10
    return 11  # Ace


def can_split(hand):
    """
    Determine if a two-card hand can be split (same value).
    :param hand: list of two card tuples
    :return: bool
    """
    return len(hand) == 2 and card_value(hand[0]) == card_value(hand[1])


def get_bet(bankroll):
    """
    Prompt the player to place a bet within their bankroll.
    :param bankroll: int current bankroll
    :return: int bet amount
    """
    while True:
        console.print("Welcome to the BlackJack Game!")
        try:
            amt = int(console.input(f"[bold yellow]Your bankroll is: ${bankroll}. Please place your bet:[/bold yellow] "))
            if 1 <= amt <= bankroll:
                return amt
        except ValueError:
            pass
        console.print("[red]Invalid bet—must be an integer between 1 and your bankroll.[/red]")


def play_single_hand(deck, cards, bet, bankroll, hand_number=None):
    """
    Play one player's hand, offering hit/stay/double as allowed.
    :param deck: Deck instance
    :param cards: list of initial card tuples for this hand
    :param bet: int current bet on this hand
    :param bankroll: int total bankroll available
    :param hand_number: optional int for display
    :return: (Player, status_str, final_bet)
    """
    player = Player("Player")
    for c in cards:
        player.add_card(c)

    # Check for natural blackjack
    if is_blackjack(player.hand):
        return player, "blackjack", bet

    first = True
    while True:
        console.print()
        console.print(show_hand(player, title=f"Hand {hand_number}" if hand_number else "Your hand"))

        # Build action options
        opts = "(h)it, (s)tay"
        if first and len(player.hand) == 2 and bet * 2 <= bankroll:
            opts += ", (d)ouble"

        action = console.input(f"[bold yellow]Bet ${bet}. Choice {opts}:[/bold yellow] ").lower()

        if action == 'h':
            # Hit
            player.add_card(deck.deal_card())
            play_card_sound()
            if player.calculate_score() > 21:
                console.print(show_hand(player, title=f"Hand {hand_number}"))
                console.print(Panel("Bust!", style="bold red"))
                return player, "bust", bet

        elif action == 'd' and first and len(player.hand) == 2 and bet * 2 <= bankroll:
            # Double down
            bet *= 2
            player.add_card(deck.deal_card())
            play_card_sound()
            console.print(show_hand(player, title=f"Hand {hand_number}"))
            if player.calculate_score() > 21:
                console.print(Panel("Bust!", style="bold red"))
                return player, "bust", bet
            console.print(Panel("Double down—standing", style="yellow"))
            return player, "play", bet

        else:
            # Stay
            break

        first = False

    return player, "play", bet


def play_split_hands(deck, hands, base_bet, bankroll):
    """
    Play multiple hands created by a split.
    :param deck: Deck instance
    :param hands: list of hands (each a list of card tuples)
    :param base_bet: int original bet per hand
    :param bankroll: int total bankroll available
    :return: (players, statuses, bets) lists
    """
    players, statuses, bets = [], [], []
    for idx, h in enumerate(hands, 1):
        console.print("\n" + "─" * 79)
        console.print(Panel(f"▶️ Playing Hand {idx}", style="bold magenta"))
        p, st, bt = play_single_hand(deck, h, base_bet, bankroll, hand_number=idx)
        players.append(p)
        statuses.append(st)
        bets.append(bt)
    return players, statuses, bets


def dealer_turn(deck, dealer):
    """
    Execute the dealer's turn: hit until 17 or more.
    :param deck: Deck instance
    :param dealer: Player instance for dealer
    :return: dealer with final hand
    """
    console.print("\n" + "─" * 79)
    console.print(Panel("Dealer's turn...", style="magenta"))
    while dealer.calculate_score() < 17:
        dealer.add_card(deck.deal_card())
        play_card_sound()
        console.print(show_hand(dealer, title="Dealer"))
    return dealer


def play_game():
    """
    Main game loop:
      - Clear screen & shuffle
      - Get bet
      - Deal initial cards
      - Handle naturals (blackjack)
      - Offer splits & play player hands
      - Dealer turn
      - Resolve outcomes & update stats
      - Repeat until bankroll depleted
    """
    bankroll = 1000
    deck = Deck()

    while True:
        deck.shuffle()

        bet = get_bet(bankroll)

        # Deal initial cards to player and dealer
        player = Player("Player")
        dealer = Player("Dealer")
        for _ in range(2):
            player.add_card(deck.deal_card())
            dealer.add_card(deck.deal_card())
        play_card_sound()

        # Display hands (hide dealer hole card)
        console.print("\n" + "─" * 79)
        console.print(show_hand(player, is_blackjack=is_blackjack(player.hand), title="Your hand"))
        console.print(show_hand(dealer, reveal_all=False, title="Dealer"))

        # Check for naturals
        p_nat = is_blackjack(player.hand)
        d_nat = is_blackjack(dealer.hand)
        if p_nat or d_nat:
            if p_nat and not d_nat:
                payout = int(1.5 * bet)
                bankroll += payout
                console.print(Panel(f"Blackjack! You win ${payout}", style="bold green"))
                update_stats("player")
            elif d_nat and not p_nat:
                bankroll -= bet
                console.print(Panel(f"Dealer Blackjack—You lose ${bet}", style="bold red"))
                update_stats("dealer")
            else:
                console.print(Panel("Tie—both Blackjack", style="bold blue"))
                update_stats("tie")
            print_stats()
            continue

        # Offer split if applicable
        hands = [player.hand]
        split_aces = False
        if can_split(player.hand):
            # Auto-split Aces
            if player.hand[0][0] == 'A' and player.hand[1][0] == 'A':
                split_aces = True
                c1, c2 = player.hand
                hands = [[c1, deck.deal_card()], [c2, deck.deal_card()]]
                play_card_sound(); play_card_sound()
            else:
                console.print("\n" + "─" * 79)
                console.print(show_hand(player, title="Your hand"))
                if console.input("[bold yellow]Split? (y/n): [/bold yellow]").lower() == 'y':
                    c1, c2 = player.hand
                    hands = [[c1, deck.deal_card()], [c2, deck.deal_card()]]
                    play_card_sound(); play_card_sound()

        # Play player hand(s)
        if split_aces:
            players, statuses, bets = [], [], []
            for h in hands:
                p = Player("Player")
                for c in h:
                    p.add_card(c)
                players.append(p)
                statuses.append("play")
                bets.append(bet)
        else:
            players, statuses, bets = play_split_hands(deck, hands, bet, bankroll)

        # Dealer's turn
        dealer = dealer_turn(deck, dealer)
        console.print("\n" + "─" * 79)
        console.print(show_hand(dealer, title="Dealer final"))

        # Resolve outcomes for each hand
        for idx, (p, st, bt) in enumerate(zip(players, statuses, bets), 1):
            console.print("\n" + "─" * 79)
            console.print(show_hand(p, title=f"Result Hand {idx}"))
            ps = p.calculate_score()
            ds = dealer.calculate_score()

            if st == "bust" or (st != "blackjack" and ds <= 21 and ps < ds):
                bankroll -= bt
                console.print(Panel(f"Hand {idx}: You lose ${bt}", style="bold red"))
                update_stats("dealer")

            elif st == "blackjack":
                payout = int(1.5 * bt)
                bankroll += payout
                console.print(Panel(f"Hand {idx}: Blackjack! You win ${payout}", style="bold green"))
                update_stats("player")

            elif ds > 21 or ps > ds:
                bankroll += bt
                console.print(Panel(f"Hand {idx}: You win ${bt}", style="bold green"))
                update_stats("player")

            else:
                console.print(Panel(f"Hand {idx}: Tie—no change", style="bold blue"))
                update_stats("tie")

        print_stats()
        console.print(f"[bold]New bankroll: ${bankroll}[/]\n")

        if bankroll < 1:
            console.print("[bold red]You are out of money! Game over.[/]")
            break


if __name__ == "__main__":
    play_game()
