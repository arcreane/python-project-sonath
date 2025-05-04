import tkinter as tk
import random
from tkinter import messagebox, Menu

TAILLE = 3  # Constante pour la taille de la grille

def creer_grille(taille):
    grille = list(range(1, taille**2))
    grille.append(0)
    random.shuffle(grille)
    return grille

def trouver_case_vide(grille, taille):
    for i in range(taille):
        for j in range(taille):
            if grille[i * taille + j] == 0:
                return i, j

def deplacer_piece(grille, taille, ligne, colonne):
    ligne_vide, colonne_vide = trouver_case_vide(grille, taille)
    if (ligne == ligne_vide and abs(colonne - colonne_vide) == 1) or \
       (colonne == colonne_vide and abs(ligne - ligne_vide) == 1):
        grille[ligne * taille + colonne], grille[ligne_vide * taille + colonne_vide] = \
            grille[ligne_vide * taille + colonne_vide], grille[ligne * taille + colonne]
        update_buttons(taille)
        compteur_coups.set(compteur_coups.get() + 1)
        if verifier_victoire(grille, taille):
            afficher_message("Félicitations !", "Vous avez gagné !")

def verifier_victoire(grille, taille):
    return grille == list(range(1, taille**2)) + [0]

def update_buttons(taille):
    for i in range(taille):
        for j in range(taille):
            index = i * taille + j
            if grille[index] == 0:
                buttons[i][j].config(text="", bg="SystemButtonFace")
            else:
                value = grille[index]
                if est_bien_place(grille, taille, i, j):
                    buttons[i][j].config(text=str(value), bg="green", font=("Helvetica", int(font_size.get())))
                else:
                    buttons[i][j].config(text=str(value), bg="SystemButtonFace", font=("Helvetica", int(font_size.get())))

def est_bien_place(grille, taille, ligne, colonne):
    index = ligne * taille + colonne
    if grille[index] != 0:
        return grille[index] == index + 1
    return False

def nouveau_jeu():
    global grille
    grille = creer_grille(TAILLE)
    update_buttons(TAILLE)
    compteur_coups.set(0)

def afficher_message(titre, message):
    global message_label, message_frame
    if message_frame:
        message_frame.destroy()

    message_frame = tk.Frame(root, bd=2, relief="solid")
    message_frame.grid(row=2, column=0, columnspan=TAILLE, pady=10)

    message_label = tk.Label(message_frame, text=message, font=("Helvetica", 12), wraplength=200)
    message_label.pack(padx=10, pady=10)

    if titre == "Comment jouer":
        bouton_ok = tk.Button(message_frame, text="OK", command=lambda: message_frame.destroy())
        bouton_ok.pack(pady=5)

def afficher_regles():
    afficher_message("Comment jouer",
                     "Bienvenue dans le jeu du Taquin !\n\n"
                     "Le but du jeu est de remettre les tuiles dans l'ordre en les faisant glisser.\n"
                     "Cliquez sur les tuiles adjacentes à la case vide pour les déplacer.\n\n"
                     "Utilisez le curseur pour régler la taille de la police.\n"
                     "Cliquez sur 'Nouveau Jeu' pour recommencer.\n\n"
                     "Amusez-vous bien !")

grille = creer_grille(TAILLE)
buttons = [[None for _ in range(TAILLE)] for _ in range(TAILLE)]

root = tk.Tk()
root.title("Jeu du Taquin")

font_size = tk.IntVar(value=17)

def changer_taille_police(valeur):
    try:
        update_buttons(TAILLE)
    except ValueError:
        print("Valeur de taille de police invalide.")

police_label = tk.Label(root, text="Taille de la police:")
police_label.grid(row=0, column=TAILLE, padx=10)
police_slider = tk.Scale(root, from_=8, to=31, orient=tk.HORIZONTAL, variable=font_size, command=changer_taille_police)
police_slider.grid(row=1, column=TAILLE, padx=10, pady=5)

button_size = 60
for i in range(TAILLE):
    for j in range(TAILLE):
        button = tk.Button(root, text="", width=button_size//5, height=button_size//10,
                           command=lambda row=i, col=j: deplacer_piece(grille, TAILLE, row, col),
                           font=("Helvetica", int(font_size.get())))
        button.grid(row=i+2, column=j, padx=5, pady=5)
        buttons[i][j] = button

compteur_coups = tk.IntVar(value=0)
compteur_label = tk.Label(root, textvariable=compteur_coups, text="Coups: 0")
compteur_label.grid(row=1, column=0, columnspan=TAILLE, sticky="w")

nouveau_jeu_button = tk.Button(root, text="Nouveau Jeu", command=nouveau_jeu)
nouveau_jeu_button.grid(row=0, column=0, columnspan=TAILLE, sticky="ew")

# Initialisation de message_frame et message_label
message_frame = None
message_label = None

# Menu
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# Menu "Jeu"
jeu_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Jeu", menu=jeu_menu)
jeu_menu.add_command(label="Nouveau Jeu", command=nouveau_jeu)
jeu_menu.add_separator()
jeu_menu.add_command(label="Quitter", command=root.quit)

# Menu "Aide"
aide_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Aide", menu=aide_menu)
aide_menu.add_command(label="Comment jouer", command=afficher_regles)

# Afficher les règles au démarrage
afficher_regles()

update_buttons(TAILLE)

root.mainloop()

import pygame
import sys

def jouer_jeu2(screen, clock, progression, retour_menu):
    running = True
    font = pygame.font.Font(None, 36)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False  # On sort du jeu pour revenir au menu

        screen.fill((100, 100, 255))
        text = font.render("Jeu 2 - Sliperry (appuie sur Échap pour revenir)", True, (255, 255, 255))
        screen.blit(text, (50, 250))

        pygame.display.flip()
        clock.tick(60)

    retour_menu()  # Revenir au menu
