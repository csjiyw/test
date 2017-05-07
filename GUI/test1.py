import pygame
import random
import wx
#import IK
#import Robot

black=(0,0,0)
white=(255,255,255)
red=(255,0,0)
yellow=(255,255,0)
blue=(0,0,255)

#myIK=IK.myIK()
#myrobot=Robot()

def draw():
    screen.fill(white)
    allSpritesList.draw(screen)
    split_line.draw(screen,black)

    for i in connect_line_list:
        i.update()
        i.draw(screen,black)

    pygame.display.flip()


class Block(pygame.sprite.Sprite):
    def __init__(self,color,width,height):
        pygame.sprite.Sprite.__init__(self)
        self.color=color
        self.width=width
        self.height=height

        self.image=pygame.Surface([width,height])
        self.image.fill(white)
        self.image.set_colorkey(white)
        pygame.draw.rect(self.image,color,[0,0,width,height])

        self.rect=self.image.get_rect()

        self.front_line=ConnectLine(self,self)
        self.next_line=ConnectLine(self,self)

    def resetPos(self):
        self.rect.x=random.randrange(0,screenWidth)
        self.rect.y=random.randrange(-100,-10)

    def setFront(self,line):
        self.front_line=line

    def setNext(self,line):
        self.next_line=line

    def self_front_connect(self):
        self.front_line.start_block=self

    def self_next_connect(self):
        self.next_line.end_block=self


    def update(self):
        self.rect.y+=1
        if self.rect.y >screenHeight:
            self.resetPos()

class Move(Block):
    def __init__(self,color,width,height):
        Block.__init__(self,color,width,height)
        self.x=0
        self.y=0
        self.z=0

    def set_pos(self,x,y,z):
        self.x=x
        self.y=y
        self.z=z

    def run(self):
        #position,flag=myIK.ik_test('left',self.x,self.y,self.z)
        #myrobot.limb.move_to_joint_positions(position)
        pygame.draw.rect(self.image,red,[0,0,self.width,self.height])
        pygame.draw.rect(self.image,self.color,[5,5,self.width-10,self.height-10])

        draw()
        pygame.time.delay(1000)
        pygame.draw.rect(self.image,self.color,[0,0,self.width,self.height])
        #print(self)
        pass


class Line:
    def __init__(self,start_pos,end_pos):
        self.start_pos=start_pos
        self.end_pos=end_pos

    def update(self):
        return 0

    def draw(self,surface,color):
        pygame.draw.line(surface,color,self.start_pos,self.end_pos)

class ConnectLine(Line):
    def __init__(self,start_block,end_block):
        Line.__init__(self,start_block.rect.midbottom,end_block.rect.midtop)
        self.start_block=start_block
        self.end_block=end_block

    def update(self):
        self.start_pos=self.start_block.rect.midbottom
        self.end_pos=self.end_block.rect.midtop
        return 0

    def connect_self(self,block):
        self.start_block=block
        self.end_block=block

    def is_self_connect(self):
        if(self.start_block==self.end_block):
            return True
        return False

def run_program():
    temp_line=program_start_block.next_line
    while(temp_line.start_block != temp_line.end_block):
        temp_line.end_block.run()
        temp_line=temp_line.end_block.next_line

    print ('finish')
    pass


app=wx.App()
app.MainLoop()
pygame.init()
screenWidth=700
screenHeight=400
screen =pygame.display.set_mode([screenWidth,screenHeight])
pygame.display.set_caption('baxter control program')

blockList=pygame.sprite.RenderPlain()
#allSpritesList=pygame.sprite.RenderPlain()
allSpritesList=pygame.sprite.LayeredUpdates()

connect_line_list=[]
block_wait_to_connect_list=[]
poslist=[]


player=Block(red,70,50)
player.rect.y=200
allSpritesList.add(player)

block1=Block(yellow,70,50)
allSpritesList.add(block1)

block2=Block(blue,70,50)
block2.rect.y=100
allSpritesList.add(block2)

program_start_block=Block(black,70,50)
program_start_block.rect.x=300
allSpritesList.add(program_start_block)
blockList.add(program_start_block)

split_distance=100

split_line=Line((split_distance,5),(split_distance,395))

done=False

clock=pygame.time.Clock()
score=0
flag=0
flag_draw_connect_line=0
flag_createNewBlock1=0
flag_move_block=0



