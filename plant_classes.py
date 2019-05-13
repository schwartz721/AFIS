class Long_Cycle_Plant(object):
    # a long cycle plant is a tree/vine/etc that grows year after year
    # the Long_Cycle_Plant class holds the growth parameters of the plant
    def __init__(self, name, diameter, height, max_diameter, max_height, diameter_rate,
                 height_rate, reqs, services):
        self.name = name
        self.radius = diameter / 2
        self.height = height
        self.max_radius = max_diameter / 2
        self.max_height = max_height
        self.radius_rate = diameter_rate / 2
        self.height_rate = height_rate
        self.reqs = reqs
        self.services = services


class Short_Cycle_Plant(object):
    # a short cycle plant is a plant that is planted and harvested each year
    # the Short_Cycle_Plant class holds the size info of the plant
    def __init__(self, name, diameter, height, max_diameter, max_height, reqs, services):
        self.name = name
        self.radius = diameter / 2
        self.height = height / 2
        self.max_radius = max_diameter / 2
        self.max_height = max_height / 2
        self.reqs = reqs
        self.services = services


class Planting_Params(object):
    # holds the parameters that determine the planting locations of a crop
    def __init__(self, crop_spacing, row_spacing, x_offset, y_offset, row_count, plot_x, plot_y):
        self.crop_spacing = crop_spacing
        self.row_spacing = row_spacing
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.repeat = row_count

        # position_crop function creates crop_locations attribute
        self.position_crop(plot_x, plot_y)

    def position_crop(self, x, y):
        # position_crop turns planting parameters into (x, y) coords for visualization.
        # x and y arguments are the dimensions of the plot
        self.crop_locations = []
        x_dim = x - self.x_offset
        y_dim = y - self.y_offset * 2
        # x_dim and y_sim are the plantable dimensions, inside the offset margins
        if self.repeat:
            row_count = int(min([self.repeat, x_dim // self.row_spacing + 1]))
        else:
            row_count = int(x_dim // self.row_spacing + 1)
        x_pos = [i * self.row_spacing + self.x_offset for i in range(row_count)]
        remainder = (y_dim % self.crop_spacing) / 2
        crop_count = int(y_dim // self.crop_spacing + 1)
        y_pos = [i * self.crop_spacing + self.y_offset + remainder for i in range(crop_count)]
        for x in x_pos:
            for y in y_pos:
                self.crop_locations.append((x, y))


class Crop(object):
    # a crop object holds the plant object, the planting parameters object,
    # and the planting year and color
    def __init__(self, plant, planting_params, plant_year, color):
        self.plant = plant
        self.planting_params = planting_params
        self.plant_year = plant_year
        self.color = color

    def size(self, year):
        if type(self.plant).__name__ == 'Long_Cycle_Plant':
            height = min([self.plant.height + self.plant.height_rate * (year - self.plant_year),
                          self.plant.max_height])
            radius = min([self.plant.radius + self.plant.radius_rate * (year - self.plant_year),
                          self.plant.max_radius])
            return (height, radius)
        else:
            height = (self.plant.height, self.plant.max_height)[int((year % 1) * 2)]
            radius = (self.plant.radius, self.plant.max_radius)[int((year % 1) * 2)]
            return (height, radius)
