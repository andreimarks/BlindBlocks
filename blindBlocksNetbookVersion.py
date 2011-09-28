#-----------Blind Blocks--------#

# Import all the necessaries...
import sys
import random
import math

import pygame
import pygame._view
from pygame.locals import *

# Variables
BACKGROUNDCOLOR = (0,0,0)
BLOCKCOLOR = (255,255,255)
BLOCKSIZE = 24 # Need to fix, text doesn't change size location in relation.
FPS = 20
DOWNRATE = 1 # Need to fix, not actually constant.
MOVERATE = BLOCKSIZE
TEXTCOLOR = (255,255,255)
FIELDHEIGHT = BLOCKSIZE*22
FIELDWIDTH = BLOCKSIZE*10
WINDOWHEIGHT = BLOCKSIZE*24
WINDOWWIDTH = BLOCKSIZE*21

#------------Functions-----------#
def createGrid():
    # Used to confirm row clears.
    xcheck = BLOCKSIZE
    ycheck = BLOCKSIZE
    
    for y in range(23):
        gridRow = []
        for x in range(10):
            gridUnit = (xcheck,ycheck)
            gridRow.append(gridUnit)
            xcheck += BLOCKSIZE
        grid.append(gridRow)
        xcheck = BLOCKSIZE
        ycheck += BLOCKSIZE    
    return


def pickRandomTetromino():
    # Called to create the next block.
    block =[]
    blockChoice = random.choice(list(blockies.items()))    
    nextBlockInfo['block'] = blockChoice[0]
    nextBlockInfo['rotationPattern'] = blockChoice[1][1]
    for i,x,y in blockChoice[1][0]:
        block.append(pygame.Rect((BLOCKSIZE*x)+BLOCKSIZE,BLOCKSIZE+(BLOCKSIZE*y), BLOCKSIZE, BLOCKSIZE))    

    return block


def getNextBlock():
    # Takes the next block and makes it the current block.
    global nextBlock
    currentBlock = nextBlock
    currentBlockInfo['block'] = nextBlockInfo['block']
    currentBlockInfo['rotationPattern'] = nextBlockInfo['rotationPattern']
    return currentBlock


def checkRotationCollision(currentBlock):
    # If the function detects a collision, returns True and disables that rotation.
    global rotation
    copyRogo = currentBlockInfo['rotationPattern'][rotation]
    copyBlock = []
    for each in currentBlock:
        copyBlock.append(each.copy())
    
    for r in range(4):
        if rotation == r:            
            for i,x,y in copyRogo:
                ((copyBlock[i])).move_ip(BLOCKSIZE*x,BLOCKSIZE*y)
        for each in copyBlock:
            if each.collidelist(usedBlocks) != -1:
                return True
    return False


def rotato(currentBlock):
    # First, checks for a collision with a block in the stack, will escape function without rotation if there is.
    # Otherwise, rotates the block.
    # Then, if it detects that the rotated block is outside of the field, it "wall kicks" the block back into the field.
    global rotation
    shift = False
    difference = 0
    rogo = currentBlockInfo['rotationPattern'][rotation]
    if checkRotationCollision(currentBlock):
        return
    rotateClick2.play()    
    for r in range(4):
        if rotation == r:
            for a,b,c in rogo:
                ((currentBlock[a])).move_ip(BLOCKSIZE*b,BLOCKSIZE*c)
    if rotation < 3: rotation += 1
    else: rotation = 0
    for block in currentBlock:
        if block.right > FIELDWIDTH:
            difference = FIELDWIDTH-block.right
            shift = True
        elif block.left < BLOCKSIZE:
            difference = BLOCKSIZE-block.left
            shift = True
    if shift==True:
        for block in currentBlock:
            block.move_ip(difference, 0)
       
    return rotation


def oldBlocks(currentBlock):
    # After a block lands, this function moves it to the used pile stack.
    for i in currentBlock:
        usedBlocks.append(i)
        takeAwayGrid.append(i.topleft)
    return None


def drawCurrentBlock(currentBlock):
    # Draws the current tetromino (which is a group of four that remain independent).
    
    global n
    global up
    
    for i in currentBlock:
        pygame.draw.rect(windowSurface, (n,n,n), i, 3)
    if up:
        n += 10
    else:
        n -=10
    if n == 250 or n == 100:
        up = not up
        
    return n


def drawNextBlock(nextBlock):
    # Draws the next block on the information side of the screen.
    for i in nextBlock:
        x = i.move(BLOCKSIZE*10,(BLOCKSIZE*7)+BLOCKSIZE/2)
        pygame.draw.rect(windowSurface, (255,255,255), x, 3)

    
def drawText(text, font, surface, color, x, y):
    # Does all the heavy lifting for creating text.
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x,y)
    surface.blit(textobj, textrect)


def pause():
    # Actually, unused. Will probably remove.
    while True:
        drawText('Game Paused. Press \'P\' to Resume.', font, windowSurface, (255,255,255), (FIELDWIDTH / 2), (FIELDHEIGHT /3))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == ord('p'):
                    return


def proximityCheckLeft(currentBlock):
    # Determines whether or not any of the current blocks is in a spot to the left
    # of a usedBlock. Then the function will return a boolean value to be used in
    # determining whether or not a left move is allowed.
    # I can probably combine these next few proximity checks into a single function.
    for each in currentBlock:
        tempBlockRight = each.move(BLOCKSIZE,0)
        tempBlockLeft = each.move(-1*BLOCKSIZE,0)
        if tempBlockLeft.collidelist(usedBlocks) != -1:
            return True
    return False


def proximityCheckRight(currentBlock):
    # Same dealy as proximity CheckLeft(), but for the right side.
    for each in currentBlock:
        tempBlockRight = each.move(BLOCKSIZE,0)
        if tempBlockRight.collidelist(usedBlocks) != -1:
            return True
    return False


def floorCheck(currentBlock):
    # Checks to see if any of the blocks have moved underneath the field.
    for each in currentBlock:
        if each.bottom < (FIELDHEIGHT+BLOCKSIZE): return True
    return False


