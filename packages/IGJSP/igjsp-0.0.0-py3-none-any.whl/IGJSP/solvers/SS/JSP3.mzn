% Conjuntos
set of int: RD;
set of int: JOBS;
set of int: TASKS;
set of int: MACHINES;
set of int: SPEEDSCALING;

% Datos
array[JOBS,TASKS,SPEEDSCALING] of int: time;
array[JOBS,TASKS,SPEEDSCALING] of int: energy;
array[JOBS,TASKS] of int: precedence;

% Variables
array[MACHINES,JOBS,TASKS] of var 0..sum(time): start_time;
array[JOBS,TASKS,MACHINES] of var 0..1: assing;
array[JOBS,TASKS,SPEEDSCALING] of var 0..1: assing_speedscaling;

%Restriccion de tarea<->machine
constraint forall(j in JOBS,t in TASKS)(
    %precedence[j,t] ->task t->machine
    assing[j,t,precedence[j,t]+1] == 1
);
%Restriccion de job/task<->speedscalling
constraint forall(j in JOBS, t in TASKS)(
    sum(s in SPEEDSCALING)(assing_speedscaling[j,t, s]) == 1
);

%Restriccion de precedencia
constraint forall(m in MACHINES,j in JOBS,p in TASKS, s in TASKS, w in SPEEDSCALING)(
if p != s then
    if precedence[j,p] > precedence[j,s] then
        start_time[m,j,p] > start_time[m,j,s] + time[j,s,w]
    else
        start_time[m,j,s] > start_time[m,j,p] + time[j,p,w]
    endif
endif
);

% Variable para el makespan (tiempo total de finalización)
var int: makespan    = max(start_time);
var int: energy_cons = sum(j in JOBS,t in TASKS,s in SPEEDSCALING)(if assing_speedscaling[j,t,s] == 1 then energy[j,t,s] else 0 endif);
var int: ob = makespan + energy_cons;

% Función objetivo
solve minimize ob;

% Salida
output ["Objective function: \(ob)\n"];
output ["Makespan: \(makespan)\n"];
output ["Energy: \(energy_cons)\n"];
%output ["Start Times: \(start_time)\n"];
%output ["SpeedScaling: \(assing_speedscaling)\n"];