import pygame as pyg
import random as rnd

#required
resolution = [640,360]

#start
pyg.init()
screen = pyg.display.set_mode(resolution)
clock = pyg.time.Clock()

#misc
def scaleup(img,scalex,scaley):
	return pyg.transform.scale(img, [img.get_width() * scalex, img.get_height() * scaley])
	
#onready
player = pyg.image.load("images/potato_guy.png").convert_alpha()
player = scaleup(player,4,4)
font = pyg.font.Font("fonts/pixel_game.otf",48)
background = pyg.image.load("images/background.png").convert_alpha()
background = scaleup(background,4,4)
ground = pyg.image.load("images/ground.png").convert_alpha()
ground = scaleup(ground,4,4)
bullet = pyg.image.load("images/bullet.png").convert_alpha()
bullet = scaleup(bullet,4,4)

pyg.mixer.music.load("music/bgm_1.ogg")
pyg.mixer.music.set_volume(0.5)
pyg.mixer.music.play(-1)
click = pyg.mixer.Sound("music/click.wav")
click.set_volume(0.3)
death = pyg.mixer.Sound("music/death.wav")
death.set_volume(0.3)

#variables
player_x = 0
player_y = 0
bullet_y_pos = rnd.uniform(250.0,300.0)
bullet_x_offset = 0
bullet_speed_increase = 0
jump_height = -15
y_vel = 0.0
onground = False
gravity = 0.8
score = 0
menu = True
death_played = False

#game loop
alive = True
running = True

while running:
	for event in pyg.event.get():
		if event.type == pyg.QUIT:
			running = False
		if event.type == pyg.MOUSEBUTTONDOWN and onground == True and alive and not menu:
		    onground = False
		    y_vel = jump_height
		if event.type == pyg.MOUSEBUTTONDOWN and not alive and not menu:
		    score = 0
		    bullet_speed_increase = 0
		    alive = True
		    bullet_x_offset = 0
		    death_played = False
		    click.play()
		if event.type == pyg.MOUSEBUTTONDOWN and menu:
		    menu = False
		    click.play()
    
			
	#game logic
	screen.fill("white")
	screen.blit(background,(0,0))
		
	## physics
	y_vel += gravity
	player_y += y_vel
	
	if player.get_height() + player_y >= 328:
	    player_y = 328 - player.get_height()
	    y_vel = 0
	    onground = True
	

		
	## player
	screen.blit(player,(player_x,player_y))
	
	## ground
	screen.blit(ground,(0,328))
	
	## bullet
	screen.blit(bullet,(650 - bullet_x_offset,bullet_y_pos))
	if alive and not menu:
	    bullet_x_offset += 5 +    bullet_speed_increase
	    bullet_speed_increase += 0.001
	        
	
	## death
	if 650 - bullet_x_offset >= player_x and 650 - bullet_x_offset <= player.get_width() + player_x and bullet_y_pos >= player_y and bullet_y_pos <= player_y + player.get_height():
	    alive = False
	    if not death_played:
	        death.play()
	        death_played = True
	 
	## score
	if 650 - bullet_x_offset < player_x:
	    score += 1
	    bullet_x_offset = 0
	    bullet_y_pos = rnd.uniform(280.0,290.0)
	score_text = font.render(f"score: {score}",True,"white")
	score_outline = font.render(f"score: {score}",True,"black")
	screen.blit(score_outline,(15,15))
	screen.blit(score_text,(10,10))
	
	## deathscreen
	if not alive:
	    reset_text = font.render("game over!",True,"#ffaa00")
	    reset_outline = font.render("game over!",True,"black")
	    screen.blit(reset_outline,(225,155))
	    screen.blit(reset_text,(220,150))
	
	## menu
	menu_title = font.render("BULLET JUMPS",True,"white")
	menu_title_outline = font.render("BULLET JUMPS",True,"black")
	menu_subtitle = font.render("click to start",True,"#808080")
	if menu:
	    screen.blit(menu_title_outline,(225,105))
	    screen.blit(menu_title,(220,100))
	    screen.blit(menu_subtitle,(220,200))
	
	#update screen
	pyg.display.flip()
	
	#time stuff
	clock.tick(60)
	
	
pyg.quit()