import pygame

pygame.init()
screen = pygame.display.set_mode((900, 600))
pygame.display.set_caption("Pong Game")
clock = pygame.time.Clock()
fps = 30

background_color = (0, 0, 0)
paddle_color = (255, 255, 255)
text = pygame.font.SysFont("Arial", 30)

class Paddle:
    def __init__(self, posx, posy, width, height, speed, color):
        self.posx = posx
        self.posy = posy
        self.width = width
        self.height = height
        self.speed = speed
        self.color = color
        self.rect = pygame.Rect(posx, posy, width, height)

    def display(self):
        pygame.draw.rect(screen, self.color, self.rect)
    
    def update(self, ydirection):
        self.posy += self.speed * ydirection

        if self.posy <= 0:
            self.posy = 0
        elif self.posy + self.height >= 600:
            self.posy = 600 - self.height

        self.rect = pygame.Rect(self.posx, self.posy, self.width, self.height)
    
    def display_score(self, font, score, posx, posy, color):
        score_surface = font.render(str(score), True, color)
        screen.blit(score_surface, (posx, posy))
    
    def get_rect(self):
        return self.rect


class Ball:
    def __init__(self, posx, posy, radius, speed, color):
        self.posx = posx
        self.posy = posy
        self.radius = radius
        self.speed = speed
        self.color = color
        self.xdirection = 1
        self.ydirection = -1
        self.firstTime = 1
        self.rect = pygame.Rect(self.posx - radius, self.posy - radius, radius*2, radius*2)

    def display(self):
        pygame.draw.circle(screen, self.color, (self.posx, self.posy), self.radius)
        self.rect = pygame.Rect(self.posx - self.radius, self.posy - self.radius, self.radius*2, self.radius*2)

    def update(self):
        self.posx += self.speed * self.xdirection
        self.posy += self.speed * self.ydirection
    
        if self.posy <= 0 or self.posy >= 600:
            self.ydirection *= -1

        if self.posx <= 0 and self.firstTime:
            self.firstTime = 0
            return 1
        elif self.posx >= 900 and self.firstTime:
            self.firstTime = 0
            return -1
        else:
            return 0

    def reset(self):
        self.posx = 900 // 2
        self.posy = 600 // 2
        self.xdirection *= -1
        self.firstTime = 1
    
    def hit(self):
        self.xdirection *= -1

    def get_rect(self):
        return self.rect


def main():
    running = True

    player1 = Paddle(20, 0, 10, 100, 10, (255, 255, 255))
    player2 = Paddle(900 - 30, 0, 10, 100, 10, (255, 255, 255))
    ball = Ball(900 // 2, 600 // 2, 7, 7, (255, 255, 255))

    listOfPlayers = [player1, player2]
    player1Score, player2Score = 0, 0
    player1YFac, player2YFac = 0, 0

    while running:
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player2YFac = -1
                if event.key == pygame.K_DOWN:
                    player2YFac = 1
                if event.key == pygame.K_w:
                    player1YFac = -1
                if event.key == pygame.K_s:
                    player1YFac = 1

            if event.type == pygame.KEYUP:
                if event.key in (pygame.K_UP, pygame.K_DOWN):
                    player2YFac = 0
                if event.key in (pygame.K_w, pygame.K_s):
                    player1YFac = 0

        for player in listOfPlayers:
            if ball.get_rect().colliderect(player.get_rect()):
                ball.hit()

        player1.update(player1YFac)
        player2.update(player2YFac)
        point = ball.update()

        if point == -1:
            player1Score += 1
        elif point == 1:
            player2Score += 1

        if point:
            ball.reset()

        player1.display()
        player2.display()
        ball.display()

        player1.display_score(text, player1Score, 100, 20, (255, 255, 255))
        player2.display_score(text, player2Score, 800, 20, (255, 255, 255))

        pygame.display.update()
        clock.tick(fps)


if __name__ == "__main__":
    main()
    pygame.quit()