import os
import sys
import pdb
import product as pd
import time

'''
Author: NILADRI GOMES
Email: niladri.gomes@gmail.com
'''


def makeProductList(fname):
	'''
		Returns a list of relevant products and 
		Departments in form arrays
	'''
	f1 = open(fname,'r')
	header = f1.readline().split(",")
	dept_list = []
	# find max no of depts and products
	pid_max = -1 # product id max
	did_max = -1 # dept id max
	while True:
		line = f1.readline().strip().split(",")
		if len(line) < 2:
			break
		if pid_max < int(line[0]):
			pid_max = int(line[0])
		if did_max < int(line[-1]):
			did_max = int(line[-1])

	f1.close()
	
	# create arrays of max possible products and departments
	# keep one extra (LAST) slot of memory in the dept_list for a product whose department is unknown
	product_list = [None]*pid_max
	dept_list = [None]*(did_max+1)

	f1 = open(fname,'r')
	header = f1.readline().split(",")
	while True:
		line = f1.readline().strip().split(",")
		if len(line) < 2:
			break
		p = pd.Product(line)
		p_id = int(line[0])-1
		#check for double entry:
		if product_list[p_id] == None:
			product_list[p_id] = p
		else:
			print("Double entry error in product id")
		d_id = int(line[-1])-1
		if dept_list[d_id] == None:
			dept_list[d_id] = 1

	f1.close()
	return pid_max,did_max, product_list, dept_list
	 

def main():

	finp = open(sys.argv[1],'r')
	fout = open(sys.argv[3],'w')

	# create lists of products and departments 
	pid_max, did_max, product_list, dept_list = makeProductList(sys.argv[2]) 

	#number of departments- one extra for unknown department
	ndept = did_max+1 

	#keep track of number of orders in a dept
	num_order_dept = [0]*ndept 
	first_order_dept = [0]*ndept
	header = finp.readline().split(",")
	while True:
		line = finp.readline().strip().split(",")
		if len(line) < 2:
			break
		line = [int(i) for i in line]
		p_id = line[1]
		# EXCEPTIONS: if product id is not in product list 
		#	1) product id > pid_max 2) product id ~ None 
		#	send them to unknown department

		if (p_id > pid_max) or product_list[p_id-1]==None :
			# if product id not in product_list, push them to "unknown" dept
			dept_id = ndept
			print("Unidentified product found.. \n pushing to unknown dept")
			if dept_list[dept_id-1] == None:
				# activate the "unknown" dept
				dept_list[dept_id-1] = 1
				# this will be the first order from the "unknown" department, hence:
				product_order = 0
		else:
			product_order = product_list[p_id-1].getOrder()
			product_list[p_id-1].addOrder()
			dept_id = product_list[p_id-1].dept

		if line[-1] == 0 and product_order == 0:
	 		#check if first time ordered 
			first_order_dept[dept_id-1] += 1
			
		num_order_dept[dept_id-1] += 1

	

	finp.close()
	
	#write answer to the output file
	
	header = "department_id,number_of_orders,number_of_first_orders,percentage"
	#print(header)
	fout.write(header+"\n")
	for i in range(ndept):
		#check if the dept is relevant
		if dept_list[i] == None:
			continue
	
		if float(num_order_dept[i]) == 0:
			ratio = 0
		else:
			ratio = float(first_order_dept[i])/float(num_order_dept[i])
		#print("%d,%d,%d,%.2f"%(i+1, num_order_dept[i], first_order_dept[i],ratio) )
		fout.write("%d,%d,%d,%.2f\n"%(i+1, num_order_dept[i], first_order_dept[i],ratio) )



	fout.close()
	pass



if __name__=="__main__":
	start_t = time.time()
	main()
	end_t = time.time()
	print("time: %fs"%(end_t-start_t))


