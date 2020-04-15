"""
The template of the main script of the machine learning process
"""

import games.arkanoid.communication as comm
from games.arkanoid.communication import ( \
    SceneInfo, GameStatus, PlatformAction
)

def ml_loop():
    """
    The main loop of the machine learning process
    This loop is run in a separate process, and communicates with the game process.
    Note that the game process won't wait for the ml process to generate the
    GameInstruction. It is possible that the frame of the GameInstruction
    is behind of the current frame in the game process. Try to decrease the fps
    to avoid this situation.
    """

    # === Here is the execution order of the loop === #
    # 1. Put the initialization code here.
    ball_served = False
    ball_x=100
    ball_y=400
    x_diff=0
    # 2. Inform the game process that ml process is ready before start the loop.
    comm.ml_ready()

    # 3. Start an endless loop.
    while True:
        # 3.1. Receive the scene information sent from the game process.
        scene_info = comm.get_scene_info()

        # 3.2. If the game is over or passed, the game process will reset
        #      the scene and wait for ml process doing resetting job.
        if scene_info.status == GameStatus.GAME_OVER or \
            scene_info.status == GameStatus.GAME_PASS:
            # Do some stuff if needed
            ball_served = False

            # 3.2.1. Inform the game process that ml process is ready
            comm.ml_ready()
            continue

        # 3.3. Put the code here to handle the scene information
        


        # 3.4. Send the instruction for this frame to the game process
        if not ball_served:
            comm.send_instruction(scene_info.frame, PlatformAction.SERVE_TO_LEFT)
            ball_served = True
        else:
            if x_diff * (scene_info.ball[0] - ball_x) < 0:
                x_diff = -x_diff
            else:
                x_diff = scene_info.ball[0] - ball_x
                
            y_diff = scene_info.ball[1] - ball_y
            ball_x = scene_info.ball[0]
            ball_y = scene_info.ball[1]
            
            if y_diff > 0: #ball down
                platform_x = (400 - scene_info.ball[1])*(x_diff/y_diff) + scene_info.ball[0]
                if platform_x > 200:
                    platform_x = 400 - platform_x
                if platform_x < 0:
                    platform_x = -platform_x    
                if platform_x > scene_info.platform[0] + 40:                   
                    comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
                elif platform_x < scene_info.platform[0]:
                    comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
                else:
                    comm.send_instruction(scene_info.frame, PlatformAction.NONE) 
            else: #ball up, fix the platform
                if scene_info.platform[0] > 80:
                    comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
                elif scene_info.platform[0] < 80:
                    comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT) 
                else:
                   comm.send_instruction(scene_info.frame, PlatformAction.NONE)
