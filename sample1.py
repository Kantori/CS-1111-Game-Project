# Andrew Walsh, abw9yd, CS 1111, Fall 2016
import pygame
import gamebox
import random
screen_width = 1000
screen_length = 600
camera = gamebox.Camera(screen_width, screen_length)
counter_space = 0
counter_coins = 0
counter_enemy = 0
counter_side = 0
counter_air = 0
life = 500
heal = 0
# Keeps character facing the same directions
orientation = 'R'
sheet = gamebox.load_sprite_sheet('images2.png', 5, 8)
enemy_sheet = gamebox.load_sprite_sheet('flameskull.png', 4, 3)
coin_sheet = gamebox.load_sprite_sheet('coins.png', 4, 8)
arrow_sheet = gamebox.load_sprite_sheet('play_arrow.png', 2, 1)
inst_button_sheet = gamebox.load_sprite_sheet('inst_button.png', 2, 1)

character = gamebox.from_image(screen_width/2, screen_length/2, sheet[counter_space])
enemies = [gamebox.from_image(random.randint(10, 990), 30, enemy_sheet[counter_enemy])]
kills = 0

character_speed = 0
coins = []
coin_timer = []
coins_towards_reload_increase = 0
score = 0
difficulty_increasing = 0

enemy_explosions = []
explosion_length = []
bullets_r = []
bullets_l = []
shot_direction = 5

reload_time = 60
enemy_spawn_rate = (60)*7

run_skulls = False
run_leaderboards = False
run_home = True
run_instructions = False

clicked_skulls = False
clicked_leaderboard = False
clicked_home = False
clicked_instructions = False

reload = 60
velocity = 0
tic_cnt = [0,0,0,0]


curr_pos = 556
falling = False

records_coins = []
waterfall_rotation = 0
falling_coin_rate = 0

# ####################################################################
loading_1 = [
    gamebox.from_text(120, 585, 'Andrew Walsh, abw9yd', 'Arial', 20, 'white', italic=True, bold=True),
    gamebox.from_text(880, 585, 'Kevin Naddoni, kn6vv', 'Arial', 20, 'white', italic=True, bold=True),
    gamebox.from_image(500, 460, 'trophy.png'),
    gamebox.from_image(500, 300, arrow_sheet[0]),
    gamebox.from_image(500, 150, inst_button_sheet[0])
]



# ####################################################################
def tick(keys):
    global bullets_l
    global bullets_r
    global character
    global character_speed
    global clicked_home
    global clicked_instructions
    global clicked_leaderboard
    global clicked_skulls
    global coin_sheet
    global coins_towards_reload_increase
    global counter_coins
    global counter_enemy
    global counter_space
    global counter_side
    global counter_air
    global curr_pos
    global difficulty_increasing
    global enemies
    global enemy_explosions
    global enemy_spawn_rate
    global explosion_length
    global falling
    global falling_coin_rate
    global heal
    global run_home
    global kills
    global life
    global line_read
    global loading_1
    global orientation
    global records_coins
    global reload
    global reload_time
    global run_home
    global run_instructions
    global run_leaderboards
    global run_skulls
    global tic_cnt
    global velocity
    global score
    global shot_direction
    global waterfall_rotation


    guidelines = [
        gamebox.from_color(100, 300, 'white', 1, 600),
        gamebox.from_color(200, 300, 'white', 1, 600),
        gamebox.from_color(300, 300, 'white', 1, 600),
        gamebox.from_color(400, 300, 'white', 1, 600),
        gamebox.from_color(500, 300, 'white', 1, 600),
        gamebox.from_color(600, 300, 'white', 1, 600),
        gamebox.from_color(700, 300, 'white', 1, 600),
        gamebox.from_color(800, 300, 'white', 1, 600),
        gamebox.from_color(900, 300, 'white', 1, 600),
        gamebox.from_color(500, 100, 'white', 1000, 1),
        gamebox.from_color(500, 200, 'white', 1000, 1),
        gamebox.from_color(500, 300, 'white', 1000, 1),
        gamebox.from_color(500, 400, 'white', 1000, 1),
        gamebox.from_color(500, 500, 'white', 1000, 1),
            ]

    score_rec_disp = open('scoreboard.txt', 'r')
    line_read = score_rec_disp.readline().split(',')
    score_rec_disp.close()
    for string_score in range(len(line_read)):
        line_read[string_score] = int(line_read[string_score])
    line_read = sorted(line_read)
    line_read.reverse()


    camera.draw(gamebox.from_image(500, 300, 'loading_bg.png'))

