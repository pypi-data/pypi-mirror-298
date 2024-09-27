import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from ....utils import bmutils

class mechanism26(bmutils):
    def __init__(self, settings):
        self.settings = settings
        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        self.ani = None

        # Extract parameters from settings
        self.R1 = self.settings['R1']
        self.R2 = self.settings['R2']
        self.R3 = self.settings['R3']
        self.R4 = self.settings['R4']
        self.R_S = self.settings['R_S']
        self.R_A = self.settings['R_A']
        self.R_B = self.settings['R_B']
        self.R_External = self.settings['R_External']
        self.theta_D = self.settings['theta_D']
        # self.theta_forward = self.settings['theta_forward']
        self.previous_theta = 0
        self.instances = settings["instances"]
        self.phase_6 = settings["phase_6"]
        self.theta_rack = 0
        # self.theta_limits = settings["theta_limits"]
        # self.perimeter_theta = settings["perimeter_theta"]
        self.setup_plot()

    def setup_plot(self):
        self.ax.set_title(f'Mechanism 26')
        self.ax.set_xlim(-self.R_B*2, self.R_B*2)
        self.ax.set_ylim(-self.R_B*2, self.R_B*2)
        self.ax.axhline(0, color='black', linewidth=0.5, linestyle='--')
        # self.ax.grid()
        self.ax.axis("off")
        self.ax.set_aspect('equal')
        super().watermark(self.ax)
    
    def plot(self, theta = 0):    
        self.setup_plot()
        # the racks (fixed internal gears)
        x_A, y_A = self.create_circle_section(self.R_A)
        self.ax.plot(x_A, y_A, color='black', linestyle='-.')
        self.ax.plot([0], [0], 'ro') 

        d_theta_1 = theta - self.previous_theta
        self.previous_theta = theta


        x1, y1 = self.create_circle_section(self.R1, phase=theta)
        self.ax.plot(x1, y1, color='red', linestyle='dotted')
        x1, y1 = self.create_circle_section(self.R1, phase=theta, end_angle=0.2*np.pi) # marker (solid section)
        self.ax.plot(x1, y1, color='red', linestyle='-', linewidth=5)

        
        R1 = self.R1
        R2 = self.R2
        R3 = self.R3
        R4 = self.R4
        R_S = self.R_S
        R_A = self.R_A
        R_B = self.R_B
        R_External = self.R_External
       


        ## rotate wheel about
        x_B, y_B = self.create_circle_section(self.R_B, phase=self.phase_6+self.theta_rack, end_angle=self.theta_D)
        
        for index, instance in enumerate(self.instances):
            self.__dict__.update(instance)
            self.theta += d_theta_1
            R2_center =   [R1+R2  , 0]
            R_intersect = [R1+2*R2, 0]

            centerx, centery = self.rotate_points(self.phase_6, [R2_center[0]],[R2_center[1]], [0,0])
            R2_center = [centerx[0],centery[0]]
            centerx, centery = self.rotate_points(self.phase_6, [R_intersect[0]],[R_intersect[1]], [0,0])
            R_intersect = [centerx[0],centery[0]]
            
            

            instance_theta = self.theta #+ d_theta_1
            if instance_theta != 0:
                direction = instance_theta/abs(instance_theta)
                self.previous_direction = direction
            else:
                direction = self.previous_direction
            self.previous_direction = direction
            instance_theta = direction * (abs(instance_theta) % (2*np.pi))


            d_theta_2 = - R1/R2 * self.theta # self.theta is theta of R1
            # d_theta_A = d_theta_2 * R2 / R_A
            d_theta_A = -d_theta_2 * R3 / R_A #+ self.theta_D/2
            # print(index, d_theta_A)
            # centerx, centery = self.rotate_points(instance_theta, [R2_center[0]],[R2_center[1]], [0,0])
            centerx, centery = self.rotate_points(d_theta_A, [R2_center[0]],[R2_center[1]], [0,0]) # it is starting at the wrong
            R2_center = [centerx[0],centery[0]]
            self.ax.plot([R2_center[0]], [R2_center[1]], 'ro')

            centerx, centery = self.rotate_points(d_theta_A, [R_intersect[0]],[R_intersect[1]], [0,0])
            R_intersect = [centerx[0],centery[0]]
            # self.ax.plot([R_intersect[0]], [R_intersect[1]], 'ro')

           
            x2, y2 = self.create_circle_section(self.R2, phase=d_theta_2)
            x3, y3 = self.create_circle_section(self.R3, phase=d_theta_2)
            self.ax.plot(x2+R2_center[0], y2+R2_center[1], color='red', linestyle='dotted')
            self.ax.plot(x3+R2_center[0], y3+R2_center[1], color='black', linestyle='dotted')

            


            if d_theta_A != 0:
                direction = d_theta_A/abs(d_theta_A)
            else:
                direction = 1
            d_theta_A = direction * (abs(d_theta_A) % 2*np.pi)
            theta_rack_start = self.theta_rack
            

            if theta_rack_start != 0:
                direction = theta_rack_start/abs(theta_rack_start)
            else:
                direction = 1
            theta_rack_start = direction * (abs(theta_rack_start) % 2*np.pi)
            theta_rack_stop = theta_rack_start + self.theta_D

            theta_rack_start = self.theta_rack
            theta_rack_start = theta_rack_start if theta_rack_start > 0 else theta_rack_start + 2* np.pi
            theta_rack_start = theta_rack_start if theta_rack_start < 2* np.pi else theta_rack_start - 2* np.pi
            


            # gear_is_active = (theta_rack_start <= d_theta_A and d_theta_A < theta_rack_stop)
            gear_is_active = self.is_point_on_circle(R_intersect, x_B, y_B)
            
            if gear_is_active:                
                _d_theta_2 = R1/R2 * d_theta_1
                if instance["type"] == 0:
                    active_rack_r = R_B
                    active_planet_r = R2
                    # print("active", index, instance["type"])
                else:
                    active_planet_r = R4
                    active_rack_r = R_S
                _d_theta_A = _d_theta_2 * R3/R_A - _d_theta_2 * active_planet_r/active_rack_r
                self.theta_rack += _d_theta_A

            if instance["type"] == 0:
                self.ax.plot(x2+R2_center[0], y2+R2_center[1], color='green', linestyle=':')
                x2, y2 = self.create_circle_section(self.R2, phase=d_theta_2, end_angle=0.1*np.pi)
                self.ax.plot(x2+R2_center[0], y2+R2_center[1], color='green', linestyle='-', linewidth=4)
            else:           
                x4, y4 = self.create_circle_section(self.R4, phase=d_theta_2)
                self.ax.plot(x4+R2_center[0], y4+R2_center[1], color='blue', linestyle='--')
                x2, y2 = self.create_circle_section(self.R2, phase=d_theta_2, end_angle=0.1*np.pi)
                self.ax.plot(x2+R2_center[0], y2+R2_center[1], color='red', linestyle='-', linewidth=4)

            
            
            for key, value in self.__dict__.items():
                if key in instance:  # Check if the key exists in the instance
                    instance[key] = value  # Update the dictionary
                elif hasattr(instance, '__dict__') and key in vars(instance):
                    setattr(instance, key, value)
        #     pass
        x_S, y_S = self.create_circle_section(self.R_S, phase=self.phase_6+self.theta_rack, end_angle=self.theta_D) # __check__ need to calculate end_angle depending on number of arms
        self.ax.plot(x_S, y_S, color='blue',linestyle='--')
        # x_B, y_B = self.create_circle_section(self.R_B, phase=self.phase_6+self.theta_rack, end_angle=self.theta_D) # __check__ need to calculate end_angle depending on number of arms
        self.ax.plot(x_B, y_B, color='green',linestyle='--')
        x_External, y_External = self.create_circle_section(R_External, phase=self.phase_6+self.theta_rack)
        self.ax.plot(x_External, y_External, color='black',linestyle='--')
        
        ''' Markers '''
        x_External, y_External = self.create_circle_section(R_External, phase=self.phase_6+self.theta_rack, end_angle=0.1*np.pi)
        self.ax.plot(x_External, y_External, color='black', linestyle='-', linewidth=5)

        x_External, y_External = self.create_circle_section(self.R_External, phase=self.phase_6+self.theta_rack, end_angle=self.theta_D)
        # Determine the start and end points of the segments
        start_S = (x_S[0], y_S[0])  # Start of the first segment
        end_S = (x_S[-1], y_S[-1])  # End of the first segment
        start_B = (x_External[0], y_External[0])  # Start of the second segment
        end_B = (x_External[-1], y_External[-1])  # End of the second segment

        # Draw lines between the points
        self.ax.plot([start_S[0], start_B[0]], [start_S[1], start_B[1]], color='black') 
        self.ax.plot([end_S[0], end_B[0]], [end_S[1], end_B[1]], color='black')  

        return self
    
    def update(self, interval=100, frames=100):
        speed = self.settings["speed"]
        len = self.settings["animation_rounds"]
        displacements = np.linspace(0, len, int(250/speed))
        # displacements = np.concatenate([displacements, displacements[::-1]])  # Reverse motion
        def animate(displacement):
            self.ax.clear()
            self.plot(displacement)

        
        self.setup_plot()
        self.ani = animation.FuncAnimation(self.fig, lambda displacement: animate(displacement), frames=displacements, interval=50, repeat=True)
        return self
        

    @staticmethod
    # return_speed: how many times return is faster than forward
    # frequency: number of oscillations of output per revolution of planet. Should be greater than one
    def Settings(R1=5,R2=20, return_speed=2, frequency = 1, animation_rounds=1, speed=1):
        num_hands = frequency *2
        theta_segment = 2*np.pi/num_hands # angle of rack segment used
        theta_D = theta_segment # theta_disk

        k = return_speed

        R_B = R1 + 2 * R2 # R_Big
        theta_2_R = theta_D * R_B / R2  # Disk 2 rotates through theta_2_R to cover distance of theta_D * R_B(entire length of rack)

        theta_D_R  = (1/(k+1) ) * theta_D
        theta_D_F = 2 * theta_D - theta_D_R

        theta_3_R = theta_2_R
        c = theta_D_R / theta_3_R
        R3 = (c * R1 + c * R2)/(1-c)
        R_A = R1 + R2 + R3  # R_Annulus
        

        theta_3_F = theta_D_F * R_A / R3
        theta_4_F = theta_3_F
        c = theta_D / theta_4_F

        R4 = c*(R1 + R2) / (1-c)
        R_S = R1 + R2 + R4

        R_External = R_B * 1.2

        theta_3_perimeter = 2*np.pi * R_A / R3
        s_2_perimeter = theta_3_perimeter * R2
        theta_1_perimeter = s_2_perimeter / R1
        perimeter_theta = theta_1_perimeter
        animation_rounds = int(animation_rounds * perimeter_theta)
        num_instances = num_hands
        theta_points = [(perimeter_theta/num_instances) * i for i in range(num_instances)]
        instances = [{"theta":theta, "type":index%2} for index, theta in enumerate(theta_points)]
        for index, instance in enumerate(instances):
            instance["previous_direction"] = 1

        
        # phase_6 = - theta_D_F/2 - theta_D_R/2 - np.pi/2
        phase_6 = - theta_D_R/2 - np.pi/2
        return {
            "R1": R1,
            "R2": R2,
            "R3": R3,
            "R4": R4,
            "R_S": R_S,
            "R_A": R_A,
            "R_B": R_B,
            "R_External": R_External,
            "theta_D": theta_D,
            # "theta_forward":theta_forward,
            "animation_rounds":animation_rounds,
            "speed":speed,
            "perimeter_theta":perimeter_theta,
            # "theta_limits":theta_limits,
            "instances":instances,
            "phase_6":phase_6,
            "frequency":frequency,
        }
    @staticmethod
    def info():
        description = (
            "Mechanism Description:\n"
            "-----------------------\n"
            "Continuous rotary to reciprocating rotary and/or linear motion with possible configuration for quick return.\n"
            "**Applications**:\n"
            "This type of mechanism is intended to be used in the development of clamp-on self-actuated long-range linear motion mechanisms.\n"
        )
        return description