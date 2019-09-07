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
    nb_columns = 0
    nb_lines = 0
    index_best_group = 0

    F1_run = True
    F2_run = False
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
        f1 = F1()
        f1.init(self.selectedEmployees, self.employees, self.nb_lines, self.full_table)


    def F2_go(self):
        # Boundaries for each threads
        '''
        print("nb_lines")
        print(self.nb_lines)
        print("nb_lines rest")
        print(self.nb_lines % 2)
        '''
        if self.nb_lines % 2 == 0:
            first_half_lines = self.nb_lines / 2
            second_half_lines = self.nb_lines
        else:
            print("FUCK IT")
            
        # Create threads
        th_first_half_tab = F2("first_half_tab", first_half_lines, self.employees, self.full_table)
        th_second_half_tab = F2("second_half_tab", second_half_lines, self.employees, self.full_table)

        # Run threads
        th_first_half_tab.start()
        th_second_half_tab.start()

        # Wait threads to finish
        th_first_half_tab.join()
        th_second_half_tab.join()

        # Convert list to int
        th_first_half_tab.value_each_group = list(map(int, th_first_half_tab.value_each_group))
        th_second_half_tab.value_each_group = list(map(int, th_second_half_tab.value_each_group))
        
        print(th_first_half_tab.value_each_group)
        print(th_second_half_tab.value_each_group)
        
        # Merge the 2 threads
        value_each_group = [x + y for x, y in zip(th_first_half_tab.value_each_group, th_second_half_tab.value_each_group)]
        
        print(value_each_group)
        
        # Get index of the best group
        self.index_best_group, maxi = self.maximum(self, value_each_group)
        '''
        print(th_first_half_tab.combin_list)
        '''
        if th_first_half_tab.combin_list:
            self.best_group = th_first_half_tab.combin_list[self.index_best_group]
            print("best_group")
            print(self.best_group)

    
    def maximum(self, value_each_group):
        '''
        Return the index of the group of employees which worked the most together
        '''
        maxi = max(value_each_group)
        print("maxi")
        print(maxi)
        # Get index of best group
        index_best_group = value_each_group.index(maxi)
        print("index_best_group")
        print(index_best_group)

        return(index_best_group, maxi)

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