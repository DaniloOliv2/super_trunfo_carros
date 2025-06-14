import pygame
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import os

# Dados dos carros
cartas = [
    {
        "nome": "BMW",
        "imagem": "imagens/bmw.png",
        "velocidade": 280,
        "aceleracao": 4.5,
        "potencia": 510,
        "peso": 1700,
    },
    {
        "nome": "Bugatti",
        "imagem": "imagens/bugatti.png",
        "velocidade": 420,
        "aceleracao": 2.4,
        "potencia": 1500,
        "peso": 1800,
    },
    {
        "nome": "Ferrari",
        "imagem": "imagens/ferrari.png",
        "velocidade": 340,
        "aceleracao": 3.0,
        "potencia": 720,
        "peso": 1650,
    },
    {
        "nome": "Lamborghini",
        "imagem": "imagens/lamborghini.png",
        "velocidade": 350,
        "aceleracao": 3.2,
        "potencia": 770,
        "peso": 1550,
    },
    {
        "nome": "Mclaren",
        "imagem": "imagens/mclaren.png",
        "velocidade": 350,
        "aceleracao": 3.0,
        "potencia": 800,
        "peso": 1400,
    },
    {
        "nome": "Porsche",
        "imagem": "imagens/porsche.png",
        "velocidade": 320,
        "aceleracao": 3.2,
        "potencia": 690,
        "peso": 1600,
    },
]

atributos = ["velocidade", "aceleracao", "potencia", "peso"]

# App
app = tk.Tk()
app.title("Super Trunfo - Carros")
app.geometry("800x600")

# Variáveis
placar_jogador = 0
placar_computador = 0
atributos_restantes = []
carta_jogador = None
carta_computador = None

# Frames
frame_menu = tk.Frame(app)
frame_jogo = tk.Frame(app)

# Funções


def mostrar_menu():
    frame_jogo.pack_forget()
    frame_menu.pack(expand=True)


def iniciar_jogo():
    frame_menu.pack_forget()
    frame_jogo.pack(expand=True)
    nova_rodada()


def voltar_ao_menu():
    frame_jogo.pack_forget()
    frame_menu.pack(expand=True)


def carregar_imagem(caminho, tamanho=(200, 150)):
    imagem = Image.open(caminho)
    imagem = imagem.resize(tamanho)
    return ImageTk.PhotoImage(imagem)


def exibir_carta(frame, carta, oculta=False):
    for widget in frame.winfo_children():
        widget.destroy()

    if oculta:
        imagem = carregar_imagem("imagens/oculta.png")
        tk.Label(frame, image=imagem).pack()
        frame.imagem = imagem
        tk.Label(frame, text="Carta Oculta", font=(
            "Arial", 14, "bold")).pack(pady=5)
        return

    imagem = carregar_imagem(carta["imagem"])
    tk.Label(frame, image=imagem).pack()
    frame.imagem = imagem

    tk.Label(frame, text=carta["nome"], font=(
        "Arial", 14, "bold")).pack(pady=5)
    tk.Label(frame, text=f"Velocidade: {carta['velocidade']}").pack()
    tk.Label(frame, text=f"Aceleração: {carta['aceleracao']}").pack()
    tk.Label(frame, text=f"Potência: {carta['potencia']}").pack()
    tk.Label(frame, text=f"Peso: {carta['peso']}").pack()


def nova_rodada():
    global carta_jogador, carta_computador, atributos_restantes

    carta_jogador = random.choice(cartas)
    carta_computador = random.choice([c for c in cartas if c != carta_jogador])

    atributos_restantes = atributos.copy()

    exibir_carta(frame_carta_jogador, carta_jogador)
    exibir_carta(frame_carta_computador, carta_computador, oculta=True)

    atualizar_placar()

    for botao in botoes_atributos:
        botao.config(state=tk.NORMAL)


def comparar(atributo):
    global placar_jogador, placar_computador, atributos_restantes

    val_jogador = carta_jogador[atributo]
    val_computador = carta_computador[atributo]

    if atributo == "aceleracao":
        vencedor = "jogador" if val_jogador < val_computador else "computador" if val_jogador > val_computador else "empate"
    else:
        vencedor = "jogador" if val_jogador > val_computador else "computador" if val_jogador < val_computador else "empate"

    if vencedor == "jogador":
        placar_jogador += 1
    elif vencedor == "computador":
        placar_computador += 1

    atualizar_placar()
    atributos_restantes.remove(atributo)

    if not atributos_restantes:
        exibir_carta(frame_carta_computador, carta_computador)
        if placar_jogador > placar_computador:
            messagebox.showinfo("Resultado da Rodada",
                                "✅ Você venceu a rodada!")
        elif placar_computador > placar_jogador:
            messagebox.showinfo("Resultado da Rodada",
                                "❌ Você perdeu a rodada!")
        else:
            messagebox.showinfo("Resultado da Rodada", "⚖️ Empate na rodada!")
    else:
        messagebox.showinfo(
            "Resultado", f"{atributo.capitalize()} comparado! Continue...")

    for botao in botoes_atributos:
        if botao["text"].lower() == atributo:
            botao.config(state=tk.DISABLED)


def atualizar_placar():
    label_placar.config(
        text=f"Jogador: {placar_jogador} | Computador: {placar_computador}")


# =====================
# Frame Menu
# =====================
label_titulo = tk.Label(
    frame_menu, text="Super Trunfo - Carros", font=("Arial", 24, "bold"))
label_titulo.pack(pady=30)

tk.Button(frame_menu, text="Jogar", width=20,
          command=iniciar_jogo).pack(pady=10)
tk.Button(frame_menu, text="Instruções", width=20, command=lambda: messagebox.showinfo("Instruções",
                                                                                       """✔ Clique em Jogar.
✔ Compare os atributos dos carros.
✔ Quem tiver mais pontos vence a rodada.
✔ Ao final de comparar todos os atributos, aparece o resultado final.""")).pack(pady=10)
tk.Button(frame_menu, text="Sair", width=20, command=app.quit).pack(pady=10)

# =====================
# Frame Jogo
# =====================
label_placar = tk.Label(frame_jogo, text="", font=("Arial", 14))
label_placar.pack(pady=5)

frame_botoes_topo = tk.Frame(frame_jogo)
frame_botoes_topo.pack()

tk.Button(frame_botoes_topo, text="Nova Rodada",
          command=nova_rodada).pack(side=tk.LEFT, padx=5)
tk.Button(frame_botoes_topo, text="Voltar ao Menu",
          command=voltar_ao_menu).pack(side=tk.LEFT, padx=5)

frame_cartas = tk.Frame(frame_jogo)
frame_cartas.pack(pady=20)

frame_carta_jogador = tk.Frame(
    frame_cartas, bd=2, relief="solid", padx=10, pady=10)
frame_carta_jogador.pack(side=tk.LEFT, padx=20)

frame_carta_computador = tk.Frame(
    frame_cartas, bd=2, relief="solid", padx=10, pady=10)
frame_carta_computador.pack(side=tk.LEFT, padx=20)

frame_botoes_atributos = tk.Frame(frame_jogo)
frame_botoes_atributos.pack(pady=10)

botoes_atributos = []
for atributo in atributos:
    btn = tk.Button(frame_botoes_atributos, text=atributo.capitalize(
    ), width=10, command=lambda a=atributo: comparar(a))
    btn.pack(side=tk.LEFT, padx=5)
    botoes_atributos.append(btn)

# Inicia no menu
mostrar_menu()

app.mainloop()
