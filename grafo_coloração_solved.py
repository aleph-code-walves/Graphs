import tkinter as tk
from tkinter import messagebox
import random
import math
import networkx as nx
import matplotlib.pyplot as plt

def criar_suduku_board(N):
    # Inicializa o tabuleiro com zeros
    board = [[0] * N for _ in range(N)]

    # Preenche o tabuleiro com valores válidos
    preencher_tabuleiro(board)

    return board

def preencher_tabuleiro(board):
    N = len(board)
    preencher_tab_recv(board, 0, 0, N)

def preencher_tab_recv(board, row, col, N):
    # Verifica se chegou ao final do tabuleiro
    if row == N - 1 and col == N:
        return True

    # Avança para a próxima linha
    if col == N:
        row += 1
        col = 0

    # Se a célula já está preenchida, avança para a próxima célula
    if board[row][col] != 0:
        return preencher_tab_recv(board, row, col + 1, N)

    # Tenta preencher a célula atual
    for num in range(1, N + 1):
        if validador(board, row, col, num):
            board[row][col] = num
            if preencher_tab_recv(board, row, col + 1, N):
                return True
            board[row][col] = 0

    return False

def validador(board, row, col, num):
    N = len(board)

    # Verifica se o número já está na linha
    if num in board[row]:
        return False

    # Verifica se o número já está na coluna
    for i in range(N):
        if board[i][col] == num:
            return False

    # Verifica se o número já está no bloco
    block_size = int(math.sqrt(N))
    start_row, start_col = block_size * (row // block_size), block_size * (col // block_size)
    for i in range(block_size):
        for j in range(block_size):
            if board[i + start_row][j + start_col] == num:
                return False

    return True

def gerar_suduku():
    try:
        N = int(entry_order.get())

        # Verificar se N é uma raiz quadrada perfeita e se está dentro do limite
        if 1 < N <= 16 and (int(N**0.5))**2 == N:
            # Criar tabuleiro Sudoku válido
            sudoku_board = criar_suduku_board(N)

            # Exibir tabuleiro Sudoku em uma nova janela
            display_sudoku_tab(sudoku_board)

            # Criar e exibir o grafo correspondente ao Sudoku =+b Resolver e exibir o Sudoku colorido em uma nova janela
            solved_sudoku_board = resolve_sudoku(sudoku_board)
            display_sudoku_colored(solved_sudoku_board)
            display_sudoku_grafo(sudoku_board)
        else:
            messagebox.showerror("Erro", "A ordem do tabuleiro Sudoku deve ser um número inteiro entre 2 e 16 e ser uma raiz quadrada perfeita.")
    except ValueError:
        messagebox.showerror("Erro", "Insira um valor numérico válido para a ordem do tabuleiro.")

def display_sudoku_tab(board):
    # Criar uma nova janela para exibir o tabuleiro
    board_window = tk.Toplevel(root)
    board_window.title("Tabuleiro Sudoku")

    # Exibir o tabuleiro na nova janela
    N = len(board)
    for i in range(N):
        for j in range(N):
            label = tk.Label(board_window, text=str(board[i][j]), font=("Arial", 10), width=3, height=1, relief="solid")
            label.grid(row=i, column=j, padx=2, pady=2)

def display_sudoku_grafo(board):
    # Criar o grafo correspondente ao Sudoku
    G = create_sudoku_grafo(board)

    # Exibir o grafo
    pos = {(i, j): (j, -i) for i in range(len(board)) for j in range(len(board))}
    nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=700, font_size=10)
    plt.title("Grafo Correspondente ao Sudoku")
    plt.show()

def create_sudoku_grafo(board):
    N = len(board)
    G = nx.Graph()

    # Adicionar vértices ao grafo
    for i in range(N):
        for j in range(N):
            G.add_node((i, j))

    # Adicionar arestas ao grafo
    for i in range(N):
        for j in range(N):
            for k in range(N):
                if k != j:
                    # Adicionar arestas entre vértices na mesma linha
                    G.add_edge((i, j), (i, k))
                    # Adicionar arestas entre vértices na mesma coluna
                    G.add_edge((j, i), (k, i))

    # Adicionar arestas entre vértices no mesmo bloco
    block_size = int(math.sqrt(N))
    for i in range(0, N, block_size):
        for j in range(0, N, block_size):
            for k in range(block_size):
                for l in range(block_size):
                    for m in range(block_size):
                        for n in range(block_size):
                            if (i + k, j + l) != (i + m, j + n):
                                G.add_edge((i + k, j + l), (i + m, j + n))

    return G

def resolve_sudoku(board):
    # Resolver o Sudoku utilizando backtracking
    resolve_board(board)
    return board

def resolve_board(board):
    N = len(board)
    for i in range(N):
        for j in range(N):
            if board[i][j] == 0:
                for num in range(1, N + 1):
                    if validador(board, i, j, num):
                        board[i][j] = num
                        if resolve_board(board):
                            return True
                        board[i][j] = 0
                return False
    return True

def display_sudoku_colored(board):
    # Criar uma nova janela para exibir o Sudoku colorido
    colored_board_window = tk.Toplevel(root)
    colored_board_window.title("Tabuleiro Sudoku Resolvido")

    # Definir cores para os números
    colors = ["red", "blue", "green", "purple", "orange", "brown", "pink", "gray", "yellow", "cyan"]

    # Exibir o Sudoku colorido na nova janela
    N = len(board)
    for i in range(N):
        for j in range(N):
            label = tk.Label(colored_board_window, text=str(board[i][j]), font=("Arial", 10), width=3, height=1, relief="solid")
            if board[i][j] != 0:
                if board[i][j] <= 9:
                    label.config(bg=colors[board[i][j] - 1])
                else:
                    label.config(bg='#{:06x}'.format(random.randint(0, 0xFFFFFF)))  # Gera uma cor aleatória
            label.grid(row=i, column=j, padx=2, pady=2)


if __name__ == '__main__':
    # Criar a janela principal
    root = tk.Tk()
    root.title("Configuração do Tabuleiro Sudoku")

    # Criar e posicionar widgets
    label_order = tk.Label(root, text="Insira a ordem do tabuleiro Sudoku (N):")
    label_order.grid(row=0, column=0)

    entry_order = tk.Entry(root)
    entry_order.grid(row=0, column=1)

    button_generate = tk.Button(root, text="Gerar Tabuleiro", command=gerar_suduku)
    button_generate.grid(row=1, column=0, columnspan=2)

    # Executar o loop principal da interface gráfica
    root.mainloop()
