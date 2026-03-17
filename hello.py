import numpy as np 
from qiskit import QuantumCircuit 


qc = QuantumCircuit(3)

qc.h(0) 
qc.p(np.pi/2 , 0)
qc.cx(0, 1) 
qc.cx(0, 2)


qc.draw(output="mpl", filename="./hello3.png")