class PhantomController():
    def __init__(self, main_window):
        self.main_window = main_window
        self.main_window.sidebar.item_list.items_list_updated.connect(self.update_phantom)

    def update_phantom (self, points_list = []):
        # the points list is a list of PointItem Class (look model.point_item file)
        # add logic here 
        # to show draw the output image call the next line
        # self.main_window.phantom_image_viewer.setset_image(image_matrix)
        pass
