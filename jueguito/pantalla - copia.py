import pygame
import sys
import random

class Enemigo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.sprites = [pygame.image.load('finn1.png'), 
                        pygame.image.load('finn2.png'), 
                        pygame.image.load('finn3.png'),]
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.alto = 150
        self.ancho = 120
        self.image = pygame.transform.scale(self.image,(self.ancho, self.alto))
        self.rect = self.image.get_rect()
        self.speed_x = -10
        self.frame_contar = 0
        #velocidad de la animacion(entre más alta, más lenta)
        self.animation_speed = 5

    #Velocidad inicial
    def update(self):
        self.rect.x -= 15
        self.speed_x -= self.rect.x
        if self.rect.right < 0:
            self.reset() 
        self.frame_contar += 1
        if self.frame_contar % self.animation_speed == 0:
            self.current_sprite = (self.current_sprite + 1) % len(self.sprites)
            self.image = self.sprites[self.current_sprite]
            self.image = pygame.transform.scale(self.image, (self.ancho, self.alto))      

    #Spaw del enemigo
    def reset(self):
        self.rect.x = 800
        self.rect.y = random.randint(20, 300)

    def __del__(self):
        self.sprites = 0
        self.current_sprite = 0
        self.image = 0
        self.alto = 0
        self.ancho = 0
        self.rect = 0
        self.speed_x = 0
        self.frame_contar = 0
        self.animation_speed = 0
        self.rect.x = 0
        self.rect.y = 0

class Jugador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('juan.png')
        self.alto = 150
        self.ancho = 150
        self.image = pygame.transform.scale(self.image,(self.ancho,self.alto))
        self.rect = self.image.get_rect()
        self.rect.center = (400, 700)
        self.speed_x = 0
        self.speed_y = 0
        self.velocidad_positiva = 15
        self.velocidad_negativa = -15
    
    #Para limitar la pantalla
    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > 800:
            self.rect.right = 800
        if self.rect.bottom > 600:
            self.rect.bottom = 600

    def reset_position(self):
        self.rect.center = (400, 700)

    def __del__(self):
        self.image = 0
        self.alto = 0
        self.ancho = 0
        self.rect = 0
        self.speed_x = 0
        self.speed_y = 0
        self.velocidad_positiva = 0
        self.velocidad_negativa = 0
        self.rect.center = 0
        self.rect.x = 0
        self.rect.y = 0
        self.rect.left = 0
        self.rect.right = 0
        self.rect.bottom = 0

pygame.init()
        