while done==False:

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            run_program()
            pass

        pos =pygame.mouse.get_pos()
        if event.type ==pygame.QUIT:
            done =True
        if event.type==pygame.MOUSEBUTTONDOWN:

            print (event.dict)


            if event.dict['button']==1 :
                #at left side
                if(pos[0]<split_distance):
                    if player.rect.collidepoint(pos):
                        #flag=1
                        poslist.append(player.rect.midbottom)
                        flag_draw_connect_line=1



                    #add new block
                    if block1.rect.collidepoint(pos):
                        flag_createNewBlock1=1
                        temp_block=Move(yellow,70,50)


                        allSpritesList.add(temp_block)
                        allSpritesList.move_to_front(temp_block)

                    if block2.rect.collidepoint(pos):
                        flag_createNewBlock1=1
                        temp_block=Block(blue,70,50)

                        allSpritesList.add(temp_block)
                        allSpritesList.move_to_front(temp_block)

                elif(pos[0]>split_distance):
                    #move block
                    for b in blockList:
                        if b.rect.collidepoint(pos):
                            flag_move_block=1
                            temp_block=b
                            break

            if event.dict['button']==3 :
                if(pos[0]>split_distance):
                    # add connect line
                    for b in blockList:
                        if b.rect.collidepoint(pos):
                            flag_draw_connect_line=1
                            block_wait_to_connect_list.append(b)
                            break

        if event.type == pygame.MOUSEBUTTONUP:
            print (event)

            # region Description
            if event.dict['button']==2 :
                if pos[0]>split_distance:
                    for b in blockList:
                        if(type(b)==Block):
                            continue
                             #add connect line part 2
                        if b.rect.collidepoint(pos):
                            print (type(b))
                            parameters=str(b.x)+','+str(b.y)+','+str(b.z)
                            dlg = wx.TextEntryDialog(None,'What is x,y,z?','Eh??', parameters)
                            #dlg.SetFocus()
                            ret = dlg.ShowModal()
                            if ret == wx.ID_OK:
                               print('You entered: %s\n' % dlg.GetValue())
                               b.x,b.y,b.z=dlg.GetValue().split(',')

                            else:
                                print('You don\'t know')

                            break


            # endregion

            if event.dict['button']==3:
                if flag_draw_connect_line==1 :
                    for b in blockList:
                        # add connect line part 2
                        if b.rect.collidepoint(pos):
                            block_wait_to_connect_list.append(b)
                            start_block=block_wait_to_connect_list.pop(0)
                            end_block=block_wait_to_connect_list.pop(0)
                            if(start_block!=end_block):

                                connect_line=ConnectLine(start_block,end_block)

                                if(not start_block.next_line.is_self_connect()):
                                    start_block.next_line.end_block.self_front_connect()
                                    connect_line_list.remove(start_block.next_line)

                                if(not end_block.front_line.is_self_connect()):
                                    end_block.front_line.start_block.self_next_connect()
                                    connect_line_list.remove(end_block.front_line)

                                start_block.setNext(connect_line)
                                end_block.setFront(connect_line)
                                connect_line_list.append(connect_line)

                                print(connect_line_list)
                            break
                    # reset
                    flag_draw_connect_line=0
                    block_wait_to_connect_list=[]

            if event.dict['button']==1:
                # add block part 2
                if flag_createNewBlock1 ==1:
                    if(pos[0]<split_distance or pygame.sprite.spritecollide(temp_block,blockList,False)):
                        temp_block.kill()
                    else:
                        blockList.add(temp_block)
                    flag_createNewBlock1=0

                    #print( blockList)
                elif flag_move_block==1:
                    flag_move_block=0
                #flag=0;





    if(flag_createNewBlock1==1 ):
        pos =pygame.mouse.get_pos()
        temp_block.rect.x=pos[0]
        temp_block.rect.y=pos[1]

    if( flag_move_block==1):
        pos =pygame.mouse.get_pos()
        if(pos[0]>split_distance):
            temp_block.rect.x=pos[0]
            temp_block.rect.y=pos[1]


    if(flag==1):
        pos =pygame.mouse.get_pos()
        player.rect.x=pos[0]
        player.rect.y=pos[1]

    draw()

    clock.tick(20)

    #blockList.update()
    #pygame.display.flip()


pygame.quit()





