from qiskit import QuantumCircuit 

qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0 , 1)

qc.measure_all()
qc.draw(output="mpl" , filename="./sampler.png")


from qiskit.primitives import StatevectorSampler

qc_measure = qc.measure_all(inplace = False)
sampler = StatevectorSampler()
job = sampler.run([qc_measure] , shots= 1000)
result = job.result()
print(result[0].data["meas"].get_counts())
