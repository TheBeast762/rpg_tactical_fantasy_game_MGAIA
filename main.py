N_LEVELS = {0.0: 1, 0.25: 2, 0.55: 3, 0.7: 4}

def show_fps(win, inner_clock, font):
    fps_text = font.render("FPS: " + str(round(inner_clock.get_fps())), True, (255, 255, 0))
    win.blit(fps_text, (2, 2))

if __name__ == "__main__":
    import os
    import sys
    import json
    import time
    from src.constants import *
    from pygame import mixer
    from src.gui import constantSprites, fonts
    from src.game_entities.movable import Movable
    from src.game_entities.character import Character
    from src.scenes.startScreen import StartScreen
    from src.scenes.level import LevelStatus
    from src.services import loadFromXMLManager as Loader
    pg.init()
    experiment = False
    monitor = False
    if len(sys.argv) > 2:
        if sys.argv[1] == '-experiment':
            experiment = True
            iterations = 0
            try:
                iterations = int(sys.argv[2])
            except:
                print("Input the amount of iterations as a parameter after -experiment!")
                exit()
            if len(sys.argv) > 3:
                if sys.argv[3] == '-monitor':
                    monitor = True
    # Load fonts
    fonts.init_fonts()

    # Window parameters
    pg.display.set_caption("Tactical RPG Game")
    screen = pg.display.set_mode((MAIN_WIN_WIDTH, MAIN_WIN_HEIGHT))
    # Load constant sprites
    Movable.init_constant_sprites()
    constantSprites.init_constant_sprites()

    # Load some data
    races = Loader.load_races()
    classes = Loader.load_classes()
    Character.init_data(races, classes)

    clock = pg.time.Clock()

    #mixer.music.load(os.path.join('sound_fx', 'sndtrk.ogg'))
    #mixer.music.play(-1)
    nLevels = 0
    maxDuration = 100
    if experiment:
        result_dict = {}
        for diff in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]:
            win_ratio = []
            avgDist = []
            heroStats = []
            foeStats = []
            for difficulty in N_LEVELS.keys():
                if diff >= difficulty:
                    nLevels = N_LEVELS[difficulty]
            it = 0
            while it < iterations:
                print("_______________")
                print("GAME diff:",diff, " iteration:",it)
                StartScreen.modify_options_file('difficulty', diff)
                start_screen = StartScreen(screen, nLevels, experimentGame=experiment)
                start_screen.new_game()
                t_end = time.time() + maxDuration#seconds to play
                avgDist.append(start_screen.level.getMeanDistToFoes())
                heroStats.append(start_screen.level.getStats('allies'))
                foeStats.append(start_screen.level.getStats('foes'))
                levels_completed = 0
                defeated = False
                timeout = False
                while levels_completed < nLevels and not defeated:
                    for e in pg.event.get():
                        if e.type == pg.QUIT:
                            quit_game = True
                        elif e.type == pg.MOUSEMOTION:
                            start_screen.motion(e.pos)
                        elif e.type == pg.MOUSEBUTTONUP:
                            if e.button == 1 or e.button == 3:
                                quit_game = start_screen.click(e.button, e.pos)
                        elif e.type == pg.MOUSEBUTTONDOWN:
                            if e.button == 1 or e.button == 3:
                                start_screen.button_down(e.button, e.pos)
                    start_screen.update_state()
                    if monitor:
                        start_screen.display()
                        show_fps(screen, clock, fonts.fonts['FPS_FONT'])
                        pg.display.update()
                        clock.tick(60)
                    if start_screen.level.game_phase == LevelStatus.ENDED_VICTORY or start_screen.level.game_phase == LevelStatus.ENDED_DEFEAT or time.time() > t_end:
                        if start_screen.level.game_phase == LevelStatus.ENDED_VICTORY:
                            levels_completed += 1
                            if levels_completed < nLevels:
                                start_screen.play(level=StartScreen.load_level(level=levels_completed,team=start_screen.level.passed_players + start_screen.level.players, experiment=experiment))
                                t_end = time.time() + maxDuration#seconds to play
                                avgDist.append(start_screen.level.getMeanDistToFoes())
                                heroStats.append(start_screen.level.getStats('allies'))
                                foeStats.append(start_screen.level.getStats('foes'))
                            else:
                                print("Protagonist party won all ", nLevels, " levels!")
                        elif time.time() > t_end:
                            #restart game
                            print("Timeout of level, restarting...")
                            it -= 1
                            avgDist.pop()
                            heroStats.pop()
                            foeStats.pop()
                            timeout = True
                            break
                        else:
                            print("Protagonist party was defeated...")
                            defeated = True
                if not timeout:
                    win_ratio.append(levels_completed/nLevels)
                it += 1
            result_dict[diff] = {'AvgWinRatio': sum(win_ratio)/len(win_ratio), 'AvgDistFoes': sum(avgDist)/len(avgDist), 'AvgHeroStats': sum(heroStats)/len(heroStats), 'AvgFoeStats': sum(foeStats)/len(foeStats)}
        with open('results.json', 'w') as outputFile:
            json.dump(result_dict, outputFile)
    else:
        diff = Loader.get_difficulty()
        for difficulty in N_LEVELS.keys():
                if diff >= difficulty:
                    nLevels = N_LEVELS[difficulty]
        start_screen = StartScreen(screen, nLevels)
        quit_game = False
        while not quit_game:
            for e in pg.event.get():
                if e.type == pg.QUIT:
                    quit_game = True
                elif e.type == pg.MOUSEMOTION:
                    start_screen.motion(e.pos)
                elif e.type == pg.MOUSEBUTTONUP:
                    if e.button == 1 or e.button == 3:
                        quit_game = start_screen.click(e.button, e.pos)
                elif e.type == pg.MOUSEBUTTONDOWN:
                    if e.button == 1 or e.button == 3:
                        start_screen.button_down(e.button, e.pos)
            start_screen.update_state()
            start_screen.display()
            show_fps(screen, clock, fonts.fonts['FPS_FONT'])
            pg.display.update()
            clock.tick(60)
    raise SystemExit
