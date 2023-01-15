import pygame
import random
from button import Button
from health import HealthBar

pygame.init()

clock = pygame.time.Clock()
fps = 60

#game window
# bottom_panel represent the panel at the bottom which contains the health bar of the player and the enemy's health bar
# along witht he potion button for the player
# the value 150 represent the height of the panel
bottom_panel = 150
# width of the screen 
# Note screen size can't be changed
screen_width = 800
# Height of the screen including the panel 400 representing background heigh and all the entity in play
# adding the height of the bottom panel since it is part of the all display
screen_height = 400 + bottom_panel

# setting the screen display width and height
screen = pygame.display.set_mode((screen_width, screen_height))
# Setting a name or caption for the current pygame screen being displayed
pygame.display.set_caption('Main Battle Page')


#define game variables
# Number of character user
current_fighter = 1
# Number of overall character in the screen
total_fighters = 3

action_cooldown = 0
action_wait_time = 90
# Action variables
attack = False
potion = False
# Potion effect is default variable that shows the value of how much the potion heals the character
potion_effect = 15
# Action variables
clicked = False
# Game over variable if value is not 0 the game is over
# 1 means player wins and -1 means player lost
game_over = 0


#fonts variables or defining the font
font = pygame.font.SysFont('Times New Roman', 26)

#colours variable or defining the colour
red = (255, 0, 0)
green = (0, 255, 0)

#load images
#background image
# list is the list of possible background image
list = ["bg1","bg2","bg3","Derp"]
# aint is a varibale that is defined as a randomized number from value 0 to 3
# used to get the randomized background image
aint = random.randint(0,3)
# Loads background image
background_img = pygame.image.load(f'img/Background/{list[aint]}.jpeg').convert_alpha()
# loads panel image
panel_img = pygame.image.load('img/Icons/panel.png').convert_alpha()
# loads button images
potion_img = pygame.image.load('img/Icons/potion.png').convert_alpha()
restart_img = pygame.image.load('img/Icons/restart.png').convert_alpha()
#loads victory and defeat images when the game is over
victory_img = pygame.image.load('img/Icons/victory.png').convert_alpha()
defeat_img = pygame.image.load('img/Icons/defeat.png').convert_alpha()
#loads sword image which is the cursor
sword_img = pygame.image.load('img/Icons/sword.png').convert_alpha()


#create function for drawing the text
def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))


#function for drawing the background
def draw_bg():
	screen.blit(background_img, (0, 0))


#function for drawing the panel
def draw_panel():
	#draw panel rectangle
	screen.blit(panel_img, (0, screen_height - bottom_panel))
	#show Player stats
	draw_text(f'{Player.name} HP: {Player.hp}', font, red, 100, screen_height - bottom_panel + 10)
	for count, i in enumerate(enemyL):
		#show name and health
		draw_text(f'{i.name} HP: {i.hp}', font, red, 550, (screen_height - bottom_panel + 10) + count * 60)




