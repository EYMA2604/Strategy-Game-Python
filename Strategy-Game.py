##GAME SETUP##
def get_game_setup():
    #gest number of rows and cols and checks validity.
    try:
        rows = int(input("Enter number of rows"))
        print()
        cols = int(input("Enter number of columns"))
        print()
        print()
        if rows < 2 or rows > 100 or cols < 2 or cols > 100:
            print("Invalid size. No game for you! Next!")
            return None, None, None
        if rows == 2 or cols == 2:
            n_to_win = 2
        elif rows == 3 or cols == 3:
            rows, cols, n_to_win = 3, 3, 3
        elif 4 <= rows <= 5 or 4 <= cols <= 5:
            n_to_win = 3
        elif 6 <= rows <= 10 or 6 <= cols <= 10:
            n_to_win = 4
        else:
            n_to_win = 5

        return rows, cols, n_to_win

    except ValueError:
        print("Invalid input. Enter a number.")
        return None, None, None
def create_board(rows, cols):
    return [['.' for _ in range(cols)] for _ in range(rows)]
def print_board(board, is_tic_tac_toe):
    for row in board:
        print("|" + "|".join(row) + "|")
    #for CONNECT-N prints cols numbers
    if not is_tic_tac_toe:
        cols = len(board[0])
        column_numbers = " " + " ".join(str(i) for i in range(1, cols + 1))
        print(column_numbers)
def get_coords_from_cell(cell_num):
    row = (cell_num - 1) // 3
    col = (cell_num - 1) % 3
    return row, col
def get_player_types(is_tic_tac_toe):
    if is_tic_tac_toe:
        return 'h', 'h'
    players = []
    for i in [1, 2]:
        while True:
            choice = input(f"Choose type for player {i}: h - human, r - random/simple computer,"
                           f" s - strategic computer: ").lower()
            if choice in ['h', 's']: # checks if player type is legal
                players.append(choice)
                break
            else:
                print("Invalid selection. Enter h or s.")
    return players[0], players[1]
##BORAD SCANS & CHECKS##
def check_sequence(board, r, c, dr, dc, n, char):
    #dc and rc = cols / rows direction
    rows = len(board)
    cols = len(board[0])
    #run over n relevant cols/rows
    for i in range(n):
        curr_r = r + i * dr
        curr_c = c + i * dc

        if not (0 <= curr_r < rows and 0 <= curr_c < cols):
            return False
        # checks for a match
        if board[curr_r][curr_c] != char:
            return False

    return True
def check_win(board, n, char):
    rows = len(board)
    cols = len(board[0])
    #checks every cell if the token's similar.
    for r in range(rows):
        for c in range(cols):
            # if the token recognized - start looking for a win from there
            if board[r][c] == char:
                # checks vertical (1,0) horizontal (0,1) and diagonals (1,1) & (1,-1)
                directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
                for dr, dc in directions:
                    if check_sequence(board, r, c, dr, dc, n, char):
                        return True
    return False
def is_board_full(board):
    # checks if there is at least one '.' in the board
    for row in board:
        if '.' in row:
            return False
    return True
##COMPUTER STRATEGIC  & MOVES##
def get_priority_columns(cols):
    # creates a priority list
    center = (cols - 1) // 2
    columns = list(range(cols))
    columns.sort(key=lambda x: (abs(x - center), x))
    return columns
def can_win(board, col, n_to_win, char):
    rows = len(board)
   #looks for the row in which the token will land
    target_row = -1
    for r in range(rows - 1, -1, -1):
        if board[r][col] == '.':
            target_row = r
            break

    if target_row == -1:
        return False
    #if a move was found - do it and see what's happening
    board[target_row][col] = char
    is_victory = check_win(board, n_to_win, char)
    board[target_row][col] = '.'
    return is_victory
