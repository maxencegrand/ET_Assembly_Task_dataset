
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import os


import numpy as np

import numpy as np

# Suppose que vous avez un tableau NumPy appelé 'arr'
arr = np.array([[1, 2, 3],
                [4, 2, 6],
                [2, 8, 9]])

# Remplacer les 2 par 0
arr = np.where(arr == 2, 0, arr)

print(arr)