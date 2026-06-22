from PPlay.window import*
from PPlay.mouse import*
from PPlay.keyboard import*

def incializar_janela():
    janela = Window(1000,600)
    janela.set_title("Dragonbounds")
    janela.set_background_color([0,0,0])

    return janela

def verificar_botoes_teclado(teclado, tela, pressionado_teclado):
    if teclado.key_pressed("ESC"):
        if not pressionado_teclado:
            if tela == "personagens":
                return "menu", True  
    return tela, pressionado_teclado

def verificar_botoes_mouse(mouse, tela, pressionado_mouse, start, conti, previews):
    personagem_escolhido = None

    if mouse.is_button_pressed(1):
        if not pressionado_mouse:
            if tela == "menu" and mouse.is_over_object(start):
                return "historia", True, None
                    
            elif tela == "historia" and mouse.is_over_object(conti):
                return "personagens", True, None
            
            elif tela == "personagens":
                # previews é um dicionário contendo os sprites de seleção
                if mouse.is_over_object(previews["arqueira"]):
                    personagem_escolhido = "arqueira"
                elif mouse.is_over_object(previews["anao"]):
                    personagem_escolhido = "anao"
                elif mouse.is_over_object(previews["maga"]):
                    personagem_escolhido = "maga"
                elif mouse.is_over_object(previews["cavaleiro"]):
                    personagem_escolhido = "cavaleiro"

                if personagem_escolhido:
                    return "fase", True, personagem_escolhido
            
            return tela, True, None
    else:
        return tela, False, None

    return tela, pressionado_mouse, None