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
LIGHTBLUE = (185,220,218)
color_light = (170,170,170)
color_dark = (100,100,100)


width = 1920
height = 1080
background_color = (0,50,100)

pygame.init()

pygame.font.init()
sysfont = pygame.font.get_default_font()

pygame.event.set_grab(True) # confines the mouse cursor to the window

class Player:

    #Player class presentint the yellow circle
    def __init__(self, x , y ):

        self.x = x
        self.y = y
        self.color  = YELLOW
        self.score  = 0
        self.distance = 0
        self.oldDistance = -99999

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
   
    clock = pygame.time.Clock()
    game = False # bool that indiocates if we are int the game or in the start menu
    score = 0
    into = True
    inside =0 # counter for the times that  the target was hit
    count=0
    diff=75 # radius of the red circle or difficulty of the game
    timeValue = 45#default value
    time = 45
    accuracy = 0.00 # accurac for the player 
    gameCounter  = 0


    

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
    
    
    
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('pygame_window')

    
    randx = random.randint(50, width-diff)
    randy = random.randint(100, height-diff)
    
    
    run = True
    while run:
        # pygame.time.delay(60)
        
       
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                    pygame.quit() 

        #prints
            
                
                # pygame.event.set_grab(True)
                
                # #print("game is running")
                # pygame.mouse.set_cursor(*pygame.cursors.broken_x)
                #pygame.mouse.set_visible(False)
            screen.fill(LIGHTBLUE)

            pygame.draw.rect(screen,GRAY,(0,0,width,50))

            scoreText,scoreTextRect = drawText('Score: ' + str(score),'Arial',35,screen,RED,700 ,50)
            scoreTextRect.topright = [width-50,10]
            screen.blit(scoreText, scoreTextRect)

            if event.type == pygame.USEREVENT: 
                counter -= 1
                if counter > 0:
                    time = str(counter).rjust(3)  
                else:

                    counter = timeValue
                    for player in players:
                        players.pop(players.index(player))
                        ge.pop(players.index(player))
                        nets.pop(players.index(player))
                    


            timeText,timeTextRect = drawText('Time:' + str(time),'Arial',35,screen,RED,0 ,50)
            timeTextRect.topleft = [0,10]
            screen.blit(timeText, timeTextRect)

            # gameCounterText,gameCounterTextRect = drawText('Game:' + str(gameCounter + 1) + "/ " + str(runs),'Arial',35,screen,RED,0 ,50)
            # gameCounterTextRect.topleft = [250,10]
            # screen.blit(gameCounterText, gameCounterTextRect)
            
            # if count!=0:
            #     accuracy = (inside/count)*100
            #     #print(inside, "/", count)
            #     accText,accTextRect = drawText('Accuracy: ' + "{:.1f}".format(accuracy) + "%",'Arial',35,screen,RED,0 ,50)
            #     accTextRect.midtop = [width-400,10]
            #     screen.blit(accText, accTextRect)
            

            
            
            pygame.draw.circle(screen,RED,(randx,randy),diff)

            for player in players:
                pygame.draw.circle(screen, YELLOW,(player.x,player.y),15)



                if player.y<50 or player.y >1070 or player.x< 10 or player.x>1910:
                    ge[players.index(player)].fitness -= 10



                player.distance = math.sqrt((player.x -randx)**2 + (player.y - randy)**2)

                if player.distance > player.oldDistance:
                    ge[players.index(player)].fitness += 15
                else:
                    ge[players.index(player)].fitness -= 20
                

                widthDiff = abs(player.x-randx)
                heightDiff = abs(player.y-randy)

            # print(str(widthDiff) + "  " + str(heightDiff))


                output = nets[players.index(player)].activate((score,widthDiff, heightDiff))

                
                if player.distance < 1000 :
                    ge[players.index(player)].fitness += 2
                elif player.distance < 800 :
                    ge[players.index(player)].fitness += 5
                elif player.distance < 500 :
                    ge[players.index(player)].fitness += 8
                elif player.distance < 200 :
                    ge[players.index(player)].fitness += 10
                elif player.distance < 100 :
                    ge[players.index(player)].fitness += 15




                if output[0] > 0.5:#up
                    player.y -=5
                elif output[1] > 0.5:#right
                    player.x +=5
                elif output[2] > 0.5:#left
                    player.x -=5
                elif output[3] > 0.5:#down
                    player.y +=5
                elif output[4] > 0.5:#click
                    click = True


                
                #if event.type == pygame.MOUSEBUTTONDOWN:
                    #ge[gameCounter].fitness += 1
                    #print('inside')
                count+=1
                if player.distance < diff:
                    ge[players.index(player)].fitness += 40
                    if click == True:
                        randx = random.randint(50, width-diff)
                        randy = random.randint(100, height-diff)
                        ge[players.index(player)].fitness += 50
                        click = False
                    else:
                        ge[players.index(player)].fitness -= 10 
                    
                player.oldDistance = player.distance
            
            

            pygame.display.update() 

    

sys.exit


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
    winner = p.run(eval_genomes, 20)

    # show final stats
    print('\nBest genome:\n{!s}'.format(winner))


if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'aimgame_config.txt')
    run(config_path)
