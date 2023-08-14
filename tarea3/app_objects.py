from __future__ import annotations
import numpy as np
import arcade
import math


class Polygon2D:
    def __init__(self, vertices, color, rot_speed=0):
        self.vertices = vertices
        self.color = color
        self.rot_speed = rot_speed

    def translate(self, dx, dy):
        TM = np.array([
            [1, 0, dx], 
            [0, 1, dy], 
            [0, 0, 1]
        ])

        return self.apply_transform(TM)
    
    def rotate(self, theta, pivot=None):
        xc, yc = pivot if pivot is not None else self.get_center()

        Mt1 = np.array([
            [1, 0, -xc], 
            [0, 1, -yc], 
            [0, 0, 1]
        ])
        Mr = np.array([
            [np.cos(theta), -np.sin(theta), 0], 
            [np.sin(theta), np.cos(theta), 0], 
            [0, 0, 1]
        ])
        Mt2 = np.array([
            [1, 0, xc], 
            [0, 1, yc], 
            [0, 0, 1]
        ])

        TM = np.dot(Mt2, np.dot(Mr, Mt1))
  
        return self.apply_transform(TM)

    def scale(self, sx, sy, pivot=None):
        xc, yc = pivot if pivot is not None else self.get_center()
        Mt1 = np.array([
            [1, 0, -xc], 
            [0, 1, -yc], 
            [0, 0, 1]
        ])
        Ms = np.array([
            [sx, 0, 0], 
            [0, sy, 0], 
            [0, 0, 1]
        ])
        Mt2 = np.array([
            [1, 0, xc], 
            [0, 1, yc], 
            [0, 0, 1]
        ])

        TM = np.dot(Mt2, np.dot(Ms, Mt1))
  
        return self.apply_transform(TM)

    def apply_transform(self, tr_matrix):
        v_array = np.transpose(np.array(
            [[v[0], v[1], 1] for v in self.vertices]
        ))

        self.vertices = np.transpose(
            np.dot(tr_matrix, v_array)[0:2, :]
        ).tolist()

    def get_center(self):
        return np.mean(np.array(self.vertices), axis=0)

    def draw(self):
        arcade.draw_polygon_outline(self.vertices, self.color, 5)


class Tank:
    def __init__(self, x, y, color,number) -> None:
        self.x = x
        self.y = y
        self.speed = 0
        self.angular_speed = 0
        self.theta = 0
        self.number = number
        self.color=color
        self.body = Polygon2D([(100 + x, y), (x, 50 + y), (x, -50 + y)], color)
        d = 2*(self.body.vertices[0][0]*(self.body.vertices[1][1]-self.body.vertices[2][1])+ self.body.vertices[1][0]*(self.body.vertices[2][1]-self.body.vertices[0][1])+ self.body.vertices[2][0]*(self.body.vertices[0][1]-self.body.vertices[1][1]))
        self.ux = ((self.body.vertices[0][0]**2 + self.body.vertices[0][1]**2)*(self.body.vertices[1][1]-self.body.vertices[2][1])+(self.body.vertices[1][0]**2 + self.body.vertices[1][1]**2)*(self.body.vertices[2][1]-self.body.vertices[0][1])+(self.body.vertices[2][0]**2 + self.body.vertices[2][1]**2)*(self.body.vertices[0][1]-self.body.vertices[1][1]))/d
        self.uy = ((self.body.vertices[0][0]**2 + self.body.vertices[0][1]**2)*(self.body.vertices[2][0]-self.body.vertices[1][0])+(self.body.vertices[1][0]**2 + self.body.vertices[1][1]**2)*(self.body.vertices[0][0]-self.body.vertices[2][0])+(self.body.vertices[2][0]**2 + self.body.vertices[2][1]**2)*(self.body.vertices[1][0]-self.body.vertices[0][0]))/d
        self.r = math.sqrt((self.ux - self.body.vertices[0][0])**2 + (self.uy - self.body.vertices[0][1])**2)
        print(f"{self.ux},{self.uy},{self.r}")
        self.left_track = Polygon2D(
            [
                (-40 + x, -30 + y), 
                (60 + x, -30 + y),
                (60 + x, -60 + y),
                (-40 + x, -60 + y), 
            ],
            color
        )
        self.right_track = Polygon2D(
            [
                (-40 + x, 30 + y), 
                (60 + x, 30 + y),
                (60 + x, 60 + y),
                (-40 + x, 60 + y), 
            ],
            color
        )
        self.bullets = []
        self.score = 0
        self.is_alive = True
    
    def shoot(self, bullet_speed):
        self.bullets.append((self.x, self.y, self.theta, bullet_speed))

    def update(self, delta_time: float):
        dtheta = self.angular_speed * delta_time
        dx = self.speed * math.cos(self.theta)
        dy = self.speed * math.sin(self.theta)
        self.theta += dtheta
        self.x += dx
        self.y += dy
        self.ux +=dx
        self.uy += dy
        self.body.translate(dx, dy)
        self.left_track.translate(dx, dy)
        self.right_track.translate(dx, dy)
        
        self.body.rotate(dtheta, pivot=(self.x, self.y))
        self.left_track.rotate(dtheta, pivot=(self.x, self.y))
        self.right_track.rotate(dtheta, pivot=(self.x, self.y))

        self.update_bullets(delta_time)

    def update_bullets(self, delta_time):
        for i, (x, y, theta, speed) in enumerate(self.bullets):
            new_x = x + speed * math.cos(theta)
            new_y = y + speed * math.sin(theta)
            self.bullets[i] = (new_x, new_y, theta, speed)

    def draw(self):
        self.body.draw()
        self.left_track.draw()
        self.right_track.draw()
        arcade.draw_point(self.x, self.y, arcade.color.RED, 4)
        xt = 10
        if self.number>1:
            xt+=400*(self.number-1)
        yt = 150
        arcade.draw_text(f"P{self.number} SCORE: {self.score}", xt, yt, self.color, 12, 400, align="left", font_name="arial")
        for bx, by, theta, speed in self.bullets:
            arcade.draw_point(bx, by, arcade.color.YELLOW, 7)
    
    def detect_collision(self, tank: Tank):
        for bullet in tank.bullets:
            if self.distance_to(bullet) < self.r:
                self.is_alive = False
                tank.score += self.score
        return self.is_alive
    
    def distance_to(self, bullet):
        xb, yb, tb, sb = bullet
        return math.sqrt((xb - self.ux)**2 + (yb - self.uy)**2)


class Enemy:
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r
        self.is_alive = True
    
    def detect_collision(self, tank: Tank):
        for bullet in tank.bullets:
            if self.distance_to(bullet) < self.r:
                self.is_alive = False
                tank.score +=10
    
    def distance_to(self, bullet):
        xb, yb, tb, sb = bullet
        return math.sqrt((xb - self.x)**2 + (yb - self.y)**2)

    def draw(self):
        if self.is_alive:
            arcade.draw_circle_filled(self.x, self.y, self.r, arcade.color.RED_DEVIL)
