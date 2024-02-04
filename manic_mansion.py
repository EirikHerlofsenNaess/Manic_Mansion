#importerer biblioteker vi bruker i koden
import pygame
import random
 
pygame.init() #starter pygame
 
 
#Farger i RGB 
BACKGROUND = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
GRAY = (60, 58, 63)
BLUE = (0, 0, 255)
DARK_GREEN = (0, 100, 0)
LIGHT_BLUE = (100,100,255)
RED = (255, 255, 0)
 
#bilder per sekund, og klokke som styrer tiden 
FPS = 60
clock = pygame.time.Clock()

#klasse for spillvindu
class Window:
    def __init__(self, width, height, color):
        self.width = width
        self.height = height
        self.color = color
        self.size = (self.width, self.height)
        self.surface = pygame.display.set_mode(self.size)
    def draw(self):
        self.surface.fill(self.color)
        
#klasse for safezones
class Zone():
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    def draw(self):
        pygame.draw.rect(main_window.surface, self.color, self.rect)
 
#generell klasse for spiller, menneske, hindring og spøkelse
class Object:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    def draw(self):
        pygame.draw.rect(main_window.surface, self.color, self.rect)
    def update(self):
        self.draw()
#klasse for spilleren
class Human(Object):
    def __init__(self, x, y, width, height, color, speed, score, carrying_sheep):
        super().__init__(x, y, width, height, color) #arver fra den generelle spillobjekt klassen
        self.speed = speed
        self.score = score
        self.carrying_sheep = carrying_sheep
    def move(self): #funksjon for å styre spilleren, med både WASD og piltaster
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP] :
            self.rect.y -= self.speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.rect.y += self.speed
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
    def increase_score(self):
        self.score += 1
    def reduce_speed(self): #styrer hva som skjer mens spilleren bærer sau
        if self.carrying_sheep == True:
            self.speed = 2
            self.color = WHITE
        else:
            self.speed = 4
            self.color = DARK_GREEN
    def check_collision(self): #sjekker om spilleren treffer en av spillets vegger
        if self.rect.x <= 0:
            self.rect.x = 0
        if self.rect.x >= main_window.width - self.width:
            self.rect.x = main_window.width - self.width
        if self.rect.y <= 0:
            self.rect.y = 0
        if self.rect.y >= main_window.height - self.height:
            self.rect.y = main_window.height - self.height
    def update(self):
        super().update()
        self.move()
        self.check_collision()
        self.reduce_speed()
#saue klasse
class Sheep(Object):
    def __init__(self, x, y, width, height, color, carried):
        super().__init__(x, y, width, height, color)
        self.carried = carried
#hindring klasse
class Obstacle(Object):
    def __init__(self, x, y, width, height, color):
        super().__init__(x, y, width, height, color)
