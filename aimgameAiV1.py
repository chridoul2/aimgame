import pygame
import sys
import random
import math
import os
import neat


BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (0 ,255 ,255)
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
    game = False
    score = 0
    into = True
    inside =0
    count=0
    diff=75
    timeValue = 45#default value
    accuracy = 0.00
    gameCounter  = 0
    
    ge = []
    nets = []

    for genome_id, genome in genomes:
        genome.fitness = 0  # start with fitness level of 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        ge.append(genome)
    
    
    
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('pygame_window')

    
    randx = random.randint(50, width-diff)
    randy = random.randint(100, height-diff)
    
    randomCircle
    
    run = True
    while run:
        # pygame.time.delay(60)
        
         mouse= pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                    pygame.quit() 

        #prints
            if(game==True and gameCounter < 20):
                
                pygame.event.set_grab(True)
                
                #print("game is running")
                pygame.mouse.set_cursor(*pygame.cursors.broken_x)
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
                        #game=False
                        gameCounter +=1
                        score  = 0
                        count = 0
                        inside =0
                        counter = timeValue
                        ge.pop(gameCounter)
                        nets.pop(gameCounter)
                        pygame.mouse.set_pos([960,540])

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        setx= pygame.mouse.get_pos()[0]
                        sety = pygame.mouse.get_pos()[1] - 1
                        pygame.mouse.set_pos([setx,sety])
                    if event.key == pygame.K_DOWN:
                        setx= pygame.mouse.get_pos()[0]
                        sety = pygame.mouse.get_pos()[1] + 1
                        pygame.mouse.set_pos([setx,sety])
                    if event.key == pygame.K_RIGHT:
                        setx= pygame.mouse.get_pos()[0] +1
                        sety = pygame.mouse.get_pos()[1]
                        pygame.mouse.set_pos([setx,sety])
                    if event.key == pygame.K_LEFT:
                        setx= pygame.mouse.get_pos()[0] -1
                        sety = pygame.mouse.get_pos()[1]
                        pygame.mouse.set_pos([setx,sety])


                timeText,timeTextRect = drawText('Time:' + str(time),'Arial',35,screen,RED,0 ,50)
                timeTextRect.topleft = [0,10]
                screen.blit(timeText, timeTextRect)

                gameCounterText,gameCounterTextRect = drawText('Game:' + str(gameCounter + 1) + "/ 20",'Arial',35,screen,RED,0 ,50)
                gameCounterTextRect.topleft = [250,10]
                screen.blit(gameCounterText, gameCounterTextRect)
                
                if count!=0:
                    accuracy = (inside/count)*100
                    #print(inside, "/", count)
                    accText,accTextRect = drawText('Accuracy: ' + "{:.1f}".format(accuracy) + "%",'Arial',35,screen,RED,0 ,50)
                    accTextRect.midtop = [width-400,10]
                    screen.blit(accText, accTextRect)
                

                
                
                pygame.draw.circle(screen,RED,(randx,randy),diff)

                pygame.draw.circle(screen, YELLOW,(yellowCirclePosX,yellowCirlePosY),15)


                x = pygame.mouse.get_pos()[0]
                y = pygame.mouse.get_pos()[1]

                if y<50 or y >1070 or x< 10 or x>1910:
                    ge[gameCounter].fitness -= 10


                sqx = (x -randx)**2
                sqy = (y - randy)**2
                

                widthDiff = abs(x-randx)
                heightDiff = abs(y-randy)

               # print(str(widthDiff) + "  " + str(heightDiff))


                output = nets[gameCounter].activate((score,widthDiff, heightDiff))


                if(widthDiff < 800 or heightDiff < 800):
                    ge[gameCounter].fitness += 1
                elif(widthDiff < 500 or heightDiff < 500):
                    ge[gameCounter].fitness += 2
                elif(widthDiff < 200 or heightDiff < 200):
                    ge[gameCounter].fitness += 5



                if output[0] < 0.5:#up
                    setx= pygame.mouse.get_pos()[0]
                    sety = pygame.mouse.get_pos()[1] -1
                    pygame.mouse.set_pos([setx,sety])
                elif output[1] < 0.5:#right
                    setx= pygame.mouse.get_pos()[0]  + 1
                    sety = pygame.mouse.get_pos()[1] 
                    pygame.mouse.set_pos([setx,sety])
                elif output[2] > 0.5:#left
                    setx= pygame.mouse.get_pos()[0] -1 
                    sety = pygame.mouse.get_pos()[1]
                    pygame.mouse.set_pos([setx,sety])
                elif output[3] > 0.5:#down
                    setx= pygame.mouse.get_pos()[0]  
                    sety = pygame.mouse.get_pos()[1] + 1
                    pygame.mouse.set_pos([setx,sety])
                elif output[4] > 0.5:#click
                    pygame.mouse.get_pressed(1)


                
                #if event.type == pygame.MOUSEBUTTONDOWN:
                    #ge[gameCounter].fitness += 1
                    #print('inside')
                count+=1
                if math.sqrt(sqx + sqy) < 50:
                    ge[gameCounter].fitness += 40
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        randx = random.randint(50, width-diff)
                        randy = random.randint(100, height-diff)
                        score += 1
                        inside += 1
                        ge[gameCounter].fitness += 20
                    
                    else:
                        ge[gameCounter].fitness -= 10 
                    

                
            else:

                title,titleRect = drawText('AIM','Arial',48,screen,RED,width/2,100)
                start,startRect = drawText('Start','Corbel',48,screen,GREEN,width/2,height/2-100)

                diffText,diffTextRect = drawText('Difficulty','Arial',48,screen,RED,width/2,700)
                diff25,diff25Rect = drawText('25','Corbel',48,screen,RED,width/2-100,800)
                diff50,diff50Rect = drawText('50','Corbel',48,screen,RED,width/2,800)
                diff75,diff75Rect = drawText('75','Corbel',48,screen,RED,width/2+100,800)

                timeValueText,timeValueTextRect = drawText('Time','Arial',48,screen,RED,width/2,900)
                timeValueText15,timeValueTextRect15 = drawText('15','Corbel',48,screen,RED,width/2-100,1000)
                timeValueText30,timeValueTextRect30 = drawText('30','Corbel',48,screen,RED,width/2,1000)
                timeValueText45,timeValueTextRect45 = drawText('45','Corbel',48,screen,RED,width/2+100,1000)

                accMenu,accMenuRect = drawText('Accuracy: ' + "{:.1f}".format(accuracy) + "%",'Arial',48,screen,RED,300,300)
                scoreMenu,scoreMenuRect = drawText('Score: ' + str(score),'Arial',48,screen,RED,300,500)

                screen.fill(background_color) # fills the background with a color 
                screen.blit(title, titleRect)
                screen.blit(accMenu, accMenuRect)
                screen.blit(scoreMenu  , scoreMenuRect)
                screen.blit(diffText, diffTextRect)
                screen.blit(timeValueText, timeValueTextRect)

                #start button
                if(startRect.midleft[0] <= mouse[0] <= startRect.midright[0] and startRect.midtop[1] <= mouse[1] <= startRect.midbottom[1]):
                    pygame.draw.rect(screen,color_light,startRect)  
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        game=True
                        counter, time = timeValue, str(timeValue).rjust(3)
                        pygame.time.set_timer(pygame.USEREVENT, 1000)

                else:
                    pygame.draw.rect(screen,color_dark,startRect)

                #diff25 button
                if(diff25Rect.midleft[0] <= mouse[0] <= diff25Rect.midright[0] and diff25Rect.midtop[1] <= mouse[1] <= diff25Rect.midbottom[1]):
                    pygame.draw.rect(screen,color_light,diff25Rect)  
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        diff=25

                else:
                    pygame.draw.rect(screen,color_dark,diff25Rect)

                #diff50 button
                if(diff50Rect.midleft[0] <= mouse[0] <= diff50Rect.midright[0] and diff50Rect.midtop[1] <= mouse[1] <= diff50Rect.midbottom[1]):
                    pygame.draw.rect(screen,color_light,diff50Rect)  
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        diff=50

                else:
                    pygame.draw.rect(screen,color_dark,diff50Rect)

                #diff50 button
                if(diff75Rect.midleft[0] <= mouse[0] <= diff75Rect.midright[0] and diff75Rect.midtop[1] <= mouse[1] <= diff75Rect.midbottom[1]):
                    pygame.draw.rect(screen,color_light,diff75Rect)  
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        diff=75

                else:
                    pygame.draw.rect(screen,color_dark,diff75Rect)



                #time15 button
                if(timeValueTextRect15.midleft[0] <= mouse[0] <= timeValueTextRect15.midright[0] and timeValueTextRect15.midtop[1] <= mouse[1] <= timeValueTextRect15.midbottom[1]):
                    pygame.draw.rect(screen,color_light,timeValueTextRect15)  
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        timeValue=15

                else:
                    pygame.draw.rect(screen,color_dark,timeValueTextRect15)

                #time30 button
                if(timeValueTextRect30.midleft[0] <= mouse[0] <= timeValueTextRect30.midright[0] and timeValueTextRect30.midtop[1] <= mouse[1] <= timeValueTextRect30.midbottom[1]):
                    pygame.draw.rect(screen,color_light,timeValueTextRect30)  
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        timeValue=30

                else:
                    pygame.draw.rect(screen,color_dark,timeValueTextRect30)

                #time45 button
                if(timeValueTextRect45.midleft[0] <= mouse[0] <= timeValueTextRect45.midright[0] and timeValueTextRect45.midtop[1] <= mouse[1] <= timeValueTextRect45.midbottom[1]):
                    pygame.draw.rect(screen,color_light,timeValueTextRect45)  
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        timeValue=45

                else:
                    pygame.draw.rect(screen,color_dark,timeValueTextRect45)
                
                # superimposing the text onto our button
                screen.blit(start , startRect)
                screen.blit(diff25 , diff25Rect)
                screen.blit(diff50 , diff50Rect)
                screen.blit(diff75 , diff75Rect)

                screen.blit(timeValueText15 , timeValueTextRect15)
                screen.blit(timeValueText30 , timeValueTextRect30)
                screen.blit(timeValueText45 , timeValueTextRect45)

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
