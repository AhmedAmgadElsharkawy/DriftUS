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
        self.main_window.m3.label.setText("Distance Error:")
        self.main_window.m4.label.setText("Area Error:")

    def update_metrics(self, _=None):
        """
        Calculate and update the 4 core geometric distortion metrics.
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
            'mean_depth_shift_mm': self._calc_mean_depth_shift(cysts, axial_magnification),
            'distance_error_pct': self._calc_distance_error(cysts, axial_magnification),
            'area_error_pct': self._calc_area_error(axial_magnification)
        }
        
        # Update UI
        self._update_displays(metrics, len(cysts))

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
            z_true = cyst.get_depth()  # in meters
            z_reconstructed = z_true * magnification
            
            # Absolute shift in millimeters
            shift_mm = abs(z_reconstructed - z_true) * 1000
            depth_shifts.append(shift_mm)
        
        return np.mean(depth_shifts)

    def _calc_distance_error(self, cysts, magnification):
        """
        Metric 3: Inter-target Axial Distance Error (%)
        
        Formula: For each pair of cysts, calculate:
                 (d_reconstructed - d_true) / d_true × 100%
                 where d = |z_a - z_b| (vertical separation only)
        
        Physical meaning: "Vertical spacing between targets is off by X%"
        
        Clinical relevance:
        - Affects multi-focal lesion assessment
        - Important for measuring disease spread
        - Critical for planning multi-target procedures
        
        Returns None if fewer than 2 cysts (distance undefined)
        """
        if len(cysts) < 2:
            return None
        
        distance_errors = []
        
        # Calculate all pairwise vertical separations
        for i in range(len(cysts)):
            for j in range(i + 1, len(cysts)):
                z_a_true = cysts[i].get_depth()
                z_b_true = cysts[j].get_depth()
                
                # True vertical separation
                d_true = abs(z_a_true - z_b_true)
                
                # Reconstructed vertical separation
                # Both depths scale by magnification, so separation also scales
                d_reconstructed = d_true * magnification
                
                # Percentage error
                error_pct = (d_reconstructed - d_true) / d_true * 100
                distance_errors.append(error_pct)
        
        return np.mean(distance_errors)

    def _calc_area_error(self, magnification):
        """
        Metric 4: Cyst Area Error (%)
        
        Formula: (magnification - 1) × 100%
        
        Physical meaning:
        - True cyst: Circle with area = π r²
        - Reconstructed: Ellipse with area = π r × (r × magnification) = π r² × magnification
        - Error: (Area_reconstructed - Area_true) / Area_true × 100%
        
        Clinical relevance:
        - Affects tumor volume calculations
        - Important for monitoring lesion size changes
        - Critical for surgical resection planning
        
        Note: This assumes isotropic cysts (circular in cross-section)
        """
        area_error_pct = (magnification - 1.0) * 100
        return area_error_pct

    def _update_displays(self, metrics, num_cysts):
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
        
        # Metric 3: Distance Error (%)
        if metrics['distance_error_pct'] is not None:
            dist_err = metrics['distance_error_pct']
            self.main_window.m3.set_value(f"{dist_err:+.2f}%")
        else:
            self.main_window.m3.set_value("Need 2+ cysts")
        
        # Metric 4: Area Error (%)
        area_err = metrics['area_error_pct']
        self.main_window.m4.set_value(f"{area_err:+.2f}%")

    def _reset_metrics(self):
        """
        Reset all metrics when no cysts are present.
        """
        self.main_window.m1.set_value("N/A")
        self.main_window.m2.set_value("N/A")
        self.main_window.m3.set_value("N/A")
        self.main_window.m4.set_value("N/A")