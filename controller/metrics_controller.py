import numpy as np

class MetricsController:
    def __init__(self, main_window):
        self.main_window = main_window
        
        # Connect to events that should trigger metric updates
        self.main_window.sidebar.item_list.items_list_updated.connect(self.update_metrics)
        self.main_window.sidebar.speed_changed.connect(self.update_metrics)
        
        # Set clear, unambiguous metric names
        self.main_window.m1.label.setText("Axial Magnification:")
        self.main_window.m2.label.setText("Mean Depth Shift:")

    def update_metrics(self, _=None):
        """
        Calculate and update the 2 core geometric distortion metrics.
        All metrics directly quantify clinically relevant distortions.
        """
        cysts = self.main_window.sidebar.item_list.get_items()
        
        if len(cysts) == 0:
            self._reset_metrics()
            return
        
        assumed_speed = self.main_window.sidebar.speed_spin_box.value()
        true_speed = self.main_window.phantom_controller.true_speed
        
        # Calculate the fundamental distortion parameter
        axial_magnification = assumed_speed / true_speed
        
        # Calculate all metrics
        metrics = {
            'axial_magnification': axial_magnification,
            'mean_depth_shift_mm': self._calc_mean_depth_shift(cysts, axial_magnification)
        }
        
        # Update UI
        self._update_displays(metrics)

    def _calc_mean_depth_shift(self, cysts, magnification):
        """
        Metric 2: Mean Absolute Axial Position Error (mm)
        
        Formula: Average of |z_reconstructed - z_true| across all cysts
        
        Physical meaning: "On average, targets appear X mm deeper/shallower than reality"
        
        Clinical relevance:
        - Affects biopsy needle placement
        - Impacts surgical planning
        - Critical for depth-dependent procedures
        """
        depth_shifts = []
        
        for cyst in cysts:
            z_true = cyst.get_depth()  # in m
            z_reconstructed = z_true * magnification  # in m
            
            # Absolute shift in millimeters
            shift_mm = abs(z_reconstructed - z_true) * 1000 # convert to mm
            depth_shifts.append(shift_mm)
        
        return np.mean(depth_shifts)

    def _update_displays(self, metrics):
        """
        Update the metric widget displays with calculated values.
        """
        # Metric 1: Axial Magnification Factor
        mag = metrics['axial_magnification']
        if mag > 1.0:
            direction = "stretch"
        elif mag < 1.0:
            direction = "compress"
        else:
            direction = "perfect"
        self.main_window.m1.set_value(f"{mag:.4f} ({direction})")
        
        # Metric 2: Mean Depth Shift (mm)
        shift = metrics['mean_depth_shift_mm']
        self.main_window.m2.set_value(f"{shift:.3f} mm")

    def _reset_metrics(self):
        """
        Reset all metrics when no cysts are present.
        """
        self.main_window.m1.set_value("N/A")
        self.main_window.m2.set_value("N/A")