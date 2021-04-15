import pygame
import random
import os
import time
import neat
import math
pygame.font.init()  # init font

WIN_WIDTH = 1920    
WIN_HEIGHT = 1080

FONT = pygame.font.SysFont("Arial", 40)


BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255 ,255,0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (230, 230, 230)
LIGHTBLUE = (185,220,218)

WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Aim Game Neat")

gen = 0

class Player:

    #Player class presentint the yellow circle
    def __init__(self, x , y , output):

        self.x = x
        self.y = y
        self.color  = YELLOW
        self.score  = 0
        self.distance = 0
        self.oldDistance = -99999
        self.output = {0,0,0,0,0}

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

class Target:

    def __init__(self, x , y):

        self.x = x
        self.y = y
        self.color  = RED 
        self.radius = 50

    def randomTarget(self):
        self.x = random.randint(50, WIN_WIDTH-self.radius)
        self.y = random.randint(100, WIN_HEIGHT-self.radius)
        pygame.draw.circle(win, YELLOW,(self.x,self.y),15)
        
    
    def draw(self, win , posx, posy):
        pygame.draw.circle(win, self.color,(posx,posy),self.radius)




def draw_window(win,players, target, gen , time):

    if gen == 0:
        gen = 1

    win.fill(LIGHTBLUE)

   

    pygame.draw.rect(win,GRAY,(0,0,WIN_WIDTH,50))


    pygame.draw.circle(win, RED,(target.x,target.y),target.radius)


    for player in players:# draw all the players from population
        player.draw(win)
    # score
    # score_label = FONT.render("Score: " + str(score),1,(255,255,255))
    # win.blit(score_label, (WIN_WIDTH - score_label.get_width() - 15, 10))

    # generations
    score_label = FONT.render("Gens: " + str(gen-1),1,(255,255,255))
    win.blit(score_label, (10, 0))


    #time 
    timeLabel = FONT.render('Time:' + str(time),1,(255,255,255))
    win.blit(timeLabel, (1700, 0))
    

    pygame.display.update()

def drawText(text,font,fontSize,screen,color,posx,posy):
   
    font = pygame.font.SysFont(font, fontSize)
    title = font.render(text, True, color)
    titleRect = title.get_rect()
    titleRect.center =(posx , posy)
    
    
    return title,titleRect

def eval_genomes(genomes, config):

    global WIN, gen
    win = WIN
    gen += 1

    nets = []
    ge = []
    players = []

    timer = 45
    dt = 0

    test  = {0,0,0,0,0}

    targetX = random.randint(50, WIN_WIDTH-50)
    targetY = random.randint(100, WIN_HEIGHT-50)

    target = Target(targetX, targetY)

    for genome_id, genome in genomes:
        genome.fitness = 0  # start with fitness level of 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        players.append(Player(960,540,test))
        ge.append(genome)
    

    print(len(players))
    print(len(ge))

    score = 0
    click  = False
    clock = pygame.time.Clock()

    run = True
    while run and len(players) > 0:


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                    pygame.quit()
            
        timer -= dt
        if timer <= 0:
            timer = 45
            for player in players:
                nets.pop(players.index(player))
                ge.pop(players.index(player))
                players.pop(players.index(player))
                player.score = 0


        # target.draw(win, targetX, targetY)


        # pygame.draw.circle(win, RED,(targetX,targetY),50)

        for player in players:
            if(players.index(player) < 20):
                
            geNumber,geNumberRect = drawText(str(players.index(player)),'Arial',10,win,RED,700 ,50)
            geNumberRect.center = [player.x,player.y]
            win.blit(geNumber, geNumberRect)
            

            if player.x < 50 or player.x > 1870 or player.y < 50 or player.y >1030:
                ge[players.index(player)].fitness -= 5
            if player.x <= 0 or player.x >= 1920 or player.y <= 0 or player.y >=1080: 
                nets.pop(players.index(player))
                ge.pop(players.index(player))
                players.pop(players.index(player))
                player.score = 0



            player.distance = math.sqrt((player.x -target.x)**2 + (player.y - target.y)**2)



            #print(player.distance)
            # if player.distance > player.oldDistance:
            #     print(players.index(player))
            #     ge[players.index(player)].fitness += 15
            # else:
            #     ge[players.index(player)].fitness -= 20
                

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
               # print(str(widthDiff) + "  " + str(heightDiff))


            output = nets[players.index(player)].activate((player.score,player.distance))

                
            




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
            
            if player.distance < target.radius:
                ge[players.index(player)].fitness += 40
                if click == True:
                    target.x = random.randint(50, WIN_WIDTH-target.radius)
                    target.y = random.randint(100, WIN_HEIGHT-target.radius)
                    player.score += 1
                    ge[players.index(player)].fitness += 50
                    click = False
                else:
                    ge[players.index(player)].fitness -= 10 
                
            player.oldDistance = player.distance
        
        win.fill(LIGHTBLUE)

   

        pygame.draw.rect(win,GRAY,(0,0,WIN_WIDTH,50))


        pygame.draw.circle(win, RED,(target.x,target.y),target.radius)


        for player in players:# draw all the players from population
            player.draw(win)
   
    # generations
        score_label = FONT.render("Gens: " + str(gen-1),1,(255,255,255))
        win.blit(score_label, (10, 0))


        #time 
        timeLabel = FONT.render('Time:' + str(time),1,(255,255,255))
        win.blit(timeLabel, (1700, 0))
        

        pygame.display.update()
        
        
        
        dt = clock.tick(30) / 1000  # / 1000 to convert to seconds
        click = False


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
    winner = p.run(eval_genomes, 50)

    # show final stats
    print('\nBest genome:\n{!s}'.format(winner))


if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'aimgame_config.txt')
    run(config_path)
                