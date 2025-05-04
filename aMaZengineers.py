import tkinter as tk
import random
import time
import os

class MovingObstacle:
    def __init__(self, start_pos, direction, grid_size, num_rows, num_cols):
        self.pos = start_pos
        self.direction = direction
        self.grid_size = grid_size
        self.num_rows = num_rows
        self.num_cols = num_cols

    def move(self):
        row, col = self.pos
        if self.direction == "right":
            col += 1
        elif self.direction == "left":
            col -= 1
        elif self.direction == "up":
            row -= 1
        elif self.direction == "down":
            row += 1

        if not (0 <= row < self.num_rows and 0 <= col < self.num_cols):
            self.direction = random.choice(["up", "down", "left", "right"])
        else:
            self.pos = (row, col)

class aMaZengineers:
    def __init__(self, root):
        self.root = root
        self.root.title("Pac-Man Challenge")

        self.grid_size = 20
        self.num_rows = 35
        self.num_cols = 62

        canvas_width = self.num_cols * self.grid_size
        canvas_height = self.num_rows * self.grid_size + 50
        self.canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="midnightblue")
        self.canvas.pack()

        self.menu_buttons = []
        self.level = 1
        self.start_time = None
        self.elapsed_time = 0
        self.best_time = self.load_best_time()
        self.bonbons = []
        self.show_start_menu()

    def load_best_time(self):
        try:
            with open("best_score.txt", "r") as f:
                return int(f.read().strip())
        except:
            return None

    def save_best_time(self, time_seconds):
        with open("best_score.txt", "w") as f:
            f.write(str(time_seconds))

    def reset_game(self):
        self.level = 1
        self.lives = 10
        self.start_time = None
        self.elapsed_time = 0
        self.player_pos = [33, 0]
        self.direction = "right"
        self.exit_unlocked = False
        self.bonbons = self.generate_bonbons(count=5)
        self.obstacles = self.generate_obstacles(count=300)
        self.moving_obstacles = self.create_moving_obstacles(count=2)
        self.clear_canvas()

    def show_start_menu(self):
        self.clear_canvas()

        if self.best_time is not None:
            self.root.after(100, self.display_best_time)

        start_button = tk.Button(self.root, text="Démarrer le jeu", font=("Arial", 16, "bold"),
                                 width=20, height=2, command=self.start_game, bg="#4CAF50", fg="white")
        quit_button = tk.Button(self.root, text="Quitter", font=("Arial", 16, "bold"),
                                width=20, height=2, command=self.root.destroy, bg="red", fg="white")

        start_button.place(relx=0.5, rely=0.4, anchor="center")
        quit_button.place(relx=0.5, rely=0.6, anchor="center")

        self.menu_buttons.extend([start_button, quit_button])

    def display_best_time(self):
        self.canvas.delete("best_time_text")
        best_minutes = self.best_time // 60
        best_seconds = self.best_time % 60
        canvas_width = self.canvas.winfo_width()
        self.canvas.create_text(canvas_width // 2, 40,
                                text=f"Meilleur temps : {best_minutes:02}:{best_seconds:02}",
                                fill="gold", font=("Arial", 18, "bold"), tags="best_time_text")

    def start_game(self):
        for btn in self.menu_buttons:
            btn.destroy()
        self.menu_buttons.clear()
        self.show_instructions()

    def show_instructions(self):
        message = (
            "Bienvenue dans Pac-Man Challenge !\n\n"
            "Objectif : Ramassez tous les bonbons pour débloquer la sortie verte.\n"
            "Utilisez les FLÈCHES pour vous déplacer.\n"
            "Vous avez 10 vies pour y arriver. Bonne chance !"
        )

        font_style = ("Arial", 14, "bold")
        text_id = self.canvas.create_text(0, 0, text=message, font=font_style, anchor="nw", tags="msg")
        self.canvas.update_idletasks()
        bbox = self.canvas.bbox(text_id)
        self.canvas.delete(text_id)

        x = (self.canvas.winfo_width() - (bbox[2] - bbox[0])) // 2
        y = (self.canvas.winfo_height() - (bbox[3] - bbox[1])) // 2

        self.canvas.create_rectangle(x - 20, y - 20, x + (bbox[2] - bbox[0]) + 20,
                                     y + (bbox[3] - bbox[1]) + 20, fill="white", outline="black", tags="msg")
        self.canvas.create_text(x + 2, y + 2, text=message, font=font_style, fill="black", anchor="nw", tags="msg")

        self.root.after(3000, self.start_play)

    def start_play(self):
        self.canvas.delete("msg")

        self.player_pos = [33, 0]
        self.direction = "right"
        self.lives = 10
        self.exit_pos = (0, 61)
        self.obstacles = self.generate_obstacles(count=300)
        self.moving_obstacles = self.create_moving_obstacles(count=2)
        self.bonbons = self.generate_bonbons(count=5)
        self.exit_unlocked = False

        self.root.bind("<Up>", self.change_direction_up)
        self.root.bind("<Down>", self.change_direction_down)
        self.root.bind("<Left>", self.change_direction_left)
        self.root.bind("<Right>", self.change_direction_right)

        if self.level == 1:
            self.start_time = time.time()

        self.move()

    def generate_obstacles(self, count=300):
        obstacles = set()
        forbidden = {tuple(self.player_pos), self.exit_pos}
        protected_zone = set()
        px, py = self.player_pos
        for i in range(px - 7, px + 8):
            for j in range(py - 7, py + 8):
                if 0 <= i < self.num_rows and 0 <= j < self.num_cols:
                    protected_zone.add((i, j))

        while len(obstacles) < count:
            row = random.randint(0, self.num_rows - 1)
            col = random.randint(0, self.num_cols - 1)
            pos = (row, col)
            if pos not in obstacles and pos not in forbidden and pos not in protected_zone:
                obstacles.add(pos)

        return list(obstacles)

    def generate_bonbons(self, count=5):
        bonbons = set()
        while len(bonbons) < count:
            row = random.randint(0, self.num_rows - 1)
            col = random.randint(0, self.num_cols - 1)
            pos = (row, col)
            if pos not in bonbons and pos not in self.obstacles and pos != tuple(self.player_pos):
                bonbons.add(pos)
        return list(bonbons)

    def create_moving_obstacles(self, count=2):
        moving_obstacles = []
        for _ in range(count):
            start_pos = (random.randint(0, self.num_rows - 1), random.randint(0, self.num_cols - 1))
            direction = random.choice(["up", "down", "left", "right"])
            moving_obstacles.append(MovingObstacle(start_pos, direction, self.grid_size, self.num_rows, self.num_cols))
        return moving_obstacles

    def draw_maze(self):
        self.clear_canvas()

        for (row, col) in self.obstacles:
            x1 = col * self.grid_size
            y1 = row * self.grid_size
            x2 = x1 + self.grid_size
            y2 = y1 + self.grid_size
            self.canvas.create_oval(x1 + 2, y1 + 2, x2 - 2, y2 - 2, fill="gray35")

        if self.exit_unlocked:
            ex, ey = self.exit_pos[1] * self.grid_size, self.exit_pos[0] * self.grid_size
            self.canvas.create_oval(ex - 5, ey - 5, ex + self.grid_size + 5, ey + self.grid_size + 5, outline="limegreen", width=4)
            self.canvas.create_oval(ex, ey, ex + self.grid_size, ey + self.grid_size, fill="limegreen", outline="black", width=2)

        for (row, col) in self.bonbons:
            x = col * self.grid_size + self.grid_size // 2
            y = row * self.grid_size + self.grid_size // 2
            self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill="white", outline="pink")

        px, py = self.player_pos[1] * self.grid_size, self.player_pos[0] * self.grid_size
        self.canvas.create_oval(px + 3, py + 3, px + self.grid_size - 3, py + self.grid_size - 3,
                                fill="yellow", outline="orange", width=3)

        for obstacle in self.moving_obstacles:
            ox, oy = obstacle.pos[1] * self.grid_size, obstacle.pos[0] * self.grid_size
            self.canvas.create_oval(ox + 3, oy + 3, ox + self.grid_size - 3, oy + self.grid_size - 3,
                                    fill="red", outline="black", width=2)

        self.draw_status()

    def draw_status(self):
        bottom_y = self.num_rows * self.grid_size + 10
        for i in range(10):
            x1 = 10 + i * 30
            y1 = bottom_y
            x2 = x1 + 20
            y2 = y1 + 20
            color = "red" if i < self.lives else "gray"
            self.canvas.create_oval(x1, y1, x2, y2, fill=color, outline="white")

        bonbons_text = f"Bonbons restants : {len(self.bonbons)}"
        self.canvas.create_text(350, bottom_y + 10, anchor="nw", text=bonbons_text, fill="white", font=("Arial", 14, "bold"))

        if self.start_time:
            self.elapsed_time = int(time.time() - self.start_time)
            minutes = self.elapsed_time // 60
            seconds = self.elapsed_time % 60
            self.canvas.create_text(self.canvas.winfo_width() - 10, bottom_y + 10, anchor="ne",
                                    text=f"Temps : {minutes:02}:{seconds:02}", fill="white", font=("Arial", 14, "bold"))

    def change_direction_up(self, event): self.direction = "up"
    def change_direction_down(self, event): self.direction = "down"
    def change_direction_left(self, event): self.direction = "left"
    def change_direction_right(self, event): self.direction = "right"

    def move(self):
        if self.lives == 0:
            self.display_game_over()
            return

        for obstacle in self.moving_obstacles:
            obstacle.move()

        row, col = self.player_pos
        if self.direction == "right":
            col += 1
        elif self.direction == "left":
            col -= 1
        elif self.direction == "up":
            row -= 1
        elif self.direction == "down":
            row += 1

        new_pos = (row, col)

        if new_pos in self.obstacles or new_pos in [o.pos for o in self.moving_obstacles] or not (0 <= row < self.num_rows and 0 <= col < self.num_cols):
            self.lives -= 1
            self.player_pos = [33, 0]
        else:
            self.player_pos = [row, col]

        if new_pos in self.bonbons:
            self.bonbons.remove(new_pos)

        if not self.bonbons and not self.exit_unlocked:
            self.exit_unlocked = True
            self.canvas.create_text(self.canvas.winfo_width() // 2, self.canvas.winfo_height() // 2,
                                    text="Sortie débloquée !", fill="lime", font=("Arial", 18, "bold"))
            self.root.after(1500, lambda: self.canvas.delete("all"))

        self.draw_maze()

        if self.exit_unlocked and tuple(self.player_pos) == self.exit_pos:
            if self.level == 3:
                self.display_victory()
                return
            else:
                self.level += 1
                self.start_play()
                return

        vitesse = {1: 140, 2: 130, 3: 120}
        self.root.after(vitesse.get(self.level, 140), self.move)

    def display_game_over(self):
        self.canvas.create_text(self.canvas.winfo_width() // 2, self.canvas.winfo_height() // 2 - 50,
                                text="Game Over!", fill="red", font=("Arial", 24, "bold"))
        self.show_restart_button()

    def display_victory(self):
        total_time = int(time.time() - self.start_time)
        minutes = total_time // 60
        seconds = total_time % 60
        self.canvas.create_text(self.canvas.winfo_width() // 2, self.canvas.winfo_height() // 2 - 70,
                                text="Félicitations ! Vous avez gagné !", fill="lime", font=("Arial", 24, "bold"))
        self.canvas.create_text(self.canvas.winfo_width() // 2, self.canvas.winfo_height() // 2 - 30,
                                text=f"Temps total : {minutes:02}:{seconds:02}", fill="white", font=("Arial", 18))

        if self.best_time is None or total_time < self.best_time:
            self.best_time = total_time
            self.save_best_time(total_time)
            self.canvas.create_text(self.canvas.winfo_width() // 2, self.canvas.winfo_height() // 2 + 10,
                                    text="Nouveau record !", fill="gold", font=("Arial", 18, "bold"))

        self.show_restart_button()

    def show_restart_button(self):
        restart_button = tk.Button(self.root, text="Rejouer", font=("Arial", 16, "bold"),
                                   command=self.restart_game, bg="orange", fg="white")
        restart_button.place(relx=0.5, rely=0.55, anchor="center")
        self.menu_buttons.append(restart_button)

    def restart_game(self):
        for btn in self.menu_buttons:
            btn.destroy()
        self.menu_buttons.clear()
        self.reset_game()
        self.show_start_menu()

    def clear_canvas(self):
        self.canvas.delete("all")

# Lancer le jeu
root = tk.Tk()
game = aMaZengineers(root)
root.mainloop()
