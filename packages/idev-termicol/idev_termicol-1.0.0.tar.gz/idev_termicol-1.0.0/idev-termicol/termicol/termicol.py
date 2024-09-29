#Imports
from re import findall as refindall




#Variables
__Colors = {
    'white' : (255, 255, 255),
    'grey' : (125, 125, 125),
    'black' : (0, 0, 0),
    'red' : (200, 0, 0),
    'green' : (0, 200, 0),
    'blue': (0, 0, 200),
    'purple': (200, 0, 200),
    'yellow' : (200, 200, 0),
    'orange' : (200, 100, 0),

    'brightred' : (255, 0, 0),
    'brightgreen' : (0, 255, 0),
    'brightblue': (0, 0, 255),
    'brightpurple': (255, 0, 255),
    'brightyellow' : (255, 255, 0),
    'brightorange' : (255, 175, 0),

    'lightgrey' : (200, 200, 200),
    'lightred' : (200, 100, 100),
    'lightgreen' : (100, 200, 100),
    'lightblue': (100, 100, 200),
    'lightpurple': (200, 100, 200),
    'lightyellow' : (200, 200, 100),
    'lightorange' : (200, 150, 100),

    'darkgrey' : (10, 10, 10),
    'darkred' : (100, 0, 0),
    'darkgreen' : (0, 100, 0),
    'darkblue': (0, 0, 100),
    'darkpurple': (100, 0, 100),
    'darkyellow' : (100, 100, 0),
    'darkorange' : (100, 50, 0),
}

__Decorations = {
    'bold' : '1',
    'italic' : '3',
    'underline' : '4',
    'inverted' : '7',
    'doubleunderline' : '21'
}

__Codes = {
    'textcolor' : ['<t', '<textcolor'],
    'backgroundcolor' : ['<b', '<bgcolor', '<backgroundcolor'],
    'decorations' : ['<d', '<deco', '<decorations']
}






#Private Functions
def __validateRGB(rgb: tuple, content: str) -> None:
    if type(rgb) != tuple: raise SystemExit(f'The rgb value "{rgb}" is not a tuple at "{content}".')
    if len(rgb) < 3: raise SystemExit(f'The rgb value "{rgb}" does not contain all needed values at "{content}".')
    if len(rgb) > 3: raise SystemExit(f'The rgb value "{rgb}" contains too many values at "{content}".')
    if any([True for i in rgb if not type(i) is int]): raise SystemExit(f'The rgb value "{rgb}" contains a non integer value at "{content}".')
    if any([True for i in rgb if i < 0 or i > 255]): raise SystemExit(f'The rgb value "{rgb}" contains a value that is out of bounds for an rgb value at "{content}".')



def __validateDecoration(deco: str, content: str) -> None:
    global __Decorations
    if deco not in __Decorations: raise SystemExit(f'The decoration {deco} provided is not a valid decoration at "{content}".')



def __createColor(rgb: tuple, content: str) -> str:
    __validateRGB(rgb, content)
    red = str(rgb[0])
    green = str(rgb[1])
    blue = str(rgb[2])

    return red + ';' + green + ';' + blue



def __constructEscapeString(textColor: str, backgroundColor: str = '', decorations: list  = []) -> str:
    escapeString = '\033[38;2;' + textColor
    if backgroundColor: escapeString += ';48;2;' + backgroundColor
    for decoration in decorations: escapeString += ';' + decoration
    return escapeString + 'm'



def __mergeList(a: list, b: list):
    newlist = []
    for i in range(min(len(a), len(b))): newlist += [a[i], b[i]]
    if len(a) < len(b): return newlist + b[min(len(a), len(b)):]
    return newlist + a[min(len(a), len(b)):]



def __parseContent(content: str):
    if not content.endswith('<r>'): content += '<r>'
    codes = [f'<{i}>' for i in refindall(r'\<(.*?)\>', content)]
    if codes: text = refindall(r'\>(.*?)\<', content)
    mergedList = __mergeList(codes, text)
    while '' in mergedList: mergedList.remove('')
    return mergedList



def __convertParsedContent(content: list):
    global __Codes
    global __Colors

    textColor = ''
    bgColor = ''
    decorations = []

    newcontent = []
    for i in range(len(content)):
        if '<r' in content[i]:
            if content[i] == '<r>':
                textColor = ''
                bgColor = ''
                decorations = []
            else:
                reset = content[i].split('=')[1].replace('>','')
                if 't' in reset: textColor = ''
                if 'b' in reset: bgColor = ''
                if 'd' in reset: decorations = []
            newcontent.append('\033[0m')

        elif any([True for code in __Codes['textcolor'] if code in content[i]]):
            color = content[i].split('=')[1].replace('>','')
            if color in __Colors: textColor = __createColor(__Colors[color], content[i])
            else:
                color = color.split(',')
                try: color = tuple([int(i) for i in color])
                except Exception as exception: raise SystemExit(f'{exception}\n\n"{content[i]}" Has caused this issue with an invalid value being passed.')
                textColor = __createColor(color, content[i])
        
        elif any(True for code in __Codes['backgroundcolor'] if code in content[i]):
            color = content[i].split('=')[1].replace('>','')
            if color in __Colors: bgColor = __createColor(__Colors[color], content[i])
            else:
                color = color.split(',')
                try: color = tuple([int(i) for i in color])
                except Exception as exception: raise SystemExit(f'{exception}\n\n"{content[i]}" Has caused this issue with an invalid value being passed.')
                bgColor = __createColor(color, content[i])

        elif any(True for code in __Codes['decorations'] if code in content[i]):
            deco = content[i].split('=')[1].replace('>','')
            if ',' in deco: deco.split(',')
            else: deco = [deco]
            for d in deco: __validateDecoration(d, content[i])
            decorations = [__Decorations[d] for d in deco]
        
        else:
            newcontent.append(__constructEscapeString(textColor, bgColor, decorations))
            newcontent.append(content[i])
    
    return ''.join(newcontent)






#Public Functions
def showColorList() -> None:
    '''
    Prints off list of valid arguments for color.
    '''
    global __Colors
    for color in __Colors: print(color)



def showDecorationList() -> None:
    '''
    Prints off list of valid arguments for decoration.
    '''
    global __Decorations
    for decoration in __Decorations: print(decoration)






#Primary Function
def tprint(content: str, end = '\n') -> None:
    '''
    Sends content to python's print function after additional parsing and reconstructing.
    '''
    print(__convertParsedContent(__parseContent(content)), end = end)