def wallCheckLeft(currentBlock):
    # Just like proximity check, except for the left side of the field.
    for each in currentBlock:
        if each.left > (0+BLOCKSIZE):
            continue
        else: return False
    return True


def wallCheckRight(currentBlock):
    # Just like proximity check, except for the right side of the field.
    for each in currentBlock:
        if each.right < (FIELDWIDTH+BLOCKSIZE):
            continue
        else:
            return False
    return True


def moveBlocks(currentBlock, xdir, ydir):
    for each in currentBlock:
        each.move_ip(xdir,ydir)    
    return currentBlock


def pingSonar():
    # Initial sonar ping originating from current tetromino.
    sonarPing.play()
    x=250
    b=random.randint(0,3)
    for i in range(BLOCKSIZE):
        for j in reversed(range(9,18)):
            pygame.draw.circle(windowSurface, (0,255,0), (currentBlock[b]).center, j*(i+1), 8)
        for doneBlock in usedBlocks:
            pygame.draw.rect(windowSurface, (0,0,0), doneBlock, 0)
        drawCurrentBlock(currentBlock)
        drawBorders()
        drawInfoSurface()
        pygame.display.update()
        windowSurface.fill(BACKGROUNDCOLOR)
        mainClock.tick(80)
    randomUsed = []
    # Return ping initiated by three randomly selected blocks on the field.
    if len(usedBlocks)>0: sonarReturn.play()
    if len(usedBlocks) > 3: randomUsed = random.sample(usedBlocks, 3)
    infoSurface.fill((0,0,0))
    drawInfoSurface()
    for j in range(10):
        for doneBlock in randomUsed:
            pygame.draw.circle(windowSurface, (0,255,0), doneBlock.midtop, 30*(j+1), 4)
            pygame.draw.rect(windowSurface, (0,0,0), doneBlock, 0)
        for doneBlock in usedBlocks:
            pygame.draw.rect(windowSurface, (0,0,0), doneBlock, 0)
        drawCurrentBlock(currentBlock)
        drawBorders()
        drawInfoSurface() 
        pygame.display.update()
        mainClock.tick(25)
    drawBorders()
    pygame.display.update()

    
def triggerFlare():
    # For the arc trail, draws a portion of an ellipse from the current block to a random location in the center of the field.
    flareShot.play()
    testRect = pygame.Rect((flareLight.topleft), (1,1))
    testRect.midtop = flareLight.topleft
    xArc = 2*(abs(testRect.centerx-(currentBlock[3]).centerx))
    yArc = 2*(abs(testRect.top-(currentBlock[3]).centery))
    testRect.width = xArc
    testRect.height = yArc
    testRect.midtop = flareLight.topleft
    flareLong.play()
    if (currentBlock[3]).centerx >= testRect.centerx and (currentBlock[3]).centery>=testRect.top:
        pygame.draw.arc(windowSurface, (255,255,255), testRect, 0,math.radians(90), 3)
    elif (currentBlock[3]).centerx < testRect.centerx and (currentBlock[3]).centery>testRect.top:
        pygame.draw.arc(windowSurface, (255,255,255), testRect, math.radians(90),math.pi, 3)
    pygame.display.update()
    mainClock.tick(10)
    
                
def removeBlockAnimation(toBeRemoved):
    exploder = random.choice(toBeRemoved[:])
    exploderValue.append(exploder)
    x = 0
    notRemoved = []
    copyUsedBlocks = []
    for i in usedBlocks:
        if i.topleft not in toBeRemoved:
            copyUsedBlocks.append(i)
    rowClearExplosion.play()
    mainClock.tick(20)
    for p in range(50):
        pygame.draw.circle(windowSurface, (x,x,x), exploder, 12*(p+1), 0)            
        for block in usedBlocks[:]:
            if block.topleft in toBeRemoved[:]:
                pygame.draw.rect(windowSurface, (x,x,x), block, 0)                
        x+=5
        drawBorders()
        drawInfoSurface()
        pygame.display.update()
        windowSurface.fill(BACKGROUNDCOLOR)            
        drawInfoSurface() 
        mainClock.tick(120)
    drawBorders()
    pygame.display.update()
    return


def removeBlocksFadeout():
    x=250
    exploder = exploderValue[0]
    for doneBlock in usedBlocks:
        pygame.draw.rect(windowSurface, (0,0,0), doneBlock, 3)
    drawBorders()
    drawInfoSurface()
    pygame.display.update()    
    for p in reversed(range(50)):
        x-=5
        pygame.draw.circle(windowSurface, (x,x,x), exploder, 12*50, 0)
        for doneBlock in usedBlocks:
            pygame.draw.rect(windowSurface, (0,0,0), doneBlock, 0)
        drawBorders()
        drawInfoSurface()
        pygame.display.update()
        mainClock.tick(60)
    drawBorders()
    return
    
    
def setBottommost(currentBlock):
    # Meant to find the bottommost block of the currentblock, set it to the desired height, and move the others accordingly.
    deficit = 0
    lowestBottom = -1
    for each in currentBlock:
       if each.bottom >= (FIELDHEIGHT+BLOCKSIZE) and each.bottom > lowestBottom:
            lowestBottom = each.bottom
    if lowestBottom < 0:
        return False
    blockLand.play()
    pygame.time.wait(80)
    deficit = lowestBottom-(FIELDHEIGHT+BLOCKSIZE)
    for each in currentBlock:
        each.move_ip(0,deficit*-1)   
    return True


def flashFinishedBlock(block):
    # Pauses the program and flashes the dropped block to show the player where it ends up.
    windowSurface.fill((0,0,0,))
    drawBorders()
    drawInfoSurface()
    n = 0
    while n < 250:
        for each in block:
            pygame.draw.rect(windowSurface, (n,n,n), each, 3)
        pygame.display.update()
        n += 5
        mainClock.tick(150)

    