#fighter class
class Fighter():
    # initializing the fighter class
	def __init__(self, x, y, name, max_hp, str, pot):
        # Name of the character or entity
		self.name = name
        # Max Hp of the object (Character/entity)
		self.max_hp = max_hp
        # Current Hp of the object (Character/entity)
		self.hp = max_hp
        # Additional strength stats bone of the object (Character/entity)
		self.str = str
        # Starting potion amount
		self.spot = pot
        # current potion amount
		self.pot = pot
        # Defining that currently the object (Character/entity) is alive or dead by true or false
		self.alive = True
        # Animation for when the character does action or even when they do nothing
		self.animation_list = []
		self.frame_index = 0
        #action value that corresponds to 0:idle, 1:attack, 2:hurt, 3:dead
		self.action = 0
		self.update_time = pygame.time.get_ticks()
		#load idle images of the sprite to make animation
		temp_list = []
		for i in range(4):
            # Loading file of the character by using name of the character
			img = pygame.image.load(f'img/{self.name}/Idle/{i}.png')
            # Scaling the image to make it fit better
			img = pygame.transform.scale(img, (img.get_width() * 2, img.get_height() * 2))
			temp_list.append(img)
		self.animation_list.append(temp_list)
		#load attack images of the sprite to make animation
		temp_list = []
		for i in range(13):
            # Loading file of the character by using name of the character
			img = pygame.image.load(f'img/{self.name}/Attack/{i}.png')
            # Scaling the image to make it fit better
			img = pygame.transform.scale(img, (img.get_width() * 2, img.get_height() * 2))
			temp_list.append(img)
		self.animation_list.append(temp_list)
		#load getting damage images of the sprite to make animation
		temp_list = []
		for i in range(3):
            # Loading file of the character by using name of the character
			img = pygame.image.load(f'img/{self.name}/Hurt/{i}.png')
            # Scaling the image to make it fit better
			img = pygame.transform.scale(img, (img.get_width() * 2, img.get_height() * 2))
			temp_list.append(img)
		self.animation_list.append(temp_list)
		#load death images of the sprite to make animation
		temp_list = []
		for i in range(6):
            # Loading file of the character by using name of the character
			img = pygame.image.load(f'img/{self.name}/Death/{i}.png')
            # Scaling the image to make it fit better
			img = pygame.transform.scale(img, (img.get_width() * 2, img.get_height() * 2))
			temp_list.append(img)
		self.animation_list.append(temp_list)
		self.image = self.animation_list[self.action][self.frame_index]
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)

    # Function use to update images for animations
	def update(self):
		animation_cooldown = 100
		#handle animation
		#update image
		self.image = self.animation_list[self.action][self.frame_index]
		#check if enough time has passed since the last update
		if pygame.time.get_ticks() - self.update_time > animation_cooldown:
			self.update_time = pygame.time.get_ticks()
			self.frame_index += 1
		#if the animation has run out then reset back to the start
		if self.frame_index >= len(self.animation_list[self.action]):
			if self.action == 3:
				self.frame_index = len(self.animation_list[self.action]) - 1
			else:
				self.idle()


	# function to the Character to idle and do nothing
	def idle(self):
		#set variables to idle animation
		self.action = 0
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()

    #Function that tells the character to attack
	def attack(self, target):
		#Randomize damge value for the characters
		rand = random.randint(-5, 5)
        # Adding bonus strength stats value to the overall damage calculation
		damage = self.str + rand
        # decreasing the target's Hp by the inflicted damage
		target.hp -= damage
		#run enemy getting damaged animation
		target.hurt()
		#check if the target have been killed
		if target.hp < 1:
			target.hp = 0
			target.alive = False
			target.death()
        # Calling the initialized class damage text to display damage inflicted as a string
		damage_text = DamageText(target.rect.centerx, target.rect.y, str(damage), red)
		damage_text_group.add(damage_text)
		#set variables to attack animation
		self.action = 1
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()

	def hurt(self):
		#set variables to getting damaged animation
		self.action = 2
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()

	def death(self):
		#set variables to death animation
		self.action = 3
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()

    # Function to reset the character when you press restart
	def reset (self):
		self.alive = True
		self.pot = self.spot
		self.hp = self.max_hp
		self.frame_index = 0
		self.action = 0
		self.update_time = pygame.time.get_ticks()

    # Draw the character in the screen
	def draw(self):
		screen.blit(self.image, self.rect)

# Damage text class to show the damage dealt
class DamageText(pygame.sprite.Sprite):
	def __init__(self, x, y, damage, colour):
		pygame.sprite.Sprite.__init__(self)
		self.image = font.render(damage, True, colour)
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
		self.counter = 0

    # Update the damage text position and counter
	def update(self):
		#move damage text up
		self.rect.y -= 1
		#delete the text after a few seconds
		self.counter += 1
		if self.counter > 30:
			self.kill()


damage_text_group = pygame.sprite.Group()

# Randomize max health value variable
you_health = random.randint(20,30)
enemy_health = random.randint(10,20)
enemy_health2 = random.randint(10,20)

# Randomize enemy postion in the screen variable
enemy_position = random.randint(140,160)
enemy_position2 = random.randint(190,210)

# Randomize strenght value variable
you_strength = random.randint(8,15)
enemy_strength = random.randint(5,10)
enemy_strength2 = random.randint(5,10)

# Randomize starting potions amount variable
you_potions = random.randint(3,5)
enemy_potions = random.randint(1,3)
enemy_potions2 = random.randint(1,3)

# Defining the characters
Player = Fighter(200, 220, 'Player', you_health, you_strength, you_potions)
enemy1 = Fighter(500, enemy_position, 'Enemy', enemy_health, enemy_strength, enemy_potions)
enemy2 = Fighter(700, enemy_position2, 'Enemy', enemy_health2, enemy_strength2,enemy_potions2)

# List of enemies
enemyL = []
enemyL.append(enemy1)
enemyL.append(enemy2)

# Health bar positioning in the screen
Player_health_bar = HealthBar(100, screen_height - bottom_panel + 40, Player.hp, Player.max_hp)
enemy1_health_bar = HealthBar(550, screen_height - bottom_panel + 40, enemy1.hp, enemy1.max_hp)
enemy2_health_bar = HealthBar(550, screen_height - bottom_panel + 100, enemy2.hp, enemy2.max_hp)

#create buttons
# Potion button to use potion
pot_butt = Button(screen, 100, screen_height - bottom_panel + 70, potion_img, 64, 64)
# Restart button to restart game when it's gme over
r_butt = Button(screen, 330, 120, restart_img, 120, 30)

