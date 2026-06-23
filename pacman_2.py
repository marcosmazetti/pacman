
import pygame #Importa a biblioteca pygame
#código para tornar a classe ElementoJogo abstrata
from abc import ABCMeta, abstractmethod
import random #importa a bilioteca ramdom

#Constantes
AMARELO = (255, 255, 0)
PRETO = (0, 0, 0)
AZUL = (0, 0, 255)
VERMELHO = (255, 0, 0)
#Parte 9
CIANO = (0, 255, 255)
LARANJA = (255, 140, 0)
ROSA = (255, 15, 192)
BRANCO = (255, 255, 255)
VELOCIDADE = 1
ACIMA = 1
ABAIXO = 2
DIREITA = 3
ESQUERDA = 4

pygame.init()

tela = pygame.display.set_mode((800, 600),0) #Tamanho da tela do jogo/surface
font = pygame.font.SysFont("arial", 20, True, False)#fonte usada nos pontos

#Variáveis

#Classe abstrata
class ElementoJogo(metaclass=ABCMeta): #elemento jogo é uma meta classe de abc meta.
#@abstractmethod é usado para evitar erros do compilador, porque os métodos ainda não foram implementados
    @abstractmethod
    def pintar(self,tela):
        pass

    @abstractmethod
    def calcular_regras(self):
        pass

    @abstractmethod
    def processar_eventos(self, eventos):
        pass
#Parte 9
class Movivel(metaclass=ABCMeta):
    @abstractmethod #obriga a classe a implementar o método
    def aceitar_movimento(self):
        pass

    @abstractmethod
    def recusar_movimento(self, direcoes):
        pass

    @abstractmethod
    def esquina(self, direcoes):
        pass







