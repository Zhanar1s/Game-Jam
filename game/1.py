from pygame import*
'''создаем игровую сцену'''
weight = 1200
height = 600
window = display.set_mode((weight,height))
bg = transform.scale(image.load('images/backround.jpg'), (weight, height))
'''Шаблон персонажей'''
class Hero(sprite.Sprite):
	def__init__(self, player_image, x, y, w, h, speed):
		sprite.Sprite.__init__(self)
		self.image = transform.scale(image.load(player_image),(w,h))
		self.speed = speed
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self











'''Игровой цикл'''
run = True
while run:
	window.blit(bg, (0,0))
	for e in event.get():
		if e.type == QUIT:
			run = False

	display.update()
