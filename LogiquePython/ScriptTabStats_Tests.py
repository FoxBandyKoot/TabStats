from numpy import *
import xlrd 
import sys
import os
import socket
socket
socket.socket

############################### DECLARATIONS ###############################

script = ''
fileXLSX = ''
selectedEmployees = ''

############################## DATA FOR TESTS ##############################

# DECOMMENT ONE FOR TESTS
#selectedEmployees = 'Fake1 Pierre Fake2 Lise Marie Fake3'
#selectedEmployees = 'Pierre Lise'
#selectedEmployees = 'Lise Pierre'
selectedEmployees = 'Chloé Mike' 

# DECOMMENT THIS FOR TESTS
selectedEmployees = selectedEmployees.split()

# DECOMMENT NEXT LINE FOR TESTS WITHOUT QT
FileXLSX = "C:/Users/Charly/CloudStation/Projets/Perso/Tab_Stat_Employes/Data/"

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
    

    #First main functionnality : Checks input, do calcul, and return result

    resultVerif = Tabstats(selectedEmployees, fileXLSX)
    
    if (resultVerif != "error"): 
        resultFile = open("C:/Users/" + os.getlogin() + "/Documents/Resultats.txt","w")
        resultFile.write(str(resultVerif)) # Need a string  
        resultFile.close()
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
    Then fill a table with data from the xlsx file.
    '''

    dir = fileXLSX
    
    filename = os.path.join(dir, "TabStats.xlsx") 
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
    tamp_list = list() # temporary list
    
    # Get the xlsx array (everything except the header)
    for x in range(lines)[1:]:
        for y in range(columns)[1:]:  # We first add the first line in a temporary array, then
            tamp_list.append(worksheet.cell(x,y).value)
        main_list.append(tamp_list)  # This line is added to the main table, then
        tamp_list = [] # We clear the temporary array to get the next line
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
    for i in range (len(selectedEmployees)): # For each employee chooses
        for j in range (len(employees)):         # We go through each column

            # If the employee exists: OK go to next
            if(selectedEmployees[i] in employees[j]):
                totalVerification += 1
                break

            if (j == len(employees)-1 and selectedEmployees[i] != employees[j]): # Pick up names that are not in the table
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

def Leplus():
    L=combinliste(employees,9)
    M=[]
    for i in range (len(L)):
        M+=[Tabstats(moisEnCours,L[i])]
    maxi=maximum(M)
    return(L[maxi])

# donne toutes les combinaisons de x employés désirées.
def combinliste(seq, k):
    p = []
    i, imax = 0, 2**len(seq)-1
    while i<=imax:
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
    
    
def maximum(selectedEmployees):
     maxi=selectedEmployees[0]
     indice=0
     for i in range (len(selectedEmployees)):
         if selectedEmployees[i]>maxi:
             maxi=selectedEmployees[i]
             indice=i
     return(indice)
     
# "1er calcul : quelle fonction excel, permet de calculer combien de fois les employés sélectionnés (ex : Eric, Sarah, David, inès, Flora, Jean, Lydie) 
# ont travaillé ensemble dans le mois. "																							
# 																							
# "2ème calcul : Quelle fonction excel ou quelle macro peut  permettre de savoir dans le tableau du mois concerné(voir sur 12 mois d'un tableau annuel)
# quelles sont les 9 personnes qui ont travaillé le plus souvent ensemble "																							

def error(resultVerif):
    resultFile = open("C:/Users/" + os.getlogin() + "/Documents/Resultats.txt", "w")
    resultFile.write(resultVerif)
    resultFile.close()

__main__(selectedEmployees, fileXLSX)