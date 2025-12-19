class ReconstructionController():
    def __init__(self, main_window):
        self.main_window = main_window
        self.main_window.sidebar.item_list.items_list_updated.connect(self.apply_reconstruction)
        self.main_window.sidebar.speed_changed.connect(self.apply_reconstruction)
        # i assumed that all that needed are the new inputs values
        # if the phantom image data itself is needed, add signal 

    def apply_reconstruction(self):
        print(self.main_window.sidebar.speed_spin_box.value())
        print(self.main_window.sidebar.item_list.get_items())

