from threading import Thread
from numpy import *

import os
import sys

class F1():
    def init(self, selectedEmployees_i, employees_i, nb_lines_i, full_table_i):
        '''
        Constructor for threads
        '''        
        # To analyse each group
        self.selectedEmployees = selectedEmployees_i.split()
        self.nbEmployeesSelected = len(self.selectedEmployees)

        self.employees = employees_i

        self.nb_lines = nb_lines_i
        
        self.full_table = full_table_i
        #First main functionnality : Checks input, do calcul, and return result
        self.Tabstats_F1()


    #def Tabstats_F1(self, selectedEmployees, pathXLSX):
    def Tabstats_F1(self):
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

        result_verif = self.verifNameEmployees()
        
        # If there is an error in a name, stop the program and indicate which name is wrong
        if (result_verif != "Tous les noms sont présents. Nombre de fois où ils ont travaillé ensemble : "):
            self.error_input(result_verif)
            return ("error")
            
        # Replaces names with numeric values
        selectedFigures = self.replaceNamesByNumbers()
        
        # Sorting in ascending order employees
        selectedFiguresSorted = self.orderList(selectedFigures)

        #Count how many time employees selected gave worked together
        result_verif += self.how_much_worked_together(selectedFiguresSorted) 

        if (result_verif != "error"): 
            self.write_result(result_verif)

    
    def verifNameEmployees(self):
        '''
        Check if selected employees exist
        ARG1: User input, ARG2: Table header, ARG3: number user input
        '''
        totalVerification = 0
        missingNames = " "
        result = " "
        stateVerification = True
        nbEmployees = len(self.employees)

        for i in range (self.nbEmployeesSelected): # For each employee chooses
            for j in range (nbEmployees):         # We go through each column

                # If the employee exists: OK go to next
                if(self.selectedEmployees[i] in self.employees[j]):
                    totalVerification += 1
                    break

                if (j == nbEmployees-1 and self.selectedEmployees[i] != self.employees[j]): # Pick up names that are not in the table
                        totalVerification += 1
                        missingNames += self.selectedEmployees[i] + " "
                        stateVerification = False
                        break
            
            if (totalVerification == self.nbEmployeesSelected and stateVerification == True): # If All employees exist: OK we go out
                result = "Tous les noms sont présents. Nombre de fois où ils ont travaillé ensemble : "
                stateVerification = True 
                break
                
            if (totalVerification == self.nbEmployeesSelected and stateVerification == False): # Returns the list of names not present
                result = "Les noms suivants ne sont pas présents : " + missingNames
            
        return(result)


    def replaceNamesByNumbers(self):
        '''
        Replaces names with their index
        ARG1: User input, ARG2: Table header
        '''
        L=[]                
        for i in range (len(self.selectedEmployees)):
            for j in range (len(self.employees)):
                if self.selectedEmployees[i]==self.employees[j]:
                    L+=[j]
        return(L)
        

    def orderList(self, selectedFigures):
        '''
        Sorting employees in ascending order
        ARG1: User input
        '''
        L=[]
        while selectedFigures != []:
            minim = selectedFigures[0]
            indice = 0
            for i in range(len(selectedFigures)):
                if selectedFigures[i] < minim:
                    minim = selectedFigures[i]
                    indice = i
            L+=[selectedFigures[indice]]
            selectedFigures = selectedFigures[0:indice] + selectedFigures[indice+1:len(selectedFigures)]
        return(L)


    def how_much_worked_together(self, selectedFiguresSorted):
        '''
        Count how many time employees selected gave worked together
        '''
        total = 0
        for j in range (self.nb_lines):
            counter = 0
            for i in range (self.nbEmployeesSelected):
                if self.full_table[j][selectedFiguresSorted[i]] != "":
                    counter += 1
            if counter == self.nbEmployeesSelected:
                total += 1

        total = str(total)
        return(total)

    
    def write_result(self, result_verif):
        '''
        Create a txt file and write the results in it
        '''
        print(result_verif)
        resultFile = open("C:/Users/" + os.getlogin() + "/Documents/Resultats.txt","w")
        resultFile.write(result_verif) # Need a string  
        resultFile.close()
    
    
    def error_input(self, result_verif):
        '''
        Create a txt file and write the errors in it
        '''
        resultFile = open("C:/Users/" + os.getlogin() + "/Documents/Resultats.txt", "w")
        resultFile.write(result_verif)
        resultFile.close()