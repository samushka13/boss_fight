import pygame
import random


class Robot:
    """Class that describes the brave robot that dares face the ghastly door."""

    def __init__(self, screen):
        self.screen = screen
        self.image = pygame.image.load("robo.png")
        self.x_position = 320-self.image.get_width()/2
        self.y_position = 480-self.image.get_height()
        self.health = 1
        self.speed = 8
        self.move_right = False
        self.move_left = False
        self.shoot = False
        self.coin_image = pygame.image.load("kolikko.png")
        self.coin_position = 340
        self.coin_speed = 15
        self.coin_movement = 0

    def draw_image(self):
        self.screen.blit(self.image, (self.x_position, self.y_position))

    def handle_commands(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.move_left = True
            if event.key == pygame.K_RIGHT:
                self.move_right = True
            if event.key == pygame.K_SPACE:
                self.shoot = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.move_left = False
            if event.key == pygame.K_RIGHT:
                self.move_right = False
            if event.key == pygame.K_SPACE:
                self.shoot = True

    def handle_movement(self):
        if self.move_right:
            if self.x_position + self.image.get_width() < 640:
                self.x_position += self.speed
            else:
                self.x_position += 0
        if self.move_left:
            if self.x_position > 0:
                self.x_position -= self.speed
            else:
                self.x_position -= 0

    def shoot_coin(self, boss):
        coin_position_x = self.x_position + random.randrange(-10, 10)
        coin_position_y = self.coin_position-self.coin_speed*self.coin_movement
        self.screen.blit(self.coin_image, (coin_position_x, coin_position_y))
        self.coin_movement += 1

        hit_boss_1 = int(round(coin_position_x, 0)) in range(int(round(boss.x_position, 0)), int(round(boss.x_position+30, 0))) and int(round(coin_position_y, 0)) in range(int(round(boss.y_position, 0)), int(round(boss.y_position+40, 0)))
        hit_boss_2 = int(round(coin_position_x, 0)) in range(int(round(boss.x_position-30, 0)), int(round(boss.x_position, 0))) and int(round(coin_position_y, 0)) in range(int(round(boss.y_position-40, 0)), int(round(boss.y_position, 0)))
        if hit_boss_1 or hit_boss_2:
            boss.handle_hit()
            self.shoot = False

    def handle_hit(self):
        self.health -= 1
        if self.health <= 0:
            self.handle_death()

    def handle_death(self):
        self.speed = 0
        self.y_position = 440       
        self.image = pygame.transform.rotate(self.image, 90)


class Boss:
    """Class that describes the ghastly door that tries to murder the brave robot."""

    def __init__(self, screen):
        self.screen = screen
        self.image = pygame.image.load("ovi.png")
        self.x_position = 320-self.image.get_width()/2
        self.y_position = 100-self.image.get_height()
        self.health = 10
        self.speed = 10
        self.teleport_delay = 300
        self.shooting_delay = 20
        self.monster_image = pygame.image.load("hirvio.png")
        self.monster_position = 120

    def draw_image(self):
        self.screen.blit(self.image, (self.x_position, self.y_position))

    def draw_health_bar(self):
        pygame.draw.rect(self.screen, (0, 0, 255), (10, 10, 62*self.health, 10))

    def teleport(self):
        self.x_position = random.randrange(20, 620)
        self.y_position = random.randrange(20, 180)
        self.teleport_delay = 300

    def shoot_monster(self, robo):
        monster_position_x = self.x_position + random.randrange(-10,10)
        monster_position_y = self.monster_position+self.monster_speed()*(-self.shooting_delay)
        self.screen.blit(self.monster_image, (monster_position_x, monster_position_y))

        hit_robo_1 = int(round(monster_position_x, 0)) in range(int(round(robo.x_position, 0)), int(round(robo.x_position+30, 0))) and int(round(monster_position_y, 0)) in range(int(round(robo.y_position, 0)), int(round(robo.y_position+40, 0)))
        hit_robo_2 = int(round(monster_position_x, 0)) in range(int(round(robo.x_position-30, 0)), int(round(robo.x_position, 0))) and int(round(monster_position_y, 0)) in range(int(round(robo.y_position-40, 0)), int(round(robo.y_position, 0)))
        if hit_robo_1 or hit_robo_2:
            robo.handle_hit()
            self.shooting_delay = 5
        elif monster_position_y > self.monster_frequency():
            self.shooting_delay = 20

    def monster_speed(self):
        if self.health in (8,9,10):
            monster_speed = 10
        if self.health in (5,6,7):
            monster_speed = 15
        if self.health in (2,3,4):
            monster_speed = 20
        if self.health == 1:
            monster_speed = 25
        return monster_speed

    def monster_frequency(self):
        if self.health in (8,9,10):
            monster_frequency = 1000
        if self.health in (4,5,6,7):
            monster_frequency = 850
        if self.health in (1,2,3):
            monster_frequency = 700
        return monster_frequency

    def handle_hit(self):
        self.health -= 1


class Scenery:
    """Class that describes the scenery that surrounds the epic battle."""

    def __init__(self, screen, boss):
        self.screen = screen
        self.boss = boss

    def draw_background(self):
        if self.boss.health > 0:
            self.screen.fill((25, 25, 25))
        else:
            self.screen.fill((173, 216, 230))

    def draw_elements(self):
        self.draw_moon()
        self.draw_rain()

    def draw_moon(self):
        if self.boss.health > 0:
            color = (255, 0, 0)
        else:
            color = (255, 255, 0)
        pygame.draw.circle(self.screen, color, (580, 70), 40)

    def draw_rain(self):
        if self.boss.health > 0:        
            for i in range(10):
                pygame.draw.circle(self.screen, (173, 216, 230), (random.randrange(620), random.randrange(480)), 2)


class Intro:
    """Class that describes the introduction of the epic battle."""

    def __init__(self, screen):
        self.screen = screen
        self.countdown = 5
        self.text = str(self.countdown)

    def draw_instructions(self):
        font = pygame.font.SysFont("Arial", 24)
        movement = font.render("Move left or right with the arrow keys", True, (255, 0, 0))
        self.screen.blit(movement, (320-movement.get_rect().width/2, 60))
        shooting = font.render("Shoot with the spacebar", True, (255, 0, 0))
        self.screen.blit(shooting, (320-shooting.get_rect().width/2, 120))
        objective = font.render("Beat the boss", True, (255, 0, 0))
        self.screen.blit(objective, (320-objective.get_rect().width/2, 180))
        self.draw_countdown()

    def draw_countdown(self):
        font_large = pygame.font.SysFont("Arial", 72)
        self.text = str(self.countdown) if self.countdown > 0 else "DIE!"
        countdown = font_large.render(self.text, True, (255, 0, 0))
        self.screen.blit(countdown, (320-countdown.get_rect().width/2, 280))

    def handle_countdown(self, event):
        if event.type == pygame.USEREVENT:
            self.countdown -= 1


class Ending:
    """Class that describes the ending scenes of the epic battle."""

    def __init__(self, screen, robo, boss):
        self.screen = screen
        self.robo = robo
        self.boss = boss
        self.countdown = 50

    def handle_ending(self):
        if self.boss.health <= 0:
            self.good_ending()
        if self.robo.health <= 0:
            self.bad_ending()

    def good_ending(self):
        font = pygame.font.SysFont("Arial", 24)
        line1 = font.render("And so the brave robot defeated the ghastly door,", True, (0, 0, 0))
        self.screen.blit(line1, (320-line1.get_rect().width/2, 120))
        if self.countdown < 35:
            line2 = font.render("and all was well with the world again...", True, (0, 0, 0))
            self.screen.blit(line2, (320-line2.get_rect().width/2, 180))
        if self.countdown < 15:
            self.screen.fill((0, 0, 0))
            line3 = font.render("Or was it?", True, (255, 0, 0))
            self.screen.blit(line3, (320-line3.get_rect().width/2, 230))
        if self.countdown < 8:
            self.boss.image = pygame.transform.scale(self.boss.image, (320, 480))
            self.boss.x_position = 540
            self.boss.x_position -= 12/self.countdown
            self.boss.y_position = 0
            self.boss.draw_image()

    def bad_ending(self):
        self.boss.x_position = self.robo.x_position
        self.boss.y_position = 120
        font = pygame.font.SysFont("Arial", 60)
        line1 = font.render("You died.", True, (255, 0, 0))
        self.screen.blit(line1, (320-line1.get_rect().width/2, 180))
        if self.countdown < 25:
            line2 = font.render("In case you didn't notice.", True, (255, 0, 0))
            self.screen.blit(line2, (320-line2.get_rect().width/2, 240))


class Game:
    """Class that describes the main game events."""

    def __init__(self, screen, robo, boss):
        self.screen = screen
        self.robo = robo
        self.boss = boss

    def handle_battle(self):
        self.robo.handle_movement()
        self.boss.draw_image()
        self.boss.draw_health_bar()
        self.handle_boss_teleport()
        self.handle_boss_shooting()
        self.handle_robo_shooting()

    def handle_robo_shooting(self):
        if self.robo.health > 0:
            if self.robo.shoot is True:
                self.robo.shoot_coin(self.boss)
            else:
                self.robo.coin_movement = 0

    def handle_boss_shooting(self):
        self.boss.shooting_delay -= 1
        if self.boss.shooting_delay <= 0:
            self.boss.shoot_monster(self.robo)

    def handle_boss_teleport(self):
        self.boss.teleport_delay -= 1
        if self.boss.teleport_delay <= 0:
            self.boss.teleport()


def start_game(): 
    pygame.init()
    pygame.display.set_caption("The Ghastly Door That Hates Coins And Murders Robots")
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()
    pygame.time.set_timer(pygame.USEREVENT, 1000)

    intro = Intro(screen)
    robo = Robot(screen)
    boss = Boss(screen)
    scenery = Scenery(screen, boss)
    game = Game(screen, robo, boss)
    ending = Ending(screen, robo, boss)

    while True:
        for event in pygame.event.get():
            intro.handle_countdown(event)
            robo.handle_commands(event)
            if event.type == pygame.QUIT:
                exit()

        scenery.draw_background()
        if intro.countdown >= 0:
            intro.draw_instructions()
        else:
            scenery.draw_elements()
            robo.draw_image()
            if boss.health > 0:
                game.handle_battle()
            if boss.health <= 0 or robo.health <= 0:
                ending.handle_ending()
                if ending.countdown > 0:
                    ending.countdown -= 0.1
                else:
                    break

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    start_game()
