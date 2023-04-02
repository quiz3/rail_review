"""TODO... add module docstring
"""
import pygame
from dataset import dataset
from graph import TransitSystem
from sys import path

path.insert(1, './')

POSSIBLE_IDS = ['delhi', 'seoul', 'singapore', 'tokyo', 'toronto']
X_PADDING, Y_PADDING = 25, 25
SCREEN_X, SCREEN_Y = 1450, 720

graphAR_X = 1000
graphAR_Y = (700 / 1200) * graphAR_X

ALL_TS = {}

for ID in POSSIBLE_IDS:
    ts = TransitSystem(ID)
    ts.load_from_cache_dict()
    ts.load_from_json('./datasets/dataset/' + ID + '.json')
    ALL_TS[ID] = ts

POSSIBLE_IDS.sort(key=lambda x: ALL_TS[x].transit_info_dict['transit_score'])


class interface:
    """TODO: add docstring
    """
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
        """TODO: add docstring
        """
        if '.ttf' in self.font:
            font = pygame.font.Font(self.font, 6 * multi)
        else:
            font = pygame.font.SysFont(self.font, self.font != 'freesansbold' and 6 * multi or 8 * multi)
        # font = pygame.font.Font(self.font + '.ttf', 8*multi)
        text = font.render(ln, True, (255, 255, 255), (0, 0, 0))

        textRect = text.get_rect()
        textRect.center = (pos[0], pos[1] - Y_PADDING)

        scrn.blit(text, textRect)

    def get_xrange(self) -> tuple[float, float]:
        """TODO: add docstring"""
        x_vals = self.ds.x_vals
        return (min(x_vals), max(x_vals))

    def get_yrange(self) -> tuple[float, float]:
        """TODO: add docstring"""
        y_vals = self.ds.y_vals
        return (min(y_vals), max(y_vals))

    def scale_x(self, num: float) -> float:
        """TODO: add docstring"""
        min_x, max_x = self.get_xrange()
        return (num - min_x) / (max_x - min_x) * graphAR_X

    def scale_y(self, num: float) -> float:
        """TODO: add docstring"""
        min_y, max_y = self.get_yrange()
        return (num - min_y) / (max_y - min_y) * (-graphAR_Y) + graphAR_Y

    def probe_distcalc(self):
        """TODO: add docstring"""
        if self.station1 == '' or self.station2 == '':
            return None

        self.calcdist = self.ts.find_shortest_path(self.station1, self.station2)[0]

    def drawDataset(self, m1clicked):
        """TODO: add docstring"""
        mouse = pygame.mouse.get_pos()
        hovered = None

        all_stations = self.ts.get_stations()
        todraw = []

        for station_name in self.ts.get_stations():
            station_info = all_stations[station_name]
            x, y = station_info.x, station_info.y

            col = (0, 0, 0)

            rect1 = pygame.draw.rect(self.screen, col,
                                     (self.scale_x(x) + X_PADDING - 2, self.scale_y(y) + Y_PADDING - 2, 8, 8))

            if station_name in {self.station1, self.station2}:
                todraw.append((self.scale_x(x) + X_PADDING - 6, self.scale_y(y) + Y_PADDING - 6, 16, 16))

            if rect1.collidepoint(mouse):
                hovered = (self.screen, (self.scale_x(x) + X_PADDING, self.scale_y(y) + Y_PADDING * 1.5), station_name)
                # self.onHover(self.screen, (self.scale_x(x) + X_PADDING, self.scale_y(y) + Y_PADDING*1.5), line_name)

                if m1clicked:
                    if self.station1 == '' and station_name != self.station2:
                        self.station1 = station_name
                        self.probe_distcalc()
                    elif self.station2 == '' and station_name != self.station1:
                        self.station2 = station_name
                        self.probe_distcalc()
                    else:
                        self.station1 = station_name
                        self.station2 = ''
                        self.calcdist = []
            elif self.drawLabels:
                self.onHover(self.screen, (self.scale_x(x) + X_PADDING, self.scale_y(y) + Y_PADDING * 1.5),
                             station_name, 2)

            for neighbour in station_info.neighbours:
                neighbour_info = self.ts.get_station_by_name(neighbour)
                new_x, new_y = neighbour_info.x, neighbour_info.y

                width = 1
                col = (0, 0, 0)
                if neighbour in self.calcdist and station_name in self.calcdist:
                    col = (255, 0, 0)
                    width = 4

                pygame.draw.line(self.screen, col,
                                 (self.scale_x(x) + X_PADDING, self.scale_y(y) + Y_PADDING),
                                 (self.scale_x(new_x) + X_PADDING, self.scale_y(new_y) + Y_PADDING), width)

        for coord in todraw:
            pygame.draw.rect(self.screen, (0, 0, 255), coord)
            pygame.draw.rect(self.screen, (255, 255, 255), (coord[0] + 4, coord[1] + 4, coord[2] / 2, coord[3] / 2))

        if hovered is not None:
            self.onHover(*hovered)

    def addButton(self, txt, pos, bg=(66, 133, 244), usefont=False):
        """TODO add docstring"""
        if usefont:
            if '.ttf' in self.font:
                smallfont = pygame.font.Font(self.font, 20)
            else:
                smallfont = pygame.font.SysFont(self.font, self.font != 'freesansbold' and 20 or 35)
        else:
            smallfont = pygame.font.SysFont('Corbel', 35)

        if bg == (66, 133, 244):
            text = smallfont.render(txt, True, (255, 255, 255), bg)
        else:
            text = smallfont.render(txt, True, (0, 0, 0), bg)

        rect2 = pygame.draw.rect(self.screen, bg, [pos[0] + 45, pos[1] - 10, text.get_width() + 10, 40])
        self.screen.blit(text, (pos[0] + 50, pos[1]))

        return rect2

    def start(self):
        """TODO: add docstring"""
        self.ds = dataset('./datasets/dataset/toronto.json')

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

                button = self.addButton(str(i + 1) + '. ' + buttonText,
                                        (initial_position[0], initial_position[1] + 45 * i))

                dsRects.append(button)

                if m1clicked and button.collidepoint(mouse):
                    if buttonText in 'tokyo':
                        self.font = 'ヒラキノ角コシックw1'
                    elif buttonText == 'seoul':
                        self.font = 'NanumSquareNeo-aLt.ttf'
                    else:
                        self.font = 'freesansbold'

                    self.station1 = ''
                    self.station2 = ''
                    self.calcdist = []

                    json_file = './datasets/dataset/' + str.lower(buttonText) + '.json'
                    self.ds.load_dataset(json_file)

                    self.ts = ALL_TS[str.lower(buttonText)]

            initial_position = (graphAR_X + 25, 600)

            self.addButton(f"City - {self.ts.transit_info_dict['city']}",
                           (initial_position[0], initial_position[1] - 45 * 5), (255, 255, 255))
            self.addButton(f"Transit Score - {round(self.ts.transit_info_dict['transit_score'] * 100, 3)}",
                           (initial_position[0], initial_position[1] - 45 * 4), (255, 255, 255))
            self.addButton(f"Number of Stations - {self.ts.transit_info_dict['total_num_stations']}",
                           (initial_position[0], initial_position[1] - 45 * 3), (255, 255, 255))
            self.addButton(f"Total unique pairs - {self.ts.transit_info_dict['total_paths']}",
                           (initial_position[0], initial_position[1] - 45 * 2), (255, 255, 255))
            self.addButton(f"Cumulative distance - {round(self.ts.transit_info_dict['total_distance'], 2)}",
                           (initial_position[0], initial_position[1] - 45 * 1), (255, 255, 255))
            self.addButton(f"Total edge length - {round(self.ts.transit_info_dict['total_edge_length'], 2)}",
                           (initial_position[0], initial_position[1] - 45 * 0), (255, 255, 255))

            sta1 = self.addButton('Station 1: ', (0, SCREEN_Y - 45), (255, 255, 255))
            sta2 = self.addButton('Station 2: ', (450, SCREEN_Y - 45), (255, 255, 255))

            self.addButton(self.station1, (0 + sta1.width, SCREEN_Y - 45), (255, 255, 255), usefont=True)
            self.addButton(self.station2, (450 + sta2.width, SCREEN_Y - 45), (255, 255, 255), usefont=True)

            changeLabels = self.addButton('Draw Labels', (graphAR_X + 25, SCREEN_Y - 45))
            if m1clicked and changeLabels.collidepoint(mouse):
                self.drawLabels = not self.drawLabels

            pygame.display.update()
            dt = clock.tick(60) / 1000

        pygame.quit()


def interface_runner():
    """TODO: add docstring"""
    new_inter = interface()
    new_inter.start()


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'max-line-length': 120,
        'extra-imports': ['pygame', 'dataset', 'sys', 'graph'],
        'allowed-io': [],
        'max-indented': 4,
        'disable': ['E9992', 'E9997']
    })
