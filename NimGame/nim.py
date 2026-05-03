import tkinter as tk
from engine import MyButton, Player
import engine

root = tk.Tk()
root.title("Nim Game")
root.configure(bg="#2B2B1C")

def restart(items, players):
    for this_object in root.winfo_children():
        this_object.destroy()
    engine.last_move = 0
    build_board()

def build_board():
    piles = [5, 7, 9, 11]
    items = []
    previous = 0
    currnet = 0
    colors = ["#89FA96","#FACF89","#CF89FA","#99F4FF"]
    this_color = colors[0]


    for row, piles_idx in enumerate(piles):
        row_frame = tk.Frame(root, bg="#2B2B1C", padx=10, pady=8)
        row_frame.pack(padx=1, pady=1, fill="x")

        tk.Label(
            row_frame,
            text=f"Row {row + 1}",
            font=("Courier", 12, "bold"),
            bg="#2B2B1C",
            fg="#cdd6f4",
            width=6,
        ).pack(side="left")

        for i in range(piles_idx):
            current = i
            if current==0 and previous==4:
                this_color = colors[1]
            elif current==0 and previous==6:
                this_color = colors[2]
            elif current==0 and previous==8:
                this_color = colors[3]
            items.append(MyButton(row_frame, pile_idx=row, item_idx=i,color=this_color))
            previous = i

    number_of_players = 2
    players = [Player(id) for id in range(number_of_players)]
    players[0].turn = 1

    enter_frame = tk.Frame(root, bg="#2B2B1C", padx=10, pady=8,)
    enter_frame.pack(padx=1, pady=1, fill="x")
    enter = tk.Button(
            enter_frame,
            text="Enter",
            font=("Courier", 15),
            width=4,
            bg="#D7CEB7",
            fg="#000000",
            bd=3,
        )
    enter.config(command=lambda:engine.enter_action(items, players, last_move_label))
    enter.pack(side="left", padx=3)


    last_move_label = tk.Label(
        enter_frame, text="Last move: —",
        font=("Courier", 12), bg="#2B2B1C", fg="#cdd6f4"
    )
    last_move_label.pack(side="left", padx=10)

    restart_btn = tk.Button(
        enter_frame, text="Restart",
        font=("Courier", 15),
        bg="#FF6B6B", fg="#000000",
        command=lambda:restart(items, players)
    )
    restart_btn.pack(side="left", padx=3)



build_board()
root.mainloop()
