import numpy as np
import h5py as hp
from tqdm import tqdm

class FRSpy:

    def __init__(self, target, membership, implication = 'Luka', conjunction = 'Luka'):
        '''
        Compute the membership values to the fuzzy-rough regions

        Attributes
        ----------
        implication: string
            options are 'Luka', 'Godel', 'Fodor', 'Goguen' (see publication for details)
        conjunction: string
            options are 'Standard', 'Algebraic', 'Luka', 'Drastic' (see publication for details)
        '''
        self.membership = membership.to_numpy().astype('int32')
        self.target = target.astype('int32')
        self.im = implication
        self.con = conjunction

    def regions(self, h5file, key, hide_progress):

        POS = np.zeros((len(np.unique(self.target)), len(self.target)))
        NEG = np.zeros((len(np.unique(self.target)), len(self.target)))
        BND = np.zeros((len(np.unique(self.target)), len(self.target)))
        
        with hp.File(h5file, "r") as f:
            for instance in tqdm(f[key].keys(), desc=key+' computing Membership Values', disable=hide_progress): # iterating through rows
                i = int(instance[3:])
                distance = f[key][instance][:]
                for k in np.unique(self.target):
                    POS[k][i], NEG[k][i], BND[k][i] = self.process_object(i, k, distance)

        return [POS, NEG, BND]

    def process_object(self, i, k, distance):

        # lower approximation
        fuzzy_relation_i_j = distance * self.membership[i,k]
        fuzzy_implication = self.implicator(fuzzy_relation_i_j, self.membership[:,k])
        infinum = min(1, fuzzy_implication)
        inf = min(infinum, self.membership[i,k])
        
        # upper approximation
        fuzzy_relation_j_i = distance * self.membership[:,k]
        fuzzy_conjunction = self.conjunction(fuzzy_relation_j_i, self.membership[:,k])
        supremum = max(0, fuzzy_conjunction)
        sup = max(supremum, self.membership[i,k])

        return inf, 1-sup, sup-inf

    def implicator(self, a, b):
        if self.im == 'Luka':
            return min(np.min(1 - a + b), 1)
        
        if self.im == 'Fodor':
            return min(np.where(a <= b, 1, np.maximum(1-a,b)))

        if self.im == 'Godel':
            return min(np.where(a <= b, 1, b))
        
        if self.im == 'Goguen':
            from numpy import inf
            goguen = np.where(a <= b, 1, b/a)
            goguen[goguen == inf] = 0
            return min(goguen)

    def conjunction(self, a, b):
        if self.con == 'Luka':
            return max(np.max(a + b - 1), 0)
        
        if self.con == 'Standard':
            return max(np.minimum(a,b))
        
        if self.con == 'Drastic':
            return max(np.maximum(np.where(b==1, a, 0),np.where(a==1, b, 0)))
        
        if self.con == 'Algebraic':
            return max(a*b)

import sys
if __name__=="__main__":
  args = FRSpy(sys.argv[1], sys.argv[2]).regions(sys.argv[3], sys.argv[4], sys.argv[5])
  print("In mymodule:",args)