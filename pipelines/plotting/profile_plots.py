import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

def plot_profiles(num_epochs, profiles_imgs, profiles_data, norm):
    """
    Plot the profiles of the images and the data profiles in a single figure.
    
    Parameters
    ----------
    num_epochs : int
        The number of epochs to plot.
    profiles_imgs : list
        A list of the images to plot. Each image should be a 2D numpy array.
        It will be in the form of a list of lists.
        Example: [[epoch1_img_data], [epoch2_img_data], [epoch3_img_data]...]
    profiles_data : list
        A list of the data profiles to plot. Each data profile should be a 1D numpy array.
        It will be in the form of a list of lists.
        Example: [[epoch1_data_profile], [epoch2_data_profile], [epoch3_data_profile]...]
    norm : ImageNormalize
        The normalization object to use for the images.
    
    Returns
    -------
    fig : matplotlib.figure.Figure
        The figure object that was created.
    """

    # Create a figure with a specific size
    fig = plt.figure(dpi=150, figsize=(10, 5))
    gs =  gridspec.GridSpec(num_epochs + 1, 1, height_ratios=[0.2] * num_epochs + [1], hspace=0.05)

    for i in range(num_epochs):
        ax = fig.add_subplot(gs[i])

        ax.imshow(profiles_imgs[i], origin='lower', cmap='inferno', norm=norm)

        ax.set_xticklabels([])
        ax.set_yticklabels([])

        # remove the tick marks
        ax.tick_params(axis='both', which='both', bottom=False, top=False, left=False, right=False)
    
    ax = fig.add_subplot(gs[-1])

    for num, prof_data in enumerate(profiles_data):
        ax.plot(prof_data, label=f'epoch{num + 1}')


    # Center the zero in the middle of the x-axis
    if len(profiles_data[0]) % 2 == 0:
        x_ticks = np.linspace(0, len(profiles_data[0]), num=5)
    else:
        x_ticks = np.linspace(0, len(profiles_data[0]) - 1, num=5)
    
    x_labels = np.linspace(-len(profiles_data[0]) // 2, len(profiles_data[0]) // 2, num=5)

    ax.set_xticks(x_ticks)
    ax.set_xticklabels([int(x) for x in x_labels])

    # add vertical lines to show the center of the box
    ax.axvline(x=len(profiles_data[0]) // 2, color='gray', linestyle='--', alpha=0.5)

    ax.legend()

    ax.set_ylabel('AB Mag')
    ax.set_xlabel('Pixels')

    ax.set_xlim(-1, len(profiles_data[0]))
    ax.set_ylim(27, 31)

    # flip the ax axis for ab mag
    ax.invert_yaxis()

    fig.tight_layout()

    return fig

