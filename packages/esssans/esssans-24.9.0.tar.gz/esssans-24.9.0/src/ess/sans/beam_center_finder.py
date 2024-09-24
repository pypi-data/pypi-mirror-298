# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2023 Scipp contributors (https://github.com/scipp)

import uuid

import numpy as np
import sciline
import scipp as sc
from scipp.core import concepts

from ess.reduce.uncertainty import UncertaintyBroadcastMode

from .conversions import ElasticCoordTransformGraph
from .logging import get_logger
from .types import (
    BeamCenter,
    DetectorBankSizes,
    DimsToKeep,
    IofQ,
    MaskedData,
    NeXusDetector,
    NormWavelengthTerm,
    QBins,
    ReturnEvents,
    SampleRun,
    WavelengthBands,
    WavelengthMask,
)


def _xy_extrema(pos: sc.Variable) -> sc.Variable:
    x_min = pos.fields.x.min()
    x_max = pos.fields.x.max()
    y_min = pos.fields.y.min()
    y_max = pos.fields.y.max()
    return sc.concat([x_min, x_max, y_min, y_max], dim='extremes')


def beam_center_from_center_of_mass(workflow: sciline.Pipeline) -> BeamCenter:
    """
    Estimate the beam center via the center-of-mass of the data counts.

    The center-of-mass is simply the weighted mean of the positions.
    Areas with low counts are excluded from the center of mass calculation, as they
    typically fall into asymmetric regions of the detector panel and would thus lead
    to a biased result. The beam is assumed to be roughly aligned with the Z axis.
    The returned beam center is the component normal to the beam direction, projected
    onto the X-Y plane.

    Parameters
    ----------
    workflow:
        The reduction workflow to compute MaskedData[SampleRun].

    Returns
    -------
    :
        The beam center position as a vector.
    """
    try:
        beam_center = workflow.compute(BeamCenter)
    except sciline.UnsatisfiedRequirement:
        beam_center = sc.vector([0.0, 0.0, 0.0], unit='m')
        workflow = workflow.copy()
        workflow[BeamCenter] = beam_center
    data = workflow.compute(MaskedData[SampleRun])
    graph = workflow.compute(ElasticCoordTransformGraph)

    dims_to_sum = set(data.dims) - set(data.coords['position'].dims)
    if dims_to_sum:
        summed = data.sum(dims_to_sum)
    else:
        summed = data.bins.sum()
    if summed.ndim > 1:
        summed = summed.flatten(to=uuid.uuid4().hex)

    pos = summed.coords['position']
    v = sc.values(summed)
    mask = concepts.irreducible_mask(summed, dim=None)
    if mask is None:
        mask = sc.zeros(sizes=pos.sizes, dtype='bool')
    extrema = _xy_extrema(pos[~mask])
    # Mean including existing masks
    cutoff = 0.1 * v.mean().data
    low_counts = v.data < cutoff
    # Increase cutoff until we no longer include pixels at the X/Y min/max.
    # This would be simpler if the logical panel shape was reflected in the
    # dims of the input data, instead of having a flat list of pixels.
    while sc.any(_xy_extrema(pos[~(mask | low_counts)]) == extrema):
        cutoff *= 2.0
        low_counts = v.data < cutoff
    # See scipp/scipp#3271, the following lines are a workaround
    select = ~(low_counts | mask)
    v = v.data[select]
    pos = pos[select]
    com = sc.sum(pos * v) / v.sum()

    # We compute the shift between the incident beam direction and the center-of-mass
    incident_beam = summed.transform_coords('incident_beam', graph=graph).coords[
        'incident_beam'
    ]
    n_beam = incident_beam / sc.norm(incident_beam)
    com_shift = com - sc.dot(com, n_beam) * n_beam
    xy = [com_shift.fields.x.value, com_shift.fields.y.value]
    return beam_center + _offsets_to_vector(data=summed, xy=xy, graph=graph)


