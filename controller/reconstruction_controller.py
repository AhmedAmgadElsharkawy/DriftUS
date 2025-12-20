class ReconstructionController():
    def __init__(self, main_window):
        self.main_window = main_window
        self.main_window.sidebar.item_list.items_list_updated.connect(self.apply_reconstruction)
        self.main_window.sidebar.speed_changed.connect(self.apply_reconstruction)
        
    def apply_reconstruction(self, _=None):
        # 1. Get the Assumed Speed of Sound from the Sidebar (User Input)
        assumed_speed = self.main_window.sidebar.speed_spin_box.value()

        # 2. Get the True Data (Time of Flight) from PhantomController
        phantom_ctrl = self.main_window.phantom_controller
        
        # Ensure data exists
        if phantom_ctrl.current_times is None:
            return 

        times = phantom_ctrl.current_times
        amps = phantom_ctrl.current_amps
        lateral_pos = phantom_ctrl.current_x 

        # 3. Calculate Reconstructed Depth
        # Formula: Depth = (Time * Assumed_Speed) / 2
        # If assumed_speed > true_speed (1540), objects appear deeper (Stretched)
        # If assumed_speed < true_speed (1540), objects appear shallower (Compressed)
        reconstructed_z = (times * assumed_speed) / 2.0

        # 4. Generate the Reconstructed Image
        # We reuse the scan conversion logic from the phantom controller.
        # CRITICAL: We pass cysts=None. We do NOT want to draw the "True" cysts.
        # We want the "voids" in the speckle pattern to appear distorted naturally.
        reconstructed_image = phantom_ctrl.points_to_image(
            lateral_pos, 
            reconstructed_z, 
            amps, 
            cysts=None 
        )

        # 5. Display the Image
        self.main_window.reconstructed_image_viewer.set_image(reconstructed_image)