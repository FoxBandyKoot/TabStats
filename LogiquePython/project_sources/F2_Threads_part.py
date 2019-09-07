from threading import Thread

class F2_Threads_part(Thread):

    def __init__(self, half_tab_i, lines_to_read_i, employees_i, full_table_i, object_per_group_i, combin_list_i):
        '''
        Constructor for threads
        '''
        Thread.__init__(self)
        # Boundaries for threads
        if half_tab_i == "first_half_tab":
            self.iterator_line = 0
        elif half_tab_i == "second_half_tab":
            self.iterator_line = int(lines_to_read_i / 2)

        self.lines_to_read = int(lines_to_read_i)

        self.employees = employees_i        # Header employees
        self.full_table = full_table_i      # All data
        self.object_per_group = object_per_group_i

        # All groups
        self.combin_list = combin_list_i
        self.value_each_group = list()

        #self.main()        

    def run(self):
        '''
        Get max for each group for one half of the tab per thread
        '''
        # REPLACE BY list() IF IT IS MORE FAST OR TO HAVE SAME CODE EVERYWHERE
        result = list()
        len_combin_list = len(self.combin_list)
        for i in range (len_combin_list):
            self.value_each_group.append(self.Tabstats_F2(result, self.combin_list[i]))
    
    def Tabstats_F2(self, result, selectedGroup):
        '''
        arg2 : group of the combin list
        Second functionnality : Checks input, do calcul, and return result
        '''            
        # Replaces names with numeric values
        #print(selectedGroup)
        selectedFigures = self.replaceNamesByNumbers(selectedGroup)
        # Sorting in ascending order employees, USELESS HERE IN THINK
        selectedFiguresSorted = self.orderList(selectedFigures)
        
        #Count how many time employees selected gave worked together
        result = self.how_much_worked_together(selectedFiguresSorted)
        #result = self.how_much_worked_together(selectedFigures)
        return(result)


    def replaceNamesByNumbers(self, selectedGroup):
        '''
        Replaces names with their index
        ARG1: User input, ARG2: Table header
        '''
        L = []                
        for i in range (len(selectedGroup)):
            for j in range (len(self.employees)):
                if selectedGroup[i] == self.employees[j]:
                    L += [j]
        return(L)


    def orderList(self, selectedGroup):
        # USELESS FUNCTION I THINK 
        #       print("orderList")
        #       print(selectedGroup)
        # AND PRINT JUST AFTER LINE "selectedFigures = self.replaceNamesByNumbers(selectedGroup, self.employees)"
        #       print("selectedFigures")
        #       print(selectedFigures)

        '''
        Sorting employees in ascending order
        ARG1: User input
        '''
        L=[]
        while selectedGroup!=[]:
            minim=selectedGroup[0]
            indice=0
            for i in range(len(selectedGroup)):
                if selectedGroup[i] < minim:
                    minim = selectedGroup[i]
                    indice = i
            L+=[selectedGroup[indice]]
            selectedGroup = selectedGroup[0:indice] + selectedGroup[indice + 1:len(selectedGroup)]
        return(L)


    def how_much_worked_together(self, selectedFiguresSorted):
        '''
        Count how many time employees selected gave worked together. Depends on threads 
        '''
        '''
        print(selectedFiguresSorted)
        '''
        total = 0
        for i in range (self.lines_to_read)[self.iterator_line:]:
            counter = 0
            for j in range (self.object_per_group):
                if self.full_table[i] [selectedFiguresSorted[j]] != "":
                    counter += 1
            if counter == self.object_per_group:
                total += 1

        total = str(total)
        return(total)

if __name__ == "__main__" and __package__ is None:
    __package__ = "F2_Threads_part"