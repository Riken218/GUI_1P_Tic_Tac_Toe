#!/usr/bin/env python

import tkinter as tk
from tkinter import messagebox
import random

# Create window
root = tk.Tk()
root.title('Tic-Tac-Toe')

# Global variables to use
global players, b_click, mark_button, X, O, clicked, turn, CP, Player
global rows, board_positions

# Markers
X = 'X'
O = 'O'
# Number of rows and columns
rows = 3
# Number of positions as a maximum value for turns
board_positions = rows**2
# True if the player clicks to go first in "reset" function
clicked = True
# First turn
turn = 1
# Define things based on if the player moves first or second
if clicked:
    # Player and CP variables to identify which player is which for AI
    CP = 1
    Player = 0
    # Player mark to change the button
    mark_button = X
else:
    CP = 0
    Player = 1
    mark_button = O
'''List of markers.
   This is why "CP" and "Player" variables exist: for this list.'''
players = [X,O]


#######################################################################

'''New "make_board" and "mark_board" functions to use the buttons but
   still make list. This allows all other functions to work.'''
def make_board(button_board):
    # Makes the current board using the button texts
    board = []
    for i in range(len(button_board)):
        row = []
        for j in range(len(button_board[i])):
            exec(
                f'row.append({button_board[i][j]})',
                locals(),
                globals())
        board.append(row)
    return board

# Checks if the board can be marked
# ("board" variable is the button name list with "cget")
def mark_board_check(board, r, c, mark):
    # Trys to mark the board list
    if board[r][c] == ' ':
        return True
    else:
        return False

# Marks the board
def mark_board(board, r, c, mark):
    board[r][c] = mark

#######################################################################

# Checks each row for it to be full of either player's marker.
def check_rows(board, players):
    # Start at Row 1
    row = 1
    for i in range(len(board)):
        xes = []
        oes = []
        # Search each row for all of one marker
        for j in range(len(board[0])):
            if board[i][j] == players[0]:
                xes.append(board[i][j])
            elif board[i][j] == players[1]:
                oes.append(board[i][j])
        # If found, output True and the row number
        if (len(xes) == len(board[0])) or (len(oes) == len(board[0])):
            return [True, row]
        # Otherwise loop through to next row
        else:
            row += 1
    # Final check for row winner
    if (len(xes) == len(board[0])) or (len(oes) == len(board[0])):
        return [True, row]
    # Else output False and non-existent row
    else:
        return [False, 0]

'''Checks each row separately for 1 less than length of row to check
   if it needs to / can block player.'''
def check_1_row(board, players, row):
    xes = []
    oes = []
    for j in range(len(board)):
        if board[row][j] == players[0]:
            xes.append(board[row][j])
        elif board[row][j] == players[1]:
            oes.append(board[row][j])
    '''Outputs whether row is full of one type of marker except for
       one empty space.'''
    if (((len(xes) == len(board[0])-1) and (len(oes) == 0)) or
        ((len(oes) == len(board[0])-1) and (len(xes) == 0))):
        return True
    else:
        return False

# Checks all rows to see if player needs to/can be blocked.
def check_rows_CPU(board, players):
    for i in range(len(board)):
        if check_1_row(board, players, i):
            return True
    return False

'''Checks if the CPU has a winning move in a row. Like
   "check_rows_CPU" function but CP specific.'''
def CPU_win_move_row(board, players, row, CP, Player):
    P_list = []
    CP_list = []
    for i in range(len(board)):
        if board[row][i] == players[CP]:
            CP_list.append(board[row][i])
        elif board[row][i] == players[Player]:
            P_list.append(board[row][i])
    if ((len(CP_list) == len(board[0])-1) and len(P_list) == 0):
        return True
    else:
        return False

'''Checks each column for it to be full of either player's marker.
   Like "check_rows" function but loops through columns instead of
   rows.'''
def check_columns(board, players):
    column = 1
    for j in range(len(board[0])):
        xes = []
        oes = []
        for i in range(len(board)):
            if board[i][j] == players[0]:
                xes.append(board[i][j])
            elif board[i][j] == players[1]:
                oes.append(board[i][j])
        if (len(xes) == len(board[0])) or (len(oes) == len(board[0])):
            return [True, column]
        else:
            column += 1
    if (len(xes) == len(board[0])) or (len(oes) == len(board[0])):
        return [True, column]
    else:
        return [False, 0]

