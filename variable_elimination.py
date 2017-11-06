'''
factor0 = (['A'], {True: 0.7, False: 0.3})
factor1 = (['B'], {True: 0.4, False: 0.6})
factor2 = (['A', 'B', 'C'], {(False, False, False): 0.12, (False, False, True): 0.48, (False, True, True): 0.28, (False, True, False): 0.12, (True, False, True): 0.08, (True, False, False): 0.02, (True, True, True): 0.63, (True, True, False): 0.27})
factor3 = (['C', 'D'], {(False, False): 0.2, (False, True): 0.8, (True, True): 0.7, (True, False): 0.3})
'''

def sumout(factor, variable):
	# get the position of variable in the list of variables (factor[0])
	pos = [i for i,x in enumerate(factor[0]) if x == variable]
	pos = pos[0]
	# assign var to the list of variables in factor[0]
	var = list(factor[0])
	# remove the current variable
	var.remove(variable)
	# assign d to the dictionary with the CPT
	d = factor[1]
	# create new dictionary for the new probabilities and keys
	new_prob = {}
	#for all keys in the factor
	for i1 in range(len(d.keys())):
		# get all keys
		u = list(d.keys())
		# get the specific keys at position i1
		u_del = list(u[i1])
	  	# delete the entry of the current variable (at pos)
		del u_del[pos]
		#for all keys after i1
		for i2 in range(i1+1, len(d.keys())):
			# get the list of all keys
			v = list(d.keys())
			# get the specific key at pos i2
			v_del = list(v[i2])
			# delete entry of current var at this position
			del v_del[pos]
			# check the length: important for creating the dictionary entries
			if len(u_del) > 1:
				# if remaining keys are the same
				if u_del == v_del:
			    	# add values to dict
					new_prob[tuple(u_del)] = d[u[i1]] + d[v[i2]]
			else:
				# if remaining keys are the same
				if u_del == v_del:
			    	# add values to dict
					new_prob[u_del[0]] = d[u[i1]] + d[v[i2]]

	# create new factor and return it
	new_factor = (var, new_prob)
	return new_factor

def multiply(factor1, factor2):
	# list of variables from both factors
	var1 = list(factor1[0])
	var2 = list(factor2[0])
	# look for the first common variable in both lists
	for i in var1:
		for j in var2:
			if i == j:
				common_var = i
				break;

	# position of common variable in factor 1
	pos1 = [i for i,x in enumerate(factor1[0]) if x == common_var]
	pos1 = pos1[0]
	# position of common variable in factor 2
	pos2 = [i for i,x in enumerate(factor2[0]) if x == common_var]
	pos2 = pos2[0]

	# assign dictionaries to d1 and d2
	d1 = factor1[1]
	d2 = factor2[1]

	# create new dictionary
	new_prob = {}
	# make a copy of var2 and delete the common variable from it
	tmp_var = list(var2)
	del tmp_var[pos2]
	# new list of variables consist of the values of var1 and the values of var2 without the common variable
	new_var = var1 + tmp_var

	# for all entries in the first factor
	for i1 in range(len(d1.keys())):
		# get all the keys
		all_keys1 = list(d1.keys())
		# check the length of var1 and get specific key
		# problems when var1 is just a bool --> have to distinguish
		if len(var1) > 1:
			key1 = list(all_keys1[i1])
		else:
			key1 = list([all_keys1[i1]])
		# for all entries in factor2
		for i2 in range(len(d2.keys())):
			# get all the keys
			all_keys2 = list(d2.keys())
			# check length and get specific key
			if len(var2) > 1:
				key2 = list(all_keys2[i2])
			else:
				key2 = list([all_keys2[i2]])
			# check if the boolean of the common variable is the same
			if key1[pos1] == key2[pos2]:
				# create new dictionary key
				tmp_list = list(key2)
				del tmp_list[pos2]
				# if both factors consist of just one variable, the key is just key1[0]
				if len(var1) > 1 or len(var2) > 1:
					new_key = tuple(key1 + tmp_list)
				else:
					new_key = key1[0]

				new_prob[new_key] = d1[all_keys1[i1]] * d2[all_keys2[i2]]


	# create new factor and return
	new_factor = (new_var, new_prob)
	return new_factor

