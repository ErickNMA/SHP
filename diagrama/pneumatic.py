import numpy as np
import matplotlib.pyplot as plt
import scienceplots

# Configurações de plot:
plt.style.use([
    'grid',
    'retro'
])
plt.rcParams['lines.linewidth'] = 5
plt.rcParams['font.size'] = 20
plt.rcParams['figure.figsize'] = (12, 5)

class PNEUMATIC:
    cilinder = []
    positions = []
    time = [0]
    changings = []
    ct = 0

    def __init__(self, pressure, airflow, ts=1e-2): #MPa e l/min
        self.pressure = (pressure*1e6)
        self.airflow = (airflow*1e6/60)
        self.ts = ts
    
    def addActuator(self, label, corse, D, d, P0): # mm
        self.cilinder.append([label, corse, (np.pi*(D**2)/4), (np.pi*(d**2)/4)])
        self.positions.append([P0])
    
    def addComand(self, com):
        for i in range(len(self.cilinder)):
            if(self.cilinder[i][0] == com[0]):
                break
        if(com[1] == '+'):
            v = (self.airflow/self.cilinder[i][2])
        elif(com[1] == '-'):
            v = -(self.airflow/self.cilinder[i][3])
        if(self.ct not in self.changings):
            self.changings.append(self.ct)
        dt = (self.cilinder[i][1]/abs(v))
        temp = np.arange(self.ts, (dt+self.ts), self.ts)
        p0 = self.positions[i][-1]
        for t in temp:
            self.time.append(self.ct + t)
            for j in range(len(self.positions)):
                if(j == i):
                    self.positions[j].append(p0+(v*t))
                else:
                    self.positions[j].append(self.positions[j][-1])
        if(v>0):
            self.positions[i][-1] = self.cilinder[i][1]
        elif(v<0):
            self.positions[i][-1] = 0
        self.ct = self.ct + dt
        self.changings.append(self.ct)
    
    def delay(self, millis):
        temp = np.arange(self.ts, (millis*1e-3), self.ts)
        for t in temp:
            self.time.append(self.ct + t)
            for j in range(len(self.positions)):
                self.positions[j].append(self.positions[j][-1])
        self.ct = self.ct + (millis*1e-3)
    
    def simulate(self):
        del self.changings[-1]
        
        plt.figure()
        lmax = 0
        for i in self.cilinder:
            if(i[1] > lmax):
                lmax = i[1]
        for i in range(len(self.positions)):
            plt.plot(self.time, self.positions[i], label=self.cilinder[i][0])
        for i in range(len(self.changings)):
            plt.plot((self.changings[i], self.changings[i]), (0, lmax), color='gray', linestyle='dashed', linewidth=3, label=f'$S_{i+1}$')
        plt.ylabel('Deslocamento [mm]')
        plt.xlabel('Tempo [s]')
        plt.legend()
        plt.show()

        sensors = []
        labels = []
        for i in range(len(self.positions)):
            labels.append(self.cilinder[i][0]+'-')
            labels.append(self.cilinder[i][0]+'+')
            sensors.append([])
            sensors.append([])
            for j in range(len(self.positions[i])):
                if(self.positions[i][j]<1e-2):
                    sensors[(2*i)].append(1)
                else:
                    sensors[(2*i)].append(0)
                if(abs(self.positions[i][j]-self.cilinder[i][1])<1e-2):
                    sensors[(2*i)+1].append(1)
                else:
                    sensors[(2*i)+1].append(0)
        plt.subplots(len(sensors), sharex=True)
        for i in range(len(sensors)):
            plt.subplot(len(sensors), 1, i+1)
            plt.plot(self.time, sensors[i], linewidth=3)
            for j in range(len(self.changings)):
                plt.plot((self.changings[j], self.changings[j]), (0, 1), color='gray', linestyle='dashed', linewidth=3)
            plt.ylabel(labels[i])
        plt.xlabel('Tempo [s]')
        plt.show()