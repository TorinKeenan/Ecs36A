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


def parseRectVals(expression):
    expression = expression[expression.find(' ') + 1:]
    return expression.split()


def line(point1, point2):
    sys.stdout.write(str(point1.x) + ' ' + str(point1.y) + ' moveto' + '\n')
    sys.stdout.write(str(point2.x) + ' ' + str(point2.y) + ' lineto' + '\n')
    sys.stdout.write('stroke' + '\n')


def parseRectParam(x, y, w, h):
    x = float(x)
    y = float(y)
    w = float(w)
    h = float(h)
    return [Point(x, y), Point(x + w, y), Point(x + w, y + h), Point(x, y + h)]


def rect(point1, point2, point3, point4):
    sys.stdout.write(str(point1.x) + ' ' + str(point1.y) + ' moveto' + '\n')
    sys.stdout.write(str(point2.x) + ' ' + str(point2.y) + ' lineto' + '\n')
    sys.stdout.write(str(point3.x) + ' ' + str(point3.y) + ' lineto' + '\n')
    sys.stdout.write(str(point4.x) + ' ' + str(point4.y) + ' lineto' + '\n')
    sys.stdout.write(str(point1.x) + ' ' + str(point1.y) + ' lineto' + '\n')
    sys.stdout.write('stroke' + '\n')


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


for inputline in lines:
    inputline = inputline.replace('\t','    ')
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
    if command == 'color':
        values = parsecolor(operation)
        color(values[0], values[1], values[2])
    elif command == 'linewidth':
        linewidth(operation[operation.find(' ')+1:])
    elif command == 'rotate' or command == 'translate':
        stack.append(operation)
    elif len(stack) == 0:
        if command == 'line':
            points = parseLinePoints(operation)
            line(points[0], points[1])
        elif command == 'rect':
            rectParam = parseRectVals(operation)
            points = parseRectParam(rectParam[0], rectParam[1], rectParam[2], rectParam[3])
            rect(points[0],points[1],points[2],points[3])
    else:
        if command == 'line':
            points = parseLinePoints(operation)
            while len(stack) > 0 :
                edit = stack.pop()
                command = parseCommand(operation)
                if parseCommand(edit) == 'translate':
                    translations = parseTranslate(edit)
                    points = translate(float(translations[0]), float(translations[1]), points)
                else:
                    points = rotate(points, float(edit[7:]))

            line(points[0], points[1])
        else:
            rectParam = parseRectVals(operation)
            points = parseRectParam(rectParam[0], rectParam[1], rectParam[2], rectParam[3])
            while len(stack) > 0:
                edit = stack.pop()

                if parseCommand(edit) == 'translate':
                    translations = parseTranslate(edit)
                    points = translate(float(translations[0]), float(translations[1]),points)
                else:
                    points = rotate(points, float(edit[7:]))
            rect(points[0], points[1], points[2], points[3])



sys.stdout.write('showpage'+'\n')
