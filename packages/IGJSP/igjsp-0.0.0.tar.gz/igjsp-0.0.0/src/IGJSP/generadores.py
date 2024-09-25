import scipy
import numpy as np
import random
import itertools 
import json
from scipy.stats import norm, beta, uniform, expon
import os

class JSP:

    def __init__(self, jobs, machines, speed, rrdd, mpt= None, distribution=None) -> None:
        self.numJobs    = jobs
        self.numMchs    = machines
        self.speed      = speed
        self.times      = []
        self.rrdd       = rrdd
        self.distribution = distribution
        
        if self.speed > 1:
            l = 0
            delta = 0.1
            for n in range(self.speed):
                self.times.append(norm(l + delta,0.1))
                l += 1/self.speed
        else:
            if distribution == "uniform":
                self.times.append(uniform(0.1,100))
            elif distribution == "normal":
                self.times.append(norm(50,20))
            elif distribution == "exponential":
                self.times.append(expon(loc=50,scale=20))
        self.JSP = {
                "nbJobs":list(range(jobs)),
                "nbMchs": list(range(machines)),
                "timeEnergy":[],
                "drDate" : []
            }
        # Si no se proporciona consumo básico se genera un consumo básico por máquina
        if self.speed > 1 and not(mpt):
            self.mpt = uniform(10,100).rvs(machines)
            self.mpt = list(map(int, self.mpt))
        else:
            self.mpt = mpt
        self.jobsToMachine()
        
    def f(self, x):
        return int(np.exp(-int(x)/100)*100)
    
    def g(self, x):
        return 90*x + 10
    
    def t(self,c):
        return 4.0704 * np.log(2) / np.log(1 + (c * 2.5093)**3)

    # Método encargado de generar el tiempo que tarda en ser procesado un trabajo y su consumo, teniendo en cuenta las
    # distintas velocidades
    def genProcEnergy(self, machine):        
        ans = []  
        for dist in self.times:
            if self.speed == 1:
                time = int(max(1,dist.rvs(1)))
            else:
                # Para cada nivel se va a obtener cuanta energía se le debe proporcionar a la máquina para que consiga
                # realizar esa tarea en ese tiempo
                consumoEnergia = min(1,max(0.1,dist.rvs(1))) * 5

                time = max(1,int(self.t(consumoEnergia) * self.mpt[machine]))
            ans.append((time, self.f(time)))
        return ans
    


    def jobsToMachine(self):
        for job in range(self.numJobs):
            machines = np.random.choice(range(self.numMchs), self.numMchs, replace=False)
            new = {
                "jobId": int(job),
                "operations":{}
            }
            releaseDateTask = random.choice(range(0,101,10))
            initial = releaseDateTask
            for machine in machines:
                if machine not in new["operations"]:
                    new["operations"][int(machine)] = {}
                if "speed-scaling" not in new["operations"][int(machine)]:
                    new["operations"][int(machine)]["speed-scaling"] = []

                for proc,energy in self.genProcEnergy(machine):
                    if self.rrdd == 2:
                        aux = {
                                "procTime": proc,
                                "energyCons": energy
                            }
                        new["operations"][int(machine)]["speed-scaling"].append(aux)
                    else:
                        new["operations"][int(machine)]["speed-scaling"].append({
                            "procTime": proc,
                            "energyCons": energy
                        })
                        releaseDateTask += self.release_due(proc) + 1
                if self.rrdd == 2:
                    new["operations"][int(machine)]['release-date'] = releaseDateTask
                    releaseDateTask += int(self.release_due(proc)) + 1
                    new["operations"][int(machine)]['due-date'] = releaseDateTask - 1
            if self.rrdd == 1:
                new["release-date"]  = initial
                new["due-date"]     = int(releaseDateTask) - 1
            self.JSP["timeEnergy"].append(new)

    def release_due(self, duration):
        if self.distribution == "uniform":
            return uniform(duration,2*duration).rvs()
        elif self.distribution == "normal":
            return max(duration,norm(loc=2*duration, scale=duration/2).rvs())
        else:
            return expon(loc=duration,scale=duration/2).rvs()


    def saveToFile(self, filename):
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w') as f:
            json.dump(self.JSP, f,indent=4)


# Generador para Flow JSP 

class FlowJSP:
    pass