'''Checks each column separately for 1 less than length of column to
   check if it needs to / can block player.
   See "check_1_row" function for more detailed explanation.'''
def check_1_column(board, players, col):
    xes = []
    oes = []
    for i in range(len(board)):
        if board[i][col] == players[0]:
            xes.append(board[i][col])
        elif board[i][col] == players[1]:
            oes.append(board[i][col])
    if (((len(xes) == len(board[0])-1) and (len(oes) == 0)) or
        ((len(oes) == len(board[0])-1) and (len(xes) == 0))):
        return True
    else:
        return False

'''Checks all columns to see if player needs to be / can be blocked.
   See "check_rows_CPU" function for more detailed explanation.'''
def check_columns_CPU(board, players):
    for j in range(len(board)):
        if check_1_column(board, players, j):
            return True
    return False

'''Checks if the CPU has a winning move in a column.
   Like "check_columns_CPU" function but CP specific.'''
def CPU_win_move_column(board, players, col, CP, Player):
    P_list = []
    CP_list = []
    for i in range(len(board)):
        if board[i][col] == players[CP]:
            CP_list.append(board[i][col])
        elif board[i][col] == players[Player]:
            P_list.append(board[i][col])
    if ((len(CP_list) == len(board[0])-1) and len(P_list) == 0):
        return True
    else:
        return False

# # Checks each diagonal for it to be full of either player's marker.
def check_diagonals(board, players):
    # Variable for the ascending diagonal
    x = len(board)-1
    for i in range(len(board)):
        '''Top-left to bottom-right diagonal check (a.k.a. descending
           diagonal). (Also checks smaller diagonals but doesn't slow
           down program overall.)'''
        # Returns "1" for "1st Diagonal" a.k.a. descending diagonal
        xes = []
        oes = []
        for j in range(len(board)):
            if board[j][j] == players[0]:
                xes.append(board[j][j])
            elif board[j][j] == players[1]:
                oes.append(board[j][j])
            if ((len(xes) == len(board[0])) or
                (len(oes) == len(board[0]))):
                return [True, 1]
        '''Bottom-left to top-right diagonal check (a.k.a. ascending 
           diagonal). (Also checks smaller diagonals but doesn't slow
           down program overall.)'''
        # Returns "2" for "2nd Diagonal" a.k.a. ascending diagonal
        xes = []
        oes = []
        for k in range(len(board)):
            if board[k][x-k] == players[0]:
                xes.append(board[k][x-k])
            elif board[k][x-k] == players[1]:
                oes.append(board[k][x-k])
            if ((len(xes) == len(board[0])) or
                (len(oes) == len(board[0]))):
                return [True, 2]
        if (len(xes) == len(board[0])) or (len(oes) == len(board[0])):
            return [True, 2]
    if (len(xes) == len(board[0])) or (len(oes) == len(board[0])):
        return [True, 2]
    else:
        return [False, 0]

'''Checks top-left to bottom-right ("descending") diagonal for CPU to
   block player.'''
def check_1st_diag(board, players):
    xes = []
    oes = []
    for j in range(len(board)):
        if board[j][j] == players[0]:
            xes.append(board[j][j])
        elif board[j][j] == players[1]:
            oes.append(board[j][j])
    if (((len(xes) == len(board[0])-1) and (len(oes) == 0)) or
        ((len(oes) == len(board[0])-1) and (len(xes) == 0))):
        return True
    else:
        return False

# Like "check_1st_diag" but specific for CPU to win
def CPU_win_move_1_diag(board, players, CP, Player):
    P_list = []
    CP_list = []
    for i in range(len(board)):
        if board[i][i] == players[CP]:
            CP_list.append(board[i][i])
        elif board[i][i] == players[Player]:
            P_list.append(board[i][i])
    if ((len(CP_list) == len(board[0])-1) and len(P_list) == 0):
        return True
    else:
        return False

'''Checks bottom-left to top-right ("ascending") diagonal for CPU to
   block player.'''