# clicked test
# #####################################################################
#sets up clicks
    # SHOWS LEADERBOARDS
    if 440 < camera.mousex < 560 and 380 < camera.mousey < 540 and camera.mouseclick and run_skulls is False and run_leaderboards is False:
        clicked_leaderboard = True
        clicked_home = False
        camera.clear('black')
    # PLAYS GAME
    if ((316 < camera.mousex < 622 and 267 < camera.mousey < 332) or (622 < camera.x < 685 and 235 < camera.y < 365)) and camera.mouseclick:
        clicked_skulls = True
        clicked_leaderboard = False
        clicked_home = False

    #changes lighting of play game arrow
    if (316 < camera.mousex < 622 and 267 < camera.mousey < 332) or (622 < camera.x < 685 and 235 < camera.y < 365):
        loading_1[3] = gamebox.from_image(500, 300, arrow_sheet[1])
    else:
        loading_1[3] = gamebox.from_image(500, 300, arrow_sheet[0])

    #changes lighting of instructions arrow
    if (316 < camera.mousex < 622 and 17 < camera.mousey < 182) or (622 < camera.x < 685 and 85 < camera.y < 185):
        loading_1[4] = gamebox.from_image(500, 150, inst_button_sheet[1])
    else:
        loading_1[4] = gamebox.from_image(500, 150, inst_button_sheet[0])

    # HOME BUTTON
    if (run_leaderboards or run_instructions) and run_skulls is False and (camera.mousex >= 936 and camera.mousey >= 536 and camera.mouseclick):
        clicked_home = True
        clicked_leaderboard = False
        clicked_instructions = False

    #sets up click for instructions
    if ((316 < camera.mousex < 622 and 17 < camera.mousey < 182) or (622 < camera.x < 685 and 235 < camera.y < 365)) and camera.mouseclick and run_skulls is False and run_instructions is False:
        clicked_instructions = True
        clicked_home = False


# #####################################################################
#uses clicks to set up runs
    if clicked_leaderboard:
        run_leaderboards = True
        run_home = False
    elif clicked_leaderboard is False:
        run_leaderboards = False

    if clicked_skulls:
        run_skulls = True

    if clicked_home:
        run_home = True
    elif clicked_home is False:
        run_home is False

    if clicked_instructions:
        run_instructions = True
        run_home = False
    elif clicked_instructions is False:
        run_instructions = False

#runs leaderboards based upon above
    if run_leaderboards:
        counter_coins += 1
        falling_coin_rate += 1
        if counter_coins == 2:
            waterfall_rotation += 1
            counter_coins = 0
        if waterfall_rotation == 28:
            waterfall_rotation = 0
        if falling_coin_rate == 5:
            falling_coin_rate = 0
            records_coins.append(gamebox.from_image(random.randint(15, 985), 15, coin_sheet[1 + waterfall_rotation]))
        for record_coin in records_coins:
            record_coin.y += 2
            record_coin = gamebox.from_image(record_coin.x, record_coin.y, coin_sheet[1 + waterfall_rotation])
            if record_coin.y > 610:
                del records_coins[0]
            camera.draw(record_coin)
        camera.draw(gamebox.from_image(968, 568, 'home_button.png'))
        camera.draw(gamebox.from_text(500, 50, 'HIGH SCORES', 'Arial', 100, 'gold', bold=True, italic=True))
        if len(line_read) < 5:
            top_five = len(line_read)
        else:
            top_five = 5

            for b in range(5, 10):
                sum_2 = 150 + 100*(b-5)
                camera.draw(gamebox.from_text(766, sum_2, str(line_read[b]), 'Arial', 100, 'white', bold=False))
                camera.draw(gamebox.from_text(623, sum_2, str(b+1)+ '.  ', 'Arial', 80, 'black'))

        for a in range(0, top_five):
            sum = 150 + 100*a
            if a < 3:
                camera.draw(gamebox.from_text(350, sum, str(line_read[a]), 'Arial', 100, 'gold', bold=True, italic=True))
                camera.draw(gamebox.from_text(220, sum, str(a+1) + '.  ', 'Arial', 80, 'red'))
            else:
                camera.draw(gamebox.from_text(333, sum, str(line_read[a]), 'Arial', 100, 'white', bold=False))
                camera.draw(gamebox.from_text(220, sum, str(a + 1) + '.  ', 'Arial', 80, 'black'))


#runs home based upon above
    if run_home:
        for parts in loading_1:
            camera.draw(parts)


    # for guides in guidelines:
    #     camera.draw(guides)