# The loop to run the whole game 
run = True
while run:

	clock.tick(fps)

	#draw background
	draw_bg()

	#draw panel
	draw_panel()
	Player_health_bar.draw(Player.hp)
	enemy1_health_bar.draw(enemy1.hp)
	enemy2_health_bar.draw(enemy2.hp)

	#draw fighters
	Player.update()
	Player.draw()
	for bandit in enemyL:
		bandit.update()
		bandit.draw()

	#draw the damage text
	damage_text_group.update()
	damage_text_group.draw(screen)

	#control player actions
	#reset action variables
	attack = False
	potion = False
	target = None
	#make sure mouse is visible
	pygame.mouse.set_visible(True)
	pos = pygame.mouse.get_pos()
	for count, enemies in enumerate(enemyL):
		if enemies.rect.collidepoint(pos):
			#hide mouse
			pygame.mouse.set_visible(False)
			#show sword in place of mouse cursor
			screen.blit(sword_img, pos)
            # Checking if the enemy is alive and if it's player turn so player can attack enemy
			if clicked == True and enemies.alive == True:
				attack = True
				target = enemyL[count]
	if pot_butt.draw():
		potion = True
	#show number of potions remaining
	draw_text(str(Player.pot), font, red, 150, screen_height - bottom_panel + 70)

    # Checking to see if the game is still running or is it over
	if game_over == 0:
		#player can take action if the game is still in play and the player is still alove
		if Player.alive == True:
			if current_fighter == 1:
				action_cooldown += 1
				if action_cooldown >= action_wait_time:
					#look for player action
					#attack the target only if you can attack it and there is a target
					if attack == True and target != None:
						Player.attack(target)
						current_fighter += 1
						action_cooldown = 0
					#potion
					if potion == True:
						if Player.pot > 0:
							#check if the potion would heal the player beyond max health 
                            # if potion heals player to beyond max health than it will calculate it so it does not go above max health
                            # and it will heal the player by that amount
							if Player.max_hp - Player.hp > potion_effect:
								heal_amount = potion_effect
							else:
								heal_amount = Player.max_hp - Player.hp
							Player.hp += heal_amount
							Player.pot -= 1
							damage_text = DamageText(Player.rect.centerx, Player.rect.y, str(heal_amount), green)
							damage_text_group.add(damage_text)
							current_fighter += 1
							action_cooldown = 0
		else:
            # You lost the game cause the player character is dead
			game_over = -1


		#enemy action
		for count, Enemies in enumerate(enemyL):
			if current_fighter == 2 + count:
				if Enemies.alive == True:
					action_cooldown += 1
					if action_cooldown >= action_wait_time:
						#check if enemy needs to heal 
                        # if the enemy is below half of its max hp and if the enemy still have potions if so heal the enemy
						if (Enemies.hp / Enemies.max_hp) < 0.5 and Enemies.pot > 0:
							#check if the potion would heal the Enemies beyond max health
                            # And calculate the healed amount
							if Enemies.max_hp - Enemies.hp > potion_effect:
								heal_amount = potion_effect
							else:
								heal_amount = Enemies.max_hp - Enemies.hp
							Enemies.hp += heal_amount
							Enemies.pot -= 1
							damage_text = DamageText(Enemies.rect.centerx, Enemies.rect.y, str(heal_amount), green)
							damage_text_group.add(damage_text)
							current_fighter += 1
							action_cooldown = 0
						else:
                            # Else the enemy just attack the Player
							Enemies.attack(Player)
							current_fighter += 1
							action_cooldown = 0
				else:
					current_fighter += 1

		#if all fighters have had a turn then reset
		if current_fighter > total_fighters:
			current_fighter = 1


	#check if all Enemies are dead
	alive_enemy = 0
	for enemies in enemyL:
		if enemies.alive == True:
			alive_enemy += 1
	if alive_enemy == 0:
        # You win if enemies is all dead
		game_over = 1


	#check if game is over
	if game_over != 0:
        # Displaying the victory screen and defeat screen
		if game_over == 1:
			screen.blit(victory_img, (250, 50))
		if game_over == -1:
			screen.blit(defeat_img, (290, 50))
        # Restart button so if you restart it will reset the game again
		if r_butt.draw():
			Player.reset()
			for bandit in enemyL:
				bandit.reset()
			current_fighter = 1
			action_cooldown
			game_over = 0



    # Event listener to stop the pygame and to check if the player click a button
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		if event.type == pygame.MOUSEBUTTONDOWN:
			clicked = True
		else:
			clicked = False
    
    #Update pygame display and show the pygame display
	pygame.display.update()
# End of pygame
pygame.quit()