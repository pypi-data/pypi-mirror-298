""" Mask classification functions. """
import numpy as np


def classify_manual(masks, template):
    """"
    Opens a GUI for manually classifying masks against a template image.

    Parameters
    ----------
    masks : np.array
        3D array of masks with dimensions (num_masks, image_height, image_width).
    template : np.array
        2D array used as a background image to assist in mask classification.

    Returns
    -------
    list of str
        List of classifications for each mask, as specified by user input.

    Notes
    -----
    User interaction is required to classify each mask. Press specific keys to classify
    each mask as 'soma', 'axon', 'dendrite', 'neuropil', 'artifact', or 'unknown'.

    Examples
    --------
    >>> masks = np.random.randint(0, 2, (5, 100, 100))
    >>> template = np.random.rand(100, 100)
    >>> types = classify_manual(masks, template)
    """
    import matplotlib.pyplot as plt
    import seaborn as sns

    mask_types = []
    plt.ioff()
    for mask in masks:
        ir = mask.sum(axis=1) > 0
        ic = mask.sum(axis=0) > 0

        il, jl = [max(np.min(np.where(i)[0]) - 10, 0) for i in [ir, ic]]
        ih, jh = [min(np.max(np.where(i)[0]) + 10, len(i)) for i in [ir, ic]]
        tmp_mask = np.array(mask[il:ih, jl:jh])

        with sns.axes_style("white"):
            fig, ax = plt.subplots(1, 3, sharex=True, sharey=True, figsize=(10, 3))

        ax[0].imshow(template[il:ih, jl:jh], cmap=plt.cm.get_cmap("gray"))
        ax[1].imshow(template[il:ih, jl:jh], cmap=plt.cm.get_cmap("gray"))
        tmp_mask[tmp_mask == 0] = np.NaN
        ax[1].matshow(tmp_mask, cmap=plt.cm.get_cmap("viridis"), alpha=0.5, zorder=10)
        ax[2].matshow(tmp_mask, cmap=plt.cm.get_cmap("viridis"))
        for a in ax:
            a.set_aspect(1)
            a.axis("off")
        fig.tight_layout()
        fig.canvas.manager.window.wm_geometry("+250+250")
        fig.suptitle("S(o)ma, A(x)on, (D)endrite, (N)europil, (A)rtifact or (U)nknown?")

        def on_button(event):
            if event.key == "o":
                mask_types.append("soma")
                plt.close(fig)
            elif event.key == "x":
                mask_types.append("axon")
                plt.close(fig)
            elif event.key == "d":
                mask_types.append("dendrite")
                plt.close(fig)
            elif event.key == "n":
                mask_types.append("neuropil")
                plt.close(fig)
            elif event.key == "a":
                mask_types.append("artifact")
                plt.close(fig)
            elif event.key == "u":
                mask_types.append("unknown")
                plt.close(fig)

        fig.canvas.mpl_connect("key_press_event", on_button)

        plt.show()
    sns.reset_orig()

    return mask_types