def checkCollisions(currentBlock):
    # Quick check for if the current block is moved into a lower block after descending. If so, pushes it up.
    blockAtIssue = 0
    deficit = 0
    for each in currentBlock:
        if each.collidelist(usedBlocks) != -1:
            bumpedBlock = usedBlocks[each.collidelist(usedBlocks)]
            deficit = (currentBlock[blockAtIssue]).bottom-(bumpedBlock.top)
            for each in currentBlock:
                each.move_ip(0,deficit*-1)
            return True
        blockAtIssue += 1
    return False

    
def terminate():
    pygame.quit()
    sys.exit()

    
def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                return


def drawBorders():
    global c, ctoggle
    
    xBord,yBord = 0, 0
    if ctoggle: c+=10
    else: c-=10
    if c == 250 or c == 150: ctoggle = not ctoggle
    for y in range (24):
        for x in range(12):
            if y == 0:
                pygame.draw.rect(windowSurface, (c,c,c), (pygame.Rect((1*x*BLOCKSIZE),(1*y*BLOCKSIZE),BLOCKSIZE,BLOCKSIZE)), 1)
            elif y == 23:
                pygame.draw.rect(windowSurface, (c,c,c), (pygame.Rect((1*x*BLOCKSIZE),(1*y*BLOCKSIZE),BLOCKSIZE,BLOCKSIZE)), 1)
            elif x==0 or x==11:
                pygame.draw.rect(windowSurface, (c,c,c), (pygame.Rect((1*x*BLOCKSIZE),(1*y*BLOCKSIZE),BLOCKSIZE,BLOCKSIZE)), 1)
                pygame.draw.rect(windowSurface, (c,c,c), (pygame.Rect((1*x*BLOCKSIZE),(1*y*BLOCKSIZE),BLOCKSIZE,BLOCKSIZE)), 1)
    pygame.draw.line(windowSurface, (c,c,c,), (BLOCKSIZE,BLOCKSIZE*3-1), (BLOCKSIZE*11,BLOCKSIZE*3-1), 3)


def drawInfoSurface():
    # infoSurface is the side panel presenting game information to the player.
    infoSurface.fill((0,0,0))
    global pingCount, infraredFill, flaresLeft, linesClear, blocksTotal, pingsTotal, blindBlocks
    pygame.draw.rect(infoSurface, (0,0,0),fieldWindow, 0)
    drawNextBlock(nextBlock)
    drawText('BLIND', blockFont, infoSurface, (255,255,255),BLOCKSIZE, BLOCKSIZE)
    drawText('BLOCKS', blockFont, infoSurface, (255,255,255),BLOCKSIZE, BLOCKSIZE*3)
    drawText('NEXT BLOCK:', blockFontSmall, infoSurface,(255,255,255), BLOCKSIZE, BLOCKSIZE*7)
    drawText('SONAR PINGS:', blockFontSmall, infoSurface,(255,255,255), BLOCKSIZE, BLOCKSIZE*11)
    if pingCount < 30: pingCountDashes = 'I'* pingCount
    else: pingCountDashes = str(pingCount)        
    drawText(pingCountDashes, blockFontSmall, infoSurface,(0,255,0), BLOCKSIZE, BLOCKSIZE*12)
    drawText('INFRARED:', blockFontSmall, infoSurface,(255,255,255), BLOCKSIZE, BLOCKSIZE*13)
    infraredMeter = pygame.Rect(BLOCKSIZE, BLOCKSIZE*14, int((BLOCKSIZE*7)*((infraredFill/400))), BLOCKSIZE/2)
    pygame.draw.rect(infoSurface, (200,0,0), infraredMeter, 0)
    drawText('FLARES:', blockFontSmall, infoSurface, (255,255,255),BLOCKSIZE, BLOCKSIZE*15)
    for i in range(flaresLeft):
        pygame.draw.rect(infoSurface, (255,255,255), (pygame.Rect(BLOCKSIZE+((BLOCKSIZE*2+10)*i), BLOCKSIZE*16, BLOCKSIZE*2, BLOCKSIZE/2)), 0)
    drawText('LINES CLEARED:', blockFontSmall, infoSurface, (255,255,255),BLOCKSIZE, BLOCKSIZE*17)
    drawText(str(linesClear), blockFontSmall, infoSurface, (255,255,255),BLOCKSIZE, BLOCKSIZE*18)
    drawText('BLOCK/PING RATIO:', blockFontSmall, infoSurface, (255,255,255),BLOCKSIZE, BLOCKSIZE*19)
    if pingsTotal==0:
        drawText('NO PINGS', blockFontSmall, infoSurface, (255,255,255),BLOCKSIZE, BLOCKSIZE*20)
        drawText((str(100*linesClear)), blockFont, infoSurface, (255,255,0),BLOCKSIZE, BLOCKSIZE*5)
    else:
        drawText(str(round(blocksTotal/pingsTotal, 2)), blockFontSmall, infoSurface, (255,255,255),BLOCKSIZE, BLOCKSIZE*20)
        drawText(str(int(100*linesClear*(round(blocksTotal/pingsTotal, 2)))), blockFont, infoSurface, (255,255,0),BLOCKSIZE, BLOCKSIZE*5)
    drawText('BLIND BLOCKS:', blockFontSmall, infoSurface, (255,255,255),BLOCKSIZE, BLOCKSIZE*21)
    drawText(str(blindBlockCount), blockFontSmall, infoSurface, (255,255,255),BLOCKSIZE, BLOCKSIZE*22)
    drawText('Press \'P\' to Pause.', fontSmall, infoSurface, (255,255,255),BLOCKSIZE, BLOCKSIZE*23)
    windowSurface.blit(infoSurface, (BLOCKSIZE*12,0))


