def main_menu(self):

    text1 = font2.render("Placeholder", 1, (255,255,255), (0,0,0))
    text2 = font2.render("Press Button to Start", 1, (255,255,255), (0,0,0))

    while(True):
        #check for inputs
        self.check_events()

        self.window.fill((0,0,255))

        #print main menu text
        self.window.blit(text1, (self.window.get_width()/2 - text1.get_width()/2, 15))
        self.window.blut(text2, (self.window.get_width()/2 - text2.get_width()/2, 50))

        #leave the main menu screen one left mouse is clicked
        if self.input_map['left_click'] == True:
            self.screen = "game"

        
        

        
