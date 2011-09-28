Blind Blocks is the first game I've ever programmed. It's written in Python 3.2 using Pygame 1.9.2.

The game is a tetris clone that hides the blocks from the player after they land, making the player rely on their memory and their limited set of tools to place blocks properly. These tools include a “sonar ping,” which pings the blocks and reveals their location momentarily; an “infrared mode” that allows the player to view the whole screen for a limited amount of time (there’s a meter that’s refilled when the player clears rows); and “flares,” which are one-time use tools that illuminate the field normally for a limited time. Player scores are based on the number of lines cleared and the number of pings used.

There are two modes, normal and hard, and they differ only in the frequency with which you’ll be able to use visual aids.

There’s also a special score that tracks how many blocks in a row you can land and clear rows with without using any visualization tools.

http://www.workworkgames.com/blind-blocks

To Do:

Configurable keys
Smaller netbook resolution. 
Fix dropped block overlap (problem based on pixel jumps)
Allow counterclockwise rotation
Have the current block remain lit for a few seconds.
Make sure the blocks light up in place.
Lock Delay
Movement buffer?
Fixed scoring issue, now it’s more responsive.
Make blind blocks icon for shortcut/installer/exe
Fix game crash after gameover
Losing focus issue still happening?
Fix the overzealous right-side wall kick.
Decrease sensitivity to background lag? Keys too sticky?
During lone line clear animations, keep the next piece in the preview area before switching it to currentBlock, so that the player can see the immediate piece that coming and strategize around it.
During line clear animation, tapping a rotation key rotates pieces before they come up. Probably just get rid of pre-rotation.
Award tetris extra points, not extra lines.