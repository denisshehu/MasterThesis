from utils.functions import *
from utils.variables import *

plt.rcParams.update({
    'font.family': 'serif',
    'text.usetex': True,
    'text.latex.preamble': r"""
        \usepackage{libertine}
        \usepackage{libertinust1math}
    """,
})
font_size = 11


def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:(i + 2)], 16) / 255.0 for i in (0, 2, 4))


blue = hex_to_rgb('#648FFF')
purple = hex_to_rgb('#785EF0')
red = hex_to_rgb('#DC267F')
orange = hex_to_rgb('#FE6100')
yellow = hex_to_rgb('#FFB000')
my_colormap = matplotlib.colors.LinearSegmentedColormap.from_list(
    'my_colormap', list(zip([0.0, 0.25, 0.5, 0.75, 1.0], [blue, purple, red, orange, yellow])))


def get_label(attribute):
    if attribute == 'topological_polysemy' or attribute == 'classification':
        return attribute.replace('_', ' ').capitalize()
    elif attribute == 'euclidicity':
        return 'Euclidicity score'
    elif attribute == 'intrinsic_dimension':
        return 'Estimated intrinsic dimension'
    elif attribute == 'original_neighborhood_thickness' or attribute == 'translated_neighborhood_thickness':
        return 'Neighborhood thickness'


def visualize_topological_polysemy(point_cloud, figure_name_prefix, colormap=my_colormap, color_bar_min=None,
                                   color_bar_max=None, elev=None, azim=None, roll=None, hide_x_tick_labels=True,
                                   hide_y_tick_labels=True, hide_z_tick_labels=True, hide_color_bar=False,
                                   hide_legend=True):
    figure_size1, pad1, point_size1, figure_size2, pad2, point_size2 = (4.9, 2.5), 0.4, 10, (4.9, 2.5), 0.6, 10

    attribute = 'topological_polysemy'
    _visualize_attribute(point_cloud, attribute, figure_name_prefix, colormap, color_bar_min, color_bar_max,
                         elev, azim, roll, hide_x_tick_labels, hide_y_tick_labels, hide_z_tick_labels, hide_color_bar,
                         hide_legend, figure_size1, pad1, point_size1, figure_size2, pad2, point_size2)


def visualize_classification(point_cloud, figure_name_prefix, colormap=my_colormap, color_bar_min=-0.2,
                             color_bar_max=2.2, elev=None, azim=None, roll=None, hide_x_tick_labels=True,
                             hide_y_tick_labels=True, hide_z_tick_labels=True, hide_color_bar=False, hide_legend=True):
    figure_size1, pad1, point_size1, figure_size2, pad2, point_size2 = (4.9, 2.5), 0.4, 10, (4.9, 2.5), 0.6, 10

    attribute = 'classification'
    _visualize_attribute(point_cloud, attribute, figure_name_prefix, colormap, color_bar_min, color_bar_max,
                         elev, azim, roll, hide_x_tick_labels, hide_y_tick_labels, hide_z_tick_labels, hide_color_bar,
                         hide_legend, figure_size1, pad1, point_size1, figure_size2, pad2, point_size2)


def visualize_euclidicity(point_cloud, figure_name_prefix, colormap=my_colormap, color_bar_min=None,
                          color_bar_max=None, elev=None, azim=None, roll=None, hide_x_tick_labels=True,
                          hide_y_tick_labels=True, hide_z_tick_labels=True, hide_color_bar=False, hide_legend=True):
    figure_size1, pad1, point_size1, figure_size2, pad2, point_size2 = (4.9, 2.5), 0.4, 10, (4.9, 2.5), 0.6, 10

    attribute = 'euclidicity'
    _visualize_attribute(point_cloud, attribute, figure_name_prefix, colormap, color_bar_min, color_bar_max,
                         elev, azim, roll, hide_x_tick_labels, hide_y_tick_labels, hide_z_tick_labels, hide_color_bar,
                         hide_legend, figure_size1, pad1, point_size1, figure_size2, pad2, point_size2)


