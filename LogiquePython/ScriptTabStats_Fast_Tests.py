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
    employees = list()
    maxi = 0
    nb_columns = 0
    nb_lines = 0

    F1_run = True
    F2_run = False
    #Decomment for tests without GUI
    pathXLSX = "C:/Users/Charly/CloudStation/Projets/Perso/TabStats/Data/"
    ############################## END DECLARATIONS #############################

    ############################## DATA FOR TESTS ##############################

    # DECOMMENT ONE FOR TESTS
    selectedEmployees = 'Fake1 Pierre Fake2 Lise Marie Fake3' #6'
    #selectedEmployees = 'Pierre Lise' # 10 times together
    #selectedEmployees = 'Lise Pierre' # 10 times together
    #selectedEmployees = 'Chloé Mike' 
    #selectedEmployees = 'David Inès' # 15 times together
    ############################ END DATA FOR TESTS ############################


    def start_program(self):
        worksheet = self.excelFileSelection(self)

        self.full_table, self.employees = self.get_header_employees(self, worksheet)
        [self.nb_lines, self.nb_columns] = shape(self.full_table)

        if self.F1_run:
            self.F1_go(self)
        elif self.F2_run:
            self.F2_go(self)


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
        
        indexHeaderTab = 0
        for y in range(columns)[1:]:            
            self.employees.append(worksheet.cell(indexHeaderTab,y).value) 
        
        main_list = list() # main list
        temp_list = list() # temporary list
        
        # Get the xlsx array (everything except the header)
        for x in range(lines)[1:]:
            for y in range(columns)[1:]:  # We first add the first line in a temporary array, then
                temp_list.append(worksheet.cell(x,y).value)
            main_list.append(temp_list)  # This line is added to the main table, then
            temp_list = [] # We clear the temporary array to get the next line
        return(main_list, self.employees)    

    def F1_go(self):
        #F1.Tabstats_F1(self, self.selectedEmployees)
        F1.init(self, self.selectedEmployees)

    def F2_go(self):
        # Boundaries for each threads
        first_half_tab = ceil(self.nb_lines / 2)
        second_half_tab = floor(self.nb_lines / 2) 

        # Create threads
        t_first_half_tab = F2(first_half_tab, self.employees, self.full_table)
        t_second_half_tab = F2(second_half_tab, eself.mployees, self.full_table)

        # Run threads
        t_first_half_tab.start()
        t_second_half_tab.start()

        # Wait threads to finish
        t_first_half_tab.join()
        t_second_half_tab.join()

        print("index T1")
        print(t_first_half_tab.index_best_group)
        print("index T2")
        print(t_second_half_tab.index_best_group)

        self.maxi = t_first_half_tab.maxi + t_second_half_tab.maxi
        print("maxi")
        print(self.maxi)

        if t_first_half_tab.combin_list:
            self.best_group = t_first_half_tab.combin_list[t_first_half_tab.index_best_group]
            print("best_group")
            print(self.best_group)

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
    __main__()