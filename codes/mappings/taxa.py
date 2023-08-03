
class Index_mapping:
    def __init__(self, taxa_list):
        self.taxa_list = []
        self.taxa_map = {}
        self.taxa_reverse_map = {}
        self.cnt = 1
        for taxa in taxa_list:
            self.add_val(taxa)
        
    
    def add_val(self, val):
        if val not in self.taxa_map:
            self.taxa_map[val] = self.cnt
            self.taxa_reverse_map[self.cnt] = val
            self.cnt += 1
            self.taxa_list.append(val)
        

    def get_index(self, val):
        return self.taxa_map[val]
    
    def get_value(self, index):
        return self.taxa_reverse_map[index]

    def get_taxa_list(self):
        return self.taxa_list

            