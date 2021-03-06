from numpy import *
import xlrd 
import sys
import os
import socket
import timeit

############################### DECLARATIONS ###############################

script = ''
fileXLSX = ''
selectedEmployees = ''

############################## DATA FOR TESTS ##############################

# DECOMMENT ONE FOR TESTS
#selectedEmployees = 'Fake1 Pierre Fake2 Lise Marie Fake3' #6'
#selectedEmployees = 'Pierre Lise' # 10 times together
#selectedEmployees = 'Lise Pierre' # 10 times together
#selectedEmployees = 'Chloé Mike' 
selectedEmployees = 'David Inès' # 15 times together

# DECOMMENT THIS FOR TESTS
selectedEmployees = selectedEmployees.split()

# DECOMMENT NEXT LINE FOR TESTS WITHOUT QT
fileXLSX = "C:/Users/Charly/CloudStation/Projets/Perso/TabStats/Data/"

############################ END DATA FOR TESTS ############################

def __main__(selectedEmployees, fileXLSX):
    
    # COMMENT THESE NEXTS 3 LINES FOR TESTS WITHOUT QT
    # GET ARGUMENTS
    '''
    selectedEmployees = sys.argv[1]
    selectedEmployees = selectedEmployees.split()
    fileXLSX = sys.argv[2]
    '''
    # DECOMMENT THESE NEXT 3 LINES FOR TESTS WITH OR WITHOUT QT 
    '''
    TestFile = open("C:/Users/" + os.getlogin() + "/Documents/TESTS.txt", "w")
    TestFile.write(str(selectedEmployees))
    TestFile.close()
    '''

    '''

    MAKE A FILE FOR EACH FUNCTIONALITY

    '''

    '''
    #First main functionnality : Checks input, do calcul, and return result
    resultVerif = Tabstats(selectedEmployees, fileXLSX)
    
    if (resultVerif != "error"): 
        resultFile = open("C:/Users/" + os.getlogin() + "/Documents/Resultats.txt","w")
        resultFile.write(str(resultVerif)) # Need a string  
        resultFile.close()
    return
    '''
    
    #Secund functionnality : 
    fullTable, employees = excelFileSelection(fileXLSX)
    result = TS_9_employes_who_worked_the_most_together(selectedEmployees, employees)
    return



def Tabstats(selectedEmployees, fileXLSX):
    '''
    First main functionnality : Checks input, do calcul, and return result
    '''

    fullTable, employees = excelFileSelection(fileXLSX)
    nbEmployeesSelected = len(selectedEmployees)
    resultVerif = verifNameEmployees(selectedEmployees, employees, nbEmployeesSelected)
    
    # If there is an error in a name, stop the program and indicate which name is wrong
    if (resultVerif != "Tous les noms sont présents. Nombre de fois où ils ont travaillé ensemble : "):
        error(resultVerif)
        return ("error")
        
    # Replaces names with numeric values
    selectedFigures=replaceNamesByNumbers(selectedEmployees, employees)
    
    # Sorting in ascending order employees
    selectedFiguresSorted=orderList(selectedFigures)

    #Count how many time employees selected gave worked together
    resultVerif += howManyTimesSelectedWorkedTogether(fullTable, nbEmployeesSelected, selectedFiguresSorted) 

    return(resultVerif)


def excelFileSelection(fileXLSX):
    '''
    Select the xlsx file then the sheet and open it. 

    Return : main_list => Table fill with data from the xlsx fil
             employees => Header xlsx file
    '''

    dir = fileXLSX
    
    filename = os.path.join(dir, "TabStats_Short.xlsx") 
    workbook = xlrd.open_workbook(filename)
    
    worksheet = workbook.sheet_by_name("Feuil1")

    lines = worksheet.nrows
    columns = worksheet.ncols
    
    # Populate the list with all the employee names in the xlsx file header
    employees = list()
    indexHeaderTab = 0
    for y in range(columns)[1:]:            
        employees.append(worksheet.cell(indexHeaderTab,y).value) 
    
    main_list = list() # main list
    temp_list = list() # temporary list
    
    # Get the xlsx array (everything except the header)
    for x in range(lines)[1:]:
        for y in range(columns)[1:]:  # We first add the first line in a temporary array, then
            temp_list.append(worksheet.cell(x,y).value)
        main_list.append(temp_list)  # This line is added to the main table, then
        temp_list = [] # We clear the temporary array to get the next line
    return(main_list, employees)


def verifNameEmployees(selectedEmployees, employees, nbEmployeesSelected):
    '''
    Check if selected employees exist
    ARG1: User input, ARG2: Table header, ARG3: number user input
    '''
    totalVerification = 0
    missingNames = " "
    result = " "
    stateVerification = True
    nbEmployees = len(employees)

    for i in range (nbEmployeesSelected): # For each employee chooses
        for j in range (nbEmployees):         # We go through each column

            # If the employee exists: OK go to next
            if(selectedEmployees[i] in employees[j]):
                totalVerification += 1
                break

            if (j == nbEmployees-1 and selectedEmployees[i] != employees[j]): # Pick up names that are not in the table
                    totalVerification += 1
                    missingNames += selectedEmployees[i] + " "
                    stateVerification = False
                    break
        
        if (totalVerification == nbEmployeesSelected and stateVerification == True): # If All employees exist: OK we go out
            result = "Tous les noms sont présents. Nombre de fois où ils ont travaillé ensemble : "
            stateVerification = True 
            break
            
        if (totalVerification == nbEmployeesSelected and stateVerification == False): # Returns the list of names not present
            result = "Les noms suivants ne sont pas présents : " + missingNames
        
    return(result)


