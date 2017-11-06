from variable_elimination import *

factor1 = (['FS'], {True: 0.05, False: 0.95})
factor2 = (['FM'], {True: float(1/28), False: float(27/28)})
factor3 = (['NA'], {True: 0.3, False: 0.7})
factor4 = (['FS', 'FB'], {(False, False): 0.9, (False, True): 0.1, (True, True): 0.6, (True, False): 0.4})
factor5 = (['NA', 'FM', 'NDG'], {(False, False, False): 1, (False, False, True): 0, (False, True, True): 0.4, (False, True, False): 0.6, (True, False, True): 0.5, (True, False, False): 0.5, (True, True, True): 0.8, (True, True, False): 0.2})
factor6 = (['FS', 'FM', 'NDG', 'FH'], {(True, True, True, True): 0.99, (True, True, True, False): 0.01, (False, False, False, True): 0, (False, False, False, False): 1, (True, False, False, True): 0.5, (True, False, False, False): 0.5, (True, False, True, True): 0.75, (True, False, True, False): 0.25, (True, True, False, True): 0.9, (True, True, False, False): 0.1, (False, True,  True, True): 0.65, (False, True, True, False): 0.35, (False, True, False, True): 0.4, (False, True, False, False): 0.6, (False, False, True, True): 0.2, (False, False, True, False): 0.8})


# 3 b)
factorList=[factor1, factor2, factor3, factor5, factor6]
orderedListOfHiddenVariables = ['NA', 'FM', 'NDG', 'FS']
queryVariables = ['FH']
#evidenceList = {'D':True}
evidenceList = { }
#inference(factorList, queryVariables, orderedListOfHiddenVariables, evidenceList)

# 3 c)
factorList = [factor1, factor6]
orderedListOfHiddenVariables = ['NDG']
queryVariables = ['FS']
evidenceList = {'FM': True, 'FH': True}
#inference(factorList, queryVariables, orderedListOfHiddenVariables, evidenceList)
#f = sumout(factor1, 'E')
#print(f)

# 3 d)
factorList = [factor1, factor4, factor6]
orderedListOfHiddenVariables = ['NDG']
queryVariables = ['FS']
evidenceList = {'FM': True, 'FH': True, 'FB': True}
#inference(factorList, queryVariables, orderedListOfHiddenVariables, evidenceList)

# 3 e)
factorList = [factor1, factor4, factor5, factor6]
orderedListOfHiddenVariables = ['NDG']
queryVariables = ['FS']
evidenceList = {'FM': True, 'FH': True, 'FB': True, 'NA': True}
inference(factorList, queryVariables, orderedListOfHiddenVariables, evidenceList)
