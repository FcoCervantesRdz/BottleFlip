import pygame
import random
import math

def distant(p1, p2):
    return ((p2[0]-p1[0])**2+(p2[1]-p1[1])**2)**(1/2)

class Space:
    def __init__(self, limit_s = [1366, 700], color = [255,255,255]):
        self.max = limit_s
        self.x_max = limit_s[0]
        self.y_max = limit_s[1]
        self.color = color
        pygame.init()
        self.screen = pygame.display.set_mode(limit_s)
        pygame.display.set_caption("BottleFlip")
        self.g = 9.81
    def update(self):
        self.screen.fill(self.color)
        return

class Time:
    def __init__(self, dt=0.01):
        self.dt = dt
        self.t = 0
        self.clock = pygame.time.Clock()
    def update(self):
        self.t += self.dt

class Arm:
    original_img = pygame.image.load("Hand.png")
    w_o = original_img.get_width()
    h_o = original_img.get_height()
    r = 0.05
    l = 0.6
    states = ["Holding", "Not Holding"]
    
    def __init__(self, pos = [100,500], pivot = [100,500], mass = 5):
        self.angle = math.pi/2
        self.img = Arm.original_img
        self.d = distant(pos,pivot)
        self.pos = pos
        self.pivot = pivot
        self.inertia_cm = mass*(1/4*(Arm.r)**2+1/12*Arm.l**2)
        self.angular_vel = 0
        self.bottle = None
        self.mass = mass
        self.give_torque = 0
        return
        
    def unhold(self):
        self.bottle.angular_vel = self.angular_vel
        self.bottle.angle = self.angle
        vx = (self.l+self.bottle.l/2)*self.angular_vel*math.cos(self.angle)
        vy = (self.l+self.bottle.l/2)*self.angular_vel*math.sin(self.angle)
        self.bottle.vel = [vx, vy]
        x = self.bottle.pos[0] + self.bottle.h_o/2*math.sin(self.angle)
        y = self.bottle.pos[1] - self.bottle.h_o/2*math.cos(self.angle)
        self.bottle.pos = [x, y]
        self.bottle.holded = False
        self.bottle = None
        return

    def update(self, space, time):
        inertia = self.inertia_cm + self.mass*(Arm.l/2)**2
        torque = self.mass*space.g*math.sin(-self.angle)*self.l/2 + self.give_torque
        if self.bottle:
            inertia += self.bottle.inertia_cm + self.bottle.mass*(self.l + self.bottle.l/2)**2
            torque += self.bottle.mass*space.g*math.sin(-self.angle)*(self.l + self.bottle.l/2)
        self.angular_ace = torque/inertia
        self.angular_vel += self.angular_ace*time.dt
        self.angle += self.angular_vel*time.dt
        if self.angle >= 2*math.pi:
            self.angle -= 2*math.pi
        elif self.angle < 0:
            self.angle += 2*math.pi
        if self.bottle:
            self.bottle.update_by_arm(space, self)
        self.draw(space)
        
    def draw(self, space):
        self.img = pygame.transform.rotate(Arm.original_img, self.angle*180/math.pi)
        xf = self.d*math.cos(self.angle)+self.pivot[0]
        yf = self.d*math.sin(self.angle)+self.pivot[1]
        if self.angle >= 0 and self.angle < math.pi/2:
            xb = xf - self.w_o*math.cos(self.angle)/2
            yb = yf + self.w_o*math.sin(self.angle)/2
        elif self.angle >= math.pi/2 and self.angle < math.pi:
            xb = xf + self.w_o*math.cos(self.angle)/2
            yb = yf - self.w_o*math.sin(self.angle)/2 + self.img.get_height()
        elif self.angle >= math.pi and self.angle < 3*math.pi/2:
            xb = xf - self.w_o*math.cos(self.angle)/2 - self.img.get_width()
            yb = yf + self.w_o*math.sin(self.angle)/2 + self.img.get_height()
        elif self.angle >= 3*math.pi/2 and self.angle < 2*math.pi:
            xb = xf + self.w_o*math.cos(self.angle)/2 - self.img.get_width()
            yb = yf - self.w_o*math.sin(self.angle)/2
        space.screen.blit(self.img, [xb, space.y_max-yb])
        # pygame.draw.circle(space.screen, [0,0,0], [xb, space.y_max-yb], 4)


