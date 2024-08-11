import numpy as np

with open('models/monu3.ply', 'r') as f:
    obj = f.readlines()[11:]
    obj = [i.split(" ")[:3] for i in obj]

    a = np.zeros((64, 64, 64), dtype=np.uint8)

    for i in range(64):
        for j in range(64):
            for k in range(64):
                if [str(i-32), str(k-32), str(j)] in obj:
                    a[i][j][k] = 1
    
    np.save('models/model2.npy', a)