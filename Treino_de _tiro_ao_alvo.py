import pygame
import random

# Inicializa o Pygame
pygame.init()

# Define o tamanho da janela
width = 800
height = 600

# Cria a superfície da janela
screen = pygame.display.set_mode((width, height))

# Define a cor de fundo da tela
bg_color = (0, 0, 0)  # Preto

# Define a fonte usada para a mensagem de fim de jogo
font = pygame.font.SysFont(None, 48)

# Define a classe do retângulo


class Rectangle:
    def __init__(self):
        self.width = 20
        self.height = 100
        self.x = width - self.width
        self.y = random.randint(0, height - self.height)
        self.speed = 5
        # Adiciona o atributo 'rect' à classe
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self):
        self.y += self.speed
        if self.y < 0 or self.y > height - self.height:
            self.speed = -self.speed
        # Atualiza o atributo 'rect' a cada frame
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, surface):
        rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(surface, (255, 0, 0), rect)


class Spaceship:
    def __init__(self):
        self.width = 50
        self.height = 25
        self.x = 50
        self.y = height / 2 - self.height / 2
        self.speed = 10
        self.bullets = []

        # Adiciona um atributo 'bullet_speed' para controlar a velocidade das balas
        self.bullet_speed = 15

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.y > 0:
            self.y -= self.speed
        if keys[pygame.K_DOWN] and self.y < height - self.height:
            self.y += self.speed
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        # Atualiza a posição de cada bala
        for bullet in self.bullets:
            bullet.x += self.bullet_speed

        # Remove as balas que saem da tela
        self.bullets = [bullet for bullet in self.bullets if bullet.x < width]

    def draw(self, surface):
        rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(surface, (255, 255, 255), rect)

    def shoot(self):
        # Cria um objeto de bala com as coordenadas corretas
        bullet = pygame.Rect(self.x + self.width, self.y +
                             self.height / 2 - 2, 10, 4)
        self.bullets.append(bullet)

    def update_bullets(self):
        # Atualiza a posição de cada bala
        for bullet in self.bullets:
            bullet.x += self.bullet_speed

        # Remove as balas que saem da tela
        self.bullets = [bullet for bullet in self.bullets if bullet.x < width]

    def draw_bullets(self, surface):
        for bullet in self.bullets:
            pygame.draw.rect(surface, (255, 255, 255), bullet)


# Define a função que verifica se há colisão entre dois retângulos
def collides(rect1, rect2):
    return rect1.colliderect(rect2)

# Define o botão Play


class PlayButton:
    def __init__(self,game):
        self.width = 200
        self.height = 50
        self.x = game.width / 2 - self.width / 2
        self.y = game.height / 2 - self.height / 2
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, surface):
        pygame.draw.rect(surface, (0, 255, 0), self.rect)
        font = pygame.font.Font(None, 36)
        text = font.render("Play", True, (255, 255, 255))
        text_rect = text.get_rect(center=self.rect.center)
        surface.blit(text, text_rect)

    def clicked(self, x, y):
        return self.rect.collidepoint(x, y)

    def update(self):
        pass  # Método vazio, já que o botão é um objeto estático


# Define a classe do jogo


class Game:
    def __init__(self):
        pygame.init()
        self.width = 800
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Space Shooter")
        self.clock = pygame.time.Clock()
        self.bg_color = (0, 0, 255)
        self.rectangle = Rectangle()
        self.spaceship = Spaceship()
        self.score = 0
        self.missed = 0
        self.running = False
        self.play_button = PlayButton(self)

    def start(self):
        self.score = 0
        self.missed = 0
        self.rectangle = Rectangle()
        self.spaceship = Spaceship()
        self.running = True
        pygame.display.update()  # Atualiza a tela para refletir as mudanças


    def update(self):
        self.rectangle.update()
        self.spaceship.update()
        self.spaceship.update_bullets()  # Adiciona a atualização das balas
        self.play_button.update()

    def draw(self):
        self.screen.fill(self.bg_color)
        self.rectangle.draw(self.screen)
        self.spaceship.draw(self.screen)
        # Adiciona o desenho das balas
        self.spaceship.draw_bullets(self.screen)
        score_text = font.render("Score: {}".format(
            self.score), True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))
        missed_text = font.render("Missed: {}".format(
            self.missed), True, (255, 255, 255))
        self.screen.blit(missed_text, (self.width - 150, 10))
        if not self.running:
            self.play_button.draw(self.screen)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.spaceship.shoot()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if not self.running and self.play_button.clicked(x, y):
                    self.start()

    def check_collisions(self):
        collided = False
        if collides(self.spaceship.rect, self.rectangle.rect):
            self.score += 1
            self.rectangle = Rectangle()
            collided = True
        for bullet in self.spaceship.bullets:
            if collides(bullet, self.rectangle.rect):
                self.score += 1
                self.spaceship.bullets.remove(bullet)
                self.rectangle = Rectangle()
                collided = True
                break
        if not collided and self.rectangle.y < 0:
            self.missed += 1
            self.rectangle = Rectangle()
        if self.missed >= 3:
            self.running = False


    def run(self):
        while True:
            self.handle_events()
            if self.running:
                self.update()
                self.check_collisions()
            self.draw()
            pygame.display.flip()
            self.clock.tick(60)


# Cria uma instância do jogo e o inicia
game = Game()
game.run()
