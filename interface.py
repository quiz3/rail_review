"""CSC111 Winter 2023 Course Project - Rail Review!

- This file contains a class representing a graphical user interface (GUI) .
- This file contains the _Station and TransitSystem classes, which correspond to the _Node and Graph ADTs we have looked
  at during this course.
"""
import pygame
from dataset import Dataset
from graph import TransitSystem

POSSIBLE_IDS = ['delhi', 'seoul', 'singapore', 'tokyo', 'toronto']
X_PADDING, Y_PADDING = 25, 25
SCREEN_X, SCREEN_Y = 1450, 720

GRAPHAR_X = 1000
GRAPHAR_Y = (700 / 1200) * GRAPHAR_X

ALL_TS = {}


class Interface:
    """Represent a Graphical User Interface (GUI) to display transit system analysis results and to illustrate the
    layout of the analyzed transit systems and potential paths therein.

    Instance Attributes:
      - screen: the screen of a pygame instance
      - ds: a Dataset object for the current transit system
      - stations: a list containing the name of two stations
      - calcdist
      - font: a string representing which font to use for the current transit system
      - ts: the transit system drawn by the interface
      - drawlabels: a boolean representing whether labels should be drawn
    """
    screen: pygame.surface
    ds: Dataset
    stations: list[str, str]
    calcdist: list[str]
    font: str
    ts: TransitSystem
    drawlabels: bool

    def __init__(self) -> None:
        self.calcdist = []
        self.font = 'freesansbold'
        self.stations = ['', '']
        self.drawlabels = True

    def onhover(self, pos: tuple[float, float], ln: str, multi: int = 4) -> None:
        """Handle event when cursor hovers over a station.
        """
        if '.ttf' in self.font:
            font = pygame.font.Font(self.font, 6 * multi)
        else:
            font = pygame.font.SysFont(self.font, self.font != 'freesansbold' and 6 * multi or 8 * multi)

        text = font.render(ln, True, (255, 255, 255), (0, 0, 0))

        textrect = text.get_rect()
        textrect.center = (pos[0], pos[1] - Y_PADDING)

        self.screen.blit(text, textrect)
        return None

    def get_xrange(self) -> tuple[float, float]:
        """Return lower and upper bounds of station x-values."""
        x_vals = self.ds.x_vals
        return (min(x_vals), max(x_vals))

    def get_yrange(self) -> tuple[float, float]:
        """Return lower and upper bounds of station y-values."""
        y_vals = self.ds.y_vals
        return (min(y_vals), max(y_vals))

    def scale_x(self, num: float) -> float:
        """Given x-value <num>, return scaled x-value."""
        min_x, max_x = self.get_xrange()
        return (num - min_x) / (max_x - min_x) * GRAPHAR_X

    def scale_y(self, num: float) -> float:
        """Given y-value <num>, return scaled y-value."""
        min_y, max_y = self.get_yrange()
        return (num - min_y) / (max_y - min_y) * (-GRAPHAR_Y) + GRAPHAR_Y

    def probe_distcalc(self) -> None:
        """Update attribute <calcdist>."""
        if self.stations[0] == '' or self.stations[1] == '':
            return None

        self.calcdist = self.ts.find_shortest_path(self.stations[0], self.stations[1])[0]
        return None

    def drawdataset(self, m1clicked: bool) -> None:
        """Draw the transit system <self.ts>.
        """
        hovered = None

        todraw = []

        for station_name in self.ts.get_stations():
            station_info = self.ts.get_station_by_name(station_name)
            x, y = station_info.x, station_info.y

            rect1 = pygame.draw.rect(self.screen, (0, 0, 0),
                                     (self.scale_x(x) + X_PADDING - 2, self.scale_y(y) + Y_PADDING - 2, 8, 8))

            if station_name in self.stations:
                todraw.append((self.scale_x(x) + X_PADDING - 6, self.scale_y(y) + Y_PADDING - 6, 16, 16))

            if rect1.collidepoint(pygame.mouse.get_pos()):
                hovered = ((self.scale_x(x) + X_PADDING, self.scale_y(y) + Y_PADDING * 1.5), station_name)

                if m1clicked:
                    if self.stations[0] == '' and station_name != self.stations[1]:
                        self.stations[0] = station_name
                        self.probe_distcalc()
                    elif self.stations[1] == '' and station_name != self.stations[0]:
                        self.stations[1] = station_name
                        self.probe_distcalc()
                    else:
                        self.stations[0] = station_name
                        self.stations[1] = ''
                        self.calcdist = []
            elif self.drawlabels:
                self.onhover((self.scale_x(x) + X_PADDING, self.scale_y(y) + Y_PADDING * 1.5),
                             station_name, 2)

            for neighbour in station_info.neighbours:
                neighbour_info = self.ts.get_station_by_name(neighbour)
                new_x, new_y = neighbour_info.x, neighbour_info.y

                is_path = neighbour in self.calcdist and station_name in self.calcdist

                pygame.draw.line(self.screen, is_path and (255, 0, 0) or (0, 0, 0),
                                 (self.scale_x(x) + X_PADDING, self.scale_y(y) + Y_PADDING),
                                 (self.scale_x(new_x) + X_PADDING, self.scale_y(new_y) + Y_PADDING), is_path and 4 or 1)

        for coord in todraw:
            pygame.draw.rect(self.screen, (0, 0, 255), coord)
            pygame.draw.rect(self.screen, (255, 255, 255), (coord[0] + 4, coord[1] + 4, coord[2] / 2, coord[3] / 2))

        if hovered is not None:
            self.onhover(*hovered)

    def addbutton(self, txt: str, pos: tuple[int, int],
                  bg: tuple[int, int, int] = (66, 133, 244), usefont: bool = False) -> pygame.Rect:
        """Create button according to given parameters and add it to <self.screen>.

        Implementation notes:
          - Return the button
        """
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

    def start(self) -> None:
        """Draw the GUI to <self.screen> for the first time.
        """
        self.ds = Dataset('./datasets/dataset/toronto.json')

        self.ts = ALL_TS['toronto']
        running = True
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y))

        while running:
            m1clicked = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONUP:
                    m1clicked = True

            self.screen.fill("white")
            mouse = pygame.mouse.get_pos()

            self.drawdataset(m1clicked)

            ds_rects = []

            initial_position = (GRAPHAR_X + 25, 50)
            for i in range(len(POSSIBLE_IDS)):
                buttontext = POSSIBLE_IDS[i]

                button = self.addbutton(str(i + 1) + '. ' + buttontext,
                                        (initial_position[0], initial_position[1] + 45 * i))

                ds_rects.append(button)

                if m1clicked and button.collidepoint(mouse):
                    if buttontext in 'tokyo':
                        self.font = 'ヒラキノ角コシックw1'
                    elif buttontext == 'seoul':
                        self.font = 'NanumSquareNeo-aLt.ttf'
                    else:
                        self.font = 'freesansbold'

                    self.stations[0] = ''
                    self.stations[1] = ''
                    self.calcdist = []

                    json_file = './datasets/dataset/' + str.lower(buttontext) + '.json'
                    self.ds.load_dataset(json_file)

                    self.ts = ALL_TS[str.lower(buttontext)]

            initial_position = (GRAPHAR_X + 25, 600)

            self.addbutton(f"City - {self.ts.transit_info_dict['city']}",
                           (initial_position[0], initial_position[1] - 45 * 5), (255, 255, 255))
            self.addbutton(f"Transit Score - {round(self.ts.transit_info_dict['transit_score'] * 100, 3)}",
                           (initial_position[0], initial_position[1] - 45 * 4), (255, 255, 255))
            self.addbutton(f"Number of Stations - {self.ts.transit_info_dict['total_num_stations']}",
                           (initial_position[0], initial_position[1] - 45 * 3), (255, 255, 255))
            self.addbutton(f"Total unique pairs - {self.ts.transit_info_dict['total_paths']}",
                           (initial_position[0], initial_position[1] - 45 * 2), (255, 255, 255))
            self.addbutton(f"Cumulative distance - {round(self.ts.transit_info_dict['total_distance'], 2)}",
                           (initial_position[0], initial_position[1] - 45 * 1), (255, 255, 255))
            self.addbutton(f"Total edge length - {round(self.ts.transit_info_dict['total_edge_length'], 2)}",
                           (initial_position[0], initial_position[1] - 45 * 0), (255, 255, 255))

            sta1 = self.addbutton('Station 1: ', (0, SCREEN_Y - 45), (255, 255, 255))
            sta2 = self.addbutton('Station 2: ', (450, SCREEN_Y - 45), (255, 255, 255))

            self.addbutton(self.stations[0], (0 + sta1.width, SCREEN_Y - 45), (255, 255, 255), usefont=True)
            self.addbutton(self.stations[1], (450 + sta2.width, SCREEN_Y - 45), (255, 255, 255), usefont=True)

            changelabels = self.addbutton('Draw Labels', (GRAPHAR_X + 25, SCREEN_Y - 45))
            if m1clicked and changelabels.collidepoint(mouse):
                self.drawlabels = not self.drawlabels

            pygame.display.update()

        pygame.quit()


def interface_runner() -> None:
    """Run the GUI defined above using our train station data."""
    for ID in POSSIBLE_IDS:
        ts = TransitSystem(ID)
        ts.load_from_cache_dict()
        ts.load_from_json('./datasets/dataset/' + ID + '.json')
        ALL_TS[ID] = ts

    POSSIBLE_IDS.sort(key=lambda x: ALL_TS[x].transit_info_dict['transit_score'])

    new_inter = Interface()
    new_inter.start()


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'max-line-length': 120,
        'extra-imports': ['pygame', 'dataset', 'graph'],
        'allowed-io': [],
        'max-nested': 4,
        'disable': ['no-member']  # aka. E1101 (python-TA fails to properly understand pygame)
    })
