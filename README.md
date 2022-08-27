# Yet Another ПАСЬЯНС Bot

This is a bot that automatically plays ПАСЬЯНС. A mini-game inside EXAPUNKS by Zachtronics (which I highly recommend!).

## How does it work?

The bot works in three stages. 

### Board Reconstruction

The first is board reconstruction. The bot takes a screenshot of the game window and analyses predefined pixels comparing them to a template (Unfortunately it assumes you're playing on full screen using 1920 x 1080 resolution). Once it knows which cards are where it reconstructs the board in code.

### Game Solving

The second stage is the most important one. Once the board is reconstructed the bot uses DFS to navigate through possible moves. It also uses some simple hashing to omit board states it has already seen (but only during that solve session). It also tries not to do stupid moves but sometimes it still does them but since it's a one-time use bot there's no point in optimising it (apart from satisfaction)

### Auto Player

Once the second stage determines the solution (a list of moves) the autoplayer uses `pyautogui` to play the game.


