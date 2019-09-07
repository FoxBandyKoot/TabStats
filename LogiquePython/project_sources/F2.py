from .F2_Threads_part import F2_Threads_part

class F2():

    #dt_name for Dictionnary
    '''
    def __init__(self, half_tab_i, lines_to_read_i, employees_i, full_table_i, object_per_group_i):
    '''
    #Constructor for threads
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
    '''

    def __init__(self, employees_i, nb_lines_i, full_table_i, object_per_group_i):
        '''
        Constructor
        '''
        self.employees = employees_i
        self. nb_lines = nb_lines_i
        self.object_per_group = object_per_group_i
        self.full_table = full_table_i

    def main(self):
        '''
        Gives the most present group at the same time
        Arg 1 : Header tab
        '''
        # Get all combinations of all groups
        combin_list = self.get_combin_list(self.employees, self.object_per_group)
        len_combin_list = len(combin_list)
        print("len_combin_list")
        print(len_combin_list)
        #self.dt_id_group = self.get_dt_id_group(combin_list, len_combin_list)         USELESS FOR NOW
        
        '''
        # REPLACE BY list() IF IT IS MORE FAST OR TO HAVE SAME CODE EVERYWHERE
        result = list()

        for i in range (len_combin_list):
            self.value_each_group.append(self.Tabstats_F2(result, combin_list[i]))
        '''
        
        # Boundaries for each threads
        if self.nb_lines % 2 == 0:
            first_half_lines = self.nb_lines / 2
            second_half_lines = self.nb_lines
        else:
            print("FUCK IT")
            
        
        # Create threads
        th_first_half_tab = F2_Threads_part("first_half_tab", first_half_lines, self.employees, self.full_table, self.object_per_group, combin_list)
        th_second_half_tab = F2_Threads_part("second_half_tab", second_half_lines, self.employees, self.full_table, self.object_per_group, combin_list)

        # Run threads
        th_first_half_tab.start()
        th_second_half_tab.start()

        # Wait threads to finish
        th_first_half_tab.join()
        th_second_half_tab.join()

        # Convert list to int
        th_first_half_tab.value_each_group = list(map(int, th_first_half_tab.value_each_group))
        th_second_half_tab.value_each_group = list(map(int, th_second_half_tab.value_each_group))
        
        
        # Merge the 2 threads
        value_each_group = [x + y for x, y in zip(th_first_half_tab.value_each_group, th_second_half_tab.value_each_group)]
        
        # Get index of the best group
        self.index_best_group, maxi = self.maximum(value_each_group)
        '''
        #print(th_first_half_tab.combin_list)
        '''
        if th_first_half_tab.combin_list:
            self.best_group = th_first_half_tab.combin_list[self.index_best_group]
            print("best_group")
            print(self.best_group)

    
    def maximum(self, value_each_group):
        '''
        #Return the index of the group of employees which worked the most together
        '''
        maxi = max(value_each_group)
        print("maxi")
        print(maxi)
        # Get index of best group
        index_best_group = value_each_group.index(maxi)

        return(index_best_group, maxi)
    

    def get_combin_list(self, seq, k):
        '''
        #Give all combinations of X desired employees.
        #">>" is a binary operation : x * 2**y
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
