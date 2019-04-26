import os
import h5py
from bokeh.plotting import figure, output_file, save
from bokeh.models import HoverTool
import numpy as np
from bob.gradiant.face.databases import RoseYoutuDatabase


def _get_ied_per_from_access(h5_access):

    file_root = h5py.File(h5_access, 'r')
    mtcnn_results = np.asarray(file_root['features'])
    keyframes = np.asarray(file_root['keyframe']).tolist()

    dict_keyframes_annotations = {}
    for i, tstamp in enumerate(keyframes):
        dict_keyframes_annotations[tstamp] = mtcnn_results[i, :]

    ied_per_access = []

    for keyframe in dict_keyframes_annotations:
        left_eye = (dict_keyframes_annotations[keyframe][4], dict_keyframes_annotations[keyframe][5])
        right_eye = (dict_keyframes_annotations[keyframe][6], dict_keyframes_annotations[keyframe][7])
        dy = right_eye[1] - left_eye[1]
        dx = right_eye[0] - left_eye[0]
        ied_per_access.append(int(np.sqrt((dx ** 2) + (dy ** 2))))

    return sum(ied_per_access)/len(ied_per_access)


def main():

    database = RoseYoutuDatabase('/media/data/databases/BBDD/AntiSpoofing/RoseYoutu2008')
    dict_all_accesses = database.get_all_accesses()

    ied_per_subset = {'Train': [],
                      'Dev': [],
                      'Test': []}

    for subset, accesses in dict_all_accesses.items():
        for access in accesses:
            ied = _get_ied_per_from_access(os.path.join(access.base_path, access.name + '.h5'))
            ied_per_subset[subset].append(ied)

    hover = HoverTool(tooltips=[
        ("index", "$index"),
        ("Count", "($y)"),
        ("IED (px)", "($x)"), ])

    fig_bokeh = figure(plot_width=900, plot_height=700, tools=[hover, 'pan', 'wheel_zoom', 'box_zoom',
                                                               'reset'], toolbar_location="above")
    fig_bokeh.title.text = " Histogram  | " + database.name() + " database  |"
    fig_bokeh.title.align = "left"
    fig_bokeh.title.text_color = "black"
    fig_bokeh.title.text_font_size = "13px"
    fig_bokeh.xaxis.axis_label = "IED (px)"
    fig_bokeh.yaxis.axis_label = "Count"

    hist_train, edges_train = np.histogram(ied_per_subset['Train'], bins='auto')
    hist_dev, edges_dev = np.histogram(ied_per_subset['Dev'], bins='auto')
    hist_test, edges_test = np.histogram(ied_per_subset['Test'], bins='auto')

    fig_bokeh.quad(top=hist_train, bottom=0, left=edges_train[:-1], right=edges_train[1:], fill_color="greenyellow",
                   line_color="darkgreen", fill_alpha=0.5, line_alpha=0.5, legend='Train')

    fig_bokeh.quad(top=hist_dev, bottom=0, left=edges_dev[:-1], right=edges_dev[1:], fill_color="firebrick",
                   line_color="darkred", fill_alpha=0.5, line_alpha=0.5, legend='Dev')

    fig_bokeh.quad(top=hist_test, bottom=0, left=edges_test[:-1], right=edges_test[1:], fill_color="navy",
                   line_color="darkblue", fill_alpha=0.5, line_alpha=0.5, legend='Test')

    fig_bokeh.legend.location = "top_right"
    fig_bokeh.legend.background_fill_color = "darkgrey"
    fig_bokeh.legend.click_policy = "hide"

    output_file('/home/mlorenzo/histogram.html')
    save(fig_bokeh)


if __name__ == '__script__':
    main()
