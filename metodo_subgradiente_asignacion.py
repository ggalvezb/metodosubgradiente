#Ubiacion: C:\Users\ggalv\Google Drive\Respaldo\Magister\Modelos deterministicos    Ejecutable: python metodo_subgradiente_asignacion.py
import time
import numpy as np
import cplex
from cplex import Cplex
from cplex.exceptions import CplexError
import sys

def metodo_subgradiente(lambdas,resta):
	print ("lambdas=",lambdas)
	print("HOLA")
	x_resultante,lower_bound=resolver_modelo(M,N,c,a,b,pi,upper_bound,lambdas,resta)
	print("x_resultante=",x_resultante)
	print("resultado iteracion =",lower_bound)
	#Formo los gradientes----------------------------------------------------------
	a_gradiente1=[]
	a_gradiente2=[]
	a_gradiente3=[]
	a_gradiente4=[]
	a_gradiente5=[]
	a_gradiente6=[]
	a_gradiente7=[]
	for i in range(len(x_resultante)):
		if x_resultante[i][1]==0:
			a_gradiente1.append(1)
		elif x_resultante[i][1]==1:
			a_gradiente2.append(1)
		elif x_resultante[i][1]==2:
			a_gradiente3.append(1)
		elif x_resultante[i][1]==3:
			a_gradiente4.append(1)
		elif x_resultante[i][1]==4:
			a_gradiente5.append(1)
		elif x_resultante[i][1]==5:
			a_gradiente6.append(1)
		else:
			a_gradiente7.append(1)								
	a_gradiente1=sum(a_gradiente1)
	a_gradiente2=sum(a_gradiente2)
	a_gradiente3=sum(a_gradiente3)
	a_gradiente4=sum(a_gradiente4)
	a_gradiente5=sum(a_gradiente5)
	a_gradiente6=sum(a_gradiente6)
	a_gradiente7=sum(a_gradiente7)
	print(type(a_gradiente1))
	print(a_gradiente2)
	print(a_gradiente3)
	print(a_gradiente4)
	print(a_gradiente5)
	print(a_gradiente6)
	print(a_gradiente7)
	gradiente1=a_gradiente1-1
	gradiente2=a_gradiente2-1
	gradiente3=a_gradiente3-1
	gradiente4=a_gradiente4-1
	gradiente5=a_gradiente5-1
	gradiente6=a_gradiente6-1
	gradiente7=a_gradiente7-1
	gradiente=[gradiente1,gradiente2,gradiente3,gradiente4,gradiente5,gradiente6,gradiente7]
	print("gradientes=",gradiente)

	#Tamaño de paso-----------------------------------------------------------------
	# if gradiente1==0 and gradiente2==0 and gradiente3==0 and gradiente4==0 and gradiente5==0 and gradiente6==0 and gradiente7==0:
	# 	tamaño_de_paso=0
	# else:	
	tamaño_de_paso=(pi*(upper_bound - lower_bound))/(gradiente1**2 + gradiente2**2 + gradiente3**2 + gradiente4**2 + gradiente5**2 + gradiente6**2 + gradiente7**2)
	print("Tamaño de paso=",tamaño_de_paso	)
	#print("tamaño_de_paso=",tamaño_de_paso)
	#Nuevos lambdas-----------------------------------------------------------------
	i=0
	for i in range(N):
		lambdatemp=lambdas[i] + tamaño_de_paso * gradiente[i]
		lambdas[i]=lambdatemp
		#print("lambdas antes de salir",lambdas)
	return(lambdas)	

def resolver_modelo(M,N,c,a,b,pi,upper_bound,lambdas,resta):
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


	for i in range(M):
		row = []
		val = []
		for j in range(N):
			row.append(x_vars[i,j])
			val.append(a[i][j])
		Model.linear_constraints.add(lin_expr = [cplex.SparsePair(ind = row, val = val)], senses = 'L', rhs = [float(b[i][0])])

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
	lower_bound=Model.solution.get_objective_value() - resta
	return(x_resultante,lower_bound)						


Nro_iteraciones=10
M=2
N=7
c=[[6,9,4,2,10,3,6],[4,8,9,1,7,5,4]]
a=[[4,1,2,1,4,3,8],[9,9,8,1,3,8,7]]
b=[[11],[22]]
pi=1
upper_bound=32
#lambdas=[0,0,0,0,0,0,0]
lambdas=[1,1,1,0,0,0,0]
#lambdas=[0,0,0,1,1,1,1]
#lambdas=[1,1,1,1,1,1,1]


for i in range(Nro_iteraciones):
	print("INICIO ITERACION" + " " + str(i)+"-------------------------------------------------------------------")
	print("LAMBDAS EN MAIN=",lambdas)
	print(type(lambdas[0]))
	resta = lambdas[0] + lambdas[1] + lambdas[2] + lambdas[3] + lambdas[4] + lambdas[5] + lambdas[6]
	y=metodo_subgradiente(lambdas,resta)
	lambdas=y


