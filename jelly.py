
#import SimpleCV
from SimpleCV import *

display = SimpleCV.Display(resolution=(640, 480))
cam = SimpleCV.Camera()
normaldisplay = True

while display.isNotDone():

        img = cam.getImage().flipHorizontal()
        #img = cam.getImage()
        dist = img.colorDistance(SimpleCV.Color.RED).dilate(2).invert()
        segmented = dist.stretch(150,255)
        blobs = segmented.findBlobs()


        jellylayer = DrawingLayer((img.width, img.height))
        img.addDrawingLayer(jellylayer)
        img.applyLayers()

        # if blobs are detected
        if blobs:
                # check each blob
                for b in blobs:
                        # if the blob is the right size, set it to jelly
                        if abs(150 - b.area() < 60):
                                jelly = b
                                print "JELLYYYYYYYYYYYYYYYYYY"
                                center_point = jelly.centroid()
                                jellybox_dim = (jelly.width(), jelly.height())
                                jellybox = jellylayer.centeredRectangle(center_point, jellybox_dim)
                                img.show()


                        else:
                                print "I see something..."
                #print blobs
                #print jelly.coordinates()
        else:
                print "no jelly"

        if normaldisplay:
                img.show()
