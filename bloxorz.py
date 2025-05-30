print("Bem vindos ao Bloxorz! Você deseja iniciar um jogo?")
resposta = input("Digite sua resposta: ").strip().lower()[0]

import tkinter as tk
class BloxorzGUI:
    def __init__(self, levels):
        self.levels = levels
        self.level_index = 0
        self.max_moves = 20
        self.cell_size = 40
        self.load_level()

        self.root = tk.Tk()
        self.root.title("Bloxorz")

        w = len(self.board[0]) * self.cell_size
        h = len(self.board) * self.cell_size + 40
        self.canvas = tk.Canvas(self.root, width=w, height=h)
        self.canvas.pack()

        self.info_label = tk.Label(self.root, text="", font=("Arial", 14))
        self.info_label.pack()

        self.root.bind("<Key>", self.on_key_press)
        self.running = True

        self.draw_board()
        self.update_info()

        self.root.mainloop()

    def load_level(self):
        level = self.levels[self.level_index]
        self.board = [row[:] for row in level["board"]]
        self.goal = level["goal"]
        self.pos = level["start"]
        self.moves = 0

    def draw_board(self):
        self.canvas.delete("all")
        rows = len(self.board)
        cols = len(self.board[0])
        for r in range(rows):
            for c in range(cols):
                x1 = c * self.cell_size
                y1 = r * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                color = "lightgrey" if self.board[r][c] == ' ' else "black"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="grey")

        # Desenhar objetivo
        gr, gc = self.goal
        x = gc * self.cell_size + self.cell_size // 2
        y = gr * self.cell_size + self.cell_size // 2
        r = self.cell_size // 4
        self.canvas.create_oval(x - r, y - r, x + r, y + r, fill="green")

        # Desenhar bloco
        if self.pos[0] == self.pos[1]:
            # Em pé: desenha um quadrado maior e de outra cor
            r, c = self.pos[0]
            x1 = c * self.cell_size + 2
            y1 = r * self.cell_size + 2
            x2 = x1 + self.cell_size - 4
            y2 = y1 + self.cell_size - 4
            self.canvas.create_rectangle(x1, y1, x2, y2, fill="purple", outline="black")
        else:
            # Deitado: desenha dois quadrados menores e de outra cor
            for (r, c) in self.pos:
                x1 = c * self.cell_size + 8
                y1 = r * self.cell_size + 8
                x2 = x1 + self.cell_size - 16
                y2 = y1 + self.cell_size - 16
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="blue", outline="black")

    def update_info(self):
        self.info_label.config(text=f"Fase: {self.level_index + 1} | Movimentos: {self.moves}/{self.max_moves}")

    def on_key_press(self, event):
        if not self.running:
            return

        key = event.keysym.lower()
        if key in ['w', 'a', 's', 'd']:
            self.move(key)
            self.draw_board()
            self.update_info()
        else:
            print("Use W A S D para mover.")

    def move(self, direction):
        r1, c1 = self.pos[0]
        r2, c2 = self.pos[1]

        if self.pos[0] == self.pos[1]:  # em pé
            r, c = self.pos[0]
            if direction == 'a':
                new = [(r, c - 2), (r, c - 1)]
            elif direction == 'd':
                new = [(r, c + 1), (r, c + 2)]
            elif direction == 'w':
                new = [(r - 2, c), (r - 1, c)]
            elif direction == 's':
                new = [(r + 1, c), (r + 2, c)]
            else:
                return
        elif r1 == r2:  # deitado horizontal
            c1, c2 = sorted([c1, c2])
            if direction == 'a':
                # Move para a esquerda, bloco fica em pé
                new = [(r1, c1 - 1), (r1, c1 - 1)]
            elif direction == 'd':
                # Move para a direita, bloco fica em pé
                new = [(r1, c2 + 1), (r1, c2 + 1)]
            elif direction == 'w':
                new = [(r1 - 1, c1), (r2 - 1, c2)]
            elif direction == 's':
                new = [(r1 + 1, c1), (r2 + 1, c2)]
            else:
                return
        elif c1 == c2:  # deitado vertical
            r1, r2 = sorted([r1, r2])
            if direction == 'w':
                # Move para cima, bloco fica em pé
                new = [(r1 - 1, c1), (r1 - 1, c1)]
            elif direction == 's':
                # Move para baixo, bloco fica em pé
                new = [(r2 + 1, c1), (r2 + 1, c1)]
            elif direction == 'a':
                new = [(r1, c1 - 1), (r2, c2 - 1)]
            elif direction == 'd':
                new = [(r1, c1 + 1), (r2, c2 + 1)]
            else:
                return

        if all(self.valid(r, c) for r, c in new):
            self.pos = new
            self.moves += 1
            self.check_goal()
            if self.moves >= self.max_moves:
                self.show_message(f" Você excedeu o limite de {self.max_moves} movimentos. Reiniciando fase...")
                self.load_level()
                self.draw_board()
                self.update_info()
        else:
            self.show_message("Movimento inválido!")

    def valid(self, r, c):
        return 0 <= r < len(self.board) and 0 <= c < len(self.board[0]) and self.board[r][c] != '#'

    def check_goal(self):
        if self.pos[0] == self.pos[1] and self.pos[0] == self.goal:
            self.show_message(f" Fase concluída em {self.moves} movimentos!")
            self.next_level()

    def next_level(self):
        self.level_index += 1
        if self.level_index < len(self.levels):
            self.show_message("Próxima fase iniciando...")
            self.load_level()
            self.draw_board()
            self.update_info()
        else:
            self.show_message(" Parabéns! Você completou todas as fases!")
            self.running = False

    def show_message(self, msg):
        self.info_label.config(text=msg)
        self.root.update()
        self.root.after(1500, lambda: self.update_info())

