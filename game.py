import curses
import time
from config import Config
from logger import logger

def desenhar_arena(stdscr):
    for y in range(Config.ALTURA_ARENA):
        for x in range(Config.LARGURA_ARENA):
            stdscr.addstr(y, x, ".")

def desenhar_jogador(stdscr, state):
    stdscr.addstr(*state["pos_jogador"], "@")

def desenhar_raios(stdscr, state):
    for r in state["raios"]:
        stdscr.addstr(*r, "*")

def desenhar_itens_vida(stdscr, state):
    for item in state["itens_vida"]:
        stdscr.addstr(*item, "+")

def mostrar_status(stdscr, state):
    stdscr.addstr(Config.ALTURA_ARENA + 1, 0, f"Vidas: {state['vidas']}")
    stdscr.addstr(Config.ALTURA_ARENA + 2, 0, f"Pontuação: {state['pontuacao']}")

def mover_jogador(tecla, state):
    y, x = state["pos_jogador"]
    if tecla == curses.KEY_UP and y > 0:
        state["pos_jogador"][0] -= 1
    elif tecla == curses.KEY_DOWN and y < Config.ALTURA_ARENA - 1:
        state["pos_jogador"][0] += 1
    elif tecla == curses.KEY_LEFT and x > 0:
        state["pos_jogador"][1] -= 1
    elif tecla == curses.KEY_RIGHT and x < Config.LARGURA_ARENA - 1:
        state["pos_jogador"][1] += 1

def verificar_colisoes(state):
    pos = tuple(state["pos_jogador"])
    if pos in state["raios"]:
        state["vidas"] -= 1
        logger.warning(f"Colisão com raio em {pos}. Vidas restantes: {state['vidas']}")
        state["raios"].clear()
        if state["vidas"] <= 0:
            logger.error("Jogador ficou sem vidas. Encerrando jogo.")
            state["jogo_ativo"] = False

    if pos in state["itens_vida"]:
        state["vidas"] += 1
        state["itens_vida"].remove(pos)
        logger.info(f"Item de vida coletado em {pos}. Vidas: {state['vidas']}")

def iniciar_jogo(stdscr, state):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(200)

    while state["jogo_ativo"]:
        stdscr.clear()
        desenhar_arena(stdscr)
        desenhar_jogador(stdscr, state)
        desenhar_raios(stdscr, state)
        desenhar_itens_vida(stdscr, state)
        mostrar_status(stdscr, state)

        tecla = stdscr.getch()
        mover_jogador(tecla, state)
        verificar_colisoes(state)

        stdscr.refresh()

    stdscr.clear()
    stdscr.addstr(Config.ALTURA_ARENA // 2, Config.LARGURA_ARENA // 2 - 5, "GAME OVER")
    stdscr.refresh()
    time.sleep(2)