def replaceNamesByNumbers(selectedEmployees, employees):
    '''
    Replaces names with their index
    ARG1: User input, ARG2: Table header
    '''
    L=[]                
    for i in range (len(selectedEmployees)):
        for j in range (len(employees)):
            if selectedEmployees[i]==employees[j]:
                L+=[j]
    return(L)
    
 # Check for library
def orderList(selectedEmployees):
    '''
    Sorting employees in ascending order
    ARG1: User input
    '''
    L=[]
    while selectedEmployees!=[]:
        minim=selectedEmployees[0]
        indice=0
        for i in range(len(selectedEmployees)):
            if selectedEmployees[i] < minim:
                minim = selectedEmployees[i]
                indice = i
        L+=[selectedEmployees[indice]]
        selectedEmployees = selectedEmployees[0:indice] + selectedEmployees[indice+1:len(selectedEmployees)]
    return(L)
   
def howManyTimesSelectedWorkedTogether(fullTable, nbEmployeesSelected, selectedFiguresSorted):
    '''
    Count how many time employees selected gave worked together
    '''

    [numberOfLines,columns]=shape(fullTable)

    total=0
    for j in range (numberOfLines):
        counter=0
        for i in range (nbEmployeesSelected):
            if fullTable[j][selectedFiguresSorted[i]] != "":
                counter+=1
        if counter == nbEmployeesSelected:
            total+=1

    total = str(total)
    return(total)




#q2



def TS_9_employes_who_worked_the_most_together(selectedEmployees, employees):
    '''
    MAIN F2
    '''
    nbEmployeesSelected = len(selectedEmployees)
    return The_Most(employees)

def The_Most(employees):
    '''

    '''
    
    # Get all combinations of X desired employees
    combin_list = get_combin_list(employees,2)
    len_combin_list = len(combin_list)
    
    print("combin_list")
    print(combin_list)

    print("len_combin_list")
    print(len_combin_list)
    
    # REPLACE BY list() IF IT IS MORE FAST OR TO HAVE SAME CODE EVERYWHERE
    how_much_work_together_each_combin = []
    resultVerif = list()

    for i in range (len_combin_list):
        # OLD
        #M += [Tabstats(moisEnCours, combin_list[i])]
        
        # NEW
        how_much_work_together_each_combin.append(Tabstats_F2(resultVerif, combin_list[i], fileXLSX))

    #Tabstats(selectedEmployees, fileXLSX)
    index, maxi = maximum(how_much_work_together_each_combin)
    best_group = combin_list[index]
    
    print("best_group")
    print(best_group)

    print("maxi")
    print(maxi)
    return(best_group)


def get_combin_list(seq, k):
    '''
    THIS FUNCTION IS OK
    Give all combinations of X desired employees
    '''

    # REPLACE BY list() IF IT IS MORE FAST OR TO HAVE SAME CODE EVERYWHERE
    p = []
    i, imax = 0, 2**len(seq)-1
    while i<=imax:
        #print(i)
        s = []
        j, jmax = 0, len(seq)-1
        while j<=jmax:
            if (i>>j)&1==1:
                s.append(seq[j])
            j += 1
        if len(s)==k:
            p.append(s)
        i += 1 
    return p
    

def Tabstats_F2(resultVerif, selectedEmployees, fileXLSX):
    '''
    First main functionnality : Checks input, do calcul, and return result
    '''

    fullTable, employees = excelFileSelection(fileXLSX)
    nbEmployeesSelected = len(selectedEmployees)
        
    # Replaces names with numeric values
    selectedFigures=replaceNamesByNumbers(selectedEmployees, employees)
    
    # Sorting in ascending order employees
    selectedFiguresSorted=orderList(selectedFigures)

    #Count how many time employees selected gave worked together
    resultVerif = howManyTimesSelectedWorkedTogether(fullTable, nbEmployeesSelected, selectedFiguresSorted)
    return(resultVerif)


def maximum(how_much_work_together_each_combin):
    '''
    Return :
        Index of the group of employees which worked the most together
        Number of days
    '''
    how_much_work_together_each_combin_int = map(int, how_much_work_together_each_combin) 
    how_much_work_together_each_combin_int = sorted(how_much_work_together_each_combin_int) 

    maxi = max(how_much_work_together_each_combin_int)

    index_group = how_much_work_together_each_combin.index(str(maxi))
    '''
    maxi = how_much_work_together_each_combin[0]
    index_group = 0
    nb_how_much_work_together_each_combin = len(how_much_work_together_each_combin)

    for i in range(nb_how_much_work_together_each_combin):
        print(how_much_work_together_each_combin[i])
        if how_much_work_together_each_combin[i]>maxi:
            maxi = how_much_work_together_each_combin[i]
            index_group = i
            break
    '''
    return(index_group, maxi)


def error(resultVerif):
    '''
    Create a txt file and write the errors in it
    '''
    resultFile = open("C:/Users/" + os.getlogin() + "/Documents/Resultats.txt", "w")
    resultFile.write(resultVerif)
    resultFile.close()



print(timeit.timeit("__main__(selectedEmployees, fileXLSX)", "from __main__ import __main__, selectedEmployees, fileXLSX", number=10))
print("TIMING")