def check_2nd_diag(board, players):
    x = len(board)-1
    xes = []
    oes = []
    for k in range(len(board)):
        if board[k][x-k] == players[0]:
            xes.append(board[k][x-k])
        elif board[k][x-k] == players[1]:
            oes.append(board[k][x-k])
    if (((len(xes) == len(board[0])-1) and (len(oes) == 0)) or
        ((len(oes) == len(board[0])-1) and (len(xes) == 0))):
        return True
    else:
        return False

# Like "check_2nd_diag" but specific for CPU to win
def CPU_win_move_2_diag(board, players, CP, Player):
    x = len(board)-1
    P_list = []
    CP_list = []
    for i in range(len(board)):
        if board[i][x-i] == players[CP]:
            CP_list.append(board[i][x-i])
        elif board[i][x-i] == players[Player]:
            P_list.append(board[i][x-i])
    if ((len(CP_list) == len(board[0])-1) and len(P_list) == 0):
        return True
    else:
        return False

# Full checking for CPU to win in next move. (all the "or"s)
def CPU_win_move(board, players, CP, Player):
    for i in range(len(board)):
        if (CPU_win_move_row(board, players, i, CP, Player) or
            CPU_win_move_column(board, players, i, CP, Player) or
            CPU_win_move_1_diag(board, players, CP, Player) or
            CPU_win_move_2_diag(board, players, CP, Player)):
            return True
    else:
        return False

'''Checks for if either player has won yet.
   Left over from 2-Player program but useful for end-of-game
   statement.'''
def check_board(board, players):
    if (check_rows(board, players)[0] or
        check_columns(board, players)[0] or
        check_diagonals(board, players)[0]):
        return True
    else:
        return False

#######################################################################

# Button and list board move for Player
def player_move(board, turn, r, c, mark):
    if mark_board_check(board, r, c, mark):
        return r,c
    else:
        messagebox.showerror("ERROR",
        "That box has already been selected\nPick Another Box" )


#######################################################################

# Define the Win-Move functions for CPU.
'''This is to be able to randomize which checks happen in what order
   because otherwise rows and columns always get blocked by CPU before
   diagonals and that's boring to me.
   
   Each function returns if it can block, and the coordinates of that
   move. If it can't block, "False" is all that's needed to be checked,
   but for consistency for the return values, defaults of r,c = 0,0 are
   used.'''

# Checks if the CP can block the Player in a row
def CPU_row_check(board, players):
    if check_rows_CPU(board, players):
        to_move = True
        for i in range(len(board)):
            if check_1_row(board, players, i):
                r = int(i)
                for col in board[i]:
                    if col == " ":
                        c = board[i].index(" ")
    else:
        to_move = False
        r,c = 0,0
    return [to_move, r, c]

# Checks if the CP can block the Player in a column
def CPU_column_check(board, players):
    if check_columns_CPU(board, players):
        to_move = True
        for j in range(len(board)):
            if check_1_column(board, players, j):
                c = int(j)
                for i in range(len(board)):
                    if board[i][c] == " ":
                        r = i
    else:
        to_move = False
        r,c = 0,0
    return [to_move, r, c]

# Checks if the CP can block the Player in the descending diagonal
def CPU_1_diag_check(board, players):
    if check_1st_diag(board, players):
        to_move = True
        for i in range(len(board)):
            if board[i][i] == " ":
                r = i
                c = i
    else:
        to_move = False
        r,c = 0,0
    return [to_move, r, c]

# Checks if the CP can block the Player in the ascending diagonal
def CPU_2_diag_check(board, players):
    x = len(board) - 1
    if check_2nd_diag(board, players):
        to_move = True
        for m in range(len(board)):
            if board[m][x-m] == " ":
                r = m
                c = x-m
    else:
        to_move = False
        r,c = 0,0
    return [to_move, r, c]

# All CPU blocking checks together
def CPU_block_check(board, players):
    if ((check_rows_CPU(board, players)) or 
        (check_columns_CPU(board, players)) or 
        (check_1st_diag(board, players)) or 
        (check_2nd_diag(board, players))):
        return True
    else:
        return False