#spøkelsesklasse
class Ghost(Object):
    def __init__(self, x, y, width, height, color, vx, vy):
        super().__init__(x, y, width, height, color)
        self.vx = vx
        self.vy = vy
    def move(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
    def check_collision(self): #gjør at spøkelset spretter av kantene av spillbrettet eller safezones
        if self.rect.x <= left_zone.rect.width:
            self.vx *= -1
        if self.rect.x >= main_window.width - right_zone.rect.width - self.rect.width:
            self.vx *= -1
        if self.rect.y <= 0:
            self.vy *= -1
        if self.rect.y >= main_window.height - self.rect.height:
            self.vy *= -1
    def update(self):
        super().update()
        self.move()
        self.check_collision()

#genererer spillbrettet og safezone
main_window = Window(800, 600, BACKGROUND)
left_zone = Zone(0, 0, 100, 600, LIGHT_BLUE)
right_zone = Zone(700, 0, 100, 600, GREEN)

#genererer spiller
 
human = Human(left_zone.width//2 - 12.5, main_window.height//2, 30, 30, DARK_GREEN, 4, 0, False)
 
obstacle_list = []
def generate_obstacle(): #funksjon som lager en hindring
    obstacle = Obstacle(random.randint(left_zone.width, right_zone.x - 30), random.randint(0, main_window.height - 30), 30, 30, GRAY) #genererer hindring mellom safezones
    #hvis den nylig genererte hindringen berører en annen hindring genereres den på nytt
    while any(obstacle.rect.colliderect(existing_obstacle.rect) for existing_obstacle in obstacle_list):
        obstacle = Obstacle(random.randint(left_zone.width, right_zone.x - 30), random.randint(0, main_window.height - 30), 30, 30, GRAY)

    obstacle_list.append(obstacle)
    return obstacle
#genererer 3 hindringer
for i in range(3):
    obstacle = generate_obstacle()
 
sheep_list = []

def generate_sheep(): #funksjon som lager en sau
    
    #genererer sau i høyre safezone
    sheep = Sheep(random.randint(right_zone.rect.x, main_window.width - 30), random.randint(right_zone.rect.y, main_window.height- 30), 30, 30, WHITE, False)
    #hvis den nylig genererte sauen berører en annen sau genereres den på nytt
    while any(sheep.rect.colliderect(existing_sheep.rect) for existing_sheep in sheep_list):
        sheep = Sheep(random.randint(right_zone.rect.x, main_window.width - 30), random.randint(right_zone.rect.y, main_window.height- 30), 30, 30, WHITE, False)

    sheep_list.append(sheep)
    return sheep
#lager noen sauer
for i in range(3):
    sheep = generate_sheep()
ghost_list = []
def generate_ghost():
    #genererer spøkelse med en tilfeldig fart, som kan bli høyere jo høyere score spilleren har
    ghost = Ghost(random.randint(left_zone.width, right_zone.x - 30), random.randint(0, main_window.height - 30), 30, 30, RED, random.randint(-1-human.score//3, 1+human.score//3), random.randint(-1-human.score//3, 1+human.score//3))
    
    #sjekker at det genererte spøkelset er i bevegelse
    while ghost.vx == 0 and ghost.vy == 0:
        ghost = Ghost(random.randint(left_zone.width, right_zone.x - 30), random.randint(0, main_window.height - 30), 30, 30, RED, random.randint(-1-human.score//3, 1+human.score//3), random.randint(-1-human.score//3, 1+human.score//3))
    ghost_list.append(ghost)
    return ghost

ghost = generate_ghost()

#kode som viser spillerens score
font = pygame.font.SysFont('Arial', 26)
def display_score():
    text_img = font.render(f"Score: {human.score}", True, WHITE)
    main_window.surface.blit(text_img, (10, 10))
 
#starter spillet
run = True
while run:
    #setter tempoet på spillet
    clock.tick(FPS)
    #funksjonalitet for å trykke seg ut av spillet 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    #laster inn spillbrettet og oppdaterer spillerens posisjon
    main_window.draw()
    left_zone.draw()
    right_zone.draw()
    human.update()
    #sjekker hvilke piltaster vi trykker på
    keys = pygame.key.get_pressed()
    for obstacle in obstacle_list:
        obstacle.update()
        #sjekker om spilleren kolliderer med hindring og gjør at det ikke er mulig å bevege seg gjennom hindringer
        if human.rect.colliderect(obstacle) and keys[pygame.K_d] or human.rect.colliderect(obstacle) and keys[pygame.K_RIGHT]:
            human.rect.x = obstacle.rect.x - human.rect.width
        if human.rect.colliderect(obstacle) and keys[pygame.K_a] or human.rect.colliderect(obstacle) and keys[pygame.K_LEFT]:
            human.rect.x = obstacle.rect.x + human.rect.width
        if human.rect.colliderect(obstacle) and keys[pygame.K_w] or human.rect.colliderect(obstacle) and keys[pygame.K_UP]:
            human.rect.y = obstacle.rect.y + human.rect.height
        if human.rect.colliderect(obstacle) and keys[pygame.K_s] or human.rect.colliderect(obstacle) and keys[pygame.K_DOWN]:
            human.rect.y = obstacle.rect.y - human.rect.height
    for sheep in sheep_list:
        sheep.update()
        if human.rect.colliderect(sheep):
            #hvis spilleren kolliderer med en sau imens de bærer en annen sau så avsluttes spillet
            if human.carrying_sheep == True:
                run = False
            else:
                human.carrying_sheep = True
                sheep_list.remove(sheep)
        #kode som styrer hva som skjer når spilleren kommer seg over til venstre safezone med en sau
        if human.rect.x <= right_zone.rect.width - 30 and human.carrying_sheep == True:
            human.carrying_sheep = False
            human.increase_score()
            generate_sheep()
            #genererer 3 nye hindringer, for ekstra vanskelighetsgrad
            for i in range(3):
                generate_obstacle()
            generate_ghost()
    for ghost in ghost_list:
        ghost.update()
        #spillet avsluttes hvis man kommer borti et spøkelse
        if human.rect.colliderect(ghost):
            run = False
            
    #viser poengscore og "snur lerrettet"
    display_score()
    pygame.display.flip()
#avslutter spillet dersom run = False
pygame.quit()