def visualize_thickness(point_cloud, figure_name_prefix, colormap=my_colormap, color_bar_min=None,
                        color_bar_max=None, elev=None, azim=None, roll=None, hide_x_tick_labels=True,
                        hide_y_tick_labels=True, hide_z_tick_labels=True, hide_color_bar=False, hide_legend=True):
    figure_size1, pad1, point_size1, figure_size2, pad2, point_size2 = (4.9, 2.5), 0.4, 10, (4.9, 2.5), 0.6, 10

    attributes = ['original_neighborhood_thickness', 'translated_neighborhood_thickness']
    for attribute in attributes:
        _visualize_attribute(point_cloud, attribute, figure_name_prefix, colormap, color_bar_min, color_bar_max,
                             elev, azim, roll, hide_x_tick_labels, hide_y_tick_labels, hide_z_tick_labels,
                             hide_color_bar, hide_legend, figure_size1, pad1, point_size1, figure_size2, pad2,
                             point_size2)


def visualize_dimension(point_cloud, figure_name_prefix, include_individual_plots=True, known_dimension=None,
                        colormap=my_colormap, color_bar_min=None, color_bar_max=None, elev=None, azim=None, roll=None,
                        hide_x_tick_labels=True, hide_y_tick_labels=True, hide_z_tick_labels=True,
                        hide_color_bar=False, hide_legend=True, is_30_to_45=False):
    figure_size1, pad1, point_size1, figure_size2, pad2, point_size2 = (4.9, 2.5), 0.4, 10, (4.9, 2.5), 0.6, 10

    attribute = 'intrinsic_dimension'
    _visualize_attribute(point_cloud, attribute, figure_name_prefix, colormap, color_bar_min, color_bar_max,
                         elev, azim, roll, hide_x_tick_labels, hide_y_tick_labels, hide_z_tick_labels, hide_color_bar,
                         hide_legend, figure_size1, pad1, point_size1, figure_size2, pad2, point_size2)

    # Individual figures
    if include_individual_plots:
        for query in point_cloud.queries:
            min_x, max_x, min_y, max_y = None, None, None, None
            for estimates, estimates_type in [(query.initial_intrinsic_dimension_estimates, 'initial'),
                                              (query.filtered_intrinsic_dimension_estimates, 'filtered')]:

                x, y = list(estimates.keys()), list(estimates.values())
                if estimates_type == 'initial':
                    min_x, max_x, min_y, max_y = min(x), max(x), min(y), max(y)

                are_words_none = None in [query.word for query in point_cloud.queries]
                q = query.word if not are_words_none else query.identifier
                x_label = 'Neighborhood cardinality'
                y_label = get_label(attribute)
                figure_name = f'{figure_name_prefix}_{q}_{estimates_type}_{attribute}'
                point_size = 3
                line_width = 1
                save_space = False
                x_ticks = [30, 35, 40, 45] if is_30_to_45 else None

                plot_line_plot(x, y, x_label=x_label, y_label=y_label, min_x=min_x, max_x=max_x, min_y=min_y,
                               max_y=max_y, a=known_dimension, figure_name=figure_name, figure_size=(4.9, 3),
                               pad=2.1, point_size=point_size, line_width=line_width, save_space=save_space,
                               x_ticks=x_ticks)


def _visualize_attribute(point_cloud, attribute, figure_name_prefix, colormap, color_bar_min, color_bar_max,
                         elev, azim, roll, hide_x_tick_labels, hide_y_tick_labels, hide_z_tick_labels, hide_color_bar,
                         hide_legend, figure_size1, pad1, point_size1, figure_size2, pad2, point_size2):
    points = point_cloud.get_query_points()
    attribute_values = np.array([getattr(query, attribute) for query in point_cloud.queries])
    label = get_label(attribute)

    # 3D plot
    color_bar_label = label
    figure_name = f'{figure_name_prefix}_3d_plot_{attribute}'

    plot_3d_scatterplot(points, attribute_values, colormap, color_bar_label, color_bar_min, color_bar_max,
                        elev, azim, roll, hide_x_tick_labels, hide_y_tick_labels, hide_z_tick_labels, hide_color_bar,
                        hide_legend, figure_name, figure_size1, pad1, point_size1)

    # Summary plot
    are_words_none = None in [query.word for query in point_cloud.queries]
    y = np.array(
        [query.word_type.replace(' ', '\n') for query in point_cloud.queries]) if not are_words_none else np.ones(
        attribute_values.shape)
    x_label = label
    figure_name = f'{figure_name_prefix}_plot_summary_{attribute}'

    plot_scatterplot(attribute_values, y, x_label, min_x=color_bar_min, max_x=color_bar_max,
                     hide_y_tick_labels=are_words_none, figure_name=figure_name, figure_size=figure_size2, pad=pad2,
                     point_size=point_size2)


