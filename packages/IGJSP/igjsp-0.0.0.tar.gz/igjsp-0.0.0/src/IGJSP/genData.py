from generadores import JSP
import numpy as np
from tqdm import tqdm

Q = 10
dist_av = ['exp','norm','unif']
distribution = ['exponential','normal','uniform']
np.random.seed(0)

for job in tqdm([5,10,20,25,50,100]):
    for machine in [5,10,20,25,50,100]:
        for d in [0,1,2]:
            for speedScaling in [1,3,5]:
                for rd in [0,1,2]:
                    for q in range(Q):
                        JSP(job, machine, speedScaling, rd, [],distribution[d]).saveToFile(f"../INSTANCES/"+f"{job}_{machine}_{d}_{speedScaling}_{rd}_{q}.json")
                    