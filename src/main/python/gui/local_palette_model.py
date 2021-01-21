
class LocalPaletteModel:

    def __init__(self):
        self.local_palettes = {} # RGB
        self.current_index = -1

    def add_local_palette(self,
                          local_palette, 
                          window_position):
        self.current_index += 1
        self.local_palettes[self.current_index] = {
            'local_palette': local_palette,
            'window_position': window_position
        }

    def get_palette(self, index: int):
        return self.local_palettes.get(index)

    def get_all_local_palettes(self):
        list_local_palettes = []
        for key in self.local_palettes.keys():
            list_local_palettes.append(self.local_palettes.get(key).get('local_palette'))
        return list_local_palettes

    def reset(self):
        # TODO: implement
        pass