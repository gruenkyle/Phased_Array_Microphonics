import numpy as np
import database as db
import matplotlib.pyplot as mpl


codes = db.getCodes()

for code in codes:
    print(code)


