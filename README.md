##  **Doggy_and_Stairs** 
#### **A simplified rebuilding of NS-SHAFT game which is written by python with only tkinter (without pygame).** ####
#### **Dec. 2020**

---
![2](https://user-images.githubusercontent.com/73574008/165480533-0185f474-8011-4782-ab37-c4d8bf1bcf8d.PNG)


#### **For single player:**

```
python SinglePlayer.py
```
---

#### **For dual-player in same local area network.**

#### **Modify the address in 【Server】Doggy & Stairs - Network Version.py:**
```
class PlayWindow(Canvas):
   
   def __init__(self):
      super().__init__(width = Constants.Canvaswidth,height = Constants.Canvasheight,background="white")
      self.initGame()
      self.pack()
        
   def initGame(self):
      '''Network Apply'''
      self.SERVER = "140.118.115.124"   #　← Modify the address here.
      self.PORT = 5050
      self.ADDR = (self.SERVER,self.PORT)
```

#### **Modify the address in 【Client】Doggy & Stairs - Network Version.py:**
```
class PlayWindow(Canvas):

   def __init__(self):
      super().__init__(width = Constants.Canvaswidth,height = Constants.Canvasheight,background="white")
      self.initGame()
      self.pack()
        
   def initGame(self):
      '''Network Apply'''
      self.CLIENT = "127.0.0.1"          #　← Modify the address here.
      self.PORT = 5050
      self.ADDR = (self.CLIENT,self.PORT)
```

#### **Then run the code:**
```
python '.\【Server】Doggy & Stairs - Network Version.py'
```
#### **for server and**
```
python '.\【Client】Doggy & Stairs - Network Version.py'
```
#### **note that the Server has to launch the code first.**
