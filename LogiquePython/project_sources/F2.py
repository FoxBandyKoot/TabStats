from threading import Thread

class F2(Thread):

    #dt_name for Dictionnary

    def __init__(self, half_tab_i, lines_to_read_i, employees_i, full_table_i, object_per_group_i):
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
        self.combin_list = list()
        self.value_each_group = list()

        self.main()         # get max for each group for one half of the tab per thread

    def main(self):
        '''
        Gives the most present group at the same time
        Arg 1 : Header tab
        '''

        # Get all combinations of all groups
        self.combin_list = self.get_combin_list(self.employees, self.object_per_group)
        len_combin_list = len(self.combin_list)
        #print("len_combin_list")
        #print(len_combin_list)
        #self.dt_id_group = self.get_dt_id_group(self.combin_list, len_combin_list)         USELESS FOR NOW
        
        # REPLACE BY list() IF IT IS MORE FAST OR TO HAVE SAME CODE EVERYWHERE
        result = list()

        for i in range (len_combin_list):
            self.value_each_group.append(self.Tabstats_F2(result, self.combin_list[i]))
            

    def get_combin_list(self, seq, k):
        '''
        Give all combinations of X desired employees.
        ">>" is a binary operation : x * 2**y
        '''
        # REPLACE BY list() IF IT IS MORE FAST OR TO HAVE SAME CODE EVERYWHERE
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
        

    def get_dt_id_group(self, combin_list, len_combin_list):
        '''
        arg1: combin of all groups, arg2: number of group for the dictionnary
        return a dictionnary which mut a key for each group, to find the group at the end of the F2, with the index
        '''
        dt_id_group = {}
        for i in range(len_combin_list):
            dt_id_group[i] = combin_list[i]
        return dt_id_group


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