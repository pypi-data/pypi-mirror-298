import json
import os

import numpy as np
from tqdm import tqdm

path = './JSP-SpeedScaling-output/'


types = ['1','2','3']

for distribution in os.listdir(path):
    for t in types:
        for name in os.listdir(path+distribution+"/"+t+"/"):
            dir = path+distribution+"/"+t+"/"+name

            data = json.load(open(dir))

            SS = len(data["timeEnergy"][0]["operations"]["0"]["speed-scaling"])

            time = np.full((len(data["nbJobs"]),len(data["nbMchs"]),SS), -1)
            energy = np.full((len(data["nbJobs"]),len(data["nbMchs"]),SS), -1)
            precedence = np.full((len(data["nbJobs"]),len(data["nbMchs"])), 0)
            

            for te in data["timeEnergy"]:
                for i,(machineId,ss) in enumerate(te["operations"].items()):
                    precedence[te["jobId"]][int(machineId)] = i
                    for j,item in enumerate(ss["speed-scaling"]):
                        time[te["jobId"]][int(machineId)]       = ss["speed-scaling"][j]["procTime"]
                        energy[te["jobId"]][int(machineId)]     = ss["speed-scaling"][j]["energyCons"]

            replace_data = {
                    "speedscaling":SS,
                    "machines": len(data["nbMchs"]),
                    "jobs": len(data["nbJobs"]),
                    "tasks": len(data["nbMchs"]),
                    "time": list(time.flatten()),
                    "energy": list(energy.flatten()),
                    "precedence": list(precedence.flatten())
                    }
            
            with open(f"./types/SS/type0.dzn","r",encoding="utf-8") as file:
                filedata = file.read()
                for kk,v in replace_data.items():
                    filedata = filedata.replace("{"+kk+"}",str(v))

                os.makedirs(os.path.dirname("/".join(dir.split('/')[:-1]).replace("output","outputdzn")+"/"), exist_ok=True)
                
                with open(dir.replace("output","outputdzn").replace(".json",".dzn"), "w+",encoding="utf-8") as new:
                    new.write(filedata)