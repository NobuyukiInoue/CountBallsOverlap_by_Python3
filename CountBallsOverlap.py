# -*- coding: utf-8 -*-

""" Count contact between balls. """

import math
import os
import pygame
import pygame.locals
import random
import re
import sys
import time

class params:
    def __init__(self):
        # default params.
        self.START_WAIT = 0
        self.MAX_WIDTH = 640
        self.MAX_HEIGHT = 480
        self.MAX_BALLS = 300
        self.RADIUS = 3
        self.MOVEMENT = (-3, 3, 1)
        self.SLEEP_SEC = 0.0
        self.CHART_HEIGHT = 0
        self.ENABLE_BAR = False
        self.BAR = bar()
        self.TURNS_REQUIRED_FOR_HEAL = 100  # -1 ... Does not heal.
        self.RATIO_OF_BALLS_STOPPED = 0.0

class drawratio:
    def __init__(self, PARAMS, infected_incremental):
        self.INFECTED_INCREMENTAL = 3
        self.WIDTH = 1
        self.HEIGHT = PARAMS.CHART_HEIGHT / PARAMS.MAX_BALLS

class bar:
    def __init__(self):
        self.POS_X = 100
        self.HEIGHT = 100
        self.WIDTH = 6

class colors:
    def __init__(self):
        self.BLACK = (0, 0, 0)
        self.BLUE = (0, 0, 255)
        self.GREEN = (0, 255, 0)
        self.SKY = (0, 255, 255)
        self.RED = (255, 0, 0)
        self.MAGENTA = (255, 0, 255)
        self.YELLOW = (255, 255, 0)
        self.WHITE = (255, 255, 255)

class ball:
    def __init__(self, pos_x, pos_y, add_x, add_y, max_x, max_y, radius, color):
        self.forecolor = color
        self.radius = radius
        self.x, self.y = pos_x, pos_y
        self.add_x, self.add_y = add_x, add_y
        self.max_x, self.max_y = max_x, max_y
        self.contacted = False
        self.turn_heal = -1
        self.turn_infection = -1
        self.healed = False

    def get_position(self):
        return (self.x, self.y)

    def set_nextposition(self, PARAMS):
        next_x = self.x + self.add_x
        next_y = self.y + self.add_y

        if next_x <= 0:
            self.add_x = abs(self.add_x)
            self.x += self.add_x - (self.x -  0)
            
        elif next_x >= self.max_x:
            self.add_x = -abs(self.add_x)
            self.x += self.add_x + (self.max_x - self.x)

        elif PARAMS.ENABLE_BAR:
            if PARAMS.BAR.POS_X <= self.x and self.x <= PARAMS.BAR.POS_X + PARAMS.BAR.WIDTH \
            and (self.y <= PARAMS.BAR.HEIGHT or PARAMS.MAX_HEIGHT - PARAMS.BAR.HEIGHT <= self.y):
                # Determine if ball in bar.
                self.x += self.add_x

            elif PARAMS.BAR.POS_X <= next_x and next_x <= PARAMS.BAR.POS_X + PARAMS.BAR.WIDTH \
            and (next_y <= PARAMS.BAR.HEIGHT or PARAMS.MAX_HEIGHT - PARAMS.BAR.HEIGHT <= next_y):
                # Determine if ball hits bar.
                if self.x <= PARAMS.BAR.POS_X:
                    self.add_x = -abs(self.add_x)
                elif PARAMS.BAR.POS_X + PARAMS.BAR.WIDTH <= self.x:
                    self.add_x = abs(self.add_x)
                else:
                    self.add_x *= -1
            self.x += self.add_x

        else:
            self.x += self.add_x

        if self.y - self.radius <= 0:
            self.add_y = abs(self.add_y)            
        elif self.y + self.radius >= self.max_y:
            self.add_y = -abs(self.add_y)
        self.y += self.add_y

    def set_contacted(self, turn_infection, turn_heal, color):
        self.forecolor = color
        self.contacted = True
        self.turn_infection = turn_infection
        self.turn_heal = self.turn_infection + turn_heal

    def set_heal(self, color):
        self.healed = True
        self.forecolor = color

    def isOverlapTo(self, target_pos):
        if math.sqrt((target_pos[0] - self.x)**2 + (target_pos[1] - self.y)**2) < 2*self.radius:
            return True
        return False