def visualize_variance(point_cloud, figure_name):
    y_monoseme = np.array([query.neighborhood_variance for query in point_cloud.queries
                           if query.word_type == 'Monoseme'])
    y_interclass = np.array([query.neighborhood_variance for query in point_cloud.queries
                             if query.word_type == 'Interclass polyseme'])
    y_intraclass = np.array([query.neighborhood_variance for query in point_cloud.queries
                             if query.word_type == 'Intraclass polyseme'])

    y1 = np.mean(y_monoseme, axis=0)
    y2 = np.mean(y_interclass, axis=0)
    y3 = np.mean(y_intraclass, axis=0)
    x = range(1, np.shape(y_monoseme)[1] + 1)
    y1_label = 'Monosemes'
    y2_label = 'Interclass polysemes'
    y3_label = 'Intraclass polysemes'
    x_label = 'Component'
    y_label = 'Variance'
    min_y = 0
    max_y = 0.12
    figure_size = (4.9, 2.5)
    pad = 0.8
    point_size = 3
    line_width = 1
    y_ticks = [0, 0.02, 0.04, 0.06, 0.08, 0.1, 0.12]

    plot_line_plot(x, y1, y2, y3, y1_label, y2_label, y3_label, x_label, y_label, min_y=min_y, max_y=max_y,
                   figure_name=figure_name, figure_size=figure_size, pad=pad, point_size=point_size,
                   line_width=line_width, y_ticks=y_ticks)


def plot_3d_scatterplot(points, values=None, colormap=my_colormap, color_bar_label=None,
                        color_bar_min=None, color_bar_max=None, elev=None, azim=None, roll=None,
                        hide_x_tick_labels=False, hide_y_tick_labels=False, hide_z_tick_labels=False,
                        hide_color_bar=False, hide_legend=True, figure_name=None, figure_size=None, pad=None,
                        point_size=None):
    dimension = points.shape[-1]

    if dimension < 4:
        points = add_extra_dimensions(points, 3)

        if dimension < 3:
            elev = -90 if elev is None else elev
            azim = 0 if azim is None else azim
            hide_z_tick_labels = True

        _plot_3d_scatterplot(points, values, colormap, color_bar_label, color_bar_min, color_bar_max, elev, azim, roll,
                             hide_x_tick_labels, hide_y_tick_labels, hide_z_tick_labels, hide_color_bar, hide_legend,
                             figure_name, figure_size, pad, point_size)


def _plot_3d_scatterplot(points, values, colormap, color_bar_label, color_bar_min, color_bar_max, elev, azim, roll,
                         hide_x_tick_labels, hide_y_tick_labels, hide_z_tick_labels, hide_color_bar, hide_legend,
                         figure_name, figure_size, pad, point_size):
    fig = plt.figure(figsize=figure_size)
    ax = fig.add_subplot(projection='3d')
    plt.tight_layout(pad=pad)

    if values is not None and type(values[0]) is np.str_:
        hide_color_bar = True

        colors = [blue, purple, red]
        positions = [0.0, 0.5, 1.0]
        colormap = matplotlib.colors.LinearSegmentedColormap.from_list('colormap', list(zip(positions, colors)))

        new_values = list()
        for value in values:
            if value == 'boundary':
                new_values.append(0)
            elif value == 'regular':
                new_values.append(1)
            else:
                new_values.append(2)
        values = new_values

        labels = ['boundary', 'regular', 'singular']
        dummy = [ax.scatter([], [], ls='-', c=c) for c in colors]
        if not hide_legend:
            ax.legend(dummy, labels, loc='upper right', fontsize=font_size, bbox_to_anchor=(1.45, 0.69))

    scatter = ax.scatter(points[:, 0], points[:, 1], points[:, 2], s=point_size, c=values, cmap=colormap)
    scatter.set_clim(vmin=color_bar_min, vmax=color_bar_max)
    ax.set_aspect('equal')
    ax.view_init(elev=elev, azim=azim, roll=roll)

    plt.tick_params(axis='both', which='major', labelsize=font_size)
    if hide_x_tick_labels:
        ax.set_xticklabels([])
    if hide_y_tick_labels:
        ax.set_yticklabels([])
    if hide_z_tick_labels:
        ax.set_zticklabels([])
    if not hide_color_bar:
        fig.colorbar(scatter, pad=0.1005).set_label(color_bar_label, fontsize=font_size)

    if figure_name is not None:
        figure_path = os.path.join(results_directory, f'{figure_name}.pdf')
        plt.savefig(figure_path)
        plt.close()
    else:
        plt.show()