def drawDarkMenuScreen():
    # Draws darkened menu screen shown during title screen animation.
    drawText('BLIND BLOCKS', titleFont, windowSurface, (0,0,0), BLOCKSIZE*4, 200)
    drawText('START', titleFontSmall, windowSurface, (0,0,0), BLOCKSIZE*10, BLOCKSIZE*14)
    drawText('DIFFICULTY', titleFontSmall, windowSurface, (0,0,0), BLOCKSIZE*10, BLOCKSIZE*16)
    drawText('INSTRUCTIONS', titleFontSmall, windowSurface, (0,0,0), BLOCKSIZE*10, BLOCKSIZE*18)    
    drawText('CREDITS', titleFontSmall, windowSurface, (0,0,0), BLOCKSIZE*10, BLOCKSIZE*20)


def checkLoss():
    # Checks to see whether or not tetrominos are present above the 20th row.
    global lossRect
    if lossRect.collidelistall(usedBlocks):        
        return True
    else: return False


def gameOver():
    # Prints the Game Over screen, scoring, etc., upon Return the game resets.
    gameOverNoise.play()
    x = 0
    q = 50
    n = 60
    up = True
    for p in range(q):
        windowSurface.fill(BACKGROUNDCOLOR)            
        pygame.draw.circle(windowSurface, (x,x,x), (BLOCKSIZE*6,BLOCKSIZE*6), 12*(p+1), 0)
        x+=5
        mainClock.tick(120)
        pygame.display.update()
    while True:
        pygame.mixer.music.stop()
        windowSurface.fill((0,0,0))
        pygame.draw.rect(windowSurface, (x,x,x), pygame.Rect(BLOCKSIZE, BLOCKSIZE, FIELDWIDTH,FIELDHEIGHT), 0)
        drawBorders()
        for o in usedBlocks:
            pygame.draw.rect(windowSurface, (0,0,0), o, 0)
        if up:
            n += 10
        else:
            n -=10
        if n == 200 or n == 50:
            up = not up
        drawText('GAME OVER', blockFont, windowSurface, (n,n,n),int(BLOCKSIZE/2), BLOCKSIZE*5)
        drawText('PRESS ESCAPE', blockFontSmall, windowSurface, (n,n,n),BLOCKSIZE*4, BLOCKSIZE*10)
        drawText('TO RETURN TO', blockFontSmall, windowSurface, (n,n,n),BLOCKSIZE*4, BLOCKSIZE*11)
        drawText('THE MAIN MENU.', blockFontSmall, windowSurface, (n,n,n),BLOCKSIZE*4, BLOCKSIZE*12)
        mainClock.tick(10)
        drawInfoSurface()        
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return


def showMainMenu():
    global n, up
    pos=0
    startRect = pygame.Rect(BLOCKSIZE*8,BLOCKSIZE*14,BLOCKSIZE,BLOCKSIZE)
    difficultyRect = pygame.Rect(BLOCKSIZE*8,BLOCKSIZE*16,BLOCKSIZE,BLOCKSIZE)
    optionsRect = pygame.Rect(BLOCKSIZE*8,BLOCKSIZE*18,BLOCKSIZE,BLOCKSIZE)
    creditsRect = pygame.Rect(BLOCKSIZE*8,BLOCKSIZE*20,BLOCKSIZE,BLOCKSIZE)
    currentRect = []
    currentRect = [startRect, difficultyRect, optionsRect, creditsRect]
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                if event.key == K_UP or event.key == ord('w'):
                    if pos==0: pos=3
                    else: pos-=1
                    select.play()
                if event.key == K_DOWN or event.key == ord('s'):
                    if pos==3:pos=0
                    else: pos+=1
                    select.play()
                if event.key == K_RETURN:
                    if pos==0:return True
                    elif pos==1: selectDifficulty()
                    elif pos==2:showOptions()
                    else: showCredits()
        windowSurface.fill((0,0,0))
        pygame.draw.rect(windowSurface, (n,n,n), currentRect[pos], 3)
        if up: n += 1
        else: n -=1
        if n == 250 or n == 20: up = not up
        drawText('BLIND BLOCKS', titleFont, windowSurface, (255,255,255), BLOCKSIZE*4, 200)
        if pos<=0: drawText('START', titleFontSmall, windowSurface, (n,n,n), BLOCKSIZE*10, BLOCKSIZE*14)
        else: drawText('START', titleFontSmall, windowSurface, (255,255,255), BLOCKSIZE*10, BLOCKSIZE*14)
        if pos==1: drawText('DIFFICULTY', titleFontSmall, windowSurface, (n,n,n), BLOCKSIZE*10, BLOCKSIZE*16)
        else: drawText('DIFFICULTY', titleFontSmall, windowSurface, (255,255,255), BLOCKSIZE*10, BLOCKSIZE*16)
        if pos==2:drawText('INSTRUCTIONS', titleFontSmall, windowSurface, (n,n,n), BLOCKSIZE*10, BLOCKSIZE*18)
        else: drawText('INSTRUCTIONS', titleFontSmall, windowSurface, (255,255,255), BLOCKSIZE*10, BLOCKSIZE*18)    
        if pos==3:drawText('CREDITS', titleFontSmall, windowSurface, (n,n,n), BLOCKSIZE*10, BLOCKSIZE*20)
        else: drawText('CREDITS', titleFontSmall, windowSurface, (255,255,255), BLOCKSIZE*10, BLOCKSIZE*20)
        pygame.display.update()
        