def load_patternfile(filename):
    """looad pattern file"""

    patternfile = open(filename, "r")
    lines = patternfile.readlines()
    patternfile.close()

    # set defalt value
    PARAMS = params()

    for line in lines:
        line = re.sub("#.*", "", line)
        line = re.sub("//.*", "", line)
        line = line.replace(" ", "").rstrip()
        line = line.replace("\t", "").rstrip()
        flds = line.split("=")

        if len(flds) >= 2:
            try:
                item_name = flds[0].lower()
                if item_name == "start_wait":
                    PARAMS.START_WAIT = int(flds[1])
                elif item_name == "max_width":
                    PARAMS.MAX_WIDTH = int(flds[1])
                elif item_name == "max_height":
                    PARAMS.MAX_HEIGHT = int(flds[1])
                elif item_name == "max_balls":
                    PARAMS.MAX_BALLS = int(flds[1])
                elif item_name == "radius":
                    PARAMS.RADIUS = int(flds[1])
                elif item_name == "movement":
                        movement_flds = flds[1].split(",")
                        if len(movement_flds) >= 3:
                            PARAMS.MOVEMENT = (int(movement_flds[0]), int(movement_flds[1]), int(movement_flds[2]))
                elif item_name == "sleep_sec":
                    PARAMS.SLEEP_SEC = float(flds[1])
                elif item_name == "chart_height":
                    PARAMS.CHART_HEIGHT = int(flds[1])
                elif item_name == "bar":
                    if flds[1].upper() == "FALSE":
                        PARAMS.ENABLE_BAR = False
                    else:
                        PARAMS.ENABLE_BAR = True
                        BAR_flds = flds[1].split(",")
                        if len(BAR_flds) >= 1:
                            PARAMS.BAR.POS_X = int(BAR_flds[0])
                            PARAMS.BAR.HEIGHT = int(BAR_flds[1])
                            PARAMS.BAR.WIDTH = int(BAR_flds[2])
                        else:
                            PARAMS.ENABLE_BAR = False
                elif item_name == "heal":
                    PARAMS.TURNS_REQUIRED_FOR_HEAL = int(flds[1])
                elif item_name == "ratio_of_balls_stopped":
                    if 0.0 <= float(flds[1]) and float(flds[1]) <= 1.0:
                        PARAMS.RATIO_OF_BALLS_STOPPED = float(flds[1])
            except:
                continue
    return PARAMS

class R_Note:
    def __init__(self, results_width):
        self.results_WIDTH = results_width
        self.term_turn = 0
        self.term_incremental = 0
        self.value = 0
        self.value_max = 0
        self.value_max_turn_begin = 0
        self.value_max_turn_end = 0

def init_ball_position(PARAMS):
    if PARAMS.ENABLE_BAR:
        while True:
            x = random.randint(PARAMS.RADIUS, PARAMS.MAX_WIDTH - PARAMS.RADIUS)
            if x + PARAMS.RADIUS < PARAMS.BAR.POS_X or PARAMS.BAR.POS_X + PARAMS.BAR.WIDTH < x - PARAMS.RADIUS:
                break
    else:
        x = random.randint(PARAMS.RADIUS, PARAMS.MAX_WIDTH - PARAMS.RADIUS)
    y = random.randint(PARAMS.RADIUS, PARAMS.MAX_HEIGHT - PARAMS.RADIUS)

    return x, y


def screen_eventcheck():
    # pygame event check.
    for event in pygame.event.get():
        if event.type == pygame.locals.QUIT:
            pygame.quit()
            exit(0)

