import pygame
pygame.init()

# Параметры экрана
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Параметры шкалы
BAR_WIDTH = 200
BAR_HEIGHT = 20
MAX_NOISE_LEVEL = 100
NOISE_INCREASE_AMOUNT = 5  # Скорость увеличения уровня шума

# Инициализация экрана
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Шкала уровня шума')

# Функция для отрисовки шкалы
def draw_noise_bar(noise_level):
    bar_length = int(noise_level / MAX_NOISE_LEVEL)
    pygame.draw.rect(screen, WHITE, (50, 50, BAR_WIDTH, BAR_HEIGHT))  # Фон шкалы
    pygame.draw.rect(screen, (255, 0, 0), (50, 50, bar_length, BAR_HEIGHT))  # Полоса шкалы

# Основной игровой цикл
running = True
noise_level = 0  # Начальный уровень шума
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Симуляция изменения уровня шума (ваша логика игры может отличаться)
    if pygame.K_SPACE:  # Пример: увеличение уровня шума при нажатии на пробел
        noise_level += NOISE_INCREASE_AMOUNT
        if noise_level > MAX_NOISE_LEVEL:
            noise_level = MAX_NOISE_LEVEL

    # Очистка экрана
    screen.fill(BLACK)

    # Отрисовка шкалы
    draw_noise_bar(noise_level)

    # Обновление экрана
    pygame.display.flip()

# Завершение Pygame
pygame.quit()