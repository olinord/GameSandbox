import math
import sys

from app import GameApp

def RunApp():
    "Setup and run the app"

    
    app = GameApp("GameIdea")
    app.SetupApp(800, 600)

    app.Run()

    return 0

if __name__ == "__main__":
    RunApp()
