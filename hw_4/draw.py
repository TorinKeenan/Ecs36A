import sys, math


class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def rotate_point(self, angle):
        angle = math.radians(angle)
        sin_angle = math.sin(angle)
        cos_angle = math.cos(angle)
        temp_x = self.x
        self.x = self.x * cos_angle - self.y * sin_angle
        self.y = temp_x * sin_angle + self.y * cos_angle

    def scale_point(self, scale):
        self.x *= scale
        self.y *= scale

    def translate_point(self, x, y):
        self.x += x
        self.y += y


def rotate_points(points, angle):
    for i in range(len(points)):
        points[i].rotate(angle)


class Expression:
    def __init__(self, token):
        self.operation = token[:token.find(' ')]
        self.param_values = token[token.find(' ') + 1:].split()

    def filter_ngon(self):
        sides = {'tri': 3, 'filledtri': 3, 'square': 4, 'filledsquare': 4,
                 'penta': 5, 'filledpenta': 5, 'hexa': 6, 'filledhexa': 6}
        if self.operation in sides:

            self.param_values.append(sides[self.operation])
            if 'filled' in self.operation:
                self.operation = 'filledngon'
            else:
                self.operation = 'ngon'

    def process_param(self):
        for i in range(len(self.param_values)):
            self.param_values[i] = float(self.param_values[i])


class Drawable:
    def __init__(self, drawn):
        self.points = []
        self.drawn = drawn

    def rotate(self, angle):
        for point in self.points:
            point.rotate_point(angle)

    def translate(self, x, y):
        for point in self.points:
            point.translate_point(x, y)

    def scale(self, scalar):
        for point in self.points:
            point.scale_point(scalar)

    def draw(self):
        sys.stdout.write(str(self.points[0].x) + ' ' + str(self.points[0].y) + ' moveto' + '\n')
        for i in range(1, len(self.points)):
            sys.stdout.write(str(self.points[i].x) + ' ' + str(self.points[i].y) + ' lineto' + '\n')
        if self.drawn:
            sys.stdout.write('stroke' + '\n')
        else:
            sys.stdout.write('fill' + '\n')

    def apply_transforms(self):
        while len(stack) > 0:
            transform = stack.pop()
            if transform.operation == 'scale':
                shape.scale(transform.param_values[0])
            elif transform.operation == 'translate':
                shape.translate(transform.param_values[0],
                                transform.param_values[1])
            else:
                shape.rotate(transform.param_values[0])


class Line(Drawable):
    def __init__(self, param):
        Drawable.__init__(self, True)
        self.points = [Point(param[0], param[1]), Point(param[2], param[3])]


def rect_points(param):
    return [Point(param[0], param[1]),
            Point(param[0] + param[2], param[1]),
            Point(param[0] + param[2], param[1] + param[3]),
            Point(param[0], param[1] + param[3]),
            Point(param[0], param[1])]


class Rect(Drawable):
    def __init__(self, param):
        Drawable.__init__(self, True)
        # x=0 y=1 w=2 h=3
        self.points = rect_points(param)


class FilledRect(Drawable):
    def __init__(self, param):
        Drawable.__init__(self, False)
        # x=0 y=1 w=2 h=3
        self.points = rect_points(param)


def ngon_points(param):
    # x = 0, y =1 , r = 2, sides = 3
    result = []
    for i in range(int(param[3])):
        point = Point(param[2], 0)
        point.rotate_point(360 * i / param[3])
        point.translate_point(param[0], param[1])
        result.append(point)
    result.append(Point(param[0] + param[2], param[1]))
    return result


def sector_points(param):
    # x = 0, y =1 , r = 2, b = 3, e = 4
    result = []
    result.append(Point(param[0], param[1]))
    point_1 = Point(param[0] + param[2], param[1])
    point_1.rotate_point(param[3])
    point_2 = Point(param[0] + param[2], param[1])
    point_2.rotate_point(param[4])
    result.append(point_1)
    result.append(point_2)
    return result


class Ngon(Drawable):
    def __init__(self, param):
        Drawable.__init__(self, True)
        self.points = ngon_points(param)


class Filled_Ngon(Drawable):
    def __init__(self, param):
        Drawable.__init__(self, False)
        self.points = ngon_points(param)


class Sector(Drawable):
    def __init__(self, param, drawable):
        self.param = param
        self.points = sector_points(param)
        self.drawable = drawable

    def draw(self):
        sys.stdout.write(str(self.points[0].x) + ' ' + str(self.points[0].y) + ' ' + 'moveto' + '\n')
        sys.stdout.write(str(self.points[1].x) + ' ' + str(self.points[1].y) + ' ' + 'lineto' + '\n')
        sys.stdout.write(str(self.param[0]) + ' ' + str(self.param[1]) + ' ' +
                         str(self.param[2]) + ' ' + str(self.param[3]) + ' ' +
                         str(self.param[4]) + ' ' + 'arc' + '\n')
        sys.stdout.write(str(self.points[0].x) + ' ' + str(self.points[0].y) + ' ' + 'lineto' + '\n')
        if self.drawable:
            sys.stdout.write('stroke' + '\n')
        else:
            sys.stdout.write('fill' + '\n')


def parse_lines(input_arr):
    expression = ''
    for input_line in input_arr:
        input_line = input_line.replace('\t', '    ')
        if input_line != '\n':
            expression += input_line.strip()
            expression += ' '
    while '  ' in expression:
        expression = expression.replace('  ', ' ')
    expression = expression.replace(') (', ')(')
    expression = expression.replace('( ', '(')
    expression = expression.replace(' )', ')')
    expression = expression.strip()
    expression = expression[1:len(expression) - 1]
    expression = expression.strip()
    return expression.split(')(')


def inst_execute(command, param):
    if command == 'color':
        sys.stdout.write(param[0] + ' ' + param[1] + ' ' + param[2] + ' ' + 'setrgbcolor' + '\n')
    elif command == 'linewidth':
        sys.stdout.write(param[0] + ' setlinewidth' + '\n')


def create_shape(token):
    if token.operation == 'ngon':
        return Ngon(token.param_values)
    elif token.operation == 'filledngon':
        return Filled_Ngon(token.param_values)
    elif token.operation == 'line':
        return Line(token.param_values)
    elif token.operation == 'rect':
        return Rect(token.param_values)
    elif token.operation == 'filledrect':
        return FilledRect(token.param_values)
    elif token.operation == 'sector':
        return Sector(token.param_values,True)
    elif token.operation == 'filledsector':
        return Sector(token.param_values,False)



lines = sys.stdin.readlines()
operations = parse_lines(lines)
sys.stdout.write('%!PS-Adobe-3.0 EPSF-3.0' + '\n')
sys.stdout.write('%%BoundingBox: 0 0 1239 1752' + '\n')
stack = []
namespace = {}
drawable = {'ngon', 'filledngon', 'line', 'rect', 'filledrect','sector','filledsector'}
stackable = {'translate', 'rotate', 'scale'}
executeable = {'color', 'linewidth', ':='}

for operation in operations:
    token = Expression(operation)
    token.filter_ngon()
    token.process_param()
    if token.operation in stackable:
        stack.append(token)
    elif token.operation in executeable:
        inst_execute(token.operation, token.param_values)
    else:
        shape = create_shape(token)
        shape.apply_transforms()
        shape.draw()
sys.stdout.write('showpage' + '\n')
