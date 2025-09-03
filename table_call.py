import pandas as pd
import numpy as np
import sys

np.set_printoptions(threshold=sys.maxsize)
np.set_printoptions(linewidth=np.inf)

location= r'C:\Users\hanye\Desktop\compiler'
file = 'SLR_Table.xlsx'

data_pd = pd.read_excel('{}/{}'.format(location, file),
                        header = None, index_col = None, names = None, engine='openpyxl')

data_np = pd.DataFrame.to_numpy(data_pd)

Row = 86
Column = 40

data_pd = data_pd.fillna(-1)
data_pd = data_pd.astype('int', errors='ignore')



arr = data_pd.to_numpy()

output = np.array2string(arr, separator=',', formatter={'int': lambda x: str(x)})
print(output)


