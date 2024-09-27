import numpy as np
import matplotlib.pyplot as plt

class bmutils:
    # def is_point_on_circle(self, R_intersect, x_B, y_B, tolerance=0.1, index=0):
    #     """
    #     Check if R_intersect falls on the circle defined by points (x_B, y_B).
        
    #     Parameters:
    #     R_intersect (list): The point to check, [x, y].
    #     x_B (array-like): X coordinates of the circle points.
    #     y_B (array-like): Y coordinates of the circle points.
    #     tolerance (float): Distance tolerance to consider for "on the circle".
        
    #     Returns:
    #     bool: True if R_intersect is on the circle, False otherwise.
    #     """
    #     for x, y in zip(x_B, y_B):
    #         distance = np.sqrt((R_intersect[0] - x) ** 2 + (R_intersect[1] - y) ** 2)
    #         # print(distance, index)
    #         if distance < tolerance:
    #             return True
    #     return False
    # def is_point_on_circle(self, point, x_arc, y_arc, tolerance=1e-5, index=0):
    def is_point_on_circle(self, point, x_arc, y_arc, tolerance=0.1):
        # Initialize variables to track the closest distance and point
        closest_distance = float('inf')
        closest_point = None

        # Iterate through pairs of points to find the closest segment
        for i in range(len(x_arc) - 1):
            # Get the current and next point
            p1 = (x_arc[i], y_arc[i])
            p2 = (x_arc[i + 1], y_arc[i + 1])
            
            # Project the point onto the line segment
            closest_on_segment = self.closest_point_on_segment(point, p1, p2)
            
            # Calculate the distance to this closest point
            distance = np.sqrt((closest_on_segment[0] - point[0])**2 + (closest_on_segment[1] - point[1])**2)
            
            # Update if this is the closest point so far
            if distance < closest_distance:
                closest_distance = distance
                closest_point = closest_on_segment

        # # Plot the closest point
        # if closest_distance <= tolerance:
        #     if closest_point is not None:
        #         self.ax.plot(closest_point[0], closest_point[1], 'go')  # __go__

        # Check if the closest distance is within the specified tolerance
        return closest_distance <= tolerance
    
    def closest_point_on_segment(self, point, p1, p2):
        # Vector from p1 to p2
        segment_vector = np.array(p2) - np.array(p1)
        # Vector from p1 to the point
        point_vector = np.array(point) - np.array(p1)

        # Project point_vector onto segment_vector
        segment_length_squared = np.dot(segment_vector, segment_vector)
        if segment_length_squared == 0:  # p1 and p2 are the same point
            return p1

        projection = np.dot(point_vector, segment_vector) / segment_length_squared
        projection = np.clip(projection, 0, 1)  # Clamp to the segment
        closest_point = p1 + projection * segment_vector

        return closest_point

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