def main():
    argv = sys.argv
    argc = len(argv)

    if argc > 1:
        if not os.path.exists(argv[1]):
            print("{0} not found.".format(argv[1]))
            return
        PARAMS = load_patternfile(argv[1])
    else:
        PARAMS = params()

    if PARAMS.CHART_HEIGHT == 0:
        PARAMS.CHART_HEIGHT = PARAMS.MAX_BALLS

    print("MAX_WIDTH = {0:d}\n"
        "MAX_HEIGHT = {1:d}\n"
        "MAX_BALLS = {2:d}\n"
        "RADIUS = {3:d}\n"
        "MOVEMENT = {4}\n"
        "SLEEP_SEC = {5:f}\n"
        "CHART_HEIGHT = {6:d}\n"
        "TURNS_REQUIRED_FOR_HEAL = {7:d}\n"
        "RATIO_OF_BALLS_STOPPED = {8}\n"
        "ENABLE_BAR = {9}".format(
                PARAMS.MAX_WIDTH,
                PARAMS.MAX_HEIGHT,
                PARAMS.MAX_BALLS,
                PARAMS.RADIUS,
                PARAMS.MOVEMENT,
                PARAMS.SLEEP_SEC,
                PARAMS.CHART_HEIGHT,
                PARAMS.TURNS_REQUIRED_FOR_HEAL,
                PARAMS.RATIO_OF_BALLS_STOPPED,
                PARAMS.ENABLE_BAR
            )
        )

    if PARAMS.ENABLE_BAR:
        print("BAR.POS_X = {0}, BAR.HEIGHT = {1}, BAR.WIDTH = {2}".format(PARAMS.BAR.POS_X, PARAMS.BAR.HEIGHT, PARAMS.BAR.WIDTH))

    COLORS = colors()
    pygame.init()

    screen_size = (PARAMS.MAX_WIDTH, PARAMS.MAX_HEIGHT + PARAMS.RADIUS + PARAMS.CHART_HEIGHT)
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption(u"CountBallsOverlap")

    # record start time.
    time_start = time.time()

    # initialize balls.
    balls = []
    if PARAMS.RATIO_OF_BALLS_STOPPED == 0.0:
        # When RATIO_OF_BALLS_STOPPED is not specified.
        for i in range(PARAMS.MAX_BALLS):
            x, y = init_ball_position(PARAMS)
            add_x, add_y = 0, 0
            while add_x == 0:
                add_x = random.randrange(PARAMS.MOVEMENT[0], PARAMS.MOVEMENT[1] + 1, PARAMS.MOVEMENT[2])
            while add_y == 0:
                add_y = random.randrange(PARAMS.MOVEMENT[0], PARAMS.MOVEMENT[1] + 1, PARAMS.MOVEMENT[2]) 
            balls.append(ball(x, y, add_x, add_y, PARAMS.MAX_WIDTH, PARAMS.MAX_HEIGHT, PARAMS.RADIUS, COLORS.BLUE))

    else:
        # When RATIO_OF_BALLS_STOPPED is specified.
        target_max = int(PARAMS.MAX_BALLS * (1.0 - PARAMS.RATIO_OF_BALLS_STOPPED))
        for i in range(target_max):
            x, y = init_ball_position(PARAMS)
            add_x, add_y = 0, 0
            while add_x == 0:
                add_x = random.randrange(PARAMS.MOVEMENT[0], PARAMS.MOVEMENT[1] + 1, PARAMS.MOVEMENT[2])
            while add_y == 0:
                add_y = random.randrange(PARAMS.MOVEMENT[0], PARAMS.MOVEMENT[1] + 1, PARAMS.MOVEMENT[2]) 
            balls.append(ball(x, y, add_x, add_y, PARAMS.MAX_WIDTH, PARAMS.MAX_HEIGHT, PARAMS.RADIUS, COLORS.BLUE))

        add_x, add_y = 0, 0
        for i in range(PARAMS.MAX_BALLS - target_max):
            x, y = init_ball_position(PARAMS)
            balls.append(ball(x, y, add_x, add_y, PARAMS.MAX_WIDTH, PARAMS.MAX_HEIGHT, PARAMS.RADIUS, COLORS.BLUE))

    # Make the first ball red.
    # balls[0].set_contacted(COLORS.RED)

    # Make the leftmost ball red.
    min_x, target_turn = sys.maxsize, 0
    for i in range(len(balls)):
        if balls[i].x < min_x:
            min_x = balls[i].x
            target_turn = i
    balls[target_turn].set_contacted(0, PARAMS.TURNS_REQUIRED_FOR_HEAL, COLORS.RED)
    contacted_count = 1

    # font for contact count information.
    font = pygame.font.Font(None, 24)

    results = []
    turn = 0
    pre_result = (0, contacted_count, contacted_count, 0)
    DRAW_RATIO = drawratio(PARAMS, 3)
    R0 = R_Note(5)

    while True:
        screen.fill(COLORS.WHITE)
        
        # draw horizontal line.
        pygame.draw.line(screen, COLORS.BLACK, (0, 0), (PARAMS.MAX_WIDTH, 0))
        pygame.draw.line(screen, COLORS.BLACK, (0, PARAMS.MAX_HEIGHT), (PARAMS.MAX_WIDTH, PARAMS.MAX_HEIGHT))

        # draw vertical line.
        pygame.draw.line(screen, COLORS.BLACK, (0, 0), (0, PARAMS.MAX_HEIGHT))
        pygame.draw.line(screen, COLORS.BLACK, (PARAMS.MAX_WIDTH, PARAMS.MAX_HEIGHT), (PARAMS.MAX_WIDTH, PARAMS.MAX_HEIGHT))

        # heal check.
        if turn > 0:
            for i in range(PARAMS.MAX_BALLS):
                if balls[i].contacted and balls[i].turn_heal == turn:
                    balls[i].set_heal(COLORS.GREEN)

        # contact check.
        infected_count, healed_count = 0, 0
        for i in range(PARAMS.MAX_BALLS):
            if balls[i].contacted and balls[i].healed == False:
                infected_count += 1
            if balls[i].healed:
                healed_count += 1
            for j in range(i + 1, PARAMS.MAX_BALLS):
                conditions_i = balls[i].contacted and balls[i].healed == False
                conditions_j = balls[j].contacted and balls[j].healed == False
                if conditions_i and conditions_j:
                    continue
                if balls[i].healed or balls[j].healed:
                    continue
                if conditions_i:
                    if balls[i].isOverlapTo(balls[j].get_position()):
                        balls[j].set_contacted(turn, PARAMS.TURNS_REQUIRED_FOR_HEAL, COLORS.RED)
                        contacted_count += 1
                elif conditions_j:
                    if balls[j].isOverlapTo(balls[i].get_position()):
                        balls[i].set_contacted(turn, PARAMS.TURNS_REQUIRED_FOR_HEAL, COLORS.RED)
                        contacted_count += 1

        # draw bar.
        if PARAMS.ENABLE_BAR:
            # draw uppwer bar.
            pygame.draw.line(screen, COLORS.BLACK, (PARAMS.BAR.POS_X, 0), (PARAMS.BAR.POS_X, PARAMS.BAR.HEIGHT), PARAMS.BAR.WIDTH)

            # draw lower bar.
            pygame.draw.line(screen, COLORS.BLACK, (PARAMS.BAR.POS_X, PARAMS.MAX_HEIGHT), (PARAMS.BAR.POS_X, PARAMS.MAX_HEIGHT - PARAMS.BAR.HEIGHT), PARAMS.BAR.WIDTH)

        # draw balls.
        for i in range(PARAMS.MAX_BALLS):
            pygame.draw.circle(screen, balls[i].forecolor, balls[i].get_position(), balls[i].radius)

        # print contact count information to console.
        if contacted_count != pre_result[1] \
        or infected_count != pre_result[2] \
        or healed_count != pre_result[3]:
            results.append((turn, contacted_count, infected_count, healed_count, PARAMS.MAX_BALLS - contacted_count))
            print("{0:d}:{1:d},{2:d},{3:d},{4:d}".format(turn, contacted_count, infected_count, healed_count, PARAMS.MAX_BALLS - contacted_count))
            pre_result = (turn, contacted_count, infected_count, healed_count)

        results_length = len(results) 
        if results_length > R0.results_WIDTH:
            R0.term_incremental = results[results_length - 1][2] - results[results_length - 1 - R0.results_WIDTH][2]
            if R0.term_incremental > 0:
                R0.term_turn = results[results_length - 1][0] - results[results_length - 1 - R0.results_WIDTH][0]
            #   R0 = (term_incremental/term_turn)*(1/PARAMS.TURNS_REQUIRED_FOR_HEAL);
            #   R0.value = (term_incremental/term_turn)*PARAMS.TURNS_REQUIRED_FOR_HEAL;
                R0.value = R0.term_incremental/R0.term_turn
                if R0.value > R0.value_max:
                    R0.value_max = R0.value
                    R0.value_max_turn_begin = results[results_length - 1 - R0.results_WIDTH][0]
                    R0.value_max_turn_end = results[results_length - 1][0]

        # draw contact count chart.
        if turn > 0 and results_length > 0:
            for i in range(0, 5):
                if PARAMS.MAX_WIDTH * i >= turn:
                    DRAW_RATIO.WIDTH = i
                    break
            
            pre_x, pre_infected, pre_healed = 0, 0, 0

            for data in results:
                x = data[0]//DRAW_RATIO.WIDTH
                y_infected = PARAMS.MAX_HEIGHT + PARAMS.RADIUS + PARAMS.CHART_HEIGHT
                y_healed = PARAMS.MAX_HEIGHT + PARAMS.RADIUS

                # draw infected line to lower.
                pygame.draw.line(screen, COLORS.RED, (x, y_infected), (x, y_infected - data[2]*DRAW_RATIO.HEIGHT), 1)

                incremental_x = x - pre_x
                if incremental_x > 0:
                    for i in range(pre_x, x):
                        # draw previous infected line.
                        pygame.draw.line(screen, COLORS.RED, (i, y_infected), (i, y_infected - pre_infected*DRAW_RATIO.HEIGHT), 1)
                pre_infected = data[2]

                # draw healed line to upper.
                if data[3] > 0:
                    pygame.draw.line(screen, COLORS.GREEN, (x, y_healed), (x, y_healed + data[3]*DRAW_RATIO.HEIGHT), 1)

                    incremental_x = x - pre_x
                    if incremental_x > 0:
                        for i in range(pre_x, x):
                            # draw previous infected line.
                            pygame.draw.line(screen, COLORS.GREEN, (i, y_healed), (i, y_healed + pre_healed*DRAW_RATIO.HEIGHT), 1)
                    pre_healed = data[3]
                pre_x = x
    
        # display contact count information to screen.
        text = font.render("turn = " + str(turn), True, COLORS.BLACK)
        screen.blit(text, [0, PARAMS.MAX_HEIGHT + 10])

        text = font.render("TURNS_REQUIRED_FOR_HEAL = " + str(PARAMS.TURNS_REQUIRED_FOR_HEAL), True, COLORS.BLACK)
        screen.blit(text, [0, PARAMS.MAX_HEIGHT + 30])

        text = font.render("contacted = " + str(contacted_count) + "/" + str(PARAMS.MAX_BALLS), True, COLORS.BLACK)
        screen.blit(text, [0, PARAMS.MAX_HEIGHT + 50])

        text = font.render("healed = " + str(healed_count) + "/" + str(PARAMS.MAX_BALLS) + "(GREEN)", True, COLORS.BLACK)
        screen.blit(text, [0, PARAMS.MAX_HEIGHT + 70])

        text = font.render("infected = " + str(infected_count) + "/" + str(PARAMS.MAX_BALLS) + "(RED)", True, COLORS.BLACK)
        screen.blit(text, [0, PARAMS.MAX_HEIGHT + 90])

        text = font.render("Basic reproduction number(R0(max)) = " + str(int(R0.value_max*100)/100.0) + " (turn ... " + str(R0.value_max_turn_begin) + " to " + str(R0.value_max_turn_end) + ")", True, COLORS.BLACK)
        screen.blit(text, [0, PARAMS.MAX_HEIGHT + 110])

        # All balls are infected.
        if contacted_count == PARAMS.MAX_BALLS:
            text = font.render("infected incremental(BLUE)(ratio ... x" + str(DRAW_RATIO.INFECTED_INCREMENTAL) + ")", True, COLORS.BLACK)
            screen.blit(text, [0, PARAMS.MAX_HEIGHT + 130])
            text = font.render("end ... All balls are infected.", True, COLORS.BLACK)
            screen.blit(text, [0, PARAMS.MAX_HEIGHT + 170])

        # The infected balls are gone.
        if infected_count == 0:
            text = font.render("infected incremental(BLUE)(ratio ... x" + str(DRAW_RATIO.INFECTED_INCREMENTAL) + ")", True, COLORS.BLACK)
            screen.blit(text, [0, PARAMS.MAX_HEIGHT + 130])
            text = font.render("end ... The infected balls are gone.", True, COLORS.BLACK)
            screen.blit(text, [0, PARAMS.MAX_HEIGHT + 170])

        # draw scale line.
        draw_scale_line(screen, PARAMS, COLORS)

        # screen update.
        pygame.display.update()

        # Confirm start.
        if turn == 0:
            if PARAMS.START_WAIT > 0:
                time0 = time.time()
                print("Wait for start {0:d} second.".format(PARAMS.START_WAIT))
                while time.time() - time0 < PARAMS.START_WAIT:
                    screen_eventcheck()

            print("\n{0:s}:{1:s},{2:s},{3:s},{4:s}".format("turn", "contact", "infected", "healed", "remaining"))

        # display wait.
        if PARAMS.SLEEP_SEC > 0.0:
            time.sleep(PARAMS.SLEEP_SEC)

        # pygame event check.
        screen_eventcheck()

        # get next position.
        for i in range(PARAMS.MAX_BALLS):
            balls[i].set_nextposition(PARAMS)

        ###################################################
        # Break out of the loop.
        ###################################################
        # All balls are infected.
        if contacted_count >= PARAMS.MAX_BALLS:
            print("End ... All balls are infected.")
            break

        # The infected ball is gone.
        if infected_count == 0:
            print("End ... The infected ball is gone.")
            break
        ###################################################

        turn += 1

    # draw incremental line.
    pre_x, pre_data = 0, 0
    for data in results:
        x = data[0]//DRAW_RATIO.WIDTH
        y = PARAMS.MAX_HEIGHT + PARAMS.CHART_HEIGHT + PARAMS.RADIUS
        incremental_data = data[1] - pre_data
        incremental_x = x - pre_x
        if incremental_x > 0:
            # draw incremental line.
            pygame.draw.line(screen, COLORS.BLUE, (x, y), (x, y - int((incremental_data/incremental_x)*DRAW_RATIO.INFECTED_INCREMENTAL)) , 1)

        pre_x = x
        pre_data = data[1]

    # draw scale line.
    draw_scale_line(screen, PARAMS, COLORS)

    # screen update.
    pygame.display.update()

    # print execute time.
    print("Execute time ... : %f[s]" %(time.time() - time_start))

    while True:
        # pygame event check.
        screen_eventcheck()

def draw_scale_line(screen, PARAMS, COLORS):
    for x in range(100, PARAMS.MAX_WIDTH, 100):
        pygame.draw.line(screen, (128, 128, 128), (x, PARAMS.MAX_HEIGHT + PARAMS.RADIUS), (x, PARAMS.MAX_HEIGHT + PARAMS.RADIUS + PARAMS.CHART_HEIGHT), 1)

    for y in range(PARAMS.MAX_HEIGHT + PARAMS.RADIUS, PARAMS.MAX_HEIGHT + PARAMS.RADIUS + PARAMS.CHART_HEIGHT, 100):
        pygame.draw.line(screen, (128, 128, 128), (0, y), (PARAMS.MAX_WIDTH, y), 1)

if __name__ == "__main__":
    main()