def showOptions():
    windowSurface.fill((0,0,0))
    drawText('Press any key to return.', fontSmall, windowSurface, (0,255,0), BLOCKSIZE*7, BLOCKSIZE)
    drawText('Instructions', fontSmall, windowSurface, (255,255,255), BLOCKSIZE, BLOCKSIZE*2)
    drawText('Play Tetris. Use sonar, IR, or flares as necessary.', fontSmall, windowSurface, (255,255,255), BLOCKSIZE*2, BLOCKSIZE*3)
    drawText('Keys', fontSmall, windowSurface, (255,255,255), BLOCKSIZE, BLOCKSIZE*4)
    drawText('Movement = ASD or Left, Down, Right Arrow Keys', fontSmall, windowSurface, (255,255,255), BLOCKSIZE*2, BLOCKSIZE*5)
    drawText('Rotate Block = W or Up Arrow Key', fontSmall, windowSurface, (255,255,255), BLOCKSIZE*2, BLOCKSIZE*6)
    drawText('Ping Sonar = Spacebar or Numpad0', fontSmall, windowSurface, (0,255,0), BLOCKSIZE*2, BLOCKSIZE*7)
    drawText('Briefly reveals playfield.', fontSmall, windowSurface, (255,255,255), BLOCKSIZE*3, BLOCKSIZE*8)
    drawText('Toggle Infrared = R or Numpad1', fontSmall, windowSurface, (255,0,0), BLOCKSIZE*2, BLOCKSIZE*9)
    drawText('Clearly reveal playfield, but depletes IR meter.', fontSmall, windowSurface, (255,255,255), BLOCKSIZE*3, BLOCKSIZE*10)
    drawText('Shoot Flare = F or Numpad2', fontSmall, windowSurface, (255,255,0), BLOCKSIZE*2, BLOCKSIZE*11)
    drawText('Flares reveal portions of the playfield as they descend.', fontSmall, windowSurface, (255,255,255), BLOCKSIZE*3, BLOCKSIZE*12)
    drawText('Toggle Background Music = M', fontSmall, windowSurface, (255,255,255), BLOCKSIZE*2, BLOCKSIZE*13)
    drawText('Increase/Decrease Volume = "+/=" Key / "-" Key', fontSmall, windowSurface, (255,255,255), BLOCKSIZE*2, BLOCKSIZE*14)
    drawText('Pause = P', fontSmall, windowSurface, (255,255,255), BLOCKSIZE*2, BLOCKSIZE*15)
    drawText('Scoring', fontSmall, windowSurface, (255,255,255), BLOCKSIZE, BLOCKSIZE*16)
    drawText('Your score is based on the number of lines cleared,', fontSmall, windowSurface, (255,255,255), BLOCKSIZE*2, BLOCKSIZE*17)
    drawText('modified by your block-to-ping ratio. Clearing four', fontSmall, windowSurface, (255,255,255), BLOCKSIZE*2, BLOCKSIZE*18)
    drawText('rows at once gives a bonus row.', fontSmall, windowSurface, (255,255,255), BLOCKSIZE*2, BLOCKSIZE*19)
    drawText('"Blind Blocks Score" - Keeps track of your longest', fontSmall, windowSurface, (255,255,255), BLOCKSIZE*2, BLOCKSIZE*20)
    drawText('streak of blocks dropped without visual aids. Only', fontSmall, windowSurface, (255,255,255), BLOCKSIZE*2, BLOCKSIZE*21)
    drawText('refreshes on line clears.', fontSmall, windowSurface, (255,255,255), BLOCKSIZE*2, BLOCKSIZE*22)
    pygame.display.update()
    waitForPlayerToPressKey()

        
def selectDifficulty():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return
                if event.key == K_UP or event.key == ord('w'):
                    difficultyLevel[0] = not difficultyLevel[0]
                    select.play()
                if event.key == K_DOWN or event.key == ord('s'):
                    difficultyLevel[0] = not difficultyLevel[0]
                    select.play()
                if event.key == K_RETURN:
                    return
        windowSurface.fill((0,0,0))
        drawText('SELECT DIFFICULTY AND PRESS ENTER:', blockFontSmall, windowSurface, (255,255,255), BLOCKSIZE*2, BLOCKSIZE*10)    
        if not difficultyLevel[0]:
            drawText('I AM NOT BATMAN.', blockFontSmall, windowSurface, (0,255,0), BLOCKSIZE*4, BLOCKSIZE*11)    
            drawText('I AM BATMAN.', blockFontSmall, windowSurface, (255,255,255), BLOCKSIZE*4, BLOCKSIZE*12)
        else:
            drawText('I AM NOT BATMAN.', blockFontSmall, windowSurface, (255,255,255), BLOCKSIZE*4, BLOCKSIZE*11)    
            drawText('I AM BATMAN.', blockFontSmall, windowSurface, (0,255,0), BLOCKSIZE*4, BLOCKSIZE*12)
        pygame.display.update()
        

def showCredits():
    # Just shows the credits screen, upon release goes back to the menu screen.
    windowSurface.fill((0,0,0))
    drawText('Blind Blocks created by Andrei Marks', font, windowSurface, (255,255,255), BLOCKSIZE*4, BLOCKSIZE*6)    
    drawText(' - http://workworkgames.com)', font, windowSurface, (255,255,255), BLOCKSIZE*6, BLOCKSIZE*7)    
    drawText('Sound Effects: Created by Andrei Marks', font, windowSurface, (255,255,255), BLOCKSIZE*4, BLOCKSIZE*9)    
    drawText('using Bfxr - http://www.bfxr.net/', font, windowSurface, (255,255,255), BLOCKSIZE*6, BLOCKSIZE*10)
    drawText('Music: "Starless Night" by Calis', font, windowSurface, (255,255,255), BLOCKSIZE*4, BLOCKSIZE*12)    
    drawText(' - http://8bc.org/members/calis/', font, windowSurface, (255,255,255), BLOCKSIZE*6, BLOCKSIZE*13)    
    drawText('Font: Unsteady Overseer by Ray Larabie', font, windowSurface, (255,255,255), BLOCKSIZE*4, BLOCKSIZE*15)
    drawText(' - http://typodermicfonts.com/', font, windowSurface, (255,255,255), BLOCKSIZE*6, BLOCKSIZE*16)
    drawText('Press any key to return to the menu.', font, windowSurface, (0,255,0), BLOCKSIZE*7, BLOCKSIZE*18)
    pygame.display.update()
    waitForPlayerToPressKey()
    return
    
#---------End of Functions, Beginning of Game---------#

# Set up pygame & the window.
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), pygame.RESIZABLE)#, pygame.FULLSCREEN)
pygame.display.set_caption('Blind Blocks: Tetris After Dark')
fullscreen = False

