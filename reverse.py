from qiskit import QuantumCircuit 

from qiskit.circuit import Gate , QuantumCircuit
from qiskit.quantum_info import Operator 
import numpy as np
from qiskit.primitives import StatevectorSampler 

#Define matrix for n gate 
N_matrix = np.array([
    [0 , 1] , [1 , 0]
])
class NGate(Gate) :
    def __init__(self):
        super().__init__('n' , 1 , [])
    def _define(self):
        qc = QuantumCircuit(1)
        qc.unitary(Operator(N_matrix),[0],label='N')
        self.definition = qc
n_gate =  NGate()
def n(self, qubit):
        return self.append(n_gate, [qubit])
QuantumCircuit.n = n

A_matrix = np.array([
    [0, 1],
    [1, 0]
])

class AGate(Gate):
    def __init__(self):
        super().__init__('a', 1, [])

    def _define(self):
        qc = QuantumCircuit(1)
        qc.unitary(Operator(A_matrix), [0], label="A")
        self.definition = qc

a_gate = AGate()

def a(self, qubit):
    return self.append(a_gate, [qubit])

QuantumCircuit.a = a

M_matrix = np.array([ [0,1] , [1,0]])
class MGate(Gate): 
    def __init__(self):
        super().__init__('m' , 1 , [])
    def _define(self):
        qc  = QuantumCircuit(1)
        qc.unitary(Operator(M_matrix) , [0] , label="M")
        self.definition = qc 
m_gate = MGate()
def m(self, qubit):
    return self.append(m_gate, [qubit])
QuantumCircuit.m = m

O_matrix = np.array([ [0,1] , [1,0]])
class OGate(Gate):
    def __init__(self):
        super().__init__('o', 1 , [])
    def _define(self):
        qc = QuantumCircuit(1)
        qc.unitary(Operator(O_matrix) , [0] , label="O")
        self.definition = qc
o_gate = OGate()
def o(self , qubit):
    return self.append(o_gate, [qubit])
QuantumCircuit.o = o 

R_matrix = np.array([ [0,1] , [1,0]])
class RGate(Gate):
    def __init__(self):
        super().__init__('r' , 1 , [])
    def _define(self):
        qc = QuantumCircuit(1)
        qc.unitary(Operator(R_matrix) , [0] , label="O")
        self.definition = qc
r_gate = RGate()
def r(self, qubit):
    return self.append(r_gate , [qubit])
QuantumCircuit.r = r

I_matrix = np.array([[0,1] , [1,0]])
class IGate(Gate): 
    def __init__(self):
        super().__init__("i" , 1 , [])
    def _define(self):
        qc = QuantumCircuit(1)
        qc.unitary(Operator(I_matrix ), [0] , label ="I" )
        self.definition = qc
i_gate = IGate()
def i(self , qubit):
    return self.append(i_gate , [qubit])
QuantumCircuit.i = i
R_matrix = np.array([[0,1] , [1,0]])
class RGate(Gate):
    def __init__(self):
        super().__init__("r" , 1 , [])
    def _define(self):
        qc = QuantumCircuit(1)
        qc.unitary(Operator(R_matrix), [0] , label="R")
        self.definition = qc
r_gate = RGate()
def r(self , qubit): 
    return self.append(r_gate , [qubit])
QuantumCircuit.r = r

G_matrix = np.array([[0,1] , [1,0]])
class GGate(Gate):
    def __init__(self):
        super().__init__("g" , 1 , [])
    def _define(self):
        qc = QuantumCircuit(1)
        qc.unitary(Operator(G_matrix), [0] , label="G")
        self.definition = qc
g_gate = GGate()
def g(self , qubit):
    return self.append(g_gate , [qubit])
QuantumCircuit.g = g

K_matrix =np.array([[0,1] , [1,0]])
class KGate(Gate):
    def __init__(self):
        super().__init__("k" , 1 , [])
    def _define(self):
        qc = QuantumCircuit(1)
        qc.unitary(Operator(K_matrix) , [0] , label ="K")
        self.definition = qc
k_gate = KGate()
def k(self , qubit):
    return self.append(k_gate , [qubit])
QuantumCircuit.k = k 
#control gate state 

cr_gate = r_gate.control(1 , ctrl_state=1)
def cr(self , control , target , state = 1):
    gate = r_gate.control(1 , ctrl_state = state , label='1')
    return self.append(gate  , [control , target])
QuantumCircuit.cr = cr

ca_gate = a_gate.control(1 , ctrl_state= 0)
def ca(self , control , target , state = 0):
    gate = a_gate.control(1 , ctrl_state= state , label = '0')
    return self.append(gate , [control , target])
QuantumCircuit.ca = ca
cg_gate = g_gate.control(1, ctrl_state= 1)
def cg(self , control , target , state = 1):
    gate = g_gate.control(1 , ctrl_state=state , label= "1")
    return self.append(gate , [control , target])
QuantumCircuit.cg = cg
ck_gate = k_gate.control(1 , ctrl_state=0)
def ck(self , control , target , state):
    gate = k_gate.control(1 ,  ctrl_state=state , label = "0")
    return self.append(gate , [control , target ])
QuantumCircuit.ck = ck 
ci_gate = i_gate.control(1 , ctrl_state=1)
def ci(self , control , target , state):
    gate = i_gate.control(1 , ctrl_state=state , label="1")
    return self.append(gate, [control , target])
QuantumCircuit.ci = ci


qc = QuantumCircuit(7)
qc.i(0)
qc.n(1)
qc.a(2)
qc.m(3)
qc.o(4)
qc.r(5)
qc.i(6)
qc_reversed = qc.reverse_bits()
print(qc_reversed.draw())
print(qc.draw())
#didnt have q_0 control gate  start with q_1 control
qc.cr(0,1 , state=1)  # 1st qubit
qc.ca(0,2 , state=0)  # 2
qc.cg(0,3 , state=1)  # 3
qc.ca(0,4 , state=0)  # 4
qc.ck(0,5 , state=0)  # 5
qc.ci(0,6 , state=1)  # 6
print(qc.draw())
qc.measure_all()
sampler = StatevectorSampler()
job = sampler.run([qc])
result = job.result()
counts = result[0].data.meas.get_counts()
bitstring = list(counts.keys())[0]
print("Raw:" , bitstring)
print("Revesred:" , bitstring[:: -1])
print("State: |" + bitstring[::-1] + "⟩")
# in left side INAMORI CONTROL STATE ALL = 1  so q_0 not have gate control set so all 0 flip to 11111111  -> : Revesred: 1010110  , 1 is state qc.i at first place 
# left side first state INAMORI control state = 1
# flip from  0 -> 1 , 1 -> 0 , in X gate , matrix [0,1 ] , [1 , 0]