def classify_manual_extended(
    masks,
    template1,
    template2,
    template3,
    template4,
    template5,
    traces1,
    traces2,
    movie,
    threshold=80,
    window=3,
):
    """
    Opens a GUI for manually classifying masks against multiple templates and additional
    trace and movie data to assist classification.

    Parameters
    ----------
    masks : np.array
        3D array of masks (num_masks, image_height, image_width).
    template1, template2, template3, template4 : np.array
        2D arrays used as background images to assist with mask classification.
    template5 : list of np.array
        Series of 2D images used as background for classification.
    traces1, traces2 : np.array
        2D arrays (num_masks, num_frames) representing activity traces of masks.
    movie : np.array
        3D array of motion-corrected imaging frames (image_height, image_width, num_frames).
    threshold : float, optional
        Percentile used to enhance mask visibility against templates, default is 80.
    window : int, optional
        Width of window used in median filter for detecting high activity frames in traces1, default is 3.

    Returns
    -------
    list of str
        List of classifications for each mask, specified by user input during GUI interaction.

    Notes
    -----
    The function integrates complex visualization from multiple sources (templates, traces, and movie)
    to facilitate informed manual classification of neuronal structures. Press specific keys to classify
    each mask ('soma', 'axon', 'dendrite', 'neuropil', 'artifact', 'unknown') during the GUI session.

    Examples
    --------
    >>> masks = np.random.randint(0, 2, (5, 100, 100))
    >>> template1 = np.random.rand(100, 100)
    >>> template2 = np.random.rand(100, 100)
    >>> template3 = np.random.rand(100, 100)
    >>> template4 = np.random.rand(100, 100)
    >>> template5 = [np.random.rand(100, 100) for _ in range(7)]
    >>> traces1 = np.random.rand(5, 300)
    >>> traces2 = np.random.rand(5, 300)
    >>> movie = np.random.rand(100, 100, 300)
    >>> types = classify_manual_extended(masks, template1, template2, template3, template4, template5, traces1, traces2, movie)
    """

    import matplotlib.pyplot as plt
    import matplotlib.cm as cm
    import seaborn as sns
    from scipy import signal

    mask_types = []
    plt.ioff()

    for mask, trace1, trace2 in zip(masks, traces1, traces2):
        with sns.axes_style("white"):
            fig, axes = plt.subplots(4, 7, figsize=(30, 20))

        ir = mask.sum(axis=1) > 0
        ic = mask.sum(axis=1) > 0

        il, jl = [max(np.min(np.where(i)[0]) - 10, 0) for i in [ir, ic]]
        ih, jh = [min(np.max(np.where(i)[0]) + 10, len(i)) for i in [ir, ic]]
        plot_mask = np.array(mask[il:ih, jl:jh])

        for ax, template in zip(
            axes[0][:6],
            [
                plot_mask,
                template1,
                template2 - template1,
                template1,
                template4,
                template3,
                template3 * template1,
            ],
        ):
            ax.matshow(template[il:ih, jl:jh], cmap=cm.get_cmap("gray"))
            ax.contour(
                plot_mask,
                np.percentile(mask[mask > 0], threshold),
                linewidths=0.8,
                colors="w",
            )
            ax.contour(plot_mask, [0.01], linewidths=0.8, colors="w")
            ax.set_aspect(1)
            ax.axis("off")

        for ax, template in zip(axes[1], template5):
            ax.matshow(template[il:ih, jl:jh], cmap=cm.get_cmap("gray"))
            ax.contour(
                plot_mask,
                np.percentile(mask[mask > 0], threshold),
                linewidths=0.8,
                colors="w",
            )
            ax.contour(plot_mask, [0.01], linewidths=0.8, colors="w")
            ax.set_aspect(1)
            ax.axis("off")

        filt_trace = signal.medfilt(trace1, window)
        idx = detect_peaks(filt_trace, mpd=len(trace1) / window)
        centers = np.flip(
            sorted(np.stack([idx, filt_trace[idx]]).T, key=lambda x: x[1])
        )[:7]
        for ax, center in zip(axes[3], sorted(centers, key=lambda x: x[0])[:][0]):
            frame = np.max(
                movie[0][
                    :, :, int(center - window / 2) : int(center + window / 2 + 0.5)
                ]
            )
            ax.matshow(frame[il:ih, jl:jh], cmap=cm.get_cmap("gray"))
            ax.contour(
                plot_mask,
                np.percentile(mask[mask > 0], threshold),
                linewidths=0.8,
                colors="w",
            )
            ax.contour(plot_mask, [0.01], linewidths=0.8, colors="w")
            ax.set_aspect(1)
            ax.axis("off")

        trace1_ax = plt.subplot(8, 1, 5)
        trace1_ax.plot(trace1)
        trace1_ax.plot(centers, trace1[[int(center) for center in centers]], "or")

        trace2_ax = plt.subplot(8, 1, 6)
        trace2_ax.plot(trace2)

        fig.tight_layout()
        fig.canvas.manager.window.wm_geometry("+250+250")
        fig.suptitle("S(o)ma, A(x)on, (D)endrite, (N)europil, (A)rtifact or (U)nknown?")

        def on_button(event):
            if event.key == "o":
                mask_types.append("soma")
                plt.close(fig)
            elif event.key == "x":
                mask_types.append("axon")
                plt.close(fig)
            elif event.key == "d":
                mask_types.append("dendrite")
                plt.close(fig)
            elif event.key == "n":
                mask_types.append("neuropil")
                plt.close(fig)
            elif event.key == "a":
                mask_types.append("artifact")
                plt.close(fig)
            elif event.key == "u":
                mask_types.append("unknown")
                plt.close(fig)

        fig.canvas.mpl_connect("key_press_event", on_button)

        plt.show()

    sns.reset_orig()

    return mask_types


def _plot(x, mph, mpd, threshold, edge, valley, ax, ind, title):
    """Plot results of the detect_peaks function."""
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib is not available.")
    else:
        if ax is None:
            _, ax = plt.subplots(1, 1, figsize=(8, 4))
            no_ax = True
        else:
            no_ax = False

        ax.plot(x, "b", lw=1)
        if ind.size:
            label = "valley" if valley else "peak"
            label = label + "s" if ind.size > 1 else label
            ax.plot(
                ind,
                x[ind],
                "+",
                mfc=None,
                mec="r",
                mew=2,
                ms=8,
                label="%d %s" % (ind.size, label),
            )
            ax.legend(loc="best", framealpha=0.5, numpoints=1)
        ax.set_xlim(-0.02 * x.size, x.size * 1.02 - 1)
        ymin, ymax = x[np.isfinite(x)].min(), x[np.isfinite(x)].max()
        yrange = ymax - ymin if ymax > ymin else 1
        ax.set_ylim(ymin - 0.1 * yrange, ymax + 0.1 * yrange)
        ax.set_xlabel("Data #", fontsize=14)
        ax.set_ylabel("Amplitude", fontsize=14)
        if title:
            if not isinstance(title, str):
                mode = "Valley detection" if valley else "Peak detection"
                title = "%s (mph=%s, mpd=%d, threshold=%s, edge='%s')" % (
                    mode,
                    str(mph),
                    mpd,
                    str(threshold),
                    edge,
                )
            ax.set_title(title)
        # plt.grid()
        if no_ax:
            plt.show()


