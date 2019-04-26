from bob.gradiant.core import AccessModifier, Access
import numpy as np


class DummyAccess(Access):

    def __init__(self, base_path,
                 name,
                 access_modifier=AccessModifier(),
                 annotation_base_path=None,
                 database_name=None):
        self.name = name
        super(DummyAccess, self).__init__(base_path,
                                          name,
                                          access_modifier,
                                          annotation_base_path=annotation_base_path,
                                          database_name=database_name)

    def load_annotations(self):
        pass

    def load(self):
        dict_images = {}
        for i in range(0,5000,33):
            if 'real' in self.name:
                dict_images[i] = np.ones((10,10,3))
            else:
                dict_images[i] = np.zeros((10, 10, 3))
        original_keys = dict_images.keys()
        dict_images = self.access_modifier.run(dict_images)
        if type(dict_images) is set:
            selected_keys = dict_images
        else:
            selected_keys = dict_images.keys()
        all_index = [int(val in selected_keys) for val in sorted(original_keys)]
        self.selected_index = [i for i, e in enumerate(all_index) if e != 0]
        return dict_images
