import vertica_python
import numpy as np
from scipy.sparse import coo_matrix
from numpy.linalg import inv

# file login.ini contains host, username, password, and db name
with open('login.ini', 'r') as f:
        host = f.readline().strip()
        username = f.readline().strip()
        password = f.readline().strip()
        database = f.readline().strip()

conn_info = {'host': host,
                         'port': 5433,
                         'user': username,
                         'password': password,
                         'database': database,
                         'read_timeout': 600,
                         'connection_timeout': 5}

connection = vertica_python.connect(**conn_info)
cur = connection.cursor()

dataset = 'diabetes'
dim = 9
stm = 'SELECT DenseGamma(i, j, v USING PARAMETERS d=' + str(dim) + ') OVER (PARTITION BY MOD(i,1) ORDER BY i,j) FROM ' + dataset

cur.execute(stm)
rows = []
cols = []
data = []
for row in cur.iterate():
    rows.append(row[0] - 1)
    cols.append(row[1] - 1)
    data.append(row[2])

gamma = coo_matrix((np.asarray(data), (np.asarray(rows), np.asarray(cols))), shape=(dim+1, dim+1)).toarray()
Q =  gamma[0:9, 0:9]
XYt =  gamma[0:9, 9]

Q_inv = inv(Q)

beta = np.dot(Q_inv, XYt)
print beta