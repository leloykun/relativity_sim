from environment import Environment
import thorpy


class Menu:
    '''
        Temujin, if you're reading this, forget about the plan I told you last time,
        kahit anong improvements gawin mo, ok la
        just make sure na:
            1) some random person would know what to do
                -> so parang like may text somewhere (bis la gamit hin make_text())
                   na nag-eexplain what to do
            2) kailangan may way na macontrol han user an speed han train
                like gamit hin inserter or smth
        
        check these out:
            http://www.thorpy.org/tutorials/minigame.html
            http://www.thorpy.org/documentation/userguide/cheatsheet.html#elements
            http://www.thorpy.org/tutorials/minigame.html
    '''
    def_text_color = (200, 200, 200)
    hover_text_color = ()
    
    def run(self):
        ###
        application = thorpy.Application(size=(640, 640), caption="Relativity Simulation")    
        
        reference_frames = ['train', 'ground']
        has_time_dims    = ['False', 'True']
        transformations  = ['lorentz', 'galilean']
        
        buttons = []
        for transformation in transformations:
            for has_time_dim in has_time_dims:
                for reference_frame in reference_frames:
                    buttons.append(thorpy.make_button(reference_frame + '-' + has_time_dim + '-' + transformation, 
                                                      func=self.sim, 
                                                      params={'reference_frame':reference_frame , 'has_time_dim':has_time_dim, 'transformation':transformation}))
        
        label1 = thorpy.Draggable.make("Einsteinian")
        label2 = thorpy.Draggable.make("Galilean")

        
        self.setProperties(label1)
        self.setProperties(label2)
        for button in buttons:
            self.setProp2(button)
            
        '''
        #set button properties
        self.setProp2(simButton1)
        self.setProp2(simButton2)
        self.setProp2(simButton3)
        self.setProp2(simButton4)
        self.setProp2(simButton5)
        self.setProp2(simButton6)
        self.setProp2(simButton7)
        self.setProp2(simButton8)
        '''

        #separate properties for quitButton
        quitButton = thorpy.make_button("Exit", func=thorpy.functions.quit_menu_func)
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

        #put buttons in box
        Elem = [label1] + buttons[0:4] + [label2] + buttons[4:8] + [quitButton]
        central_box = thorpy.Box.make(elements = Elem)
        central_box.fit_children(margins=(20,20))
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

    ####
    
    def setProperties(self, simButton):
        simButton.set_main_color((255,255,255))
        simButton.set_font_color_hover((255, 0, 0))
        simButton.set_font_size(23)
        simButton.set_size((200,50))
        simButton.set_font('Calibri')

    def setProp2(sefl, simButton):
        simButton.set_main_color((255,200,255))
        simButton.set_font_color_hover((255,0,0))
        simButton.set_font_size(15)
        simButton.set_size((150,25))
        simButton.set_font('Calibri')
    
    def sim(self, reference_frame, has_time_dim, transformation):
        print(reference_frame, bool(has_time_dim), transformation)
        env = Environment(self, reference_frame=reference_frame, has_time_dim=bool(has_time_dim), transformation=transformation, switchable=True)
        env.run()

        
if __name__ == '__main__':
    '''
    env = Environment(menu=None, reference_frame='ground', has_time_dim=False, transformation='galilean', switchable=True)
    env.run()
    '''
    my_menu = Menu()
    my_menu.run()