# Generador para JSP Flexibles
class FJSP:
    def __init__(self, jobs, machines, p, speeds) -> None:
        self.numJobs = jobs
        self.numMchs = machines
        self.p       = p
        self.speeds  = speeds
        self.FJSP = {
                "nbJobs":list(range(jobs)),
                "nbMchs": list(range(machines)),
                "timeEnergy":[],
                "drDate" : [],
                "predSucc": []
            }

        self.times = []
        if speeds > 1:
            l = -6
            for n in range(speeds):
                self.times.append(norm(l,1))
                l += 10/speeds
        else:
            self.times.append(uniform(0,1))
        # [beta(2,8), beta(5,5), beta(8,2)]

        # Estructura de datos auxiliar para almacenar los jobs que asignados a cada máquina
        self.machines = {}
        for m in self.FJSP['nbMchs']:
            self.machines[m] = []

        self.jobsToMachines()
        self.jobsReleaseDueDate()
        self.jobPredSucc()

    def addJobMachine(self, j, m):
        for proc, energy in self.genProcEnergy(m):
            self.FJSP['timeEnergy'].append({
                    "jobId": j,
                    "machId": m,
                    "procTime": proc,
                    "energyCons": energy
                })

    def jobsToMachines(self):
        permutation = np.random.choice(self.FJSP['nbJobs'], len(self.FJSP['nbMchs']), replace=False).astype('int')
        asignado = self.FJSP['nbJobs'][:]
        # Al menos un job por máquina
        for machine, job in enumerate(permutation):
            asignado.remove(job)
            self.addJobMachine(job, machine)
            self.machines[machine].append(job)
        # Al menos un machine por job que no tenga ya asignado una máquina
        permutation = np.random.choice(self.FJSP['nbMchs'], len(asignado)).astype('int')
        for job, machine  in zip(asignado,permutation):
            self.addJobMachine(job, machine)
            self.machines[machine].append(job)

        listaJobs = self.FJSP['nbJobs'][:]
        # Si existe probabilidad de que un trabajo se pueda realizar en una máquina
        while self.p > 0.001 and listaJobs:
            # Se genera un vector de 0s y 1s donde un 0 en la posición i indica que el trabajo i no se ejecuta en otra máquina
            # y un 1 indica que se realiza en más de dos máquinas
            permutation = list(scipy.stats.binom.rvs(n=1,p=self.p, size=len(listaJobs)).astype('int'))
            for job, cond in zip(listaJobs[:], permutation):
                if cond:
                    self.addJobMachine(int(job), np.random.choice(self.FJSP['nbMchs']).astype('int'))
                else:
                    listaJobs.remove(job)
            self.machines[machine].append(job)
            self.p = self.p / 2

    def jobsReleaseDueDate(self):
        for job in self.FJSP['nbJobs']:
            ddate = self.genDueDate()
            self.FJSP['drDate'].append({
                "jobId": job,
                "ddate": ddate,
                "weight": 0,
                "rdate": int(ddate + self.genReleaseDate(ddate))
            })

    def jobPredSucc(self):
        for machine, jobs in self.machines.items():
            jobs = set(jobs)
            for jp, js in itertools.permutations(jobs, 2):
                self.FJSP['predSucc'].append({
                    "machId": machine,
                    "jobPred": jp,
                    "jobSucc": js,
                    "setupTime": self.genSetupTime()
                })
    
    def saveToFile(self, filename):
        # Convertir los datos a tipos de datos que se pueden serializar 
        for item in self.FJSP['timeEnergy']:
            item['jobId'] = int(item['jobId'])
            item['machId'] = int(item['machId'])
            item['procTime'] = int(item['procTime'])
            item['energyCons'] = int(item['energyCons'])

        
        for item in self.FJSP['predSucc']:
            item['machId'] = int(item['machId'])
            item['jobPred'] = int(item['jobPred'])
            item['jobSucc'] = int(item['jobSucc'])
            item['setupTime'] = int(item['setupTime'])

        
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        # Guardar el problema en formato JSON
        with open(filename, 'w') as f:
            json.dump(self.FJSP, f,indent=4)

    # Método encargado de generar el tiempo que tarda en ser procesado un trabajo y su consumo, teniendo en cuenta tres velocidades
    def genProcEnergy(self, machine):        
        ans = []  
        for dist in self.times:
            if self.speeds == 1:
                time = max(0, dist.rvs())
            else:
                time = 100 * max(0.1,(min(max(-8,dist.rvs(1)),6) + 8) / 14)
            # time = 100 * max(0.1 , dist.rvs(1)[0])
            ans.append((time, np.exp(-time/100)*100))
        return ans

    # Método encargado de generar el tiempo de partida de un trabajo
    def genDueDate(self):
        return random.choice(range(0,101,10))
    
    # Método encargado de generar el tiempo de Vencimiento
    def genReleaseDate(self, Proc):
        return random.uniform(Proc,2*Proc)
    
    # Método encargado de generar el tiempo de setup entre dos jobs
    def genSetupTime(self):
        return random.uniform(10,100)
    
# Generador para Open JSP
class OJSP:
    pass