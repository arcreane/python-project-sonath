import tkinter as tk

def toggle(button_index):
    """Fonction qui change la couleur du bouton cliqué et qui """
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
        buttons[i].config(bg="black" if colors[i] else "white")


def check_win():
    """Vérifie si tous les boutons sont noirs et affiche un message de victoire."""
    if all(colors):
        label.config(text="Vous avez gagné !", fg="green", font=("Arial", 14, "bold"))
        for btn in buttons:
            btn.config(state=tk.DISABLED)  # Désactive les boutons après la victoire
    else:
        label.config(text="")


# Création de la fenêtre
window = tk.Tk()
window.title("Jeu des 5 boutons")

# Initialisation des couleurs des boutons (False = blanc, True = noir)
colors = [False] * 5

# Création des boutons
frame = tk.Frame(window)
frame.pack()

buttons = []
for i in range(5):
    btn = tk.Button(frame, width=5, height=2, bg="white", command=lambda i=i: toggle(i))
    btn.grid(row=0, column=i, padx=5, pady=5)
    btn.config(relief=tk.FLAT, borderwidth=0, highlightthickness=0)
    btn.config(font=("Arial", 12, "bold"), padx=15, pady=15)
    btn.config(height=2, width=5)
    btn.config(bg="white", activebackground="black")
    buttons.append(btn)

label = tk.Label(window, text="Changez la couleur de tous les boutons en noir !")
label.pack()

window.mainloop()