import sys
import copy
import os
import string
import numpy as np
from PIL import Image
from collections import defaultdict

frames = []

def snapshot(sparseDict, printToScreen = True, saveAnimation = False, update = False, transpose = True, **kwargs):
    if not printToScreen and not saveAnimation:
        return
    frame = copy.copy(sparseDict)
    if update:
        frame.update(update)
    if saveAnimation:
        global frames
        frames += [frame]
    if printToScreen:
        asciiPrint(frame, transpose = transpose, **kwargs)

def sparseToDense(bitmap):
    # import scipy.sparse
    items = list(bitmap.items())
    vs = [v for (i,j), v in items]
    ii = [i for (i,j), v in items]
    min_ii = min(ii)
    ii = [i-min_ii for i in ii] # avoid negative indices
    jj = [j for (i,j), v in items]
    min_jj = min(jj)
    jj = [i-min_jj for i in jj] # avoid negative indices
    # Todo: load better
    arr = np.zeros((max(ii)+1,max(jj)+1), 'int8')
    for i,j,v in zip(ii,jj,vs):
        arr[i][j] = v
    return arr
    # return scipy.sparse.csr_matrix((vs, (ii, jj))).toarray()

def asciiPrint(bitmap, transpose=False, reset=False, header=""):
    if isinstance(bitmap, dict):
        bitmap = sparseToDense(bitmap)
    else:
        bitmap = np.array(bitmap)
    if transpose:
        bitmap = bitmap.transpose()
    if bitmap.shape[0] > 500 or bitmap.shape[1] > 500:
        raise(Exception(f"Bitmap too large to be printed: {np.array(bitmap).shape}"))
    if reset:
        print(chr(27) + "[2J", flush=False)
    print(header, flush=False)
    tiles = {str(i):v for i,v in enumerate([u"⬛️",u"⬜️",u"🟥",u"🟨", u"🔵",u"🟦",u"🤖",u"🔑",u"🚪", u"🟩"])}
    tiles.update({i:v for i,v in enumerate([u"⬛️",u"⬜️",u"🟥",u"🟨", u"🔵",u"🟦",u"🤖",u"🔑",u"🚪", u"🟩"])})
    tiles.update({' ': u"⬛️", '.': u"⬜️", '#': u"🟥"})
    tiles.update({c:c+' ' for c in string.ascii_uppercase})
    print("\n".join(''.join(tiles[i] for i in line) for line in bitmap), flush=False)
    sys.stdout.flush()

def saveAnimatedGIF(frames, tileSize = 10, outputFile = 'animation.gif', freq = 1, duration = 10, backgroundColour = 'black', skipTile = None):
    if len(frames) == 0:
        print("No frames…")
        return
    frames = frames + [frames[-2]] * 30
    tilePath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tiles')

    print(f"Saving animation ({len(frames)} frames)…")
    tiles = {str(i):Image.open(f'{tilePath}/{i}.png', 'r').resize((tileSize,)*2) for i in range(2)}
    tiles.update({i:Image.open(f'{tilePath}/{i}.png', 'r').resize((tileSize,)*2) for i in range(2)})
    tiles.update({c:Image.open(f'{tilePath}/{i}.png', 'r').resize((tileSize,)*2) for c,i in {'#':2,' ':0, '.':1}.items()})
    tiles.update({c:Image.open(f'{tilePath}/0.png', 'r').resize((tileSize,)*2) for c in string.ascii_uppercase})
    if isinstance(frames[0], dict):
        dims = sparseToDense(frames[-1]).shape
        minY = min(y for _,y in frames[-1])
        minX = min(x for x,_ in frames[-1])

        def frameToImage(frame, i):
            img = Image.new('RGBA', (dims[0]*tileSize, dims[1]*tileSize), backgroundColour)
            for (y,x),v in frame.items():
                img.paste(tiles[v], ((y - minY)*tileSize, (x - minX)*tileSize), mask=tiles[v])
            print(f"saved: {i}/{len(frames)}", end="\r")
            return img.convert('P', palette=Image.ADAPTIVE)

        images = (frameToImage(f,i) for i,f in enumerate(frames) if i%freq == 0)
    else:
        dims = frames[0].shape
        def frameToImage(frame, i):
            img = Image.new('RGBA', (dims[0]*tileSize, dims[1]*tileSize), backgroundColour)
            for (x,y) in np.ndindex(dims):
                if skipTile and frame[x,y] == skipTile: continue
                tile = tiles[frame[x,y]]
                img.paste(tile, (x*tileSize, y*tileSize), mask=tile)
            print(f"saved: {i}/{len(frames)}", end="\r")
            return img.convert('P', palette=Image.ADAPTIVE)

    images = (frameToImage(f,i) for i,f in enumerate(frames) if i%freq == 0)

    next(images).save(
        outputFile,
        save_all=True,
        append_images=images,
        duration=duration,
        loop=0,
        optimize=True
    )
