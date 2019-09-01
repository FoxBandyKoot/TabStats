from threading import Thread
from numpy import *

import sys

class F1():

    


    #def Tabstats_F1(self, selectedEmployees, pathXLSX):
    def Tabstats_F1(self, selectedEmployees):
        '''
        First main functionnality : Checks input, do calcul, and return result
        '''

                # COMMENT THESE NEXTS 3 LINES FOR TESTS WITHOUT GUI
        # GET ARGUMENTS
        '''
        selectedEmployees = sys.argv[1]
        selectedEmployees = selectedEmployees.split()
        pathXLSX = sys.argv[2]
        '''
        # DECOMMENT THIS FOR TESTS
        selectedEmployees = selectedEmployees.split()

        nbEmployeesSelected = len(selectedEmployees)
        resultVerif = self.verifNameEmployees(self, self.selectedEmployees, employees, nbEmployeesSelected)
        
        # If there is an error in a name, stop the program and indicate which name is wrong
        if (resultVerif != "Tous les noms sont présents. Nombre de fois où ils ont travaillé ensemble : "):
            self.error_input(resultVerif)
            return ("error")
            
        # Replaces names with numeric values
        selectedFigures = self.replaceNamesByNumbers(selectedEmployees, employees)
        
        # Sorting in ascending order employees
        selectedFiguresSorted = self.orderList(selectedFigures)

        #Count how many time employees selected gave worked together
        resultVerif += self.how_much_worked_together(self.full_table, nbEmployeesSelected, selectedFiguresSorted) 

        if (resultVerif != "error"): 
            self.write_result()

    def init(self, selectedEmployees_i):
        '''
        Constructor for threads
        '''

        self.selectedEmployees = selectedEmployees_i
        
        #First main functionnality : Checks input, do calcul, and return result
        #Tabstats_F1(selectedEmployees, pathXLSX)
        self.Tabstats_F1(self.selectedEmployees)

    def verifNameEmployees(self, selectedEmployees, employees, nbEmployeesSelected):
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


    def replaceNamesByNumbers(self, selectedEmployees, employees):
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
        

    def orderList(self, selectedEmployees):
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


    def how_much_worked_together(self, full_table, nbEmployeesSelected, selectedFiguresSorted):
        '''
        Count how many time employees selected gave worked together
        '''
        total = 0
        for j in range (self.array_part):
            counter = 0
            for i in range (nbEmployeesSelected):
                if self.full_table[j][selectedFiguresSorted[i]] != "":
                    counter += 1
            if counter == nbEmployeesSelected:
                total += 1

        total = str(total)
        return(total)

    
    def write_result():
        resultFile = open("C:/Users/" + os.getlogin() + "/Documents/Resultats.txt","w")
        resultFile.write(str(resultVerif)) # Need a string  
        resultFile.close()
    
    
    def error_input(self, resultVerif):
        '''
        Create a txt file and write the errors in it
        '''
        resultFile = open("C:/Users/" + os.getlogin() + "/Documents/Resultats.txt", "w")
        resultFile.write(resultVerif)
        resultFile.close()