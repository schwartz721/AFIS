from plant_classes import Crop


class Simulation(object):
    def __init__(self):
        # on initialization, separate dicts are made for storing Long Cycle and Short Cycle crops
        # these dictionaries are used by draw_sim() to draw the plants on the canvas
        # frame_list stores Frame_Info objects which hold information about drawing the sidebar
        self.long_crop_dict = {}
        self.short_crop_dict = {}
        self.frame_list = []

    def resize(self, x, y, unit):
        # resize is called when starting a new simulation, or changing the dimensions of the plot
        self.x_dim = x
        self.y_dim = y
        self.unit = unit

    def add_crop(self, plant, planting_params, plant_year, color):
        # add_crop takes a plant type and the spacing parameters, creates a Crop object,
        # and stores it in the proper dictionary
        if type(plant).__name__ == 'Long_Cycle_Plant':
            key = 'L%d' % (max([int(i[1:]) for i in self.long_crop_dict.keys()], default=0) + 1)
            self.long_crop_dict[key] = Crop(plant, planting_params, plant_year, color)
            return key
        else:
            key = 'S%d' % (max([int(i[1:]) for i in self.short_crop_dict.keys()], default=0) + 1)
            self.short_crop_dict[key] = Crop(plant, planting_params, plant_year, color)
            return key


class Frame_Info(object):
    # holds info for drawing the sidebar, and the sidebar's edit/delete functionality
    def __init__(self, crop, key):
        self.crop = crop
        self.key = key
