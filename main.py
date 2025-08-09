import curses
import threading
import time
import random
from config import Config
from game import iniciar_jogo
from logger import logger

state = {
    "pos_jogador": [Config.ALTURA_ARENA // 2, Config.LARGURA_ARENA // 2],
    "raios": [],
    "itens_vida": [],
    "vidas": 3,
    "pontuacao": 0,
    "jogo_ativo": True
}

lock_pontuacao = threading.Lock()
semaphore_vidas = threading.Semaphore()

def gerar_posicao():
    return (random.randint(0, Config.ALTURA_ARENA - 1),
            random.randint(0, Config.LARGURA_ARENA - 1))

def thread_gerar_raios():
    while state["jogo_ativo"]:
        time.sleep(Config.TEMPO_ENTRE_RAIOS)
        pos = gerar_posicao()
        state["raios"].append(pos)
        logger.info(f"Raio gerado em {pos}")

def thread_gerar_vida():
    while state["jogo_ativo"]:
        time.sleep(Config.TEMPO_ENTRE_VIDAS)
        with semaphore_vidas:
            pos = gerar_posicao()
            state["itens_vida"].append(pos)
            logger.info(f"Item de vida gerado em {pos}")

def thread_cronometro_pontuacao():
    inicio = time.time()
    while state["jogo_ativo"] and (time.time() - inicio < Config.DURACAO_PARTIDA):
        time.sleep(1)
        with lock_pontuacao:
            state["pontuacao"] += 10
            logger.info(f"Pontuação atualizada: {state['pontuacao']}")
    state["jogo_ativo"] = False
    logger.info("Tempo de partida encerrado.")

def main():
    threads = [
        threading.Thread(target=thread_gerar_raios, daemon=True),
        threading.Thread(target=thread_gerar_vida, daemon=True),
        threading.Thread(target=thread_cronometro_pontuacao, daemon=True)
    ]
    for t in threads:
        t.start()
    curses.wrapper(iniciar_jogo, state)

if __name__ == "__main__":
    main()
