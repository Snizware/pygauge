import pygame
from math import radians, sin, cos

"""
Author: James Hunt
This module is dependent on pygame and was written for python 3.
I apologize for sloppy syntax and confusing comments.  I'm pretty new at this.  

 Example application:          Once it is running, use up and down arrows to move the sample gauges

    #The following code defines an object of type PyGauge and calls it RPM1

    # Arguements are:     square start end  # of    round to    highest         lowest          thickness of
    #              x    y  size  arc  arc  digits   #of digits  possible value  possible value    the ring
    RPM1 = PyGauge(10, 10, 250, 150, 330, digits=5, decimals=0, maxvalue=12000, minvalue=50, arcthickness=3,\

    #            font size relative  true type       digital readout
    #            to gauge size         font       offset in percent of gauge
                 fontrelativity=13, fontfile="", digital_x=45, digital_y=20, \
    #
                 #            range   arc   needle  | color arc definitions |
                 #            -  +   color  color   low  high  arc    needle   low  high  arc  needle   etc...
                 arc_colors=[(0, 80, GREEN, WHITE),(80.1, 95, YELLOW, YELLOW),(95.1, 100, RED, RED)],\
    #            gauge background  needle when not in arc range
                 bg_color=MASK,      needle_color=WHITE):

    #To draw the gauge, simply call:
    RPM1.draw(screen, value)
        # 'screen' is the pygame surface to draw on.
        # 'value' sets the position & display of the gauge

    #Don't forget: pygame.display.flip()


    #Anything outside of the range from the lowest to highest value causes a red X to display on
    #the digital display box if it is visible.
    #Start Arc and End Arc are degrees from top dead center to display the range arc
    #Setting digits=0 removes the digital display box and only a round dial remains
"""

#Color definitions for ease of use
MASK  = (255,   0, 255)
BLACK = (  0,   0,   0)
BROWN = (185, 122,  87)
YELLOW= (255, 255,   0)
WHITE = (255, 255, 255)
BLUE  = (  0,   0, 255)
GREEN = (  0, 255,   0)
RED   = (255,   0,   0)
GREY  = (200, 200, 200)
CYAN  = (  0, 255, 255)

class PyGauge():
    def __init__(self, x=50, y=50, size=200, minangle=90, maxangle=320, arcthickness=3,\
                 minvalue=0.0, maxvalue=100.0, digits=5, decimals=1, fontrelativity=13, fontfile="",\
                 digital_x=45, digital_y=20, \
                 #            range   arc   needle range is next    arc   needle   etc...
                 #            -  +   color  color  percent range  color  color
                 arc_colors=[(0, 80, GREEN, WHITE),(80.1, 95, YELLOW, YELLOW),(95.1, 100, RED, RED)],\
                 bg_color=MASK, needle_color=WHITE):

        self.position = (x, y)
        self.arc_colors = arc_colors
        self.bg_color = bg_color
        self.needle_color = needle_color

        self.minvalue = minvalue
        self.maxvalue = maxvalue
        self.valuerange = maxvalue - minvalue

        self.gaugeimage = pygame.Surface((size, size))
        self.gaugeimage.fill(bg_color)
        self.gaugeimage.set_colorkey(bg_color)

        self.minangle = minangle
        self.maxangle = maxangle
        self.gaugerange = self.maxangle - self.minangle
        self.size = size

        self.digits = digits

        #Formats digits for digital display
        self.fstring = '{:-' + str(digits) + '.' + str(decimals) + 'f}'

        self.needlethickness = int(0.03125 * self.size)

        if digits > 0:
            if fontfile == "":
                self.digitalfont = pygame.font.SysFont("monospace", int(self.size * (fontrelativity/100)))
            else:
                self.digitalfont = pygame.font.Font(fontfile, int(self.size * (fontrelativity/100)))

            self.digitalfont.set_bold(True)
            fonttest = self.digitalfont.render('X' * digits, True, WHITE, BLACK)

            self.digitaloffset = (int(self.size * (digital_x/100)) , int(self.size * (digital_y / 100)))  #Digial Display Relative Position
            self.digitalsize = (fonttest.get_rect()[2] + self.needlethickness * 2,fonttest.get_height() + self.needlethickness * 1.8)
            self.digitalposition = (self.position[0] + self.digitaloffset[0] + int(self.needlethickness * .76), self.position[1] + self.digitaloffset[1] + int(self.needlethickness * .83))

            b = int(self.needlethickness )
            self.redx = pygame.Surface((int(self.digitalsize[0] - b), int(self.digitalsize[1] - b)))
            self.redx.fill(bg_color)
            self.redx.set_colorkey(bg_color)
            pygame.draw.line(self.redx, RED, (0,0), (self.digitalsize[0] - b, self.digitalsize[1] - b) , int(self.needlethickness))
            pygame.draw.line(self.redx, RED, (self.digitalsize[0] - b,0), (0, self.digitalsize[1] - b) , int(self.needlethickness))

        correctionangle = 90    #This moves the ARC clockwise 90 degrees to align it with the needle

        self.gaugecenter = (int(self.size / 2),int(self.size / 2))

        if self.digits > 0:
            pygame.draw.rect(self.gaugeimage, GREY, [self.digitaloffset[0], self.digitaloffset[1], self.digitalsize[0], self.digitalsize[1]], int(self.needlethickness/2))

        if self.minangle < self.maxangle:
            s = 1
        else:
            s = -1

        for arcdraw in range(self.minangle,self.maxangle,s):
            value = ((arcdraw - self.minangle) / self.gaugerange * self.valuerange) + self.minvalue

            gaugeinnerx = (self.size / 2 - int(arcthickness / 100 * self.size)) * cos(radians(arcdraw - correctionangle))
            gaugeinnery = (self.size / 2 - int(arcthickness / 100 * self.size)) * sin(radians(arcdraw - correctionangle))
            gaugeouterx = (self.size / 2) * cos(radians(arcdraw - correctionangle))
            gaugeoutery = (self.size / 2) * sin(radians(arcdraw - correctionangle))

            pygame.draw.line(self.gaugeimage, self.range_color(value), (self.gaugecenter[0] + gaugeinnerx, self.gaugecenter[1] + gaugeinnery), (self.gaugecenter[0] + gaugeouterx, self.gaugecenter[1] + gaugeoutery) , int(self.size / 50))

    def range_color(self, value, needle=False):
        for band in self.arc_colors:
            if value >= band[0] and value <= band[1]:
                if needle:
                    return band[3]
                else:
                    return band[2]
        if needle:
            return self.needle_color
        else:
            return self.bg_color

    def draw(self, drawingsurface, value=-1):

        #percent = (value - self.minvalue) / self.valuerange * 100
        needlecolor = self.range_color(value, True)

        #Slap down a new gauge on the background - Drawing the gauge arc takes a while so
        # it is done when the gauge is initialized, and then copied for all the updates
        #A.K.A. Blit the gauge image onto the background
        drawingsurface.blit(self.gaugeimage, self.position)

        #Render the digital display value
        if self.digits > 0:
            digitaldisplay = self.digitalfont.render(self.fstring.format(value), True, needlecolor)

            #Blit the text onto the background
            drawingsurface.blit(digitaldisplay, (self.digitalposition[0],self.digitalposition[1] + int(self.needlethickness * .83)))

        if value >= self.minvalue and value <= self.maxvalue:
            #gaugehandx = self.size / 2.2 * cos(radians((value / 100 * self.gaugerange) + self.minangle - 90))
            #gaugehandy = self.size / 2.2 * sin(radians((value / 100 * self.gaugerange) + self.minangle - 90))
            gaugehandx = self.size / 2.2 * cos(radians(((value - self.minvalue) / self.valuerange * self.gaugerange) + self.minangle - 90))
            gaugehandy = self.size / 2.2 * sin(radians(((value - self.minvalue) / self.valuerange * self.gaugerange) + self.minangle - 90))
            #Draw the gauge needle
            drawingsurface.set_colorkey(self.bg_color)
            pygame.draw.line(drawingsurface, needlecolor, (self.gaugecenter[0] + self.position[0], self.gaugecenter[1] + self.position[1]), (self.gaugecenter[0] + gaugehandx + self.position[0], self.gaugecenter[1] + gaugehandy + self.position[1]) , self.needlethickness)
        else:
            if self.digits > 0:
                drawingsurface.blit(self.redx, self.digitalposition)


