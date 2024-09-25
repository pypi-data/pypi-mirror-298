"""
Generates a visual representation of a Wardley Map using Matplotlib.

This function takes a Wardley Map object as input and utilises Matplotlib to generate
a visual representation of the map. It supports various styles for the map, such as 'wardley',
'handwritten', 'default', and 'plain', among others available in Matplotlib. The function
configures the plot's appearance, including font, title, axes, and grid lines. It then adds
the Wardley Map components like nodes, edges, annotations, and special features such as
evolve markers and pipeline representations to the plot. The output is a Matplotlib figure
object, which can be displayed in a Jupyter notebook or saved as an image file.

Parameters:
    map (WardleyMap): An instance of the WardleyMap class containing the elements and
    properties of the map to be visualised, including components, relationships, and annotations.

Returns:
    matplotlib.figure.Figure: A Matplotlib figure object representing the Wardley Map. This object
    can be used to display the map within a Jupyter notebook or saved to a file in formats supported
    by Matplotlib, such as PNG or SVG.

Raises:
    ValueError: If an unrecognised style is specified in the WardleyMap object.
    KeyError: If a node referenced in edges, bluelines, evolves, or pipelines is not defined in the map.

Notes:
    The function automatically adjusts the plot settings based on the specified style in the WardleyMap object.
    It supports advanced customisation through the WardleyMap object, allowing users to define specific aspects
        of the map, such as evolution stages, visibility levels, and custom annotations.
    Warnings are generated and appended to the WardleyMap object's warnings attribute for any inconsistencies or
        issues detected during the map generation process, such as missing components or unsupported styles.
"""

import matplotlib
from matplotlib import patches
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from .wardley_maps import WardleyMap


def initialize_plot(figsize=(15, 9)):
    """
    Initializes a Matplotlib figure and axes tailored for Wardley Map plotting.

    Sets up a figure with specified dimensions and configures the axes with predefined limits suitable for
    Wardley Maps, ensuring a consistent foundation for subsequent plotting. The function also resets Matplotlib's
    configuration to its default settings to avoid unintended styling side effects from previous plots, maintaining
    a clean visual slate for each Wardley Map visualisation.

    Parameters:
        figsize (tuple, optional): The dimensions of the figure in inches, given as a tuple (width, height).
            Defaults to (24, 15), providing ample space for detailed Wardley Maps.

    Returns:
        tuple: A tuple containing two elements:
            - fig (matplotlib.figure.Figure): The Matplotlib figure object for the plot, serving as the canvas for drawing.
            - ax (matplotlib.axes.Axes): The axes object for the plot, representing the area where the map elements are placed.

    Note:
        This function currently does not use the WardleyMap object directly but is designed to potentially
        accommodate future enhancements that might require specific map attributes for plot initialisation.
    """

    matplotlib.rcParams.update(matplotlib.rcParamsDefault)
    fig, ax = plt.subplots(figsize=figsize)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1.1)
    return fig, ax


