import tkinter as tk
from tkinter import messagebox  # Using this for displaying the game in GUI

# Initialize global variables for tracking the scores
player_x_score = 0  # Score for Player X (human)
player_o_score = 0  # Score for Player O (computer)
draws = 0           # Count of draws
winner = False
buttons = []

# Function to check if there's a winner or if the game is a draw
def check_winner():
    global winner, player_x_score, player_o_score, draws
    # Define all possible winning combinations
    winning_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
        [0, 4, 8], [2, 4, 6]              # diagonals
    ]
    
    # Check each winning combination
    for combo in winning_combinations:
        if buttons[combo[0]]["text"] == buttons[combo[1]]["text"] == buttons[combo[2]]["text"] != "":
            # Highlight winning buttons
            buttons[combo[0]].config(bg="green")
            buttons[combo[1]].config(bg="green")
            buttons[combo[2]].config(bg="green")
            winner = True  # Set winner flag
            # Update score based on the winner
            if buttons[combo[0]]["text"] == "X":
                player_x_score += 10  # Increase score by 10 for Player X
                update_score()  # Update displayed scores
                messagebox.showinfo("Tic-Tac-Toe", "Player X wins!")  # Inform player
            else:
                player_o_score += 10  # Increase score by 10 for Player O
                update_score()  # Update displayed scores
                messagebox.showinfo("Tic-Tac-Toe", "Player O wins!")  # Inform player
            reset_board()  # Reset the board for a new game
            return

    # Check for a draw
    if all(button["text"] != "" for button in buttons) and not winner:
        draws += 1  # Increment draw count
        update_score()  # Update displayed scores
        messagebox.showinfo("Tic-Tac-Toe", "It's a draw!")  # Inform players
        reset_board()  # Reset the board for a new game

# Minimax algorithm to calculate the best move for the computer
def minimax(board, depth, is_maximizing):
    score = evaluate(board)  # Evaluate the current board state

    # Return scores based on the game outcome
    if score == 10:  # Computer wins
        return 10 - depth  # Prefer winning sooner
    if score == -10:  # Human wins
        return -10 + depth  # Prefer losing later
    if all(button["text"] != "" for button in buttons):  # Draw condition
        return 0  # Return 0 for a draw

    # Maximizing player's turn (Computer)
    if is_maximizing:
        best = -float('inf')  # Initialize best score
        for i in range(9):
            if buttons[i]["text"] == "":  # Check for empty cell
                buttons[i]["text"] = "O"  # Simulate computer's move
                best = max(best, minimax(buttons, depth + 1, False))  # Recur for minimizing player
                buttons[i]["text"] = ""  # Undo move
        return best  # Return best score for maximizing player
    else:  # Minimizing player's turn (Human)
        best = float('inf')  # Initialize best score
        for i in range(9):
            if buttons[i]["text"] == "":  # Check for empty cell
                buttons[i]["text"] = "X"  # Simulate human's move
                best = min(best, minimax(buttons, depth + 1, True))  # Recur for maximizing player
                buttons[i]["text"] = ""  # Undo move
        return best  # Return best score for minimizing player

# Evaluate the current board state
def evaluate(board):
    winning_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
 [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0 , 4, 8], [2, 4, 6]
    ]
    
    # Check each winning combination
    for combo in winning_combinations:
        if buttons[combo[0]]["text"] == buttons[combo[1]]["text"] == buttons[combo[2]]["text"]:
            if buttons[combo[0]]["text"] == "O":
                return 10  # Computer wins
            elif buttons[combo[0]]["text"] == "X":
                return -10  # Human wins
    return 0  # Return 0 for a draw or incomplete game

# Calculate the best move for the computer (Player 2, 'O')
def best_move():
    best_val = -float('inf')  # Initialize best score
    best_move = -1  # Initialize best move

    for i in range(9):
        if buttons[i]["text"] == "":  # Check for empty cell
            buttons[i]["text"] = "O"  # Simulate computer's move
            move_val = minimax(buttons, 0, False)  # Evaluate move using Minimax
            buttons[i]["text"] = ""  # Undo move
            if move_val > best_val:
                best_val = move_val
                best_move = i  # Update best move
    return best_move  # Return best move for the computer

# Computer's move based on Minimax algorithm
def computer_move():
    best = best_move()  # Calculate the best move using Minimax
    if best != -1:
        buttons[best]["text"] = "O"  # Make the computer's move
        check_winner()  # Check for a winner or draw
        if not winner:
            toggle_player()  # Toggle player's turn

# Toggle between players
def toggle_player():
    global current_player
    current_player = "X" if current_player == "O" else "O"  # Toggle player
    label.config(text=f"Player {current_player}'s turn")  # Update displayed player's turn

# Handle button click for human player's move
def button_click(index):
    if buttons[index]["text"] == "" and not winner:
        buttons[index]["text"] = current_player  # Make human's move
        check_winner()  # Check for a winner or draw
        if not winner:
            toggle_player()  # Toggle player's turn
            if current_player == "O":  # Computer's turn
                computer_move()  # Make computer's move using Minimax

# Reset the board for a new game
def reset_board():
    global winner
    winner = False
    for button in buttons:
        button["text"] = ""
        button.config(bg="SystemButtonFace")  # Reset button colors

# Update the score display
def update_score():
    score_label.config(text=f"Player X: {player_x_score}  Player O: {player_o_score}  Draws: {draws}")

# Initialize the game window
root = tk.Tk()
root.title("Tic-Tac-Toe")

# Create the game buttons
buttons = [tk.Button(root, text="", font=('Arial', 24), width=5, height=2,
                     command=lambda i=i: button_click(i)) for i in range(9)]
for i, button in enumerate(buttons):
    button.grid(row=i // 3, column=i % 3)

current_player = "X"
winner = False

# Create a label to show which player's turn it is
label = tk.Label(root, text=f"Player {current_player}'s turn", font=('Arial', 16))
label.grid(row=3, column=0, columnspan=3)

# Create a score label to track the scores of both players
score_label = tk.Label(root, text=f"Player X: {player_x_score}  Player O: {player_o_score}  Draws: {draws}", font=('Arial', 16))
score_label.grid(row=4, column=0, columnspan=3)

root.mainloop()