# Lista de fases
levels = [
    {
        "board": [
            list("########"),
            list("#      #"),
            list("#  O   #"),
            list("#      #"),
            list("########")
        ],
        "goal": (2, 2),  # círculo verde no centro
        "start": [(2, 1), (2, 2)]  # bloco deitado horizontal, pode ficar em pé no centro
    },
    {
        "board": [
            list("##########"),
            list("#        #"),
            list("#        #"),
            list("#   O    #"),
            list("#        #"),
            list("#        #"),
            list("##########")
        ],
        "goal": (4, 5),
        "start": [(3, 4), (3, 5)]
    },
    {
        "board": [
            list("###########"),
            list("#         #"),
            list("#         #"),
            list("#    O    #"),
            list("#         #"),
            list("#         #"),
            list("###########")
        ],
        "goal": (3, 5),
        "start": [(1, 4), (1, 5)]
    },
    {
        "board": [
            list("##############"),
            list("#      #     #"),
            list("#      #     #"),
            list("#  O   #     #"),
            list("#      #     #"),
            list("#      #     #"),
            list("##############")
        ],
        "goal": (3, 3),
        "start": [(5, 5), (5, 6)]
    },
    {
        "board": [
            list("#############"),
            list("#           #"),
            list("#    ###    #"),
            list("#    #O#    #"),
            list("#    ###    #"),
            list("#           #"),
            list("#############")
        ],
        "goal": (3, 6),
        "start": [(1, 7), (1, 7)]
    },

    {
        "board": [
            list("#############"),
            list("#   #   #   #"),
            list("#   #   #   #"),
            list("# O #   #   #"),
            list("#   #####   #"),
            list("#           #"),
            list("#############")
        ],
        "goal": (3, 2),
        "start": [(5, 5), (5, 6)]
    },
    {
        "board": [
            list("###############"),
            list("#             #"),
            list("#   #####     #"),
            list("#   #   #     #"),
            list("#   # O #     #"),
            list("#   #####     #"),
            list("#             #"),
            list("###############")
        ],
        "goal": (4, 6), 
        "start": [(1, 5), (1, 5)]
    }
]
  

if __name__ == "__main__":

    if resposta == "s":
        print("iniciando o jogo...")
    else:
        print("Saindo do jogo...")
        exit()

    BloxorzGUI(levels)