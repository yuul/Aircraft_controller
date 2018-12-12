"""
Authored By: Ulysses Yu
Description: This creates an aircraft controller that works for two aircaft on an x/y plane
It can detect collisions and change direction accordingly
"""


class Controller:
    """
    This is the flight controller
    It has internal variables of x_dest, y_dest, direction, x, y
    """

    def __init__(self, destination_x, destination_y, start_x, start_y):
        """
        Initializes the destination
        """
        self.x_dest = destination_x
        self.y_dest = destination_y
        self.x = start_x
        self.y = start_y

    def set_dir(self, new_dir):
        """
        Sets the direction
        """
        self.direction = new_dir

    def set_location(self, new_x, new_y):
        """
        Sets the current location of the plane
        """
        self.x = new_x
        self.y = new_y

    def found_destination(self):
        return (self.x == self.x_dest) and (self.y == self.y_dest)

    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y

    def get_dir(self):
        return self.direction

    @staticmethod
    def calc_left_turn(direction):
        """
        Changes given a cardinal direction, returns the direction to the left
        """
        if direction == "W":
            ret_val = "S"
        elif direction == "S":
            ret_val = "E"
        elif direction == "E":
            ret_val = "N"
        else: # going north
            ret_val = "W"

        return ret_val

    @staticmethod
    def calc_right_turn(direction):
        """
        Changes given a cardinal direction, returns the direction to the right
        """
        if direction == "W":
            ret_val = "N"
        elif direction == "S":
            ret_val = "W"
        elif direction == "E":
            ret_val = "S"
        else: # going north
            ret_val = "E"

        return ret_val

    @staticmethod
    def next_location(x, y, direction):
        """
        Given a current location and a direction, moves in one step to that direction
        Returns the x and y coordinates for that new direction
        """
        new_x = x
        new_y = y

        if direction == "W":
            new_x = new_x - 1
        elif direction == "S":
            new_y = new_y - 1
        elif direction == "E":
            new_x = new_x + 1
        else: # going north
            new_y = new_y + 1

        return new_x, new_y

    @staticmethod
    def range_detector(self, other_obj, sqr_range):
        """
        Inputs: the current controller, another controller object, and the sqr_range
        Outputs: a boolean indicating if the two controllers are in communication range
        The two controllers are in range if they are within sqr_range units of each other both x and y wise
        Thus, the boundary for each controller looks like a square with length sqr_range * 2
        Choose sqr_range = 2 for communication, sqr_range = 1 for collision
        """
        x_dist = abs(self.x - other_obj.x)
        y_dist = abs(self.y - other_obj.y)

        if x_dist <= sqr_range and y_dist <= sqr_range:
            return True
        else:
            return False

    def collision_free_destination(self):
        """
        This sets the path for the controller if the controller is not in range of another aircraft
        To do this, the controller checks if the aircraft is headed to the destination
        If it is, it stays on path
        If not, it turns towards the destination
        """

        x_difference = self.x_dest - self.x
        y_difference = self.y_dest - self.y

        #print("X difference: " + str(x_difference) + " Y difference: " + str(y_difference))
        if x_difference >= 0 and y_difference >= 0:

            # want to head either north or east
            if self.direction == "S":
                self.set_dir("E")
            elif self.direction == "W":
                self.set_dir("N")
            elif x_difference > y_difference:
                self.set_dir("E")
            else:
                self.set_dir("N")

        elif x_difference >= 0 and y_difference < 0:

            # want to head either south or east
            if self.direction == "W":
                self.set_dir("S")
            elif self.direction == "N":
                self.set_dir("E")
            elif x_difference > abs(y_difference):
                self.set_dir("E")
            else:
                self.set_dir("S")
                

        elif x_difference < 0 and y_difference >= 0:

            # want to head either north or west
            if self.direction == "E":
                self.set_dir("N")
            elif self.direction == "S":
                self.set_dir("W")
            elif abs(x_difference) > y_difference:
                self.set_dir("W")
            else:
                self.set_dir("N")

        else:

            # want to head either south or west
            if self.direction == "N":
                self.set_dir("W")
            elif self.direction == "E":
                self.set_dir("S")
            elif abs(x_difference) > abs(y_difference):
                self.set_dir("W")
            else:
                self.set_dir("S")

## this is the test script
new_controller = Controller(0, 0, 10, 20)
new_controller.set_dir("S")

while not(new_controller.found_destination()):

    new_controller.collision_free_destination()
    new_x, new_y = new_controller.next_location(new_controller.get_x(), new_controller.get_y(), new_controller.get_dir())
    print("(" + str(new_x) + ", " + str(new_y) + ")")
    # print("This is the new x: " + str(new_x) + " This is the new y: " + str(new_y))
    new_controller.set_location(new_x, new_y)

