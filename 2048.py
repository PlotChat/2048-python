import pygame, random, os

pygame.init()

# Khởi tạo màn hình + biến cần thiết:
WIDTH = 400
HEIGHT = 500
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("2048")
timer = pygame.time.Clock()
fps = 60
font = pygame.font.Font("freesansbold.ttf", 24)
font0 = pygame.font.Font("freesansbold.ttf", 33)

# Màu game 2048 (dict):
colors = {
    0: (204, 192, 179),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46),
    "light text": (249, 246, 242),
    "dark text": (119, 110, 101),
    "other": (0, 0, 0),
    "bg": (187, 173, 160),
}


def create_menu():
    # Caption + screen color:
    pygame.display.set_caption("2048 Menu")
    screen.fill(colors["bg"])

    # Render boxes:
    pygame.draw.rect(screen, colors[16], [178, 50, 160, 100], 0, 10)  # "2048" box
    pygame.draw.rect(screen, colors[2048], [67, 50, 100, 100], 0, 5)  # "Game!" box

    pygame.draw.rect(screen, colors[0], [67, 180, 271, 70], 0, 5)  # Start box
    pygame.draw.rect(screen, colors[0], [67, 275, 271, 70], 0, 5)  # Info box
    pygame.draw.rect(screen, colors[0], [67, 370, 271, 70], 0, 5)  # Quit box

    # Create texts:
    name_text = font0.render("2048", True, "white")
    name_text0 = font0.render("Game!", True, "white")
    start_text = font0.render("Start", True, colors["dark text"])
    info_text = font0.render("Info", True, colors["dark text"])
    quit_text = font0.render("Quit", True, colors["dark text"])

    # Render texts on screen:
    screen.blit(name_text, (78, 83))
    screen.blit(name_text0, (203, 83))
    screen.blit(start_text, (155, 198))
    screen.blit(info_text, (161, 293))
    screen.blit(quit_text, (156, 388))


def create_info():
    global pos
    screen.fill(colors["bg"])
    img = pygame.image.load("cachchoi.png").convert()
    screen.blit(img, (0, 0))
    create_back()


def create_back():
    global pos

    pygame.draw.rect(screen, colors[8], [0, 199, 792, 10], 0, 10) # Line

    pygame.draw.rect(screen, colors[0], [260, 273, 271, 70], 0, 10) # Start box
    pygame.draw.rect(screen, colors[0], [260, 368, 271, 70], 0, 10) # Back box

    back_text = font0.render("Back", True, colors["dark text"])
    start_text = font0.render("Start", True, colors["dark text"])

    screen.blit(back_text, (353, 385))
    screen.blit(start_text, (353, 290))


# Biến cần thiết:
board_values = [[0 for _ in range(4)] for _ in range(4)]
game_over = False
spawn_new = True
init_count = 0
direction = ""
score = 0
file = open("high_score", "r")
file.write("0")
init_high = file.readline()
init_high.split()
print(init_high)
file.close()
high_score = init_high

# Vẽ màn hình thua:
def draw_over():
    pygame.draw.rect(screen, "black", [50, 50, 300, 100], 0, 10)
    game_over_text1 = font.render("Game Over!", True, "white")
    game_over_text2 = font.render("Press Enter to Restart", True, "white")
    screen.blit(game_over_text1, (130, 65))
    screen.blit(game_over_text2, (70, 105))


# Di chuyển các khối chữ:
def take_turn(direc, board):
    global score
    merged = [[False for _ in range(4)] for _ in range(4)]
    if direc == 'UP':
        for i in range(4):
            for j in range(4):
                shift = 0
                if i > 0:
                    for q in range(i):
                        if board[q][j] == 0:
                            shift += 1
                    if shift > 0:
                        board[i - shift][j] = board[i][j]
                        board[i][j] = 0
                    if board[i - shift - 1][j] == board[i - shift][j] and not merged[i - shift][j] \
                            and not merged[i - shift - 1][j]:
                        board[i - shift - 1][j] *= 2
                        score += board[i - shift - 1][j]
                        board[i - shift][j] = 0
                        merged[i - shift - 1][j] = True

    elif direc == "DOWN":
        for i in range(3):
            for j in range(4):
                shift = 0
                for q in range(i + 1):
                    if board[3 - q][j] == 0:
                        shift += 1
                if shift > 0:
                    board[2 - i + shift][j] = board[2 - i][j]
                    board[2 - i][j] = 0
                if 3 - i + shift <= 3:
                    if (
                        board[2 - i + shift][j] == board[3 - i + shift][j]
                        and not merged[3 - i + shift][j]
                        and not merged[2 - i + shift][j]
                    ):
                        board[3 - i + shift][j] *= 2
                        score += board[3 - i + shift][j]
                        board[2 - i + shift][j] = 0
                        merged[3 - i + shift][j] = True

    elif direc == "LEFT":
        for i in range(4):
            for j in range(4):
                shift = 0
                for q in range(j):
                    if board[i][q] == 0:
                        shift += 1
                if shift > 0:
                    board[i][j - shift] = board[i][j]
                    board[i][j] = 0
                if (
                    board[i][j - shift] == board[i][j - shift - 1]
                    and not merged[i][j - shift - 1]
                    and not merged[i][j - shift]
                ):
                    board[i][j - shift - 1] *= 2
                    score += board[i][j - shift - 1]
                    board[i][j - shift] = 0
                    merged[i][j - shift - 1] = True

    elif direc == "RIGHT":
        for i in range(4):
            for j in range(4):
                shift = 0
                for q in range(j):
                    if board[i][3 - q] == 0:
                        shift += 1
                if shift > 0:
                    board[i][3 - j + shift] = board[i][3 - j]
                    board[i][3 - j] = 0
                if 4 - j + shift <= 3:
                    if (
                        board[i][4 - j + shift] == board[i][3 - j + shift]
                        and not merged[i][4 - j + shift]
                        and not merged[i][3 - j + shift]
                    ):
                        board[i][4 - j + shift] *= 2
                        score += board[i][4 - j + shift]
                        board[i][3 - j + shift] = 0
                        merged[i][4 - j + shift] = True
    return board


