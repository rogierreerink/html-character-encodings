import html
import pprint
import json


html5Names = list(html.entities.html5.keys())
html5Values = list(html.entities.html5.values())


def printError(char: str, reason: str):
    charHex = '{0:#0{1}x}'.format(ord(char), 6)
    print(f'Failed to transcode character \'{char}\' ({charHex}): {reason}.')


def utf8HexStringToChar(input: str) -> str:
    byteString = input.split(' ')
    byteHexString = ['0x' + x for x in byteString]
    byteCharacter = bytes(int(x, 0) for x in byteHexString)
    return byteCharacter.decode('utf-8')


def find_indices(list: list[str], item: str) -> list[int]:
    indices = []
    for idx, value in enumerate(list):
        if value == item:
            indices.append(idx)
    return indices


def charToHtmlEntity(char: str) -> list[str]:
    entities = list()
    for idx in find_indices(html5Values, char):
        entities.append('&' + html5Names[idx])
    entities.append(char
                    .encode('ascii', 'xmlcharrefreplace')
                    .decode('utf-8'))
    if len(entities) == 0:
        printError(char, 'has no matching HTML entity')
    return entities


def parseCharacterFile(path: str) -> list[dict]:
    file = open(path)
    chars = list()
    for line in file.readlines():
        charHex = line.replace('\n', '')
        if len(charHex) > 0:
            char = utf8HexStringToChar(charHex)
            for entity in charToHtmlEntity(char):
                if char != entity:
                    chars.append({
                        'character': char,
                        'entity': entity
                    })
    return chars


def writeOutputFile(data: list[dict]):
    with open('output.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


writeOutputFile(
    parseCharacterFile('assets/teletext.txt')
)
