import pygame, sys, engine, interface

# Initializes pygame module
pygame.init()

# Sets up game screen with specifice screen resolution (800 x 600)
game_screen = pygame.display.set_mode(interface.SCREEN_RESOLUTION)

# Changes the default window caption to the title of the game, ICA$H
pygame.display.set_caption(interface.GAME_TITLE)

# Initializes a Clock object used in tracking time
clock = pygame.time.Clock()

# State of the game that dictates the flow and is saved to/loaded from an external file
game_state = engine.create_or_load_save_file()

# Source: https://www.reddit.com/r/pygame/comments/7lh9fq/what_are_the_ways_to_create_a_timer/
# Timer set-up variables
passed_time = 0
timer_started = False

# Game loop end condition
game_has_ended = False

# Game Loop
while not game_has_ended:
    game_screen.fill(interface.BLACK)

    # Event Handling and State Management
    ## Each event changes the game_state which either gets reset or saved to an external file

    ## Goes through the event queue one by one
    for event in pygame.event.get():
        ### For when the player tries to close the window
        if event.type == pygame.QUIT:
            if game_state["scene"] == interface.PLAY:
                game_state["scene"] = interface.SAVE
            else:
                ##### Reset game state and write to file
                engine.save_to_file(engine.SAVE_STATE)
                game_has_ended = True
        
        ### For when the player clicks with the mouse
        elif event.type == pygame.MOUSEBUTTONUP:
            #### For when the player clicks the start button
            if game_state["scene"] == interface.START:
                if interface.START_BTN.is_colliding(event.pos):
                    game_state["scene"] = interface.MODES

            #### For when the player chooses one of the game modes
            elif game_state["scene"] == interface.MODES:
                if interface.RND_WRDS_BTN.is_colliding(event.pos):
                    game_state["mode"] = interface.RANDOM_WORDS
                    game_state["scene"] = interface.SET_TIMER
                elif interface.ANAGRAMS_BTN.is_colliding(event.pos):
                    game_state["mode"] = interface.ANAGRAMS
                    game_state["scene"] = interface.SET_TIMER

            #### For when the player sets the time duration, if any
            elif game_state["scene"] == interface.SET_TIMER:
                if interface.SET_TIMER_SELECT.is_colliding(event.pos):
                    interface.SET_TIMER_SELECT.change_text()

            #### For when the player is at the GAME OVER screen and wants to exit out of the game
            elif game_state["scene"] == interface.GAME_OVER:
                game_has_ended = True

            #### For when the player chooses to save the current game state or reset it, exiting
            #### out of the game in the process
            elif game_state["scene"] == interface.SAVE:
                if interface.YES_BTN.is_colliding(event.pos):
                    engine.save_to_file(game_state)
                elif interface.NO_BTN.is_colliding(event.pos):
                    engine.save_to_file(engine.SAVE_STATE)
                game_has_ended = True
        
        ### For when the player presses a keyboard key
        elif event.type == pygame.KEYUP:
            #### For when the player confirms the time duration of the run by hitting Enter
            if game_state["scene"] == interface.SET_TIMER:
                if event.key == pygame.K_RETURN:
                    set_timer_txt = interface.SET_TIMER_SELECT.text
                    ##### Setting up for timer
                    if set_timer_txt == "NO TIME":
                        game_state["with_timer"] = False
                    else:
                        game_state["with_timer"] = True
                        game_state["time_left"] = 60*int(interface.SET_TIMER_SELECT.text[:2])
                    ##### Setting up for PLAY SCENE
                    if game_state["mode"] == interface.RANDOM_WORDS:
                        game_state["char_seq"] = engine.combine_words(engine.pick_set_of_words())
                        game_state["valid_words"] = engine.get_valid_words_from_seq(game_state["char_seq"])
                    elif game_state["mode"] == interface.ANAGRAMS:
                        game_state["char_seq"] = engine.pick_word(game_state)
                        game_state["valid_words"] = engine.get_anagrams_for_word(game_state["char_seq"])
                    game_state["scene"] = interface.PLAY

            #### For player input
            elif game_state["scene"] == interface.PLAY:
                ##### Checks whether key pressed was a character key
                char = pygame.key.name(event.key).lower()
                if char in interface.ALPHABET:
                    interface.PLAYER_INPUT.add_input(char)
                ##### Removes last character inputted by player
                elif char == "backspace":
                    interface.PLAYER_INPUT.backspace()
                ##### Confirms input and score is calculated if valid
                elif char == "return":
                    input_txt = interface.PLAYER_INPUT.text
                    ###### Checks if word is valid; if not, decrement no. of retries
                    if input_txt in game_state["valid_words"]:
                        game_state["score"] += engine.get_score_equivalent_of_word(input_txt)
                        game_state["valid_words"].remove(input_txt)
                        game_state["used_words"].append(input_txt)
                        if game_state["valid_words"] == []:
                            if game_state["mode"] == interface.RANDOM_WORDS:
                                game_state["char_seq"] = engine.combine_words(engine.pick_set_of_words())
                                game_state["valid_words"] = engine.get_valid_words_from_seq(game_state["char_seq"])
                            else:
                                game_state["char_seq"] = engine.pick_word(game_state)
                                game_state["valid_words"] = engine.get_anagrams_for_word(game_state["char_seq"])
                    else:
                        game_state["retries"] -= 1
                    interface.PLAYER_INPUT.reset_input()
                    ###### Checks to see if no. of retries has reached zero; if so, GAME OVER screen is shown
                    if not game_state["retries"]:
                        game_state["scene"] = interface.GAME_OVER
                        
            #### Start a new game
            elif game_state["scene"] == interface.GAME_OVER:
                if event.key == pygame.K_n:
                    game_state["scene"] = interface.MODES

    # Game Scenes and Layouts
    
    ## START SCENE (shows the starting screen of the game)
    if game_state["scene"] == interface.START:
        game_screen.blit(interface.TITLE.printable(), interface.TITLE.get_coordinates())
        interface.START_BTN.hover = interface.START_BTN.is_colliding(pygame.mouse.get_pos())
        start_btn_pos = interface.START_BTN.get_coordinates()
        game_screen.blit(interface.START_BTN.printable(), start_btn_pos)
    
    ## MODES SCENE (players can pick which game mode they want to play in this scene)
    elif game_state["scene"] == interface.MODES:
        ### Help text for the scene
        game_screen.blit(interface.MODES_HELP.printable(), interface.MODES_HELP.get_coordinates())
        
        ### Visual aesthetic used in separating the game modes
        game_screen.blit(interface.DIVIDER.printable(), interface.DIVIDER.get_coordinates())

        ### Display buttons (with hover states) for each game mode
        interface.RND_WRDS_BTN.hover = interface.RND_WRDS_BTN.is_colliding(pygame.mouse.get_pos())
        interface.ANAGRAMS_BTN.hover = interface.ANAGRAMS_BTN.is_colliding(pygame.mouse.get_pos())
        rnd_words_btn_pos = interface.RND_WRDS_BTN.get_coordinates()
        anagrams_btn_pos = interface.ANAGRAMS_BTN.get_coordinates()
        game_screen.blit(interface.RND_WRDS_BTN.printable(), rnd_words_btn_pos)
        game_screen.blit(interface.ANAGRAMS_BTN.printable(), anagrams_btn_pos)
    
    ## SET TIMER SCENE (players specify whether they want a timer or not when playing)
    elif game_state["scene"] == interface.SET_TIMER:
        ### Help text 1
        game_screen.blit(interface.SET_TIMER_HELP_1.printable(), interface.SET_TIMER_HELP_1.get_coordinates())

        ### Select object used for specifying the time duration, if any
        interface.SET_TIMER_SELECT.hover = interface.SET_TIMER_SELECT.is_colliding(pygame.mouse.get_pos())
        set_timer_select_pos = interface.SET_TIMER_SELECT.get_coordinates()
        game_screen.blit(interface.SET_TIMER_SELECT.printable(), set_timer_select_pos)

        ### Help text 2
        game_screen.blit(interface.SET_TIMER_HELP_2.printable(), interface.SET_TIMER_HELP_2.get_coordinates())
    
    ## PLAY SCENE (gameplay is shown here, depending on the mode the players selected earlier)
    elif game_state["scene"] == interface.PLAY:
        ### A timer object is revealed if the player set a time duration for the run
        if game_state["with_timer"]:
            interface.display_time(engine.get_time(game_state["time_left"]), game_screen)
            if not timer_started:
                timer_started = not timer_started
                start_time = pygame.time.get_ticks()
            #### Checks to see if a second has passed
            if pygame.time.get_ticks() - start_time >= 1000:
                game_state["time_left"] -= 1
                ##### Update time display
                interface.display_time(engine.get_time(game_state["time_left"]), game_screen)
                start_time = pygame.time.get_ticks()
                ##### Changes scene when time is up
                if not game_state["time_left"]:
                    game_state["scene"] = interface.GAME_OVER

        ### Either a word or sequence of characters is shown here, depending on the chosen mode
        interface.display_char_seq(game_state["char_seq"], game_screen)

        ### Player input object
        game_screen.blit(interface.PLAYER_INPUT.printable(), interface.PLAYER_INPUT.get_coordinates(interface.INPUT_OFFSET))

        ### Score display
        interface.display_score(game_state["score"], game_screen)

        ### Retries display (Max. of 3 retries, shown as NX, N being the no. of retries)
        interface.display_retries(game_state["retries"], game_screen)

    ## GAME OVER SCENE (shows the final score/amount of money bagged by the player; can opt to play another game or just exit out)
    elif game_state["scene"] == interface.GAME_OVER:
        ### Help text for starting a new game (press n)
        game_screen.blit(interface.NEW_GAME.printable(), interface.NEW_GAME.get_coordinates())

        ### Display for the GAME OVER text
        game_screen.blit(interface.GAME_OVER_DISPLAY.printable(), interface.GAME_OVER_DISPLAY.get_coordinates())

        ### Final score display
        interface.display_final_score(game_state["score"], game_screen)

        ### Help text for exiting out of the game (click anywhere)
        game_screen.blit(interface.EXIT_GAME.printable(), interface.EXIT_GAME.get_coordinates())

    ## SAVE SCENE (only available if the user exits out of the program during the PLAY SCENE; otherwise, game state is reset)
    elif game_state["scene"] == interface.SAVE:
        ## Display for "SAVE STATE?"
        game_screen.blit(interface.SAVE_STATE.printable(), interface.SAVE_STATE.get_coordinates())

        ## Yes and no buttons (both have hover state management)
        interface.YES_BTN.hover = interface.YES_BTN.is_colliding(pygame.mouse.get_pos())
        interface.NO_BTN.hover = interface.NO_BTN.is_colliding(pygame.mouse.get_pos())
        yes_btn_pos = interface.YES_BTN.get_coordinates()
        no_btn_pos = interface.NO_BTN.get_coordinates()
        game_screen.blit(interface.YES_BTN.printable(), yes_btn_pos)
        game_screen.blit(interface.NO_BTN.printable(), no_btn_pos)

    # Updates game screen every iteration
    pygame.display.update()

    # Updates game clock every iteration
    clock.tick(30)

# Closes pygame module
pygame.quit()