def _offsets_to_vector(data: sc.DataArray, xy: list[float], graph: dict) -> sc.Variable:
    """
    Convert x,y offsets inside the plane normal to the beam to a vector in absolute
    coordinates.
    """
    u = data.coords['position'].unit
    # Get two vectors that define the plane normal to the beam
    coords = data.transform_coords(
        ['cyl_x_unit_vector', 'cyl_y_unit_vector'], graph=graph
    ).coords
    center = xy[0] * coords['cyl_x_unit_vector'] + xy[1] * coords['cyl_y_unit_vector']
    center.unit = u
    return center


def _iofq_in_quadrants(
    xy: list[float],
    workflow: sciline.Pipeline,
    detector: sc.DataArray,
    norm: sc.DataArray,
) -> dict[str, sc.DataArray]:
    """
    Compute the intensity as a function of Q inside 4 quadrants in Phi.

    Parameters
    ----------
    xy:
        The x,y offsets in the plane normal to the beam.
    detector:
        The raw detector.
    norm:
        The denominator data for normalization.

    Returns
    -------
    :
        A dictionary containing the intensity as a function of Q in each quadrant.
        The quadrants are named 'south-west', 'south-east', 'north-east', and
        'north-west'.
    """
    pi = sc.constants.pi.value
    phi_bins = sc.linspace('phi', -pi, pi, 5, unit='rad')
    quadrants = ['south-west', 'south-east', 'north-east', 'north-west']

    graph = workflow.compute(ElasticCoordTransformGraph)
    workflow = workflow.copy()
    workflow[BeamCenter] = _offsets_to_vector(data=detector, xy=xy, graph=graph)
    calibrated = workflow.compute(MaskedData[SampleRun])
    with_phi = calibrated.transform_coords(
        'phi', graph=graph, keep_intermediate=False, keep_inputs=False
    )
    # If gravity-correction is enabled, phi depends on wavelength (and event).
    # We cannot handle this below, so we approximate phi by the mean value.
    if ('phi' not in with_phi.coords) and ('phi' in with_phi.bins.coords):
        # This is the case where we have a phi event coord but no coord at the top level
        phi = with_phi.bins.coords['phi'].bins.mean()
    else:
        phi = with_phi.coords['phi']
        if phi.bins is not None or 'wavelength' in phi.dims:
            phi = phi.mean('wavelength')

    out = {}
    for i, quad in enumerate(quadrants):
        # Select pixels based on phi
        sel = (phi >= phi_bins[i]) & (phi < phi_bins[i + 1])
        # The beam center is applied when computing CalibratedDetector, set quadrant
        # *before* that step.
        workflow[NeXusDetector[SampleRun]] = sc.DataGroup(data=detector[sel])
        # MaskedData would be computed automatically, but we did it above already
        workflow[MaskedData[SampleRun]] = calibrated[sel]
        workflow[NormWavelengthTerm[SampleRun]] = (
            norm if norm.dims == ('wavelength',) else norm[sel]
        )
        out[quad] = workflow.compute(IofQ[SampleRun])
    return out


