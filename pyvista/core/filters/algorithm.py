"""Methods for handling vtkAlgorithm."""

import pyvista
from pyvista.utilities import (wrap, ProgressMonitor)


def _update_alg(alg, progress_bar=False, message=''):
    """Update an algorithm with or without a progress bar."""
    if progress_bar:
        with ProgressMonitor(alg, message=message):
            alg.Update()
    else:
        alg.Update()


def _get_output(algorithm, iport=0, iconnection=0, oport=0, active_scalars=None,
                active_scalars_field='point'):
    """Get the algorithm's output and copy input's pyvista meta info."""
    ido = algorithm.GetInputDataObject(iport, iconnection)
    data = wrap(algorithm.GetOutputDataObject(oport))
    if not isinstance(data, pyvista.MultiBlock):
        data.copy_meta_from(ido)
        if not data.field_arrays and ido.field_arrays:
            data.field_arrays.update(ido.field_arrays)
        if active_scalars is not None:
            data.set_active_scalars(active_scalars, preference=active_scalars_field)
    return data
