import tkinter as tk
import random

class PacmanGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Pac-Man Challenge")

        self.canvas = tk.Canvas(root, width=1250, height=700, bg="teal")
        self.canvas.pack()

        self.grid_size = 40  # Taille d'une case
        self.num_rows = 17
        self.num_cols = 31



        self.player_pos = [16, 0]  # Position initiale (ligne, colonne)
        self.direction = "right"  # Direction initiale
        self.exit_pos = (0, 30)  # Position de sortie (ligne, colonne)

        # generer aleatoirement des obstacles
        self.obstacles = self.generate_obstacles(count=100)




        self.draw_maze()
        self.root.bind("<space>", self.change_direction)
        self.move()


    def generate_obstacles(self, count=100):
        obstacles = set()
        forbidden = {tuple(self.player_pos), self.exit_pos}
        while len(obstacles) < count:
            row = random.randint(0, self.num_rows - 1)
            col = random.randint(0, self.num_cols - 1)
            if (row, col) not in obstacles and (row, col) not in forbidden:
                obstacles.add((row, col))

        return list(obstacles)






    def draw_maze(self):
        """Dessine le labyrinthe avec les obstacles, le joueur et la sortie."""
        self.canvas.delete("all")

        # Dessiner les lignes et colonnes de la grille
        for i in range(32):
            self.canvas.create_line(i * self.grid_size, 0, i * self.grid_size, 17 * self.grid_size, fill="navy")

        for i in range(18):
            self.canvas.create_line(0, i * self.grid_size, 31 * self.grid_size, i * self.grid_size, fill="navy")


        # Dessiner les obstacles
        for (row, col) in self.obstacles:
            x1, y1 = col * self.grid_size, row * self.grid_size
            x2, y2 = x1 + self.grid_size, y1 + self.grid_size
            self.canvas.create_rectangle(x1, y1, x2, y2, fill="black")

        # Dessiner la porte de sortie
        x1, y1 = self.exit_pos[1] * self.grid_size, self.exit_pos[0] * self.grid_size
        x2, y2 = x1 + self.grid_size, y1 + self.grid_size
        self.canvas.create_rectangle(x1, y1, x2, y2, fill="green")

        # Dessiner le joueur (Pac-Man)
        x1, y1 = self.player_pos[1] * self.grid_size, self.player_pos[0] * self.grid_size
        x2, y2 = x1 + self.grid_size, y1 + self.grid_size
        self.player = self.canvas.create_oval(x1, y1, x2, y2, fill="yellow", outline="orange", width=3)

    def change_direction(self, event):
        """Change la direction du joueur entre droite et haut."""
        if self.direction == "right":
            self.direction = "up"
        else:
            self.direction = "right"

    def move(self):
        """Fait avancer le joueur dans la direction actuelle."""
        row, col = self.player_pos
        if self.direction == "right":
            col += 1
        else:
            row -= 1

        # Vérifier les collisions avec les obstacles ou les limites
        if (row, col) in self.obstacles or not (0 <= row < 19 and 0 <= col < 31):
            self.player_pos = [16, 0]  # Réinitialiser la position
        else:
            self.player_pos = [row, col]

        self.draw_maze()

        # Vérifier si le joueur a atteint la sortie
        if tuple(self.player_pos) == self.exit_pos:
            self.canvas.create_text(650, 350, text="Vous avez gagné !", font=("Arial", 40, "bold"), fill="blue")
        else:
            self.root.after(200, self.move) #temps de déplacement

# Lancer le jeu
root = tk.Tk()
game = PacmanGame(root)
root.mainloop()
