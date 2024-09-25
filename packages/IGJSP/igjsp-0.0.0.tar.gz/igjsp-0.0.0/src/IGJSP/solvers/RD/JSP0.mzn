% Conjuntos
set of int: RD;
set of int: JOBS;
set of int: TASKS;
set of int: MACHINES;

% Datos
array[JOBS,TASKS] of int: time;
array[JOBS,TASKS] of int: energy;
array[JOBS,TASKS] of int: precedence;

% Variables
array[MACHINES,JOBS,TASKS] of var 0..sum(time): start_time;
array[JOBS,TASKS,MACHINES] of var 0..1: assing;

%Restriccion de tarea<->machine
constraint forall(j in JOBS,t in TASKS)(
    %precedence[j,t] ->task t->machine
    assing[j,t,precedence[j,t]+1] == 1
);

%Restriccion de precedencia
constraint forall(m in MACHINES,j in JOBS,p in TASKS, s in TASKS)(
if p != s then
    if precedence[j,p] > precedence[j,s] then
        start_time[m,j,p] > start_time[m,j,s] + time[j,s]
    else
        start_time[m,j,s] > start_time[m,j,p] + time[j,p]
    endif
endif
);

% Variable para el makespan (tiempo total de finalización)
var int: makespan = max(start_time);

var int: ob = makespan;
% Función objetivo (minimizar el makespan)
solve minimize ob; %+energy_cons

% Salida
output ["Objective function: \(ob)\n"];
output ["Makespan: \(makespan)\n"];
output ["Start Times: \(start_time)\n"];