# Set up the fonts
fontSmall = pygame.font.Font("freesansbold.ttf", int(BLOCKSIZE/2))
font = pygame.font.Font("freesansbold.ttf", int(BLOCKSIZE/2))
fontLarge = pygame.font.Font("freesansbold.ttf", BLOCKSIZE*2)
blockFont = pygame.font.Font("unsteady oversteer.ttf", BLOCKSIZE*2)
blockFontSmall = pygame.font.Font("unsteady oversteer.ttf", int(BLOCKSIZE/2))
titleFont = pygame.font.Font("unsteady oversteer.ttf", BLOCKSIZE*2)
titleFontSmall = pygame.font.Font("unsteady oversteer.ttf", BLOCKSIZE)

# Set up sounds
rowClearExplosion = pygame.mixer.Sound('Sounds/rowClearExplosion.wav')
rowDown = pygame.mixer.Sound('Sounds/rowDown.wav')
sonarPing = pygame.mixer.Sound('Sounds/sonarPing.wav')
sonarReturn = pygame.mixer.Sound('Sounds/sonarReturn.wav')
flareShot = pygame.mixer.Sound('Sounds/flareShot.wav')
flareLong = pygame.mixer.Sound('Sounds/flareLong.wav')
infraredHum = pygame.mixer.Sound('Sounds/infraredHum.wav')
blockLand = pygame.mixer.Sound('Sounds/blockLand.wav')
rotateClick2 = pygame.mixer.Sound('Sounds/rotateClick3.wav')
select = pygame.mixer.Sound('Sounds/Blip_Select56.wav')
gameOverNoise = pygame.mixer.Sound('Sounds/gameOverNoise.wav')
background = pygame.mixer.music.load('Sounds/calis_-_Starless_Night.mp3')
currentVolume = 1.0
musicPause = False
pygame.mixer.music.set_volume(currentVolume)

# Block Dictionary.
BLOCK = pygame.Rect(FIELDWIDTH/2,0, BLOCKSIZE, BLOCKSIZE)
blockies = {'oBlock':[[(0,4,0), (1,5,0), (2,4,1), (3,5,1)],
            [[(0,1,0), (1,0,1), (2,0,-1), (3,-1,0)],    # Translation coordinates for rotation 1.
            [(0,0,1),(1,-1,0),(2,1,0),(3,0,-1)],        # ...for rotation 2.
            [(0,-1,0),(1,0,-1),(2,0,1),(3,1,0)],        # ...for rotation 3.
            [(0,0,-1),(1,1,0),(2,-1,0),(3,0,1)]]],      # ... for rotation 4.
            'iBlock':[[(0,3,0), (1,4,0), (2,5,0), (3,6,0)],#    etc.
            [[(0,2,-1), (1,1,0), (2,0,1), (3,-1,2)],
            [(0,1,2),(1,0,1),(2,-1,0),(3,-2,-1)],
            [(0,-2,1),(1,-1,0),(2,0,-1),(3,1,-2)],
            [(0,-1,-2),(1,0,-1),(2,1,0),(3,2,1)]]],
            'tBlock':[[(0,4,0), (1,3,1), (2,4,1), (3,5,1)],
            [[(0,1,1), (1,1,-1), (2,0,0), (3,-1,1)],
            [(0,-1,1),(1,1,1),(2,0,0),(3,-1,-1)],
            [(0,-1,-1),(1,-1,1),(2,0,0),(3,1,-1)],
            [(0,1,-1),(1,-1,-1),(2,0,0),(3,1,1)]]],
            'sBlock':[[(0,4,0), (1,5,0), (2,3,1), (3,4,1)],
            [[(0,1,1), (1,0,2), (2,1,-1), (3,0,0)],
            [(0,-1,1),(1,-2,0),(2,1,1),(3,0,0)],
            [(0,-1,-1),(1,0,-2),(2,-1,1),(3,0,0)],
            [(0,1,-1),(1,2,0),(2,-1,-1),(3,0,0)]]],
            'zBlock':[[(0,3,0), (1,4,0), (2,4,1), (3,5,1)],
            [[(0,2,0), (1,1,1), (2,0,0), (3,-1,1)],
            [(0,0,2),(1,-1,1),(2,0,0),(3,-1,-1)],
            [(0,-2,0),(1,-1,-1),(2,0,0),(3,1,-1)],
            [(0,0,-2),(1,1,-1),(2,0,0),(3,1,1)]]],
            'jBlock':[[(0,3,0), (1,3,1), (2,4,1), (3,5,1)],
            [[(0,2,0), (1,1,-1), (2,0,0), (3,-1,1)],
            [(0,0,2),(1,1,1),(2,0,0),(3,-1,-1)],
            [(0,-2,0),(1,-1,1),(2,0,0),(3,1,-1)],
            [(0,0,-2),(1,-1,-1),(2,0,0),(3,1,1)]]],
            'lBlock':[[(0,5,0), (1,3,1), (2,4,1), (3,5,1)],
            [[(0,0,2), (1,1,-1), (2,0,0), (3,-1,1)],
            [(0,-2,0),(1,1,1),(2,0,0),(3,-1,-1)],
            [(0,0,-2),(1,-1,1),(2,0,0),(3,1,-1)],
            [(0,2,0),(1,-1,-1),(2,0,0),(3,1,1)]]]}

# Starting a Fresh Game
reset = True
difficultyLevel = []
difficultyLevel = [False]


#----------Start Animation----------#
start=False 
currentBlock =[]
currentBlockInfo = {}
n=200
up=True
rotation=0
currentBlock1 = blockies['tBlock']#random.choice(list(blockies.keys()))#
currentBlockInfo['block'] = currentBlock1[0]
currentBlockInfo['rotationPattern'] = currentBlock1[1]
for i,x,y in currentBlock1[0]:
    currentBlock.append(pygame.Rect((BLOCKSIZE*x)+BLOCKSIZE,BLOCKSIZE+(BLOCKSIZE*y), BLOCKSIZE, BLOCKSIZE))
