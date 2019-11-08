from random import randrange as rnd,choice
from tkinter import*
import math
import time
root=Tk()
fr=Frame(root)
root.geometry('800x600')
canv=Canvas(root,bg='white')
canv.pack(fill=BOTH,expand=1)
class ball():
 def __init__(self,x=40,y=450):
  self.x=x
  self.y=y
  self.r=10
  self.vx=0
  self.vy=0
  self.color=choice(['blue','green','red','brown'])
  self.id=canv.create_oval(self.x-self.r,self.y-self.r,self.x+self.r,self.y+self.r,fill=self.color)
  self.live=30
 def set_coords(self):
  canv.coords(self.id,self.x-self.r,self.y-self.r,self.x+self.r,self.y+self.r)
 def move(self):
  if self.y<=500:
   self.vy-=1.2
   self.y-=self.vy
   self.x+=self.vx
   self.vx*=0.99
   self.set_coords()
  else:
   if self.vx**2+self.vy**2>10:
    self.vy=-self.vy/2
    self.vx=self.vx/2
    self.y=499
   if self.live<0:
    balls.pop(balls.index(self))
    canv.delete(self.id)
   else:
    self.live-=1
  if self.x>780:
   self.vx=-self.vx/2
   self.x=779
 def hittest(self,ob):
  if abs(ob.x-self.x)<=(self.r+ob.r)and abs(ob.y-self.y)<=(self.r+ob.r):
   return True
  else:
   return False
"""
ÐÐ»Ð°ÑÑ gun Ð¾Ð¿Ð¸ÑÑÐ²Ð°ÐµÑ Ð¿ÑÑÐºÑ. 
"""
class gun():
 def __init__(self,x=40,y=450):
  self.f2_power=10
  self.f2_on=0
  self.an=1
  self.ball=0
  self.x=x
  self.y=y
  self.id=canv.create_line(x,y,x+30,y-30,width=7)
 def fire2_start(self):
  self.f2_on=1
 def fire2_end(self):
  global balls,bullet
  bullet+=1
  self.ball=ball(self.x-10,self.y)
  self.ball.r+=5
  self.an=math.atan((y_coord-self.ball.y)/(x_coord-self.ball.x))
  self.ball.vx=self.f2_power*math.cos(self.an)
  self.ball.vy=-self.f2_power*math.sin(self.an)
  balls+=[self.ball]
  self.f2_on=0
  self.f2_power=10
 def targeting(self,x,y):
  self.an=math.atan((y-self.y)/(x-self.x)) 
  if self.f2_on:
   canv.itemconfig(self.id,fill='orange')
  else:
   canv.itemconfig(self.id,fill='black')
  canv.coords(self.id,self.x,self.y,self.x+max(self.f2_power,20)*math.cos(self.an),self.y+max(self.f2_power,20)*math.sin(self.an))
 def power_up(self):
  if self.f2_on:
   if self.f2_power<100:
    self.f2_power+=1
   canv.itemconfig(self.id,fill='orange')
  else:
   canv.itemconfig(self.id,fill='black')
"""
ÐÐ»Ð°ÑÑ target Ð¾Ð¿Ð¸ÑÑÐ²Ð°ÐµÑ ÑÐµÐ»Ñ. 
"""

class target():

    def __init__(self):
        '''Конструктор класса target

        args
        x, y - coords
        vx, vy - start velocity
        '''
        self.points = 0
        self.live = 1
        self.id = canv.create_oval(0, 0, 0, 0)
        self.id_points = canv.create_text(30, 30, text=self.points, font='28')
        self.new_target()
        self.vx = rnd(-10, 10)
        self.vy = rnd(-10, 10)

    def new_target(self):
        """ Инициализация новой цели. """
        x = self.x = rnd(150, 700)
        y = self.y = rnd(150, 550)
        r = self.r = rnd(5, 50)
        color = self.color = 'red'
        canv.coords(self.id, x - r, y - r, x + r, y + r)
        canv.itemconfig(self.id, fill=color)

    def hit(self, points=1):
        """Попадание шарика в цель."""
        canv.coords(self.id, -10, -10, -10, -10)
        self.points += points
        canv.itemconfig(self.id_points, text=self.points)

    def move(self):
        if self.x + self.vx >= 780:
            self.x = 780
        if self.x + self.vx <= 20:
            self.x = 20
        if (self.x >= 780) or (self.x <= 20):
            self.vx = - self.vx
        if (self.y >= 550) or (self.y <= 50):
            self.vy = - self.vy
        self.x += self.vx
        self.y += self.vy
        canv.move(self.id, self.vx, self.vy)

t1=target()
screen1=canv.create_text(400,300,text='',font='28')
n = int(input())
g = [0]*(n+10)
for i in range (n):
 g[i+1] = gun(rnd(0,100), rnd(10,450))

bullet=0
balls=[]

def targeting(event):
 global g,x_coord, y_coord, n
 x_coord = event.x
 y_coord = event.y
 for i in range(n):
  g[i+1].targeting(x_coord,y_coord)

def fire2_start(event):
 global g,n
 for i in range(n):
  g[i+1].fire2_start()

def fire2_end(event):
 global g,x_coord,y_coord,n
 for i in range(n):
  g[i+1].fire2_end()

def power_up():
 global g,n
 for i in range(n):
  g[i+1].power_up()

def new_game(event=''):
 global gun,t1,screen1,balls,bullet,g,n
 t1.new_target()
 bullet=0
 balls=[]
 canv.bind('<Button-1>',fire2_start)
 canv.bind('<ButtonRelease-1>',fire2_end)
 canv.bind('<Motion>',targeting)

 z=0.03
 t1.live=1
 while t1.live or balls:
  for b in balls:
   b.move()
   if b.hittest(t1)and t1.live:
    t1.live=0
    t1.hit()
    canv.bind('<Button-1>','')
    canv.bind('<ButtonRelease-1>','')
    canv.itemconfig(screen1,text='ÐÑ ÑÐ½Ð¸ÑÑÐ¾Ð¶Ð¸Ð»Ð¸ ÑÐµÐ»Ñ Ð·Ð° '+str(bullet)+' Ð²ÑÑÑÑÐµÐ»Ð¾Ð²')
  canv.update()
  t1.move()
  time.sleep(0.03)
  power_up()
 canv.itemconfig(screen1,text='')
 canv.delete(gun)
 root.after(750,new_game)
new_game() 
mainloop()



#!!!При запуске в консоль пишите количество пушек