# Button and list board move for CPU
def CPU_move(board, rows, mark, CP, Player, players):
    # Make list to assign for CPU blocking
    blocking_list = []
    for i in range(4):
        blocking_list.append(i)
    # Assign checks to list
    blocking_list[0] = CPU_row_check(board, players)
    blocking_list[1] = CPU_column_check(board, players)
    blocking_list[2] = CPU_1_diag_check(board, players)
    blocking_list[3] = CPU_2_diag_check(board, players)
    # Shuffle the list for that randomness I meantioned
    random.shuffle(blocking_list)
    
    loop = True
    while loop:
        x = len(board) - 1
        # Can the CPU win in the next move?
        if CPU_win_move(board, players, CP, Player):
            for i in range(len(board)):
                if CPU_win_move_row(board, players, i, CP, Player):
                    r = int(i)
                    for col in board[i]:
                        if col == " ":
                            c = board[i].index(" ")
                elif CPU_win_move_column(board,
                                         players,
                                         i,
                                         CP,
                                         Player):
                    c = int(i)
                    for row in range(len(board)):
                        if board[row][c] == " ":
                            r = row
                elif CPU_win_move_1_diag(board, players, CP, Player):
                    if board[i][i] == " ":
                        r = i
                        c = i
                elif CPU_win_move_2_diag(board, players, CP, Player):
                    if board[i][x-i] == " ":
                        r = i
                        c = x-i
        # If it can't win, can the CPU block in the next move?
        elif CPU_block_check(board, players):
            for i in range(4):
                '''If it can block, use the first coordinates in the
                   shuffled list where the block return is "True".'''
                if blocking_list[i][0]:
                    r, c = blocking_list[i][1], blocking_list[i][2]
                    break
        # If CPU can't win or block, play random move.
        else:
            r = random.randint(0,rows-1)
            c = random.randint(0,rows-1)
        # Check the board to proceed to next turn.
        # Loop through until CPU successfully makes a move
        if mark_board_check(board, r, c, mark):
            mark_board(board, r, c, mark)
            '''Exit loop if marked (technically, I don't need 
               "loop = False", but it's for my peace of mind).'''
            loop = False
            return r,c

#######################################################################

# Checks the board to see if either player has won and how they won.
# Returns True if game is over, False if ongoing
def where_winner(turn, board_positions, board, players):
    x = len(board)
    if check_board(board, players):
        disable_all_buttons()
        if check_rows(board, players)[0]:
            for i in range(1,4):
                # Long string to execute
                exec_str = (f'red_box(button'
                            f'{check_rows(board, players)[1]}{i})')
                exec(exec_str, locals(), globals())
            
            # Long string for message
            msg_str = (f"Player {players[(turn)%2]} is the winner in "
                       f"Row {check_rows(board, players)[1]}\t")
            messagebox.showinfo("Winner!", msg_str)
            return True
        
        elif check_columns(board, players)[0]:
            for i in range(1,4):
                # Long string to execute
                exec_str = (f'red_box(button{i}'
                            f'{check_columns(board, players)[1]})')
                exec(exec_str, locals(), globals())
            
            # Long string for message
            msg_str = (f"Player {players[(turn)%2]} is the winner in "
                       f"Column {check_columns(board, players)[1]}\t")
            messagebox.showinfo("Winner!", msg_str)
            return True
        
        elif check_diagonals(board, players)[0]:
            # Check if descending diagonal
            if check_diagonals(board, players)[1] == 1:
                for i in range(1,4):
                    exec(f'red_box(button{i}{i})', locals(), globals())
                
                # Long string for message
                msg_str = (f"Player {players[(turn)%2]} is the winner "
                           f"in\t\nthe Descending Diagonal")
                messagebox.showinfo("Winner!", msg_str)
            
            # Check if ascending diagonal
            elif check_diagonals(board, players)[1] == 2:
                for i in range(1,4):
                    # Long(ish) string to execute
                    exec_str = f'red_box(button{x-i+1}{i})'
                    exec(exec_str, locals(), globals())
                
                # Long string for message
                msg_str = (f"Player {players[(turn)%2]} is the winner "
                           f"in\t\nthe Ascending Diagonal")
                messagebox.showinfo("Winner!", msg_str)
            return True
    # Check for draw
    elif turn > board_positions:
        disable_all_buttons()
        messagebox.showinfo("Tied Up Loose Ends",
                            "The game was a draw\t")
        return True
    else:
        return False

'''Function for player going first.
   Does both player's and CPU's turns at once to get called at once
   for the player's click.'''
