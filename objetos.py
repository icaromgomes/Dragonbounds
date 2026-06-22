from PPlay.sprite import*
from personagens import*


def inicializar_barra_de_hp_player():
    barra_de_hp = []
    for _ in range(3):
        barra = Sprite("Imagem_Objetos/barra_de_hp_menor.png")
        barra_de_hp.append(barra)

    return barra_de_hp

def inicializar_barra_de_hp_inimigo():
    lista_hp = []
    for i in range(1): 
        bloco = Sprite("Imagem_Objetos/barra_de_hp_menor.png")
        lista_hp.append(bloco)
    return lista_hp


def mover_barra_de_hp_player(barras, personagem):
        
        distancia_x = 0
        for barra in barras:
            barra.y = personagem.y + personagem.height
            barra.x = personagem.x + distancia_x - 12
            distancia_x += barra.width + 2
            barra.draw()

def mover_barra_de_hp_inimigo(barras_inimigos, inimigos):
    for i in range(min(len(barras_inimigos), len(inimigos))):
        inimigo = inimigos[i]
        sublista_hp = barras_inimigos[i]
        distancia_x = 0
        for barra in sublista_hp:
            barra.y = inimigo.y + inimigo.height + 2
            barra.x = inimigo.x + distancia_x
            distancia_x += barra.width + 2
            barra.draw()


from PPlay.sprite import *

from PPlay.sprite import *

def inicializar_colisoes_mapa(janela):
    # NOTA: Vamos criar objetos pequenos e usar as hitboxes originais da imagem (sem esticar no código)
    # Crie uma imagem quadrada de teste (ex: 150x150 ou use a sua própria) para cobrir os cantos.
    
    # BLOCO 1: Canto Superior Esquerdo (Afasta do meio para não travar a Maga)
    b1 = Sprite("Imagem_Objetos/hitbox_invisivel (2).png")
    b1.set_position(0, 0)
    # Forçamos um tamanho fixo menor que NÃO chegue até o meio da tela:
    b1.width = int(janela.width * 0.35)  
    b1.height = int(janela.height * 0.35)

    # BLOCO 2: Canto Inferior Direito
    b2 = Sprite("Imagem_Objetos/hitbox_invisivel (2).png")
    b2.width = int(janela.width * 0.4)
    b2.height = int(janela.height * 0.4)
    b2.set_position(janela.width - b2.width, janela.height - b2.height)

    # BLOCO 3: Canto Inferior Esquerdo (Borda das árvores de baixo)
    b3 = Sprite("Imagem_Objetos/hitbox_invisivel (1).png")
    b3.width = int(janela.width * 0.15)
    b3.height = int(janela.height * 0.30)
    b3.set_position(0, janela.height - b3.height-150)

    # BLOCO 4: Canto Superior Direito (Acima da estrada da direita)
    b4 = Sprite("Imagem_Objetos/hitbox_invisivel (1).png")
    b4.width = int(janela.width * 0.25)
    b4.height = int(janela.height * 0.25)
    b4.set_position(janela.width - b4.width + 40, 0)
    
    b5 = Sprite("Imagem_Objetos/hitbox_invisivel (1).png")
    # Fica encostado na direita (janela.width - b5.width), mas desce cerca de 130 pixels
    b5.set_position(int(janela.width * 0.40), -10)

    return [b1, b2, b3, b4, b5]

    