def plot_scatterplot(x, y, x_label=None, y_label=None, min_x=None, max_x=None, min_y=None, max_y=None,
                     hide_y_tick_labels=False, figure_name=None, figure_size=None, pad=None, point_size=None):
    fig, ax = plt.subplots(figsize=figure_size)

    ax.scatter(x, y, s=point_size, c='k')

    ax.set_xlabel(x_label, fontsize=font_size)
    ax.set_ylabel(y_label, fontsize=font_size)
    ax.set_xlim(min_x, max_x)
    ax.set_ylim(min_y, max_y)

    plt.tick_params(axis='both', which='major', labelsize=font_size)
    if hide_y_tick_labels:
        ax.set_yticklabels([])

    if figure_name is not None:
        figure_path = os.path.join(results_directory, f'{figure_name}.pdf')
        plt.tight_layout(pad=pad)
        plt.savefig(figure_path)
        plt.close()
    else:
        plt.show()


def plot_line_plot(x, y1, y2=None, y3=None, y1_label=None, y2_label=None, y3_label=None, x_label=None, y_label=None,
                   min_x=None, max_x=None, min_y=None, max_y=None, use_x_log_scale=False, use_y_log_scale=False,
                   plot_y_equals_x=False, y_equals_x_label=None, a=None, a_label=None,
                   figure_name=None, figure_size=None, pad=None, point_size=None, line_width=None, save_space=True,
                   x_ticks=None, y_ticks=None):
    fig, ax = plt.subplots(figsize=figure_size)
    if not save_space:
        plt.tight_layout(pad=pad)

    if use_x_log_scale:
        plt.xscale('log')
    if use_y_log_scale:
        plt.yscale('log')

    if plot_y_equals_x:
        color = red if y2 is None else 'black'
        ax.plot([min_x, max_x], [min_y, max_y], '-', linewidth=line_width, color=color, label=y_equals_x_label)

    if a is not None:
        color = red if y2 is None else 'black'
        ax.plot([min_x, max_x], [a, a], '-', linewidth=line_width, color=color, label=a_label)

    if y2 is None:
        ax.plot(x, y1, 'k:o', linewidth=line_width, markersize=point_size, label=y1_label)
    elif y3 is None:
        ax.plot(x, y1, ':o', color=purple, linewidth=line_width, markersize=point_size, label=y1_label)
        ax.plot(x, y2, ':o', color=red, linewidth=line_width, markersize=point_size, label=y2_label)
    else:
        ax.plot(x, y1, ':o', color=blue, linewidth=line_width, markersize=point_size, label=y1_label)
        ax.plot(x, y2, ':o', color=purple, linewidth=line_width, markersize=point_size, label=y2_label)
        ax.plot(x, y3, ':o', color=red, linewidth=line_width, markersize=point_size, label=y3_label)

    if ax.get_legend_handles_labels()[1]:
        ax.legend(fontsize=font_size)

    ax.set_xlabel(x_label, fontsize=font_size)
    ax.set_ylabel(y_label, fontsize=font_size)
    ax.set_xlim(min_x, max_x)
    ax.set_ylim(min_y, max_y)

    if x_ticks is not None:
        plt.xticks(x_ticks)
    if y_ticks is not None:
        plt.yticks(y_ticks)
    plt.tick_params(axis='both', which='major', labelsize=font_size)

    if figure_name is not None:
        figure_path = os.path.join(results_directory, f'{figure_name}.pdf')
        if save_space:
            plt.tight_layout(pad=pad)
        plt.savefig(figure_path)
        plt.close()
    else:
        plt.show()
