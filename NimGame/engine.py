import random
import tkinter as tk
from tkinter import messagebox

class MyButton:
    def __init__(self, parent, pile_idx, item_idx, color):
        self.pile_idx = pile_idx
        self.item_idx = item_idx
        self.toggled = False
        self.color = color

        self.button = tk.Button(
            parent,
            font=("Courier", 15),
            width=2,
            bg=color,
            fg="#000000",
            bd=3,
        )
        self.button.config(command=self.toggle)
        self.button.pack(side="left", padx=3)

    def toggle(self):
        self.toggled = not self.toggled
        this_color = "#FF6B6B" if self.toggled else self.color
        self.button.config(bg=this_color)

    def remove(self):
        self.button.destroy()

class Player:
    def __init__(self, id):
        self.id = id
        self.turn = 0
        self.mv_count = 0
        self.win = False

last_move = 0
random_guy = True

def enter_update():
    global last_move
    last_move = enter_action(items, last_move)


def valid_move(previous_move, actual_move):
    if previous_move == 0:
        return True
    return actual_move in (previous_move-1,previous_move+1)

def enter_action(items, players, last_move_label):
    global last_move
    toggled_items = [item for item in items if item.toggled]
    actual_move = len(toggled_items)

    if actual_move > 4:
        messagebox.showwarning("Invalid", "Can take only 4 at max")
        return

    elif actual_move > 1:
        for i in range(len(toggled_items)-1):
            if toggled_items[i].pile_idx != toggled_items[i+1].pile_idx:
                messagebox.showwarning("Invalid", "You can only take from the same pile")
                return

    if not valid_move(last_move, actual_move):
        messagebox.showwarning("Invalid","Must be +/- 1 than the previous move")
        return

    else:
        for item in toggled_items:
            item.remove()
            items.remove(item)

        last_move = actual_move

        if players[0].turn == 1:
            players[0].turn = 0
            players[1].turn = 1
        else:
            players[0].turn = 1
            players[1].turn = 0

        possible_moves = [last_move - 1, last_move + 1] if last_move != 0 else [1,2,3,4]
        possible_moves = [m for m in possible_moves if 0 < m <= 4]

        can_move = False
        for item in items:
            pile_size = sum(1 for x in items if x.pile_idx == item.pile_idx)
            if any(m <= pile_size for m in possible_moves):
                can_move = True
                break

        if not can_move:
            if players[0].turn == 1:
                messagebox.showinfo("Game Over", "Player 1 cannot move. Player 2 wins!")
            else:
                messagebox.showinfo("Game Over", "Player 2 cannot move. Player 1 wins!")
            return

        if not items:
            print("Game Finshed")
            if players[0].turn == 1:
                messagebox.showinfo("Player 1 wins","Player 1 wins")
            else:
                messagebox.showinfo("Player 2 wins","Player 2 wins")

    last_move_label.config(text=f"Last move: {actual_move}")

    if players[1].turn == 1 and random_guy:
        last_move_label.after(500, lambda: computer_turn(items, players, last_move_label))


def computer_move(items, players, last_move_label):
    global last_move
    piles = {}

    for item in items:
        piles.setdefault(item.pile_idx, []).append(item)

    if last_move == 0:
        possible_moves = [1, 2, 3, 4]
    else:
        possible_moves = [last_move - 1, last_move + 1]
    possible_moves = [m for m in possible_moves if m > 0 and m <= 4]

    valid_moves = []
    for pile_idx, pile_items in piles.items():
        for move in possible_moves:
            if move <= len(pile_items):
                valid_moves.append((pile_idx, move))

    if not valid_moves:
        messagebox.showinfo("Game Over", "Computer cannot move. Player wins!")
        return

    pile_idx, move = random.choice(valid_moves)

    selected = [item for item in items if item.pile_idx == pile_idx][:move]

    for item in selected:
        item.remove()
        items.remove(item)

    last_move = move
    last_move_label.config(text=f"Last move: {move}")

def computer_turn(items, players, last_move_label):
    global last_move
    computer_move(items, players, last_move_label)

    players[1].turn = 0
    players[0].turn = 1

    if not items:
        messagebox.showinfo("Game Over", "Computer wins!")
