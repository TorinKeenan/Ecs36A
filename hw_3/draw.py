import sys, math

lines = sys.stdin.readlines()
sys.stdout.write('%!PS-Adobe-3.1' + '\n')
expression = ''
stack = []


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def parseCommand(expression):
    return expression[:expression.find(' ')]


def parseLinePoints(expression):
    expression = expression[expression.find(' ') + 1:]
    rawval = expression.split()
    for i in range(len(rawval)):
        rawval[i] = float(rawval[i])
    return [Point(rawval[0], rawval[1]), Point(rawval[2], rawval[3])]


def parse4Vals(expression):
    expression = expression[expression.find(' ') + 1:]
    return expression.split()


def line(point1, point2):
    sys.stdout.write(str(point1.x) + ' ' + str(point1.y) + ' moveto' + '\n')
    sys.stdout.write(str(point2.x) + ' ' + str(point2.y) + ' lineto' + '\n')
    sys.stdout.write('stroke' + '\n')


def drawPoints(points):
    sys.stdout.write(str(points[0].x) + ' ' + str(points[0].y) + ' moveto' + '\n')
    for i in range(1, len(points)):
        sys.stdout.write(str(points[i].x) + ' ' + str(points[i].y) + ' lineto' + '\n')
    sys.stdout.write('stroke' + '\n')


def fillPoints(points):
    sys.stdout.write(str(points[0].x) + ' ' + str(points[0].y) + ' moveto' + '\n')
    for i in range(1, len(points)):
        sys.stdout.write(str(points[i].x) + ' ' + str(points[i].y) + ' lineto' + '\n')
    sys.stdout.write('fill' + '\n')


def parseRectParam(x, y, w, h):
    x = float(x)
    y = float(y)
    w = float(w)
    h = float(h)
    return [Point(x, y), Point(x + w, y), Point(x + w, y + h), Point(x, y + h), Point(x, y)]


def translate(x, y, points):
    translatedPoints = []
    for point in points:
        translatedPoints.append(Point(point.x + x, point.y + y))
    return translatedPoints


def parseTranslate(word):
    fragments = word.split()
    return fragments[1:]


def rotate(points, angle):
    rotatedPoints = []
    for point in points:
        rotatedPoints.append(rotatePoint(point, angle))
    return rotatedPoints


def rotatePoint(point, angle):
    angle = math.radians(angle)
    x = point.x
    point.x = ((math.cos(angle) * point.x) - (math.sin(angle) * point.y))
    point.y = x * math.sin(angle) + point.y * math.cos(angle)
    return point


def color(r, g, b):
    sys.stdout.write(r + ' ' + g + ' ' + b + ' ' + 'setrgbcolor' + '\n')


def parsecolor(expression):
    return expression[expression.find(' ') + 1:].split()


def linewidth(w):
    sys.stdout.write(w + ' setlinewidth' + '\n')


def ngonPoints(x, y, r, sides):
    x = float(x)
    y = float(y)
    r = float(r)
    sides = int(sides)
    points = []
    for i in range(sides):
        point = Point(r, 0)
        point = rotatePoint(point, 360 * i / sides)
        points.append(Point(x + point.x, y + point.y))
    points.append(Point(x + r, y))
    return points


def scale(scale, points):
    scaled = []
    for point in points:
        x = scale * float(point.x)
        y = scale * float(point.y)
        scaled.append(Point(x, y))
    return scaled


for inputline in lines:
    inputline = inputline.replace('\t', '    ')
    if inputline != '\n':
        expression += inputline.strip()
        expression += ' '
while '  ' in expression:
    expression = expression.replace('  ', ' ')
expression = expression.replace(') (', ')(')
expression = expression.replace('( ', '(')
expression = expression.replace(' )', ')')
expression = expression.strip()
expression = expression[1:len(expression) - 1]
expression = expression.strip()
operations = expression.split(')(')