def _cost(xy: list[float], *args) -> float:
    """
    Cost function for determining how close the :math:`I(Q)` curves are in all four
    quadrants. The cost is defined as

    .. math::

       \\text{cost} = \\frac{\\sum_{Q}\\sum_{i=1}^{i=4} \\overline{I}(Q)\\left(I(Q)_{i} - \\overline{I}(Q)\\right)^2}{\\sum_{Q}\\overline{I}(Q)} ~,

    where :math:`i` represents the 4 quadrants and :math:`\\overline{I}(Q)` is the mean
    intensity of the 4 quadrants as a function of :math:`Q`. This is basically a
    weighted mean of the square of the differences between the :math:`I(Q)` curves in
    the 4 quadrants with respect to the mean, and where the weights are
    :math:`\\overline{I}(Q)`.
    We use a weighted mean, as opposed to relative (percentage) differences to give
    less importance to regions with low statistics which are potentially noisy and
    would contribute significantly to the computed cost.

    Parameters
    ----------
    xy:
        The x,y offsets in the plane normal to the beam.
    *args:
        Arguments passed to :func:`iofq_in_quadrants`.

    Returns
    -------
    :
        The sum of the residuals for :math:`I(Q)` in the 4 quadrants, with respect to
        the mean :math:`I(Q)` in all quadrants.

    Notes
    -----
    Mantid uses a different cost function. They compute the horizontal (Left - Right)
    and the vertical (Top - Bottom) costs, and require both to be below the tolerance.
    The costs are defined as

    .. math::

       \\text{cost} = \\sum_{Q} \\left(I(Q)_{\\text{L,T}} - I(Q)_{\\text{R,B}}\\right)^2 ~.

    Using absolute differences instead of a weighted mean is similar to our cost
    function in the way that it would give a lot of weight to even a small difference
    in a high-intensity region. However, it also means that an absolute difference of
    e.g. 2 in a high-intensity region would be weighted the same as a difference of 2
    in a low-intensity region.
    It is also not documented why two separate costs are computed, instead of a single
    one. The Mantid implementation is available
    `here <https://github.com/mantidproject/mantid/blob/main/Framework/PythonInterface/plugins/algorithms/WorkflowAlgorithms/SANS/SANSBeamCentreFinder.py`_.
    """  # noqa: E501
    iofq = _iofq_in_quadrants(xy, *args)
    all_q = sc.concat([sc.values(da) for da in iofq.values()], dim='quadrant')
    ref = all_q.mean('quadrant')
    c = (all_q - ref) ** 2
    out = (sc.sum(ref * c) / sc.sum(ref)).value
    logger = get_logger('sans')
    if not np.isfinite(out):
        out = np.inf
        logger.info(
            'Non-finite value computed in cost. This is likely due to a division by '
            'zero. If the final results for the beam center are not satisfactory, '
            'try restricting your Q range, or increasing the size of your Q bins to '
            'improve statistics in the denominator.'
        )
    logger.info('Beam center finder: x=%s, y=%s, cost=%s', xy[0], xy[1], out)
    return out


