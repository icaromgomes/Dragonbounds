from PPlay.window import*
from PPlay.mouse import*
from PPlay.keyboard import*
from PPlay.sprite import*
import math
import random

def spawn_esqueleto(janela):
    esqueleto_sprites = {
        "andar": Sprite("Imagem_Personagens/esqueleto_inimigo.png"),
        "ataque": Sprite("Imagem_Personagens/esqueleto_ataque.png")
    }
    
    esqueleto_sprites["estado"] = "andar"
    esqueleto_sprites["tempo_carregando"] = 0.0
    esqueleto_sprites["cooldown_ataque"] = 0.0

    # Definição dos 3 pontos fixos (Ajuste os valores de X e Y se necessário para encaixar na sua resolução)
    ponto_1 = (janela.width - 280, 10)                        # Fim Superior Direito
    ponto_2 = (170, janela.height - 80)                        # Fim Inferior Esquerdo
    ponto_3 = (janela.width - 60, int(janela.height * 0.45))  # Fim Lateral Direito (ruínas)

    # Sorteia qual dos 3 pontos vai usar
    ponto_escolhido = random.choice([ponto_1, ponto_2, ponto_3])
    x, y = ponto_escolhido

    # Define a posição inicial em ambos os sprites
    esqueleto_sprites["andar"].set_position(x, y)
    esqueleto_sprites["ataque"].set_position(x, y)
    
    return esqueleto_sprites
        
        
def movimentacao_inimigo(inimigos, player, dt, lista_obstaculos):
    vel = 150 * dt
    
    for esqueleto in inimigos:
        if isinstance(esqueleto, dict):
            estado_atual = esqueleto["estado"]
            sprite_esqueleto_atual = esqueleto[estado_atual]
        else:
            sprite_esqueleto_atual = esqueleto
        
        # Só tenta mover se NÃO estiver colado no player atacando
        if not sprite_esqueleto_atual.collided(player):
            # Guarda a posição anterior de ambos os eixos antes de mover
            pos_anterior_x = sprite_esqueleto_atual.x
            pos_anterior_y = sprite_esqueleto_atual.y

            dx = player.x - sprite_esqueleto_atual.x
            dy = player.y - sprite_esqueleto_atual.y
            distancia = math.sqrt(dx ** 2 + dy ** 2)

            if distancia > 0:
                # Calcula o quanto ele deveria andar
                novo_x = sprite_esqueleto_atual.x + (dx / distancia) * vel
                novo_y = sprite_esqueleto_atual.y + (dy / distancia) * vel
                
                if isinstance(esqueleto, dict):
                    # --- TESTE NO EIXO X ---
                    esqueleto["andar"].x = novo_x
                    esqueleto["ataque"].x = novo_x
                    for obstaculo in lista_obstaculos:
                        if sprite_esqueleto_atual.collided(obstaculo):
                            # Colidiu no X? Cancela o movimento do X
                            esqueleto["andar"].x = pos_anterior_x
                            esqueleto["ataque"].x = pos_anterior_x
                            break

                    # --- TESTE NO EIXO Y ---
                    esqueleto["andar"].y = novo_y
                    esqueleto["ataque"].y = novo_y
                    for obstaculo in lista_obstaculos:
                        if sprite_esqueleto_atual.collided(obstaculo):
                            # Colidiu no Y? Cancela o movimento do Y
                            esqueleto["andar"].y = pos_anterior_y
                            esqueleto["ataque"].y = pos_anterior_y
                            break
                else:
                    # Caso legado (Sprite puro)
                    esqueleto.x = novo_x
                    esqueleto.y = novo_y


def movimentacao_player(personagem, dt, janela, teclado, lista_obstaculos):
    vel_x = 200 * dt
    vel_y = 200 * dt
    andando = False

    # Guarda a posição atual antes de mover
    pos_anterior_x = personagem.x
    pos_anterior_y = personagem.y

    # Movimento para Direita
    if teclado.key_pressed("right") and (personagem.x + personagem.width) <= janela.width:
        personagem.x += vel_x
        andando = True
        # Se colidir com a floresta, desfaz o movimento desse eixo
        for obstaculo in lista_obstaculos:
            if personagem.collided(obstaculo):
                personagem.x = pos_anterior_x
                break

    # Movimento para Esquerda
    if teclado.key_pressed("left") and personagem.x > 0:
        personagem.x -= vel_x
        andando = True
        for obstaculo in lista_obstaculos:
            if personagem.collided(obstaculo):
                personagem.x = pos_anterior_x
                break

    # Movimento para Baixo
    if teclado.key_pressed("DOWN") and (personagem.y + personagem.height) <= janela.height:
        personagem.y += vel_y
        andando = True
        for obstaculo in lista_obstaculos:
            if personagem.collided(obstaculo):
                personagem.y = pos_anterior_y
                break

    # Movimento para Cima
    if teclado.key_pressed("UP") and personagem.y > 0:
        personagem.y -= vel_y
        andando = True
        for obstaculo in lista_obstaculos:
            if personagem.collided(obstaculo):
                personagem.y = pos_anterior_y
                break

    return andando

    
