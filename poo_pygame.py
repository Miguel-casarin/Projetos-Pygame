import pygame

pygame.init()

class Tela:
    def __init__(self, eixo_x, eixo_y):
        self.eixo_x = eixo_x
        self.eixo_y = eixo_y
        self.screen = None

    def resolucao(self):
        self.screen = pygame.display.set_mode([self.eixo_x, self.eixo_y])
        return self.screen

class Pontos:
    def __init__(self, eixo_x, eixo_y, pontos):
        self.eixo_x = eixo_x
        self.eixo_y = eixo_y
        self.pontos = pontos
        pygame.font.init()
        self.font = pygame.font.SysFont('Arial', 36)

    def local_pontos(self):
        posicao_pontos_x = ((self.eixo_x // 2.7) + (self.eixo_x / 4)) 
        posicao_pontos_y = ((self.eixo_y / 3) - (self.eixo_y // 4.5)) 
        return posicao_pontos_x, posicao_pontos_y

    def desenhar_pontos(self, screen):
        posicao_x, posicao_y = self.local_pontos()
        pontos_surface = self.font.render(f'Pontos: {self.pontos}', True, (0, 0, 0))
        screen.blit(pontos_surface, (posicao_x, posicao_y))
    

class Som:
    def __init__(self, musica):
        self.musica = musica
        pygame.mixer.init()

    def player_sound(self):
        pygame.mixer.music.load(self.musica)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)


tamanho_eixo_x = 640
tamanho_eixo_y = 480

cor_boneco = (0, 255, 255)

fps = pygame.time.Clock()

resolucao_estancia = Tela(tamanho_eixo_x, tamanho_eixo_y)
screen = resolucao_estancia.resolucao()

# fazer depois a função dentro do jo que vai retornar os pontos
pontos_instancia = Pontos(tamanho_eixo_x, tamanho_eixo_y, 0)


def posicao_boneco_tamanho(tamanho):
    tamanho_dis = tamanho / 2
    return tamanho_dis

 # Movimentando o objeto
x_boneco = posicao_boneco_tamanho(tamanho_eixo_x)
y_boneco = posicao_boneco_tamanho(tamanho_eixo_y)



def playuer():
    musica = 'Cyberpunk Moonlight Sonata.mp3'
    estancia_som = Som(musica)
    estancia_som.player_sound()


running = True
while running:

    fps.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    teclas = pygame.key.get_pressed()
    
    if teclas[pygame.K_a]:
        x_boneco = x_boneco - 20
    if teclas[pygame.K_d]:
        x_boneco = x_boneco + 20
    if teclas[pygame.K_w]:
        y_boneco = y_boneco - 20
    if teclas[pygame.K_s]:
        y_boneco = y_boneco + 20

    # Limita a posição do boneco dentro dos limites da tela
    if x_boneco < 0:
        x_boneco = 0
    if x_boneco > tamanho_eixo_x - 30:  # largura do boneco é 30
        x_boneco = tamanho_eixo_x - 30
    if y_boneco < 0:
        y_boneco = 0
    if y_boneco > tamanho_eixo_y - 30:  # altura do boneco é 30
        y_boneco = tamanho_eixo_y - 30


    screen.fill((255, 255, 255))
    #pontos_instancia = Pontos(tamanho_eixo_x, tamanho_eixo_y, 0)
    pontos_instancia.desenhar_pontos(screen)

     # Desenhando o objeto (retângulo)
    pygame.draw.rect(screen, cor_boneco, (x_boneco, y_boneco, 30, 30))
    
    # Atualizando a tela
    pygame.display.flip()

    #Exemplo = playuer()

pygame.quit()
