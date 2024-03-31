from UserInterface.interface import HandGestureApp  # Import the HandGestureApp class from the UserInterface package

class Main:
    def __init__(self):
        self.app = HandGestureApp()  # Initialize an instance of the HandGestureApp

    def run(self):
        self.app.geometry("800x800")  # Set the initial size of the application window to 800x800 pixels
        self.app.resizable(False, False)  # Disable resizing of the application window
        self.app.mainloop()  # Start the main event loop to run the application

if __name__ == '__main__':
    main = Main()  # Create an instance of the Main class
    main.run()  # Run the application
