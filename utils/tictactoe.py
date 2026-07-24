"""
utils/tictactoe.py
--------------------
منطق بازی دوز (Tic-Tac-Toe) بین کاربر (X) و ربات (O).
حالت بازی فقط در حافظه نگه داشته می‌شود (نیازی به ذخیره دائمی نیست).
ربات از الگوریتم Minimax استفاده می‌کند، یعنی هرگز نمی‌بازد.
"""

_games: dict[str, list[str]] = {}

WIN_LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6),
]


def _key(chat_id: int, user_id: int) -> str:
    return f"{chat_id}:{user_id}"


def start_game(chat_id: int, user_id: int) -> list[str]:
    board = [" "] * 9
    _games[_key(chat_id, user_id)] = board
    return board


def get_board(chat_id: int, user_id: int) -> list[str] | None:
    return _games.get(_key(chat_id, user_id))


def end_game(chat_id: int, user_id: int) -> None:
    _games.pop(_key(chat_id, user_id), None)


def check_winner(board: list[str]) -> str | None:
    """برمی‌گرداند 'X'، 'O'، 'draw' یا None (بازی هنوز ادامه دارد)."""
    for a, b, c in WIN_LINES:
        if board[a] != " " and board[a] == board[b] == board[c]:
            return board[a]
    if " " not in board:
        return "draw"
    return None


def _minimax(board: list[str], is_bot_turn: bool) -> int:
    winner = check_winner(board)
    if winner == "O":
        return 1
    if winner == "X":
        return -1
    if winner == "draw":
        return 0

    if is_bot_turn:
        best = -2
        for i in range(9):
            if board[i] == " ":
                board[i] = "O"
                best = max(best, _minimax(board, False))
                board[i] = " "
        return best
    else:
        best = 2
        for i in range(9):
            if board[i] == " ":
                board[i] = "X"
                best = min(best, _minimax(board, True))
                board[i] = " "
        return best


def bot_move(board: list[str]) -> int | None:
    """بهترین حرکت ممکن برای ربات (O) را انتخاب و اعمال می‌کند."""
    best_score = -2
    best_index = None
    for i in range(9):
        if board[i] == " ":
            board[i] = "O"
            score = _minimax(board, False)
            board[i] = " "
            if score > best_score:
                best_score = score
                best_index = i
    if best_index is not None:
        board[best_index] = "O"
    return best_index


def apply_user_move(chat_id: int, user_id: int, index: int) -> list[str] | None:
    """حرکت کاربر (X) را اعمال می‌کند؛ اگر خانه پر بود یا بازی وجود نداشت None برمی‌گرداند."""
    board = get_board(chat_id, user_id)
    if board is None or board[index] != " ":
        return None
    board[index] = "X"
    return board