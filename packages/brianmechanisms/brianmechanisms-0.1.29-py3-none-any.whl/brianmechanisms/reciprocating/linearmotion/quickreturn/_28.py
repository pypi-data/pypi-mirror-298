import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from ....utils import bmutils

class mechanism28(bmutils):
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
        self.previous_section_type = 0 # it starts with section 0 
        self.current_section_theta = 0
        self.previous_section_theta = 0
        # self.theta_limits = settings["theta_limits"]
        # self.perimeter_theta = settings["perimeter_theta"]
        self.setup_plot()

    def setup_plot(self):
        self.ax.set_title(f'Mechanism 28')
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

        if theta == 0:
            self.previous_section_type = 0
            self.previous_section_theta = 0
            self.previous_theta = 0
            self.current_section_theta = 0 # theta2 = theta3 = theta4
            self.theta_rack = 0
        d_theta_1 = theta - self.previous_theta
        self.previous_theta = theta


        x1, y1 = self.create_circle_section(self.R1, phase=theta)
        self.ax.plot(x1, y1, color='red', linestyle='dotted')
        x1, y1 = self.create_circle_section(self.R1, phase=theta, end_angle=0.2*np.pi) # marker (solid section)
        self.ax.plot(x1, y1, color='red', linestyle='-', linewidth=5)

        
        # check descriptions of these in settings method
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

        segment_instances = self.settings["segment_instances"]
        

        
        '''
        Since there will be just a single instance of these (single planet), adjust the calculation of rack position to use theta_A rather than d_theta_A since sometimes d_theta is greater than max for that section.
        That is the easier way of doing it for a single planet system.
        '''
        for index, instance in enumerate(self.instances):
            self.__dict__.update(instance)
            if theta == 0:
                self.theta = 0
            self.theta += d_theta_1

            ## initialize for each instance
            R2_center =   [R1+R2  , 0]
            R_intersect = [R1+2*R2, 0] # this point is on circumference of R_B

            centerx, centery = self.rotate_points(self.phase_6, [R2_center[0]],[R2_center[1]], [0,0])
            R2_center = [centerx[0],centery[0]]
            centerx, centery = self.rotate_points(self.phase_6, [R_intersect[0]],[R_intersect[1]], [0,0])
            R_intersect = [centerx[0],centery[0]]

            theta_2 = - R1/R2 * self.theta # self.theta is theta of R1
            theta_A = -theta_2 * R3 / R_A #+ self.theta_D/2 # total theta_A (Annulus)
            centerx, centery = self.rotate_points(theta_A, [R2_center[0]],[R2_center[1]], [0,0]) # it is starting at the wrong
            R2_center = [centerx[0],centery[0]]
            self.ax.plot([R2_center[0]], [R2_center[1]], 'ro')

            centerx, centery = self.rotate_points(theta_A, [R_intersect[0]],[R_intersect[1]], [0,0]) # on fixed annulus. 
            R_intersect = [centerx[0],centery[0]]
            # self.ax.plot([R_intersect[0]], [R_intersect[1]], 'ro')
           
            x2, y2 = self.create_circle_section(self.R2, phase=theta_2)
            x3, y3 = self.create_circle_section(self.R3, phase=theta_2)
            self.ax.plot(x2+R2_center[0], y2+R2_center[1], color='red', linestyle='dotted')
            self.ax.plot(x3+R2_center[0], y3+R2_center[1], color='black', linestyle='dotted')

            sections_max_thetas =[
                [segment_instance["section_max_theta"] for segment_instance in segment_instances if segment_instance["type"] == self.previous_section_type][0],
                [segment_instance["section_max_theta"] for segment_instance in segment_instances if segment_instance["type"] != self.previous_section_type][0],
            ]
            section_types = [
                [segment_instance["type"] for segment_instance in segment_instances if segment_instance["type"] == self.previous_section_type][0],
                [segment_instance["type"] for segment_instance in segment_instances if segment_instance["type"] != self.previous_section_type][0],
            ]
            remaining_for_previous_section =  sections_max_thetas[0] - self.previous_section_theta # the angle that we needed to add to fill previous section
            index = 0
            d_theta_2 = R1/R2 * d_theta_1
            previous_section_theta = self.previous_section_theta
            while d_theta_2 > 0 : # we are currently only working with positive d_thetas
                binary_index = (index)%2
                section_theta_max = sections_max_thetas[binary_index]
                remaining_for_previous_section =  section_theta_max - previous_section_theta
                used_in_section = d_theta_2 if d_theta_2 <= remaining_for_previous_section else remaining_for_previous_section
                d_theta_2 -= used_in_section
                total_section_theta = previous_section_theta + used_in_section
                previous_section_theta = total_section_theta if total_section_theta < section_theta_max else 0
                self.previous_section_theta = previous_section_theta

                binary_index_next = (index)%2
                self.previous_section_type =  section_types[binary_index] if previous_section_theta != 0 else section_types[binary_index_next]

                current_section_type = section_types[binary_index]

                # active_segment_type = [segment_instance["type"] for segment_instance in segment_instances if segment_instance["type"] == current_section_type][0]

                if current_section_type == 0: 
                    active_rack_r = R_B
                    active_planet_r = R2
                    not_active_rack_r = R_S
                    not_active_planet_r = R4
                else:
                    active_rack_r = R_S
                    active_planet_r = R4
                    not_active_rack_r = R_B
                    not_active_planet_r = R2
                    # self.ax.plot([R_intersect[0]], [R_intersect[1]], 'ro') 
                    
                d_theta_rack = used_in_section * R3/R_A - used_in_section * active_planet_r/active_rack_r #
                self.theta_rack += d_theta_rack                
                index+=1


            # if instance["type"] == 0:
            self.ax.plot(x2+R2_center[0], y2+R2_center[1], color='green', linestyle=':')
            x2, y2 = self.create_circle_section(self.R2, phase=theta_2, end_angle=0.1*np.pi)
            self.ax.plot(x2+R2_center[0], y2+R2_center[1], color='green', linestyle='-', linewidth=4)
            # else:           
            x4, y4 = self.create_circle_section(self.R4, phase=theta_2)
            self.ax.plot(x4+R2_center[0], y4+R2_center[1], color='blue', linestyle='--')
            x2, y2 = self.create_circle_section(self.R2, phase=theta_2, end_angle=0.1*np.pi)
            self.ax.plot(x2+R2_center[0], y2+R2_center[1], color='red', linestyle='-', linewidth=4)
            
            for key, value in self.__dict__.items():
                if key in instance:  # Check if the key exists in the instance
                    instance[key] = value  # Update the dictionary
                elif hasattr(instance, '__dict__') and key in vars(instance):
                    setattr(instance, key, value)

        segment_endpoints = []
        for instance in segment_instances:
            if instance["type"] == 0:
                active_r = self.R_B
                color = "green"
            else:
                active_r = self.R_S
                color = "blue"
            x_i, y_i = self.create_circle_section(active_r, phase=self.phase_6+self.theta_rack + instance["theta"], end_angle=self.theta_D)
            instance["segment"] = [x_i, y_i]
            self.ax.plot(x_i, y_i, color=color, linestyle='--',)
            
            segment_endpoints.append([x_i[-1], y_i[-1]])
            segment_endpoints.append([x_i[0], y_i[0]])

        for index, point in enumerate(segment_endpoints): # the lines conneting end of R_B to beginning of R_S
            if index%2 == 0:
                continue
            next_point_index = index+1 if (index+1) < len(segment_endpoints) else 0
            next_point = segment_endpoints[next_point_index]

            # Draw lines between the points
            self.ax.plot([point[0],next_point[0]],[point[1],next_point[1]] , color='black') 
            # break
            
        x_External, y_External = self.create_circle_section(R_External, phase=self.phase_6+self.theta_rack)
        self.ax.plot(x_External, y_External, color='black',linestyle='--')
        
        # ''' Markers '''
        x_External, y_External = self.create_circle_section(R_External, phase=self.phase_6+self.theta_rack, end_angle=0.1*np.pi)
        self.ax.plot(x_External, y_External, color='black', linestyle='-', linewidth=5)
        
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
        R_S = R1 + R2 + R4 # R_Small. Moves mechanism forward in contrast to R_Big which moves it backwards

        R_External = R_B * 1.2

        theta_3_perimeter = 2*np.pi * R_A / R3
        s_2_perimeter = theta_3_perimeter * R2
        theta_1_perimeter = s_2_perimeter / R1
        perimeter_theta = theta_1_perimeter
        animation_rounds = int(animation_rounds * perimeter_theta)
        num_instances = num_hands
        theta_points = [(perimeter_theta/num_instances) * i for i in range(num_instances)]
        instances = [{"theta":0}]
        # for sections on R_B(ig) and R_S(mall)
        s_section_B = theta_D * R_B
        s_section_S = theta_D * R_S
        theta_max_B = s_section_B/R2 # both theta2 and theta3 since they are equal, being co-axial
        theta_max_S = s_section_S/R4 # both theta4 and theta2
        section_max_theta = [theta_max_B,theta_max_S ] # theta_3s
        segment_instances = [{"theta":theta, "type":index%2, "section_max_theta":section_max_theta[index%2]} for index, theta in enumerate(theta_points)]
        for index, instance in enumerate(instances):
            instance["previous_direction"] = 1

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
            "segment_instances":segment_instances,
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