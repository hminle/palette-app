class GlobalPalette:
    def __init__(self):
        self.original_palette = None
        self.current_palette = None
    
    def set_original_palette(self, palette):
        self.original_palette = palette
    
    def set_current_palette(self, palette):
        self.current_palette = palette