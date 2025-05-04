import tkinter as tk
import random
import time
import os

# Paramètres globaux
grid_size = 20
num_rows = 35
num_cols = 62
exit_pos = (0, 61)

# Variables de jeu
canvas = None
root = None
player_pos = [33, 0]
direction = "right"
obstacles = []
moving_obstacles = []
bonbons = []
exit_unlocked = False
lives = 10
level = 1
start_time = None
elapsed_time = 0
best_time = None
menu_buttons = []

def load_best_time():
    try:
        with open("best_score.txt", "r") as f:
            return int(f.read().strip())
    except:
        return None

def save_best_time(time_seconds):
    with open("best_score.txt", "w") as f:
        f.write(str(time_seconds))

def reset_game():
    global player_pos, direction, obstacles, moving_obstacles, bonbons, exit_unlocked, lives, level, start_time, elapsed_time
    player_pos = [33, 0]
    direction = "right"
    lives = 10
    level = 1
    start_time = None
    elapsed_time = 0
    exit_unlocked = False
    obstacles = generate_obstacles()
    moving_obstacles = create_moving_obstacles()
    bonbons = generate_bonbons()

def show_start_menu():
    clear_canvas()
    if best_time is not None:
        root.after(100, display_best_time)
    start_btn = tk.Button(root, text="Démarrer le jeu", font=("Arial", 16, "bold"),
                          width=20, height=2, command=start_game, bg="#4CAF50", fg="white")
    quit_btn = tk.Button(root, text="Quitter", font=("Arial", 16, "bold"),
                         width=20, height=2, command=root.destroy, bg="red", fg="white")
    start_btn.place(relx=0.5, rely=0.4, anchor="center")
    quit_btn.place(relx=0.5, rely=0.6, anchor="center")
    menu_buttons.extend([start_btn, quit_btn])

def display_best_time():
    canvas.delete("best_time_text")
    best_minutes = best_time // 60
    best_seconds = best_time % 60
    canvas.create_text(canvas.winfo_width() // 2, 40,
                       text=f"Meilleur temps : {best_minutes:02}:{best_seconds:02}",
                       fill="gold", font=("Arial", 18, "bold"), tags="best_time_text")

def start_game():
    for btn in menu_buttons:
        btn.destroy()
    menu_buttons.clear()
    show_instructions()

def show_instructions():
    msg = (
        "Bienvenue dans Pac-Man Challenge !\n\n"
        "Objectif : Ramassez tous les bonbons pour débloquer la sortie verte.\n"
        "Utilisez les FLÈCHES pour vous déplacer.\n"
        "Vous avez 10 vies pour y arriver. Bonne chance !"
    )
    font_style = ("Arial", 14, "bold")
    text_id = canvas.create_text(0, 0, text=msg, font=font_style, anchor="nw", tags="msg")
    canvas.update_idletasks()
    bbox = canvas.bbox(text_id)
    canvas.delete(text_id)
    x = (canvas.winfo_width() - (bbox[2] - bbox[0])) // 2
    y = (canvas.winfo_height() - (bbox[3] - bbox[1])) // 2
    canvas.create_rectangle(x - 20, y - 20, x + (bbox[2] - bbox[0]) + 20,
                            y + (bbox[3] - bbox[1]) + 20, fill="white", outline="black", tags="msg")
    canvas.create_text(x + 2, y + 2, text=msg, font=font_style, fill="black", anchor="nw", tags="msg")
    root.after(3000, start_play)

def start_play():
    global player_pos, direction, lives, obstacles, bonbons, moving_obstacles, exit_unlocked, start_time
    canvas.delete("msg")
    player_pos = [33, 0]
    direction = "right"
    lives = 10
    obstacles = generate_obstacles()
    moving_obstacles = create_moving_obstacles()
    bonbons = generate_bonbons()
    exit_unlocked = False
    root.bind("<Up>", lambda e: change_direction("up"))
    root.bind("<Down>", lambda e: change_direction("down"))
    root.bind("<Left>", lambda e: change_direction("left"))
    root.bind("<Right>", lambda e: change_direction("right"))
    if level == 1:
        start_time = time.time()
    move()

def change_direction(new_dir):
    global direction
    direction = new_dir

def generate_obstacles(count=300):
    forbidden = {(33, 0), exit_pos}
    protected_zone = {(i, j) for i in range(26, 41) for j in range(0, 15)}
    obstacles = set()
    while len(obstacles) < count:
        pos = (random.randint(0, num_rows - 1), random.randint(0, num_cols - 1))
        if pos not in obstacles and pos not in forbidden and pos not in protected_zone:
            obstacles.add(pos)
    return list(obstacles)

def generate_bonbons(count=5):
    bonbons_set = set()
    while len(bonbons_set) < count:
        pos = (random.randint(0, num_rows - 1), random.randint(0, num_cols - 1))
        if pos not in bonbons_set and pos not in obstacles and pos != tuple(player_pos):
            bonbons_set.add(pos)
    return list(bonbons_set)

def create_moving_obstacles(count=7):
    return [{"pos": (random.randint(0, num_rows - 1), random.randint(0, num_cols - 1)),
             "dir": random.choice(["up", "down", "left", "right"])} for _ in range(count)]

def move_obstacles():
    for mob in moving_obstacles:
        row, col = mob["pos"]
        direction = mob["dir"]
        if direction == "up":
            row -= 1
        elif direction == "down":
            row += 1
        elif direction == "left":
            col -= 1
        elif direction == "right":
            col += 1
        if 0 <= row < num_rows and 0 <= col < num_cols:
            mob["pos"] = (row, col)
        else:
            mob["dir"] = random.choice(["up", "down", "left", "right"])

