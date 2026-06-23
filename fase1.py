from PPlay.sprite import*
from PPlay.gameimage import*
from personagens import*
from objetos import *

def executar_fase(janela, teclado, mouse, player_sprites, player_hitbox_ataque, obstaculos_cenario):

    dt = janela.delta_time()
    
    lista_esqueletos = []
    barras_de_hp_inimigos = []
    barras_de_hp_player = inicializar_barra_de_hp_player()
    
    cooldown_spawn_esqueleto = 1.0
    timer_spawn_esqueleto = 0
    limite_inimigos_fase = 1
    inimigos_gerados = 0
    
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

    portal_saida = Sprite("Imagem_Objetos/portal.png")
    portal_ativo = False
    
    # Carrega o fundo da fase aqui dentro
    fundo_mapa = Sprite("Imagem_FUNDO/fundo.png")

    # Loop interno da fase
    while True:
        dt = janela.delta_time()
        
        # O ESC dentro da fase faz voltar para o menu
        if teclado.key_pressed("ESC"):
            return "menu"
        
        # GAME OVER
        if not barras_de_hp_player:
            return "gameover"

        # Desenha o plano de fundo
        fundo_mapa.draw()

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
            andando = movimentacao_player_fase1(sprite_atual, dt, janela, teclado, obstaculos_cenario)
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

        # 4. SPAWN DE INIMIGOS
        timer_spawn_esqueleto += dt
        if timer_spawn_esqueleto >= cooldown_spawn_esqueleto and inimigos_gerados < limite_inimigos_fase:
            esqueleto = spawn_esqueleto(janela)
            lista_esqueletos.append(esqueleto)
            
            bloco_hp = Sprite("Imagem_Objetos/barra_de_hp_menor.png")
            barras_de_hp_inimigos.append([bloco_hp]) 
            
            inimigos_gerados += 1
            timer_spawn_esqueleto = 0

        # 5. MOVIMENTAÇÃO E DESENHO DOS ESQUELETOS
        movimentacao_inimigo(lista_esqueletos, sprite_atual, dt, obstaculos_cenario)
        
        for i in range(len(lista_esqueletos)):
            esqueleto = lista_esqueletos[i]
            sprite_esqueleto_atual = esqueleto[esqueleto["estado"]]
            sprite_esqueleto_atual.draw() 
            
            sublista_hp = barras_de_hp_inimigos[i]
            for j in range(len(sublista_hp)):
                bloco = sublista_hp[j]
                bloco.x = sprite_esqueleto_atual.x + (j * (bloco.width + 2))
                bloco.y = sprite_esqueleto_atual.y + sprite_esqueleto_atual.height + 4
                bloco.draw()
        
        # LÓGICA DE FIM DA FASE (PORTAL)
        if inimigos_gerados >= limite_inimigos_fase and len(lista_esqueletos) == 0:
            portal_ativo = True
            pos_x = 650
            pos_y = 20
            portal_saida.set_position(pos_x, pos_y)
            portal_saida.draw()
            
            if sprite_atual.collided(portal_saida):
                return "fase final"  # Sai da função e limpa tudo automaticamente

        # 6. LÓGICA DE DANO NO INIMIGO
        if estado_player == "ataque" and cronometro_sprite_ataque == dt:
            for i in range(len(lista_esqueletos) - 1, -1, -1):
                esqueleto = lista_esqueletos[i]
                sprite_esqueleto_atual = esqueleto[esqueleto["estado"]]
                
                if esqueleto is not None and i < len(barras_de_hp_inimigos):
                    if sprite_esqueleto_atual.collided(player_hitbox_ataque):
                        if len(barras_de_hp_inimigos[i]) > 0:
                            barras_de_hp_inimigos[i].pop()

        # Remover inimigos mortos
        for i in range(len(lista_esqueletos) - 1, -1, -1):
            if i < len(barras_de_hp_inimigos) and len(barras_de_hp_inimigos[i]) == 0:
                del lista_esqueletos[i]          
                del barras_de_hp_inimigos[i]

        # 7. LÓGICA DE DANO NO PLAYER
        tempo_para_esqueleto_atacar = 1.0  
        tempo_cooldown_esqueleto = 3.0     
        
        for esqueleto in lista_esqueletos:
            if esqueleto is not None:
                sprite_esqueleto_atual = esqueleto[esqueleto["estado"]]
                
                if esqueleto["cooldown_ataque"] > 0:
                    esqueleto["cooldown_ataque"] -= dt
                    esqueleto["tempo_carregando"] = 0.0 
                    esqueleto["estado"] = "andar"
                    continue 

                if invencivel:
                    esqueleto["tempo_carregando"] = 0.0
                    esqueleto["estado"] = "andar"
                    continue

                if sprite_esqueleto_atual.collided(sprite_atual):
                    esqueleto["estado"] = "ataque" 
                    esqueleto["tempo_carregando"] += dt 
                    
                    if esqueleto["tempo_carregando"] >= tempo_para_esqueleto_atacar:
                        if barras_de_hp_player:
                            barras_de_hp_player.pop() 
                            invencivel = True 
                        
                        esqueleto["tempo_carregando"] = 0.0
                        esqueleto["cooldown_ataque"] = tempo_cooldown_esqueleto 
                        esqueleto["estado"] = "andar"
                else:
                    esqueleto["tempo_carregando"] = 0.0
                    esqueleto["estado"] = "andar"

        # 8. SISTEMA DE INVENCIBILIDADE (PISCADA) DO PLAYER
        if invencivel:
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

        if mostra_player:
            player_sprites[estado_player].draw()
            
        janela.update()