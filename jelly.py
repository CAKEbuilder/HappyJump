
#import SimpleCV
from SimpleCV import *

# setup the camera
display = SimpleCV.Display(resolution=(640, 480))
cam = SimpleCV.Camera()

normaldisplay = True

# define counters for stuff you want to track
jellycount = 0
applecount = 0
floorcount = 0



while display.isNotDone():


        if display.mouseRight:
                normaldisplay = not(normaldisplay)
                print "Display Mode:", "Normal" if normaldisplay else "Segmented"

        #img = cam.getImage().flipHorizontal()
        #img = cam.getImage()
        #img = cam.getImage().flipVertical()
        img = cam.getImage().rotate90()

        # red blob detection (jelly/apples)
        dist = img.colorDistance(SimpleCV.Color.RED).dilate(2).invert()
        segmented = dist.stretch(150,255)
        blobs = segmented.findBlobs()

        # green blob detection (floor)
        dist_g = img.colorDistance(SimpleCV.Color.GREEN).dilate(2).invert()
        segmented_g = dist_g.stretch(130,255)

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
                        if abs(b.area() > 550):
                                jelly = b

                                # count the number of jellys so we can print them to the console
                                #jellycount = len(blobs)
                                #print "I see the jelly"

                                #print b.area()
                                center_point = jelly.centroid()
                                jellybox_dim = (jelly.width(), jelly.height())
                                jellybox = jellylayer.centeredRectangle(center_point, jellybox_dim, color=(SimpleCV.Color.RED), width=2)



                        # look for apples
                        if abs(b.area() < 200) and abs(b.area() >100):
                                apple = b

                                #applecount = len(blobs)
                                #print "I see an apple"

                                center_point = apple.centroid()
                                applebox_dim = (apple.width(), apple.height())
                                applebox = applelayer.circle(center_point, apple.radius())
                        else:
                                applecount = 0

                #print blobs
                #print jelly.coordinates()




        # if green blobs are detected
        if blobs_g:
                for b in blobs_g:
                        # look for floors
                        # floors that touch the left/right edges of the screen aren't detected. I believe this is due to the fact that the floor and the phone are grouped into one blob
                        if abs(b.area() < 800) and abs(b.width() > 20):
                                floor = b

                                #print b.area()
                                #print b.width()
                                #print "I see floors"

                                center_point = floor.centroid()
                                floorbox_dim = (floor.width(), floor.height())
                                #floorbox = floorlayer.centeredRectangle(center_point, floorbox_dim)
                                floorbox = floorlayer.centeredRectangle(center_point, floorbox_dim, color=(SimpleCV.Color.GREEN), width=2)
                        else:
                                floorcount = 0

        if normaldisplay:
                img.show()
        else:
                # red layer
                #segmented.show()

                # green layer
                segmented_g.show()
