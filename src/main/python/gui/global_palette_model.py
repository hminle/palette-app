import copy

class GlobalPaletteModel:

    def __init__(self):
        self.original_global_palette = None # Lab
        self.current_global_palette = None # Lab

    def set_palette(self, global_palette):
        if self.original_global_palette is None:
            self.original_global_palette = copy.deepcopy(global_palette)
        self.current_global_palette = global_palette

    def get_current_palette(self):
        return self.current_global_palette

    def get_original_palette(self):
        return self.original_global_palette

    def update_palette(self, chosen_color_Lab, palette_index):
        self.current_global_palette[palette_index] = chosen_color_Lab

    def reset(self):
        self.current_global_palette = copy.deepcopy(self.original_global_palette)