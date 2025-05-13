import tkinter
import tkinter.messagebox as messagebox
import random

ROWS = 25
COLS = 25
TILE_SIZE = 25

WINDOW_WIDTH = TILE_SIZE * ROWS
WINDOW_HEIGHT = TILE_SIZE * COLS

class Tile:
    def __init__(self, x, y, color="lime green"):
        self.x = x
        self.y = y
        self.color = color

# Game window
window = tkinter.Tk()
window.title("Snake")
window.resizable(False, False)

canvas = tkinter.Canvas(window, bg="black", width=WINDOW_WIDTH, height=WINDOW_HEIGHT, borderwidth=0, highlightthickness=0)
canvas.pack()
window.update()

# Center the window
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

window_x = int((screen_width / 2) - (window_width / 2))
window_y = int((screen_height / 2) - (window_height / 2))
window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

# Initialize game
snake = Tile(5 * TILE_SIZE, 5 * TILE_SIZE, "lime green")  # Start with lime green
food = Tile(10 * TILE_SIZE, 10 * TILE_SIZE)
snake_body = []
velocityX = 0
velocityY = 0
game_over = False
score = 0

# Multiple food colors
food_colors = ["red", "yellow", "orange", "cyan", "magenta", "white", "pink"]
current_food_color = random.choice(food_colors)

# Snake color (global variable)
snake_color = "lime green"  # Initial snake color (green)


def change_direction(e):
    global velocityX, velocityY, game_over
    if game_over:
        if e.keysym == "space":
            restart_game()
        return

    if e.keysym == "Up" and velocityY != 1:
        velocityX = 0
        velocityY = -1
    elif e.keysym == "Down" and velocityY != -1:
        velocityX = 0
        velocityY = 1
    elif e.keysym == "Left" and velocityX != 1:
        velocityX = -1
        velocityY = 0
    elif e.keysym == "Right" and velocityX != -1:
        velocityX = 1
        velocityY = 0


# def show_game_over_popup():
#     messagebox.showinfo("Game Over", f"Game Over!\nYour score: {score}")


def show_game_over_popup():
    popup = tkinter.Toplevel(window)
    popup.title("Game Over")
    popup.geometry("300x150")
    popup.configure(bg="#333333")  # Dark background

    # Center the popup window
    popup_x = window.winfo_x() + (WINDOW_WIDTH // 2) - 150
    popup_y = window.winfo_y() + (WINDOW_HEIGHT // 2) - 75
    popup.geometry(f"+{popup_x}+{popup_y}")

    label = tkinter.Label(popup, text=f"Game Over!\nYour Score: {score}", 
                          font=("Arial", 14, "bold"), fg="white", bg="#333333")
    label.pack(pady=20)

    btn = tkinter.Button(popup, text="OK", font=("Arial", 12), bg="#00bfff", fg="white", 
                         activebackground="#1e90ff", command=popup.destroy)
    btn.pack(pady=10)

    # Make sure popup is modal (blocks input to the main window)
    popup.transient(window)
    popup.grab_set()
    window.wait_window(popup)



def restart_game():
    global snake, food, snake_body, velocityX, velocityY, game_over, score, snake_color, current_food_color

    # Random starting position for snake
    start_x = random.randint(0, COLS - 1) * TILE_SIZE
    start_y = random.randint(0, ROWS - 1) * TILE_SIZE
    snake = Tile(start_x, start_y, "lime green")  # Reset with lime green

    # Random starting position for food (not same as snake)
    while True:
        food_x = random.randint(0, COLS - 1) * TILE_SIZE
        food_y = random.randint(0, ROWS - 1) * TILE_SIZE
        if food_x != start_x or food_y != start_y:
            break
    food = Tile(food_x, food_y)

    snake_body = []
    velocityX = 0
    velocityY = 0
    game_over = False
    score = 0
    snake_color = "lime green"
    current_food_color = random.choice([color for color in food_colors if color != snake_color])



def move():
    global snake, snake_body, game_over, score, snake_color, current_food_color

    if game_over:
        return

    if snake.x < 0 or snake.x >= WINDOW_WIDTH or snake.y < 0 or snake.y >= WINDOW_HEIGHT:
        game_over = True
        show_game_over_popup()
        return

    for tile in snake_body:
        if snake.x == tile.x and snake.y == tile.y:
          game_over = True
          show_game_over_popup()
          return


    # Collision with food
    if snake.x == food.x and snake.y == food.y:
        # Eat food → grow
        snake_body.append(Tile(food.x, food.y))  # No color stored per-tile
        score += 1

        # Update snake color to match the food just eaten
        snake_color = current_food_color

        # Generate new food position
        food.x = random.randint(0, COLS - 1) * TILE_SIZE
        food.y = random.randint(0, ROWS - 1) * TILE_SIZE

        # Pick a food color different from snake color
        current_food_color = random.choice([c for c in food_colors if c != snake_color])

    # Move snake body
    for i in range(len(snake_body) - 1, -1, -1):
        if i == 0:
            snake_body[i].x = snake.x
            snake_body[i].y = snake.y
        else:
            snake_body[i].x = snake_body[i - 1].x
            snake_body[i].y = snake_body[i - 1].y

    # Move snake head
    snake.x += velocityX * TILE_SIZE
    snake.y += velocityY * TILE_SIZE


def draw():
    global snake, food, snake_body, game_over, score

    move()
    canvas.delete("all")

    # Draw food
    canvas.create_rectangle(food.x, food.y, food.x + TILE_SIZE, food.y + TILE_SIZE, fill=current_food_color)

    # Draw snake head
    canvas.create_rectangle(snake.x, snake.y, snake.x + TILE_SIZE, snake.y + TILE_SIZE, fill=snake_color)

    # Draw snake body
    for tile in snake_body:
        canvas.create_rectangle(tile.x, tile.y, tile.x + TILE_SIZE, tile.y + TILE_SIZE, fill=snake_color)

    # Only show score text while game is active
    if not game_over:
        canvas.create_text(30, 20, font="Arial 10", text=f"Score: {score}", fill="white")

    window.after(100, draw)


draw()

window.bind("<KeyRelease>", change_direction)
window.mainloop()
