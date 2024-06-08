import pygame
import sys
from random import shuffle, randint

# Inicializa o Pygame e o mixer
pygame.init()
pygame.mixer.init()

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

    def atualizar_pontos(self, novos_pontos):
        self.pontos = novos_pontos

class Som:
    def __init__(self, musicas):
        self.musicas = musicas
        shuffle(self.musicas)  
        self.musica_atual = 0
        pygame.mixer.music.set_volume(0.3)

    def player_sound(self):
        if self.musica_atual < len(self.musicas):
            pygame.mixer.music.load(self.musicas[self.musica_atual])
            pygame.mixer.music.play()
            self.musica_atual += 1
        else:
            self.musica_atual = 0
            shuffle(self.musicas)  

    def check_music_end(self):
        if not pygame.mixer.music.get_busy():
            self.player_sound()

class SomEfeito:
    def __init__(self, efeito):
        self.efeito = pygame.mixer.Sound(efeito)

    def player_sound_efeito(self):
        self.efeito.play()

class Radon:
    def __init__(self, eixo_x, eixo_y):
        self.eixo_x = eixo_x
        self.eixo_y = eixo_y
    
    def radon_eixo(self):
        radon_x = randint(0, self.eixo_x - 55)  
        radon_y = randint(0, self.eixo_y - 55)
        return radon_x, radon_y

class Chase:
    def __init__(self, resultado):
        self.resultado = resultado
    
    def close(self):
        return self.resultado < -1
    
class Tempo:
    def __init__(self):
        self.start_time = None
        self.duration = None

    def start(self, duration):
        self.start_time = pygame.time.get_ticks()
        self.duration = duration

    def has_elapsed(self):
        if self.start_time is None:
            return False
        return (pygame.time.get_ticks() - self.start_time) >= self.duration

tamanho_eixo_x = 640
tamanho_eixo_y = 480

fps = pygame.time.Clock()

resolucao_instancia = Tela(tamanho_eixo_x, tamanho_eixo_y)
screen = resolucao_instancia.resolucao()

placar = 0

pontos_instancia = Pontos(tamanho_eixo_x, tamanho_eixo_y, placar)

# Carregar as imagens
image = pygame.image.load('pietro.png')
proerd = pygame.image.load('proerdpixel.png')
filho = pygame.image.load('filho.png')
cigarro = pygame.image.load('cigarropixel.png')
beck = pygame.image.load('beckpixel.png')
pinga = pygame.image.load('51pixel.png')

# Carregar e redimensionar a imagem da grama para preencher a tela
grama = pygame.image.load('grama.png')
grama = pygame.transform.scale(grama, (tamanho_eixo_x, tamanho_eixo_y))

# Redimensionar as outras imagens
image = pygame.transform.scale(image, (55, 55))
proerd = pygame.transform.scale(proerd, (55, 55))
filho = pygame.transform.scale(filho, (55, 55))
cigarro = pygame.transform.scale(cigarro, (70, 70))
beck = pygame.transform.scale(beck, (70, 70))
pinga = pygame.transform.scale(pinga, (70, 70))

