import tkinter as tk
import random
import time

total_score = 0
start_time = None
timer_running = False
restart_button = None

# Initialiser la fenêtre principale
window = tk.Tk()
window.title("GreenButton - La Sonath")
window.geometry("800x400")  # largeur x hauteur (à adapter selon ton écran)

# Menu de démarrage
def start_game():
    main_menu_frame.pack_forget()  # Masque le menu de démarrage
    game_frame.pack()  # Affiche le jeu
    start_level()  # Lance le jeu

def quit_game():
    window.quit()  # Quitte l'application

# Cadre du menu de démarrage
main_menu_frame = tk.Frame(window)
main_menu_frame.pack()

label = tk.Label(main_menu_frame, text="GreenButton", font=("Arial", 24))
label.pack(pady=20)

start_button = tk.Button(main_menu_frame, text="Jouer", font=("Arial", 14), command=start_game)
start_button.pack(pady=10)

quit_button = tk.Button(main_menu_frame, text="Quitter", font=("Arial", 14), command=quit_game)
quit_button.pack(pady=5)

# Cadre du jeu
game_frame = tk.Frame(window)

# Configuration des niveaux
LEVELS = [
    {"buttons": 3, "moves": 20, "hints": 3},
    {"buttons": 4, "moves": 20, "hints": 2},
    {"buttons": 5, "moves": 15, "hints": 1},
    {"buttons": 6, "moves": 15, "hints": 0},
]

current_level = 0
moves_left = 0
hints_left = 0
colors = []
solution = []
buttons = []


def start_level():
    global moves_left, colors, hints_left, buttons, solution
    config = LEVELS[current_level]
    moves_left = config["moves"]
    hints_left = config["hints"]
    num_buttons = config["buttons"]

    # Initialisation correcte des couleurs (tous les boutons doivent être "off" au début)
    colors = [False] * num_buttons  # Tous les boutons commencent en blanc

    solution = [random.choice([True, False]) for _ in range(num_buttons)]  # Solution aléatoire

    # Réinitialiser les boutons de l'interface
    for widget in game_frame.winfo_children():
        widget.destroy()
    buttons.clear()

    # Créer les boutons
    for i in range(num_buttons):
        btn = tk.Button(game_frame, width=10, height=4, bg="white", command=lambda i=i: toggle(i))
        btn.grid(row=0, column=i, padx=5, pady=5)
        buttons.append(btn)

    update_buttons()
    update_ui()


def toggle(index):
    global moves_left

    if moves_left <= 0 or all(colors):
        return

    # Changement de couleur du bouton cliqué
    colors[index] = not colors[index]

    # Influence simple : change aussi ses voisins
    if index > 0:
        colors[index - 1] = not colors[index - 1]
    if index < len(colors) - 1:
        colors[index + 1] = not colors[index + 1]

    moves_left -= 1
    update_buttons()
    check_end()


def update_buttons():
    for i, btn in enumerate(buttons):
        btn.config(bg="green" if colors[i] else "white")
    move_label.config(text=f"Coups restants : {moves_left}")
    hint_label.config(text=f"Indices restants : {hints_left}")


def show_hint():
    global hints_left
    if hints_left <= 0:
        return
    for i, val in enumerate(solution):
        if val:
            buttons[i].config(bg="lightgreen")
    hints_left -= 1
    hint_button.config(state=tk.DISABLED)
    update_ui()


def check_end():
    if all(colors):
        label.config(text="Gagné ! Passage au niveau suivant...")
        disable_buttons()
        window.after(2000, next_level)
        global total_score, timer_running
        total_score += 1
        timer_running = False
        score_label.config(text=f"Score total : {total_score}")

    elif moves_left == 0:
        label.config(text="Perdu !", fg="red")
        for btn in buttons:
            btn.config(bg="red")
        disable_buttons()

        global restart_button
        if restart_button is not None:
            restart_button.destroy()

        restart_button = tk.Button(window, text="Recommencer", command=restart_level)
        restart_button.pack(pady=10)

        timer_running = False