class Cenario(ElementoJogo):#Classe cenario herda a classe elementoJogo, obrigando a implementação dos métodos da mesma
    def __init__(self, tamanho, pac, fan): # tamanho, pac e fan são parâmetros da função init(método construtor)
        self.pacman = pac
        self.fantasma = fan
        #Parte 9
        self.moviveis = [pac, fan]
        self.tamanho = tamanho
        self.pontos = 0
        self.estado = 0 ## Estados possiveis 0-Jogando 1-Pausado 2-GameOver  3-Vitoria
        self.matriz = [
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 1, 1, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2],
            [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
            [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
            [2, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 0, 0, 0, 0, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 0, 0, 0, 0, 0, 0, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 2, 0, 0, 0, 0, 0, 0, 2, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 0, 0, 0, 0, 0, 0, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 2],
            [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
            [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
            [2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 1, 1, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
        ]
    #Parte 9
    def adicionar_movivel(self, obj):
        self.moviveis.append(obj)

    def pintar_pontos(self, tela):#método para exibir os pontos na tela.
        pontos_x = self.tamanho * 30
        pontos_img = font.render("Score {}".format(self.pontos), True, AMARELO)
        tela.blit(pontos_img, (pontos_x, 50)) #Inserindo o texto na tela


    def pintar_linha(self, tela, numero_linha, linha): #método pinta_linha faz o desenho(pintar) da matriz
        for numero_coluna, coluna in enumerate(linha):
            x = numero_coluna * self.tamanho
            y = numero_linha * self.tamanho
            half = self.tamanho // 2
            cor = PRETO
            if coluna == 2:
                cor = AZUL
            pygame.draw.rect(tela, cor, (x, y, self.tamanho, self.tamanho), 0)
            if coluna == 1:
                pygame.draw.circle(tela, AMARELO, (x + half,y + half),self.tamanho // 10)


    def pintar(self, tela):
        if self.estado == 0:
            self.pintar_jogando(tela)
        elif self.estado == 1:
             self.pintar_jogando(tela) #desenho da matriz
             self.pintar_pausado(tela)
        elif self.estado == 2:
            self.pintar_jogando(tela)
            self.pintar_gameover(tela)
        elif self.estado == 3:
            self.pintar_jogando(tela)
            self.pintar_vitoria(tela)

    def pintar_texto_centro(self, tela, texto):
        texto_img = font.render(texto, True, AMARELO)
        texto_x = (tela.get_width() - texto_img.get_width()) // 2
        texto_y = (tela.get_height() - texto_img.get_height()) // 2
        tela.blit(texto_img, (texto_x, texto_y))

    def pintar_vitoria(self, tela):
        self.pintar_texto_centro(tela, "P A R A B E N S  V O C E  V E N C E U  ! ! !")

    def pintar_gameover(self, tela):
        self.pintar_texto_centro(tela, "G A M E   O V E R")

    def pintar_pausado(self, tela):
        self.pintar_texto_centro(tela, "P A U S A D Os")

    """def pintar_pausado(self, tela):
        texto_img = font.render('PAUSADO', True, AMARELO)
        texto_x = (tela.get_width() - texto_img.get_width()) // 2
        texto_y = (tela.get_height() - texto_img.get_height()) // 2
        tela.blit(texto_img, (texto_x, texto_y))"""

    def pintar_jogando(self, tela): #método pintar percorre a matriz e o método pintar_linha pinta a mesma. tela é um parâmetro da função pintar.
        for numero_linha, linha in enumerate(self.matriz): #enumerate retorna o indice e o elemento da matriz:numero_linha(indice) linha(elemento/conteúdo)
            self.pintar_linha(tela, numero_linha, linha)
        self.pintar_pontos(tela)#Pinta os pontos na tela

    def get_direcoes(self, linha, coluna): # verifica quais movimentos são possíveis sem atravessar paredes
        direcoes = [] # Cria uma lista vazia que vai armazenar direções válidas.
        # 2 → representa parede (bloqueio)
        if self.matriz[int(linha - 1)][int(coluna)] != 2:
            direcoes.append(ACIMA)
        if self.matriz[int(linha + 1)][int(coluna)] != 2:
            direcoes.append(ABAIXO)
        if self.matriz[int(linha)][int(coluna - 1)] != 2:
            direcoes.append(ESQUERDA)
        if self.matriz[int(linha)][int(coluna + 1)] != 2:
            direcoes.append(DIREITA)
        return direcoes # Retorna uma lista com todas as direções possíveis.

    def calcular_regras(self):
        if self.estado == 0:
            self.calcular_regras_jogando()
        elif self.estado == 1:
            self.calcular_regras_pausado()
        elif self.estado == 2:
            self.calcular_regras_gameover()

    def calcular_regras_gameover(self):
        pass

    def calcular_regras_pausado(self):
        pass

    def calcular_regras_jogando(self):
        for movivel in self.moviveis:
            lin = int(movivel.linha)
            col = int(movivel.coluna)
            lin_intencao = int(movivel.linha_intencao)
            col_intencao = int(movivel.coluna_intencao)
            direcoes = self.get_direcoes(lin, col)
            if len(direcoes) >= 3:
                movivel.esquina(direcoes)
            if isinstance(movivel, Fantasma) and movivel.linha == self.pacman.linha and \
                    movivel.coluna == self.pacman.coluna:
                self.estado = 2 #Game Over
            else:
                if 0 <= col_intencao < 28 and 0 <= lin_intencao < 29 and self.matriz[lin_intencao][col_intencao] != 2:
                    movivel.aceitar_movimento()
                    #Parte 9
                    if isinstance(movivel, Pacman) and self.matriz[lin][col] == 1:
                        self.pontos += 1
                        self.matriz[lin][col] = 0
                        if self.pontos >= 306:
                            self.estado = 3
                    else:
                        movivel.recusar_movimento(direcoes)

        """Função refatorada acima para usar a classe abstrata Movivel
        direcoes = self.get_direcoes(self.fantasma.linha, self.fantasma.coluna)
        if len(direcoes) >= 3: #Verifica se existem 3 ou mais caminhos possíveis
            self.fantasma.esquina(direcoes)
        print("Direções", direcoes)
        col = self.pacman.coluna_intencao
        lin = self.pacman.linha_intencao
        #if 0 <= col < 28 and 0 <= lin < 29: #Verifica se está nos limites da matriz
        if 0 <= col < len(self.matriz[0]) and 0 <= lin < len(self.matriz):#forma profissional de verificar tamanho da matriz
            if self.matriz[lin][col] != 2: #Verifica se não é parede(cor azul)
                self.pacman.aceitar_movimento() #Chama o método aceitar_movimento para movimentar o pacman
                if self.matriz[lin][col] == 1: #Verifica se a célula é igual a 1 (se possui ponto amarelo)
                    self.pontos += 1 #acresenta 1 aos pontos a cada pastilha que tocar/comer
                    self.matriz[lin][col] = 0 #Preenche com 0 (deixa a célula vazia/sem o ponto amarelo/pastilha)
                    #print(self.pontos) exibe os pontos na área de compilação

        col = int(self.fantasma.coluna_intencao)
        lin = int(self.fantasma.linha_intencao)
        if 0 <= col < 28 and 0 <= lin < 29 and self.matriz[lin][col] != 2:
            self.fantasma.aceitar_movimento()
        else:
            self.fantasma.recusar_movimento(direcoes)"""

    #Método implementado da classe abstrata
    def processar_eventos(self, evts):#Método responsável por lidar com evento QUIT
        for e in evts:
            if e.type == pygame.QUIT:
                exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_p:
                    if self.estado == 0:
                        self.estado = 1
                    else:
                        self.estado = 0


class Pacman(ElementoJogo, Movivel):
    def __init__(self, tamanho): #construtor - define os atributos do pacman que serão usados pelos métodos
        self.coluna = 1
        self.linha = 1
        self.centro_x = 400
        self.centro_y = 300
        self.tamanho = tamanho #800 // 30
        #self.tamanho = 100
        self.vel_x = 0
        self.vel_y = 0
        self.raio = self.tamanho // 2
        self.coluna_intencao = self.coluna
        self.linha_intencao = self.linha


    def pintar(self, tela): #Definindo o método pintar da classe pacman. tela é um parâmetro da função pintar.

        # Desenhar o corpo do Pacman
        pygame.draw.circle(tela, AMARELO,(self.centro_x, self.centro_y), self.raio,0)

        #Desenho da boca do Pacman
        canto_boca = (self.centro_x, self.centro_y)
        labio_superior = (self.centro_x + self.raio, self.centro_y - self.raio)
        labio_inferior = (self.centro_x + self.raio, self.centro_y)
        pontos = [canto_boca, labio_superior, labio_inferior]
        pygame.draw.polygon(tela, PRETO, pontos,0)

        #Desenho do olho do Pacman
        olho_x = int(self.centro_x + self.raio / 3)
        olho_y = int(self.centro_y - self.raio * 0.70)
        olho_raio = int(self.raio / 10)
        pygame.draw.circle(tela, PRETO, (olho_x, olho_y), olho_raio, 0)

    def processar_eventos(self, eventos): #Definindo o método processar_eventos da classe pacman
        for e in eventos:
            if e.type == pygame.KEYDOWN:#evento de pressionamento de tecla
                if e.key == pygame.K_RIGHT:#Propriedade key
                    self.vel_x = VELOCIDADE
                elif e.key == pygame.K_LEFT:
                    self.vel_x = -VELOCIDADE
                elif e.key == pygame.K_UP:
                    self.vel_y = -VELOCIDADE
                elif e.key == pygame.K_DOWN:
                    self.vel_y = VELOCIDADE
            elif e.type == pygame.KEYUP:
                if e.key == pygame.K_RIGHT:
                    self.vel_x = 0
                elif e.key == pygame.K_LEFT:
                    self.vel_x = 0
                elif e.key == pygame.K_UP:
                    self.vel_y = 0
                elif e.key == pygame.K_DOWN:
                    self.vel_y = 0


    def calcular_regras(self):
        #calculo das regras com base na velocidade das coordenadas x e y
        """
        self.centro_x = self.centro_x + self.vel_x #Movimentando o pacman na posição x
        self.centro_y = self.centro_y + self.vel_y #Movimentando o pacman na posição y
        """
        #calcula a intenção de movimento
        self.coluna_intencao = self.coluna + self.vel_x#grava a telcla pressionada, mas ainda não move
        self.linha_intencao = self.linha + self.vel_y
        self.centro_x = int(self.coluna * self.tamanho + self.raio)
        self.centro_y = int(self.linha * self.tamanho + self.raio)

        """
        #código usado para verifciar se houve colisão com as bordas
        if self.centro_x + self.raio >= 800:
            self.vel_x = -1
        if self.centro_x - self.raio <= 0:
            self.vel_x = 1
        if self.centro_y + self.raio >= 600:
            self.vel_y = -1
        if self.centro_y - self.raio <= 0:
            self.vel_y = 1
        """
    def aceitar_movimento(self):#Método faz o movimento do pacman, Transforma a intenção em posição real
        self.linha = self.linha_intencao
        self.coluna = self.coluna_intencao

    #Parte 9
    def recusar_movimento(self, direcoes):
        self.linha_intencao = self.linha
        self.coluna_intencao = self.coluna

    def esquina(self, direcoes):
        pass


class Fantasma(ElementoJogo, Movivel):
    def __init__(self, cor, tamanho):
        self.coluna = 13.0 #6.0
        self.linha = 15.0 #2.0 #8.0
        self.linha_intencao = self.linha
        self.coluna_intencao = self.coluna
        self.velocidade = 1
        self.direcao = ABAIXO #0
        self.tamanho = tamanho
        self.cor = cor

    def pintar(self, tela):
        fatia = self.tamanho // 8
        px = int(self.coluna * self.tamanho)
        py = int(self.linha * self.tamanho)
        contorno = [(px, py + self.tamanho), (px + fatia, py + fatia * 2), (px + fatia * 3, py + fatia // 2), (px + fatia * 3, py), (px + fatia * 5, py), (px + fatia * 6, py + fatia // 2), (px + fatia * 7, py + fatia * 2), (px + self.tamanho, py + self.tamanho)]
        pygame.draw.polygon(tela, self.cor, contorno, 0)

        olho_raio_ext = fatia
        olho_raio_int = fatia // 2

        olho_e_x = int(px + fatia * 2.5)
        olho_e_y = int(py + fatia * 2.5)

        olho_d_x = int(px + fatia * 5.5)
        olho_d_y = int(py + fatia * 2.5)

        pygame.draw.circle(tela, BRANCO, (olho_e_x, olho_e_y), olho_raio_ext, 0)
        pygame.draw.circle(tela, PRETO, (olho_e_x, olho_e_y), olho_raio_int, 0)
        pygame.draw.circle(tela, BRANCO, (olho_d_x, olho_d_y), olho_raio_ext, 0)
        pygame.draw.circle(tela, PRETO, (olho_d_x, olho_d_y), olho_raio_int, 0)

        #print(contorno)

    def calcular_regras(self): # calcula uma posição futura (intenção)
        if self.direcao == ACIMA:
            self.linha_intencao -= self.velocidade
        elif self.direcao == ABAIXO:
            self.linha_intencao += self.velocidade
        elif self.direcao == ESQUERDA:
            self.coluna_intencao -= self.velocidade
        elif self.direcao == DIREITA:
            self.coluna_intencao += self.velocidade

    def mudar_direcao(self, direcoes): #Seleciona uma direção aleatória
        self.direcao = random.choice(direcoes)

    def esquina(self, direcoes): # Método chamado quando o fantasma chega em um cruzamento
        self.mudar_direcao(direcoes)

    def aceitar_movimento(self): #Aplica o movimento que foi validado
        self.linha = self.linha_intencao
        self.coluna = self.coluna_intencao

    def recusar_movimento(self, direcoes): #Cancela a intenção de movimento
        self.linha_intencao = self.linha
        self.coluna_intencao = self.coluna
        self.mudar_direcao(direcoes)

    def processar_eventos(self, evts):
        pass


if __name__ == "__main__":
    tamanho = 600 // 30
    # Criando o objetos(pacman, blinky e cenario)
    pacman = Pacman(tamanho) # tamanho é o argumento passado para o parametro tamanho no init do Pacman.
    blinky = Fantasma(VERMELHO, tamanho)
    #Parte 9
    inky = Fantasma(CIANO, tamanho)
    clyde = Fantasma(LARANJA, tamanho)
    pinky = Fantasma(ROSA, tamanho)
    cenario = Cenario(tamanho, pacman, blinky)
    cenario.adicionar_movivel(pacman)
    cenario.adicionar_movivel(blinky)
    cenario.adicionar_movivel(inky)
    cenario.adicionar_movivel(clyde)
    cenario.adicionar_movivel(pinky)

    while True:
        #Calcular as regras
        pacman.calcular_regras() #chamando o método calcular_regras da classe pacman
        blinky.calcular_regras() ##chamando o método calcular_regras da classe fantasma
        #Parte 9
        inky.calcular_regras()  ##chamando o método calcular_regras da classe fantasma
        clyde.calcular_regras()  ##chamando o método calcular_regras da classe fantasma
        pinky.calcular_regras()  ##chamando o método calcular_regras da classe fantasma
        cenario.calcular_regras() #chamando o método calcular_regras da classe cenario

        #Pintar a tela
        tela.fill(PRETO)
        cenario.pintar(tela) # tela é um argumento  do método pintar.
        pacman.pintar(tela) #chamando o método pintar da classe pacman. tela é o argumento que foi passado para o parâmetro da função pintar.
        blinky.pintar(tela)
        #Parte 9
        inky.pintar(tela)
        clyde.pintar(tela)
        pinky.pintar(tela)
        pygame.display.update()
        pygame.time.delay(100)

        #Captura eventos
        eventos = pygame.event.get() #armazena os eventos capturados na variável eventos
        pacman.processar_eventos(eventos) #chamando o método processar_eventos da classe pacman
        cenario.processar_eventos(eventos) #chamando o método processar_eventos da classe cenario


