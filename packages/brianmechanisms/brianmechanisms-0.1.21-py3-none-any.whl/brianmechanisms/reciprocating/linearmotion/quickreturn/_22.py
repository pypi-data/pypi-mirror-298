import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class mechanism22:
    def __init__(self, settings):
        self.settings = settings
        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        self.ani = None

        # Extract parameters from settings
        self.R1 = self.settings['R1']
        self.R2 = self.settings['R2']
        self.R3 = self.settings['R3']
        self.L = self.settings['L']
        self.theta_R = self.settings['theta_R']
        self.theta_forward = self.settings['theta_forward']
        self.centers = self.settings['centers']
        self.displacement = self.settings['displacement']

        self.mobile_rack_xes = [-self.L,0]
        self.active_wheel_index = 0
        self.previous_active_wheel_index = 0
        self.previous_theta = 0
        self.cycle_theta = 0
        self.stroke_start_theta = 0

        self.setup_plot()

    def setup_plot(self):
        # max_radius = max(inst['radius1'] for inst in self.instances)
        self.ax.set_xlim(-self.L * 4, 4 * self.L)
        self.ax.set_ylim(-2 * self.R3, 2 * self.R3)
        self.ax.axhline(0, color='black', linewidth=0.5, linestyle='--')
        self.ax.grid()
        self.ax.set_aspect('equal')

    def create_circle_section(self, r, num_points=100, start_angle=0, end_angle=2 * np.pi, phase=0):
        theta = np.linspace(start_angle + phase, end_angle + phase, num_points)
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        return x, y

    def plot(self, displacement=0):        
        self.ax.set_title(f'Mechanism 22')

        centers = [i * self.L - displacement for i in range(len(self.centers))]
        theta_R2 = displacement/self.R2
        x2, y2 = self.create_circle_section(self.R2, phase=theta_R2)
        x3, y3 = self.create_circle_section(self.R3, phase=theta_R2)
        x1, y1 = self.create_circle_section(self.R1, phase=theta_R2)
        
        for i,center in enumerate(centers):
            if i%2 ==0:
                self.ax.plot(x2+center, y2, color='black', linestyle='--')
                self.ax.plot(x3+center, y3, color='blue', linestyle='--')
            else:
                self.ax.plot(x2+center, y2, color='black', linestyle='--')
                self.ax.plot(x1+center, y1, color='green', linestyle='--')

            if self.mobile_rack_xes[0] <= center and center <= self.mobile_rack_xes[1]:
                self.active_wheel_index = i

        if self.previous_active_wheel_index != self.active_wheel_index:
            self.stroke_start_theta = theta_R2
            self.previous_active_wheel_index = self.active_wheel_index
            self.previous_theta = theta_R2
        # cycle_theta = theta_R2 - self.stroke_start_theta

        d_theta = theta_R2 - self.previous_theta
        self.previous_theta = theta_R2
        
        stroke_displacement = 0
        if self.active_wheel_index % 2 == 0:
            stroke_displacement = -((d_theta * self.R2) - d_theta * self.R3)
        else:
            stroke_displacement = -((d_theta * self.R2) - d_theta * self.R1)
        self.mobile_rack_xes[0] += stroke_displacement
        self.mobile_rack_xes[1] += stroke_displacement

        self.ax.plot([-self.L*4, self.L*4], [-self.R2, -self.R2], color='black', linestyle='--')
        
        # Set limits
        self.ax.set_ylim(-self.R3*2, self.R3*2)  # Adjust based on your specific needs
        self.ax.set_xlim(-self.L*4, 4*self.L)  # Adjust limits based on L

        # Annotations
        self.ax.set_title('Mechanism 22')
        self.ax.axis('off')
        self.ax.grid()
        self.ax.axhline(0, color='black', linewidth=0.5, linestyle='--')
        self.ax.plot(centers, [0] * len(centers), 'ro', label='Centers')  # Red dots at the centers
        self.ax.plot(centers, [0] * len(centers), 'r--')  # Red line through the centers

        mobile_rack_xes = self.mobile_rack_xes
        self.ax.plot(mobile_rack_xes, [-self.R3, -self.R3], color='blue', linestyle='--')
        self.ax.plot(mobile_rack_xes, [-self.R1, -self.R1], color='green', linestyle='--')
        self.ax.plot([mobile_rack_xes[0], mobile_rack_xes[0]], [-self.R1, -self.R3], color='pink', linestyle='--')
        self.ax.plot([mobile_rack_xes[1], mobile_rack_xes[1]], [-self.R1, -self.R3], color='pink', linestyle='-')
        return self

    def update(self, interval=100, frames=100):
        max = (self.settings["num_wheels"]-1)*150 /6
        max = int(max)
        displacements = np.linspace(0, (self.settings["num_wheels"]-1)*self.L, max)
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
            self.ani.save(f"{fileName}.gif", writer='Pillow') # how to set fps
        else:
            plt.savefig(f"{fileName}.png")
        return self

    @staticmethod
    def Settings(R2=3, R3=4, L=10, num_wheels=4, displacement=0):
        
        theta_R = L / R3
        # theta_forward = 2 * theta_R * (R3 / R2 - 1)
        theta_forward = theta_R * (2*R3 / R2 - 1)
        # Avoid division by zero for R1
        if theta_forward != 0:
            R1 = L / theta_forward
        else:
            R1 = np.nan
        
        # Horizontal dashed line from -L/2 to +L/2
        centers = [i * L for i in range(num_wheels)]
        return {
            "R1": R1,
            "R2": R2,
            "R3": R3,
            "L": L,
            "theta_R": theta_R,
            "theta_forward": theta_forward,
            "centers": centers,
            "displacement": displacement,
            "num_wheels": num_wheels,
        }
    
    @staticmethod
    def info():
        description = (
            "Mechanism Description:\n"
            "-----------------------\n"
            "This mechanism is a continuous linear motion into reciprocating linear motion.\n"
            "**Applications**:\n"
            "This type of mechanism is intended to be used in the development of clamp-on self-actuated long-range linear motion mechanisms.\n"
        )
        return description
