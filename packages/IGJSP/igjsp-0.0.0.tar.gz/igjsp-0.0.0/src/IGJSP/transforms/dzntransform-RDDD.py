import json
import os

import numpy as np
from tqdm import tqdm

path = './JSPoutput/'


types = ['0','1','2']

for distribution in os.listdir(path):
    for t in types:
        for name in os.listdir(path+distribution+"/"+t+"/"):
            dir = path+distribution+"/"+t+"/"+name

            data = json.load(open(dir))

            time = np.full((len(data["nbJobs"]),len(data["nbMchs"])), -1)
            energy = np.full((len(data["nbJobs"]),len(data["nbMchs"])), -1)
            precedence = np.full((len(data["nbJobs"]),len(data["nbMchs"])), 0)

            if t == '1':
                release_date = np.full(len(data["nbJobs"]),0)
                due_date = np.full(len(data["nbJobs"]),0)
            elif t == '2':
                release_date = np.full((len(data["nbJobs"]), len(data["nbMchs"])),0)
                due_date = np.full((len(data["nbJobs"]), len(data["nbMchs"])),0)


            for te in data["timeEnergy"]:
                for i,(machineId,ss) in enumerate(te["operations"].items()):
                    time[te["jobId"]][int(machineId)]       = ss["speed-scaling"][0]["procTime"]
                    energy[te["jobId"]][int(machineId)]     = ss["speed-scaling"][0]["energyCons"]
                    precedence[te["jobId"]][int(machineId)] = i
                    if t == '2':
                        release_date[te["jobId"], int(machineId)] = ss["release-date"]
                        due_date[te["jobId"], int(machineId)] = ss["due-date"]
                if t == '1':
                    release_date[te["jobId"]] = te["release-date"]
                    due_date[te["jobId"]] = te["due-date"]


            replace_data = {
                    "machines": len(data["nbMchs"]),
                    "jobs": len(data["nbJobs"]),
                    "tasks": len(data["nbMchs"]),
                    "time": list(time.flatten()),
                    "energy": list(energy.flatten()),
                    "precedence": list(precedence.flatten())
                    }
            if t == "1":
                replace_data["releaseDate"] = list(release_date)
                replace_data["dueDate"] = list(due_date)
            elif t == "2":
                replace_data["releaseDate"] = list(release_date.flatten())
                replace_data["dueDate"] = list(due_date.flatten())

            with open(f"./types/type{t}.dzn","r",encoding="utf-8") as file:
                filedata = file.read()
                for kk,v in replace_data.items():
                    filedata = filedata.replace("{"+kk+"}",str(v))

                os.makedirs(os.path.dirname("/".join(dir.split('/')[:-1]).replace("output","outputdzn")+"/"), exist_ok=True)
                
                with open(dir.replace("output","outputdzn").replace(".json",".dzn"), "w+",encoding="utf-8") as new:
                    new.write(filedata)