def restrict(factor, variable, value):
	# get the variables of the factor
	var = list(factor[0])
	# find the position of the variable
	pos = [i for i,x in enumerate(factor[0]) if x == variable]
	pos = pos[0]

	# d is now the dictionary
	d = factor[1]
	# create new list of variables without the specific variable
	new_var = list(var)
	del new_var[pos]

	# create new dictionary
	new_prob = {}

	# for all entries in the factor
	for i in range(len(d.keys())):
		# get all keys
		all_keys = list(d.keys())
		# get key of position u1
		key = list(all_keys[i])
		# check if the bool fits to the value
		if key[pos] == value:
			# create the new key
			new_key = list(key)
			del new_key[pos]
			# again: distinguish according to the length of the variable list
			if len(new_key) > 1:
				new_key = tuple(new_key)
				new_prob[new_key] = d[all_keys[i]]
			else:
				new_prob[new_key[0]] = d[all_keys[i]]

	# create and return new factor
	new_factor = (new_var, new_prob)
	return new_factor


def inference(factorList, queryVariables, orderedListOfHiddenVariables, evidenceList):
	# restrict factors that contain evidence to this value
	for evidence in list(evidenceList.keys()):
		for i in range(len(factorList)):
			tmp_fac = factorList[i]
			if evidence in tmp_fac[0]:
				print("Due to restiction of the variable ", evidence, " the factor ", factorList[i])
				factorList[i] = restrict(tmp_fac, evidence, evidenceList[evidence])
				print("is changed to: ", factorList[i], "\n")

	# create additional factor list to store factors that contain the hidden variable
	hiddenFactorList = []
	# store original indices to delte them later
	hiddenFactorIndices = []

	# for every hidden variable
	for hiddenVar in orderedListOfHiddenVariables:
		for i in range(len(factorList)):
			# get the factor from the list
			tmp_fac = factorList[i]
			# check if hiddenVar in the variable list
			if hiddenVar in tmp_fac[0]:
				# append the factor and the index to the corresponding list
				hiddenFactorList.append(tmp_fac)
				hiddenFactorIndices.append(i)
				# if the factor just contains the hiddenVar, it is a 'basic factor'
				# need this factor to multiply it with the other factors later
				if len(tmp_fac[0])==1:
					basis_factor = tmp_fac;

		# check if the length > 1 and more factors are stored in the list
		if len(hiddenFactorList) > 1:
			for i in range(len(hiddenFactorList)):
				# if the current factor is not the basic factor
				if hiddenFactorList[i] != basis_factor:
					# multiply it with the basic factor
					new_factor1 = multiply(hiddenFactorList[i], basis_factor)
					#print(new_factor1, " NEW FACTOR after multiply")
					# sumout the hiddenVar
					new_factor2 = sumout(new_factor1, hiddenVar)
					print("Variable elimination of ", hiddenVar, " leads to new factor: ", new_factor2, "\n")
					# and append it to the factor list
					factorList.append(new_factor2)
		else:
			# just sumout the hiddenVar
			new_factor2 = sumout(hiddenFactorList[0], hiddenVar)
			factorList.append(new_factor2)

		
		# delete used factors of the original list
		deleted = 0
		#print(hiddenFactorIndices, ".. indeces....")
		for i in hiddenFactorIndices:
			# adapt index 
			ind = i - deleted
			print("Due to variable elimination the following factor is deleted from the list: ", factorList[ind], "\n")
			del factorList[ind]
			#print(hiddenVar, " hV ", ind, factorList)
			deleted += 1

		# initialize lists new again
		hiddenFactorList = []
		hiddenFactorIndices = []

	# now all factors should only depend on one variable
	# multiply them until just one factor is left
	while len(factorList) > 1:
		factorList[0] = multiply(factorList[0], factorList[1])
		del factorList[1]


	# get and print the result
	result = normalize(factorList[0])
	print("This is the resulting factor: ", result)

def normalize(factor):
	sumOfProb = 0
	factorKeys = list(factor[1].keys())
	# sum up all values
	for i in range(len(factor[1].keys())):
		sumOfProb += factor[1][factorKeys[i]]

	# normalize it
	new_prob = {}
	for i in range(len(factor[1].keys())):
		new_prob[factorKeys[i]] = factor[1][factorKeys[i]]/sumOfProb

	# return new factor
	new_factor = (factor[0], new_prob)
	return new_factor
