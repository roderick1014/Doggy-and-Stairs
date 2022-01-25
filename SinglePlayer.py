import time
import sys
import random
import tkinter as tk
from tkinter import Tk,  Frame, Canvas, ALL, NW

class Constants:
   CurrentDistance = 0
   Canvasheight = 600
   Canvaswidth = 600
   CharacterSize =  34
   StairLength = 100
   StairDepth = 20
   Moving = 10
   Delay = 20
   Falling = False
   DoggyState = 0
   BottomEdge = 600
   MaximumStairs = 12
   MinimumStairs = 3
   MoveUpConstant = 5
   Life = 10
   Hurt = 4
   KeyP = 0
   KeyR = 0 
   DogIm = {}
   HurtDogIm = {}
   HurtState = False
   KeepMoving = False
   DoggyRunningRight = False
   DoggyRunningLeft = False
   Gravity = 3 #2
   LifeIm = {}
   
class PlayWindow(Canvas):

   def __init__(self):
      super().__init__(width = Constants.Canvaswidth,height = Constants.Canvasheight,background="white")
      self.initGame()
      self.pack()
        
   def initGame(self):
      self.Time = 0
      self.MovingDelay = 0
      self.Probability = 0
      self.RandonStairX = 0
      self.leftFrame = 1
      self.rightFrame = 5
      self.inGame = True
      self.StairsIndex = 8
      self.HealingStairs = [5,6,7,8]
      self.Stairs = 4
      self.HurtDoggy = False
      '''Doggy moving variables'''
      self.moveX = 0
      self.moveY = 0
      '''Starting position'''
      self.DoggyX = 300
      self.DoggyY =  266 #266
      self.InjureTime = 0
      self.Hurting = False
      self.InjureTimeCounting = False
      self.Injure = False
      self.LoadImages()
      self.CreateObj()
      self.bind_all("<KeyPress>",self.onKeyPressed)
      self.bind_all("<KeyRelease>",self.onKeyReleased)
      self.after(Constants.Delay , self.Timer)
      
      
   def LoadImages(self):
      self.Ceiling =  tk.PhotoImage(file='Ceiling.png')
      self.TrapStairs = tk.PhotoImage(file='TrapStairs.png')
      self.BackGround = tk.PhotoImage(file='background.png')
      self.StairsImage = tk.PhotoImage(file='Stairs.png') #Import stairs
      self.DoggyImageData0 = tk.PhotoImage(file='Doggy1.png')  #Doggy stand and face right
      self.DoggyImageData1 = tk.PhotoImage(file='Doggy1-Left1.png') #Doggy moving left
      self.DoggyImageData2 = tk.PhotoImage(file='Doggy1-Left2.png') #Doggy moving left
      self.DoggyImageData3 = tk.PhotoImage(file='Doggy1-Left.png')   #Doggy face left and stop
      self.DoggyImageData4 = tk.PhotoImage(file='Doggy1-2.png') #Doggy stand and face left
      self.DoggyImageData5 = tk.PhotoImage(file='Doggy1-Right1.png') #Doggy moving right
      self.DoggyImageData6 = tk.PhotoImage(file='Doggy1-Right2.png') #Doggy moving right
      self.DoggyImageData7 = tk.PhotoImage(file='Doggy1-Right.png') #Doggy face right and stop
      
      Constants.DogIm[0] = self.DoggyImageData0
      Constants.DogIm[1] = self.DoggyImageData1
      Constants.DogIm[2] = self.DoggyImageData2
      Constants.DogIm[3] = self.DoggyImageData3
      Constants.DogIm[4] = self.DoggyImageData4
      Constants.DogIm[5] = self.DoggyImageData5
      Constants.DogIm[6] = self.DoggyImageData6
      Constants.DogIm[7] = self.DoggyImageData7

      Constants.HurtDogIm[0] = tk.PhotoImage(file='Doggy1H.png')
      Constants.HurtDogIm[1] = tk.PhotoImage(file='Doggy1_Left1H.png')
      Constants.HurtDogIm[2] = tk.PhotoImage(file='Doggy1_Left2H.png') 
      Constants.HurtDogIm[3] = tk.PhotoImage(file='Doggy1_LeftH.png')
      Constants.HurtDogIm[4] = tk.PhotoImage(file='Doggy1-2H.png')
      Constants.HurtDogIm[5] = tk.PhotoImage(file='Doggy1_Right1H.png')
      Constants.HurtDogIm[6] = tk.PhotoImage(file='Doggy1_Right2H.png')
      Constants.HurtDogIm[7] = tk.PhotoImage(file='Doggy1_RightH.png')
      
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

   def CreateObj(self):
       self.create_image(301,60, anchor='n',image=self.BackGround,tag = "Background")
       self.DoggyCharacter = self.create_image(self.DoggyX , self.DoggyY , anchor='n',image=self.DoggyImageData0 , tag="Doggy")
       self.create_image(301,60,anchor='n',image=self.Ceiling,tag = "Ceiling")
       self.create_image(300, 0,anchor='n',image = Constants.LifeIm[10] , tag="LifeShow")
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
         self.move(Doggy,0,self.moveY)
         
         if (self.Hurting == False):
            if (Constants.DoggyState == 0):
               self.itemconfigure(Doggy,image = Constants.DogIm[0])
            if (Constants.DoggyState == 4):
                self.itemconfigure(Doggy,image = Constants.DogIm[4])
            if (Constants.DoggyRunningLeft == True) and (self.moveX<0):
               if (self.leftFrame == 3):
                  self.leftFrame = 1
               else:
                  self.leftFrame +=1
               self.itemconfigure(Doggy,image = Constants.DogIm[self.leftFrame])
            if (Constants.DoggyRunningRight == True) and (self.moveX>0):
               if (self.rightFrame == 7):
                  self.rightFrame = 5
               else:
                  self.rightFrame +=1
               self.itemconfigure(Doggy,image = Constants.DogIm[self.rightFrame])
         else:
            if (Constants.DoggyState == 0):
               self.itemconfigure(Doggy,image = Constants.HurtDogIm[0])
            if (Constants.DoggyState == 4):
                self.itemconfigure(Doggy,image = Constants.HurtDogIm[4])
            if (Constants.DoggyRunningLeft == True) and (self.moveX<0):
               if (self.leftFrame == 3):
                  self.leftFrame = 1
               else:
                  self.leftFrame +=1
               self.itemconfigure(Doggy,image = Constants.HurtDogIm[self.leftFrame])
            if (Constants.DoggyRunningRight == True) and (self.moveX>0):
               if (self.rightFrame == 7):
                  self.rightFrame = 5
               else:
                  self.rightFrame +=1
               self.itemconfigure(Doggy,image = Constants.HurtDogIm[self.rightFrame])
            
   def CheckStairTouch(self):
       if self.inGame:
          Trap = list(self.find_withtag("TrapStairs"))
          Doggy = self.find_withtag(2)
          Crds = self.coords(Doggy)
          x1 , y1 , x2  , y2 = self.bbox(Doggy)
          y2 =  y2 + 20
          overlap = list(self.find_overlapping(x1 , y1 , x2 , y2))
          #print(overlap)
          if (1 in overlap):
             del overlap[0] ,  overlap[0]
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
                       #print(overlap[0])
                       if  (overlap[0] in self.HealingStairs) and Constants.Life< 10 :
                          Constants.Life +=1 #Life healing
                          self.HealingStairs.remove(overlap[0])
                          #print("Heal")
                       
                       if Trap:
                          x1 , y1 , x2  , y2 = self.bbox(Doggy)
                          overlap = list(self.find_overlapping(x1 , y1 , x2 , y2+1))
                          if (1 in overlap):
                             del overlap[0] ,  overlap[0]
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
            self.gameOver()
            self.moveY = 0
            self.gameOver()
    
   def onKeyPressed(self,e):
       Key = e.keysym
       Doggy = self.find_withtag(2)
       Crds = self.coords(Doggy)
       LEFT = "Left"
       RIGHT = "Right"
       
       if Key == LEFT and self.moveX >= 0:
        # Constants.KeepMoving = True
          self.moveX  = -Constants.Moving
          Constants.DoggyRunningLeft = True
          Constants.KeyP += 1
          #Constants.DoggyRunningRight = False
       
       if Key == RIGHT and self.moveX <=0:
          self.moveX = Constants.Moving
          #Constants.KeepMoving = True
         # Constants.DoggyRunningLeft = False
          Constants.KeyP += 1
          Constants.DoggyRunningRight = True

       
   def onKeyReleased(self,e):
      Key = e.keysym
      
      LEFT = "Left"
      RIGHT = "Right"
      #Constants.KeyR += 1
      
      if Constants.KeyP > Constants.KeyR:
         if self.moveX >0 and Key == RIGHT:
            Constants.DoggyState = 0
            Constants.KeyR += 1
         
         elif self.moveX <0 and Key == LEFT:
            Constants.DoggyState = 4
            Constants.KeyR += 1
            #print("Release   " , Key)
         else:
            Constants.DoggyState = 0
            Constants.KeyR += 1
            
      if Constants.KeyP == Constants.KeyR:
          self.moveX =0
      #print("KL  ",Constants.KeyR)

   def MoveUpAuto(self):
      if self.inGame:
         MOVEITEM = list(self.find_all())
         del MOVEITEM[0]
         del MOVEITEM[1]
         del MOVEITEM[1]
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
            #print(Deletion)
            #self.HealingStairs.remove(Deletion)
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
          if (self.Stairs <= Constants.MaximumStairs ):
             self.Probability = random.randrange(1,100,3)
             #print(self.Probability)
             if (self.Probability>5):
                CheckOvr = self.find_overlapping(0 , Constants.BottomEdge , Constants.BottomEdge , Constants.BottomEdge + 50)
                if not CheckOvr:
                   self.RandonStairX = random.randrange(80 , Constants.BottomEdge-80 , 3 )
                   self.Probability = random.randrange(1,100,4)
                   if (self.Probability >= 30):
                       self.create_image( self.RandonStairX, 650, anchor='n',image=self.StairsImage,tag = "Stairs")
                       self.Stairs += 1
                       self.StairsIndex +=1
                       self.HealingStairs.append(self.StairsIndex)
                       #print(self.HealingStairs)
                   else:
                       self.create_image(self.RandonStairX,650, anchor='n',image=self.TrapStairs,tag = "TrapStairs")
                       self.Stairs += 1
                       self.StairsIndex +=1
  
   def StepOnTrap(self):
      if (self.Injure == True) and (self.InjureTimeCounting == False):
          Constants.Life = Constants.Life - Constants.Hurt
          self.Hurting = True
          self.InjureTimeCounting = True
          #print("Hurt")
      if (self.InjureTimeCounting == True):
          self.Injure = False
       
   def Timer(self):            #Timing variation here...
       if self.inGame:
          self.itemconfigure(self.find_withtag("LifeShow"),image = Constants.LifeIm[Constants.Life])
          self.StepOnTrap()
          if (self.InjureTimeCounting == True):
            self.InjureTime += Constants.Delay
            
            if (self.InjureTime == 30*Constants.Delay):
               #print("count complete")
               self.InjureTime = 0
               self.Injure = False
               self.InjureTimeCounting = False
               self.Hurting = False
               
          if (Constants.Life<=0):   
             self.inGame = False
             self.gameOver()
             
          self.Time += Constants.Delay
          if ((self.Time % (2*Constants.Delay)) == 0):
              self.StairsGenerator()

          self.StairsDeletor()
          self.after(Constants.Delay , self.Timer)
          self.CheckStairTouch()
          self.DoggyCurrentState()
          self.MoveUpAuto()
          
   def gameOver(self):
        self.delete(ALL)
        self.inGame = False
        self.create_text(self.winfo_width() /2, self.winfo_height()/2,text="Game Over", fill="Black")

class Doggy(Frame):
   def __init__(self):
      super().__init__()
      self.master.title('Doggy')
      self.PlayWindow = PlayWindow()
      self.pack()

def main():
   root = Tk()
   root.title('Doggy')
   root.geometry('800x600')
   nib = Doggy()
   root.mainloop()

if __name__ == '__main__':
      main()
