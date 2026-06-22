from PPlay.window import*
from PPlay.gameimage import*
from PPlay.mouse import*
from PPlay.sprite import*
from PPlay.keyboard import*
from personagens import*
from objetos import*
import math

def ataque_bola_de_fogo(dragao):
    bolas_de_fogo = []
    angulo = math.radians(225)
    for _ in range(3):
        bola = Sprite("Imagem_Objetos/bola_de_fogo1.png")
        bola.set_position(dragao.x + (dragao.width - bola.width)/2, dragao.y + dragao.height)
        dir_x = math.cos(angulo)
        dir_y = -math.sin(angulo)
        bolas_de_fogo.append({
            "item": bola,
            "dir_x": dir_x,
            "dir_y": dir_y
        })
        angulo += math.radians(45)

    return bolas_de_fogo

def movimentacao_bola_fogo(bolas_de_fogo, dt):

    vel = 300
    for item in bolas_de_fogo:
        bola = item["item"]
        bola.x += item["dir_x"] * vel * dt
        bola.y += item["dir_y"] * vel * dt

def colisao_bola_fogo_personagem(bolas_de_fogo, sprite_atual, barras_de_hp_player):
    for bola in bolas_de_fogo[:]:
        if bola["item"].collided(sprite_atual):
            bolas_de_fogo.remove(bola)
            if barras_de_hp_player:
                barras_de_hp_player.pop()
                return True


