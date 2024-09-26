import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from ....utils import bmutils

class mechanism25(bmutils):
    def __init__(self, settings):
        self.settings = settings
        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        self.ani = None

        # Extract parameters from settings
        self.R1 = self.settings['R1']
        self.R2 = self.settings['R2']
        self.R3 = self.settings['R3']
        self.R4 = self.settings['R4']
        self.R5 = self.settings['R5']
        self.theta_forward = self.settings['theta_forward']
        self.previous_theta = 0
        self.instances = settings["instances"]
        self.theta_limits = settings["theta_limits"]
        self.perimeter_theta = settings["perimeter_theta"]
        self.setup_plot()

    def setup_plot(self):
        self.ax.set_title(f'Mechanism 25')
        self.ax.set_xlim(-self.R5*2, self.R5*2)
        self.ax.set_ylim(-self.R5*2, self.R5*2)
        self.ax.axhline(0, color='black', linewidth=0.5, linestyle='--')
        # self.ax.grid()
        self.ax.axis("off")
        self.ax.set_aspect('equal')
        super().watermark(self.ax)
    
    def plot(self, theta = 0):    
        self.setup_plot()
        # the racks (fixed internal gears)
        x5, y5 = self.create_circle_section(self.R5, end_angle = 2*np.pi - self.theta_forward, phase=-self.theta_forward/2)
        x4, y4 = self.create_circle_section(self.R4, end_angle = self.theta_forward, phase=-np.pi/2-self.theta_forward/2)
        self.ax.plot(x5, y5, color='black', linestyle='--')
        self.ax.plot(x4, y4, color='blue', linestyle='--')


        x1, y1 = self.create_circle_section(self.R1, phase=theta)
        self.ax.plot(x1, y1, color='red', linestyle='--')
        self.ax.plot([0], [0], 'ro') 
        x1, y1 = self.create_circle_section(self.R1, phase=theta, end_angle=0.2*np.pi) # marker (solid section)
        self.ax.plot(x1, y1, color='red', linestyle='-', linewidth=5)

        d_theta_1 = theta - self.previous_theta
        self.previous_theta = theta
        R1 = self.R1
        R2 = self.R2
        R3 = self.R3
        R4 = self.R4
        R5 = self.R5
        d_theta_2 = R1/R2 * d_theta_1
        d_theta_3 = d_theta_2
        d_theta_5 = R1/R2 * R3/R5 * d_theta_1
        d_theta_4 = R1/R4 * d_theta_1

        # R2_center = [0, -R1-R2]

        ## rotate wheel about
        for index, instance in enumerate(self.instances):
            self.__dict__.update(instance)
            self.theta += d_theta_1
            R2_center = [0, -R1-R2]
            
            instance_theta = self.theta #+ d_theta_1
            if instance_theta != 0:
                direction = instance_theta/abs(instance_theta)
                self.previous_direction = direction
            else:
                direction = self.previous_direction
            self.previous_direction = direction
            instance_theta = direction * (abs(instance_theta) % self.perimeter_theta)
            if instance_theta < 0 :
                instance_theta += self.perimeter_theta

            d_theta_2 = - R1/R2 * instance_theta
            # check the section where instance_theta is
            if 0 <= instance_theta and instance_theta < self.theta_limits[0]: # first section
                d_theta_4 = instance_theta * (R1/R2) * (R3/R4)
                # d_theta_4 = R1/R4 * instance_theta
                centerx, centery = self.rotate_points(d_theta_4, [R2_center[0]],[R2_center[1]], [0,0])
                R2_center = [centerx[0],centery[0]]
            elif self.theta_limits[0] <= instance_theta and instance_theta < self.theta_limits[1]:
                
                d_theta_5 = self.theta_forward/2 + R1/R5 * (instance_theta-self.theta_limits[0])
                centerx, centery = self.rotate_points(d_theta_5, [R2_center[0]],[R2_center[1]], [0,0])
                R2_center = [centerx[0],centery[0]]
            elif self.theta_limits[1] <= instance_theta and instance_theta < self.theta_limits[2]:
                # d_theta_4 = (2*np.pi - self.theta_forward/2) + R1/R4 * (instance_theta-self.theta_limits[1]) 
                d_theta_4 = (2*np.pi - self.theta_forward/2) + (instance_theta-self.theta_limits[1]) * (R1/R2) * (R3/R4)
                centerx, centery = self.rotate_points(d_theta_4, [R2_center[0]],[R2_center[1]], [0,0])
                R2_center = [centerx[0],centery[0]]
                pass

            x2, y2 = self.create_circle_section(self.R2, phase=d_theta_2)
            x3, y3 = self.create_circle_section(self.R3, phase=d_theta_2)
            # if index == 0: 
            self.ax.plot(x2+R2_center[0], y2+R2_center[1], color='blue', linestyle='--')
            self.ax.plot(x3+R2_center[0], y3+R2_center[1], color='black', linestyle='--')

            x2, y2 = self.create_circle_section(self.R2, phase=d_theta_2, end_angle=0.2*np.pi) # marker (solid section)
            x3, y3 = self.create_circle_section(self.R3, phase=d_theta_2, end_angle=0.05*np.pi) # marker (solid section)
            self.ax.plot(x2+R2_center[0], y2+R2_center[1], color='blue', linestyle='-', linewidth=5)
            self.ax.plot(x3+R2_center[0], y3+R2_center[1], color='black', linestyle='-', linewidth=5)
            # if index == 1: 
            #     self.ax.plot(x2+R2_center[0], y2+R2_center[1], color='blue', linestyle='--')
            #     self.ax.plot(x3+R2_center[0], y3+R2_center[1], color='green', linestyle='--')
            
            for key, value in self.__dict__.items():
                if key in instance:  # Check if the key exists in the instance
                    instance[key] = value  # Update the dictionary
                elif hasattr(instance, '__dict__') and key in vars(instance):
                    setattr(instance, key, value)
            pass

        return self
    
    def update(self, interval=100, frames=100):
        speed = self.settings["speed"]
        len = self.settings["animation_rounds"]
        displacements = np.linspace(0, len, int(250/speed))
        displacements = np.concatenate([displacements, displacements[::-1]])  # Reverse motion
        def animate(displacement):
            self.ax.clear()
            self.plot(displacement)

        
        self.setup_plot()
        self.ani = animation.FuncAnimation(self.fig, lambda displacement: animate(displacement), frames=displacements, interval=50, repeat=True)
        return self
        

    @staticmethod
    # theta_forward in radians
    # theta(offset) in perimeter fraction
    def Settings(R1=5,R2=4, theta_forward=0.5*np.pi, return_fraction=1/3, animation_rounds=2, speed=0.5, num_instances=2):
        w_forward = theta_forward/(1 - return_fraction)
        w_return = (2*np.pi-theta_forward)/(return_fraction)

        # R1 radius of sun
        # R2 Radius of smaller of the 2 in compound gear
        # R3 Radius of bigger of the 2 in compound gear
        k = w_return/w_forward
        R3 = R2 / k
        R4 = R1 + R2 + R3
        R5 = R1 + 2 * R2

        theta_limits = [] # theta for R1 to complete the various sections
        theta_1_section_1 = theta_forward/2 * (R2/R1) * (R4/R3)
        # print((R1/R2) * (R3/R4))

        theta_limits.append(theta_1_section_1) # OK
        theta_return = 2*np.pi - theta_forward
        s_limit_2_R5 = theta_return * R5
        # theta_3 = s_limit_2_R5/ R2

        theta_1_section_2 = s_limit_2_R5/R1 # theta_2 = theta_3
        theta_limits.append(theta_1_section_2+theta_1_section_1)
        theta_limits.append(theta_1_section_1+theta_1_section_2+theta_1_section_1)
        perimeter_theta = theta_limits[-1]
        animation_rounds = int(animation_rounds * perimeter_theta)
        theta_points = [(perimeter_theta/num_instances) * i for i in range(num_instances)]
        instances = [{"theta":theta, "rim_theta":((2*np.pi/num_instances )*index)} for index, theta in enumerate(theta_points)]
        for instance in instances:
            instance["previous_direction"] = 1
        # instances[0]["theta"] = perimeter_theta/2
        
        
        return {
            "R1": R1,
            "R2": R2,
            "R3": R3,
            "R4": R4,
            "R5": R5,
            "theta_forward":theta_forward,
            "animation_rounds":animation_rounds,
            "speed":speed,
            "perimeter_theta":perimeter_theta,
            "theta_limits":theta_limits,
            "instances":instances,
        }
    @staticmethod
    def info():
        description = (
            "Mechanism Description:\n"
            "-----------------------\n"
            "Continuous rotary motion with different constant velocities for different sections.\n"
            "**Applications**:\n"
            "This type of mechanism is intended to be used in the development of clamp-on self-actuated long-range linear motion mechanisms. and 2-spoke rimless wheels\n"
        )
        return description