def Player_first(board, r, c, button):
    global turn
    # Mark depending on whose turn it is
    if (turn+1)%2 == 0:
        mark_button = X
    else:
        mark_button = O
    # Make/update the board
    board = make_board(button_names)
    # Check if the game is over
    game_over = where_winner(turn, board_positions, board, players)
    
    if (not game_over) and (turn <= board_positions):
        # If already marked, give the error and try again
        try:
            r,c = player_move(board, turn, r, c, mark_button)
            button['text'] = mark_button
            mark_board(board, r, c, mark_button)
            turn += 1
        except:
            return None
    else:
        return None
    
    # CPU Turn inside of button click
    if (turn+1)%2 == 0:
        mark_button = X
    else:
        mark_button = O
    # Check if the game is over
    game_over = where_winner(turn, board_positions, board, players)
    if (not game_over) and (turn < board_positions):
        r,c = CPU_move(board, rows, mark_button, CP, Player, players)
        if (turn+1)%2 == 0:
            mark_button_ = X
        else:
            mark_button_ = O
        
        # Long(ish) string to execute
        exec_str = f'button{r+1}{c+1}["text"] = mark_button_'
        #Mark the button given the coordinates and button ID
        exec(exec_str, locals(), globals())
        mark_board(board, r, c, mark_button)
        turn += 1
        # Again, check if the game is over
        game_over = where_winner(turn, board_positions, board, players)
    else:
        return None

'''Function for CPU going first.
   Does both player's and CPU's turns at once to get called at once
   for player's click.'''
def CPU_first(board, r, c, button):
    global turn
    # Save values for Player's click
    r_, c_ = r, c
    '''First turn was done in "reset" function (with random
       coordinates), so next is Player's turn.
       Basically the same as "Player_first" function'''
    if (turn+1)%2 == 0:
        mark_button_ = X
    else:
        mark_button_ = O
    # Update the board
    board = make_board(button_names)
    # Check if the game is over
    game_over = where_winner(turn, board_positions, board, players)
    if (not game_over) and (turn < board_positions):
        # If already marked, give the error and try again
        try:
            r,c = player_move(board, turn, r_, c_, mark_button_)
            button['text'] = mark_button_
            mark_board(board, r, c, mark_button_)
            turn += 1
        except:
            return None
    else:
        return None
    
    # CP's turn
    if (turn+1)%2 == 0:
        mark_button = X
    else:
        mark_button = O
    # Check if the game is over
    game_over = where_winner(turn, board_positions, board, players)
    # Last part of conditional there for peace of mind
    if ((not game_over) and
        (turn <= board_positions) and
        ((turn+1)%2 == 0)):
        r,c = CPU_move(board, rows, mark_button, CP, Player, players)
        if (turn+1)%2 == 0:
            mark_button = X
        else:
            mark_button = O
        
        # Long(ish) string to execute
        exec_str = f'button{r+1}{c+1}["text"] = mark_button'
        # Mark the button given the coordinates and button ID
        exec(exec_str, locals(), globals())
        mark_board(board, r, c, mark_button)
        turn += 1
        one_click_CPU = 1
    else:
        return None
    # One last check for Game Over in case of a draw
    game_over = where_winner(turn, board_positions, board, players)


#######################################################################


# Disable Buttons after finished game
def disable_all_buttons():
    for i in range(1,4):
        for j in range(1,4):
            # Long string to execute
            exec_str = (f'button{i}{j}.config(state="disabled",'
                        f'bg="#50509f")')
            exec(exec_str, locals(), globals())

# Turn one button at a time red
def red_box(button):
    button['bg'] = '#900000'

# Clicked Button Function
def b_click(b):
    global clicked, turn, X, O, mark_button
    # Get clicked button coordinates
    for i in range(1,4):
        for j in range(1,4):
            if str(b.cget('command')) == str(command_names[i-1][j-1]):
                r = i-1
                c = j-1
    # Make/update the board
    board = make_board(button_names)
    
    '''If the player clicked to go first, use "Player_first" function,
       otherwise, use "CPU_first" function.'''
    if clicked:
        Player_first(board, r, c, b)
    else:
        CPU_first(board, r, c, b)
    
