from Model.PlayerData import PlayerData


def hexNoLeader(number):
    return hex(number).replace("0x", "")

def ToHex(numbers):
    return ('#' + hexNoLeader(numbers[0]).zfill(2) + 
                hexNoLeader(numbers[1]).zfill(2) + 
                hexNoLeader(numbers[2]).zfill(2))


#method for marking an image based purely on pixel offsets.
def markPlayerPreview(pixels, imgsize, startOffset, garbageOffset, gs):
    markColor = (255, 255, 255)
    garboColor = (0, 255, 0)
    w, h = imgsize
    for y in range(20):
        yPix = round(y * gs + startOffset[1]) 
        if yPix >= h:
            break
        for x in range(10):
            xPix = round(x * gs + startOffset[0])
            if xPix >= w:
                break
                
            pixels[xPix, yPix] = markColor     
        xPix = round(x * gs + startOffset[0] + garbageOffset)
        if xPix >= w:
            continue
        pixels[xPix, yPix] = garboColor 

def markImagePreview(fullImageMarker, image):
    pixels = image.load()
        
    startOffset = [20, 20]  # magic number :(
    garbageOffset = fullImageMarker.WindowSettings.garbageXOffset

    PixelOffsetArgs = (pixels, image.size, startOffset, garbageOffset, fullImageMarker.WindowSettings.gridSize)
    # mark player 1
    markPlayerPreview(*PixelOffsetArgs)
        
    startOffset[0] += fullImageMarker.WindowSettings.playerDistance
    # mark player 2
    markPlayerPreview(*PixelOffsetArgs)



# Section below is marking for output to external programs
def markImageOutput(imageMarker, image):
    pixels = image.load()
    garbageOffset = imageMarker.WindowSettings.garbageXOffset
    startOffset = [20, 20]  # magic number :(
    # mark player 1
    for player in imageMarker.data:
        markPlayerOutput(imageMarker, player, pixels, image.size, garbageOffset, startOffset)            
        startOffset[0] += imageMarker.WindowSettings.playerDistance
        
def markPlayerOutput(imageMarker, player, pixels, imgsize, garbageOffset, startOffset):
    player.resetGarbage()
    gs = imageMarker.WindowSettings.gridSize
    w, h = imgsize
    y = 0
    x = 0

    for y in range(PlayerData.MATRIX_Y):
        yPix = round(y * gs + startOffset[1]) 
        if yPix >= h:
            break
        for x in range(PlayerData.MATRIX_X):
            xPix = round(x * gs + startOffset[0])
            if xPix >= w:
                break
            player.updateField(x, y, ToHex(pixels[xPix, yPix]))
        
    # garbage detection
    for y in range(PlayerData.MATRIX_Y - 1, -1, -1):
        yPix = round(y * gs + startOffset[1])
        xPix = round(x * gs + startOffset[0] + garbageOffset)
        if xPix >= w or yPix >= h:
            continue
        player.updateGarbage(20 - y, pixels[xPix, yPix])