"""
Práctica 1: Mecánica pulmonar

Departamento de Ingeniería Eléctrica y Electrónica, Ingeniería Biomédica
Tecnológico Nacional de México [TecNM - Tijuana]
Blvd. Alberto Limón Padilla s/n, C.P. 22454, Tijuana, B.C., México

Nombre del alumno: Marin Paredes Leslie Avelladith
Número de control: 20212506
Correo institucional: l20212506@tectijuana.edu.mx

Asignatura: Modelado de Sistemas Fisiológicos
Docente: Dr. Paul Antonio Valle Trujillo; paul.valle@tectijuana.edu.mx
"""
# Instalar librerias en consola
#!pip install control
#!pip install slycot

# Librerías para cálculo numérico y generación de gráficas
import numpy as np
import math as m 
import matplotlib.pyplot as plt
import control as ctrl

# Datos de la simulación
x0,t0,tend,dt,w,h = 0,0,10,1E-3,6,3
N = round((tend-t0)/dt) + 1 #veces de solucion numerica, numeros enteros
t = np.linspace(t0,tend,N) #linea de tiempo de 0,10
u1 = np.ones(N) #señal escalon
u2 = np.zeros(N); u2[round(1/dt):round(2/dt)] = 1 # señal impulso, solo 0 excepto en el intervalo 1/dt y 2/dt
u3 = (np.linspace(0,tend,N))/tend #señal rampa con pendiente 1/10
u4 = np.sin(m.pi/2*t) #señal funcion sinusoidal, pi/2 = 250 mHz

#arreglo de todas las señales
u = np.stack((u1,u2,u3,u4), axis=1) #junta las funciones en una sola matriz
signal = ['Escalon', 'Impulso','Rampa','Sin']

# Componentes del circuito RLC y función de transferencia
R = 3E3 # CALCULAR LA RESISTENCIA
L = 1E-3 #
C = 220E-6 #PROPONER CAPACITOR

#funcion de transferencia viene con denominador y numerador
num = [(R*C*L),((C*(R**2))+1),R] #sacado de la funcion PA(S)/Pao(S) = -->1<-- / CLS^2+RCS+1
den = [3*R*C*L,((5*(R**2)*C)+L),2*R] #S2, S, CONSTANTE si fuera cubica sería S3, S2, S, CONSTANTE 1 / --> CLS^2+RCS+1 <--

#aplicacion de la funcion de transferencia
sys = ctrl.tf(num,den)
print(sys) #despliegue de funcion de transferencia

# - - - - - - - - - - - - CONTROLADOR - - - - - - - - - - - - - - - - - - -

# Componentes del controlador
# Rr,Re,Cr
KI = 182
KP = 0.86
Cr = 1E-6
Re = 1/(KI*Cr); print('Re =', Re)
Rr = (KP*Re); print('Rr =', Rr)
numPI = [(Rr*Cr)+1]
denPI = (Re*Cr,0)
PI = ctrl.tf(numPI,denPI)
print(PI)

# Sistema de control en lazo cerrado SYSPID
X = ctrl.series(PI,sys) #FUNCION DE SERIES DE LIBRERIA DE CONTROL multiplicacion de funciones de transferencia
sysPI = ctrl.feedback(X,1, sign = -1) #retroalimentacion de x
print(sysPI) #FUNCION DE TRANSFERENCIA

fig1 = plt.figure(); #1era figura codigo basado en page 87
#grafica de entrada, escalon, funcion constante, con valor de 1
plt.plot(t,u1,'-', linewidth=3, color = [0.8,0.3,0.6], label = 'Ve(t)' ) # ENTRADA tiempo con respecto a la primera entrada, como linea solida, colocar colores del 0 al 1
_,PA=ctrl.forced_response(sys,t,u1,x0) #dos columnas, tiempo y respuesta el guion bajo significa que no nos interesa ese punto de la funcion
plt.plot(t,PA,'-', linewidth=3, color = [0.3,0.8,0.8], label = 'Vs(t)' ) #RESPUESTA
# + EL PID
_, VPI = ctrl.forced_response(sysPI,t,u1,x0)
plt.plot(t,VPI,':',linewidth=5.2, color = [0.9,0.6,0.3], label = 'VPI(t)' )
plt.xlim(-0.15,10); plt.xticks(np.arange(0,11,1.0))
plt.ylim(0,1.1); plt.yticks(np.arange(0,1.2,0.1))
plt.ylabel('V(t) [V]', fontsize =11)
plt.xlabel('(t) [s]', fontsize =11)
plt.legend(bbox_to_anchor = (0.5,-0.3), loc = 'center', ncol = 3, fontsize = 8, frameon = False)
plt.show()
#guardar figura
fig1.savefig('step.pdf',bbox_inches ='tight')

