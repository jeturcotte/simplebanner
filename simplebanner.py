import http.server

defaultText = 'WHAT/ABOUT/SECOND/BREAKFAST'
docWidth = 400
docHeight = 600
bandWidth = docWidth
bandHeight = docHeight / 2
bandStart = (docHeight - bandHeight) / 2
baseWidth = 50
baseHeight = 80
lineSep  = 10
baseLength = 10
baseSize = 75
bgColor = '#111'
fontColor = '#FFF'
bands = {
    'GOV': '#555',
    'MIL': '#585',
    'POL': '#558',
    'RES': '#855',
    'def': '#555'
}

def build(path, band):
    finalWords = ''
    allWords = path.split('/')
    numWords = len(allWords)
    fullHeight = 0
    fontSize = {}
    fontHeight = {}
    for word in allWords:
        wordLength = len(word)
        fontSize[word] = baseSize + baseSize * (baseLength-wordLength) / baseLength
        fontHeight[word] = (baseHeight / baseSize) * fontSize[word]
        fullHeight += fontHeight[word]
    textPosition = (docHeight - fullHeight) / 2.8
    for word in allWords:
        displayWord = word.replace("_"," ")
        finalWords += f'<tspan x="200" dy="{fontHeight[word]}" font-size="{fontSize[word]}">{displayWord}</tspan>'
    out = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {docWidth} {docHeight}"><rect width="{docWidth}" height="{docHeight}" fill="{bgColor}" stroke-dasharray="3" stroke="{band}"/><rect x="0" y="{bandStart}" width="{bandWidth}" height="{bandHeight}" fill="{band}"/><text x="{docWidth/2}" y="{textPosition}" font-family="Helvetica Neue Condensed Bold, Arial Narrow Bold, Arial Narrow, sans-serif-condensed" font-weight="900" fill="{fontColor}" text-anchor="middle" dominant-baseline="middle">{finalWords}</text></svg>'
    return out

class BoardHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        usePath = self.path[1:].upper()
        useBand = bands['def']
        try:
            usePath, band = usePath.split('.')
            useBand = bands[band]
        except:
            print(' -- no band specified')
        out = ''
        if usePath:
            out = build(usePath, useBand)
        else:
            out = build(defaultText, useBand)
        self.send_response(200)
        self.send_header("Content-type", "image/svg+xml")
        self.end_headers()
        self.wfile.write(out.encode('utf-8'))

http.server.HTTPServer(("0.0.0.0", 8080), BoardHandler).serve_forever()
