import argparse
import json
import sys

import numpy as np
from generadores import *
from tqdm import *
import time

sys.path.append('../')

parser = argparse.ArgumentParser()

try:
    # Número de trabajos
    parser.add_argument('-J','--jobs', type=json.loads, default='[10]')
    # Número de Máquinas
    parser.add_argument('-M','--machines', type=json.loads, default='[4]')
    # Semilla
    parser.add_argument('-s','--seed', type= int, default=1)
    # Tipo de problema
    # 1 - JSP, 2 - FlowJSP, 3 - FlexibleJSP, 4 - OpenJSP
    # parser.add_argument('-T','--type', type=int, default=1)
    # Niveles de dificultad
    # Speed Scaling
    parser.add_argument('-S', '--speed-scaling', type=int, default=1)
    # Tiempo estandar de procesamiento de una máquina
    parser.add_argument('-mpt', '--machine-processing-time', dest='mpt', type=json.loads, default=[])
    # Energy 
    #parser.add_argument('-E', '--energy', type=int, default=0)
    # Release and Due date
    # 0 -> Tiempo infinito
    # 1 -> Tiempo por trabajo
    # 2 -> Tiempo por tarea de cada trabajo
    parser.add_argument('-RDDD', '--release-due', type=int, default=0)
    # Time
    # parser.add_argument('-Ti', '--time', type=int, default=0)
    # Path
    parser.add_argument('-P', '--path', type=str, default="./output")
    # Probability
    # parser.add_argument('-prb', '--prb', type=float, default=0.1)
    # Quantity
    parser.add_argument('-Q', '--quantity', type=int, default=1)
    # Distribution
    parser.add_argument('-D','--distribution', type=str, default="normal")

    args = parser.parse_args()
    np.random.seed(args.seed)

    start = time.time()
    for j in tqdm(args.jobs,desc='Jobs',leave=False):
        for m in tqdm(args.machines,desc='Machines',leave=False):
            for i in trange(args.quantity,desc='Quantity',leave=False):
                jm_path = str(j)+"_"+str(m)+"/"
                # if args.type  == 1:
                JSP(j, m, args.speed_scaling, args.release_due,args.mpt,args.distribution).saveToFile(f"{args.path}/JSP/"+jm_path+f"{j}x{m}_{i}.json")
                # elif args.type == 2:
                #     FlowJSP().saveToFile(f"{args.path}/FlowJSP/"+jm_path+f"{j}x{m}_{i}.json")
                # elif args.type == 3:
                #     FJSP(j, m, args.prb, args.speed_scaling, args.release_due).saveToFile(f"{args.path}/FJSP/"+jm_path+f"{j}x{m}_{i}.json")
                # else:
                #     OJSP().saveToFile(f"{args.path}/OJSP/"+jm_path+f"{j}x{m}_{i}.json")
                    
    
except Exception as e:
    raise