def executar_fase_final(janela, teclado, player_sprites, player_hitbox_ataque, dragao_sprites, obstaculos_cenario):

    # VARIÁVEIS RELACIONADAS AO PLAYER
    barras_de_hp_player = inicializar_barra_de_hp_player()
    estado_player = "parado" 
    tempo_ataque = 0.3
    cronometro_sprite_ataque = 0
    cooldown_ataque = 1.0
    cronometro_ataque = 0
    pode_atacar = True

    invencivel = False
    tempo_pisca = 2.0
    cronometro_pisca = 0
    cronometro_mostra = 0
    mostra_player = True

    # VARIÁVEIS RELACIONADAS AO DRAGÃO
    estado_dragao = "parado"
    direcao_dragao = 1
    cronometro_dragao_ataque = 0
    tempo_dragao_ataque = 0.6
    cronometro_dragao_parado = 0
    tempo_dragao_parado = 1.0
    cronometro_dragao_andando = 0
    tempo_dragao_andando = 2.0
    bolas_de_fogo = []
    vel_dragao = 100

    barras_de_hp_dragao = []
    for _ in range(5):
        barras_de_hp_dragao.append(Sprite("Imagem_Objetos/barra_de_hp_menor.png"))

    # Variáveis de Ataque Físico/Colisão do Dragão com o Player
    tempo_para_dragao_atacar = 1.0
    tempo_cooldown_dragao_colisao = 2.0
    cronometro_colisao_dragao = 0
    cooldown_ataque_fisico_dragao = 0

    fundo_mapa_final = Sprite("Imagem_FUNDO/fase_final.png")

    while True:
        dt = janela.delta_time()
        fundo_mapa_final.draw()
        if teclado.key_pressed("ESC"):
            return "menu"        
        if barras_de_hp_player == []:
            return "menu"

        # ----- PLAYER -------
        # 1. ESTADO E SPRITE DO PLAYER
        sprite_atual = player_sprites[estado_player]

        # 2. INPUT DE ATAQUE DO PLAYER
        if teclado.key_pressed("space") and pode_atacar:
            estado_player = "ataque"
            pode_atacar = False
            cronometro_ataque = 0
            cronometro_sprite_ataque = 0 

        if not pode_atacar:
            cronometro_ataque += dt
            if cronometro_ataque >= cooldown_ataque:
                pode_atacar = True

        if estado_player == "ataque":
            cronometro_sprite_ataque += dt
            if cronometro_sprite_ataque >= tempo_ataque:
                estado_player = "parado"

        # 3. MOVIMENTAÇÃO DO PLAYER
        if estado_player != "ataque":
            # ADICIONADO: obstaculos_cenario no final da chamada
            andando = movimentacao_player(sprite_atual, dt, janela, teclado, obstaculos_cenario)
            if andando:
                estado_player = "andar"
            else:
                estado_player = "parado"

        # Sincroniza posições do player
        for spr in player_sprites.values():
            spr.x = sprite_atual.x
            spr.y = sprite_atual.y
        
        player_hitbox_ataque.x = sprite_atual.x
        player_hitbox_ataque.y = sprite_atual.y

        mover_barra_de_hp_player(barras_de_hp_player, sprite_atual)

        # 8. SISTEMA DE INVENCIBILIDADE (PISCADA) DO PLAYER
        if invencivel:
            for bola_dict in bolas_de_fogo[:]:
                if bola_dict["item"].collided(sprite_atual):
                    bolas_de_fogo.remove(bola_dict)
            cronometro_pisca += dt
            if cronometro_pisca >= tempo_pisca:
                cronometro_pisca = 0
                invencivel = False
                mostra_player = True
                continue

            cronometro_mostra += dt
            if cronometro_mostra >= 0.1:
                mostra_player = not mostra_player
                cronometro_mostra = 0

        # ----- DRAGAO -----

        # 1. ESTADO E SPRITE DO DRAGÃO
        dragao_atual = dragao_sprites[estado_dragao]
        for spr in dragao_sprites.values():
            spr.set_position(dragao_atual.x, dragao_atual.y)

        # 2. MUDANÇAS DE COMPORTAMENTO DO DRAGÃO
        if estado_dragao == "parado":
            cronometro_dragao_parado += dt
            #. Iniciar o ataque do dragao
            if cronometro_dragao_parado >= tempo_dragao_parado:
                bolas_de_fogo.extend(ataque_bola_de_fogo(dragao_atual))
                cronometro_dragao_parado = 0
                estado_dragao = "ataque"

        if estado_dragao == "ataque":
            cronometro_dragao_ataque += dt
            #. Tempo de ataque estourou, o dragao pode comecar a andar
            if cronometro_dragao_ataque >= tempo_dragao_ataque:
                cronometro_dragao_ataque = 0
                estado_dragao = "andar"

        if estado_dragao == "andar":
            # Movimenta o dragão para os lados
            dragao_atual.x += vel_dragao * direcao_dragao * dt

            # Se bater nas bordas da janela, inverte a direção
            if dragao_atual.x >= janela.width - dragao_atual.width or dragao_atual.x <= 0:
                direcao_dragao *= -1

            cronometro_dragao_andando += dt
            if cronometro_dragao_andando >= tempo_dragao_andando:
                # Ele já andou o suficiente. Para novamente para recomeçar o ciclo
                cronometro_dragao_andando = 0
                estado_dragao = "parado"

        for bola_dict in bolas_de_fogo[:]:
            bola_sprite = bola_dict["item"]
            bola_sprite.draw()

            if bola_sprite.x + bola_sprite.width < 0 or bola_sprite.y > janela.height or bola_sprite.x > janela.width:
                bolas_de_fogo.remove(bola_dict)
                
        if not invencivel:
            invencivel = colisao_bola_fogo_personagem(bolas_de_fogo, sprite_atual, barras_de_hp_player)
        if mostra_player:
            player_sprites[estado_player].draw()            
        dragao_atual.draw()

        # Atualizamos a posição e desenhamos as barras LOGO ABAIXO dele
        distancia_x = 0
        for bloco in barras_de_hp_dragao:
            bloco.x = dragao_atual.x + distancia_x
            # 'dragao_atual.y + dragao_atual.height' coloca o bloco exatamente na base do dragão.
            # Somar + 4 deixa uma pequena margem de respiro abaixo dele.
            bloco.y = dragao_atual.y + dragao_atual.height + 4 
            distancia_x += bloco.width + 2
            bloco.draw()

        # [LÓGICA DE DANO NO DRAGÃO]
        if estado_player == "ataque" and cronometro_sprite_ataque == dt:
            if dragao_atual.collided(player_hitbox_ataque):
                if len(barras_de_hp_dragao) > 0:
                    barras_de_hp_dragao.pop()

        # LÓGICA DE DANO CONTRA O PLAYER (Colisão corporal com o Dragão)
        if cooldown_ataque_fisico_dragao > 0:
            cooldown_ataque_fisico_dragao -= dt
            cronometro_colisao_dragao = 0.0
        elif not invencivel and dragao_atual.collided(sprite_atual):
            cronometro_colisao_dragao += dt
            if cronometro_colisao_dragao >= tempo_para_dragao_atacar:
                if barras_de_hp_player:
                    barras_de_hp_player.pop()
                    invencivel = True
                cronometro_colisao_dragao = 0.0
                cooldown_ataque_fisico_dragao = tempo_cooldown_dragao_colisao
        else:
            cronometro_colisao_dragao = 0.0
        movimentacao_bola_fogo(bolas_de_fogo, dt)

        if not barras_de_hp_dragao:
            return "victoria"

        janela.update()





        
        