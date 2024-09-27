import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class mechanism23:
    def __init__(self, settings):
        self.settings = settings
        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        self.ani = None

        # Extract parameters from settings
        self.R1 = self.settings['R1']
        self.R2 = self.settings['R2']
        self.R3 = self.settings['R3']
        self.R4 = self.settings['R4']
        self.L = self.settings['L']
        self.centers = self.settings['centers']
        self.origin = self.settings['origin']
        self.bar_length = self.L * 2
        self.bar_height = self.R4
        self.bar_height_max_disp = 0.5
        # self.x = 0
        # self.previous_theta = 0
        # self.direction = 1
        # self.previous_direction = 1
        # self.arm_angle = 0
        self.instances = settings["instances"]
        self.setup_plot()


    def setup_plot(self):
        self.ax.set_xlim(self.settings['x_limits'][0], self.settings['x_limits'][1])
        self.ax.set_ylim(-2 * self.R4, 2 * self.R4)
        self.ax.axhline(0, color='black', linewidth=0.5, linestyle='--')
        self.ax.grid()
        self.ax.set_aspect('equal')

    def create_circle_section(self, r, num_points=100, start_angle=0, end_angle=2 * np.pi, phase=0):
        theta = np.linspace(start_angle + phase, end_angle + phase, num_points)
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        return x, y
    
    # Function to find the closest point on a line segment to a point
    def closest_point_on_segment(self, px, py, x1, y1, x2, y2):
        # Vector from x1,y1 to x2,y2
        segment_vec = np.array([x2 - x1, y2 - y1])
        segment_length_sq = np.dot(segment_vec, segment_vec)

        if segment_length_sq == 0:  # x1, y1 and x2, y2 are the same point
            return x1, y1

        # Project point onto the line segment, computing t
        t = np.dot(np.array([px - x1, py - y1]), segment_vec) / segment_length_sq
        t = np.clip(t, 0, 1)  # Clamp t to the segment
        closest_x = x1 + t * segment_vec[0]
        closest_y = y1 + t * segment_vec[1]
        return closest_x, closest_y
    
    # Find the closest point on the cam profile
    def cam_is_active(self, cam_x_values, cam_y_values, midpoint, line, line_floating, perpendicular, perpendicular_floating, cam_distance):
        x_perpendicular,y_perpendicular = perpendicular
        x_line, y_line = line
        x_line_floating, y_line_floating = line_floating
        x_new_line_floating, y_new_line_floating = perpendicular_floating
        midpoint_x, midpoint_y = midpoint
        midpoint_x_o, midpoint_y_o = midpoint
        closest_dist = float('inf')
        closest_point = (None, None)

        centers = self.centers
        if self.x == centers[0] or self.x == centers[-1]:
                rotation_theta = self.arm_angle if self.direction == 1 else self.arm_angle + np.pi
                rotation_matrix = np.array([[np.cos(rotation_theta), -np.sin(rotation_theta)],
                                        [np.sin(rotation_theta), np.cos(rotation_theta)]])
                rotation_center = centers[0] if midpoint_x < 0 else centers[-1]
                midpoint_xs, midpoint_ys = self.rotate_points(rotation_matrix, [midpoint_x], [midpoint_y], rotation_center, 0)
                midpoint_x = midpoint_xs[0]
                midpoint_y = midpoint_ys[0]
                x_line, y_line = self.rotate_points(rotation_matrix, x_line, y_line, rotation_center, 0)
                x_line_floating, y_line_floating = self.rotate_points(rotation_matrix, x_line_floating, y_line_floating, rotation_center, 0)
                x_new_line_floating, y_new_line_floating = self.rotate_points(rotation_matrix, x_new_line_floating, y_new_line_floating, rotation_center, 0)
                x_perpendicular,y_perpendicular = self.rotate_points(rotation_matrix, x_perpendicular,y_perpendicular, rotation_center, 0)
        
        else:
            if self.direction != self.previous_direction:
                rotation_theta = -np.pi #if self.direction == -1 else 0
                rotation_matrix = np.array([[np.cos(rotation_theta), -np.sin(rotation_theta)],
                                 [np.sin(rotation_theta), np.cos(rotation_theta)]])
                rotation_center = self.x # centers[0] if midpoint_x < 0 else centers[-1]
                midpoint_xs, midpoint_ys = self.rotate_points(rotation_matrix, [midpoint_x], [midpoint_y], rotation_center, 0)
                midpoint_x = midpoint_xs[0]
                midpoint_y = midpoint_ys[0]
                x_line, y_line = self.rotate_points(rotation_matrix, x_line, y_line, rotation_center, 0)
                x_line_floating, y_line_floating = self.rotate_points(rotation_matrix, x_line_floating, y_line_floating, rotation_center, 0)
                x_new_line_floating, y_new_line_floating = self.rotate_points(rotation_matrix, x_new_line_floating, y_new_line_floating, rotation_center, 0)
                x_perpendicular,y_perpendicular = self.rotate_points(rotation_matrix, x_perpendicular,y_perpendicular, rotation_center, 0)

        for i in range(len(cam_x_values) - 1):
            x1, y1 = cam_x_values[i], cam_y_values[i]
            x2, y2 = cam_x_values[i + 1], cam_y_values[i + 1]
            closest_x, closest_y = self.closest_point_on_segment(midpoint_x, midpoint_y, x1, y1, x2, y2)
            
            # Calculate distance from the midpoint to the closest point
            dist = np.sqrt((closest_x - midpoint_x) ** 2 + (closest_y - midpoint_y) ** 2)
            
            if dist < closest_dist:
                closest_dist = dist
                closest_point = (closest_x, closest_y)

            if closest_dist > (cam_distance):
                cam_active = False
            else:
                cam_active = True

        return cam_active, [midpoint_x, midpoint_y], closest_point, [x_line, y_line], [x_line_floating, y_line_floating], [x_perpendicular, y_perpendicular], [x_new_line_floating, y_new_line_floating]
    
    def rotate_points(self, rotation_matrix, x_points, y_points, center_x, center_y):
            # Convert lists to numpy arrays
            x_points = np.array(x_points)
            y_points = np.array(y_points)

            # Translate points to the origin
            translated_x = x_points - center_x
            translated_y = y_points - center_y
            
            # Rotate points
            rotated = rotation_matrix @ np.array([translated_x, translated_y])
            
            # Translate points back
            return rotated[0] + center_x, rotated[1] + center_y

    def plot(self, theta = 0):    
        self.ax.set_title(f'Mechanism 23')
        self.ax.set_xlim(self.settings['x_limits'][0], self.settings['x_limits'][1])
        self.ax.set_ylim(-2 * self.R4, 2 * self.R4)
        self.ax.axis("off")
        theta_g = theta
        for index, instance in enumerate(self.instances):    
            self.__dict__.update(instance)
            
            theta = theta_g + self.theta_offset
            theta_R2 = -theta
            x1, y1 = self.create_circle_section(self.R1, phase=theta_R2)
            x2, y2 = self.create_circle_section(self.R2, phase=theta_R2)
            
            
            centers = self.centers
            if index == 1: # plot only once
                for i,center in enumerate(centers): # the compound gears
                    self.ax.plot(x1+center, y1, color='black', linestyle='--')
                    self.ax.plot(x2+center, y2, color='red', linestyle='--')
            
            # the cam profiles
            x3, y3 = self.create_circle_section(self.R3, end_angle=np.pi*0.8, phase=np.pi/2+0.2*np.pi)
            x4, y4 = self.create_circle_section(self.R4, end_angle=np.pi*0.8, phase=np.pi/2)
            x3_b, y3_b = self.create_circle_section(self.R3, end_angle=np.pi*0.8, phase=-np.pi/2)
            x4_b, y4_b = self.create_circle_section(self.R4, end_angle=np.pi*0.8, phase=-np.pi/2+0.2*np.pi)

            d_x = 0

            d_theta = theta - self.previous_theta
            self.previous_theta = theta

            cam1_block = True
            cam2_block = True
            if cam1_block: # for readability
                cam1_x_values = np.concatenate([
                    x3 + centers[0], 
                    [centers[0], centers[-1]],
                    x3_b + centers[-1],
                ])
                cam1_y_values = np.concatenate([
                    y3, 
                    [-self.R3, -self.R3],
                    y3_b, 
                ])
                self.ax.plot(cam1_x_values, cam1_y_values, color='black', linestyle='-') # cam profile 1

                x_line = [-self.bar_length/2+self.x, self.bar_length/2+self.x]
                y_line = [-self.R1*self.previous_direction, -self.R1*self.previous_direction]
                y_line_floating = [-self.R1*self.previous_direction-self.bar_height_max_disp* self.previous_direction, -self.R1*self.previous_direction-self.bar_height_max_disp* self.previous_direction]

                # Calculate midpoint
                midpoint_x = (x_line[0] + x_line[1]) / 2
                midpoint_y = (y_line[0] + y_line[1]) / 2

                # Length of the new line
                length = self.R4

                x_new_line = [midpoint_x, midpoint_x]
                y_new_line =          [midpoint_y , midpoint_y - length *self.previous_direction]
                y_new_line_floating = [midpoint_y -self.bar_height_max_disp* self.previous_direction, midpoint_y - length *self.previous_direction-self.bar_height_max_disp* self.previous_direction]

                x_line_floating = x_line.copy()
                x_new_line_floating = x_new_line.copy()
                cam1_active, midpoint, closest_point, [x_line, y_line],[x_line_floating,y_line_floating], [x_new_line,y_new_line],[x_new_line_floating, y_new_line_floating]= self.cam_is_active(cam1_x_values, cam1_y_values, [midpoint_x, midpoint_y],[x_line, y_line],[x_line_floating,y_line_floating], [x_new_line,y_new_line], [x_new_line_floating, y_new_line_floating],self.R3 - self.R1)
                if cam1_active:
                    # ____1
                    self.ax.plot([midpoint[0], closest_point[0]], [midpoint[1], closest_point[1]], color='green', linestyle='--')
                    self.ax.plot(closest_point[0], closest_point[1], 'ko') 
                    d_x = self.R1 * d_theta

                else:
                    y_line = y_line_floating.copy()
                    x_line = x_line_floating.copy()
                    x_new_line = x_new_line_floating.copy()
                    y_new_line = y_new_line_floating.copy()

                x_1_line = x_line
                y_1_line = y_line
                x_p_1_line = x_new_line
                y_p_1_line = y_new_line


            if cam2_block: # for readability
                cam2_x_values = np.concatenate([
                    x4_b + centers[-1],
                    [centers[0], centers[-1]],
                    x4 + centers[0], 
                ])
                cam2_y_values = np.concatenate([
                    y4_b, 
                    [self.R4, self.R4],
                    y4, 
                ])
                self.ax.plot(cam2_x_values, cam2_y_values, color='red', linestyle='-') # cam profile 2


                x_line = [-self.bar_length/2+self.x, self.bar_length/2+self.x]
                y_line = [-self.R2*self.previous_direction, -self.R2*self.previous_direction]
                y_line_floating = [-self.R2*self.previous_direction-self.bar_height_max_disp* self.previous_direction, -self.R2*self.previous_direction-self.bar_height_max_disp* self.previous_direction]

                # Calculate midpoint
                midpoint_x = (x_line[0] + x_line[1]) / 2
                midpoint_y = (y_line[0] + y_line[1]) / 2

                length_perpendicular = self.R4 

                x_perpendicular = [midpoint_x, midpoint_x]
                y_perpendicular =     [midpoint_y, midpoint_y - length_perpendicular*self.previous_direction]
                y_new_line_floating = [midpoint_y - self.bar_height_max_disp* self.previous_direction, midpoint_y - length_perpendicular*self.previous_direction - self.bar_height_max_disp* self.previous_direction]

                x_line_floating = x_line.copy()
                x_new_line_floating = x_perpendicular.copy()

                cam2_active, midpoint, closest_point, [x_line, y_line], [x_line_floating,y_line_floating], [x_perpendicular, y_perpendicular],[x_new_line_floating, y_new_line_floating]= self.cam_is_active(cam2_x_values, cam2_y_values, [midpoint_x, midpoint_y], [x_line, y_line],[x_line_floating,y_line_floating], [x_perpendicular,y_perpendicular],[x_new_line_floating, y_new_line_floating], self.R4 - self.R2)
                if cam2_active:
                    self.ax.plot([midpoint[0], closest_point[0]], [midpoint[1], closest_point[1]], color='blue', linestyle='--')
                    self.ax.plot(closest_point[0], closest_point[1], 'ro') 
                    d_x = self.R2 * d_theta
                else:
                    y_line = y_line_floating.copy()
                    x_line = x_line_floating.copy()
                    x_perpendicular = x_new_line_floating
                    y_perpendicular = y_new_line_floating

                x_2_line = x_line
                y_2_line = y_line
                x_p_2_line = x_perpendicular
                y_p_2_line = y_perpendicular
                    

            # we can handle the previous direction here....
            if self.direction != self.previous_direction:
                self.previous_direction = self.direction

            mod_arm_angle = self.arm_angle# % (-2*np.pi)
            if self.x == centers[0]:
                if -np.pi > self.arm_angle and self.arm_angle > -2*np.pi:
                    self.arm_angle = - np.pi
                elif self.arm_angle > 0:
                    self.arm_angle = 0
                elif self.arm_angle <= -2*np.pi:
                    self.arm_angle = 0
                mod_arm_angle = self.arm_angle
                if (mod_arm_angle) <= -np.pi:
                    self.direction = -1
                elif mod_arm_angle >= 0:
                    self.direction = 1
            if self.x == centers[-1]:
                if 0 > self.arm_angle and self.arm_angle > -np.pi:
                    self.arm_angle = -np.pi
                elif self.arm_angle < -2*np.pi:
                    self.arm_angle = -2*np.pi
                elif self.arm_angle >= 0:
                    self.arm_angle = -2*np.pi
                mod_arm_angle = self.arm_angle
                if (mod_arm_angle) >= -np.pi:
                    self.direction = -1
                elif (mod_arm_angle) <= -2*np.pi:
                    self.direction = 1
            
            d_x *= self.direction
            if self.x-d_x < centers[0] or (0 > self.arm_angle and self.arm_angle > -np.pi): # arm is rotating
                self.x = centers[0]
                self.arm_angle -= d_theta

                if -np.pi > self.arm_angle and self.arm_angle > -2*np.pi:
                    self.arm_angle = - np.pi
                elif self.arm_angle > 0:
                    self.arm_angle = 0
                elif self.arm_angle <= -2*np.pi:
                    self.arm_angle = 0
                
            elif self.x-d_x > centers[-1] or (-np.pi > self.arm_angle and self.arm_angle > -2*np.pi): # arm is rotating
                self.x = centers[-1]
                self.arm_angle -= d_theta

                if 0 > self.arm_angle and self.arm_angle > -np.pi:
                    self.arm_angle = -np.pi
                elif self.arm_angle < -2*np.pi:
                    self.arm_angle = -2*np.pi
                elif self.arm_angle >= 0:
                    self.arm_angle = -2*np.pi

            else:
                self.x-=d_x
            
            self.ax.plot(x_1_line, y_1_line, color='black', linestyle='-', linewidth=3)
            self.ax.plot(x_p_1_line, y_p_1_line, color='black', linestyle='-')
            self.ax.plot(x_2_line, y_2_line, color='red', linestyle='-', linewidth=3)
            self.ax.plot(x_p_2_line, y_p_2_line, color='red', linestyle='-')
            
            
            self.ax.plot(centers, [0] * len(centers), 'ro')
            for key, value in self.__dict__.items():
                if key in instance:  # Check if the key exists in the instance
                    instance[key] = value  # Update the dictionary
                elif hasattr(instance, '__dict__') and key in vars(instance):
                    setattr(instance, key, value)
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

    def show(self):
        plt.show()
        return self

    def save(self, fileName):
        if self.ani is not None:
            # writer = PillowWriter(fps=25)
            self.ani.save(f"{fileName}.gif", writer='PillowWriter') # how to set fps
        else:
            plt.savefig(f"{fileName}.png")
        return self

    @staticmethod
    def Settings(R1=1,R2=4.5,R3=9, R4=10, L=10, num_wheels=3, num_instances = 2, speed=0.25, animation_rounds=5):
        
        centers = [i * L for i in range(num_wheels)]
        # center the centers
        origin = centers[-1]/2
        centers[:] = [center - origin for center in centers] 
        x_limits = [centers[0]-2*R4,centers[-1]+2*R4]

        # instance params
        # the
            # self.x = 0
            # self.previous_theta = 0
            # self.direction = 1
            # self.previous_direction = 1
            # self.arm_angle = 0
            # self.theta_0 = 0
        ## calculate theta to complete the cirlce
        ## divide equally by the number of instances
        perimeter_theta = ((centers[-1] - centers[0] ))/R2 + ((centers[-1] - centers[0] )/R1) + (2*np.pi)
        theta_points = [(perimeter_theta/num_instances) * i for i in range(num_instances)]
        # calculate the corresponding xes
        theta_section1 = (((centers[-1] - centers[0] ))/2)/R1
        theta_section2 = theta_section1 + np.pi
        theta_section3 = theta_section2 + ((centers[-1] - centers[0] ))/R2
        theta_section4 = theta_section3 + np.pi
        theta_section5 = theta_section4 + (((centers[-1] - centers[0] ))/2)/R1
        theta_sections = [theta_section1, theta_section2, theta_section3, theta_section4, theta_section5]
        x_limits1 = -(centers[-1] - centers[0] ) /2 
        x_limits2 = x_limits1 
        x_limits3 = (centers[-1] - centers[0] )/2
        x_limits4 = x_limits3
        x_limits5 = 0

        animation_rounds = int(animation_rounds * perimeter_theta)

        def get_x(theta): # [x, direction, theta, arm_angle]
            theta = theta % perimeter_theta
            if 0 <=theta and theta < theta_sections[0]:
                return [0 - theta * R1, 1, -theta, 0] 
            elif theta_sections[0] <= theta and theta < theta_sections[1]:
                return [x_limits1,1 , -theta, -(theta-theta_sections[0])]
            elif theta_sections[1] <theta and theta < theta_sections[2]:
                return [x_limits2 + (theta - theta_section2) * R2 ,-1, -theta, -np.pi]
            elif theta_sections[2] <theta and theta < theta_sections[3]:
                return [x_limits3,-1, -theta, -np.pi - (theta-theta_section3)]
            else:
                return [x_limits3 - (theta - theta_section4) * R1,1, -theta, -2*np.pi]
            
        starting_xes = [get_x(theta) for theta in theta_points]
        instances = [{"x":instance[0], "direction":instance[1], "theta":instance[2], "arm_angle":instance[3],} for instance in starting_xes]
        for instance in instances:
            instance["previous_direction"] = instance["direction"]
            instance["previous_theta"] = instance["theta"]
            instance["theta_offset"] = instance["theta"]
        # print(instances)

        return {
            "R1": R1,
            "R2": R2,
            "R3": R3,
            "R4": R4,
            "L": L,
            "centers": centers,
            "origin":origin,
            "x_limits": x_limits,
            "instances": instances,
            "animation_rounds": animation_rounds,
            "speed": speed,
        }
    @staticmethod
    def info():
        description = (
            "Mechanism Description:\n"
            "-----------------------\n"
            "Multi-legged ULMW with quick return.\n"
            "**Applications**:\n"
            "This type of mechanism is intended to be used in the development of clamp-on self-actuated long-range linear motion mechanisms.\n"
        )
        return description