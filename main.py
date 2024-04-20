import customtkinter
from CTkMessagebox import CTkMessagebox
import tkinter as tk
from PIL import Image,ImageTk
from pygame import mixer
from dijkstra import Dijkstra
from marks import Marks
from car_line import Line

class App(customtkinter.CTk):
  
    def __init__(self):
        super().__init__()

        self.title("Gaza Strip Navigation")
        self.geometry("1200x800")
        self.geometry(f"+{350}+{100}")
        self.minsize(1200, 800)
        self.bind("<Command-w>", self.destroy)
        customtkinter.set_appearance_mode("dark")

        self.dj = Dijkstra()
        self.marker_list=[]
        self.path_list=[]
        self.lines=[]

        ### create Frames and imgaes ###
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_left = customtkinter.CTkFrame(self, width=180, corner_radius=0)
        self.frame_left.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")

        self.frame_right = customtkinter.CTkFrame(master=self, corner_radius=0,width=1020,height=800)
        
        self.frame_right.grid(row=0, column=1, rowspan=1, pady=0, padx=0, sticky="nsew")

        self.logo_image = customtkinter.CTkImage(Image.open("image/map.png"),size=(45,45))

        self.logoIMG = Image.open("image/continents.png").resize((130, 130))
        self.logo = ImageTk.PhotoImage(self.logoIMG)
        
        self.mapIMG = Image.open("image/map.png").resize((70, 70))
        self.logo_map = ImageTk.PhotoImage(self.mapIMG)

        self.markIMG = Image.open("image/pin.png").resize((20, 20))
        self.mark_image = ImageTk.PhotoImage(self.markIMG)
       
        self.startIMG = Image.open("image/racing-flag.png").resize((30, 30))
        self.start_image = ImageTk.PhotoImage(self.startIMG)

        self.endIMG = Image.open("image/finish.png").resize((35, 35))
        self.end_image = ImageTk.PhotoImage(self.endIMG)
        
        ### frame_left ####
        self.label= customtkinter.CTkLabel(self.frame_left,text="",image=self.logo_image)
        self.label.place(x=60,y=1)

        self.button_1 = customtkinter.CTkButton(self.frame_left,text="Get Cities And Dierction",command=self.load)
        self.button_1.place(x=10,y=60)

        self.button_2 = customtkinter.CTkButton(self.frame_left,text="Clear",width=160,command=self.clear)
        self.button_2.place(x=10,y=105)

        self.start_label = customtkinter.CTkLabel(self.frame_left, text="Start From", anchor="w")
        self.start_label.place(x=50,y=180)
        
        self.startVar=customtkinter.StringVar()
        self.start_option = customtkinter.CTkOptionMenu(self.frame_left, values=[""],state="disabled",variable=self.startVar,command=lambda x: self.on_selectStrat("option_var.get()"))
        self.start_option.place(x=16,y=210)


        self.end_label = customtkinter.CTkLabel(self.frame_left, text="End At", anchor="w")
        self.end_label.place(x=60,y=250)
       
        self.endVar=customtkinter.StringVar()
        self.end_option = customtkinter.CTkOptionMenu(self.frame_left, values=[""],state="disabled",variable=self.endVar,command=lambda x: self.on_selectEnd("option_var.get()"))
        self.end_option.place(x=16,y=280)


        self.button_3 = customtkinter.CTkButton(self.frame_left,text="Show",width=100,command=self.show,state="disabled",fg_color="Black")
        self.button_3.place(x=40,y=350)

        self.textBox= customtkinter.CTkTextbox(self.frame_left,state="disabled",width=160,corner_radius=8,font=("Times New Roman",13,"bold"))
        self.textBox.place(x=10,y=390)

        self.res_label= customtkinter.CTkLabel(self.frame_left,text="",text_color="red",font=("Times New Roman",19,"bold"))
        self.res_label.place(x=48,y=620)

        self.error_label= customtkinter.CTkLabel(self.frame_left,text="",text_color="red",font=("Times New Roman",18,"underline"))
        self.error_label.place(x=5,y=620)


        ### frame_right ###
        self.mapIMG = Image.open("image/mapp.jpeg").resize((1020, 800))
        self.map_image = ImageTk.PhotoImage(self.mapIMG)
        self.canvas = customtkinter.CTkCanvas(self.frame_right, width=1020, height=800)
        self.canvas.pack(side="top",fill="both",expand=True)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.map_image)
        self.canvas.create_text(210,130,text="   Dijkstra 23-24",font=('Times New Roman', 20, 'bold'))
        self.canvas.create_image(150, 140, anchor=tk.NW, image=self.logo)
        self.canvas.create_image(690, 440, anchor=tk.NW, image=self.logo_map)
        self.main_text=self.canvas.create_text(730,520, text="Gaza Strip Navigation", font=("Times new roman", 20,'bold'), fill="Red")
        
        self.labelS = customtkinter.CTkLabel(self.canvas, text_color="Red",bg_color="White",font=('Helvetica', 14, 'bold'))
        self.labelE = customtkinter.CTkLabel(self.canvas, text_color="Red",bg_color="White",font=('Helvetica', 14, 'bold'))
     

    #read file method
    def load(self):

        mixer.init()
        mixer.music.load("sound/click.wav")
        mixer.music.play()
        
        file = 'xx.txt'
        self.dj.read(file)

        self.startVar.set("")
        self.endVar.set("")

        self.textBox.configure(state="normal")
        self.textBox.delete("0.0", customtkinter.END) 
        self.textBox.configure(state="disabled")

        self.res_label.configure(text="")
 
        str = []
        for i in self.dj.vertic.values() :
            # or i.st == "TRUE"
            if i.st == "FALSE":
                str+= [i.name]
                self.create_vertices(i.name,float(i.x),float(i.y))
                x_cor , y_cor = self.address_to_img(i.x,i.y)
                self.canvas.create_text(x_cor,y_cor, text=i.name,font=('Helvetica', 14, 'bold'))
                # x=customtkinter.CTkLabel(self.canvas, text_color="Red",bg_color="White",font=('Helvetica', 14, 'bold'))
                # x.place(x=i.x+20,y=i.y-40)
                # x.configure(text=i.name)

                sorted_values = sorted(str)   
                self.start_option.configure(values = sorted_values,state="normal")
                self.end_option.configure(values = sorted_values,state="normal") 
                self.button_3.configure(state="normal",fg_color="red") 
        
                
         
    #run method
    def show(self): 
        if  self.startVar.get() == "" or self.endVar.get() == "" or self.startVar.get() == self.endVar.get(): 
            mixer.init()
            mixer.music.load("sound/warn.wav")
            mixer.music.play()
            CTkMessagebox(title="Warning",message="Please, Selete Start point and End Point!!",icon="info", option_1="Thanks")   
        else:
            self.textBox.configure(state="normal")
            self.textBox.delete("0.0", customtkinter.END) 
            self.res_label.configure(text="")
            
            self.dj.calculate_dijkstra(self.startVar.get(),self.endVar.get())
            dis = "{:.2f}".format(self.dj.distance)

            if dis == "0.00" and (self.startVar.get() != self.endVar.get()):
                 self.error_label.configure(text="No Edges \nBetween this Points!!!")
            else: 
                mixer.init()
                mixer.music.load("sound/car.wav")
                mixer.music.play()

                self.error_label.configure(text="")   
                self.textBox.insert("1.0",self.dj.short_path)
                self.textBox.configure(state="disabled")
                time = "{:.2f}".format(float(dis) / 30)
                self.res_label.configure(text=f" {dis} KM \n\n {time} Hour")

                self.lines.clear()
                self.set_icon_StartEnd()

                z=self.dj.short_path_vert[0]
                x1,y1=self.address_to_img(self.dj.vertic[z.name].x,self.dj.vertic[z.name].y)
                carline = Line(x1,y1)
                self.lines.append(carline)

                #draw a path
                for element in range(0,len(self.dj.short_path_vert)-1):
                    x=self.dj.short_path_vert[element]
                    x2=self.dj.short_path_vert[element+1]

                    x1_plan,y1_plan=self.address_to_img(self.dj.vertic[x.name].x,self.dj.vertic[x.name].y)
                    x2_plan,y2_plan=self.address_to_img(self.dj.vertic[x2.name].x,self.dj.vertic[x2.name].y)
                    
                    carline2 = Line(x2_plan,y2_plan)
                    self.lines.append(carline2)
                    
                    line =self.canvas.create_line(x1_plan+18,y1_plan+12,x2_plan+18,y2_plan+12, fill="#a84877",width=5)
                    self.path_list.append(line)
                    
                #car animation
                for i in range(0,len(self.lines)-1): 
                    self.move_car_along_line(self.lines[i].x,self.lines[i].y+5,self.lines[i+1].x,self.lines[i+1].y+5)
                    self.canvas.delete(self.car)  


    # move a car 
    def move_car_along_line(self, x1, y1, x2, y2):
        
        self.carIMG = Image.open("image/car.png").resize((45, 45))
        m = (y2 - y1) / (x2 - x1)
        b = y1 - m * x1
        
        if int(x1) > int(x2):
            self.carIMG = Image.open("image/car.png").resize((45, 45))
            self.car_image = ImageTk.PhotoImage(self.carIMG)
            self.car = self.canvas.create_image(x1-10,y1-15, anchor=tk.NW, image=self.car_image)
            for i in range(int(x1), int(x2), -4):
                v = m * i + b
                self.canvas.coords(self.car, i, v - 10)
                self.canvas.update()
        else :  
             self.carIMG= self.carIMG.rotate(180) 
             self.car_image=ImageTk.PhotoImage(self.carIMG)
             self.car = self.canvas.create_image(x1-10,y1-15, anchor=tk.NW, image=self.car_image)
             for i in range(int(x1), int(x2), 4):
                v = m * i + b
                self.canvas.coords(self.car, i, v - 10)
                self.canvas.update()
                     
    #clear all maker and data 
    def clear(self):
        
        if self.startVar.get() != "" and self.endVar.get() != "" :
            self.return_icon()    
        
        self.startVar.set("")
        self.endVar.set("")

        self.textBox.configure(state="normal")
        self.textBox.delete("0.0", customtkinter.END) 
        self.textBox.configure(state="disabled")

        self.res_label.configure(text="")

        # self.labelStart.destroy()
        # self.labelEnd.destroy()
        self.labelE.destroy()
        self.labelS.destroy()
        
        for path in self.path_list:
            self.canvas.delete(path)
        

    #change icon For start and end point
    def set_icon_StartEnd(self):
        x=0
        for item in self.marker_list:
            if item.name == self.startVar.get(): break
            x+=1
        y=0
        for item2 in self.marker_list:
            if item2.name == self.endVar.get(): break
            y+=1    
            
        self.canvas.delete(self.marker_list[x].m)   
        self.canvas.delete(self.marker_list[y].m)   
        self.marker_list[x].m = self.canvas.create_image(self.marker_list[x].x+10, self.marker_list[x].y-10, anchor=tk.NW, image=self.start_image)
        self.marker_list[y].m = self.canvas.create_image(self.marker_list[y].x, self.marker_list[y].y, anchor=tk.NW, image=self.end_image) 

        #Return to orignal icon
    def return_icon(self):
            x=0
            for item in self.marker_list:
                if item.name == self.startVar.get(): break
                x+=1
            y=0
            for item2 in self.marker_list:
                if item2.name == self.endVar.get(): break
                y+=1    
                
            self.canvas.delete(self.marker_list[x].m)   
            self.canvas.delete(self.marker_list[y].m)   
            self.marker_list[x].m = self.canvas.create_image(self.marker_list[x].x, self.marker_list[x].y, anchor=tk.NW, image=self.mark_image)
            self.marker_list[y].m = self.canvas.create_image(self.marker_list[y].x, self.marker_list[y].y, anchor=tk.NW, image=self.mark_image)

            self.canvas.tag_bind(self.marker_list[x].m , '<Enter>', lambda event: self.on_enter(self.marker_list[x].name,self.marker_list[x].x,self.marker_list[x].y))
            self.canvas.tag_bind(self.marker_list[x].m , '<Button-1>', lambda event: self.getMarker(self.marker_list[x].name))
            self.canvas.tag_bind(self.marker_list[x].m , '<Leave>', lambda event: self.on_leave(self.marker_list[y].name))
            
            self.canvas.tag_bind(self.marker_list[y].m, '<Enter>', lambda event: self.on_enter(self.marker_list[y].name,self.marker_list[y].x,self.marker_list[y].y))
            self.canvas.tag_bind(self.marker_list[y].m, '<Button-1>', lambda event: self.getMarker(self.marker_list[y].name)) 
            self.canvas.tag_bind(self.marker_list[y].m , '<Leave>', lambda event: self.on_leave(self.marker_list[y].name))
            
    #when touch the marker
    def on_enter(self,name,x,y):
        self.label = customtkinter.CTkLabel(self.canvas, text_color="Red",bg_color="White",font=('Helvetica', 14, 'bold'))
        self.label.place(x=x+20,y=y-40)
        self.label.configure(text=name)

    def on_leave(self,name):
        self.label.destroy()

        
    #when press on ther marher, vertices    
    def getMarker(self,name):
        mixer.init()
        mixer.music.load("sound/buttonclick.wav")
        mixer.music.play()
        if not self.startVar.get() :
            self.startVar.set(name)
            self.on_selectStrat(name)
        elif not self.endVar.get(): 
            self.endVar.set(name)  
            self.on_selectEnd(name)
        else:  
            msg =CTkMessagebox(title="Warning",message="Start Point and End Point is Selected!!",icon="check", option_2="Thanks",option_1="Clear",corner_radius=15,fade_in_duration=10,sound=bool)
            if msg.get()=="Clear":self.clear()    


    #create vertices on map
    def create_vertices(self, name,x,y):
    
        x_cor , y_cor = self.address_to_img(x,y)

        mark = self.canvas.create_image(x_cor, y_cor, anchor=tk.NW, image=self.mark_image)
        self.marker_list.append(Marks(mark,name,x_cor,y_cor))

        # self.canvas.tag_bind(mark, '<Enter>', lambda event: self.on_enter(name,x_cor,y_cor))
        self.canvas.tag_bind(mark, '<Button-1>', lambda event: self.getMarker(name))
        # self.canvas.tag_bind(mark, '<Leave>', lambda event: self.on_leave(name))
        

    #convert longtude lountude to x,y on canvas
    def address_to_img(self,x,y):        

        minlau=34.11494246966773
        maxlau=34.7597971259985

        minlon=31.208148396914798
        maxlon=31.588119491315728

        WyMax=750
        WxMax=1020
     
        q= WxMax/(maxlau-minlau)
        vr=y-minlau
        x_cor=vr*q

        q1= WyMax/(maxlon-minlon)
        vr1=maxlon-x
        y_cor=vr1*q1

        return x_cor,y_cor

    #dispaly a selected item
    def on_selectStrat(self,name):
        self.labelS.destroy()
        self.labelS = customtkinter.CTkLabel(self.canvas, text_color="Red",bg_color="White",font=('Helvetica', 14, 'bold'))

        x=0
        for item in self.marker_list:
            if item.name == self.startVar.get(): break
            x+=1
        
        self.labelS.place(x=self.marker_list[x].x+20,y=self.marker_list[x].y-40)
        self.labelS.configure(text=self.startVar.get())  

    #dispaly a selected item
    def on_selectEnd(self,name):
        self.labelE.destroy()
        self.labelE = customtkinter.CTkLabel(self.canvas, text_color="Red",bg_color="White",font=('Helvetica', 14, 'bold'))

        y=0
        for item2 in self.marker_list:
            if item2.name == self.endVar.get(): break
            y+=1    
    
        self.labelE.place(x=self.marker_list[y].x+20,y=self.marker_list[y].y-40)
        self.labelE.configure(text=self.endVar.get())         

if __name__ == "__main__":
    app = App()
    app.mainloop()