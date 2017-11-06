factor0 = (['A'], {True: 0.7, False: 0.3})
factor1 = (['A', 'B'], {(False, False): 0.6, (False, True): 0.4, (True, True): 0.9, (True, False): 0.1})
factor2 = (['B', 'C'], {(False, False): 0.2, (False, True): 0.8, (True, True): 0.7, (True, False): 0.3})
def sumout(factor, variable):
	pos = [i for i,x in enumerate(factor[0]) if x == variable]
	pos = pos[0]
	var = list(factor[0])
	var.remove(variable)
	d = factor[1]
	new_prob = {}
	#for all keys in factor
	for i1 in range(len(d.keys())):
		# get all keys
		u = list(d.keys())
		# get key of position u1
		u_del = list(u[i1])
	  	# del binary of variable
		del u_del[pos]
		#for all keys after i1
		for i2 in range(i1+1, len(d.keys())):
			v = list(d.keys())
			v_del = list(v[i2])
			del v_del[pos]
			# if new keys are the same
			if len(u_del) > 1:
				if u_del == v_del:
			    	# add values to dict
					new_prob[tuple(u_del)] = d[u[i1]] + d[v[i2]]
			else:
				if u_del == v_del:
			    	# add values to dict
					new_prob[u_del[0]] = d[u[i1]] + d[v[i2]]

	new_factor = (var, new_prob)
	return new_factor

def multiply(factor1, factor2):
	# possible that more than one common variable????
	var1 = list(factor1[0])
	var2 = list(factor2[0])
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

	d1 = factor1[1]
	d2 = factor2[1]

	new_prob = {}
	tmp_var = list(var2)
	del tmp_var[pos2]
	new_var = var1 + tmp_var

	for i1 in range(len(d1.keys())):
		all_keys1 = list(d1.keys())
		# get key of position u1
		list1 = list(all_keys2[i1])
		if len([all_keys1[i1]]) > 1:
			key1 = list(all_keys1[i1])

		else:
			key1 = list([all_keys1[i1]])
		print(key1, "key1")
		for i2 in range(len(d2.keys())):
			all_keys2 = list(d2.keys())
			if len([all_keys2[i2]]) > 1:
				key2 = list(all_keys2[i2])
			else:
				key2 = list([all_keys2[i2]])
			if key1[pos1] == key2[pos2]:
				tmp_list = list(key2)
				del tmp_list[pos2]
				new_key = tuple(key1 + tmp_list)
				new_prob[new_key] = d1[all_keys1[i1]] * d2[all_keys2[i2]]



	new_factor = (new_var, new_prob)
	return new_factor

def restrict(factor, variable, value):
	var = list(factor[0])
	pos = [i for i,x in enumerate(factor[0]) if x == variable]
	pos = pos[0]

	d = factor[1]
	new_var = list(var)
	del new_var[pos]

	new_prob = {}

	for i in range(len(d.keys())):
		all_keys = list(d.keys())
		# get key of position u1
		key = list(all_keys[i])
		if key[pos] == value:
			new_key = list(key)
			del new_key[pos]
			if len(new_key) > 1:
				new_key = tuple(new_key)
				new_prob[new_key] = d[all_keys[i]]
			else:
				new_prob[new_key[0]] = d[all_keys[i]]

	new_factor = (new_var, new_prob)
	return new_factor

factorList=[factor0, factor1, factor2]
orderedListOfHiddenVariables = ['B']
queryVariables = ['A']
evidenceList = {'C':True}
def inference(factorList, queryVariables, orderedListOfHiddenVariables, evidenceList):
	# restrict factors that contain evidence to this value
	for evidence in list(evidenceList.keys()):
		for i in range(len(factorList)):
			tmp_fac = factorList[i]
			if evidence in tmp_fac[0]:
				factorList[i] = restrict(tmp_fac, evidence, evidenceList[evidence])

	print(factorList)

	# sumout hidden variables according to the order of the list
	hiddenFactorList = []
	hiddenFactorIndices = []
	# find factors that 
	#for hiddenVar in orderedListOfHiddenVariables:
	hiddenVar = 'B'
	for i in range(len(factorList)):
		tmp_fac = factorList[i]
		if hiddenVar in tmp_fac[0]:
			hiddenFactorList.append(tmp_fac)
			hiddenFactorIndices.append(i)

	print(hiddenFactorList)

	# multiply the factors of hiddenFactorList
	while len(hiddenFactorList) > 1:
		# generate new factor
		new_factor = multiply(hiddenFactorList[0], hiddenFactorList[1])
		# put it on the first position of the list
		hiddenFactorList[0] = new_factor
		# remove the other part of the project
		del hiddenFactorList[1]

	print(hiddenFactorList)

	# delete used factors
	deleted = 0
	for i in hiddenFactorIndices:
		ind = i - deleted
		del factorList[ind]
		deleted += 1


	# sumout the hidden variable
	remainingFactor = hiddenFactorList[0]
	new_factor = sumout(remainingFactor, hiddenVar)

	# add new factor to factor list
	factorList.append(new_factor)

	while len(factorList) > 1:
		factorList[0] = multiply(factorList[0], factorList[1])
		del factorList[1]

	print(factorList)




inference(factorList, queryVariables, orderedListOfHiddenVariables, evidenceList)
#f = sumout(factor1, 'E')
#print(f)
