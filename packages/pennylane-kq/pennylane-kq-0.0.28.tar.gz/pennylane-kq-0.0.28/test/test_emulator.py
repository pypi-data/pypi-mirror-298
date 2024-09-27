import pennylane as qml

accessKeyId = "DV7Z3NNQZET1O1QLIS31ZE32OOQTEIFE"
secretAccessKey = "TEhIFzeZhXiR1bIO/DZ8+lyiA8VZp+qHEKc6fxaOIAM="

dev = qml.device(
    "kq.emulator",
    wires=2,
    shots=2048,
    accessKeyId=accessKeyId,
    secretAccessKey=secretAccessKey,
)


@qml.qnode(dev)
def circuit():
    qml.Hadamard(wires=1)
    qml.CNOT(wires=[1, 0])
    return qml.expval(qml.PauliZ(1))


result = circuit()
print(result)
