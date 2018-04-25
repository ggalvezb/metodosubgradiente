#Ubiacion: C:\Users\ggalv\Google Drive\Respaldo\Magister\Modelos deterministicos    Ejecutable: python metodo_subgradiente_capacidad.py
import time
import numpy as np
import cplex
from cplex import Cplex
from cplex.exceptions import CplexError
import sys
import pandas as pd


def metodo_subgradiente(lambdas):
	print ("lambdas=",lambdas)
	x_resultante,lower_bound=resolver_modelo(M,N,c,a,b,pi,upper_bound,lambdas)
	print("resultado iteracion =",lower_bound)
	#Formo los gradientes----------------------------------------------------------
	a_gradiente1=[]
	a_gradiente2=[]
	for i in range(len(x_resultante)):
		if x_resultante[i][0]==0:
			a_gradiente1.append(a[x_resultante[i][0]][x_resultante[i][1]])
		else:
			a_gradiente2.append(a[x_resultante[i][0]][x_resultante[i][1]])	
	a_gradiente1=sum(a_gradiente1)
	a_gradiente2=sum(a_gradiente2)
	gradiente1=a_gradiente1-b[0][0]
	gradiente2=a_gradiente2-b[1][0]
	gradiente=[gradiente1,gradiente2]
	#print("gradientes=",gradiente)

	#Tamaño de paso-----------------------------------------------------------------
	tamaño_de_paso=(pi*(upper_bound - lower_bound))/(gradiente1**2 + gradiente2**2)
	#print("tamaño_de_paso=",tamaño_de_paso)
	#Nuevos lambdas-----------------------------------------------------------------
	i=0
	for i in range(M):
		lambdatemp=max(0,lambdas[i] + tamaño_de_paso * gradiente[i])
		lambdas[i]=lambdatemp
		#print("lambdas antes de salir",lambdas)
	return(lambdas,lower_bound)	

def resolver_modelo(M,N,c,a,b,pi,upper_bound,lambdas):
	#print("LAMBDAS DENTRO DE LA FUNCION CREAR MODELO",lambdas)
	Model = cplex.Cplex()
	before = time.clock()
	T_exec = 3600

	#print("N = {} | D = {} | P = {} | K = {} | V = {}\n".format(N,D,P,K,V))

	#Variable de decision----------------------------------------------------------------------------------------------
	x_vars = np.array([["x(" + str(i) + "," +str(j)+ ")"  for j in range(0,N)] for i in range(0,M)])
	x_varnames = x_vars.flatten()
	x_vartypes = 'B'*len(x_varnames)
	x_varlb = [0.0]*len(x_varnames)
	x_varub = [1.0]*len(x_varnames)
	x_varobj = []
	for i in range(M):
		for j in range(N):
			p=[]
			o=[]
			l=[]
			g=a[i][j]
			o=lambdas[i]
			#print("soy O",o)
			l=c[i][j]
			x_varobj.append(float(l+o*g))	
	Model.variables.add(obj = x_varobj, lb = x_varlb, ub = x_varub, types = x_vartypes, names = x_varnames)	

	Model.objective.set_sense(Model.objective.sense.minimize)				

	#Restricciones -----------------------------------------------------------------------------------------------------

	for j in range(N):
		row = []
		val = []
		for i in range(M):
			row.append(x_vars[i,j])
			val.append(1)
		Model.linear_constraints.add(lin_expr = [cplex.SparsePair(ind = row, val = val)], senses = 'E', rhs = [1])
		print("ROW=",row)
		print("VAL=",val)




	Model.parameters.timelimit.set(float(T_exec))
	Model.parameters.workmem.set(9000.0)
	Model.solve()
	
	#Mostrar soluciones
	"""
	def show_solution():
			print("\nObjective Function Value = {}".format((Model.solution.get_objective_value()-resta)))
			for i in range(0,M):
				for j in range(0,N):
					if(Model.solution.get_values("x("+str(i)+","+str(j)+")")!=0.0):
						print("x("+str(i)+","+str(j)+")"+" = "+str(Model.solution.get_values("x("+str(i)+","+str(j)+")")))
			print("")

	show_solution()
	"""

	x_resultante=[]
	for i in range(M):
		for j in range(N):
			if(Model.solution.get_values("x("+str(i)+","+str(j)+")")!=0.0):
				x_resultante.append((i,j))
	#print(x_resultante)
	#print("resta",resta)
	lower_bound=Model.solution.get_objective_value()-resta
	return(x_resultante,lower_bound)						

Nro_iteraciones=10
M=2
N=7
c=[[6,9,4,2,10,3,6],[4,8,9,1,7,5,4]]
a=[[4,1,2,1,4,3,8],[9,9,8,1,3,8,7]]
b=[[11],[22]]
pi=1
upper_bound=32
#lambdas=[0,0]
#lambdas=[0,1]
#lambdas=[1,0]
lambdas=[1,1]
valores_Z=[]


for i in range(Nro_iteraciones):
	print("LAMBDAS EN MAIN=",lambdas)
	resta=b[0][0]*lambdas[0]+b[1][0]*lambdas[1]
	y,z=metodo_subgradiente(lambdas)
	lambdas=y
	valores_Z.append(z)
df = pd.DataFrame(valores_Z, columns=["valores_Z"])
df.to_csv('list.txt', index=True)