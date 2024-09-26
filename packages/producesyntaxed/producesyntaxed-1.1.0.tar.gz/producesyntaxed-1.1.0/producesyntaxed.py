import sys

RED = '\033[38;5;203m'
ORANGE = '\033[38;5;208m'
GREEN = '\033[38;5;120m'
YELLOW = '\033[38;5;226m'
BLUE = '\033[38;5;117m' #dark-aqua sort of colour
BLUE2 = '\033[96m' #darker blue

#This doesn't really need to be part of the ESDExt so it's here now
def producesyntaxed(text, color, useSpace=True, newLine=True):
    match color:
        case 'red':
            colour = RED
        case 'orange':
            colour = ORANGE
        case 'green':
            colour = GREEN
        case 'yellow':
            colour = YELLOW
        case 'blue':
            colour = BLUE
        case 'blue2':
            colour = BLUE2
        case _:
            colour = Exception('Invalid colour')
    if useSpace and newLine:
        sys.stdout.write(colour + text + '\033[0m' + ' \n')
    elif useSpace:
        sys.stdout.write(colour + text + '\033[0m' + ' ')
    elif newLine:
        sys.stdout.write(colour + text + '\033[0m' + '\n')
    else:
        sys.stdout.write(colour + text + '\033[0m')