# Start the game over
def reset():
    # Make the buttons global
    for i in range(1,4):
        for j in range(1,4):
            exec(f'global button{i}{j}', locals(), globals())
    global clicked, turn, X, O, CP, Player
    
    # "Yes" means the player goes first, "No" means the CP goes first
    clicked = messagebox.askyesno("Tic Tac Toe",
                                  "Player to go first?\t")
    # See beginning of this program for explanations of the variables
    turn = 1
    X = 'X'
    O = 'O'
    # Make the full User Interface with this function
    make_GUI_et_al()
    if clicked:
        CP = 1
        Player = 0
        mark_button = X
    else:
        '''If CP is first, an empty board needs to be created and a
           random move be completed.'''
        CP = 0
        Player = 1
        mark_button = O
        board = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
        r = random.randint(0,rows-1)
        c = random.randint(0,rows-1)
        # Mark the button given the random coordinates and button ID
        exec(f'button{r+1}{c+1}["text"] = X', locals(), globals())
        mark_board(board, r, c, X)
        turn +=1

# Make the window, frames, and buttons
def make_GUI_et_al():
    global frame_names
    global button_names
    global command_names
    
    # Lists of things to allow easy "exec" "for" loops
    
    # List to make button frames and place them in the grid
    frame_names = []
    # List to make buttons and call them to change the text to a marker
    button_names = []
    # List to identify where the player clicked given the command name
    command_names = []
    
    # Make it all
    for i in range(1,4):
        # Makes each row its own list in the list of objects
        frame_names.append([])
        button_names.append([])
        command_names.append([])
        for j in range(1,4):
            exec(f'global frame{i}{j}', locals(), globals())
            exec(f'global button{i}{j}', locals(), globals())
            exec(f'frame_names[{i-1}].append("frame{i}{j}")',
                 locals(),
                 globals())
            # Append "cget" to make getting the button's text easier
            # Long string to execute
            exec_str = (f'button_names[{i-1}].append(str("button{i}'
                        f'{j}.cget(\'text\')"))')
            exec(exec_str, locals(), globals())
            
            # Make square buttons
            size = 150
            exec_str = (f'frame{i}{j} = tk.Frame(frame, width={size},'
                        f'height={size},)')
            exec(exec_str, locals(), globals())
            #exec(f'button{i}{j} = tk.Button(frame{i}{j}, text=" ", bg="#000000", fg="#ffffff", command=lambda: b_click(button{i}{j}),)', locals(), globals())
            global b_click_lambda
            ''' "b_click_lambda" function is a workaround for 
               "lambda: fn()" not working in "exec" function commented
               out 2 lines above this. I'm leaving the line in as a
               reminder and guide.'''
            def b_click_lambda():
                d = globals()
                # Buttons to be clicked
                exec_str = (f'button{i}{j} = tk.Button(frame{i}{j},'
                            f'text=" ", font=("lucida", 48),'
                            f'bg="#000040", fg="#9f9f9f",'
                            f'command=lambda: b_click(button{i}{j}),)')
                exec(exec_str, d)
                return d[f'button{i}{j}']
            # Implement workaround for "lambda"
            bcl = b_click_lambda()
            bcl
            
            '''Get command names to compare to easily mark the board
               in "b_click" function.'''
            exec_str = (f'command_names[{i-1}].append(str(button{i}{j}'
                        f'.cget("command")))')
            exec(exec_str, locals(), globals())
            
            # Configure the frames to be square
            exec(f'frame{i}{j}.grid_propagate(False)',
                 locals(),
                 globals())
            exec(f'frame{i}{j}.columnconfigure(0, weight=1)',
                 locals(),
                 globals())
            exec(f'frame{i}{j}.rowconfigure(0, weight=1)',
                 locals(),
                 globals())
            
            # Set each frame in the proper grid formation
            exec(f'frame{i}{j}.grid(row={i}, column={j})',
                 locals(),
                 globals())
            exec(f'button{i}{j}.grid(sticky="wens")',
                 locals(),
                 globals())


# Create Frame for Buttons (width=height => square Button)
# and Buttons named for positions on board
frame = tk.Frame(root)
frame.grid(row=1, column = 0)

# Create and place Reset Button above game board
reset_button = tk.Button(root,
                         text="Reset Game",
                         font=('arial',12),
                         command=reset,)
reset_button.grid(row=0, column=0)
reset_button.grid(sticky='w')

# Runs to open GUI and also resets board after clicking "Reset Game"
reset()

# Loop the window
root.mainloop()
