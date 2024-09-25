import numpy as np
import matplotlib.pyplot as plt

class bmutils:
    def watermark(self, ax):
        ax.text(0.5, 0.5, 'BrianMechanisms', transform=ax.transAxes,
                fontsize=40, color='gray', alpha=0.5,
                ha='center', va='center', rotation=30)
        
    def create_circle_section(self, r, num_points=100, start_angle=0, end_angle=2 * np.pi, phase=0):
        theta = np.linspace(start_angle + phase, end_angle + phase, num_points)
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        return x, y
    
    def rotate_points(self, theta_radians, x_points, y_points , center):
        center_x, center_y = center
        # x_points, y_points = points
        rotation_matrix = np.array([[np.cos(theta_radians), -np.sin(theta_radians)],
                                    [np.sin(theta_radians), np.cos(theta_radians)]])
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