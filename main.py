from GameObject import GameObject
from Game import Game
from GameDefs import SpriteType
from GameDefs import globals
import tkinter as tk

root = tk.Tk()
canvas = tk.Canvas(root, bg="black")
game = Game()
gameScale = 20
globals.game = game

def refresh_canvas():
    """
    Clears the canvas and redraws a character at a random position.
    """
    # Clear the canvas
    finished = game.update()
    canvas.delete("all")

    # Generate a new random position

    for o in GameObject.gameObjects:
        x = o.position.x * gameScale
        y = o.position.y * gameScale

    # Draw the character 'X' at the new random position
        if o.type == SpriteType.PACMAN:
            canvas.create_arc(x, y, x+gameScale, y+gameScale, start=30, extent=300, fill="yellow", outline="yellow")

        elif o.type ==  SpriteType.GHOST:
            if globals.pill.isActive():
                canvas.create_oval(x, y, x+gameScale, y+gameScale, fill="blue" )  # Head
                canvas.create_rectangle(x, y + gameScale/2-2, x+gameScale, y+gameScale, fill="blue", outline="blue" )  # Bottom
            else:
                canvas.create_oval(x, y, x+gameScale, y+gameScale, fill="red" )  # Head
                canvas.create_rectangle(x, y + gameScale/2-2, x+gameScale, y+gameScale, fill="red", outline="red" )  # Bottom

        elif o.type ==  SpriteType.PILL:
            canvas.create_oval(x, y, x+gameScale, y+gameScale, fill="white", outline="black")

        elif o.type ==  SpriteType.WALL:
            canvas.create_rectangle(x, y, x+gameScale, y+gameScale, fill="cyan")
        elif o.type == SpriteType.DOT:
            canvas.create_oval(x+gameScale/2-1, y+gameScale/2-1, x + gameScale/2+1, y + gameScale/2+1, fill="white", outline="black")

    # Schedule the next canvas refresh in 1000ms (1 second)
    if not finished:
        root.after(300, refresh_canvas)

def main():
    size = gameScale * globals.gameSize
    canvas.config(width=size, height=size)

    canvas.pack(fill="both", expand=True)

    refresh_canvas()

    root.mainloop()

    print("Game over! ",Game.gameTime," moves")


if __name__ == "__main__":
    main()
