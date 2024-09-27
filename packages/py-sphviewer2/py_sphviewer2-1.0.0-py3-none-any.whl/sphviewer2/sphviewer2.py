###############################################################################
#                     Py-SPHViewer2 - Rendering Library Wrapper               #
#                                                                             #
# This Python module provides an interface for rendering images based on      #
# Smoothed Particle Hydrodynamics (SPH) data using the private `smeshl`       #
# library. The shared library is proprietary and was developed by Alejandro   #
# Benitez-Llambay. It is not publicly available and must be obtained          #
# from the link provided                                                      #
#                                                                             #
# Author: Alejandro Benitez-Llambay                                           #
# Email: alejandro.benitezllambay@unimib.it                                   #
# License: Private                                                            #
#                                                                             #
# This wrapper provides a Python interface to the `smeshl` library, which     #
# must be compiled for your operating system (macOS/Linux). Ensure that the   #
# appropriate shared library (.dylib/.so) is present in your system path.     #
#                                                                             #
# DISCLAIMER:                                                                 #
# This software is provided "as is", without any warranty of any kind, either #
# expressed or implied, including but not limited to the warranties of        #
# merchantability, fitness for a particular purpose, and non-infringement.    #
# In no event shall the author be liable for any claim, damages, or other     #
# liability, whether in an action of contract, tort, or otherwise, arising    #
# from, out of, or in connection with the software or the use or other        #
# dealings in the software.                                                   #
#                                                                             #
# Users should NOT distribute this software, in whole or in part,             #
# without prior written permission from the author.                           #
###############################################################################

import ctypes as _ctypes
import numpy as _np
import platform as _platform

class sphviewer2:
    """
    A Python wrapper for rendering images using smeshl shared library.
    """

    def __init__(self):
        """
        Initializes the sphviewer2 instance and loads the shared C library.
        Determines the platform-specific shared library extension and loads the corresponding shared library.

        Raises:
            OSError: If the operating system is unsupported or the shared library cannot be loaded.
        """
        library_name = "libsmeshl"
        file_extension = self._get_shared_library_extension()

        # Construct the library file path
        library_file = f"{library_name}{file_extension}"

        # Load the shared library
        try:
            self.lib = _ctypes.CDLL(library_file)
        except OSError as e:
            raise OSError(f"Failed to load the library: {library_file}") from e

        # Define argument types and return type for the C function 'render'
        self.lib.render.argtypes = [
            _ctypes.POINTER(_ctypes.c_float), _ctypes.POINTER(_ctypes.c_float),
            _ctypes.POINTER(_ctypes.c_float), _ctypes.POINTER(_ctypes.c_float),
            _ctypes.c_int, _ctypes.c_float, _ctypes.c_float,
            _ctypes.c_float, _ctypes.c_int, _ctypes.c_int,
            _ctypes.POINTER(_ctypes.c_float)
        ]
        self.lib.render.restype = _ctypes.c_int

    def render(self, x, y, m, h, xmin, ymin, Lbox, LevelMin, LevelMax, k=None):
        """
        Renders an image based on the SPH data passed as arguments.

        Args:
            x (np.ndarray or float): Array or scalar representing the x-coordinates of particles.
            y (np.ndarray or float): Array or scalar representing the y-coordinates of particles.
            m (np.ndarray or float): Array or scalar representing the mass of particles.
            h (np.ndarray or float): Array or scalar representing the smoothing lengths of particles.
            xmin (float): The minimum x-coordinate of the bounding box.
            ymin (float): The minimum y-coordinate of the bounding box.
            Lbox (float): The size of the bounding box.
            LevelMin (int): The minimum refinement level.
            LevelMax (int): The maximum refinement level (determines the image size as 2^LevelMax).
            k (np.ndarray, optional): Indices to subset the particles. Defaults to None.

        Returns:
            np.ndarray: A 2D array representing the rendered image.

        Raises:
            RuntimeError: If the C function returns a non-zero error code.
            ValueError: If any of the input parameters are invalid.
        """
        # Validate inputs
        if not isinstance(LevelMax, int) or LevelMax < 1:
            raise ValueError("LevelMax should be a positive integer.")
        if not isinstance(xmin, (int, float)) or not isinstance(ymin, (int, float)):
            raise ValueError("xmin and ymin must be numeric values.")

        # Determine output image size based on LevelMax
        size = 1 << LevelMax  # size = 2^LevelMax
        output_image = _np.zeros((size, size), dtype=_np.float32)

        # Ensure x, y, m, h are arrays or convert scalars to arrays
        x = self._ensure_array(x)
        y = self._ensure_array(y)
        m = self._ensure_array(m)
        h = self._ensure_array(h)

        # If k is provided, use it to subset the arrays
        if k is not None:
            x = x[k]
            y = y[k]
            m = m[k]
            h = h[k]

        Npart = len(x)

        # Convert numpy arrays to ctypes pointers
        x_ptr = x.ctypes.data_as(_ctypes.POINTER(_ctypes.c_float))
        y_ptr = y.ctypes.data_as(_ctypes.POINTER(_ctypes.c_float))
        m_ptr = m.ctypes.data_as(_ctypes.POINTER(_ctypes.c_float))
        h_ptr = h.ctypes.data_as(_ctypes.POINTER(_ctypes.c_float))
        output_ptr = output_image.ctypes.data_as(_ctypes.POINTER(_ctypes.c_float))

        # Call the C function for rendering
        result = self.lib.render(
            x_ptr, y_ptr, m_ptr, h_ptr,
            Npart, xmin, ymin,
            Lbox, LevelMin, LevelMax,
            output_ptr
        )

        # Check the result and raise an error if rendering failed
        if result != 0:
            raise RuntimeError(f"C function returned an error code: {result}")

        return output_image

    def _ensure_array(self, data):
        """
        Ensures that the input is an array. If the input is a scalar, it converts it into a 1-element numpy array.

        Args:
            data (float or np.ndarray): The input data to ensure as an array.

        Returns:
            np.ndarray: The input data as a numpy array.
        """
        if isinstance(data, _np.ndarray):
            return data.astype(_np.float32)
        else:
            return _np.array([data], dtype=_np.float32)

    def _get_shared_library_extension(self):
        """
        Returns the platform-specific extension for shared libraries.

        Returns:
            str: The file extension for the shared library (e.g., '.dylib' for macOS, '.so' for Linux).

        Raises:
            OSError: If the operating system is unsupported.
        """
        current_os = _platform.system()
        
        if current_os == 'Darwin':  # macOS
            return '.dylib'
        elif current_os == 'Linux':
            return '.so'
        else:
            raise OSError(f"Unsupported operating system: {current_os}")