import numpy as np
from qiskit import QuantumCircuit 


qc = QuantumCircuit(3)
qc.h(0)
qc.p(np.pi / 2 ,  0)
qc.cx(0, 1) 
qc.cx(0 , 2 )

qc_measure  = qc.measure_all(inplace = False)

from qiskit.primitives import StatevectorSampler
sampler = StatevectorSampler()
job = sampler.run([qc_measure], shots = 1000 )
result = job.result() 
# 50% 000 in time - output   , 50% 111 output 
print(f" > Count : {result[0].data['meas'].get_counts()}")
       # 50%  0 | 1    :  output 

from qiskit.quantum_info import SparsePauliOp 
operator = SparsePauliOp.from_list([("XYY" , 1  ) , ( "XYX" , 1) , ("YXX" , 1  ) , ("YYY " , 1 ) ])

from qiskit.primitives import StatevectorEstimator 
estimator = StatevectorEstimator()
job = estimator.run([(qc, operator )] , precision = 1e-3 ) 
result = job.result() 
print( f"  > Expectation values  : {result[0].data.evs}") 