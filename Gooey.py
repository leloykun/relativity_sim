import thorpy, test2

def setProperties(simButton):
    simButton.set_main_color((255,255,255))
    simButton.set_font_color_hover((255, 0, 0))
    simButton.set_font_size(23)
    simButton.set_size((200,50))
    simButton.set_font('Calibri')

def setProp2(simButton):
    simButton.set_main_color((255,200,255))
    simButton.set_font_color_hover((255,0,0))
    simButton.set_font_size(15)
    simButton.set_size((150,25))
    simButton.set_font('Calibri')

    
####
    
def launch_game1():
    test2.env = test2.Environment(sim_type='train_frame', light_type='einstein')
    if __name__ == '__main__':
        test2.env.run()





###
application = thorpy.Application(size=(700, 700), caption="Relativity Simulation")    

#make buttons
simButton1 = thorpy.make_button("Einstein1", func = launch_game1)
simButton2 = thorpy.make_button("Einstein2", func = launch_game1)
simButton3 = thorpy.make_button("Einstein3", func = launch_game1)
simButton4 = thorpy.make_button("Einstein4", func = launch_game1)
simButton5 = thorpy.make_button("Galileo1 ", func = launch_game1)
simButton6 = thorpy.make_button("Galileo2 ", func = launch_game1)
simButton7 = thorpy.make_button("Galileo3 ", func = launch_game1)
simButton8 = thorpy.make_button("Galileo4 ", func = launch_game1)

label1 = thorpy.Draggable.make("Einsteinian")
label2 = thorpy.Draggable.make("Galilean")

                         
#set button properties
setProperties(label1)
setProperties(label2)
setProp2(simButton1)
setProp2(simButton2)
setProp2(simButton3)
setProp2(simButton4)
setProp2(simButton5)
setProp2(simButton6)
setProp2(simButton7)
setProp2(simButton8
         )


#separate properties for quitButton
quitButton = thorpy.make_button("Quit", func=thorpy.functions.quit_menu_func)
quitButton.set_main_color((255,255,255))
quitButton.set_font_color_hover((255, 0, 0))
quitButton.set_font_size(15)
quitButton.set_size((200,50))
quitButton.set_font('Calibri')

# add help/descriptions
"""
thorpy.makeup.add_basic_help(simButton1,"insert description here")
thorpy.makeup.add_basic_help(simButton2,"insert description here")
"""


#set button text
simButton1.set_text("  1  ")
simButton2.set_text("  2  ")
simButton3.set_text("  3  ")
simButton4.set_text("  4  ")
simButton5.set_text("  5  ")
simButton6.set_text("  6  ")
simButton7.set_text("  7  ")
simButton8.set_text("  8  ")

quitButton.set_text("  Exit  ")


#put buttons in box
Elem = [label1, simButton1,simButton2, simButton3, simButton4, label2,  simButton5, simButton6,
        simButton7, simButton8, quitButton]
central_box = thorpy.Box.make(elements = Elem)
central_box.fit_children(margins=(40,40))
central_box.center()

#central_box.add_lift()  #this adds scroll bar
central_box.set_main_color((220, 220, 220, 180))

#make title
title_element = thorpy.make_text("Relativity Simulation\n", 55, (0,0,0))
title_element.set_font('Comic_Sans')
title_element.center()
            
#set background
background = thorpy.Background.make(color=(200, 200, 255),
                                    elements=[title_element, central_box])
thorpy.store(background)

#menu event handling
menu = thorpy.Menu(background) 
menu.play()

application.quit()