def beam_center_from_iofq(
    *,
    workflow: sciline.Pipeline,
    q_bins: int | sc.Variable,
    minimizer: str | None = None,
    tolerance: float | None = None,
) -> BeamCenter:
    """
    Find the beam center of a SANS scattering pattern using an I(Q) calculation.

    Description of the procedure:

    #. obtain an initial guess by computing the center-of-mass of the pixels,
       weighted by the counts on each pixel
    #. from that initial guess, divide the panel into 4 quadrants
    #. compute :math:`I(Q)` inside each quadrant and compute the residual difference
       between all 4 quadrants
    #. iteratively move the centre position and repeat 2. and 3. until all 4
       :math:`I(Q)` curves lie on top of each other

    Parameters
    ----------
    workflow:
        The reduction workflow to compute I(Q).
    q_bins:
        The binning in the Q dimension to be used.
    minimizer:
        The Scipy minimizer method to use (see the
        `Scipy docs <https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.minimize.html>`_
        for details).
    tolerance:
        Tolerance for termination (see the
        `Scipy docs <https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.minimize.html>`_
        for details).

    Returns
    -------
    :
        The beam center position as a vector.

    Notes
    -----
    We record here the thought process we went through during the writing of this
    algorithm. This information is important for understanding why the beam center
    finding is implemented the way it is, and should be considered carefully before
    making changes to the logic of the algorithm.

    **Use a + cut, not an X cut**

    The first idea for implementing the beam center finder was to cut the detector
    panel into 4 wedges using a cross (X) shape. This is what Mantid does, and seemed
    natural, because the offsets when searching for the beam center would be applied
    along the horizontal and vertical directions.
    This worked well on square detector panels (like the SANS2D detector), but on
    rectangular detectors, the north and south wedges ended up holding many less pixels
    than the east and west panels.
    More pixels means more contributions to a particular :math:`Q` bin, and comparing
    the :math:`I(Q)` curves in the 4 wedges was thus not possible.
    We therefore divided the detector panel into 4 quadrants using a ``+`` cut instead.
    Note that since we are looking at an isotropic scattering pattern, the shape of the
    cut (and the number of quadrants) should not matter for the resulting shapes of the
    :math:`I(Q)` curves.

    **Normalization inside the 4 quadrants**

    The first attempt at implementing the beam center finder was to only compute the
    raw counts as a function of $Q$ for the sample run, and not compute any
    normalization term.
    The idea was that even though this would change the shape of the :math:`I(Q)` curve,
    because we were looking at isotropic scattering, it would change the shape of the
    curve isotropically, thus still allowing us to find the center when the curves in
    all 4 quadrants overlap.
    The motivation for this was to save computational cost.

    After discovering the issue that using a ``X`` shaped cut for dividing the detector
    panel would yield different contributions to :math:`I(Q)` in the different wedges,
    we concluded that some normalization was necessary.
    The first version was to simply sum the counts in each quadrant and use this to
    normalize the counts for each intensity curve.

    This was, however, not sufficient in cases where masks are applied to the detector
    pixels. It is indeed very common to mask broken pixels, as well as the region of
    the detector where the sample holder is casting a shadow.
    Such a sample holder will not appear in all 4 quadrants, and because it spans a
    range of scattering (:math:`2{\\theta}`) angles, it spans a range of :math:`Q` bins.

    All this means that we in fact need to perform a reduction as close as possible to
    the full :math:`I(Q)` reduction in each of the 4 quadrants to achieve a reliable
    result.
    We write 'as close as possible' because In the full :math:`I(Q)` reduction, there
    is a term :math:`D({\\lambda})` in the normalization called the 'direct beam' which
    gives the efficiency of the detectors as a function of wavelength.
    Because finding the beam center is required to compute the direct beam in the first
    place, we do not include this term in the computation of :math:`I(Q)` for finding
    the beam center. This changes the shape of the :math:`I(Q)` curve, but since it
    changes it in the same manner for all :math:`{\\phi}` angles, this does not affect
    the results for finding the beam center.

    This is what is now implemented in this version of the algorithm.
    """
    from scipy.optimize import minimize

    logger = get_logger('sans')

    logger.info('Requested minimizer: %s', minimizer)
    logger.info('Requested tolerance: %s', tolerance)
    minimizer = minimizer or 'Nelder-Mead'
    tolerance = tolerance or 0.1
    logger.info('Using minimizer: %s', minimizer)
    logger.info('Using tolerance: %s', tolerance)

    keys = (
        NeXusDetector[SampleRun],
        MaskedData[SampleRun],
        NormWavelengthTerm[SampleRun],
        ElasticCoordTransformGraph,
    )
    workflow = workflow.copy()
    # Avoid reshape of detector, which would break boolean-indexing by cost function
    workflow[DetectorBankSizes] = {}
    results = workflow.compute(keys)
    detector = results[NeXusDetector[SampleRun]]['data']
    data = results[MaskedData[SampleRun]]
    norm = results[NormWavelengthTerm[SampleRun]]
    graph = results[ElasticCoordTransformGraph]

    # Avoid reloading the detector
    workflow[NeXusDetector[SampleRun]] = sc.DataGroup(data=detector)
    workflow[UncertaintyBroadcastMode] = UncertaintyBroadcastMode.upper_bound
    workflow[ReturnEvents] = False
    workflow[DimsToKeep] = ()
    workflow[WavelengthMask] = None
    workflow[WavelengthBands] = None
    workflow[QBins] = q_bins

    # Use center of mass to get initial guess for beam center
    com_shift = beam_center_from_center_of_mass(workflow)
    logger.info('Initial guess for beam center: %s', com_shift)

    coords = data.transform_coords(
        ['cylindrical_x', 'cylindrical_y'], graph=graph
    ).coords
    bounds = [
        (coords['cylindrical_x'].min().value, coords['cylindrical_x'].max().value),
        (coords['cylindrical_y'].min().value, coords['cylindrical_y'].max().value),
    ]

    # Refine using Scipy optimize
    res = minimize(
        _cost,
        x0=[com_shift.fields.x.value, com_shift.fields.y.value],
        args=(workflow, detector, norm),
        bounds=bounds,
        method=minimizer,
        tol=tolerance,
    )

    center = _offsets_to_vector(data=data, xy=res.x, graph=graph)
    logger.info('Final beam center value: %s', center)
    logger.info('Beam center finder minimizer info: %s', res)
    return center