class Bottle:
    List = []
    original_img = pygame.image.load("bottle.png")
    w_o = original_img.get_width()
    h_o = original_img.get_height()
    r = 0.05
    l = 0.2
    holded = True
    def __init__(self, arm, mass = 1.5):
        self.pos = [arm.pos[0], arm.pos[1] - Arm.h_o]
        self.pivot = arm.pivot[:]
        self.d = distant(self.pos,self.pivot)
        self.img = Bottle.original_img
        self.mass = mass
        self.inertia_cm = mass*(1/4*(Bottle.r)**2+1/12*Bottle.l**2)
        arm.bottle = self
        self.angle = arm.angle
        self.angular_vel = None
        self.vel = None
        self.move = True
        Bottle.List.append(self)
        return

    def update_by_arm(self, space, arm):
        self.angle = arm.angle
        self.pos[0] = arm.pos[0]+arm.h_o*math.sin(self.angle)
        self.pos[1] = arm.pos[1]-arm.h_o*math.cos(self.angle)
        self.draw_holding(space)
    
    def update(self, space, time):
        if self.holded:
            return
        if not self.move:
            self.draw_not_holding(space)
            return
        self.angle += self.angular_vel*time.dt
        if self.angle >= 2*math.pi:
            self.angle -= 2*math.pi
        elif self.angle < 0:
            self.angle += 2*math.pi
        self.vel[1] -= space.g*time.dt
        self.pos[1] += self.vel[1]*time.dt*500
        self.pos[0] += self.vel[0]*time.dt*500
        h = self.draw_not_holding(space)
        if self.pos[1] - h/2 <= 0 and self.move:
            self.move = False
        
    def draw_not_holding(self, space):
        self.img = pygame.transform.rotate(Bottle.original_img, self.angle*180/math.pi)
        w = self.img.get_width()
        h = self.img.get_height()
        xb = self.pos[0]-w/2
        yb = self.pos[1]+h/2
        space.screen.blit(self.img, [xb, space.y_max-yb])
        return h

    def draw_holding(self, space):
        self.img = pygame.transform.rotate(Bottle.original_img, self.angle*180/math.pi)
        xf = self.d*math.cos(self.angle+3/2*math.pi)+self.pivot[0]
        yf = self.d*math.sin(self.angle+3/2*math.pi)+self.pivot[1]
        if self.angle >= 0 and self.angle < math.pi/2:
            xb = xf - self.w_o*math.cos(self.angle)/2
            yb = yf + self.w_o*math.sin(self.angle)/2
        elif self.angle >= math.pi/2 and self.angle < math.pi:
            xb = xf + self.w_o*math.cos(self.angle)/2
            yb = yf - self.w_o*math.sin(self.angle)/2 + self.img.get_height()
        elif self.angle >= math.pi and self.angle < 3*math.pi/2:
            xb = xf - self.w_o*math.cos(self.angle)/2 - self.img.get_width()
            yb = yf + self.w_o*math.sin(self.angle)/2 + self.img.get_height()
        elif self.angle >= 3*math.pi/2 and self.angle < 2*math.pi:
            xb = xf + self.w_o*math.cos(self.angle)/2 - self.img.get_width()
            yb = yf - self.w_o*math.sin(self.angle)/2
        space.screen.blit(self.img, [xb, space.y_max-yb])

S1 = Space()
T1 = Time()
arm = Arm()
Bottle(arm)
angle = 0
running = True
while running:
    T1.update()
    S1.update()
    arm.update(S1, T1)
    for bot in Bottle.List:
        bot.update(S1, T1)
    pygame.display.update()
    T1.clock.tick(int(1/T1.dt))

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == 1073741903: #Derecha
                arm.give_torque = 50
            elif event.key == 1073741904: #Izquierda
                arm.give_torque = -50
        elif event.type == pygame.KEYUP:
            if event.key == 1073741903: #Derecha
                arm.give_torque = 0
            elif event.key == 1073741904: #Izquierda
                arm.give_torque = 0
            elif event.key == 32: #Space
                if arm.bottle:
                    arm.unhold()
            elif event.key == 98: #b
                if not arm.bottle:
                    Bottle(arm)

        elif event.type == pygame.QUIT:
            pygame.quit()
            running = False
