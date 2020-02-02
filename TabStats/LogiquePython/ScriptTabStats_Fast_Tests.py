from  timeit import timeit

from project_sources.F2 import F2
from project_sources.F1 import F1

from numpy import *

import xlrd 
import os

class TabStats():

    ################################ DECLARATIONS ###############################
    script = ''
    pathXLSX = ''
    full_table = list()    
    '''
    TO CHANGE
    ''' 
    object_per_group = 2           # Object per combin

    F1_run = False
    F2_run = True
    #Decomment for tests without GUI
    pathXLSX = "C:/Users/Charly/CloudStation/Projets/Perso/TabStats/Data/"
    ############################## END DECLARATIONS #############################

    ############################## DATA FOR TESTS ##############################

    # DECOMMENT ONE FOR TESTS
    selectedEmployees = 'Fake1 Pierre Fake2 Lise Marie Fake3'
    #selectedEmployees = 'Pierre Lise' # 10 times together
    #selectedEmployees = 'Lise Pierre' # 10 times together
    #selectedEmployees = 'Chloé Mike' 
    #selectedEmployees = 'Paul Sarah' # 30 times together
    #selectedEmployees = 'David Inès' # 15 times together
    ############################ END DATA FOR TESTS ############################


    def start_program(self):
        '''
        Run the button that user clickeds
        '''
        # Get the worksheet
        worksheet = self.excelFileSelection(self)

        self.full_table, employees = self.get_header_employees(self, worksheet)
        [nb_lines, nb_columns] = shape(self.full_table)

        if self.F1_run:
            self.F1_go(self, employees, nb_lines)

        elif self.F2_run:
            self.F2_go(self, employees, nb_lines)


    def excelFileSelection(self):
        '''
        Select the xlsx file then the sheet and return it. 
        '''
        dir = self.pathXLSX
        fileXLSX = "TabStats_Short_10C.xlsx"
        filename = os.path.join(dir, fileXLSX) 
        workbook = xlrd.open_workbook(filename)
        worksheet = workbook.sheet_by_name("Feuil1")
        return worksheet

        
    def get_header_employees(self, worksheet):
        '''
        # Populate the list with all the employee names in the xlsx file header

        Return : main_list => Table fill with data from the xlsx fil
        employees => Header xlsx file
        '''
        lines = worksheet.nrows
        columns = worksheet.ncols
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


    def F1_go(self, employees, nb_lines):
        f1 = F1()
        f1.init(self.selectedEmployees, employees, nb_lines, self.full_table)


    def F2_go(self, employees, nb_lines):
        
        f2 = F2(employees, nb_lines, self.full_table, self.object_per_group)
        f2.main()
    

'''
END CLASS
'''

def __main__():
    tabStats = TabStats
    tabStats.start_program(tabStats)

if __name__ == '__main__':

    # DECOMMENT THESE NEXT 3 LINES FOR TESTS WITH OR WITHOUT QT 
    '''
    TestFile = open("C:/Users/" + os.getlogin() + "/Documents/TESTS.txt", "w")
    TestFile.write(str(selectedEmployees))
    TestFile.close()
    '''

    print(timeit("__main__()", "from __main__ import __main__", number = 10))
    print("TIMING")

    #__main__()