def create_wardley_map_plot(wardley_map, figsize=(15, 9)):
    """
    Generates and visualizes a Wardley Map using Matplotlib, based on the provided WardleyMap object.

    This function interprets the structure and elements defined in a WardleyMap object to create a visual representation
    of the map using Matplotlib. It accommodates various visual styles by leveraging Matplotlib's styling capabilities
    and custom settings to represent nodes, edges, annotations, and other components of a Wardley Map. The function
    ensures the map's elements are accurately positioned and styled according to their respective attributes within
    the WardleyMap object, supporting a range of customization options for personalized map visualization.

    Parameters:
        wardley_map (WardleyMap): An instance of the WardleyMap class, encapsulating the structure, components,
            and configuration of the Wardley Map to be visualized.

    Returns:
        tuple: A tuple containing two elements:
            - wm (WardleyMap): The WardleyMap object, potentially augmented with warnings about any issues encountered during plotting.
            - fig (matplotlib.figure.Figure): The Matplotlib figure object representing the visualized Wardley Map.

    Raises:
        ValueError: If the style specified in the WardleyMap object is unrecognized or unsupported by the function.
        KeyError: If elements referenced in edges, pipelines, or annotations are undefined in the WardleyMap object.

    Notes:
        - The function dynamically adjusts plot settings based on the style attribute of the WardleyMap object,
          enabling a variety of visual themes for the map representation.
        - It is capable of handling advanced customization through the WardleyMap object, allowing for detailed
          specification of evolution stages, visibility levels, and custom annotations.
        - Potential inconsistencies or issues detected during the plotting process, such as missing components or
          unsupported styles, are recorded as warnings in the WardleyMap object for user review.
    """

    CIRCLESIZE = 5

    # Parse the OWM syntax:
    wm = WardleyMap(wardley_map)

    # Initialise the plot
    fig, ax = initialize_plot(figsize)

    if wm.style is None:
        wm.style = "wardley"

    if wm.style == "wardley":
        # Use a monospaced font:
        matplotlib.rcParams["font.family"] = "monospace"
        matplotlib.rcParams["font.size"] = 6

        # Add the gradient background
        norm = matplotlib.colors.Normalize(0, 1)
        colors = [[norm(0.0), "white"], [norm(0.5), "white"], [norm(1.0), "#f6f6f6"]]
        cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", colors)
        plt.xlim(0, 1)
        plt.ylim(0, 1.1)
        plotlim = plt.xlim() + plt.ylim()
        ax.imshow(
            [[1, 0, 1], [1, 0, 1]],
            cmap=cmap,
            interpolation="bicubic",
            extent=plotlim,
            aspect="auto",
        )
    elif wm.style in ["handwritten"]:
        matplotlib.rcParams["font.family"] = "Gloria Hallelujah"
        fig, ax = plt.subplots()
    elif wm.style in ["default", "plain"]:
        fig, ax = plt.subplots()
    elif wm.style in plt.style.available:
        with plt.style.context(wm.style):
            fig, ax = plt.subplots()
    elif wm.style is not None:
        wm.warnings.append(f"Map style '{wm.style}' not recognised or supported.")

    # Set up basic properties:
    if wm.title:
        plt.title(wm.title)
    plt.xlim(0, 1)
    plt.ylim(0, 1.1)

    # Plot the lines
    l = []
    for edge in wm.edges:
        if edge[0] in wm.nodes and edge[1] in wm.nodes:
            n_from = wm.nodes[edge[0]]
            n_to = wm.nodes[edge[1]]
            l.append([(n_from["mat"], n_from["vis"]), (n_to["mat"], n_to["vis"])])
        else:
            for n in edge:
                if n not in wm.nodes:
                    wm.warnings.append(f"Could not find component called {n}")
    if len(l) > 0:
        lc = LineCollection(l, color=matplotlib.rcParams["axes.edgecolor"], lw=0.5)
        ax.add_collection(lc)

    # Plot blue lines
    b = []
    for blueline in wm.bluelines:
        if blueline[0] in wm.nodes and blueline[1] in wm.nodes:
            n_from = wm.nodes[blueline[0]]
            n_to = wm.nodes[blueline[1]]
            b.append([(n_from["mat"], n_from["vis"]), (n_to["mat"], n_to["vis"])])
        else:
            for n in blueline:
                if n not in wm.nodes:
                    wm.warnings.append(f"Could not find blueline component called {n}")
    if len(b) > 0:
        lc = LineCollection(b, color="blue", lw=1)
        ax.add_collection(lc)

    # Plot Evolve
    e = []
    for evolve_title, evolve in wm.evolves.items():
        if evolve_title in wm.nodes:
            n_from = wm.nodes[evolve_title]
            e.append([(n_from["mat"], n_from["vis"]), (evolve["mat"], n_from["vis"])])
        else:
            wm.warnings.append(
                f"Could not find evolve component called {evolve_title}"
            )
    if len(e) > 0:
        lc = LineCollection(e, color="red", lw=0.5, linestyles="dotted")
        ax.add_collection(lc)

    # Add the nodes:
    for node_title, n in wm.nodes.items():
        if n["type"] == "component":
            plt.plot(
                n["mat"],
                n["vis"],
                marker="o",
                color=matplotlib.rcParams["axes.facecolor"],
                markeredgecolor=matplotlib.rcParams["axes.edgecolor"],
                markersize=CIRCLESIZE,
                lw=1,
            )
            if "label_x" in n and "label_y" in n:
                # If label offsets exist, use them
                ax.annotate(
                    node_title,
                    fontsize=matplotlib.rcParams["font.size"],
                    fontfamily=matplotlib.rcParams["font.family"],
                    xy=(n["mat"], n["vis"]),
                    xycoords="data",
                    xytext=(n["label_x"], n["label_y"]),
                    textcoords="offset pixels",
                    horizontalalignment="left",
                    verticalalignment="bottom",
                )
            else:
                # No label offsets; place the label at the node's position
                ax.annotate(
                    node_title,
                    fontsize=matplotlib.rcParams["font.size"],
                    fontfamily=matplotlib.rcParams["font.family"],
                    xy=(n["mat"], n["vis"]),
                    xycoords="data",
                    horizontalalignment="left",
                    verticalalignment="bottom",
                )

    # Add the anchors:
    for node_title, n in wm.nodes.items():
        if n["type"] == "anchor":
            plt.plot(
                n["mat"],
                n["vis"],
                marker="o",
                color=matplotlib.rcParams["axes.facecolor"],
                markeredgecolor="blue",
                markersize=CIRCLESIZE,
                lw=1,
            )
            if "label_x" in n and "label_y" in n:
                ax.annotate(
                    node_title,
                    fontsize=matplotlib.rcParams["font.size"],
                    fontfamily=matplotlib.rcParams["font.family"],
                    xy=(n["mat"], n["vis"]),
                    xycoords="data",
                    xytext=(n["label_x"], n["label_y"]),
                    textcoords="offset pixels",
                    horizontalalignment="left",
                    verticalalignment="bottom",
                )
            else:
                ax.annotate(
                    node_title,
                    fontsize=matplotlib.rcParams["font.size"],
                    fontfamily=matplotlib.rcParams["font.family"],
                    xy=(n["mat"], n["vis"]),
                    xycoords="data",
                    horizontalalignment="left",
                    verticalalignment="bottom",
                )

    # Add the evolve nodes:
    for evolve_title, evolve in wm.evolves.items():
        if evolve_title in wm.nodes:
            n = wm.nodes[evolve_title]
            plt.plot(
                evolve["mat"],
                n["vis"],
                marker="o",
                color=matplotlib.rcParams["axes.facecolor"],
                markeredgecolor="red",
                markersize=CIRCLESIZE,
                lw=1,
            )
            if "label_x" in n and "label_y" in n:
                ax.annotate(
                    evolve_title,
                    fontsize=matplotlib.rcParams["font.size"],
                    fontfamily=matplotlib.rcParams["font.family"],
                    xy=(evolve["mat"], n["vis"]),
                    xycoords="data",
                    xytext=(n["label_x"], n["label_y"]),
                    textcoords="offset pixels",
                    horizontalalignment="left",
                    verticalalignment="bottom",
                )
            else:
                ax.annotate(
                    evolve_title,
                    fontsize=matplotlib.rcParams["font.size"],
                    fontfamily=matplotlib.rcParams["font.family"],
                    xy=(evolve["mat"], n["vis"]),
                    xycoords="data",
                    horizontalalignment="left",
                    verticalalignment="bottom",
                )
        else:
            wm.warnings.append(f"Node '{evolve_title}' does not exist in the map.")

    # Add the pipeline nodes:
    for pipeline_title, _pipeline in wm.pipelines.items():
        if pipeline_title in wm.nodes:
            n = wm.nodes[pipeline_title]
            plt.plot(
                n["mat"],
                n["vis"],
                marker="s",
                color=matplotlib.rcParams["axes.facecolor"],
                markersize=CIRCLESIZE,
                lw=0.5,
            )
        else:
            wm.warnings.append(f"Node '{pipeline_title}' does not exist in the map.")

    # Plot Pipelines
    for pipeline_title, pipeline in wm.pipelines.items():
        if pipeline_title in wm.nodes:
            n_from = wm.nodes[pipeline_title]
            rectangle = patches.Rectangle(
                (pipeline["start_mat"], n_from["vis"] - 0.02),
                pipeline["end_mat"] - pipeline["start_mat"],
                0.02,
                fill=False,
                lw=0.5,
            )
            ax.add_patch(rectangle)
        else:
            wm.warnings.append(
                f"Could not find pipeline component called {pipeline_title}"
            )

    # Add the notes:
    for note in wm.notes:
        plt.text(
            note["mat"],
            note["vis"],
            note["text"],
            fontsize=matplotlib.rcParams["font.size"],
            fontfamily=matplotlib.rcParams["font.family"],
            fontweight='bold',
            fontname='monospace'
        )

    plt.yticks(
        [0.0, 0.925], ["Invisible", "Visible"], rotation=90, verticalalignment="bottom"
    )
    plt.ylabel("Visibility", fontweight="bold")
    plt.xticks(
        [0.0, 0.17, 0.4, 0.70],
        ["Genesis", "Custom-Built", "Product\n(+rental)", "Commodity\n(+utility)"],
        ha="left",
    )
    plt.xlabel("Evolution", fontweight="bold")

    plt.tick_params(axis="x", direction="in", top=True, bottom=True, grid_linewidth=1)
    plt.grid(visible=True, axis="x", linestyle="--")
    plt.tick_params(axis="y", length=0)

    wm.warnings = list(set(wm.warnings))

    return wm, fig