#runs instructions
    if run_instructions:
        #camera.clear('black')
        camera.draw(gamebox.from_image(968, 568, 'home_button.png'))
        camera.draw(gamebox.from_text(500, 100, 'Hello! This is __ created by Andrew Walsh and Kevin Naddoni. Objectives and controls are listed below.', 'Arial', 20, 'white', False, False))
        camera.draw(gamebox.from_text(500, 150, 'On the homepage, click on the Trophy to see the Top Scores!', 'Arial', 20, 'white'))
        camera.draw(gamebox.from_text(200, 200, 'Objectives:','Arial', 20, 'white', True, False))
        camera.draw(gamebox.from_text(500, 250, 'Collect as many coins as possible!','Arial', 20, 'white', False, False))
        camera.draw(gamebox.from_text(500, 300, 'Enemies will hurt you if you touch them. Shoot them down with your laser pistol!', 'Arial', 20, 'white', False, False))
        camera.draw(gamebox.from_text(500, 350, 'Play until you reach the top of the leaderboards!','Arial', 20, 'white', False, False))
        camera.draw(gamebox.from_text(200, 400, 'Controls:', 'Arial', 20, 'white', True, False))
        camera.draw(gamebox.from_text(500, 450, 'Use arrow keys (←,→,↓,↑) to travel the map', 'Arial', 20, 'white', False,False))
        camera.draw(gamebox.from_text(500, 500, 'Press the spacebar to shoot at enemies', 'Arial', 20, 'white', False, False))


