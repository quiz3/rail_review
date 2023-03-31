import pygame
from dataset import dataset

from sys import path
path.insert(1, './')

from graph import TransitSystem

POSSIBLE_IDS = ['delhi', 'london', 'seoul', 'singapore', 'tokyo', 'toronto']
X_PADDING, Y_PADDING = 25, 25
SCREEN_X, SCREEN_Y = 1250, 900
ALL_TS = {}

for id in POSSIBLE_IDS:
    ts = TransitSystem(id)
    ts.load_from_json('./dataset/dataset/' + id + '.json')
    ALL_TS[id] = ts


class interface:
    screen: any
    ds: dataset
    running: bool
    station1: str
    station2: str
    calcdist: list
    font: str
    ts: TransitSystem
    drawLabels: bool

    def __init__(self) -> None:
        self.station1 = ''
        self.station2 = ''
        self.calcdist = []
        self.font = 'freesansbold'
        self.drawLabels = True

    def onHover(self, scrn, pos, ln, multi=3):
        if '.ttf' in self.font:
            font = pygame.font.Font(self.font, 8*multi)
        else:
            font = pygame.font.SysFont(self.font, 8*multi)
        # font = pygame.font.Font(self.font + '.ttf', 8*multi)
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
        return ((num - min_x) / (max_x - min_x) * 1200)

    def scale_y(self, num):
        min_y, max_y = self.get_yrange()
        return (num - min_y) / (max_y - min_y) * (-700) + 700

    def probe_distcalc(self):
        if self.station1 == '' or self.station2 == '':
            return

        self.calcdist = self.ts.find_shortest_path(self.station1, self.station2)[0]

    def drawDataset(self, m1clicked):
        mouse = pygame.mouse.get_pos()
        hovered = None

        for line_name in self.ds.loaded:
            line_data = self.ds.loaded[line_name]
            station_names = list(line_data.keys())
            prev_station_name = station_names[0]
            x, y = line_data[prev_station_name]["x"], line_data[prev_station_name]["y"]

            rect1 = pygame.draw.rect(self.screen, self.ds.cmap[line_name],
                                     (self.scale_x(x) + X_PADDING, self.scale_y(y) + Y_PADDING, 4, 4))

            if rect1.collidepoint(mouse):
                hovered = (self.screen, (self.scale_x(x) + X_PADDING, self.scale_y(y) + Y_PADDING*1.5), line_name)
                # self.onHover(self.screen, (self.scale_x(x) + X_PADDING, self.scale_y(y) + Y_PADDING*1.5), line_name)

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
            elif self.drawLabels:
                self.onHover(self.screen, (self.scale_x(x) + X_PADDING, self.scale_y(y) + Y_PADDING*1.5), line_name, 1)

            for station_name in station_names[1:]:
                x, y = line_data[station_name]["x"], line_data[station_name]["y"]

                prev_x, prev_y = line_data[prev_station_name]["x"], line_data[prev_station_name]["y"]

                rect2 = pygame.draw.rect(self.screen, self.ds.cmap[line_name],
                                         (self.scale_x(x) + X_PADDING, self.scale_y(y) + Y_PADDING, 4, 4))

                if rect2.collidepoint(mouse):
                    hovered = (self.screen, (self.scale_x(x) + X_PADDING, self.scale_y(y) + Y_PADDING*1.5), station_name)
                    # self.onHover(self.screen, (self.scale_x(x) + X_PADDING, self.scale_y(y) + Y_PADDING*1.5), station_name)

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
                elif self.drawLabels:
                    self.onHover(self.screen, (self.scale_x(x) + X_PADDING, self.scale_y(y) + Y_PADDING*1.5), station_name, 1)

                col = self.ds.cmap[line_name]
                width = 1
                if prev_station_name in self.calcdist and station_name in self.calcdist:
                    col = (255, 0, 0)
                    width = 4

                pygame.draw.line(self.screen, col,
                                 (self.scale_x(x) + X_PADDING, self.scale_y(y) + Y_PADDING),
                                 (self.scale_x(prev_x) + X_PADDING, self.scale_y(prev_y) + Y_PADDING), width)

                prev_station_name = station_name
        if hovered is not None:
            self.onHover(*hovered)

    def addButton(self, txt, pos):
        smallfont = pygame.font.SysFont('Corbel', 35)
        text = smallfont.render(txt, True, (255, 0, 0), (0, 255, 0))

        rect2 = pygame.draw.rect(self.screen, (0, 255, 0), [pos[0] + 45, pos[1] - 10, text.get_width() + 10, 40])
        self.screen.blit(text, (pos[0] + 50, pos[1]))

        return rect2

    def start(self):
        self.ds = dataset('./dataset/dataset/toronto.json')

        self.ts = ALL_TS['toronto']
        self.running = True
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y))
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

            initial_position = (50, 750)
            prev_margins = []
            for i in range(len(POSSIBLE_IDS)):
                buttonText = POSSIBLE_IDS[i]

                button = self.addButton(buttonText, (initial_position[0] + sum(prev_margins), initial_position[1]))

                prev_margins.append(button.width + 10)
                dsRects.append(button)

                if m1clicked and button.collidepoint(mouse):
                    if buttonText in 'tokyo':
                        self.font = 'ヒラキノ角コシックw1'
                    elif buttonText == 'seoul':
                        self.font = 'NanumSquareNeo-aLt.ttf'
                    else:
                        self.font = 'freesansbold'

                    json_file = './dataset/dataset/' + str.lower(buttonText) + '.json'
                    self.ds.load_dataset(json_file)

                    self.ts = ALL_TS[str.lower(buttonText)]

            self.addButton('Station 1: ' + self.station1, (50, 795))
            self.addButton('Station 2: ' + self.station2, (50, 840))

            changeLabels = self.addButton('Draw Labels', (800, 750))
            if m1clicked and changeLabels.collidepoint(mouse):
                self.drawLabels = not self.drawLabels

            pygame.display.update()
            dt = clock.tick(60) / 1000

        pygame.quit()


def interface_runner():
    new_inter = interface()
    new_inter.start()


# TODO, improve button design, add colors
if __name__ == '__main__':
    interface_runner()
