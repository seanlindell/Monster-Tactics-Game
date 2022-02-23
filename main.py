from game import Game

g = Game()

while g.running:
    g.clock.tick(30)
    g.curr_menu.display_menu()
    g.opening()
    g.game_loop()