for operation in operations:
    command = parseCommand(operation)
    command = parseCommand(operation)
    if command == 'tri' or command == 'filledtri':
        operation = operation.replace('filledtri', 'filledngon')
        operation = operation.replace('tri', 'ngon')
        command = command.replace('filledtri', 'filledngon')
        command = command.replace('tri', 'ngon')
        operation += ' 3'
    elif command == 'square' or command == 'filledsquare':
        operation = operation.replace('filledsquare', 'filledngon')
        operation = operation.replace('square', 'ngon')
        command = command.replace('filledsquare', 'filledngon')
        command = command.replace('square', 'ngon')
        operation += ' 4'
    elif command == 'penta' or command == 'filledpenta':
        operation = operation.replace('filledpenta', 'filledngon')
        operation = operation.replace('penta', 'ngon')
        command = command.replace('filledpenta', 'filledngon')
        command = command.replace('penta', 'ngon')
        operation += ' 5'
    elif command == 'hexa' or command == 'filledhexa':
        operation = operation.replace('filledhexa', 'filledngon')
        operation = operation.replace('hexa', 'ngon')
        command = command.replace('filledhexa', 'filledngon')
        command = command.replace('hexa', 'ngon')
        operation += ' 6'

    if command == 'color':
        values = parsecolor(operation)
        color(values[0], values[1], values[2])
    elif command == 'linewidth':
        linewidth(operation[operation.find(' ') + 1:])
    elif command == 'rotate' or command == 'translate' or command == 'scale':
        stack.append(operation)
    elif len(stack) == 0:
        if command == 'line':
            points = parseLinePoints(operation)
            line(points[0], points[1])
        elif command == 'rect':
            rectParam = parse4Vals(operation)
            points = parseRectParam(rectParam[0], rectParam[1], rectParam[2], rectParam[3])
            drawPoints(points)
        elif command == 'filledrect':
            rectParam = parse4Vals(operation)
            points = parseRectParam(rectParam[0], rectParam[1], rectParam[2], rectParam[3])
            fillPoints(points)

        elif command == 'ngon':
            params = parse4Vals(operation)
            points = ngonPoints(params[0], params[1], params[2], params[3])
            drawPoints(points)
        elif command == 'filledngon':
            params = parse4Vals(operation)
            points = ngonPoints(params[0], params[1], params[2], params[3])
            fillPoints(points)
    else:
        if command == 'line':
            points = parse4Vals(operation)
            points = [Point(float(points[0]), float(points[1])), Point(float(points[2]), float(points[3]))]
            while len(stack) > 0:
                edit = stack.pop()
                command = parseCommand(operation)
                if parseCommand(edit) == 'translate':
                    translations = parseTranslate(edit)
                    points = translate(float(translations[0]), float(translations[1]), points)
                elif parseCommand(edit) == 'rotate':

                    points = rotate(points, float(edit[7:]))
                else:

                    points = scale(float(edit[6:]), points)

            line(points[0], points[1])
        elif command == 'rect':
            rectParam = parse4Vals(operation)
            points = parseRectParam(rectParam[0], rectParam[1], rectParam[2], rectParam[3])
            while len(stack) > 0:
                edit = stack.pop()

                if parseCommand(edit) == 'translate':
                    translations = parseTranslate(edit)
                    points = translate(float(translations[0]), float(translations[1]), points)
                elif parseCommand(edit) == 'rotate':
                    points = rotate(points, float(edit[7:]))
                else:
                    points = scale(float(edit[6:]), points)
            drawPoints(points)
        elif command == 'filledrect':
            rectParam = parse4Vals(operation)
            points = parseRectParam(rectParam[0], rectParam[1], rectParam[2], rectParam[3])
            while len(stack) > 0:
                edit = stack.pop()

                if parseCommand(edit) == 'translate':
                    translations = parseTranslate(edit)
                    points = translate(float(translations[0]), float(translations[1]), points)
                elif parseCommand(edit) == 'rotate':
                    points = rotate(points, float(edit[7:]))
                else:
                    points = scale(float(edit[6:]), points)
            fillPoints(points)
        elif command == 'ngon':
            params = parse4Vals(operation)
            points = ngonPoints(params[0], params[1], params[2], params[3])
            while len(stack) > 0:
                edit = stack.pop()

                if parseCommand(edit) == 'translate':
                    translations = parseTranslate(edit)
                    points = translate(float(translations[0]), float(translations[1]), points)
                elif parseCommand(edit) == 'rotate':
                    points = rotate(points, float(edit[7:]))
                else:
                    points = scale(float(edit[6:]), points)
            drawPoints(points)
        elif command == 'filledngon':
            params = parse4Vals(operation)
            points = ngonPoints(params[0], params[1], params[2], params[3])
            while len(stack) > 0:
                edit = stack.pop()

                if parseCommand(edit) == 'translate':
                    translations = parseTranslate(edit)
                    points = translate(float(translations[0]), float(translations[1]), points)
                elif parseCommand(edit) == 'rotate':
                    points = rotate(points, float(edit[7:]))
                else:
                    points = scale(float(edit[6:]), points)
            fillPoints(points)

sys.stdout.write('showpage' + '\n')
