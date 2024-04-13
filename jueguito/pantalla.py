import pygame
import sys
import random

class Enemigo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.sprites = [pygame.image.load('finn1.png'), 
                        pygame.image.load('finn5.png'),
                        pygame.image.load('finn6.png'), 
                        pygame.image.load('finn5.png')]
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.alto = 150
        self.ancho = 120
        self.image = pygame.transform.scale(self.image, (self.ancho, self.alto))     
        self.rect = self.image.get_rect()
        self.speed_x = -10
        self.frame_contar = 0
        #velocidad de la animacion(entre más alta, más lenta)
        self.animation_speed = 10

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


class Game(object):
    def __init__(self):
        self.nivel = 0
        self.contar_vidas = 3
        self.alto_pantalla= 600
        self.ancho_pantalla= 800

        self.pantalla = pygame.image.load("fondo.png").convert()
        self.pantalla = pygame.transform.scale(self.pantalla,(self.ancho_pantalla,self.alto_pantalla))
        self.pantalla_perdedor = pygame.image.load("fondo1.png").convert()
        self.pantalla_perdedor = pygame.transform.scale(self.pantalla_perdedor,(self.ancho_pantalla,self.alto_pantalla))
        
        self.enemigo1 = pygame.image.load('finn3.png')
        self.enemigo1 = pygame.transform.scale(self.enemigo1,(400,500))
        #tipografia
        self.font = pygame.font.SysFont('comicsansms', 37)
        self.font1 = pygame.font.SysFont('comicsansms', 50)

        self.jugador = Jugador()
        self.enemigo = Enemigo()

        pygame.display.set_caption("Colisión de Sprites")
        self.todos_sprites = pygame.sprite.Group()
        self.todos_sprites.add(self.jugador)
        self.todos_sprites.add(self.enemigo)
        pygame.mouse.set_visible(1)
    
    def proceso_evento(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            #Movimiento de Teclado
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    self.jugador.speed_x = self.jugador.velocidad_positiva
                if event.key == pygame.K_a:
                    self.jugador.speed_x= self.jugador.velocidad_negativa
                if event.key == pygame.K_s:
                    self.jugador.speed_y= self.jugador.velocidad_positiva
                if event.key == pygame.K_w:
                    self.jugador.speed_y= self.jugador.velocidad_negativa
                if event.key == pygame.K_y:
                    sys.exit()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_d:
                    self.jugador.speed_x = 0
                if event.key == pygame.K_a:
                    self.jugador.speed_x = 0
                if event.key == pygame.K_s:
                    self.jugador.speed_y = 0
                if event.key == pygame.K_w:
                   self.jugador.speed_y = 0
        return False
    
    def logica(self):

        self.colisiones = pygame.sprite.spritecollide(self.jugador, [self.enemigo], False)
        if self.colisiones:
            self.jugador.reset_position()
            self.enemigo.reset()
            self.contar_vidas -= 1

        if self.jugador.rect.y <= -135:   
            self.nivel += 1     
            self.enemigo.reset()
            self.jugador.reset_position()

        if random.randint(0, 7) < self.nivel:
            self.enemigo.rect.x -= 20
            self.jugador.velocidad_negativa = 20
            self.jugador.velocidad_negativa = -20
        
        if self.nivel == 8:
            self.enemigo.rect.x += 20

        if self.nivel > 8:
            self.enemigo.rect.x -= 5
            self.jugador.velocidad_negativa = 25 
            self.jugador.velocidad_negativa = -25

    def display_frame(self, screen):

        self.nivel_texto = self.font1.render(f'Nivel: {self.nivel}', True, (255, 255, 255))
        self.vidas_texto = self.font1.render(f'Vidas: {self.contar_vidas}', True, (255, 255, 255))

        screen.blit(self.pantalla, [0,0])
        self.todos_sprites.update()
        screen.blit(self.nivel_texto, (590, 15))
        screen.blit(self.vidas_texto, (20, 15))
        self.todos_sprites.draw(screen)
        pygame.display.flip()

        if self.contar_vidas == 0 :
           self.game_nivel = self.font.render(f'Haz Llegado al nivel: {self.nivel}', True, (255,0,0))
           self.game_perdedor = self.font.render('Perdiste :)', True, (255,0,0))
           self.game_denuevo = self.font.render('Presiona cualquier tecla para jugar denuevo', True, (255,0,0))
           screen.blit(self.pantalla_perdedor, [0,0])
           screen.blit(self.game_nivel, (200, 200))
           screen.blit(self.game_perdedor, (310, 250))
           screen.blit(self.game_denuevo, (30, 350))
           pygame.display.flip()
           self.waiting = True
           while self.waiting:
               for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.waiting = False
                        return True
                    if event.type == pygame.KEYDOWN:
                        self.jugador.reset_position()
                        self.enemigo.reset()
                        self.contar_vidas = 3
                        self.nivel = 0
                        self.waiting = False
                        if event.key == pygame.K_y:
                            sys.exit()
                    if event.type == pygame.KEYUP:
                        #Para que el personaje no se mueva al presionar alguna tecla
                        if event.key == pygame.K_d:
                            self.jugador.speed_x = 0
                        if event.key == pygame.K_a:
                            self.jugador.speed_x = 0
                        if event.key == pygame.K_s:
                            self.jugador.speed_y = 0
                        if event.key == pygame.K_w:
                            self.jugador.speed_y = 0

        if self.nivel == 10:
            self.game_nivel = self.font.render(f'Haz Llegado al nivel: {self.nivel}', True, (0,255,0))
            self.game_ganador = self.font.render('Ganaste!!!', True, (0,255,0))
            self.game_denuevo = self.font.render('Presiona cualquier tecla para jugar denuevo', True, (0,255,0))
            screen.blit(self.pantalla, [0,0])
            screen.blit(self.enemigo1, (-50,-30))
            screen.blit(self.enemigo1, (550,360))
            screen.blit(self.game_nivel, (200, 200))
            screen.blit(self.game_ganador, (310, 250))
            screen.blit(self.game_denuevo, (30, 350))
            pygame.display.flip()
            self.waiting = True
            while self.waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.waiting = False
                        return True
                    if event.type == pygame.KEYDOWN:
                        self.jugador.reset_position()
                        self.enemigo.reset()
                        self.contar_vidas = 3
                        self.nivel = 0
                        self.waiting = False
                        if event.key == pygame.K_y:
                            sys.exit()
                    if event.type == pygame.KEYUP:
                        #Para que el personaje no se mueva al presionar alguna tecla
                        if event.key == pygame.K_d:
                            self.jugador.speed_x = 0
                        if event.key == pygame.K_a:
                            self.jugador.speed_x = 0
                        if event.key == pygame.K_s:
                            self.jugador.speed_y = 0
                        if event.key == pygame.K_w:
                            self.jugador.speed_y = 0    
    def __del__(self):
        self.nivel = 0
        self.contar_vidas = 0
        self.alto_pantalla= 0
        self.ancho_pantalla= 0
        self.pantalla = 0
        self.pantalla_perdedor = 0     
        self.enemigo1 = 0
        self.font = 0
        self.font1 = 0
        self.jugador = 0
        self.enemigo = 0
        self.todos_sprites = 0
        self.waiting = 0

if __name__ == "__main__":

    pygame.init()

    size = 800,600
    screen= pygame.display.set_mode(size)
    clock= pygame.time.Clock()
    done = False

    game = Game()

    pygame.mixer.music.load("music/juan2.mp3")


    while not done:
        done = game.proceso_evento()
        game.logica()
        game.display_frame(screen)
        clock.tick(60)

    pygame.quit()
