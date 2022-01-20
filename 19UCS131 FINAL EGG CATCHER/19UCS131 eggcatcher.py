from itertools import cycle
from random import randrange
from PIL import ImageTk,Image
from tkinter import Canvas, Text,Tk,messagebox,font
#  Above segment helps us to import various LIBRARIES from their MODULES 



canvas_width=1300
canvas_height=800

root =Tk()

c=Canvas(root,width=canvas_width,height=canvas_height)
bgimage=ImageTk.PhotoImage(Image.open("2122578.png"))
c.create_image(0,0,anchor="nw",image=bgimage)

c.pack()

color_cycle=cycle(["#ffe6e6","#e6ffe6","#cceeff","#ccffdd","#ffffb3"])
egg_width=45
egg_height=55
egg_score=10
egg_speed=60
egg_interval=2000

difficulty=0.95
catcher_color="#fff"
catcher_width=100
catcher_height=100
catcher_startx=canvas_width/2 - catcher_width/2
catcher_starty=canvas_height - catcher_height - 20
catcher_startx1=catcher_startx +catcher_width
catcher_starty1=catcher_starty+catcher_height

catcher=c.create_arc(catcher_startx,catcher_starty,catcher_startx1,catcher_starty1,start=200,extent=140,style="arc",outline=catcher_color,width=3)

game_font=font.nametofont("TkFixedFont")
game_font.config(size=40)

score=0
score_text=c.create_text(10,10,anchor="nw",font=game_font,fill="#fff",text="Score :"+str(score))

lives_remaining=3
lives_text=c.create_text(canvas_width-10,10, anchor="ne" ,font=game_font,fill="#fff",text="Lives :"+str(lives_remaining))

eggs=[]


def create_eggs():
    x=randrange(100,1000)
    y=4
    new_egg=c.create_oval(x,y,x+egg_width,y+egg_height,fill=next(color_cycle),width=0)
    eggs.append(new_egg)
    root.after(egg_interval,create_eggs)

def move_eggs():
    for egg in eggs:
        (eggx,eggy,eggx1,eggy1)=c.coords(egg)
        c.move(egg,0,10)
        if eggy1>canvas_height:
            egg_dropped(egg)
    root.after(egg_speed,move_eggs)

def egg_dropped(egg):
    eggs.remove(egg)
    c.delete(egg)
    lose_a_life()
    if lives_remaining==0:
        messagebox.showinfo("Game Over!","Final Score:  "+str(score))
        root.destroy() 

def lose_a_life():
    global lives_remaining
    lives_remaining=lives_remaining-1
    c.itemconfigure(lives_text,text="Lives: "+str(lives_remaining))


def catch():
    (catcherx,catchery,catcherx1,catchery1)=c.coords(catcher)
    for egg in eggs:
        (eggx,eggy,eggx1,eggy1)=c.coords(egg)
        if catcherx < eggx and catcherx1 > eggx1 and  catchery1-eggy1<35 :
            eggs.remove(egg)
            c.delete(egg)
            increase_score(egg_score)
    root.after(100,catch)

def increase_score(points):
    global score , egg_speed , egg_interval
    score=score+points

    egg_speed=int(egg_speed*difficulty)    
    # egg_interval=int(egg_speed*difficulty) # THIS SEGMENT WAS CAUSING CREATION OF TOO MANY EGGS AFTER FEW CATCHES

    c.itemconfigure(score_text,text="Score :"+str(score))

def mover(event):
    (x,y,x1,y1)=c.coords(catcher)
    if x1<canvas_width:
        c.move(catcher,20,0)

def movel(event):
    (x,y,x1,y1)=c.coords(catcher)
    if x>0:
        c.move(catcher,-20,0)

c.bind("<Left>",movel)
c.bind("<Right>",mover)
c.focus_set()

root.after(2000,create_eggs)
root.after(1000,move_eggs)
root.after(1000,catch)


root.mainloop()
