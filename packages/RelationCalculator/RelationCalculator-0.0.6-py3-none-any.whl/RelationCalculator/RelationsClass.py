import numpy as np

# Perform logical multiplication on two boolean matrices.
def logicMulti(a, b):
    c = np.matmul(a, b)
    return (c >= 1) * 1

class Relation:
    """
    Attributes:
        elements (set): Elements in the set.
        relations (dict): A dictionary storing pairs of relationships between elements.
        relations_list (list): A list storing tuples of relationships between elements.
        matrix (np.array): Store the relation matrix.
    """

    def __init__(self, elements=None, relations=None):
        if elements:
            self.elements = list(elements)
        else:
            self.elements = []
        self.relations = {}
        self.relations_list = []
        self.matrix = None

        if relations:
            for element1,element2 in relations:
                if element1 not in self.elements:
                    self.elements.append(element1)
                if element2 not in elements:
                    self.elements.append(element2)
                self.add_relation(element1, element2)
                if (element1, element2) not in self.relations_list:
                    self.relations_list.append((element1, element2))
        self.set_relation_matrix()

    def add_relation(self, element1, element2):
        if (element1, element2) not in self.relations_list:
            self.relations_list.append((element1, element2))
        if element1 not in self.relations:
            self.relations[element1] = set()

        self.relations[element1].add(element2)
        self.set_relation_matrix()

    def set_relation_matrix(self):
        n = len(self.elements)
        self.matrix = np.zeros((n, n),dtype=np.int64)
        for element1, element2 in self.relations_list:
            i = self.elements.index(element1)
            j = self.elements.index(element2)
            self.matrix[i, j] = 1

    def count_relations(self):
        return len(self.relations_list)

    def get_all_elements(self):
        return self.elements

    def get_all_relations(self):
        return self.relations_list

    def get_relation_matrix(self):
        self.set_relation_matrix()
        return self.matrix

    # Check if there is a relationship between two elements.
    def is_related(self, element1, element2):
        return element2 in self.relations.get(element1, set())

    # Determine whether a relation is reflexive.
    def isReflexive(self):
        if not self.elements:
            return True

        for element in self.elements:
            if (element,element) not in self.relations_list:
                return False

        return True

    # Determine whether a relation is anti-reflexive.
    def isIrreflexive(self):
        if not self.elements:
            return True

        for element in self.elements:
            if (element,element) in self.relations_list:
                return False

        return True

    # Determine whether a binary relation is symmetric.
    def isSymmetric(self):
        if not self.elements:
            return True

        for element1,element2 in self.relations_list:
            if (element2,element1) not in self.relations_list:
                return False

        return True

    # Determine whether a binary relation is anti-symmetric.
    def isAntisymmetric(self):
        m1 = self.matrix
        np.fill_diagonal(m1, 0)
        m2 = np.transpose(m1)
        m3 = m1 + m2
        return np.all(m3 < 1.5)

    # Determine whether a binary relation is transitive.
    def isTransitive(self):
        m1 = self.matrix
        m2 = logicMulti(m1, m1)
        return ((m2 > m1).sum() == 0)


class RelationDefineByMatrix(Relation):

    def __init__(self,m):
        shape = m.shape
        if shape[0] != shape[1]:
            raise ValueError("The input matrix dimensions are incorrect.")
        elements = list(range(1, shape[0] + 1))
        relations = []
        for index, ele in np.ndenumerate(m):
            if ele == 1:
                relations.append((index[0]+1,index[1]+1))
        super().__init__(elements,relations)
        if not isinstance(m,type([])) and not isinstance(m,np.ndarray) and not isinstance(m,np.array):
            raise ValueError("The input data should be an array, ndarray, or list.")

        self.m = m

    # Convert a boolean matrix to binary data, and finally convert it to decimal data.
    def matrix2num(self):
        k = self.m.reshape(1, -1)
        return int("".join(str(i) for i in k[0]), 2)

    # Judge reflexivity
    def isReflexive(self):
        m1 = np.diag(self.m)
        return np.all(m1 == 1)

    # Judge antireflexivity
    def isIrreflexitive(self):
        m1 = np.diag(self.m)
        return np.all(m1 == 0)

    # Judge symmetry
    def isSymmetric(self):
        m1 = self.m
        m2 = np.transpose(m1)
        m3 = (m1 == m2)
        return np.all(m3 == 1)

    # Judge antisymmetry
    def isAntiSymmetric(self):
        m1 = self.m
        np.fill_diagonal(m1, 0)
        m2 = np.transpose(m1)
        m3 = m1 + m2
        return np.all(m3 < 1.5)

    # Judge transmissibility
    def isTransitive(self):
        m1 = self.m
        m2 = logicMulti(m1, m1)
        return ((m2 > m1).sum() == 0)


class RelationDefineByInt(RelationDefineByMatrix):

    def __init__(self, n, size):
        self.n = n
        self.size = size
        k = bin(self.n)[2:].rjust(self.size ** 2, '0')
        matrix =  np.array(list(map(int, list(k)))).reshape(self.size, self.size)
        super().__init__(matrix)

    # After converting the decimal number n to a binary number, it is converted to a matrix of size*size
    def num2matrix(self):
        if self.size < 0:
            raise ValueError("The function parameter is invalid.")

        k = bin(self.n)[2:].rjust(self.size ** 2, '0')
        return np.array(list(map(int, list(k)))).reshape(self.size, self.size)

# relation = Relation({'A','B','C'},[('C',6)])
#
# relation.add_relation('A','B')
# relation.add_relation('A', 'C')
# relation.add_relation('B','C')
#
# 
# print(relation.count_relations())
#
# print(relation.is_related('A','C'))
# print(relation.is_related('B','A')) 
# print(relation.is_related('C',6)) 
#
# print(relation.get_all_elements())
# print(relation.get_all_relations())
#
# print(relation.isReflexive())
# print(relation.isIrreflexive())
# print(relation.isTransitive())
#
# print(relation.get_relation_matrix())

# relation = RelationDefineByInt(511,3)

# print(relation.get_all_elements())