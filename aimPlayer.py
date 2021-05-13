import pygame
import sys
import random
import math
import os
import neat

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (230, 230, 230)
LIGHTBLUE = (185,220,218)

color_light = (170,170,170)
color_dark = (100,100,100)


width = 1920
height = 1080
background_color = (40,0,150)


widthBourder = 400
heightBourder = 200



pygame.font.init()
sysfont = pygame.font.get_default_font()

crosshairImg = pygame.image.load('crosshair.jpg') #load the image to a variable
crosshairImgRect = crosshairImg.get_rect() #create a rect to for the image



class Ball:
    def __init__(self, x , y):

        self.x = x
        self.y = y
        self.color  = RED
        
        

    def draw(self, win, diff):
        pygame.draw.circle(win,self.color,(self.x,self.y),diff)


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

   

def main():
    pygame.init()
    clock = pygame.time.Clock()
    game = False
    score = 0
    into = True
    inside =0
    count=0
    diff=30
    timeValue = 15#default value
    accuracy = 0.00
    bestscore = 0
    bestAccuracy = 0.00
    
    mouseX = pygame.mouse.get_pos()[0]
    mouseY = pygame.mouse.get_pos()[1]

    balls = []

    for i in range(3):
        balls.append(Ball(random.randint(widthBourder, width-widthBourder),random.randint(heightBourder, height-heightBourder)))
    
    
    
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('pygame_window')
    
    #makes mouse invisible

    # rand = random.randint(widthBourder, width-widthBourder)
    # rand2 = random.randint(heightBourder, height-heightBourder)
    
    
    run = True
    while run:
        # pygame.time.delay(60)
        
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit() 

        #prints
            if(game==True):
                
                pygame.event.set_grab(True)
                pygame.mouse.set_visible(True) 
                
                x = pygame.mouse.get_pos()[0]
                y = pygame.mouse.get_pos()[1]

                #print("game is running")
                pygame.mouse.set_cursor(*pygame.cursors.broken_x)
                screen.fill((30,0,150))

                pygame.draw.rect(screen,GRAY,(0,0,width,50))
                

                scoreText,scoreTextRect = drawText('Score: ' + str(score),'Arial',35,screen,RED,700 ,50)
                scoreTextRect.topright = [width-50,10]
                screen.blit(scoreText, scoreTextRect)

                # crosshairImgRect.center = pygame.mouse.get_pos()
                # # screen.blit(crosshairImg, crosshairImgRect)
                # pygame.draw.line(screen,GREEN,(x,y-2),(x,y-10),4)
                # pygame.draw.line(screen,GREEN,(x,y+2),(x,y+10),4)
                # pygame.draw.line(screen,GREEN,(x-2,y),(x-10,y),4)
                # pygame.draw.line(screen,GREEN,(x+2,y),(x+10,y),4)
                

                if event.type == pygame.USEREVENT: 
                    counter -= 1
                    if counter > 0:
                        time = str(counter).rjust(3)  
                    else:
                        game=False

                timeText,timeTextRect = drawText('Time:' + str(time),'Arial',35,screen,RED,0 ,50)
                timeTextRect.topleft = [0,10]
                screen.blit(timeText, timeTextRect)
                
                if count!=0:
                    accuracy = (inside/count)*100
                    #print(inside, "/", count)
                    accText,accTextRect = drawText('Accuracy: ' + "{:.1f}".format(accuracy) + "%",'Arial',35,screen,RED,0 ,50)
                    accTextRect.midtop = [width/2,10]
                    screen.blit(accText, accTextRect)
                

                
                
                # pygame.draw.circle(screen,RED,(rand,rand2),diff)
                for ball in balls:
                    ball.draw(screen,diff)
                    

               

                

                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    print('clicked')
                    count+=1
                    for ball in balls:
                        print("loop")
                        if math.sqrt((mouseX -ball.x)**2 + (mouseY -ball.y)**2) < diff:
                            print('inside the ball')
                            #rand = random.sample(range(50, 1870), 1)
                            #rand2 = random.sample(range(100, 1030), 1)
                            # rand = random.randint(widthBourder, width-widthBourder)
                            # rand2 = random.randint(heightBourder, height-heightBourder)
                            
                            ball.x = random.randint(widthBourder, width-widthBourder)
                            ball.y =  random.randint(heightBourder, height-heightBourder) 
                            
                            score += 1
                            inside += 1
                    # elif inside > 0:
                    #     inside -= 1

                
                
                if score > bestscore:
                    bestscore = score
                if accuracy > bestAccuracy:
                    bestAccuracy = accuracy

            else:

                pygame.mouse.set_visible(True) 

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

                bestAccMenu,bestAccMenuRect = drawText('Best Accuracy: ' + "{:.1f}".format(bestAccuracy) + "%",'Arial',48,screen,RED,300,300)
                lastAccMenu,lastAccMenuRect = drawText('Last Accuracy: ' + "{:.1f}".format(accuracy) + "%",'Arial',48,screen,RED,300,400)

                bestScoreMenu,bestScoreMenuRect = drawText('Best Score: ' + str(bestscore),'Arial',48,screen,RED,225,600)
                lastScoreMenu,lastScoreMenuRect = drawText('Last Score: ' + str(score),'Arial',48,screen,RED,225,700)

                screen.fill(background_color) # fills the background with a color 
                screen.blit(title, titleRect)
                screen.blit(bestAccMenu, bestAccMenuRect)
                screen.blit(lastAccMenu, lastAccMenuRect)
                screen.blit(bestScoreMenu  , bestScoreMenuRect)
                screen.blit(lastScoreMenu  , lastScoreMenuRect)
                screen.blit(diffText, diffTextRect)
                screen.blit(timeValueText, timeValueTextRect)

                #start button
                if(startRect.midleft[0] <= mouse[0] <= startRect.midright[0] and startRect.midtop[1] <= mouse[1] <= startRect.midbottom[1]):
                    pygame.draw.rect(screen,color_light,startRect)  
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        game=True
                        score = 0
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

    

# main()
sys.exit




if __name__ == "__main__":
    main()