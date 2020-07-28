#main.py
#pip install pygame
#pip3 install pygame
#python3 -m pip install pygame
#C:\Python38\python.exe -m pip install pygame

import pygame
import math #หา square root
import random
import csv


pygame.init() #เซ็ตอัพเริ่มต้นให้ pygame ทำงาน

WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH,HEIGHT)) #ปรับขนาดหน้าจอหลัก
pygame.display.set_caption('T3ammy VS Covid-19') #ตั้งชื่อเกมส์

icon = pygame.image.load('icon.png') #โหลดไฟล์ img
pygame.display.set_icon(icon) #สั่งเซ็ตรูปภาพที่ชื่อเกมส์

background = pygame.image.load('background.png') #โหลด background

########### FONT ###########
fontscore = pygame.font.Font('BLS-Bold.ttf',20)
fontover = pygame.font.Font('BLS-Bold.ttf',80)
fonttext = pygame.font.Font('BLS-Bold.ttf',60)

########### OBJECT - T3AMMY ############ 1 - player - t3ammy.png
psize = 128 #ความกว้างของ img

pimg = pygame.image.load('t3ammy.png')
px = 100 #จุดเริ่มต้นแกน X (แนวนอน)
py = HEIGHT - psize #จุดเริ่มต้นแกน Y (แนวตั้ง)
pxchange = 0

def Player(x,y):
	screen.blit(pimg,(x,y)) #blit = วางภาพในหน้าจอ

########### OBJECT - ENEMY ############ 2 - enemy - virus.png
### SINGLE ENEMY
esize = 64

epic = 'virus.png'
eimg = pygame.image.load(epic)
ex = 50
ey = esize
eychange = 1

def Enemy(x,y):
	screen.blit(eimg,(x,y))

### MULTI ENEMY
exlist = [] #ตำแหน่งแกน x ของ enemy
eylist = [] #ตำแหน่งแกน y ของ enemy
eychange_list = [] #ความเร็ว enemy
allenemy = 4 #จำนวนของ enemy ทั้งหมด

for i in range(allenemy):
	exlist.append(random.randint(0, WIDTH - esize))
	eylist.append(random.randint(0,50))
	# eychange_list.append(random.randint(1,5)) #สุ่มความเร็วให้ enemy
	eychange_list.append(1) #กำหนดความเร็วเป็น 1 ก่อนแล้วค่อยเพิ่มหลังจากยิงโดน

########### OBJECT - MASK ############ 3 - mask - mask.png
msize = 32

mimg = pygame.image.load('mask.png')
mx = 100
my = HEIGHT - psize
mychange = 20 #ปรับความเร็วของ layer
mstate = 'ready' #เซ็ต state พร้อมยิง

def Fire_mask(x,y):
	global mstate

	mstate = 'fire' #เซ็ต state ยิง
	screen.blit(mimg,(x,y))

########### OBJECT - ITEM ########### 4 - item(apple) - apple.png
isize = 64

iimg = pygame.image.load('apple.png')
ix = random.randint(0, WIDTH - isize)
iy = 0
iychange = 5
istate = 'deactive'

def Item(x,y):
	screen.blit(iimg,(x,y))

########### OBJECT - LIFE ########### 5 - life - heart.png
life = 3

limg = pygame.image.load('heart.png')
lx = 700
ly = 20

def Life(x,y):
	screen.blit(limg,(x,y))

########### OBJECT - SOUND ###########
pygame.mixer.Channel(0).play(pygame.mixer.Sound('virusaleart.wav')) #start sound

def bgsound():
	pygame.mixer.music.load('bgsound.mp3') #backgroud sound
	pygame.mixer.music.set_volume(0.2) #ความดังของเสียง
	pygame.mixer.music.play(loops=-1) #-1 คือ loop forever

bgsound()
	
########### FUNCTION - COLLISION ENEMY ###########
def isCollision(ecx,ecy,mcx,mcy):
	#เช็คว่า Mask กับ Enemy ชนกันหรือไม่? หากชนให้บอกว่า True
	dte = math.sqrt(math.pow(ecx - mcx,2)+math.pow(ecy - mcy,2)) #distance enemy
	# print('DISTANCE:',dte)

	if dte < ((esize/2) + (msize/2)): #ระยะที่ชนกัน
		return True
	else:
		return False

########### FUNCTION - COLLISION ITEM ###########
playsoundItem = False

def isCollisionItem(icx,icy,pcx,pcy):

	dti = math.sqrt(math.pow(icx - pcx,2)+math.pow(icy - pcy,2)) #distance item
	if dti < ((isize/2) + (psize/2)): #ระยะที่ชนกัน
		return True
	else:
		return False