# Tạo các khối ngẫu nhiên mỗi lượt chơi:
def new_pieces(board):
    count = 0
    full = False
    while any(0 in row for row in board) and count < 1:
        row = random.randint(0, 3)
        col = random.randint(0, 3)
        if board[row][col] == 0:
            count += 1
            if random.randint(1, 10) == 10:
                board[row][col] = 4
            else:
                board[row][col] = 2
    if count < 1:
        full = True
    return board, full


# Vẽ nền cho lưới
def draw_board():
    pygame.draw.rect(screen, colors["bg"], [0, 0, 400, 400], 0, 10)
    score_text = font.render(f"Score: {score}", True, "black")
    high_score_text = font.render(f"High Score: {high_score}", True, "black")
    screen.blit(score_text, (10, 410))
    screen.blit(high_score_text, (10, 450))


# Vẽ lưới và quyết định màu sắc của từng ô, chữ
def draw_pieces(board):
    for i in range(4):
        for j in range(4):
            value = board[i][j]
            if value > 8:
                value_color = colors["light text"]
            else:
                value_color = colors["dark text"]
            if value <= 2048:
                color = colors[value]
            else:
                color = colors["other"]
            pygame.draw.rect(screen, color, [j * 95 + 20, i * 95 + 20, 75, 75], 0, 5)
            if value > 0:
                value_len = len(str(value))
                font = pygame.font.Font("freesansbold.ttf", 48 - (5 * value_len))
                value_text = font.render(str(value), True, value_color)
                text_rect = value_text.get_rect(center=(j * 95 + 57, i * 95 + 57))
                screen.blit(value_text, text_rect)
                pygame.draw.rect(
                    screen, "black", [j * 95 + 20, i * 95 + 20, 75, 75], 2, 5
                )


# Vòng lặp while:
run = True
play = False
menu = True
can_press = True
while run:
    if play == False:
        if menu == True:
            create_menu() # Render menu
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False # Sản phẩm ngừng chạy
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if 67 <= pos[0] <= 338 and 180 <= pos[1] <= 250 and can_press: # Start button
                    if event.button == 1: 
                        play = True # Bắt đầu trò chơi, đóng vòng lặp điều kiện play == False
                elif 67 <= pos[0] <= 338 and 275 <= pos[1] <= 345 and can_press: # info button
                    if event.button == 1:
                        menu = False # Đóng menu
                        can_press = False # Tắt chức năng bấm được các nút start, info, quit
                        screen = pygame.display.set_mode([792, HEIGHT]) # Chỉnh cửa sổ to lên
                        create_info() # Render info
                elif menu == False and can_press == False: # Các buton trong info
                    if 260 <= pos[0] <= 531 and 271 <= pos[1] <= 341:
                        if event.button == 1:
                            play = True
                            screen = pygame.display.set_mode([WIDTH, HEIGHT]) # Chỉnh cửa sổ nhỏ đi
                    if 260 <= pos[0] <= 531 and 368 <= pos[1] <= 438:
                        if event.button == 1:
                            menu = True # Mở menu
                            can_press = True # Bật chức năng bấm được các nút start, info, quit
                            screen = pygame.display.set_mode([WIDTH, HEIGHT]) # Chỉnh cửa sổ nhỏ đi
                elif 67 <= pos[0] <= 338 and 370 <= pos[1] <= 440 and can_press:
                    if event.button == 1:
                        run = False # Sản phẩm ngừng chạy

    if play == True:
        timer.tick(fps)
        screen.fill("gray")
        draw_board()
        draw_pieces(board_values)
        if spawn_new or init_count < 2:
            board_values, game_over = new_pieces(board_values)
            spawn_new = False
            init_count += 1
        if direction != "":
            board_values = take_turn(direction, board_values)
            direction = ""
            spawn_new = True
        if game_over:
            draw_over()
            if high_score > init_high:
                file = open("high_score", "w")
                file.write(f"{high_score}")
                file.close()
                init_high = high_score

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    direction = "UP"
                elif event.key == pygame.K_DOWN:
                    direction = "DOWN"
                elif event.key == pygame.K_LEFT:
                    direction = "LEFT"
                elif event.key == pygame.K_RIGHT:
                    direction = "RIGHT"

                if game_over:
                    if event.key == pygame.K_RETURN:
                        board_values = [[0 for _ in range(4)] for _ in range(4)]
                        spawn_new = True
                        init_count = 0
                        score = 0
                        direction = ""
                        game_over = False

        if score > high_score:
            high_score = score

    pygame.display.update()
pygame.quit()
quit()
