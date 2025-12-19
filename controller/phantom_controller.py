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

        # Reconstruction Parameters
        self.current_times = None
        self.current_amps = None
        self.current_x = None

        self.update_phantom([])

    def update_phantom_(self, points_list=[]):
        # the points list is a list of PointItem Class (look model.point_item file)
        # add logic here
        # to show draw the output image call the next line
        # self.main_window.phantom_image_viewer.setset_image(image_matrix)
        pass

    def update_phantom(self, points_list):
        """
        Combines background speckle with user-added points (targets).
        """
        # 1. Parse User Points from the GUI List
        user_x = []
        user_z = []
        user_amp = []

        for point in points_list:
            # Assume inputs are in mm, so we convert to meters
            z_m = point.get_depth() / 1000.0
            x_m = point.get_lateral() / 1000.0

            user_z.append(z_m)
            user_x.append(x_m)
            user_amp.append(10.0)

        # 2. Combine Speckle + User Targets
        if user_x:
            total_x = np.concatenate([self.speckles_x, np.array(user_x)])
            total_z = np.concatenate([self.speckles_z, np.array(user_z)])
            total_amp = np.concatenate([self.speckles_amplitude, np.array(user_amp)])
        else:
            total_x = self.speckles_x
            total_z = self.speckles_z
            total_amp = self.speckles_amplitude
        # 3. Calculate True Time of Flight
        self.current_times = (2 * total_z) / self.true_speed
        self.current_amps = total_amp
        self.current_x = total_x

        # 4. Generate "Ground Truth" Image
        # We visualize using the TRUE positions (total_x, total_z)
        image_matrix = self.points_to_image(total_x, total_z, total_amp)

        # 5. Send to Viewer
        self.main_window.phantom_image_viewer.set_image(image_matrix)

        # 6. Trigger Reconstruction to update immediately
        # self.main_window.reconstruction_controller.apply_reconstruction()

    def points_to_image(self, x, z, amp, img_w=512, img_h=512):
        """
        Scan Conversion: Converts scatter points (x, z) into a 2D image grid.
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

        # Apply Log Compression (Ultrasound images are always log-compressed)
        # Log(1 + pixel) to handle zeros safely
        image = np.log1p(image)

        return image