iterations = 0
while iterations <= 90:
    for event in pygame.event.get():
        if event.type == QUIT:
            terminate()
        if event.type == KEYDOWN:
            start=True
            break
    if start == True: break
    windowSurface.fill(BACKGROUNDCOLOR)
    drawDarkMenuScreen()
    drawCurrentBlock(currentBlock)
    moveBlocks(currentBlock, 0, 5)
    if iterations == 15 or iterations == 30 or iterations == 40 or iterations == 60 or iterations == 70:
        rotateClick2.play()
        rogo = currentBlockInfo['rotationPattern']
        for r in range(4):
            if rotation == r and start!=True:
                for i,x,y in rogo[rotation]:
                    ((currentBlock[i])).move_ip(BLOCKSIZE*x,BLOCKSIZE*y)
        if rotation < 3: rotation += 1
        else: rotation = 0             
    if iterations == 5 or iterations == 50 or iterations == 75:
        sonarPing.play()
        for i in range(BLOCKSIZE):
            #print('drawing')
            b=3
            for j in reversed(range(9,18)):
                pygame.draw.circle(windowSurface, (0,255,0), (currentBlock[b]).center, j*(i+1), 8)
            drawCurrentBlock(currentBlock)
            drawDarkMenuScreen()
            pygame.display.update()            
            windowSurface.fill(BACKGROUNDCOLOR)
            mainClock.tick(30)
    pygame.display.update()
    iterations +=1
    mainClock.tick(60)
    if start==True: break
if start != True:
    x=0
    rowClearExplosion.play()
    mainClock.tick(20)
    for p in range(50):
        windowSurface.fill(BACKGROUNDCOLOR)            
        pygame.draw.circle(windowSurface, (x,x,x), (335,520), 12*(p+1), 0)
        drawDarkMenuScreen()
        x+=5
        mainClock.tick(120)
        pygame.display.update()
    for p in reversed(range(50)):
        windowSurface.fill(BACKGROUNDCOLOR)
        x-=5
        pygame.draw.circle(windowSurface, (x,x,x), (335,520), 12*50, 0)
        drawDarkMenuScreen()
        pygame.display.update()
        windowSurface.fill(BACKGROUNDCOLOR)
        mainClock.tick(30)

# Show the "Start" screen
mainMenu=True