if __name__ == "__main__":
    # Initialize pygame
    pygame.init()
    # Set screen size
    size = [800, 600]
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Engine Monitor")

    # Main loop
    done = False
    clock = pygame.time.Clock()
                                        #fontfile can be set to the path of any ".ttf" true type font file
    RPM1 = PyGauge(10, 10, 250, 150, 330, digits=5, decimals=0, maxvalue=12000, minvalue=50, arc_colors=[(0, 50, BLACK, GREY),(51, 9600, GREEN, WHITE),(9601, 11400, YELLOW, YELLOW), (11401, 12000, RED, RED)], fontfile="")
    BAT = PyGauge(270, 10, 200, 160, 320, digits=4, decimals=2, maxvalue=8.0, minvalue = 4.0, arc_colors=[(4, 4.76, RED, RED),(4.77, 5.6, WHITE, WHITE),(5.61, 6.00, RED, RED),(6.01, 6.4, YELLOW, YELLOW),(6.41, 7.22, GREEN, WHITE),(7.23, 8.0, RED, RED)], fontfile="")

    #Here's an example of a very minimal definition resulting in a default gauge 250x250 pixels in size.
    # for now, all gauges are square.
    RPM3 = PyGauge(35, 230, 250)
    RA = PyGauge(270, 250, 200, 92, 0, digits=0, decimals=0, digital_x=52, digital_y=55, maxvalue=120, minvalue = 0, arcthickness=5, arc_colors=[(0, 6.9, BROWN, BROWN), (7, 24, GREEN, GREEN),(24.1, 50, CYAN, YELLOW),(50.1, 120, CYAN, CYAN)], bg_color=MASK, needle_color=WHITE, fontfile="")

    val = 120
    pygame.key.set_repeat(1,40) #After a 1 millisecond delay, key repeat every 40 milliseconds
    while not done:

        # Only let the main loop run at 30 times per second max.
        # Comment out to max out the CPU.

        clock.tick(30)

        # Go through all the "events" (clicks, moves, etc.) that have collected since the last pass
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #
                done=True # Allows the main loop to know it is time to stop

            if event.type == pygame.KEYDOWN:    # One or more keys is pressed... go check which ones...
                if event.key == pygame.K_DOWN:  # was it the DOWN key?
                    val -= 1

                if event.key == pygame.K_UP:    # was it the UP key?
                    val += 1

        # Clears the screen
        screen.fill(BLACK)

        #This is all that's required to update the gauges once they're initialized
        # although, to cause them to appear, pygame.display.flip() is still required
        # "screen" is the surface being drawn on.  The second argument is the gauge's displayed value.
        # the values shown below are simply for demonstrational purposes.  Put whatever you want there.
        RPM1.draw(screen, val * 45.010)
        BAT.draw(screen, val *.04)
        RPM3.draw(screen, val / 4)
        RA.draw(screen, val - 100)

        # This is like flipping pages in a flip-book.
        # You drew everything on a surface, now flip it into view.
        pygame.display.flip()

    pygame.quit()


