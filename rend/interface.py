import pygame
from dataset import dataset

from sys import path
path.insert(1, './')

from graph import TransitSystem

POSSIBLE_IDS = ['delhi', 'london', 'seoul', 'singapore', 'tokyo', 'toronto']
X_PADDING, Y_PADDING = 25, 25
SCREEN_X, SCREEN_Y = 1450, 720

graphAR_X = 1000
graphAR_Y = (700/1200) * graphAR_X

ALL_TS = {}

for id in POSSIBLE_IDS:
    ts = TransitSystem(id)
    ts.load_from_cache_dict()
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

    def onHover(self, scrn, pos, ln, multi=4):
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
        return ((num - min_x) / (max_x - min_x) * graphAR_X)

    def scale_y(self, num):
        min_y, max_y = self.get_yrange()
        return (num - min_y) / (max_y - min_y) * (-graphAR_Y) + graphAR_Y

    def probe_distcalc(self):
        if self.station1 == '' or self.station2 == '':
            return

        self.calcdist = self.ts.find_shortest_path(self.station1, self.station2)[0]

    def drawDataset(self, m1clicked):
        mouse = pygame.mouse.get_pos()
        hovered = None
        drawn_stations = []

        for line_name in self.ds.loaded:
            line_data = self.ds.loaded[line_name]
            station_names = list(line_data.keys())
            prev_station_name = station_names[0]
            x, y = line_data[prev_station_name]["x"], line_data[prev_station_name]["y"]

            if prev_station_name not in drawn_stations:
                rect1 = pygame.draw.rect(self.screen, self.ds.cmap[line_name],
                                        (self.scale_x(x) + X_PADDING, self.scale_y(y) + Y_PADDING, 8, 8))

                if rect1.collidepoint(mouse):
                    hovered = (self.screen, (self.scale_x(x) + X_PADDING, self.scale_y(y) + Y_PADDING*1.5), prev_station_name)
                    # self.onHover(self.screen, (self.scale_x(x) + X_PADDING, self.scale_y(y) + Y_PADDING*1.5), line_name)

                    if m1clicked:
                        if self.station1 == '':
                            self.station1 = prev_station_name
                            self.probe_distcalc()
                        elif self.station2 == '':
                            self.station2 = prev_station_name
                            self.probe_distcalc()
                        else:
                            self.station1 = prev_station_name
                            self.station2 = ''
                            self.calcdist = []
                elif self.drawLabels:
                    self.onHover(self.screen, (self.scale_x(x) + X_PADDING, self.scale_y(y) + Y_PADDING*1.5), prev_station_name, 2)

                drawn_stations.append(prev_station_name)

            for station_name in station_names[1:]:
                if station_name in drawn_stations:
                    continue
                drawn_stations.append(station_name)
                x, y = line_data[station_name]["x"], line_data[station_name]["y"]

                prev_x, prev_y = line_data[prev_station_name]["x"], line_data[prev_station_name]["y"]

                rect2 = pygame.draw.rect(self.screen, self.ds.cmap[line_name],
                                         (self.scale_x(x) + X_PADDING, self.scale_y(y) + Y_PADDING, 8, 8))

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
                    self.onHover(self.screen, (self.scale_x(x) + X_PADDING, self.scale_y(y) + Y_PADDING*1.5), station_name, 2)

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

    def addButton(self, txt, pos, bg=(0, 255, 0)):
        smallfont = pygame.font.SysFont('Corbel', 35)
        text = smallfont.render(txt, True, (255, 0, 0), bg)

        rect2 = pygame.draw.rect(self.screen, bg, [pos[0] + 45, pos[1] - 10, text.get_width() + 10, 40])
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

            initial_position = (graphAR_X + 25, 50)
            for i in range(len(POSSIBLE_IDS)):
                buttonText = POSSIBLE_IDS[i]

                button = self.addButton(buttonText, (initial_position[0], initial_position[1] + 45 * i))

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

            initial_position = (graphAR_X + 25, 600)
            # i1 = 0
            # for metric in self.ts.transit_info_dict:
            #     self.addButton(metric + ' ' + str(self.ts.transit_info_dict[metric]), (initial_position[0], initial_position[1] - 45 * i1), (255, 255, 255))
            #     i1 += 1
            self.addButton(f"City - {self.ts.transit_info_dict['city']}", (initial_position[0], initial_position[1] - 45 * 5), (255, 255, 255))
            self.addButton(f"Transit Score - {round(self.ts.transit_info_dict['transit_score'] * 100, 3)}", (initial_position[0], initial_position[1] - 45 * 4), (255, 255, 255))
            self.addButton(f"Number of Stations - {self.ts.transit_info_dict['total_num_stations']}", (initial_position[0], initial_position[1] - 45 * 3), (255, 255, 255))
            self.addButton(f"Total possible paths - {self.ts.transit_info_dict['total_paths']}", (initial_position[0], initial_position[1] - 45 * 2), (255, 255, 255))
            self.addButton(f"Cumulative distance - {round(self.ts.transit_info_dict['total_distance'], 2)}", (initial_position[0], initial_position[1] - 45 * 1), (255, 255, 255))
            self.addButton(f"Total edge length - {round(self.ts.transit_info_dict['total_edge_length'], 2)}", (initial_position[0], initial_position[1] - 45 * 0), (255, 255, 255))

            self.addButton('Station 1: ' + self.station1, (50, SCREEN_Y - 45), (255, 255, 255))
            self.addButton('Station 2: ' + self.station2, (500, SCREEN_Y - 45), (255, 255, 255))

            changeLabels = self.addButton('Draw Labels', (graphAR_X + 25, SCREEN_Y - 45))
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
