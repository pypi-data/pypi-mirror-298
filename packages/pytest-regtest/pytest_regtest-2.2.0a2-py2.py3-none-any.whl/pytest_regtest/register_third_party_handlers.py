try:
    import numpy as np  # noqa: F401

    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

try:
    import pandas as pd  # noqa: F401

    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False


if HAS_PANDAS and HAS_NUMPY:

    def is_dataframe(obj):
        try:
            import pandas as pd

            return isinstance(obj, pd.DataFrame)
        except ImportError:
            return False

    from .pandas_handler import DataFrameHandler
    from .snapshot_handler import snapshot_handlers

    snapshot_handlers.append((is_dataframe, DataFrameHandler))

if HAS_NUMPY:

    def is_numpy(obj):
        try:
            import numpy as np

            return isinstance(obj, np.ndarray)
        except ImportError:
            return False

    from .numpy_handler import NumpyHandler
    from .snapshot_handler import snapshot_handlers

    snapshot_handlers.append((is_numpy, NumpyHandler))