########### FUNCTION - SCORE ###########
allscore = 0

def Showscore():
	ReadHighScore()

	highscore = fontscore.render('High Score: {} Point'.format(filecsv[0][1]),True,(219,13,133))
	screen.blit(highscore,(10,5))

	score = fontscore.render('Your Score: {} Point'.format(allscore),True,(252,174,5))
	screen.blit(score,(10,30))

def AddHighScore():
	ReadHighScore()

	if allscore > int(filecsv[0][1]):
		with open('score.csv','w', newline='') as file: 
			writer = csv.writer(file)
			writer.writerow(['highscore',allscore])

def ReadHighScore():
	global filecsv

	filecsv = []

	with open('score.csv','r') as file:
		reader = csv.reader(file)
		for r in reader:
			filecsv.append(r)
		# print(filecsv)

########### FUNCTION - PAUSED ###########
pause = False

def Paused():
	global pause
	
	# print(pause)

	while pause:
		for event in pygame.event.get():
			if event.type == pygame.QUIT: #ถ้ากดกากบาทให้ปิดเกมส์
				pause = False
				
			elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
				pause = not pause
				# print(pause)

########### FUNCTION - GAME BREAK ###########
continueus = True

def GameBreak():
	global life
	global continueus

	life -= 1

	breaktext = fonttext.render('Press [C] for Continue...',True,(134,4,181))
	screen.blit(breaktext,(60,200))

	newtext = fonttext.render('Press [N] for New Game',True,(39,27,150))
	screen.blit(newtext,(60,300))

	continueus = False

########### FUNCTION - GAME OVER ###########
playsoundOver = False
gameover = False


def GameOver():
	global playsoundOver
	global continueus

	overtext = fontover.render('Game Over',True,(255,0,0))
	screen.blit(overtext,(200,200))

	newtext = fonttext.render('Press [N] for New Game',True,(39,27,150))
	screen.blit(newtext,(60,300))

	if playsoundOver == False:

		pygame.mixer.music.load('gameover.wav') #game over sound
		pygame.mixer.music.set_volume(0.5) #ความดังของเสียง
		pygame.mixer.music.play()

		playsoundOver = True
		continueus = False

	AddHighScore()

############################################ GAME LOOP ############################################
running = True #บอกให้โปรแกรมทำงาน

clock = pygame.time.Clock() #game clock

FPS = 30 #frame rate

