from threading import Thread



class F2(Thread):

    def __init__(self, array_part_i, employees_i, full_table_i):
        '''
        Constructor for threads
        '''
        Thread.__init__(self)
        
        # Boundaries for threads
        self.array_part = int(array_part_i)
        
        # Header employees
        self.employees = employees_i
        
        # All data
        self.full_table = full_table_i
        
        # Object per combin
        self.object_per_group = 2

        # To analyse each group
        self.selectedEmployees = ''
        self.nbEmployeesSelected = 0

        # All groups
        self.combin_list = list()

        # Position of group in list
        self.index_best_group, self.maxi = self.The_Most(self.employees)

    def The_Most(self, employees):
        '''
        Gives the most present group at the same time
        Arg 1 
        '''

        # Get all combinations of X desired employees
        self.combin_list = self.get_combin_list(employees, self.object_per_group)
        len_combin_list = len(self.combin_list)
        
        print("combin_list")
        print(self.combin_list)

        print("len_combin_list")
        print(len_combin_list)
        
        # REPLACE BY list() IF IT IS MORE FAST OR TO HAVE SAME CODE EVERYWHERE
        value_each_group = list()
        resultVerif = list()

        for i in range (len_combin_list):
            # OLD
            #M += [Tabstats(moisEnCours, combin_list[i])]
            
            # NEW
            value_each_group.append(self.Tabstats_F2(resultVerif, self.combin_list[i]))
        
        return self.maximum(value_each_group)


    def get_combin_list(self, seq, k):
        '''
        Give all combinations of X desired employees
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
                print(s)
                p.append(s)
            i += 1 
        return p
        

    def Tabstats_F2(self, resultVerif, selectedEmployees):
        '''
        Second functionnality : Checks input, do calcul, and return result
        '''
        self.nbEmployeesSelected = len(selectedEmployees)
            
        # Replaces names with numeric values
        selectedFigures = self.replaceNamesByNumbers(selectedEmployees, self.employees)
        
        # Sorting in ascending order employees
        selectedFiguresSorted = self.orderList(selectedFigures)

        #Count how many time employees selected gave worked together
        resultVerif = self.how_much_worked_together(self.full_table, self.nbEmployeesSelected, selectedFiguresSorted)
        return(resultVerif)


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
            for i in range (self.nbEmployeesSelected):
                if self.full_table[j][selectedFiguresSorted[i]] != "":
                    counter += 1
            if counter == self.nbEmployeesSelected:
                total += 1

        total = str(total)
        return(total)


    def maximum(self, value_each_group):
        '''
        Return :
            Index of the group of employees which worked the most together
            Number of days
        '''
        # Convert to int sorted list and get max
        value_each_group_int = map(int, value_each_group) 
        value_each_group_int = sorted(value_each_group_int) 
        maxi = max(value_each_group_int)

        # Get index of best group
        index_best_group = value_each_group.index(str(maxi))

        return(index_best_group, maxi)