# Obter os retângulos das imagens para posicionamento
image_rect = image.get_rect()
image_rect.center = (tamanho_eixo_x // 2, tamanho_eixo_y // 2)

# Gerar posições aleatórias para as outras imagens
radon_instancia = Radon(tamanho_eixo_x, tamanho_eixo_y)
proerd_rect = proerd.get_rect(topleft=radon_instancia.radon_eixo())
filho_rect = filho.get_rect(topleft=radon_instancia.radon_eixo())
cigarro_rect = cigarro.get_rect(topleft=radon_instancia.radon_eixo())
beck_rect = beck.get_rect(topleft=radon_instancia.radon_eixo())
pinga_rect = pinga.get_rect(topleft=radon_instancia.radon_eixo())

# Lista de músicas
musicas = ['dedo.wav', 'derame.wav', 'eu.wav', 'iml.wav', 'mi.wav', 'pau.wav']
som_instancia = Som(musicas)
som_instancia.player_sound()

direcao = 'direita'

running = True

estancia_close = Chase(placar)
if estancia_close.close == True:
    running = False

velocidade = 20
velocidade_normal = 20

tempo_instancia = Tempo()

while running:

    velocidade_proerd = 4
    velocidade_filho = 2

    fps.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    teclas = pygame.key.get_pressed()
    
    if teclas[pygame.K_a]:
        if direcao != 'esquerda':
            image = pygame.transform.flip(image, True, False)
            direcao = 'esquerda'
        image_rect.x -= velocidade
    if teclas[pygame.K_d]:
        if direcao != 'direita':
            image = pygame.transform.flip(image, True, False)
            direcao = 'direita'
        image_rect.x += velocidade
    if teclas[pygame.K_w]:
        image_rect.y -= velocidade
    if teclas[pygame.K_s]:
        image_rect.y += velocidade

    # Limita a posição do boneco dentro dos limites da tela
    if image_rect.x < 0:
        image_rect.x = 0
    if image_rect.x > tamanho_eixo_x - image_rect.width:
        image_rect.x = tamanho_eixo_x - image_rect.width
    if image_rect.y < 0:
        image_rect.y = 0
    if image_rect.y > tamanho_eixo_y - image_rect.height:
        image_rect.y = tamanho_eixo_y - image_rect.height

    # Lógica de perseguição do Proerd
    if proerd_rect.x < image_rect.x:
        proerd_rect.x += velocidade_proerd
    elif proerd_rect.x > image_rect.x:
        proerd_rect.x -= velocidade_proerd

    if proerd_rect.y < image_rect.y:
        proerd_rect.y += velocidade_proerd
    elif proerd_rect.y > image_rect.y:
        proerd_rect.y -= velocidade_proerd

    # Lógica de perseguição do filho
    if filho_rect.x < image_rect.x:
        filho_rect.x += velocidade_filho
    elif filho_rect.x > image_rect.x:
        filho_rect.x -= velocidade_filho

    if filho_rect.y < image_rect.y:
        filho_rect.y += velocidade_filho
    elif filho_rect.y > image_rect.y:
        filho_rect.y -= velocidade_filho


    # Desenhar a grama no fundo
    screen.blit(grama, (0, 0))

    # Desenhar a imagem principal na tela
    screen.blit(image, image_rect)

    # Desenhar as outras imagens na tela
    screen.blit(proerd, proerd_rect)
    screen.blit(filho, filho_rect)
    screen.blit(cigarro, cigarro_rect)
    screen.blit(beck, beck_rect)
    screen.blit(pinga, pinga_rect)

    # Desenhar os pontos
    pontos_instancia.desenhar_pontos(screen)
    
    # Colisões / pontos
    if image_rect.colliderect(proerd_rect):
        proerd_rect.topleft = radon_instancia.radon_eixo()
        placar -= 1
        hit_efeito = 'hum.wav'
        som_efeito = SomEfeito(hit_efeito)
        som_efeito.player_sound_efeito()

    elif image_rect.colliderect(cigarro_rect):
        cigarro_rect.topleft = radon_instancia.radon_eixo()
        placar += 2

        velocidade = 10  
        tempo_instancia.start(5000)  

        cigarro_efeito = 'sla.wav'
        som_efeito = SomEfeito(cigarro_efeito)
        som_efeito.player_sound_efeito()

    elif image_rect.colliderect(pinga_rect):
        pinga_rect.topleft = radon_instancia.radon_eixo()
        placar += 1

        velocidade = 30  
        tempo_instancia.start(5000)  
        
        pinga_efeito = 'sla.wav'
        som_efeito = SomEfeito(pinga_efeito)
        som_efeito.player_sound_efeito()

    elif image_rect.colliderect(beck_rect):
        beck_rect.topleft = radon_instancia.radon_eixo()
        placar += 3

        velocidade = 5  
        tempo_instancia.start(4000)  

        beck_efeito = 'sla.wav'
        som_efeito = SomEfeito(beck_efeito)
        som_efeito.player_sound_efeito()
    
    elif image_rect.colliderect(filho_rect):
        filho_rect.topleft = radon_instancia.radon_eixo()
        placar += - 2
        hit_efeito = 'hum.wav'
        som_efeito = SomEfeito(hit_efeito)
        som_efeito.player_sound_efeito()

    # Verifica se o tempo já passou e reseta a velocidade
    if tempo_instancia.has_elapsed():
        velocidade = velocidade_normal

    pontos_instancia.atualizar_pontos(placar)

    # Condição para fechar o placar 
    estancia_close = Chase(placar)
    if estancia_close.close():
        running = False

    som_instancia.check_music_end()

    pygame.display.flip()

pygame.quit()
sys.exit()
