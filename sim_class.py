from plant_classes import Crop


class Simulation(object):
    def __init__(self):
        # on initialization, separate dicts are made for storing Long Cycle and Short Cycle crops
        # these dictionaries are used by draw_sim() to draw the plants on the canvas
        # frame_list stores Frame_Info objects which hold information about drawing the sidebar
        self.crop_dict = {}
        self.start_year = 0

    def resize(self, x, y, unit):
        # resize is called when starting a new simulation, or changing the dimensions of the plot
        self.x_dim = x
        self.y_dim = y
        self.unit = unit

    def add_crop(self, plant, planting_params, plant_year, color):
        # add_crop takes a plant type and the spacing parameters, creates a Crop object,
        # and stores it in the proper dictionary
        if type(plant).__name__ == 'Long_Cycle_Plant':
            prefix = 'L'
        else:
            prefix = 'S'
        key = '%s%d' % (prefix, (max([int(i[1:]) for i in self.crop_dict.keys()], default=0) + 1))
        crop = Crop(plant, planting_params, plant_year, color)
        self.crop_dict[key] = crop
        return (key, crop)

    def all_crops(self, action):
        for crop in self.crop_dict.values():
            if isinstance(action, int):
                crop.plant_year += action
            else:
                if action == 'unit change':
                    crop.unit_change(self.unit)
                crop.planting_params.position_crop(self.x_dim, self.y_dim)