def detect_peaks(
    x,
    mph=None,
    mpd=1,
    threshold=0,
    edge="rising",
    kpsh=False,
    valley=False,
    show=False,
    ax=None,
):
    """
    Detect peaks in data based on their amplitude and other features.

    Parameters
    ----------
    x : 1D array_like
        data.
    mph : {None, number}, optional (default = None)
        detect peaks that are greater than minimum peak height.
    mpd : positive integer, optional (default = 1)
        detect peaks that are at least separated by minimum peak distance (in
        number of data).
    threshold : positive number, optional (default = 0)
        detect peaks (valleys) that are greater (smaller) than `threshold`
        in relation to their immediate neighbors.
    edge : {None, 'rising', 'falling', 'both'}, optional (default = 'rising')
        for a flat peak, keep only the rising edge ('rising'), only the
        falling edge ('falling'), both edges ('both'), or don't detect a
        flat peak (None).
    kpsh : bool, optional (default = False)
        keep peaks with same height even if they are closer than `mpd`.
    valley : bool, optional (default = False)
        if True (1), detect valleys (local minima) instead of peaks.
    show : bool, optional (default = False)
        if True (1), plot data in matplotlib figure.
    ax : a matplotlib.axes.Axes instance, optional (default = None).

    Returns
    -------
    ind : 1D array_like
        indeces of the peaks in `x`.

    Notes
    -----
    The detection of valleys instead of peaks is performed internally by simply
    negating the data: `ind_valleys = detect_peaks(-x)`

    The function can handle NaN's

    See this IPython Notebook [1]_.

    References
    ----------
    .. [1] http://nbviewer.ipython.org/github/demotu/BMC/blob/master/notebooks/DetectPeaks.ipynb

    __author__ = "Marcos Duarte, https://github.com/demotu/BMC"
    __version__ = "1.0.4"
    __license__ = "MIT"
    """

    x = np.atleast_1d(x).astype("float64")
    if x.size < 3:
        return np.array([], dtype=int)
    if valley:
        x = -x
    # find indices of all peaks
    dx = x[1:] - x[:-1]
    # handle NaN's
    indnan = np.where(np.isnan(x))[0]
    if indnan.size:
        x[indnan] = np.inf
        dx[np.where(np.isnan(dx))[0]] = np.inf
    ine, ire, ife = np.array([[], [], []], dtype=int)
    if not edge:
        ine = np.where((np.hstack((dx, 0)) < 0) & (np.hstack((0, dx)) > 0))[0]
    else:
        if edge.lower() in ["rising", "both"]:
            ire = np.where((np.hstack((dx, 0)) <= 0) & (np.hstack((0, dx)) > 0))[0]
        if edge.lower() in ["falling", "both"]:
            ife = np.where((np.hstack((dx, 0)) < 0) & (np.hstack((0, dx)) >= 0))[0]
    ind = np.unique(np.hstack((ine, ire, ife)))
    # handle NaN's
    if ind.size and indnan.size:
        # NaN's and values close to NaN's cannot be peaks
        ind = ind[
            np.in1d(
                ind, np.unique(np.hstack((indnan, indnan - 1, indnan + 1))), invert=True
            )
        ]
    # first and last values of x cannot be peaks
    if ind.size and ind[0] == 0:
        ind = ind[1:]
    if ind.size and ind[-1] == x.size - 1:
        ind = ind[:-1]
    # remove peaks < minimum peak height
    if ind.size and mph is not None:
        ind = ind[x[ind] >= mph]
    # remove peaks - neighbors < threshold
    if ind.size and threshold > 0:
        dx = np.min(np.vstack([x[ind] - x[ind - 1], x[ind] - x[ind + 1]]), axis=0)
        ind = np.delete(ind, np.where(dx < threshold)[0])
    # detect small peaks closer than minimum peak distance
    if ind.size and mpd > 1:
        ind = ind[np.argsort(x[ind])][::-1]  # sort ind by peak height
        idel = np.zeros(ind.size, dtype=bool)
        for i in range(ind.size):
            if not idel[i]:
                # keep peaks with the same height if kpsh is True
                idel = idel | (ind >= ind[i] - mpd) & (ind <= ind[i] + mpd) & (
                    x[ind[i]] > x[ind] if kpsh else True
                )
                idel[i] = 0  # Keep current peak
        # remove the small peaks and sort back the indices by their occurrence
        ind = np.sort(ind[~idel])

    if show:
        if indnan.size:
            x[indnan] = np.nan
        if valley:
            x = -x
        _plot(x, mph, mpd, threshold, edge, valley, ax, ind)

    return ind
