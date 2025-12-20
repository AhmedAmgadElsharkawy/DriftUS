import numpy as np

class PhantomController:
    def __init__(self, main_window):
        self.main_window = main_window
        self.main_window.sidebar.item_list.items_list_updated.connect(
            self.update_phantom
        )

        # Phantom properties
        self.true_speed = 1540.0  # m/s
        self.true_width = 0.04  # m
        self.max_depth = 0.08  # m

        # Generate initial phantom
        self.num_speckles = 50000
        self.speckles_x = (np.random.rand(self.num_speckles) - 0.5) * self.true_width

        self.speckles_z = np.random.rand(self.num_speckles) * self.max_depth

        self.speckles_amplitude = np.random.rand(self.num_speckles) * 0.2

        # Generate initial cysts (anechoic regions with acoustic mismatch)
        self.cysts = self._generate_cysts()

        # Reconstruction Parameters
        self.current_times = None
        self.current_amps = None
        self.current_x = None

        # self.update_phantom([])

    def _generate_cysts(self):
        """
        Generate cyst objects (anechoic lesions with acoustic mismatch).
        Cysts are characterized by:
        - Low/no internal echoes (anechoic)
        - Acoustic shadow effect below them
        - Circular/elliptical shape
        """
        cysts = []
        # Define 2-3 cysts at different depths for good visualization
        # Each cyst: (center_x, center_z, radius)
        cysts.append({'x': -0.010, 'z': 0.025, 'radius': 0.004})  # Left cyst at mid-depth
        cysts.append({'x': 0.008, 'z': 0.045, 'radius': 0.005})   # Right cyst deeper
        cysts.append({'x': 0.002, 'z': 0.062, 'radius': 0.003})   # Small cyst very deep
        return cysts

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

    def update_phantom_(self, points_list=[]):
        # the points list is a list of PointItem Class (look model.point_item file)
        # add logic here
        # to show draw the output image call the next line
        # self.main_window.phantom_image_viewer.setset_image(image_matrix)
        pass

    def update_phantom(self, points_list):
        """
        Combines background speckle with cysts and user-added points (targets).
        """
        # Parse User Points from the GUI List
        user_x = []
        user_z = []
        user_amp = []

        for point in points_list:
            # Assume inputs are in mm, so we convert to meters
            z_m = point.get_depth() / 1000.0
            x_m = point.get_lateral() / 1000.0

            user_z.append(z_m)
            user_x.append(x_m)
            user_amp.append(2.0)

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


        # Combine Speckle + User Targets
        if user_x:
            total_x = np.concatenate([speckles_x, np.array(user_x)])
            total_z = np.concatenate([speckles_z, np.array(user_z)])
            total_amp = np.concatenate([speckles_amp, np.array(user_amp)])
        else:
            total_x = speckles_x
            total_z = speckles_z
            total_amp = speckles_amp

        #  Calculate True Time of Flight
        self.current_times = (2 * total_z) / self.true_speed
        self.current_amps = total_amp
        self.current_x = total_x

        #  Generate "Ground Truth" Image
        # We visualize using the TRUE positions (total_x, total_z)
        image_matrix = self.points_to_image(total_x, total_z, total_amp, cysts=None)

        #  Send to Viewer
        self.main_window.phantom_image_viewer.set_image(image_matrix)

        # Trigger Reconstruction to update immediately
        # self.main_window.reconstruction_controller.apply_reconstruction()

    def points_to_image(self, x, z, amp, img_w=512, img_h=512, cysts=None):
        """
        Scan Conversion: Converts scatter points (x, z) into a 2D image grid.
        Cysts are rendered as anechoic (dark) regions with visible acoustic shadows.
        """
        # Create empty grid
        image = np.zeros((img_w, img_h))

        # Map real coordinates to grid indices
        # X: -0.02 to 0.02 -> 0 to img_w
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

        # # Render cysts as anechoic (dark) regions on the image
        # if cysts:
        #     for cyst in cysts:
        #         # Convert cyst center to pixel coordinates
        #         cx_px = int(((cyst['x'] + (self.true_width / 2)) / self.true_width) * img_w)
        #         cz_px = int((cyst['z'] / self.max_depth) * img_h)
        #         radius_px = int((cyst['radius'] / self.true_width) * img_w)

        #         # Create anechoic region (set to near-zero)
        #         for dy in range(-radius_px, radius_px + 1):
        #             for dx in range(-radius_px, radius_px + 1):
        #                 py, px = cz_px + dy, cx_px + dx
        #                 if 0 <= py < img_h and 0 <= px < img_w:
        #                     dist = np.sqrt(dx**2 + dy**2)
        #                     if dist <= radius_px:
        #                         # Anechoic interior - very low amplitude
        #                         image[py, px] = 0.01

        # Apply Log Compression (Ultrasound images are always log-compressed)
        # Log(1 + pixel) to handle zeros safely
        image = np.log1p(image)

        image = np.rot90(image , k=1)
        return image
