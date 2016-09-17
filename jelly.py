
#import SimpleCV
from SimpleCV import *

# setup the camera
display = SimpleCV.Display(resolution=(640, 480))
cam = SimpleCV.Camera()

normaldisplay = True


while display.isNotDone():


        if display.mouseRight:
                normaldisplay = not(normaldisplay)
                print "Display Mode:", "Normal" if normaldisplay else "Segmented"

        img = cam.getImage().flipHorizontal()
        #img = cam.getImage()

        # red blob detection (jelly/apples)
        dist = img.colorDistance(SimpleCV.Color.RED).dilate(2).invert()
        segmented = dist.stretch(150,255)
        blobs = segmented.findBlobs()

        # green blob detection (floor)
        dist_g = img.colorDistance(SimpleCV.Color.GREEN).dilate(2).invert()
        segmented_g = dist_g.stretch(150,255)
        blobs_g = segmented_g.findBlobs()



        # prepare the jelly detection
        jellylayer = DrawingLayer((img.width, img.height))
        img.addDrawingLayer(jellylayer)

        # prepare the apple detection
        applelayer = DrawingLayer((img.width, img.height))
        img.addDrawingLayer(applelayer)

        # prepare the floor detection
        floorlayer = DrawingLayer((img.width, img.height))
        img.addDrawingLayer(floorlayer)

        img.applyLayers()



        # if red blobs are detected
        if blobs:
                # check each blob
                for b in blobs:

                        # look for jelly
                        # in a 640x480 frame with the S5 touching the top and bottom of the window, the jelly should have an estimated area of 450 (no math done for this, just trial and error)
                        if abs(b.area() > 300):
                                jelly = b
                                print "JELLYYYYYYYYYYYYYYYYYY"
                                #print b.area()
                                center_point = jelly.centroid()
                                jellybox_dim = (jelly.width(), jelly.height())
                                jellybox = jellylayer.centeredRectangle(center_point, jellybox_dim)

                        # look for apples
                        if abs(b.area() < 200):
                                apple = b
                                print "APPLESSSSSSSSSSSSSSSSS"
                                center_point = apple.centroid()
                                applebox_dim = (apple.width(), apple.height())
                                applebox = applelayer.circle(center_point, apple.radius())

                #print blobs
                #print jelly.coordinates()
        else:
                print "no jelly"

        # if green blobs are detected
        if blobs_g:
                for b in blobs_g:
                        if abs(b.area() < 300):
                                floor = b
                                print "FLOOORRRSSSSSSSSSSSSS"
                                center_point = floor.centroid()
                                floorbox_dim = (floor.width(), floor.height())
                                floorbox = floorlayer.centeredRectangle(center_point, floorbox_dim)






        if normaldisplay:
                img.show()
        else:
                # red layer
                #segmented.show()

                # green layer
                segmented_g.show()
