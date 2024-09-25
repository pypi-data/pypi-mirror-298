import pygame
import random

# Inicializar o Pygame
pygame.init()

# Definir dimensões da janela do jogo
WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncing Square")

# Definir cores
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)

# Definir FPS
FPS = 60

# Classe para o quadrado
class Square:
    def __init__(self, color, x, y, size, speed_x, speed_y):
        self.color = color
        self.rect = pygame.Rect(x, y, size, size)
        self.speed_x = speed_x
        self.speed_y = speed_y

    def move(self):
        # Mover o quadrado
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Colisões com as bordas da janela
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.speed_x = -self.speed_x
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.speed_y = -self.speed_y

    def draw(self, window):
        pygame.draw.rect(window, self.color, self.rect)

# Gerar quadrados aleatórios
def generate_squares(num_squares, size):
    squares = []
    colors = [RED, BLUE, GREEN, YELLOW, PURPLE]
    for _ in range(num_squares):
        x = random.randint(0, WIDTH - size)
        y = random.randint(0, HEIGHT - size)
        speed_x = random.choice([-5, 5])
        speed_y = random.choice([-5, 5])
        color = random.choice(colors)
        square = Square(color, x, y, size, speed_x, speed_y)
        squares.append(square)
    return squares

# Função principal do jogo
def main():
    clock = pygame.time.Clock()
    run = True

    # Configurar quadrados
    squares = generate_squares(5, 50)

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Mover e desenhar os quadrados
        window.fill(WHITE)
        for square in squares:
            square.move()
            square.draw(window)

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
