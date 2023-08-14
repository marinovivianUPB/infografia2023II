import arcade
import random
from app_objects import Tank, Enemy
from time import sleep

# definicion de constantes
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Tank"

SPEED = 10

def get_random_color():
    return (
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
    )


class App(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.BLACK)
        self.rot_speed = 0.5
        self.speed = 10
        self.tank = Tank(150, 400, get_random_color(),1)
        self.gameover= arcade.color.BLACK
        self.winner=0
        self.enemies = [
            Enemy(
                random.randrange(0, SCREEN_WIDTH),
                random.randrange(0, SCREEN_HEIGHT),
                random.randrange(10, 50)
            )
            for _ in range(10)
        ]

        self.tank2 = Tank(650, 400, get_random_color(),2)
    
    def on_mouse_release(self, x: int, y: int, button: int, modifiers: int):
        self.tank.shoot(20)

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.UP:
            self.tank.speed = SPEED
        if symbol == arcade.key.DOWN:
            self.tank.speed = -SPEED

        if symbol == arcade.key.LEFT:
            self.tank.angular_speed = 1.5
        if symbol == arcade.key.RIGHT:
            self.tank.angular_speed = -1.5
        
        if symbol == arcade.key.W:
            self.tank2.speed = SPEED
        if symbol == arcade.key.S:
            self.tank2.speed = -SPEED

        if symbol == arcade.key.A:
            self.tank2.angular_speed = 1.5
        if symbol == arcade.key.D:
            self.tank2.angular_speed = -1.5
            
    def on_key_release(self, symbol: int, modifiers: int):
        if symbol in (arcade.key.UP, arcade.key.DOWN):
            self.tank.speed = 0

        if symbol in (arcade.key.LEFT, arcade.key.RIGHT):
            self.tank.angular_speed = 0
        
        if symbol in (arcade.key.W, arcade.key.S):
            self.tank2.speed = 0

        if symbol in (arcade.key.A, arcade.key.D):
            self.tank2.angular_speed = 0
        
        if symbol == arcade.key.Q:
            self.tank2.shoot(20)

    def on_update(self, delta_time: float):
        self.tank.update(delta_time)
        self.tank2.update(delta_time)
        if len(self.enemies) >0:
            for e in self.enemies:
                e.detect_collision(self.tank)
                e.detect_collision(self.tank2)
                if e.is_alive==False:
                    del e
        
        if self.tank.detect_collision(self.tank2)==False:
            self.gameover=self.tank2.color
            self.winner=2
            sleep(2)
        if self.tank2.detect_collision(self.tank)==False:
            self.gameover=self.tank.color
            self.winner=1
            sleep(2)
            
            

        
    def on_draw(self):
        arcade.start_render()
        arcade.draw_text(f"PLAYER {self.winner} WON\n P{self.winner} SCORE: {self.tank.score if self.winner==1 else self.tank.score}", 200, 400, self.gameover, 32, 400, align="center", font_name="arial", multiline=True)
        for e in self.enemies:
            e.draw()
        self.tank.draw()
        self.tank2.draw()
        
    
    
if __name__ == "__main__":
    app = App()
    arcade.run()
