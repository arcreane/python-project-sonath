import tkinter as tk


def toggle(button_index):
    """Change la couleur du bouton cliqué et influe sur d'autres boutons."""
    colors[button_index] = not colors[button_index]

    # Règles d'influence entre les boutons
    influence_map = {
        0: [1, 2],  # Bouton 0 affecte 1 et 2
        1: [0, 3],  # Bouton 1 affecte 0 et 3
        2: [4],  # Bouton 2 affecte 4
        3: [1, 4],  # Bouton 3 affecte 1 et 4
        4: [2, 3]  # Bouton 4 affecte 2 et 3
    }

    for affected in influence_map.get(button_index, []):
        colors[affected] = not colors[affected]

    update_buttons()
    check_win()


def update_buttons():
    """Met à jour l'affichage des boutons selon leur état."""
    for i in range(5):
        buttons[i].config(bg="#4CAF50" if colors[i] else "#f0f0f0", fg="black")


def check_win():
    """Vérifie si tous les boutons sont verts et affiche un message de victoire."""
    if all(colors):
        label.config(text="Vous avez gagné !", fg="#FFD700", font=("Arial", 16, "bold"))
        for btn in buttons:
            btn.config(state=tk.DISABLED)  # Désactive les boutons après la victoire
    else:
        label.config(text="")


# Création de la fenêtre
root = tk.Tk()
root.title("Jeu des 5 boutons")
root.geometry("400x200")
root.configure(bg="#222831")  # Fond de la fenêtre en gris foncé

# Initialisation des couleurs des boutons (False = blanc, True = vert)
colors = [False] * 5

# Création des boutons
frame = tk.Frame(root, bg="#222831")  # Fond du cadre en gris foncé
frame.pack(pady=20)

buttons = []
for i in range(5):
    btn = tk.Button(frame, width=6, height=2, bg="#f0f0f0", fg="black", font=("Arial", 12, "bold"),
                     command=lambda i=i: toggle(i), relief=tk.RAISED, borderwidth=2, highlightthickness=0)
    btn.grid(row=0, column=i, padx=8, pady=8)
    btn.config(activebackground="#4CAF50", activeforeground="white")
    buttons.append(btn)

label = tk.Label(root, text="Changez la couleur de tous les boutons en vert !", bg="#222831", fg="#f8f9fa",
                 font=("Arial", 12, "italic"))
label.pack()

root.mainloop()