def get_move(board, player_type, n_to_win, my_char, opp_char):
    cols = len(board[0])
    priority_cols = get_priority_columns(cols)

    # Priority 1: win
    for col in priority_cols:
        if can_win(board, col, n_to_win, my_char):
            print(f"Computer chose column {col + 1}")
            return col

    # Priority 2: avoid losing
    for col in priority_cols:
        if can_win(board, col, n_to_win, opp_char):
            print(f"Computer chose column {col + 1}")
            return col

    # Priority 3: make a sequence
    if n_to_win > 3:
        for col in priority_cols:
            if can_win(board, col, 3, my_char):
                print(f"Computer chose column {col + 1}")
                return col

        # Priority 4: stop other player's sequence
        for col in priority_cols:
            if can_win(board, col, 3, opp_char):
                print(f"Computer chose column {col + 1}")
                return col

    # Priority 5 (default): follow the priority strategic
    for col in priority_cols:
        if board[0][col] == '.':
            print(f"Computer chose column {col + 1}")
            return col
def get_human_move(board, is_ttt):
    rows = len(board)
    cols = len(board[0])

    while True:
        try:
            #gets the choice of the player and handles invalid inputs
            if is_ttt:
                prompt = "Enter position (1-9): "
            else:
                prompt = f"Enter column (1-{cols}): "

            user_input = input(prompt)
            print()
            move = int(user_input)

            if is_ttt:
                if 1 <= move <= 9:
                    r, c = (move-1)//3, (move-1)%3
                    if board[r][c] == '.': return move
                    print("Cell already taken.")
                else:
                    print("Invalid cell. Choose between 1 and 9.")
            else:
                if 1 <= move <= cols:
                    if board[0][move-1] != '.':
                        print(f"Column {move} is full. Choose another one.")
                    else:
                        return move - 1
                else:
                    print(f"Invalid column. Choose between 1 and {cols}.")

        except ValueError:
            print("Invalid input. Enter a number.")
def make_move(board, move, char, is_ttt):
    if is_ttt:
        r, c = get_coords_from_cell(move)
        board[r][c] = char
    else:
        for r in range(len(board) - 1, -1, -1):
            if board[r][move] == '.':
                board[r][move] = char
                break
##MAIN##
def main():
    #sets up the game
    rows, cols, n_to_win = get_game_setup()
    if rows is None:
        return

        # is the game Tic-Tac-Toe or not
    is_ttt = (n_to_win == 3 and rows == 3 and cols == 3)
    game_name = "Tic-Tac-Toe" if is_ttt else f"Connect Four - Or More [Or Less]"

    if is_ttt:
        print("Tic Tac Toe (Human vs Human)")
    else:
        print(f'Connect Four - Or More [Or Less] ({rows} rows x {cols} cols, connect {n_to_win})')

    # choosing player types
    p1_type, p2_type = get_player_types(is_ttt)
    print()

    player_types = {1: p1_type, 2: p2_type}
    symbols = {1: 'X', 2: 'O'}

    #creates and prints the board
    board = create_board(rows, cols)
    print_board(board, is_ttt)

    current_player = 1
    while True:
        char = symbols[current_player]
        opp_char = 'O' if char == 'X' else 'X'
        p_type = player_types[current_player]

        if not is_ttt:
            print(f"Player {current_player} ({char}) turn.")

        #gets the move based on the player type
        if p_type == 'h':
            move = get_human_move(board, is_ttt)
        else:
            move = get_move(board, 's', n_to_win, char, opp_char)

        # makes the move and prints the updated board
        make_move(board, move, char, is_ttt)
        print_board(board, is_ttt)

        # checks for a victory
        if check_win(board, n_to_win, char):
            print(f"Player {current_player} ({char}) wins!")
            break

        # checks for a tie
        if is_board_full(board):
            print("Board full and no winner. It's a tie!")
            break

        # switch players
        current_player = 2 if current_player == 1 else 1

if __name__ == "__main__":

    main()
