from PPlay.window import *
from PPlay.gameimage import *
from PPlay.mouse import *
from PPlay.sprite import *
from PPlay.keyboard import *
from personagens import*
from objetos import *
from fase1 import *
from fase_final import *
from janela import *

janela = incializar_janela()
player_hitbox_ataque = Sprite("Imagem_Personagens/cavaleiro_hitbox_ATAQUE.png")

fundo_historia = Sprite("Imagem_FUNDO/FundoHistoria.png")
conti = Sprite("Imagem_Objetos/continue.png")
conti.set_position(janela.width/2 - conti.width/2, janela.height - conti.height)

obstaculos_cenario = inicializar_colisoes_mapa(janela)
teclado = Keyboard()
mouse = Mouse()

tela = "menu"
pressionado_mouse = False
pressionado_teclado = False

# Menu
fundoMenu = GameImage("Imagem_FUNDO/FundoMenu.png")
start = Sprite("Imagem_Objetos/button_start.png")
start.set_position(janela.width/2 - start.width/2, janela.height - janela.height/4)

player_sprites = {}

# Escolha de personagens (Agrupados em um dicionário para a função do mouse)
fundoPersonagem = GameImage("Imagem_FUNDO/FundoPersonagens.png")

fundoVictoria = GameImage("Imagem_FUNDO/fundoVictoria.png")

previews_personagens = {
    "arqueira": Sprite("Imagem_Personagens/arqueira_grande.png"),
    "anao": Sprite("Imagem_Personagens/anao_grande.png"),
    "cavaleiro": Sprite("Imagem_Personagens/cavaleiro_grande.png"),
    "maga": Sprite("Imagem_Personagens/maga_grande.png")
}

previews_personagens["arqueira"].set_position(110, janela.height/2 - previews_personagens["arqueira"].height/2 + 20)
previews_personagens["anao"].set_position(250 , janela.height/2 - previews_personagens["anao"].height/2 + 20)
previews_personagens["maga"].set_position(540, janela.height/2 - previews_personagens["maga"].height/2 + 20)
previews_personagens["cavaleiro"].set_position(750, janela.height/2 - previews_personagens["cavaleiro"].height/2 - 15)


while True:
    # 1. PROCESSAMENTO DE INPUT MODULARIZADO (Teclado e Mouse)
    tela, pressionado_teclado = verificar_botoes_teclado(teclado, tela, pressionado_teclado)
    
    # Reseta a trava do teclado se soltar a tecla ESC (antigo 'if not teclado.key_pressed...')
    if not teclado.key_pressed("ESC") and not mouse.is_button_pressed(1):
        pressionado_teclado = False

    tela, pressionado_mouse, personagem_escolhido = verificar_botoes_mouse(
        mouse, tela, pressionado_mouse, start, conti, previews_personagens
    )

    # 2. SELEÇÃO E CARREGAMENTO DO PERSONAGEM (Disparado pelo clique do mouse)
    if personagem_escolhido:
        player_sprites = {
            "parado": Sprite(f"Imagem_Personagens/{personagem_escolhido}_parado.png"),
            "andar": Sprite(f"Imagem_Personagens/{personagem_escolhido}_andar.png"),
            "ataque": Sprite(f"Imagem_Personagens/{personagem_escolhido}_ataque.png")
        }
        
        for spr in player_sprites.values():
            spr.set_position((janela.width - spr.width)/2, (janela.height - spr.height)/2)
        
        player_hitbox_ataque.set_position((janela.width - player_sprites["parado"].width)/2, (janela.height - player_sprites["parado"].height)/2)
        
        # Inicia a fase e espera o retorno dela
        tela = executar_fase(janela, teclado, mouse, player_sprites, player_hitbox_ataque, obstaculos_cenario)

    # 3. RENDERIZAÇÃO DOS MENUS
    if tela == "menu":
        fundoMenu.draw()
        start.draw()
    
    elif tela == "historia":
        fundo_historia.draw()
        conti.draw()

    elif tela == "personagens":
        fundoPersonagem.draw()
        for p_sprite in previews_personagens.values():
            p_sprite.draw()

    elif tela == "fase final":

        # Inicializa os sprites do dragão, para não ter que inicializar antes do game loop
        dragao_sprites = {
        "andar": Sprite("Imagem_Personagens/dragao_andando.png"),
        "parado": Sprite("Imagem_Personagens/dragao_parado.png"),
        "ataque": Sprite("Imagem_Personagens/dragao_ataque.png") 
    }
        for spr in dragao_sprites.values():
            spr.set_position((janela.width - spr.width)/2, 0)

        # Inicia a fase final e espera o retorno dela
        tela = executar_fase_final(janela, teclado, player_sprites, player_hitbox_ataque, dragao_sprites, obstaculos_cenario)

    elif tela == "victoria":
        fundoVictoria.draw()

        if teclado.key_pressed("ESC"):
            tela = "menu"



    janela.update()