# ############################################################################################################################
    if run_skulls:
        coin_sound = gamebox.load_sound('coin_sound.wav')
        gun_sound = gamebox.load_sound('gun_sound.wav')
        enemy_death_sound = gamebox.load_sound('enemy_death_sound.wav')
        game_over_sound = gamebox.load_sound('game_over.wav')
        for varb in range(len(tic_cnt)):
            tic_cnt[varb] += 1

        if pygame.K_p in keys:
            gamebox.pause()

        background = gamebox.from_image(500, 300, 'background_image.jpg')
        background.size = 1000, 700
        camera.draw(background)

    #                            x center//y center//colour//width//height
        walls = [gamebox.from_image(500, 595, 'platform_block.png'),
                 gamebox.from_image(75, 500, 'platform_block.png'),
                 gamebox.from_image(400, 380, 'platform_block.png'),
                 gamebox.from_image(290, 440, 'platform_block.png'),
                 gamebox.from_image(600, 398, 'platform_block.png'),
                 gamebox.from_image(900, 320, 'platform_block.png'),
                 gamebox.from_image(750, 540, 'platform_block.png'),
                 gamebox.from_image(160, 340, 'platform_block.png'),
                 gamebox.from_image(860, 480, 'platform_block.png'),
                 gamebox.from_image(765, 440, 'platform_block.png'),
                 gamebox.from_image(450, 500, 'platform_block.png'),
                 gamebox.from_image(30, 260, 'platform_block.png'),
                 gamebox.from_image(250, 150, 'platform_block.png'),
                 gamebox.from_image(450, 150, 'platform_block.png'),
                 gamebox.from_image(100, 205, 'platform_block.png'),
                 gamebox.from_image(650, 260, 'platform_block.png'),
                 gamebox.from_image(550, 205, 'platform_block.png'),
                 ]

        walls[0].size = 1000, 10
        walls[1].size = 200, 10
        walls[2].size = 50, 10
        walls[3].size = 50, 10
        walls[4].size = 200, 10
        walls[5].size = 250, 10
        walls[6].size = 160, 10
        walls[7].size = 200, 10
        walls[8].size = 50, 10
        walls[9].size = 50, 10
        walls[10].size = 180, 10
        walls[11].size = 60, 10
        walls[12].size = 130, 10
        walls[13].size = 130, 10
        walls[14].size = 20, 10
        walls[15].size = 100, 10
        walls[16].size = 20, 10
        sides = [
            gamebox.from_color(1, 300, 'black', 2, 600),
            gamebox.from_color(999, 300, 'black', 2, 600)
        ]

    #    Variables

        invincibility = False
        coin_life_span = (60)*6
        character_speed = 4
        enemy_speed = 2
        heal_power = 25
        jump_power = -15
        sprite_speed = 8
    # Number of seconds it takes for a new enemy to spawn
        coin_spawn_rate = (60)*5
    # ####### Increasing Difficulty #########################

        coins_to_hasten_reload = 8
        reload_reduction = 4
        coins_to_increase_enemy_spawn_rate = 6
        amount_spawn_rate_increases = 30
        coins_to_heal = 10

    # Sets the speed that the animation changes
        if tic_cnt[1] % sprite_speed == 0:
            tic_cnt[1] = 0
            counter_space += 1
            counter_side += 1
            counter_enemy += 1
            counter_coins += 1

        if counter_enemy == 3:
            counter_enemy = 0
        if counter_space == 6:
            counter_space = 0
        if counter_side == 5:
            counter_side = 0
        if counter_coins == 28:
            counter_coins = 0

    # Creates 'Gravity'
        velocity += 1
        character.y += velocity

    # **Sets boundaries of the screen

        if character.x > 1000:
            character.x = 1000
        if character.x < 0:
            character.x = 0
        if character.y < 30:
            character.y = 30
        if character.y > 590:
            character.y = 590

    # Test for falling
        if curr_pos != character.y:
            falling = True
        else:
            falling = False
        curr_pos = character.y

    # Create Enemies

        tic_cnt[2] += 1
        if tic_cnt[2] >= enemy_spawn_rate:
            enemies.append(gamebox.from_image(random.randint(10, 990), 30, enemy_sheet[counter_enemy]))
            tic_cnt[2] = 0

    # ############################ SHOOTING ###########################################################

        if reload > 0:
            reload -= 1
        if reload == 0:
            if pygame.K_SPACE in keys:
                if orientation == 'L':
                    bullets_l.append(gamebox.from_image(character.x, character.y, 'bullet_l.png'))
                    gun_sound.play()
                    reload = reload_time
                else:
                    bullets_r.append(gamebox.from_image(character.x, character.y, 'bullet_r.png'))
                    gun_sound.play()
                    reload = reload_time

        for c in range(len(bullets_l)):
            bullets_l[c].x -= 5
        for d in range(len(bullets_r)):
            bullets_r[d].x += 5

        for p in range(len(explosion_length)):
            explosion_length[p] += 1
            if explosion_length[p] == 15:
                del enemy_explosions[p]
                del explosion_length[p]

        for bullet_l in bullets_l:
            for side in sides:
                if bullet_l.touches(side):
                    bullets_l.remove(bullet_l)
            for wall in walls:
                if bullet_l.touches(wall):
                    bullets_l.remove(bullet_l)
            for enemy in enemies:
                if bullet_l.touches(enemy):
                    enemy_explosions.append(gamebox.from_image(enemy.x, enemy.y, 'explosion.png'))
                    explosion_length.append(0)
                    enemies.remove(enemy)
                    enemy_death_sound.play()
                    kills += 1
                    if bullet_l in bullets_l:
                        bullets_l.remove(bullet_l)
            if life != 0:
                camera.draw(bullet_l)

        for bullet_r in bullets_r:
            for side in sides:
                if bullet_r.touches(side):
                    bullets_r.remove(bullet_r)
            for wall in walls:
                if bullet_r.touches(wall):
                    bullets_r.remove(bullet_r)
            for enemy in enemies:
                if bullet_r.touches(enemy):
                    enemy_explosions.append(gamebox.from_image(enemy.x, enemy.y, 'explosion.png'))
                    explosion_length.append(0)
                    enemies.remove(enemy)
                    enemy_death_sound.play()
                    kills += 1
                    if bullet_r in bullets_r:
                        bullets_r.remove(bullet_r)
            if life != 0:
                camera.draw(bullet_r)

        if orientation == 'L':
            shot_direction = -5
        else:
            shot_direction = 5

    # ############################ SHOOTING ###########################################################

        if pygame.K_RIGHT in keys:
            if character.x <= 988:
                character.x += 1
                if pygame.K_SPACE not in keys or falling:
                    character.x += character_speed
            orientation = 'R'

        if pygame.K_LEFT in keys:
            if character.x >= 12:
                character.x -= 1
                if pygame.K_SPACE not in keys or falling:
                    character.x -= character_speed
            orientation = 'L'

        if pygame.K_SPACE in keys and pygame.K_RIGHT not in keys and pygame.K_LEFT not in keys and not falling:
            character = gamebox.from_image(character.x, character.y, sheet[19])

        elif pygame.K_SPACE in keys and (pygame.K_RIGHT in keys or pygame.K_LEFT in keys) and not falling:
            character = gamebox.from_image(character.x, character.y, sheet[16 + counter_space])
        elif pygame.K_SPACE not in keys and (pygame.K_RIGHT in keys or pygame.K_LEFT in keys) and not falling:
            character = gamebox.from_image(character.x, character.y, sheet[8 + counter_side])
        else:
            character = gamebox.from_image(character.x, character.y, sheet[1 + counter_space])

    # ############# Health ################################################
        for hurt in enemies:
            if character.touches(hurt):
                #if life > 0:
                life -= 5
        if life == 0:

            if invincibility == False:
                gamebox.pause()
            game_over_sound.play()

            # score_rec_disp = open('scoreboard.txt', 'r')
            # line_read = score_rec_disp.readline().split(',')
            # score_rec_disp.close()

            score_clearing = open('scoreboard.txt', 'w')
            score_clearing.write('')
            score_clearing.close()

            # for string_score in range(len(line_read)):
            #     line_read[string_score] = int(line_read[string_score])

            line_read.append(score)
            line_read = sorted(line_read)
            line_read.reverse()
            score_recording = open('scoreboard.txt', 'a')
            for number_of_scores in range(len(line_read)):
                if number_of_scores == 0:
                    score_recording.write(str(line_read[number_of_scores]))
                else:
                    score_recording.write(','+str(line_read[number_of_scores]))
            score_recording.close()
            score_display = gamebox.from_text(500, 300, 'Your final score is: ' + str(score), 'Arial', 90, 'red', italic=True, bold=True)
            camera.draw(score_display)

        health = gamebox.from_image(500, 15, 'health_bar.png')
        no_health = gamebox.from_image(500, 15, 'no_health_bar.png')
        health.size = life, 30
        no_health.size = 500, 30

        if heal == coins_to_heal and life < 500:
            heal = 0
            life += heal_power
    # ############# Health ################################################

    # ############# ENEMY #################################################
        for enemy in enemies:
            if enemy.x < character.x:
                enemy.x += enemy_speed
            elif enemy.x > character.x:
                enemy.x -= enemy_speed
            if enemy.y < character.y:
                enemy.y += enemy_speed
            elif enemy.y > character.y:
                enemy.y -= enemy_speed
    # ############# ENEMY #################################################

    # ############ Coins ##################################################
        tic_cnt[3] += 1
        if tic_cnt[3] == coin_spawn_rate:
            coins.append(gamebox.from_image(random.randint(15, 985), 15, coin_sheet[1 + counter_coins]))

            coin_timer.append(coin_life_span)
            tic_cnt[3] = 0
        for coin in coins:
            coin.y += 5
            coin_timer[coins.index(coin)] -= 1
            if coin.touches(character):
                coin_sound.play()
                score += 1
                heal += 1
                coin_timer.remove(coin_timer[coins.index(coin)])
                coins.remove(coin)
                coins_towards_reload_increase += 1
                difficulty_increasing += 1
            for time_left in coin_timer:
                if time_left == 0:
                    coins.remove(coins[coin_timer.index(time_left)])
                    coin_timer.remove(time_left)
            coin = gamebox.from_image(coin.x, coin.y, coin_sheet[counter_coins])
            if life != 0:
                camera.draw(coin)
        score_display = gamebox.from_text(20, 15, str(score), 'Arial', 20, 'yellow', italic=True, bold=True)
        health_display = gamebox.from_text(500, 15, str(life), 'Arial', 20, 'white', italic=True, bold=True)
        kills_display = gamebox.from_text(20, 40, str(kills), 'Arial', 20, 'red', italic=True, bold=True)

        if coins_towards_reload_increase == coins_to_hasten_reload and (reload_time-reload_reduction) >= 0:
            reload_time -= reload_reduction
            coins_towards_reload_increase = 0

        if difficulty_increasing == coins_to_increase_enemy_spawn_rate and enemy_spawn_rate > amount_spawn_rate_increases:
            enemy_spawn_rate -= amount_spawn_rate_increases
            difficulty_increasing = 0
    # ############ Coins ##################################################

        # **// Creates Jumping // Stops Sprite Overlapping
        for wall in walls:
            if character.bottom_touches(wall):
                velocity = 0
                if pygame.K_UP in keys:
                    velocity = jump_power
            for koin in coins:
                # koin.scale_by(0.2)
                if koin.bottom_touches(wall):
                    koin.move_to_stop_overlapping(wall)
            if character.touches(wall):
                character.move_to_stop_overlapping(wall)
            if life != 0:
                camera.draw(wall)

        if orientation == 'L':
            character == character.flip()

    # General Drawing area
        if life != 0:
            camera.draw(score_display)
            camera.draw(kills_display)
            camera.draw(character)
            camera.draw(no_health)
            camera.draw(health)
            camera.draw(health_display)
            for evil in enemies:
                evil = gamebox.from_image(evil.x, evil.y, enemy_sheet[counter_enemy])
                camera.draw(evil)
            for z in range(len(sides)):
                camera.draw(sides[z])
            for things in enemy_explosions:
                camera.draw(things)


        #camera.display()
    camera.display()
ticks_per_second = 60
gamebox.timer_loop(ticks_per_second, tick)
