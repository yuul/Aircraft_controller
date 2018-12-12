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
                return "E"
            elif self.direction == "W":
                return "N"
            elif x_difference > y_difference:
                return "E"
            else:
                return "N"

        elif x_difference >= 0 and y_difference < 0:

            # want to head either south or east
            if self.direction == "W":
                return "S"
            elif self.direction == "N":
                return "E"
            elif x_difference > abs(y_difference):
                return "E"
            else:
                return "S"
                

        elif x_difference < 0 and y_difference >= 0:

            # want to head either north or west
            if self.direction == "E":
                return "N"
            elif self.direction == "S":
                return "W"
            elif abs(x_difference) > y_difference:
                return "W"
            else:
                return "N"

        else:

            # want to head either south or west
            if self.direction == "N":
                return "W"
            elif self.direction == "E":
                return "S"
            elif abs(x_difference) > abs(y_difference):
                return "W"
            else:
                return "S"

    def with_collision_destination(self, other_obj):
        """
        This function accounts for potential collisions between the aircrafts in the x-y plane
        It sets a path by iterating through the list of possible paths for both planes and evaluating if they create
        unsafe paths.
        It takes as input the two planes and then returns the direction for both planes
        This function does not take into account route planning
        """
        possible_paths = [("L", "F"), ("L", "R"),
                            ("F", "L"), ("F", "F"), ("F", "R"),
                            ("R", "L"), ("R", "F")]
        
        cont1_curdir = self.direction
        cont2_curdir = other_obj.get_dir()
        i = 0
        colliding = True

        while i < len(possible_paths) and colliding:

            if possible_paths[i][0] == "L":
                cont1_curdir = self.calc_left_turn(cont1_curdir)
            elif possible_paths[i][0] == "R":
                cont1_curdir = self.calc_right_turn(cont1_curdir)
            
            if possible_paths[i][1] == "L":
                cont2_curdir = other_obj.calc_left_turn(cont2_curdir)
            elif possible_paths[i][1] == "R":
                cont2_curdir = other_obj.calc_right_turn(cont2_curdir)

            new1_x, new1_y = self.next_location(self.get_x(), self.get_y(), cont1_curdir)
            new2_x, new2_y = self.next_location(other_obj.get_x(), other_obj.get_y(), cont2_curdir)

            colliding = range_detector(new1_x, new1_y, new2_x, new2_y, 1)
            i = i + 1

        return cont1_curdir, cont2_curdir    
            
#############################################
# END CLASS
#############################################

def range_detector(first_x, first_y, second_x, second_y, sqr_range):
    """
    Inputs: the current controller, another controller object, and the sqr_range
    Outputs: a boolean indicating if the two controllers are in communication range
    The two controllers are in range if they are within sqr_range units of each other both x and y wise
    Thus, the boundary for each controller looks like a square with length sqr_range * 2
    Choose sqr_range = 2 for communication, sqr_range = 1 for collision
    """
    x_dist = abs(first_x - second_x)
    y_dist = abs(first_y - second_y)

    if x_dist <= sqr_range and y_dist <= sqr_range:
        return True
    else:
        return False

## this is the executions script
new_controller = Controller(0, 10, 0, -1)
new_controller.set_dir("S")
cont_2 = Controller(0, -10, 0, 1)
cont_2.set_dir("W")

while not(new_controller.found_destination()) or not(cont_2.found_destination()):

    comm_range = range_detector(new_controller.get_x(), new_controller.get_y(), cont_2.get_x(), cont_2.get_y(), 2)
    cont1_dest = new_controller.found_destination()
    cont2_dest = cont_2.found_destination()

    # checks if the controllers are in communication range
    if comm_range and not(cont1_dest) and not(cont2_dest):
        # print("Communication Range")
        cont1_path, cont2_path = new_controller.with_collision_destination(cont_2)

        # sets path to avoid collisions
        new_controller.set_dir(cont1_path)
        cont_2.set_dir(cont2_path)

        # calculates new locations and sets them
        new_x, new_y = new_controller.next_location(new_controller.get_x(), new_controller.get_y(), new_controller.get_dir())
        cont2_x, cont2_y = cont_2.next_location(cont_2.get_x(), cont_2.get_y(), cont_2.get_dir())
        new_controller.set_location(new_x, new_y)
        cont_2.set_location(cont2_x, cont2_y)

    else:
        # print("Not Communicating")

        # sets the path of controller one
        if not(cont1_dest):
            new_controller.set_dir(new_controller.collision_free_destination())
            new_x, new_y = new_controller.next_location(new_controller.get_x(), new_controller.get_y(), new_controller.get_dir())
            new_controller.set_location(new_x, new_y)

        # sets the path of controller two
        if not(cont2_dest):
            cont_2.set_dir(cont_2.collision_free_destination())
            cont2_x, cont2_y = cont_2.next_location(cont_2.get_x(), cont_2.get_y(), cont_2.get_dir())
            cont_2.set_location(cont2_x, cont2_y)

    if range_detector(new_controller.get_x(), new_controller.get_y(), cont_2.get_x(), cont_2.get_y(), 1) and not(cont1_dest) and not(cont2_dest):
        print("Planes collided!")

    print("Plane 1: (" + str(new_controller.get_x()) + ", " + str(new_controller.get_y()) + 
        ") Plane 2: (" + str(cont_2.get_x()) + ", " + str(cont_2.get_y()) + ")")