import cv2
import time

class tatSelection():
    def __init__(self, arg1=None) -> None:
        self.__arg1 = arg1

    def getPath(self, arg2=None):
        img = cv2.imread(r'selectTat.png', cv2.IMREAD_COLOR)  # Reading path of selection image

        tat1 = cv2.imread(r'tat.png', cv2.IMREAD_COLOR)
        tat2 = cv2.imread(r'sleeve.png', cv2.IMREAD_COLOR)              # Reading paths of all tattoos
        tat3 = cv2.imread(r'skull.png', cv2.IMREAD_COLOR)
        tat4 = cv2.imread(r'snake.png', cv2.IMREAD_UNCHANGED)

        path = "end"
        sizeArr=[]     # Declaring/initializing variables for path, rotation, and size
        rotAdj = 0

        cv2.imshow("Please Select a Tattoo", img) # Showing the window

        while True:  
            k = cv2.waitKey(1)
            if k == ord('q'): # If q is pressed, end program. Does not change path, so path stays as "end" which tells main program to not run any tattoo calculations
                break
            elif(k == ord('1')):  # Checking for key press of '1'
                self.showOption(tat1) # Calling showOption on tattoo 1
                path = 'tat.png' # Changing to correct path
                sizeArr = [0.09,0.24] #Correct scaling max and mins - derived from testing
                break
            elif(k == ord('2')):
                self.showOption(tat2)
                path = 'sleeve.png'           # Too lazy to write that for all of them, but same idea lol
                sizeArr = [0.09, 0.35]
                rotAdj = -15 #rotAdj is the adjustment for rotation because some images are slightly rotated, so to correct for that
                break
            elif(k == ord('3')):
                self.showOption(tat3)
                path = 'skull.png'
                sizeArr = [0.06, 0.18]
                rotAdj=-12
                break
            elif(k == ord('4')):
                self.showOption(tat4)
                path = 'snake.png'
                sizeArr = [0.12, 0.36]
                rotAdj = -15
                break

        cv2.destroyAllWindows()
        return path, sizeArr, rotAdj

    def showOption(self, tat): 
        cv2.destroyWindow("Please Select a Tattoo") # Getting rid of the selection window
        cv2.imshow("Selected Tattoo", tat) # Displaying the selected tattoo for 2 seconds
        cv2.waitKey(2000)
        #if (k == ord('y')):
            #break