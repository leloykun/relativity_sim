import thorpy, test2
#import thorpy and game file

#function to set Properties
def setProperties(simButton):
    simButton.set_main_color((255,255,255))
    simButton.set_font_color_hover((255, 0, 0))
    simButton.set_font_size(23)
    simButton.set_size((200,50))
    simButton.set_font('Calibri')
    
#launch the game
# you must have launch_game function

    
def launch_game1():
    test2.env = test2.Environment(sim_type='train_frame', light_type='einstein')
    if __name__ == '__main__':
        test2.env.run()
        
def launch_game2():
    test2.env = test2.Environment(sim_type='train_frame', light_type='gallilean')
    if __name__ == '__main__':
        test2.env.run()




###
application = thorpy.Application(size=(700, 600), caption="Relativity Simulation")    

#make buttons
simButton1 = thorpy.make_button("Einstein", func = launch_game1)
simButton2 = thorpy.make_button("Galilean", func = launch_game2)

                         
#set button properties
setProperties(simButton2)
setProperties(simButton1)

#separate properties for quitButton
quitButton = thorpy.make_button("Quit", func=thorpy.functions.quit_menu_func)
quitButton.set_main_color((255,255,255))
quitButton.set_font_color_hover((255, 0, 0))
quitButton.set_font_size(23)
quitButton.set_size((200,50))
quitButton.set_font('Calibri')

# add help/descriptions
"""
thorpy.makeup.add_basic_help(simButton1,"insert description here")
thorpy.makeup.add_basic_help(simButton2,"insert description here")
"""


#set button text
simButton1.set_text("  Einsteinian ")
simButton2.set_text("  Galilean")
quitButton.set_text("  Exit  ")


#put buttons in box
Elem = [simButton1, simButton2, quitButton]
central_box = thorpy.Box.make(elements = Elem)
central_box.fit_children(margins=(40,40))
central_box.center()

#central_box.add_lift()  #this adds scroll bar
central_box.set_main_color((220, 220, 220, 180))

#make title
title_element = thorpy.make_text("Relativity Simulation\n", 55, (0,0,0))
title_element.set_font('Jokerman')
title_element.center()
            
#set background
background = thorpy.Background.make(color=(200, 200, 255),
                                    elements=[title_element, central_box])
thorpy.store(background)

#menu event handling
menu = thorpy.Menu(background) 
menu.play()

application.quit()
