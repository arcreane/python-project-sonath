import tkinter as tk

class PacmanGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Pac-Man Challenge")

        self.canvas = tk.Canvas(root, width=1250, height=700, bg="white")
        self.canvas.pack()

        self.grid_size = 40  # Taille d'une case
        self.player_pos = [15, 0]  # Position initiale (ligne, colonne)
        self.direction = "right"  # Direction initiale

        self.obstacles = [
            (5, 2), (6, 3), (4, 4), (3, 2), (2, 4), (6, 6), (1,2), (0,0)
        ]  # Moins d'obstacles et recentrés
        self.exit_pos = (0, 30)  # Position de sortie (ligne, colonne)

        self.draw_maze()
        self.root.bind("<space>", self.change_direction)
        self.move()

    def draw_maze(self):
        """Dessine le labyrinthe avec les obstacles, le joueur et la sortie."""
        self.canvas.delete("all")

        # Dessiner les lignes et colonnes de la grille
        for i in range(32):
            self.canvas.create_line(i * self.grid_size, 0, i * self.grid_size, 16 * self.grid_size, fill="gray")

        for i in range(17):
            self.canvas.create_line(0, i * self.grid_size, 31 * self.grid_size, i * self.grid_size, fill="gray")


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
        self.player = self.canvas.create_oval(x1, y1, x2, y2, fill="yellow")

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
            self.player_pos = [15, 0]  # Réinitialiser la position
        else:
            self.player_pos = [row, col]

        self.draw_maze()

        # Vérifier si le joueur a atteint la sortie
        if tuple(self.player_pos) == self.exit_pos:
            self.canvas.create_text(200, 200, text="Vous avez gagné !", font=("Arial", 20, "bold"), fill="blue")
        else:
            self.root.after(500, self.move)

# Lancer le jeu
root = tk.Tk()
game = PacmanGame(root)
root.mainloop()