def restart_level():
    global colors, moves_left, hints_left, timer_running, start_time
    # Réinitialiser les données du niveau actuel
    level_data = LEVELS[current_level]
    num_buttons = level_data["buttons"]
    moves_left = level_data["moves"]
    hints_left = level_data["hints"]

    # Réinitialiser les couleurs des boutons (les boutons doivent être "off" au début)
    colors = [False] * num_buttons  # Tous les boutons commencent en blanc

    # Réinitialiser la solution
    solution[:] = [random.choice([True, False]) for _ in range(num_buttons)]

    # Mettre à jour l'interface
    label.config(text="", fg="black")
    update_buttons()
    update_ui()

    # Redémarrer le timer
    start_time = time.time()
    timer_running = True
    update_timer()

    # Cacher le bouton "Recommencer" après avoir redémarré le niveau
    if restart_button is not None:
        restart_button.pack_forget()

    # Réactiver les boutons du jeu
    for btn in buttons:
        btn.config(state=tk.NORMAL)


def disable_buttons():
    for btn in buttons:
        btn.config(state=tk.DISABLED)

def update_timer():
    if timer_running:
        elapsed = int(time.time() - start_time)
        timer_label.config(text=f"Temps : {elapsed} sec")
        window.after(1000, update_timer)

def next_level():
    global current_level
    current_level += 1
    if current_level < len(LEVELS):
        start_level()
    else:
        label.config(text="Félicitations ! Vous avez terminé tous les niveaux.", fg="blue")
        hint_button.config(state=tk.DISABLED)


def update_ui():
    move_label.config(text=f"Coups restants : {moves_left}")
    hint_label.config(text=f"Indices restants : {hints_left}")
    hint_button.config(state=tk.NORMAL if hints_left > 0 else tk.DISABLED)

def use_hint():
    global hints_left
    if hints_left > 0:
        # Trouver les boutons non résolus (ceux qui sont encore blancs)
        unresolved_buttons = [i for i in range(len(colors)) if not colors[i]]

        if unresolved_buttons:
            # Choisir un bouton au hasard parmi ceux non résolus (blancs)
            button_to_hint = unresolved_buttons[0]  # Pour le moment, on prend le premier bouton non résolu

            # Mettre ce bouton en lightblue pour l'indice
            buttons[button_to_hint].config(bg="lightblue")

            # Afficher un message expliquant l'indice
            label.config(
                text=f"Indice : cliquez sur le bouton lightblue !\nIndices restants : {hints_left - 1}",
                fg="blue",
            )

            # Après 5 secondes, remettre la couleur normale
            window.after(5000, update_buttons)  # On remet la couleur après 5 secondes
        else:
            label.config(text="Tous les boutons sont déjà au bon état.", fg="gray")

        hints_left -= 1
        update_ui()
    else:
        label.config(text="Plus d'indices disponibles.", fg="red")


def jouer_jeu1(screen, clock, progression, retour_menu_callback):
    import tkinter as tk

    def on_close():
        root.destroy()
        retour_menu_callback()  # <- Retour au menu après fermeture

    root = tk.Tk()
    root.title("GreenButton - La Sonath")

    # Ton code de jeu ici...
    # root.mainloop() à la fin

    root.protocol("WM_DELETE_WINDOW", on_close)  # Gérer la fermeture proprement
    root.mainloop()


# --- Interface Tkinter ---
frame = tk.Frame(window)
frame.pack()

hints_left = LEVELS[current_level]["hints"]

buttons = []

label = tk.Label(window, text="Jeu", font=("Arial", 14))
label.pack()

move_label = tk.Label(window, text="", font=("Arial", 12))
move_label.pack()

hint_label = tk.Label(window, text="", font=("Arial", 12))
hint_label.pack()


hint_button = tk.Button(window, text="Indice", command=show_hint)
hint_button.pack(pady=5)

score_label = tk.Label(window, text="Score total : 0", font=("Arial", 12))
score_label.pack()

timer_label = tk.Label(window, text="Temps : 0 sec", font=("Arial", 12))
timer_label.pack()

start_level()
window.mainloop()