def pantalla():

    size = 800,600
    alto_pantalla= 600
    ancho_pantalla= 800
    screen=pygame.display.set_mode(size)
    clock=pygame.time.Clock()
    done = False
    pantalla = pygame.image.load("fondo.png").convert()
    pantalla = pygame.transform.scale(pantalla,(ancho_pantalla,alto_pantalla))
    pantalla_perdedor = pygame.image.load("fondo1.png").convert()
    pantalla_perdedor = pygame.transform.scale(pantalla_perdedor,(ancho_pantalla,alto_pantalla))
    pygame.display.set_caption("Colisión de Sprites")
    enemigo1 = pygame.image.load('finn3.png')
    enemigo1 = pygame.transform.scale(enemigo1,(400,500))
    jugador = Jugador()
    enemigo = Enemigo()
    contar_vidas = 3
    nivel = 0
    #tipografia
    font = pygame.font.SysFont('comicsansms', 37)
    font1 = pygame.font.SysFont('comicsansms', 50)
    todos_sprites = pygame.sprite.Group()
    todos_sprites.add(jugador)
    todos_sprites.add(enemigo)
    pygame.mouse.set_visible(1)

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            #Movimiento de Teclado
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    jugador.speed_x = jugador.velocidad_positiva
                if event.key == pygame.K_a:
                    jugador.speed_x= jugador.velocidad_negativa
                if event.key == pygame.K_s:
                    jugador.speed_y= jugador.velocidad_positiva
                if event.key == pygame.K_w:
                    jugador.speed_y= jugador.velocidad_negativa

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_d:
                    jugador.speed_x = 0
                if event.key == pygame.K_a:
                    jugador.speed_x = 0
                if event.key == pygame.K_s:
                    jugador.speed_y = 0
                if event.key == pygame.K_w:
                   jugador.speed_y = 0

        #Detecta las colisiones de jugador con el enemigo
        colisiones = pygame.sprite.spritecollide(jugador, [enemigo], False)
        if colisiones:
            jugador.reset_position()
            enemigo.reset()
            contar_vidas -= 1

        if jugador.rect.y <= -135:   
            nivel += 1     
            enemigo.reset()
            jugador.reset_position()

        if random.randint(0, 7) < nivel:
            enemigo.rect.x -= 20
            jugador.velocidad_negativa = 20
            jugador.velocidad_negativa = -20
        
        if nivel == 8:
            enemigo.rect.x += 20

        if nivel > 8:
            enemigo.rect.x -= 5
            jugador.velocidad_negativa = 25 
            jugador.velocidad_negativa = -25       

        nivel_texto = font1.render(f'Nivel: {nivel}', True, (255, 255, 255))
        vidas_texto = font1.render(f'Vidas: {contar_vidas}', True, (255, 255, 255))


        screen.blit(pantalla, [0,0])
        todos_sprites.update()
        screen.blit(nivel_texto, (590, 15))
        screen.blit(vidas_texto, (20, 15))
        todos_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(60)

        if contar_vidas == 0 :
           game_nivel = font.render(f'Haz Llegado al nivel: {nivel}', True, (255,0,0))
           game_perdedor = font.render('Perdiste :)', True, (255,0,0))
           game_denuevo = font.render('Presiona cualquier tecla para jugar denuevo', True, (255,0,0))
           screen.blit(pantalla_perdedor, [0,0])
           screen.blit(game_nivel, (200, 200))
           screen.blit(game_perdedor, (310, 250))
           screen.blit(game_denuevo, (30, 350))
           pygame.display.flip()
           waiting = True
           while waiting:
               for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        done = True
                        waiting = False
                    if event.type == pygame.KEYDOWN:
                        jugador.reset_position()
                        enemigo.reset()
                        contar_vidas = 3
                        nivel = 0
                        waiting = False
                    if event.type == pygame.KEYUP:
                        #Para que el personaje no se mueva al presionar alguna tecla
                        if event.key == pygame.K_d:
                            jugador.speed_x = 0
                        if event.key == pygame.K_a:
                            jugador.speed_x = 0
                        if event.key == pygame.K_s:
                            jugador.speed_y = 0
                        if event.key == pygame.K_w:
                            jugador.speed_y = 0

        if nivel == 10:
            game_nivel = font.render(f'Haz Llegado al nivel: {nivel}', True, (0,255,0))
            game_ganador = font.render('Ganaste!!!', True, (0,255,0))
            game_denuevo = font.render('Presiona cualquier tecla para jugar denuevo', True, (0,255,0))
            screen.blit(pantalla, [0,0])
            screen.blit(enemigo1, (-50,-30))
            screen.blit(enemigo1, (550,360))
            screen.blit(game_nivel, (200, 200))
            screen.blit(game_ganador, (310, 250))
            screen.blit(game_denuevo, (30, 350))
            pygame.display.flip()
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        done = True
                        waiting = False
                    if event.type == pygame.KEYDOWN:
                        jugador.reset_position()
                        enemigo.reset()
                        contar_vidas = 3
                        nivel = 0
                        waiting = False
                    if event.type == pygame.KEYUP:
                        #Para que el personaje no se mueva al presionar alguna tecla
                        if event.key == pygame.K_d:
                            jugador.speed_x = 0
                        if event.key == pygame.K_a:
                            jugador.speed_x = 0
                        if event.key == pygame.K_s:
                            jugador.speed_y = 0
                        if event.key == pygame.K_w:
                            jugador.speed_y = 0

    pygame.quit()

pantalla()