fig2 = plt.figure(); #1era figura codigo basado en page 87
#grafica de entrada, escalon, funcion constante, con valor de 1
plt.plot(t,u2,'-',linewidth=3, color = [0.8,0.3,0.6], label = 'Ve(t)' ) # ENTRADA tiempo con respecto a la primera entrada, como linea solida, colocar colores del 0 al 1
_,PA=ctrl.forced_response(sys,t,u2,x0) #dos columnas, tiempo y respuesta el guion bajo significa que no nos interesa ese punto de la funcion
plt.plot(t,PA,'-', linewidth=3, color = [0.1,0.3,0.9], label = 'Vs(t)' ) #RESPUESTA
_, VPI= ctrl.forced_response(sysPI,t,u2,x0)
plt.plot(t,VPI,':',linewidth=5.2, color = [0.9,0.6,0.3], label = 'VPI(t)' )
plt.xlim(-0.15,10); plt.xticks(np.arange(0,11,1.0))
plt.ylim(0,1.2); plt.yticks(np.arange(0,1.3,0.1))
plt.ylabel('V(t) [V]', fontsize =11)
plt.xlabel('(t) [s]', fontsize =11)
plt.legend(bbox_to_anchor = (0.5,-0.3), loc = 'center', ncol = 3, fontsize = 8, frameon = False)
plt.show()
fig2.savefig('step2.pdf',bbox_inches ='tight')

fig3 = plt.figure(); #1era figura codigo basado en page 87
#grafica de entrada, escalon, funcion constante, con valor de 1
plt.plot(t,u3,'-', linewidth=3, color = [0.8,0.3,0.6], label = 'Ve(t)' ) # ENTRADA tiempo con respecto a la primera entrada, como linea solida, colocar colores del 0 al 1
_,PA=ctrl.forced_response(sys,t,u3,x0) #dos columnas, tiempo y respuesta el guion bajo significa que no nos interesa ese punto de la funcion
plt.plot(t,PA,'-',linewidth=3, color = [0.3,0.8,0.8], label = 'Vs(t)' ) #RESPUESTA
_, VPI = ctrl.forced_response(sysPI,t,u3,x0)
plt.plot(t,VPI,':',linewidth=5.2, color = [0.9,0.6,0.3], label = 'VPI(t)' )
plt.xlim(-0.15,10); plt.xticks(np.arange(0,11,1.0))
plt.ylim(0,1.2); plt.yticks(np.arange(0,1.3,0.1))
plt.ylabel('V(t) [V]', fontsize =11)
plt.xlabel('(t) [s]', fontsize =11)
plt.legend(bbox_to_anchor = (0.5,-0.3), loc = 'center', ncol = 3, fontsize = 8, frameon = False)
plt.show()
fig3.savefig('step3.pdf',bbox_inches ='tight')

fig4 = plt.figure(); #1era figura codigo basado en page 87
#grafica de entrada, escalon, funcion constante, con valor de 1
plt.plot(t,u4,'-', linewidth=3, color = [0.8,0.3,0.6], label = 'Ve(t)' ) # ENTRADA tiempo con respecto a la primera entrada, como linea solida, colocar colores del 0 al 1
_,PA=ctrl.forced_response(sys,t,u4,x0) #dos columnas, tiempo y respuesta el guion bajo significa que no nos interesa ese punto de la funcion
plt.plot(t,PA,'-', linewidth=3, color = [0.3,0.8,0.8], label = 'Vs(t)' ) #RESPUESTA
_, VPI= ctrl.forced_response(sysPI,t,u4,x0)
plt.plot(t,VPI,':',linewidth=5.2, color = [0.9,0.6,0.3], label = 'VPI(t)' )
plt.xlim(-0.15,10); plt.xticks(np.arange(0,11,1.0))
plt.ylim(-1,1.2); plt.yticks(np.arange(-1.2,1.3,0.2))
plt.ylabel('V(t) [V]', fontsize =11)
plt.xlabel('(t) [s]', fontsize =11)
plt.legend(bbox_to_anchor = (0.5,-0.3), loc = 'center', ncol = 3, fontsize = 8, frameon = False)
plt.show()
fig4.savefig('step4.pdf',bbox_inches ='tight')