def move():
    global player_pos, lives, bonbons, exit_unlocked, level, elapsed_time
    if lives == 0:
        display_game_over()
        return

    move_obstacles()

    row, col = player_pos
    if direction == "right": col += 1
    elif direction == "left": col -= 1
    elif direction == "up": row -= 1
    elif direction == "down": row += 1

    new_pos = (row, col)

    if new_pos in obstacles or new_pos in [o["pos"] for o in moving_obstacles] or not (0 <= row < num_rows and 0 <= col < num_cols):
        lives -= 1
        player_pos = [33, 0]
    else:
        player_pos = [row, col]

    if new_pos in bonbons:
        bonbons.remove(new_pos)

    if not bonbons and not exit_unlocked:
        exit_unlocked = True
        canvas.create_text(canvas.winfo_width() // 2, canvas.winfo_height() // 2,
                           text="Sortie débloquée !", fill="lime", font=("Arial", 18, "bold"))
        root.after(1500, clear_canvas)

    draw_maze()

    if exit_unlocked and tuple(player_pos) == exit_pos:
        if level == 3:
            display_victory()
            return
        else:
            level += 1
            start_play()
            return

    vitesse = {1: 140, 2: 130, 3: 120}
    root.after(vitesse.get(level, 140), move)

def draw_maze():
    clear_canvas()
    for (r, c) in obstacles:
        x1 = c * grid_size
        y1 = r * grid_size
        x2 = x1 + grid_size
        y2 = y1 + grid_size
        canvas.create_oval(x1 + 2, y1 + 2, x2 - 2, y2 - 2, fill="gray35")

    if exit_unlocked:
        ex, ey = exit_pos[1] * grid_size, exit_pos[0] * grid_size
        canvas.create_oval(ex - 5, ey - 5, ex + grid_size + 5, ey + grid_size + 5, outline="limegreen", width=4)
        canvas.create_oval(ex, ey, ex + grid_size, ey + grid_size, fill="limegreen", outline="black", width=2)

    for (r, c) in bonbons:
        x = c * grid_size + grid_size // 2
        y = r * grid_size + grid_size // 2
        canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill="white", outline="pink")

    px, py = player_pos[1] * grid_size, player_pos[0] * grid_size
    canvas.create_oval(px + 3, py + 3, px + grid_size - 3, py + grid_size - 3, fill="yellow", outline="orange", width=3)

    for mob in moving_obstacles:
        ox, oy = mob["pos"][1] * grid_size, mob["pos"][0] * grid_size
        canvas.create_oval(ox + 3, oy + 3, ox + grid_size - 3, oy + grid_size - 3, fill="red", outline="black", width=2)

    draw_status()

def draw_status():
    bottom_y = num_rows * grid_size + 10
    for i in range(10):
        x1 = 10 + i * 30
        x2 = x1 + 20
        color = "red" if i < lives else "gray"
        canvas.create_oval(x1, bottom_y, x2, bottom_y + 20, fill=color, outline="white")

    canvas.create_text(350, bottom_y + 10, anchor="nw", text=f"Bonbons restants : {len(bonbons)}", fill="white", font=("Arial", 14, "bold"))

    if start_time:
        elapsed = int(time.time() - start_time)
        mins = elapsed // 60
        secs = elapsed % 60
        canvas.create_text(canvas.winfo_width() - 10, bottom_y + 10, anchor="ne",
                           text=f"Temps : {mins:02}:{secs:02}", fill="white", font=("Arial", 14, "bold"))

def display_game_over():
    canvas.create_text(canvas.winfo_width() // 2, canvas.winfo_height() // 2 - 50,
                       text="Game Over!", fill="red", font=("Arial", 24, "bold"))
    show_restart_button()

def display_victory():
    global best_time
    total = int(time.time() - start_time)
    mins = total // 60
    secs = total % 60
    canvas.create_text(canvas.winfo_width() // 2, canvas.winfo_height() // 2 - 70,
                       text="Félicitations ! Vous avez gagné !", fill="lime", font=("Arial", 24, "bold"))
    canvas.create_text(canvas.winfo_width() // 2, canvas.winfo_height() // 2 - 30,
                       text=f"Temps total : {mins:02}:{secs:02}", fill="white", font=("Arial", 18))
    if best_time is None or total < best_time:
        best_time = total
        save_best_time(total)
        canvas.create_text(canvas.winfo_width() // 2, canvas.winfo_height() // 2 + 10,
                           text="Nouveau record !", fill="gold", font=("Arial", 18, "bold"))
    show_restart_button()

def show_restart_button():
    restart_btn = tk.Button(root, text="Rejouer", font=("Arial", 16, "bold"),
                            command=restart_game, bg="orange", fg="white")
    restart_btn.place(relx=0.5, rely=0.55, anchor="center")
    menu_buttons.append(restart_btn)

def restart_game():
    for btn in menu_buttons:
        btn.destroy()
    menu_buttons.clear()
    reset_game()
    show_start_menu()

def clear_canvas():
    canvas.delete("all")

# Initialisation de la fenêtre
root = tk.Tk()
root.title("Pac-Man Challenge")
canvas = tk.Canvas(root, width=num_cols * grid_size, height=num_rows * grid_size + 50, bg="midnightblue")
canvas.pack()

best_time = load_best_time()
reset_game()
show_start_menu()

root.mainloop()