while running:
			
	for event in pygame.event.get(): #เช็ค event ที่เกิดขึ้น
		if event.type == pygame.QUIT: #ถ้ากดกากบาทให้ปิดเกมส์
			running = False

		if event.type == pygame.KEYDOWN: #ถ้ามีการกดปุ่ม
			if event.key == pygame.K_LEFT:
				pxchange = -10
				if istate == 'active':
					pxchange += -20

			if event.key == pygame.K_RIGHT:
				pxchange = 10
				if istate == 'active':
					pxchange += 20
				
			if event.key == pygame.K_SPACE:
				if mstate == 'ready':

					pygame.mixer.Channel(1).play(pygame.mixer.Sound('laser.wav')) #laser sound
					
					mx = px + (psize/2) - (msize/2) #ขยับให้ยิง mask ออกจากหัว
					Fire_mask(mx,my)

			if event.key == pygame.K_c:

				if continueus == False:
					istate = 'deactive'
					for i in range(allenemy):
						eychange_list[i] = 1
						exlist[i] = random.randint(0, WIDTH - esize)
						eylist[i] = random.randint(0,50)
					continueus = True

			if event.key == pygame.K_n:
				allscore = 0
				life = 3
				playsoundOver = False
				gameover = False
				istate = 'deactive'
				iy = 0
				continueus = True
				bgsound()
				
				for i in range(allenemy):
					eychange_list[i] = 1
					exlist[i] = random.randint(0, WIDTH - esize)
					eylist[i] = random.randint(0,50)

			if event.key == pygame.K_p:
				pause = not pause
				Paused()
				

					
		if event.type == pygame.KEYUP: #ถ้ามีการปล่อยปุ่ม

			if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
				pxchange = 0

	######## RUN SHOWSCORE ########
	Showscore()

	######## RUN PLAYER ########
	Player(px,py) #px, py คือจุดเริ่มต้นของ player

	#ทำให้ player ขยับ ซ้าย-ขวา
	if px <= 0:
		#หากชนขอบจอซ้าย ให้ปรับค่า pxchange เป็น +5
		# pxchange = 5
		px = 0
		px += pxchange
	elif px >= WIDTH - psize: #WIDTH  (ความกว้างของหน้าจอ - ความกว้างของภาพ t3ammy)
		#หากชนขอบจอขวา ให้ปรับค่า pxchange เป็น -5
		# pxchange = -5
		px = WIDTH - psize
		px += pxchange
	else:
		#หากอยู่ระหว่างหน้าจอ ให้ทำการ บวก/ลบ ตามค่า pxchange ที่เปลี่ยนไปใน if-elif
		px += pxchange
		# print('PX:',px)

	######## RUN LIFE ########
	Life(lx,ly)
	# print('LIFE:',life)
	fontlife = pygame.font.Font('BLS-Bold.ttf',20)

	if gameover == False:
		flife = fontlife.render('x {}'.format(life),True,(39,27,150))
		screen.blit(flife,(730,15))

		flife = fontlife.render('Press "P" to Pause',True,(39,27,150))
		screen.blit(flife,(600,HEIGHT - 45))
	elif gameover == True:
		flife = fontlife.render('x 0',True,(39,27,150))
		screen.blit(flife,(730,15))

	######## RUN ENEMY SINGLE ########
	# for i in range(5):
	# 	Enemy(ex + (i*100),ey)
	############
	# Enemy(ex,ey)
	# ey += eychange

	######## COLLISION SINGLE ########
	# collision = isCollision(ex,ey,mx,my) #เช็คว่า Mask กับ Enemy ชนกันหรือไม่? หากชนให้บอกว่า True
	# if collision:
	# 	my = HEIGHT - psize
	# 	mstate = 'ready'
	# 	ey = 0
	# 	ex = random.randint(0, WIDTH - esize) #สุ่มตำแหน่ง ex ของ enemy
	# 	allscore += 1

	######## RUN MULTI ENEMY ########
	# print('EYCHENG_LIST:',eychange_list)
	for i in range(allenemy):
		
		
		Enemy(exlist[i],eylist[i])
		######## RUN GAME BREAK and OVER ########
		
		# print('EYLIST:',eylist)
		if eylist[i] > HEIGHT - esize and life > 1 and gameover == False:
			# print('EYLIST:',eylist[i])
			pygame.mixer.Channel(3).play(pygame.mixer.Sound('gamebreak.wav')) #game break sound
			# pygame.mixer.Channel(3).set_volume(0.5) #ความดังของเสียง
			for i in range(allenemy):
				eylist[i] = 0
			# Paused()
			GameBreak()
			# print(life)
			# break
			
		elif eylist[i] > HEIGHT - esize and life == 1 and gameover == False:
			gameover = True


		elif eylist[i] > HEIGHT - esize and gameover == True:
			# print('EYLIST:',eylist[i])
			iy = 1000
			for i in range(allenemy):
				eylist[i] = 1000
			GameOver()
			# break

			
		######## COLLISION ENEMY MULTI ########
		collisionmulti = isCollision(exlist[i],eylist[i],mx,my)
		if collisionmulti:
			my = HEIGHT - psize
			mstate = 'ready'
			eylist[i] = 0
			exlist[i] = random.randint(0, WIDTH - esize) #สุ่มตำแหน่ง ex ของ enemy
			allscore += 1
			eychange_list[i] += 1 #เพิ่มความเร็วของ enemy เพิ่มขึ้น 1 step

			pygame.mixer.Channel(2).play(pygame.mixer.Sound('broken.wav')) #broken sound
			pygame.mixer.Channel(2).set_volume(0.3)

		eylist[i] += eychange_list[i] #สุ่มความเร็วของ enemy

	######## RUN ITEM ########
	# bonus = [5,10,15,20]

	if istate == 'deactive' and allscore != 0 and allscore >=5:
		Item(ix,iy)
		iy += iychange

		######## COLLISION ITEM ########
		collisionitem = isCollisionItem(ix,iy,px,py)
		if collisionitem:
			iy = 1000
			life += 1
			istate = 'active'
			# print('ISTATE:',istate)

			if playsoundItem == False:
				osound = pygame.mixer.Sound('item.wav')
				osound.set_volume(0.2)
				osound.play()

				playsoundItem = True

	######## RUN FIRE MASK ########
	if mstate == 'fire':
		Fire_mask(mx,my)
		my -= mychange #my = my - mychange #ทำให้กระสุน mask เราขยับ

	if my <= 0: #เช็คว่า Mask วิ่งชนขอบบนแล้วหรือยัง? ถ้าชนให้ปรับ state เป็น ready
		my = HEIGHT - psize
		mstate = 'ready'

	# print('PX:',px)
	pygame.display.update()
	pygame.display.flip()
	pygame.event.pump()
	screen.fill((0,0,0,))
	screen.blit(background,(0,0))
	clock.tick(FPS)