# The game loop starts.
while True:
    while mainMenu==True:
        windowSurface.fill((0,0,0))
        if showMainMenu()==True: break
    mainMenu=False

    if reset == True: # Reset is set to True if the game is escaped or after Game Over.
        # Start Data
        moveLeft = moveRight = moveUp = moveDown = False
        DOWNRATE = 1
        usedBlocks = []
        rotation = 0
        currentBlockInfo = {}
        nextBlockInfo = {}
        grid = []
        takeAwayGrid = []
        createGrid()
        flareLight = pygame.Rect(BLOCKSIZE*(random.randint(3,8)),BLOCKSIZE*2, BLOCKSIZE,BLOCKSIZE)
        flareColor = 0
        c = 160
        ctoggle = False
        n=200
        r=0
        irDelay=0
        IFon=True
        up = True
        infrared=False
        flare = False
        infoSurface = pygame.Surface((BLOCKSIZE*10, WINDOWHEIGHT)).convert()
        infoSurface.set_colorkey((0,0,0))
        fieldWindow = pygame.Rect(0,0,BLOCKSIZE*10,BLOCKSIZE*24)
        pygame.draw.rect(infoSurface, (0,0,0),fieldWindow, 0)
        lossRect = pygame.Rect(BLOCKSIZE, BLOCKSIZE, BLOCKSIZE*10, BLOCKSIZE*2)
        
        # Counts
        pingCount = 1
        infraredFill = 400
        flaresLeft = 3
        linesClear = 0
        blocksTotal = 0
        pingsTotal = 0
        blindBlocks = 0
        blindBlockCount = 0

        # Set up blocks for real game.    
        nextBlock = pickRandomTetromino()
        currentBlock = getNextBlock()
        blocksTotal+=1
        nextBlock = pickRandomTetromino()
        rotation = 0
        n=200
        up=True
        pygame.mixer.music.play(-1)
        reset=False
        
    for event in pygame.event.get():
        if event.type == QUIT:
            terminate()
        if event.type == KEYDOWN:
            # Movement Keys
            if event.key == K_LEFT or event.key == ord('a'):
                moveRight = False
                moveLeft = True
                mainClock.tick(40)
            if event.key == K_RIGHT or event.key == ord('d'):
                moveLeft = False
                moveRight = True
                mainClock.tick(40)
            if event.key == K_UP or event.key == ord('w'):
                rotato(currentBlock)
            if event.key == K_DOWN or event.key == ord('s'):
                moveUp = False
                moveDown = True
            if event.key == K_F12:
                if fullscreen==False:
                    pygame.display.set_mode((0,0),pygame.FULLSCREEN)
                else:pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
                fullscreen = not fullscreen
                pygame.display.update()
            # Pause
            if event.key == ord('p'):
                showOptions()
            # Tools
            if (event.key == K_SPACE or event.key == K_KP0) and pingCount>0: # Sonar
                pingSonar()
                pingCount -= 1
                pingsTotal += 1
                blindBlocks = 0
            if (event.key == ord('r') or event.key == K_KP1) and infraredFill > 0: # Infrared
                if infrared == False: infraredHum.play(-1)
                else: infraredHum.stop()#fadeout(100)
                infrared = not infrared
                blindBlocks = 0
            if (event.key == ord('f') or event.key == K_KP2) and flare != True and flaresLeft > 0:
                triggerFlare()
                flare = True
                flaresLeft -= 1
                blindBlocks = 0
            # Volume Controls
            if event.key == ord('m'):
                if musicPause == False:
                    pygame.mixer.music.pause()                    
                else:
                    pygame.mixer.music.unpause()
                musicPause = not musicPause
            if event.key == K_EQUALS and currentVolume < 1.0:
                currentVolume += 0.1
                pygame.mixer.music.set_volume(currentVolume)
                print(currentVolume)
            if event.key == K_MINUS and currentVolume > 0:
                currentVolume -= 0.1
                pygame.mixer.music.set_volume(currentVolume)
                print(currentVolume)
                
        if event.type == KEYUP:
            if event.key == K_ESCAPE:
                pygame.mixer.music.stop()
                infraredHum.stop()
                mainMenu=True
                reset=True
            if event.key == K_LEFT or event.key == ord('a'):
                moveLeft = False
            if event.key == K_RIGHT or event.key == ord('d'):
                moveRight = False
            if event.key == K_DOWN or event.key == ord('s'):
                moveDown = False

    # Player's Movement
    if moveLeft and wallCheckLeft(currentBlock) and not proximityCheckLeft(currentBlock):
        moveBlocks(currentBlock, MOVERATE*-1, 0)
        mainClock.tick(40)
    if moveRight and wallCheckRight(currentBlock) and not proximityCheckRight(currentBlock):
        moveBlocks(currentBlock, MOVERATE, 0)
        mainClock.tick(40)
    if moveDown and floorCheck(currentBlock):
        moveBlocks(currentBlock, 0, MOVERATE)

    # Inexorable motion downward.
    if setBottommost(currentBlock):
        oldBlocks(currentBlock) # Function to run when block goes off playing field.
        flashFinishedBlock(currentBlock)
        currentBlock = getNextBlock()
        blocksTotal+=1        
        if not difficultyLevel[0]: pingCount += 1
        blindBlocks+=1
        nextBlock = pickRandomTetromino()
        rotation = 0
    elif checkCollisions(currentBlock):
        blockLand.play()
        pygame.time.wait(80)
        oldBlocks(currentBlock)
        flashFinishedBlock(currentBlock)
        currentBlock = getNextBlock()
        blocksTotal+=1
        if not difficultyLevel[0]: pingCount += 1
        blindBlocks+=1
        nextBlock = pickRandomTetromino()
        rotation = 0
    else:
        moveBlocks(currentBlock,0,DOWNRATE)
    
    # Check for Row Clears
    toBeRemoved = []
    numRemoveRows = []
    scootDown = []
    for i in range(22):
        if len((set(grid[i]) & set(takeAwayGrid))) == len(grid[i]): # This line checks if there are ten blocks present in a row.
            # If there are, it adds the tuple to toBeRemovedList.
            # Everything is held in toBeRemoved until all rows are checked.
            toBeRemoved.extend(grid[i])
            numRemoveRows.append(i)
            if len(numRemoveRows)==4:
                linesClear += 1
            linesClear += 1
            if difficultyLevel[0]: pingCount += 1
            if linesClear % 10 == 0:
                DOWNRATE +=1
            if blindBlocks > blindBlockCount: blindBlockCount = blindBlocks
    if toBeRemoved:
        exploderValue=[]
        removeBlockAnimation(toBeRemoved)
    for each in usedBlocks[:]:
        if each.topleft in toBeRemoved:
            usedBlocks.remove(each)                    
            takeAwayGrid.remove(each.topleft)
    numRemoveRows.sort()
    # Okay, I think the best thing to do here is move blocks in the rows
    # above the removed blocks. In other words, for each row removed, calculate
    # any of the blocks above that are a part of it, and move_ip them
    # all down a block space.
    for each in numRemoveRows: # let's say rows 19, 20, 21
      # then, we want to tag all the blocks in the rows above those rows
      # so, we'd want 0-18, again 0-19, again 0-20.
        rowDown.play()
        for i in range(each): # so first this would give us an i for 0, 1, 2...18
            scootDown.extend(grid[i]) # this should add the blocks that we would want to move down,
        for o in usedBlocks[:]:
             if o.topleft in scootDown:
                o.move_ip(0, BLOCKSIZE)
        removeBlocksFadeout()            
    takeAwayGrid = []
    for i in usedBlocks:
        takeAwayGrid.append(i.topleft)
    windowSurface.fill(BACKGROUNDCOLOR)
    
    # Did the player use a Flare?
    if flare == True:
        if flareLight.centery <= WINDOWHEIGHT:
            flareSize = BLOCKSIZE*6
            pygame.draw.circle(windowSurface, (flareColor,flareColor,flareColor), flareLight.topleft, flareSize,0)
            flareLight.move_ip(0,4)
            if flareColor >240: flareColor = 180
            for each in usedBlocks:
                pygame.draw.rect(windowSurface, (0,0,0), each, 0)
        else:
            flareFade=200
            for x in range(20):
                drawBorders()
                drawInfoSurface()
                pygame.draw.circle(windowSurface, (flareFade,flareFade,flareFade), flareLight.topleft, flareSize,0)
                flareFade -= 10
                for doneBlock in usedBlocks:
                    pygame.draw.rect(windowSurface, (0,0,0), doneBlock, 0)
                pygame.display.update()
                mainClock.tick(60)
            #Reset Flare
            flareLong.fadeout(10)
            flare = False
            flareColor=180
            flareLight = pygame.Rect(BLOCKSIZE*(random.randint(3,8)),BLOCKSIZE*2, 1,1)
        flareColor += 10

    # Did the player turn on IR?
    if infrared and infraredFill > 0:
        if not difficultyLevel[0]: infraredFill -=1
        else: infraredFill -=2
        for doneBlock in usedBlocks:
            if irDelay == 10:
                if IFon:
                    r += 1
                else:
                    r -= 1
                irDelay = 0
            elif r > 50 or r == 0:
                IFon = not IFon
            irDelay += 1
            pygame.draw.rect(windowSurface, (40+r,r,r), doneBlock, 0)
    if infraredFill <= 0:
        infraredHum.fadeout(10)
        
    # Loss Condition
    if checkLoss():
        play = False
        gameOver()
        mainMenu = True        
        reset = True
        
    # Display Update
    drawCurrentBlock(currentBlock)
    drawBorders()
    drawInfoSurface()
    pygame.display.update()
    
    # Keep gameloop time correctly:
    mainClock.tick(FPS)
    
