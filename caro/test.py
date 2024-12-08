import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller
from selenium.webdriver.chrome.options import Options
# Tự động cài đặt Chrome driver
chromedriver_autoinstaller.install()

# Khởi tạo trình duyệt (Chrome)
@pytest.fixture
def driver():
    # Tạo ChromeOptions
    chrome_options = Options()
    chrome_options.add_argument("--mute-audio")  # Tắt âm thanh trong trình duyệt
    
    driver = webdriver.Chrome(options=chrome_options)

    driver.get("https://playtictactoe.org/")

    yield driver
    driver.quit()

# =======================
# Thuật toán Minimax
# =======================

def check_winner(board):
    """Kiểm tra trạng thái chiến thắng."""
    win_patterns = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Hàng ngang
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Hàng dọc
        [0, 4, 8], [2, 4, 6]              # Đường chéo
    ]
    for pattern in win_patterns:
        if board[pattern[0]] == board[pattern[1]] == board[pattern[2]] != "":
            return board[pattern[0]]  # "X" hoặc "O"
    return None

def is_draw(board):
    """Kiểm tra trận hòa."""
    return all(cell != "" for cell in board) and check_winner(board) is None

def minimax(board, depth, is_maximizing):
    """Thuật toán Minimax."""
    winner = check_winner(board)
    if winner == "X":  # Người chơi thắng
        return 10 - depth
    if winner == "O":  # Máy thắng
        return depth - 10
    if is_draw(board):  # Trận hòa
        return 0

    if is_maximizing:
        best_score = -float("inf")
        for i in range(9):
            if board[i] == "":
                board[i] = "X"
                score = minimax(board, depth + 1, False)
                board[i] = ""
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = float("inf")
        for i in range(9):
            if board[i] == "":
                board[i] = "O"
                score = minimax(board, depth + 1, True)
                board[i] = ""
                best_score = min(score, best_score)
        return best_score

def find_best_move(board):
    """Tìm nước đi tốt nhất."""
    best_score = -float("inf")
    best_move = None
    for i in range(9):
        if board[i] == "":
            board[i] = "X"  # Giả sử người chơi là "X"
            score = minimax(board, 0, False)
            board[i] = ""
            if score > best_score:
                best_score = score
                best_move = i
    return best_move

# =======================
# Tương tác với Giao diện Web
# =======================
def make_move(driver, move_index):
    """Thực hiện nước đi trên giao diện."""
    squares = driver.find_elements(By.CLASS_NAME, "square")
    squares[move_index].click()

def play_game_until_result(driver):
    while True:
        # Kiểm tra trạng thái bàn cờ sau mỗi lượt đi
        squares = driver.find_elements(By.CLASS_NAME, "square")
        board = []
        for square in squares:
            inner = square.find_element(By.TAG_NAME, "div").get_attribute("class")
            if inner == "x":
                board.append("X")
            elif inner == "o":
                board.append("O")
            else:
                board.append("")

        # Kiểm tra kết quả
        winner = check_winner(board)
        if winner:
            return winner
        if is_draw(board):
            return "Tie"

        # Tìm nước đi tốt nhất và thực hiện
        best_move = find_best_move(board)
        if best_move is not None:
            make_move(driver, best_move)
        time.sleep(1)


def reset_game(driver):
    """Khởi động lại trò chơi bằng cách nhấn vào nút restart."""
    driver.refresh()
    time.sleep(3)  # Đảm bảo có thời gian để game được reset

# =======================
# Các Test Case
# =======================

def test_win_x(driver):
    """Test người chơi (X) thắng"""
    make_move(driver, 0)  # Người chơi đánh vào ô 1
    time.sleep(1)
    result = play_game_until_result(driver)
    if result == "Tie":
        reset_game(driver)
    else:
        assert result == "X", f"Expected 'X' to win, but got {result}"

# def test_multiple_draws(driver):
#     """Test chạy 10 lần và kiểm tra xem có trận hòa nào không."""
#     for i in range(10):
#         print(f"Running game {i + 1}")
#         reset_game(driver)  # Đảm bảo rằng mỗi lần test sẽ bắt đầu một game mới
#         result = play_game_until_result(driver)
#         if result == "Tie":
#             reset_game(driver)
#         else:
#             assert result == "X", f"Expected 'X' to win, but got {result}"


def test_lose_to_bot(driver):
    """Test người chơi (X) thua bot (O)."""
    # Người chơi (X) đi vào những ô không hợp lý (để bot dễ dàng thắng).
    make_move(driver, 0)  # Người chơi đánh vào ô 1
    time.sleep(1)
    make_move(driver, 2)  # Người chơi đánh vào ô 3
    time.sleep(1)

    # Bot (O) sẽ đi tối ưu và chọn ô 5 để chiếm trung tâm, giúp bot dễ dàng thắng.
    make_move(driver, 4)  # Người chơi đánh vào ô 5
    time.sleep(1)
    
    # Bot tiếp tục chơi tối ưu và đánh vào ô 1 (chặn người chơi và tạo cơ hội thắng).
    make_move(driver, 3)  # Người chơi đánh vào ô 4
    time.sleep(1)

    # Kiểm tra kết quả: Bot (O) sẽ thắng
    result = play_game_until_result(driver)
    
    # Kiểm tra nếu bot (O) thắng
    assert result == "O", f"Expected 'O' (Bot) to win, but got {result}"

def test_draw(driver):
    """Test trường hợp hòa giữa người chơi (X) và bot (O) tự động đánh."""
    
    # Người chơi (X) thực hiện các nước đi mà không tạo cơ hội thắng
    make_move(driver, 0)  # Người chơi đánh vào ô 1
    time.sleep(1)
    make_move(driver, 2)  # Người chơi đánh vào ô 3
    time.sleep(1)
    make_move(driver, 4)  # Người chơi đánh vào ô 5
    time.sleep(1)
    make_move(driver, 6)  # Người chơi đánh vào ô 7
    time.sleep(1)
    make_move(driver, 8)  # Người chơi đánh vào ô 9
    time.sleep(1)

    # Sau khi người chơi đi, bot (O) sẽ tự động đánh
    result = play_game_until_result(driver)  # Bot tự động chơi theo thuật toán Minimax

    # Kiểm tra kết quả: Trận đấu sẽ hòa (Không có người thắng)
    assert result == "Tie", f"Expected 'Tie', but got {result}"
