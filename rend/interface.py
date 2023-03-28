import pygame
from dataset import dataset

POSSIBLE_IDS = ['delhi', 'london', 'seoul', 'singapore', 'tokyo', 'toronto']
X_PADDING, Y_PADDING = 25, 25


class interface:
    screen: any
    ds: dataset
    running: bool
    station1: str
    station2: str
    calcdist: list

    def __init__(self) -> None:
        self.station1 = ''
        self.station2 = ''
        self.calcdist = []

    def onHover(self, scrn, pos, ln):
        font = pygame.font.Font('freesansbold.ttf', 16)
        text = font.render(ln, True, (255, 255, 255), (0, 0, 0))

        textRect = text.get_rect()
        textRect.center = (pos[0], pos[1] - Y_PADDING)

        scrn.blit(text, textRect)

    def get_xrange(self):
        x_vals = self.ds.x_vals
        return (min(x_vals), max(x_vals))

    def get_yrange(self):
        y_vals = self.ds.y_vals
        return (min(y_vals), max(y_vals))

    def scale_x(self, num):
        min_x, max_x = self.get_xrange()
        return (num - min_x)/(max_x - min_x) * 700

    def scale_y(self, num):
        min_y, max_y = self.get_yrange()
        return (num - min_y)/(max_y - min_y) * 700

    def probe_distcalc(self):
        # TODO, waiting for the alg and what it returns, but the rest should follow smoothly

        # im assuming here that i get a list of the station names, so i can change their colors to red
        # pass
        self.calcdist = ['Greenwood', 'Coxwell', 'Woodbine']

    def drawDataset(self, m1clicked):
        mouse = pygame.mouse.get_pos()

        for line_name in self.ds.loaded:
            line_data = self.ds.loaded[line_name]
            station_names = list(line_data.keys())
            prev_station_name = station_names[0]
            x, y = line_data[prev_station_name]["x"], line_data[prev_station_name]["y"]

            rect1 = pygame.draw.rect(self.screen, self.ds.cmap[line_name],
                                     (self.scale_x(x) + X_PADDING, self.scale_y(y) + Y_PADDING, 4, 4))

            if rect1.collidepoint(mouse):
                self.onHover(self.screen, (self.scale_x(x) + X_PADDING, self.scale_y(y) + Y_PADDING), line_name)

                if m1clicked:
                    if self.station1 == '':
                        self.station1 = line_name
                        self.probe_distcalc()
                    elif self.station2 == '':
                        self.station2 = line_name
                        self.probe_distcalc()
                    else:
                        self.station1 = line_name
                        self.station2 = ''
                        self.calcdist = []

            for station_name in station_names[1:]:
                x, y = line_data[station_name]["x"], line_data[station_name]["y"]

                prev_x, prev_y = line_data[prev_station_name]["x"], line_data[prev_station_name]["y"]

                rect2 = pygame.draw.rect(self.screen, self.ds.cmap[line_name],
                                         (self.scale_x(x) + X_PADDING, self.scale_y(y) + Y_PADDING, 4, 4))
                if rect2.collidepoint(mouse):
                    self.onHover(self.screen, (self.scale_x(x) + X_PADDING, self.scale_y(y) + Y_PADDING), station_name)

                    if m1clicked:
                        if self.station1 == '':
                            self.station1 = station_name
                            self.probe_distcalc()
                        elif self.station2 == '':
                            self.station2 = station_name
                            self.probe_distcalc()
                        else:
                            self.station1 = station_name
                            self.station2 = ''
                            self.calcdist = []

                col = self.ds.cmap[line_name]
                if station_name in self.calcdist:
                    col = (255, 0, 0)

                pygame.draw.line(self.screen, col,
                                 (self.scale_x(x) + X_PADDING, self.scale_y(y) + Y_PADDING),
                                 (self.scale_x(prev_x) + X_PADDING, self.scale_y(prev_y) + Y_PADDING))

                prev_station_name = station_name

    def addButton(self, txt, pos):
        smallfont = pygame.font.SysFont('Corbel', 35)
        text = smallfont.render(txt, True, (255, 0, 0))

        rect2 = pygame.draw.rect(self.screen, (0, 255, 0), [pos[0], pos[1], 140, 40])
        self.screen.blit(text, (pos[0] + 50 - text.get_width()/2, pos[1] + text.get_height() / 2))

        return rect2

    def start(self):
        self.ds = dataset('./dataset/dataset/toronto.json')

        self.running = True
        pygame.init()
        self.screen = pygame.display.set_mode((1250, 750))
        clock = pygame.time.Clock()
        dt = 0

        while self.running:
            m1clicked = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONUP:
                    m1clicked = True

            self.screen.fill("white")
            mouse = pygame.mouse.get_pos()

            self.drawDataset(m1clicked)

            dsRects = []

            initial_position = (750, 100)
            for i in range(len(POSSIBLE_IDS)):
                buttonText = POSSIBLE_IDS[i]
                button = self.addButton(buttonText, (initial_position[0], initial_position[1] + i * 45))

                dsRects.append(button)

                if m1clicked and button.collidepoint(mouse):
                    self.ds.load_dataset('./dataset/dataset/' + str.lower(buttonText) + '.json')

            sta1 = self.addButton('Station 1: ' + self.station1, (750, 400))
            sta2 = self.addButton('Station 2: ' + self.station2, (initial_position[0], 445))

            # pygame.display.flip()
            # keys = pygame.key.get_pressed()
            # if keys[pygame.K_w]:
            #     player_pos.y -= 300 * dt

            pygame.display.update()
            dt = clock.tick(60) / 1000

        pygame.quit()


def interface_runner():
    new_inter = interface()
    new_inter.start()


# TODO, improve button design, add colors
# if __name__ == '__main__':
#     interface_runner()
