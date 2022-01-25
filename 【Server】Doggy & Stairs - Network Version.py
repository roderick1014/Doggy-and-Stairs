import time
import sys
import random
import tkinter as tk
import socket
import threading
from tkinter import Tk,  Frame, Canvas, ALL, NW

class Constants:
   CurrentDistance = 0
   CurrentDistance2 = 0
   Canvasheight = 600
   Canvaswidth = 600
   CharacterSize =  34
   StairLength = 100
   StairDepth = 20
   Moving = 9 #不錯的是9
   Delay = 30 #不錯的是30
   Falling = False
   DoggyState = 0
   Doggy2State = 0
   BottomEdge = 600
   MaximumStairs = 12
   MinimumStairs = 3
   MoveUpConstant = 3 #值是2
   Life = 10
   Life2  = 10
   Hurt = 4
   DogIm = {}
   HurtDogIm = {}
   Dog2Im = {}
   HurtDog2Im = {}
   LifeIm = {}
   Life2Im = {}
   KeyP = 0
   KeyR = 0
   SendLeft = False
   SendRight = False
   SendHurt = False
   KeepMoving = False
   DoggyRunningRight = False
   DoggyRunningLeft = False
   Gravity =  2#2
   StairGen = False
   TrapGen = False
   
   
class PlayWindow(Canvas):
   
   def __init__(self):
      super().__init__(width = Constants.Canvaswidth,height = Constants.Canvasheight,background="white")
      self.initGame()
      self.pack()
        
   def initGame(self):
      '''Network Apply'''
      self.SERVER = "140.118.115.124"
      self.PORT = 5050
      self.ADDR = (self.SERVER,self.PORT)
      self.Server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      self.Server.bind(self.ADDR)
      self.msg = ''
      self.SendIDX = 'NONO 0'
      self.connected = False
      self.conn = ''
      self.addr = ''
      self.CanConnect = True
      self.GoToTheGame = True
      self.Time = 0
      self.Probability = 0
      self.RandonStairX = 0
      self.leftFrame = 1
      self.rightFrame = 5
      self.DoggyFrame = 0
      self.inGame = True
      self.StairsIndex = 10
      self.HealingStairs = [7,8,9,10]
      self.Stairs = 4
      '''Doggy moving variables'''
      self.moveX = 0
      self.moveY = 0
      '''Starting position'''
      self.DoggyX = 283
      self.DoggyY =  266 #266
      self.Doggy2X = 317
      self.Doggy2Y =  266
      self.InjureTime = 0
      self.Hurting = False
      self.InjureTimeCounting = False
      self.Injure = False
      self.LoadImages()
      self.CreateObj()
      self.bind_all("<KeyPress>",self.onKeyPressed)
      self.bind_all("<KeyRelease>",self.onKeyReleased)
      self.start()

   def AllStart(self):
      self.after(Constants.Delay , self.Timer)
      
   def LoadImages(self):
      self.Ceiling =  tk.PhotoImage(file='Ceiling.png')
      self.TrapStairs = tk.PhotoImage(file='TrapStairs.png')
      self.BackGround = tk.PhotoImage(file='background.png')
      self.StairsImage = tk.PhotoImage(file='Stairs.png') #Import stairs

      Constants.DogIm[0] = tk.PhotoImage(file='Doggy1.png')
      Constants.DogIm[1] = tk.PhotoImage(file='Doggy1-Left1.png')
      Constants.DogIm[2] = tk.PhotoImage(file='Doggy1-Left2.png')
      Constants.DogIm[3] = tk.PhotoImage(file='Doggy1-Left.png')
      Constants.DogIm[4] = tk.PhotoImage(file='Doggy1-2.png')
      Constants.DogIm[5] = tk.PhotoImage(file='Doggy1-Right1.png')
      Constants.DogIm[6] = tk.PhotoImage(file='Doggy1-Right2.png')
      Constants.DogIm[7] = tk.PhotoImage(file='Doggy1-Right.png')

      Constants.HurtDogIm[0] = tk.PhotoImage(file='Doggy1H.png')
      Constants.HurtDogIm[1] = tk.PhotoImage(file='Doggy1_Left1H.png')
      Constants.HurtDogIm[2] = tk.PhotoImage(file='Doggy1_Left2H.png') 
      Constants.HurtDogIm[3] = tk.PhotoImage(file='Doggy1_LeftH.png')
      Constants.HurtDogIm[4] = tk.PhotoImage(file='Doggy1-2H.png')
      Constants.HurtDogIm[5] = tk.PhotoImage(file='Doggy1_Right1H.png')
      Constants.HurtDogIm[6] = tk.PhotoImage(file='Doggy1_Right2H.png')
      Constants.HurtDogIm[7] = tk.PhotoImage(file='Doggy1_RightH.png')

      Constants.Dog2Im[0] = tk.PhotoImage(file='Doggy2.png')
      Constants.Dog2Im[1] = tk.PhotoImage(file='Doggy2-Left1.png') 
      Constants.Dog2Im[2] = tk.PhotoImage(file='Doggy2-Left2.png') 
      Constants.Dog2Im[3] =  tk.PhotoImage(file='Doggy2-Left.png') 
      Constants.Dog2Im[4] = tk.PhotoImage(file='Doggy2-2.png')
      Constants.Dog2Im[5] = tk.PhotoImage(file='Doggy2-Right1.png') 
      Constants.Dog2Im[6] = tk.PhotoImage(file='Doggy2-Right2.png') 
      Constants.Dog2Im[7] = tk.PhotoImage(file='Doggy2-Right.png')

      Constants.HurtDog2Im[0] = tk.PhotoImage(file='Doggy2H.png')
      Constants.HurtDog2Im[1] = tk.PhotoImage(file='Doggy2_Left1H.png')
      Constants.HurtDog2Im[2] = tk.PhotoImage(file='Doggy2_Left2H.png') 
      Constants.HurtDog2Im[3] = tk.PhotoImage(file='Doggy2_LeftH.png')
      Constants.HurtDog2Im[4] = tk.PhotoImage(file='Doggy2-2H.png')
      Constants.HurtDog2Im[5] = tk.PhotoImage(file='Doggy2_Right1H.png')
      Constants.HurtDog2Im[6] = tk.PhotoImage(file='Doggy2_Right2H.png')
      Constants.HurtDog2Im[7] = tk.PhotoImage(file='Doggy2_RightH.png')
      
      Constants.LifeIm[0] = tk.PhotoImage(file='Life-0.png')
      Constants.LifeIm[1] = tk.PhotoImage(file='Life-1.png')
      Constants.LifeIm[2] = tk.PhotoImage(file='Life-2.png')
      Constants.LifeIm[3] = tk.PhotoImage(file='Life-3.png')
      Constants.LifeIm[4] = tk.PhotoImage(file='Life-4.png')
      Constants.LifeIm[5] = tk.PhotoImage(file='Life-5.png')
      Constants.LifeIm[6] = tk.PhotoImage(file='Life-6.png')
      Constants.LifeIm[7] = tk.PhotoImage(file='Life-7.png')
      Constants.LifeIm[8] = tk.PhotoImage(file='Life-8.png')
      Constants.LifeIm[9] = tk.PhotoImage(file='Life-9.png')
      Constants.LifeIm[10] = tk.PhotoImage(file='Life-10.png')
      
      Constants.Life2Im[0] = tk.PhotoImage(file='Life2-0.png')
      Constants.Life2Im[1] = tk.PhotoImage(file='Life2-1.png')
      Constants.Life2Im[2] = tk.PhotoImage(file='Life2-2.png')
      Constants.Life2Im[3] = tk.PhotoImage(file='Life2-3.png')
      Constants.Life2Im[4] = tk.PhotoImage(file='Life2-4.png')
      Constants.Life2Im[5] = tk.PhotoImage(file='Life2-5.png')
      Constants.Life2Im[6] = tk.PhotoImage(file='Life2-6.png')
      Constants.Life2Im[7] = tk.PhotoImage(file='Life2-7.png')
      Constants.Life2Im[8] = tk.PhotoImage(file='Life2-8.png')
      Constants.Life2Im[9] = tk.PhotoImage(file='Life2-9.png')
      Constants.Life2Im[10] = tk.PhotoImage(file='Life2-10.png') 
      
   def CreateObj(self):
       self.create_image(301,60, anchor='n',image=self.BackGround,tag = "Background")
       self.DoggyCharacter = self.create_image(self.DoggyX , self.DoggyY , anchor='n',image=Constants.DogIm[0] , tag="Doggy")
       self.create_image(301,60,anchor='n',image=self.Ceiling,tag = "Ceiling")
       self.create_image(150, 0,anchor='n',image = Constants.LifeIm[10] , tag="MyLifeShow")
       self.Doggy2Character = self.create_image(self.Doggy2X , self.Doggy2Y , anchor='n',image=Constants.Dog2Im[0] , tag="Doggy2")
       self.create_image(450, 0,anchor='n',image = Constants.Life2Im[10] , tag="EnemyLifeShow")
       self.create_image(500, 500, anchor='n',image=self.StairsImage,tag = "Stairs")
       self.create_image(400, 200, anchor='n',image=self.StairsImage,tag = "Stairs")
       self.create_image(200, 450, anchor='n',image=self.StairsImage,tag = "Stairs")
       self.create_image(300, 300, anchor='n',image=self.StairsImage,tag = "Stairs")
       
   def DoggyCurrentState(self):
      if self.inGame:
         Doggy = self.find_withtag("Doggy")
         Crds = self.coords(Doggy)
         if ((0.5*Constants.CharacterSize)<=Crds[0]) and (self.moveX<0):
            self.move(Doggy , self.moveX , 0)
         if ((Constants.BottomEdge-0.5*Constants.CharacterSize)>=Crds[0]) and (self.moveX>0):
            self.move(Doggy , self.moveX , 0)
         if Constants.Falling == True:
            self.move(Doggy,0,self.moveY)

         if (self.Hurting == False):
            if (Constants.DoggyState == 0):
               self.itemconfigure(Doggy,image = Constants.DogIm[0])
               self.DoggyFrame = 0
               Constants.SendLeft = False
               Constants.SendRight = False
            if (Constants.DoggyState == 4):
                self.itemconfigure(Doggy,image = Constants.DogIm[4])
                self.DoggyFrame = 4
                Constants.SendLeft = False
                Constants.SendRight = False
            if (Constants.DoggyRunningLeft == True) and (self.moveX<0):
               if (self.leftFrame == 3):
                  self.leftFrame = 1
                  self.DoggyFrame = 1
               else:
                  self.DoggyFrame +=1
                  self.leftFrame +=1
               self.itemconfigure(Doggy,image = Constants.DogIm[self.leftFrame])
               Constants.SendLeft = True
            if (Constants.DoggyRunningRight == True) and (self.moveX>0):
               if (self.rightFrame == 7):
                  if(self.DoggyFrame==7):
                     self.DoggyFrame = 5
                  self.rightFrame = 5
               else:
                  self.rightFrame +=1
                  self.DoggyFrame += 1
               self.itemconfigure(Doggy,image = Constants.DogIm[self.rightFrame])
               Constants.SendRight = True
         else:
               Constants.SendHurt = True
               if (Constants.DoggyState == 0):
                  self.itemconfigure(Doggy,image = Constants.HurtDogIm[0])
                  self.DoggyFrame = 0
                  Constants.SendLeft = False
                  Constants.SendRight = False
               if (Constants.DoggyState == 4):
                   self.itemconfigure(Doggy,image = Constants.HurtDogIm[4])
                   self.DoggyFrame = 4
                   Constants.SendLeft = False
                   Constants.SendRight = False
               if (Constants.DoggyRunningLeft == True) and (self.moveX<0):
                  if (self.leftFrame == 3):
                     self.leftFrame = 1
                     self.DoggyFrame = 1
                  else:
                     self.DoggyFrame +=1
                     self.leftFrame +=1
                  self.itemconfigure(Doggy,image = Constants.HurtDogIm[self.leftFrame])
                  Constants.SendLeft = True
               if (Constants.DoggyRunningRight == True) and (self.moveX>0):
                  if (self.rightFrame == 7):
                     if(self.DoggyFrame==7):
                        self.DoggyFrame = 5
                     self.rightFrame = 5
                  else:
                     self.rightFrame +=1
                     self.DoggyFrame += 1
                  self.itemconfigure(Doggy,image = Constants.HurtDogIm[self.rightFrame])
                  Constants.SendRight = True

   def Dog2Stand(self):
                Doggy2 = self.find_withtag(5)
                x1 , y1 , x2  , y2 = self.bbox(Doggy2)
                y1 = y1-8
                y2 =  y2 + 20
                overlap = list(self.find_overlapping(x1 , y1 , x2 , y2))
                if (1 in overlap):
                   del overlap[0] ,  overlap[0]
                if ('5' in overlap):
                   del overlap[0]
                if overlap:
                   Dx1 , Dy1 , Dx2  , Dy2 = self.bbox(Doggy2)
                   Sx1 , Sy1 , Sx2  , Sy2 = self.bbox(overlap[0])
                   Constants.CurrentDistance2 = Sy1 - Dy2
                   if (0<Constants.CurrentDistance2 <= 18):
                      self.move(Doggy2,0,Constants.CurrentDistance2)
                   elif  (-20<=Constants.CurrentDistance2 < 0):
                      self.move(Doggy2,0,Constants.CurrentDistance2)
      
   def DontFall(self):
       if self.inGame:
          D1x1 ,D1y1  , D1x2  , D1y2 = self.bbox(self.find_withtag("Doggy"))
          D2x1 ,D2y1  , D2x2  , D2y2 = self.bbox(self.find_withtag("Doggy2"))
          if (self.moveY < 0)and (D1x1 - D2x1 > 33) and (D2x2-D1x2 > 33):
             Constants.Falling =False
             self.moveY = 0
          if (D1y2 == D2y1) and (D1x1 - D2x1 > 33) and (D2x2-D1x2 > 33):
             self.moveY= 0
             Constants.Falling =False
   
   def CheckStairTouch(self):
       if self.inGame:
          Trap = list(self.find_withtag("TrapStairs"))
          Doggy = self.find_withtag(2)
          Crds = self.coords(Doggy)
          x1 , y1 , x2  , y2 = self.bbox(Doggy)
          y2 =  y2 + 20
          overlap = list(self.find_overlapping(x1 , y1 , x2 , y2))
          if (1 in overlap):
             del overlap[0] ,  overlap[0]
          if ('5' in overlap):
             del overlap[0]
          if (Crds[1] <= Constants.BottomEdge-30):
              if overlap:
                 if (3 in overlap):
                    Dx1 , Dy1 , Dx2  , Dy2 = self.bbox(Doggy)
                    Sx1 , Sy1 , Sx2  , Sy2 = self.bbox(3)
                    if (Dy1 - Sy2) < -18:
                       self.move(Doggy,0,53)
                       Constants.Life = Constants.Life -Constants.Hurt
                       Constants.Falling = True
                       self.moveY += Constants.Gravity
                 else:                  
                    Dx1 , Dy1 , Dx2  , Dy2 = self.bbox(Doggy)
                    Sx1 , Sy1 , Sx2  , Sy2 = self.bbox(overlap[0])
                    Constants.CurrentDistance = Sy1 - Dy2
                    if(0==Constants.CurrentDistance):
                       Constants.Falling = False
                       self.moveY = 0
                       x1 , y1 , x2  , y2 = self.bbox(Doggy)
                       y2 =  y2 + 1
                       overlap = list(self.find_overlapping(x1 , y1 , x2 , y2))
                       if (1 in overlap):
                             del overlap[0] ,  overlap[0]
                       if ('5' in overlap):
                             overlap.remove('5')
                       if  (overlap[0] in self.HealingStairs) and Constants.Life< 10 :
                          Constants.Life +=1 
                          self.HealingStairs.remove(overlap[0])
                       if Trap:
                          x1 , y1 , x2  , y2 = self.bbox(Doggy)
                          overlap = list(self.find_overlapping(x1 , y1 , x2 , y2+1))
                          if (1 in overlap):
                             del overlap[0] ,  overlap[0]
                          if ('5' in overlap):
                             overlap.remove('5')
                          if overlap:
                             if overlap[0] in Trap:
                                 self.Injure = True
                    elif  (Constants.CurrentDistance <= 20) and (self.moveY >= Constants.CurrentDistance):
                       self.moveY = Constants.CurrentDistance - Constants.MoveUpConstant
                       Constants.Falling = True
              else:
                 Constants.Falling = True
                 self.moveY +=Constants.Gravity              
          else:
            Constants.Falling = False
            self.inGame = False
            Constants.Life = 0
            self.gameOver()
            self.moveY = 0
    
   def onKeyPressed(self,e):
       Key = e.keysym
       Doggy = self.find_withtag(2)
       Crds = self.coords(Doggy)
       LEFT = "Left"
       RIGHT = "Right"
       if Key == LEFT and self.moveX >= 0:
          self.moveX  = -Constants.Moving
          Constants.DoggyRunningLeft = True
          Constants.KeyP += 1
       if Key == RIGHT and self.moveX <=0:
          self.moveX = Constants.Moving
          Constants.DoggyRunningRight = True
          Constants.KeyP += 1
        
   def onKeyReleased(self,e):
      Key = e.keysym 
      LEFT = "Left"
      RIGHT = "Right"
      if Constants.KeyP > Constants.KeyR:
         if self.moveX >0 and Key == RIGHT:
            Constants.DoggyState = 0
            Constants.KeyR += 1
         elif self.moveX <0 and Key == LEFT:
            Constants.DoggyState = 4
            Constants.KeyR += 1
         else:
            Constants.DoggyState = 0
            Constants.KeyR += 1
      if Constants.KeyP == Constants.KeyR:
          self.moveX =0

   def MoveUpAuto(self):
      if self.inGame:
         MOVEITEM = list(self.find_all())
         del MOVEITEM[0]
         del MOVEITEM[1]
         del MOVEITEM[1]
         del MOVEITEM[2]
         if '5' in MOVEITEM:
            MOVEITEM.remove('5')
         if (Constants.Falling == False):
            for item in MOVEITEM:
                self.move(item , 0, -Constants.MoveUpConstant)
         elif (Constants.Falling == True):
            del MOVEITEM[0]
            for item in MOVEITEM:
                self.move(item , 0, -Constants.MoveUpConstant)

   def StairsDeletor(self):
      StairMembers = list(self.find_withtag("Stairs"))
      Trap = list(self.find_withtag("TrapStairs"))
      if StairMembers:
         CheckOvr = list(self.find_overlapping(0 , 0 , Constants.BottomEdge ,60))
         if CheckOvr:
            Deletion = list(set(CheckOvr).intersection(set(StairMembers)))
         if Deletion:
            Deletion = Deletion[0]
            self.delete(Deletion)
            self.Stairs -= 1
      if Trap:
         CheckOvrTrap = list(self.find_overlapping(0 , 0 , Constants.BottomEdge ,60))
         if CheckOvrTrap:
           Deletion = list(set(CheckOvrTrap).intersection(set(Trap)))
           if Deletion:
              Deletion = Deletion[0]
              self.delete(Deletion)
              self.Stairs -= 1
   
   def StairsGenerator(self):
       if self.inGame:
             if ((self.Time % (2*Constants.Delay)) == 0):
                if (self.Stairs <= Constants.MaximumStairs ):
                   self.Probability = random.randrange(1,100,3)
                   if (self.Probability>5):
                      CheckOvr = self.find_overlapping(0 , Constants.BottomEdge , Constants.BottomEdge , Constants.BottomEdge + 50)
                      if not CheckOvr:
                         self.RandonStairX = random.randrange(50 , Constants.BottomEdge-50 , 3 )
                         self.Probability = random.randrange(1,100,4)
                         if (self.Probability >= 30):
                             self.StairsIndex +=1
                             self.HealingStairs.append(self.StairsIndex)
                             self.create_image( self.RandonStairX, 650, anchor='n',image=self.StairsImage,tag = "Stairs")
                             self.Stairs += 1
                             self.HealingStairs.append(self.StairsIndex)
                             self.SendIDX = "S " + str(self.StairsIndex)
                         else:
                           self.Stairs += 1
                           self.StairsIndex +=1
                           Constants.TrapGen = True
                           self.create_image(self.RandonStairX,650, anchor='n',image=self.TrapStairs,tag = "TrapStairs")
                           self.SendIDX = "T " + str(self.StairsIndex)
  
   def StepOnTrap(self):
      if (self.Injure == True) and (self.InjureTimeCounting == False):
          Constants.Life = Constants.Life - Constants.Hurt
          self.InjureTimeCounting = True
          self.Hurting = True
      if (self.InjureTimeCounting == True):
          self.Injure = False
       
   def Timer(self):            #Timing variation here...
       if self.inGame:
          if Constants.Life < 0:
             Constants.Life = 0
          if Constants.Life2 < 0:
             Constants.Life2 = 0
          self.itemconfigure(self.find_withtag("MyLifeShow"),image = Constants.LifeIm[Constants.Life])
          self.itemconfigure(self.find_withtag("EnemyLifeShow"),image = Constants.Life2Im[Constants.Life2])
          self.StepOnTrap()
          if (self.InjureTimeCounting == True):
            self.InjureTime += Constants.Delay
            if (self.InjureTime == 30*Constants.Delay):
               self.InjureTime = 0
               self.Injure = False
               self.InjureTimeCounting = False
               self.Hurting = False
          if (Constants.Life<=0):
             self.inGame = False
             self.CanConnect = False
             self.gameOver()
          self.Time += Constants.Delay
          if ((self.Time % (2*Constants.Delay)) == 0):
              self.StairsGenerator()
          self.StairsDeletor()
          self.after(Constants.Delay , self.Timer)
          self.CheckStairTouch()
          self.DontFall()
          self.DoggyCurrentState()
          self.Message()
          self.MoveUpAuto()
          self.Dog2Stand()
      
   def Message(self):
         if self.inGame:
               Doggy2 = self.find_withtag("Doggy2")
               Doggy1 = self.find_withtag("Doggy")
               Crds = self.coords(Doggy1)
               Crds2 = self.coords(Doggy2)
               if (self.msg.startswith("$:")):
                  Info = self.msg.split(" ")
                  Constants.Doggy2State = int(Info[1])
                  self.move(Doggy2,int(float(Info[2]))-Crds2[0],int(float(Info[3]))-Crds2[1]) #-29
                  Constants.Life2 = int(Info[4])              
                  if Info[5] == 'N':
                     self.itemconfigure(Doggy2,image = Constants.Dog2Im[Constants.Doggy2State])
                  else:
                     self.itemconfigure(Doggy2,image = Constants.HurtDog2Im[Constants.Doggy2State])
               
               if (Constants.SendLeft == True) and (Constants.SendHurt == False):
                  Msg = "$: "+str(self.leftFrame)+" "+str(int(Crds[0]))+" "+str(int(Crds[1]))+" "+str(Constants.Life)+" "+str(self.SendIDX)+" "+str(self.RandonStairX)+" N"
                  self.conn.send(Msg.encode())
                  Constants.SendLeft = False
               elif (Constants.SendLeft == True) and (Constants.SendHurt == True):#
                  Msg = "$: "+str(self.leftFrame)+" "+str(int(Crds[0]))+" "+str(int(Crds[1]))+" "+str(Constants.Life)+" "+str(self.SendIDX)+" "+str(self.RandonStairX)+" H"
                  self.conn.send(Msg.encode())
                  Constants.SendLeft = False
                  Constants.SendHurt = False
               elif (Constants.SendRight == True) and (Constants.SendHurt == False):
                  Msg = "$: "+str(self.rightFrame)+" "+str(int(Crds[0]))+" "+str(int(Crds[1]))+" "+str(Constants.Life)+" "+str(self.SendIDX)+" "+str(self.RandonStairX)+" N"
                  self.conn.send(Msg.encode())
                  Constants.SendRight = False
               elif (Constants.SendRight == True) and (Constants.SendHurt == True): #
                  Msg = "$: "+str(self.rightFrame)+" "+str(int(Crds[0]))+" "+str(int(Crds[1]))+" "+str(Constants.Life)+" "+str(self.SendIDX)+" "+str(self.RandonStairX)+" H"
                  self.conn.send(Msg.encode())
                  Constants.SendRight = False
                  Constants.SendHurt = False
               elif (Constants.SendRight == False) and (Constants.SendLeft == False):
                   if (Constants.SendHurt == False):
                     Msg = "$: "+str(self.DoggyFrame)+" "+str(int(Crds[0]))+" "+str(int(Crds[1]))+" "+str(Constants.Life)+" "+str(self.SendIDX)+" "+str(self.RandonStairX)+" N"
                     self.conn.send(Msg.encode())
                   else:
                      Msg = "$: "+str(self.DoggyFrame)+" "+str(int(Crds[0]))+" "+str(int(Crds[1]))+" "+str(Constants.Life)+" "+str(self.SendIDX)+" "+str(self.RandonStairX)+" H"
                      self.conn.send(Msg.encode())
                      Constants.SendHurt = False
               Constants.StairGen = False
         
   def gameOver(self):
        self.CanConnect = False
        self.conn.close()
        self.delete(ALL)
        self.inGame = False
        self.create_text(self.winfo_width() /2, self.winfo_height()/2,text="Game Over", fill="Black")
   
   def handle_client(self):
       self.connected = True
       while self.connected:
           if (self.GoToTheGame == True):
              self.AllStart()
              self.GoToTheGame = False
           if(self.inGame == False):
               self.connected = False
               self.conn.close()
           if(self.CanConnect == True):
               self.msg = self.conn.recv(4096).decode()
       self.conn.close()

   def start(self):
      self.Server.listen()
      self.conn , self.addr = self.Server.accept()
      thread = threading.Thread(target = self.handle_client)
      thread.start()

class Doggy(Frame):
   def __init__(self):
      super().__init__()
      self.master.title('Doggy_SERVER')
      self.PlayWindow = PlayWindow()   #Start Condition
      self.pack()

def main():
   root = Tk()
   root.title('Doggy_SERVER')
   root.geometry('800x600')
   nib = Doggy()
   root.mainloop()

if __name__ == '__main__':
      main()
