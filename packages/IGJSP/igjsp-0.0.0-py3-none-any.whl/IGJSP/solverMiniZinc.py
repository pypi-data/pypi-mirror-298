import json
import os
import sys
import time
from datetime import timedelta

from minizinc import *
from tqdm import tqdm
import itertools
from joblib import Parallel, delayed

sys.path.append('../')

from TelegramBot import TelegramBot

tl = TelegramBot()
start = time.time()

def solfunct(solver,name,dzn,tl,orig):
    try:
        tipo = orig.split("-")[1] #RD or SS
        data_distr = dzn.split("/")[3] 
        config = dzn.split("/")[2] 
        model = Model(f"./solvers/{tipo}/JSP{dzn.split('/')[-2]}.mzn")
        model.add_file(dzn,parse_data=True)
        instance = Instance(Solver.lookup(solver), model)
        result = instance.solve(timeout=timedelta(seconds=60))
        if result:
            save = result.__dict__
            if "status" in save.keys() : save['status'] = str(result.status)
            if "solution" in save.keys() : save["solution"] =  result.solution.__dict__
            if "time" in save["statistics"].keys() : save["statistics"]["time"] = save["statistics"]["time"].total_seconds() * 1000
            if "optTime" in save["statistics"].keys() : save["statistics"]["optTime"] = save["statistics"]["optTime"].total_seconds() * 1000
            if "flatTime" in save["statistics"].keys(): save["statistics"]["flatTime"] = save["statistics"]["flatTime"].total_seconds() * 1000
            if "initTime" in save["statistics"].keys()  : save["statistics"]["initTime"] = save["statistics"]["initTime"].total_seconds() * 1000
            if "solveTime" in save["statistics"].keys() : save["statistics"]["solveTime"] = save["statistics"]["solveTime"].total_seconds() * 1000
        else:
            save = {'solution':'None'}
        
        #create if not exist
        sol_path = f"solutions/{tipo}/{solver}/{config}/{data_distr}/"
        os.makedirs(os.path.dirname(sol_path), exist_ok=True)
        with open(f"{sol_path}/{name}".replace(".dzn",".json"), 'w', encoding='utf-8') as f:
                json.dump(save, f, ensure_ascii=False, indent=4)
    except Exception as e:
        tl.send_message(f"ERROR IN {solver} - {name} : \n {str(e)}",disable_notification=True)
        save = {'solution':'None'}
        #create if not exist
        sol_path = f"solutions/{tipo}/{solver}/{config}/{data_distr}/"
        os.makedirs(os.path.dirname(sol_path), exist_ok=True)
        with open(f"{sol_path}/{name}".replace(".dzn",".json"), 'w', encoding='utf-8') as f:
                json.dump(save, f, ensure_ascii=False, indent=4)

try:
    #info telegram
    tl.send_message(f"Solver JSP start ({time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())})",disable_notification=True)
    for dnzpath in ["./JSP-SS-outputdzn/" ,"./JSP-RD-outputdzn/"]:
        orig = dnzpath.split("/")[1]
        files = [(f,os.path.join(root, f).replace("\\","/") ) for (root,dirs,files) in os.walk(dnzpath) for f in files ]
        solv_file = list(itertools.product(*[ ["cpsatlp","cplex"],files]))

        #info telegram
        tl.send_message(f"--- {len(files)} Files loaded({time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())})",disable_notification=True)

        Parallel(n_jobs=-1, backend="threading")(delayed(solfunct)(solver,name,save,tl,orig) for solver,(name,save) in tqdm(solv_file))
    
    
    #info telegram
    tl.send_message(f"Solver JSP finish ({time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())})",disable_notification=True)
except Exception as e:
    # tl.send_message(f"ERROR IN '{__file__}' : \n {' '.join(str(e).splitlines()[:5])+' /n ...'}")
    tl.send_message(f"ERROR IN '{__file__}' : \n {str(e)}")
    