import numpy as np
from model.cyst_item import CystItem

class PhantomController:
    def __init__(self, main_window):
        self.main_window = main_window
        self.main_window.sidebar.item_list.items_list_updated.connect(
            self.update_phantom
        )

        # Phantom properties
        self.true_speed = 1540.0  # m/s
        self.true_width = 0.08  # m
        self.max_depth = 0.08  # m

        # Generate initial phantom
        self.num_speckles = 50000
        self.speckles_x = (np.random.rand(self.num_speckles) - 0.5) * self.true_width

        self.speckles_z = np.random.rand(self.num_speckles) * self.max_depth

        self.speckles_amplitude = np.random.rand(self.num_speckles) * 0.2

        # Generate initial cysts (anechoic regions)
        self.cysts = []

        # Reconstruction Parameters
        self.current_times = None
        self.current_amps = None
        self.current_x = None

    
    def is_cyst_exists(self, cyst: CystItem):
        for existing_cyst in self.cysts:
            if existing_cyst['x'] == cyst.get_lateral() and existing_cyst['z'] == cyst.get_depth() and existing_cyst['radius'] == cyst.get_radius():
                return True
        return False
    
    def add_cyst(self, cyst: CystItem):
        self.cysts.append({"x": cyst.get_lateral(), "z": cyst.get_depth(), "radius": cyst.get_radius()})

    def delete_cyst(self, cyst: CystItem):
        for i, existing_cyst in enumerate(self.cysts):
            if existing_cyst['x'] == cyst.get_lateral() and existing_cyst['z'] == cyst.get_depth() and existing_cyst['radius'] == cyst.get_radius():
                del self.cysts[i]
                return

    def _point_in_cyst(self, x, z):
        """
        Check if a point (x, z) is inside any cyst.
        Returns the cyst index if inside, -1 otherwise.
        """
        for i, cyst in enumerate(self.cysts):
            dx = x - cyst['x']
            dz = z - cyst['z']
            dist = np.sqrt(dx**2 + dz**2)
            if dist <= cyst['radius']:
                return i
        return -1

    def update_phantom(self, points_list):
        """
        Combines background speckle with cysts.
        """

        # Remove speckles inside cysts (cysts are anechoic)
        speckles_x = self.speckles_x.copy()
        speckles_z = self.speckles_z.copy()
        speckles_amp = self.speckles_amplitude.copy()

        # Mask for points to keep (not inside cysts)
        valid_speckles = []
        for i in range(len(speckles_x)):
            cyst_idx = self._point_in_cyst(speckles_x[i], speckles_z[i])
            if cyst_idx == -1:
                valid_speckles.append(True)
            else:
                valid_speckles.append(False)

        valid_speckles = np.array(valid_speckles)
        speckles_x = speckles_x[valid_speckles]
        speckles_z = speckles_z[valid_speckles]
        speckles_amp = speckles_amp[valid_speckles]


        #  Calculate True Time of Flight
        self.current_times = (2 * speckles_z) / self.true_speed
        self.current_amps = speckles_amp
        self.current_x = speckles_x

        #  Generate "Ground Truth" Image
        # We visualize using the TRUE positions (total_x, total_z)
        image_matrix = self.points_to_image(speckles_x, speckles_z, speckles_amp)

        #  Send to Viewer
        self.main_window.phantom_image_viewer.set_image(image_matrix)

    def points_to_image(self, x, z, amp, img_w=512, img_h=512): 
        """
        Scan Conversion: Converts scatter points (x, z) into a 2D image grid.
        Cysts are rendered as anechoic (dark) regions.
        """
        # Create empty grid
        image = np.zeros((img_w, img_h))

        # Map real coordinates to grid indices
        x_idx = ((x + (self.true_width / 2)) / self.true_width * img_w).astype(int)

        # Z: 0 to max_depth -> 0 to img_h
        z_idx = (z / self.max_depth * img_h).astype(int)

        # Filter points that are out of bounds
        valid_mask = (x_idx >= 0) & (x_idx < img_w) & (z_idx >= 0) & (z_idx < img_h)

        x_idx = x_idx[valid_mask]
        z_idx = z_idx[valid_mask]
        amp = amp[valid_mask]

        # Accumulate amplitudes at the corresponding pixel locations
        np.add.at(image, (x_idx, z_idx), amp)


        # Apply Log Compression (Ultrasound images are always log-compressed)
        # Log(1 + pixel) to handle zeros safely
        image = np.log1p(image)

        image = np.rot90(image , k=1)
        return image
