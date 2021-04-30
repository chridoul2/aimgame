import pygame
import sys
import random
import math
import os
import neat


BLACK = (0, 0, 0)
RED = (255, 0, 0)


YELLOW = (255 ,255,0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (230, 230, 230)
ORANGE = (240,136,0)
WHITE = (255,255,255)
PURPLE = (230,0,255)
PINK = (255,153,204)
DARKGREEN = (0,34,0)
DARKRED = (34,0,0)
DARKBLUE = (0,0,34)
GOLD = (255,200,0)



LIGHTBLUE = (185,220,218)
color_light = (170,170,170)
color_dark = (100,100,100)
colors = [YELLOW,GREEN,GRAY,ORANGE,BLUE,PURPLE,PINK,WHITE,DARKGREEN,DARKRED,DARKBLUE,GOLD]


width = 1920
height = 1080
background_color = (0,50,100)

gen = 0

pygame.init()

pygame.font.init()
sysfont = pygame.font.get_default_font()

pygame.event.set_grab(False) # confines the mouse cursor to the window

class Player:

    #Player class presentint the yellow circle
    def __init__(self, x , y ):

        self.x = x
        self.y = y
        self.color  = (0,0,0)
        self.score  = 0
        self.distance = 0
        self.oldDistance = 99999

    def draw(self, win):

        pygame.draw.circle(win, YELLOW,(self.x,self.y),15)
        # popNumberText,popNumberTextRect = drawText(str(popNumber),'Arial',35,win,RED,0 ,0)
        # popNumberTextRect.center = [self.x,self.y]
        # screen.blit(popNumberText, popNumberTextRect)

    def move(self, up,right,down,left):

        if(up == True ):
            self.y -= 1
        elif(right == True):
            self.x += 1
        elif(down == True):
            self.y += 1
        elif(left == True):
            self.x -= 1 

def resource_path(relative_path):
    try:
    # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def win(width,height):
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('pygame_window')
    # screen.fill(background_color) #This syntax fills the background with a color 
    

def drawText(text,font,fontSize,screen,color,posx,posy):
   
    font = pygame.font.SysFont(font, fontSize)
    title = font.render(text, True, color)
    titleRect = title.get_rect()
    titleRect.center =(posx , posy)
    
    
    return title,titleRect

def randomCircle(screen,color,radius):
    #rand = random.sample(range(100, 700), 2)
    pos = [100,100]

    pygame.draw.circle(screen,color,rand,radius)
    return pos

   

def eval_genomes(genomes, config):
   
    global gen
    clock = pygame.time.Clock()
    game = False # bool that indiocates if we are int the game or in the start menu
   
    diff=75 # radius of the red circle or difficulty of the game
    timer = 15
    dt = 0

    gen += 1

    count =0


    

    click = False

    players = []
    ge = []
    nets = []


    for genome_id, genome in genomes:
        genome.fitness = 0  # start with fitness level of 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        ge.append(genome)
        players.append(Player(960,540))
    
    for player in players:
        col = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
        player.color = col


    # colorsPallete = []

    # for x in 25:
    #     colorsPallete.append((random.randint(0,255),(random.randint(0,255),(random.randint(0,255)))

        
    
    
    
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('pygame_window')

    
    randx = random.randint(50, width-diff)
    randy = random.randint(100, height-diff)
    
    
    run = True
    while run:
        # pygame.time.delay(60)
        timer -= dt 

        # if len(players) == 0:
        #     break
       
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                    pygame.quit() 
                # if event.key == pygame.K_SPACE:
                #     run = False 

        #prints
            
                
                # pygame.event.set_grab(True)
                
                # #print("game is running")
                # pygame.mouse.set_cursor(*pygame.cursors.broken_x)
            #pygame.mouse.set_visible(False)
        screen.fill(LIGHTBLUE)

        pygame.draw.rect(screen,GRAY,(0,0,width,50))


        timeText,timeTextRect = drawText('Time:' + str(round(timer, 2)),'Arial',35,screen,RED,0 ,50)
        timeTextRect.topleft = [0,10]
        screen.blit(timeText, timeTextRect)

        playersAliveText,playersAliveTextRect = drawText('Players Alive:' + str(count),'Arial',35,screen,RED,0 ,50)
        playersAliveTextRect.midtop = [width/2,10]
        screen.blit(playersAliveText, playersAliveTextRect)


        genText,genTextRect = drawText('Gen:' + str(gen),'Arial',35,screen,RED,0 ,50)
        genTextRect.topright = [width-20,10]
        screen.blit(genText, genTextRect)

        c = 0   
        if timer <= 0:
            
            for player in players:
                print(len(players))
                print("\t")
                nets.pop(players.index(player))
                ge.pop(players.index(player))
                players.pop(players.index(player))
            timer = 15
            # break
                    


            
        

        
        
        pygame.draw.circle(screen,RED,(randx,randy),diff)

        for player in players:
            if players.index(player) == 0:
                count =1
            else:
                count +=1

            pygame.draw.line(screen,RED,(player.x,player.y),(randx,randy),2)

            pygame.draw.circle(screen,player.color,(player.x,player.y),20)
            
            # popNumberText,popNumberTextRect = drawText(str(players.index(player)),'Arial',15,screen,RED,0 ,0)
            # popNumberTextRect.center = [player.x-6,player.y]
            # screen.blit(popNumberText, popNumberTextRect)

            scoreText,scoreTextRect = drawText(str(player.score),'Arial',20,screen,RED,0 ,0)
            scoreTextRect.center = [player.x,player.y]
            screen.blit(scoreText, scoreTextRect)



            if player.y<50 or player.y >1070 or player.x< 10 or player.x>1910:
                ge[players.index(player)].fitness -= 10
                ge.pop(players.index(player))
                nets.pop(players.index(player))
                players.pop(players.index(player))


        for player in players:
            player.distance = math.sqrt((player.x -randx)**2 + (player.y - randy)**2)

            if player.distance < player.oldDistance:
                ge[players.index(player)].fitness += 200
            elif player.distance > player.oldDistance:
                ge[players.index(player)].fitness -= 50
            else :
                ge[players.index(player)].fitness -= 10
                ge.pop(players.index(player))
                nets.pop(players.index(player))
                players.pop(players.index(player))


            

            widthDiff = abs(player.x-randx)
            heightDiff = abs(player.y-randy)

        # print(str(widthDiff) + "  " + str(heightDiff))

        for player in players:
            output = nets[players.index(player)].activate((player.score,player.distance))

            


            if output[0] > 0.5:#up
                player.y -=5
            if output[1] > 0.5:#right
                player.x +=5
            if output[2] > 0.5:#left
                player.x -=5
            if output[3] > 0.5:#down
                player.y +=5
            if output[4] > 0.5:#click
                click = True


            
            if player.distance < diff:
                ge[players.index(player)].fitness += 100
                if click == True:
                    ge[players.index(player)].fitness += 150
                    player.score +=1
                    randx = random.randint(50, width-diff)
                    randy = random.randint(100, height-diff)
                    click = False
                
            player.oldDistance = player.distance
        
        
        dt = clock.tick(30) / 1000 # / 1000 to convert to seconds.
        click = False
        pygame.display.update() 




def run(config_file):
    """
    runs the NEAT algorithm to train a neural network to play flappy bird.
    :param config_file: location of config file
    :return: None
    """
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    #p.add_reporter(neat.Checkpointer(5))

    # Run for up to 50 generations.
    winner = p.run(eval_genomes, 100)

    # show final stats
    print('\nBest genome:\n{!s}'.format(winner))


if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'aimgame_config.txt')
    run(config_path)
