import numpy as np
import matplotlib.pyplot as plt

# Number of transitive relations on n labeled nodes.
TRANSITIVE_RELATIONS = [1, 2, 13, 171, 3994, 154303, 9415189, 878222530, 122207703623, 24890747921947,
                      7307450299510288, 3053521546333103057, 1797003559223770324237, 1476062693867019126073312,
                      1679239558149570229156802997, 2628225174143857306623695576671, 5626175867513779058707006016592954,
                      16388270713364863943791979866838296851, 64662720846908542794678859718227127212465]

# Number of partially ordered sets ("posets") with n labeled elements (or labeled acyclic transitive digraphs).
POSETS_NUM = [1, 1, 3, 19, 219, 4231, 130023, 6129859, 431723379, 44511042511, 6611065248783, 1396281677105899,
            414864951055853499, 171850728381587059351, 98484324257128207032183, 77567171020440688353049939,
            83480529785490157813844256579, 122152541250295322862941281269151, 241939392597201176602897820148085023]

# Number of different quasi-orders (or topologies, or transitive digraphs) with n labeled elements.
QUASI_ORDER = [1, 1, 4, 29, 355, 6942, 209527, 9535241, 642779354, 63260289423, 8977053873043,
            1816846038736192, 519355571065774021, 207881393656668953041, 115617051977054267807460,
            88736269118586244492485121, 93411113411710039565210494095, 134137950093337880672321868725846,
            261492535743634374805066126901117203]

# Perform logical multiplication on two boolean matrices.
def logicMulti(a, b):
    c = np.matmul(a, b)
    return (c >= 1) * 1

import numpy as np
import matplotlib.pyplot as plt

def plot_matrices(matrices, num_rows, num_cols, output_filename):
    # Convert the generated matrix list to a NumPy array.
    matrices = np.array(matrices)

    # Calculate the number of matrices.
    num_matrices = len(matrices)

    # Ensure that the number of subplots matches the number of matrices.
    if num_matrices > num_rows * num_cols or num_matrices < num_rows * num_cols:
        raise ValueError("The number of matrices is not equal to the number of subgraphs.")

    # Create a figure object.
    fig, axes = plt.subplots(num_rows, num_cols, figsize=(25, 14))

    # If there is only one matrix, convert the axes to an array.
    if num_matrices == 1:
        axes = np.array([axes])

    # Iterate over each matrix and plot it in a subplot.
    for i, matrix in enumerate(matrices):
        row = i // num_cols
        col = i % num_cols
        ax = axes[row, col]

        im = ax.imshow(matrix, cmap='binary')

        # Add a black border.
        ax.set_xlim(-0.5, matrix.shape[1] - 0.5)
        ax.set_ylim(matrix.shape[0] - 0.5, -0.5)
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_color('black')
            spine.set_linewidth(2)

        # Determine whether it is a matrix of all zeros or all ones.
        if np.array_equal(matrix, np.ones_like(matrix)):
            ax.fill_between([-0.5, matrix.shape[1] - 0.5], [-0.5, -0.5], [matrix.shape[0] - 0.5, matrix.shape[0] - 0.5], color='black')
            ax.set_facecolor('black')

    # Adjust the spacing between subplots and save the image.
    plt.subplots_adjust(wspace=0.1, hspace=0.1)
    plt.savefig(output_filename)
    plt.close(fig) 


class Calculator:

    def __init__(self, n):
       
        self.size = n
        self.all_retlation_num = 2 ** (self.size ** 2)
    
    def count_all_relations(self):
       
        return self.all_retlation_num

   # Generate all binary relationships on a set of n elements, represented as binary numbers
    def generate_all_relations(self):
        if self.size < 0:
            raise ValueError("The function parameter is invalid.")

        all_relations = []
        for i in range(2 ** (self.size * self.size)):
            binary = bin(i)[2:].zfill(self.size * self.size)
            relation = [int(bit) for bit in binary]
            relation_str = ''.join(str(bit) for bit in relation)
            all_relations.append(relation_str)
        return all_relations

    # Generate all binary relationships on a set of n elements, represented in the form of a matrix of relations
    def generate_all_relations_as_matrices(self):
        if self.size < 0:
            raise ValueError("The function parameter is invalid.")

        relation_matrices = []
        for i in range(2 ** (self.size * self.size)):
            binary = bin(i)[2:].zfill(self.size * self.size)
            relation = [int(bit) for bit in binary]
            matrix = np.array(relation).reshape(self.size, self.size)
            relation_matrices.append(matrix)
        return relation_matrices
    
    # Reflexive relationship
    def count_reflexive_relations(self):
        if self.size < 0:
            raise ValueError("The function parameter is invalid.")

        return 2 ** (self.size ** 2 - self.size)

    # Generate all reflexive relationships on a set of n elements, represented as binary numbers
    def generate_reflexive_relations(self):
        all_relations = []
        all_relations_set = set()
        for i in range(2 ** (self.size * self.size)):
            binary = list(bin(i)[2:].zfill(self.size * self.size))
            for j in range(self.size):
                binary[j * self.size + j] = '1'
            binary = ''.join(binary)
            if binary in all_relations_set:
                continue
            all_relations_set.add(binary)
            all_relations.append(binary)
        return all_relations

    # Generate all reflexive relationships on a set of n elements, represented in the form of a matrix of relations
    def generate_reflexive_relations_as_matrices(self):
        reflexive_matrices = []
        all_relations_set = set()
        for i in range(self.all_retlation_num):
            binary = list(bin(i)[2:].zfill(self.size * self.size))
            for j in range(self.size):
                binary[j * self.size + j] = '1'
            binary = ''.join(binary)
            if binary in all_relations_set:
                continue
            all_relations_set.add(binary)
            relation = [int(bit) for bit in binary]
            relation_matrix = np.array(relation).reshape(self.size, self.size)
            reflexive_matrices.append(relation_matrix)
        return reflexive_matrices

    # Count irreflexive relations
    def count_irreflexive_relations(self):
        if self.size < 0:
            raise ValueError("The function parameter is invalid.")

        return 2 ** (self.size ** 2 - self.size)

    # Generate all irreflexive relationships on a set of n elements, represented as binary numbers
    def generate_all_irreflexive_relations(self):
        all_relations = []
        all_relations_set = set()
        for i in range(self.all_retlation_num):
            binary = list(bin(i)[2:].zfill(self.size * self.size))
            for j in range(self.size):
                binary[j * self.size + j] = '0'
            binary = ''.join(binary)
            if binary in all_relations_set:
                continue
            all_relations_set.add(binary)
            all_relations.append(binary)
        return all_relations

    # Generate all irreflexive relationships on a set of n elements, represented in the form of a matrix of relations
    def generate_irreflexive_relations_as_matrices(self):
        irreflexive_matrices = []
        all_relations_set = set()
        for i in range(self.all_retlation_num):
            binary = list(bin(i)[2:].zfill(self.size * self.size))
            for j in range(self.size):
                binary[j * self.size + j] = '0'
            binary = ''.join(binary)
            if binary in all_relations_set:
                continue
            all_relations_set.add(binary)
            relation = [int(bit) for bit in binary]
            relation_matrix = np.array(relation).reshape(self.size, self.size)
            irreflexive_matrices.append(relation_matrix)
        return irreflexive_matrices

    # Count Symmetric relations
    def count_symmetric_relations(self):
        if self.size < 0:
            raise ValueError("The function parameter is invalid.")

        return 2 ** ((self.size ** 2 + self.size) // 2)

    # Generate a binary representation of a symmetrical binary relationship on a set of n elements
    def generate_all_symmetric_relations(self):
        all_relations = []
        for i in range(2 ** (self.size * (self.size + 1) // 2)):
            binary = bin(i)[2:].zfill(self.size * (self.size + 1) // 2)
            binary_new = ['0'] * (self.size * self.size)
            k = 0
            for j in range(self.size):
                for l in range(j, self.size):
                    index1 = j * self.size + l
                    index2 = l * self.size + j
                    binary_new[index1] = binary[k]
                    binary_new[index2] = binary[k]
                    k += 1
            all_relations.append(''.join(binary_new))
        return all_relations

    # Generate a matrix corresponding to all symmetry relationships on n elements
    def generate_symmetric_relations_as_matrices(self):
        symmetric_matrices = []
        for i in range(2 ** (self.size * (self.size + 1) // 2)):
            binary = bin(i)[2:].zfill(self.size * (self.size + 1) // 2)
            relation = [int(bit) for bit in binary]
            relation_matrix = np.zeros((self.size, self.size), dtype=int)
            triu_indices = np.triu_indices(self.size)  
            relation_matrix[triu_indices] = relation
            symmetric_matrix = np.maximum(relation_matrix, relation_matrix.T) 
            symmetric_matrices.append(symmetric_matrix)
        return symmetric_matrices

    # Count Antisymmetric relations
    def count_antisymmetric_relations(self):
        if self.size < 0:
            raise ValueError("The function parameter is invalid.")

        return 2 ** self.size * 3 ** ((self.size ** 2 - self.size) // 2)

    # Generate a binary representation of a antisymmetrical binary relationship on a set of n elements
    def generate_all_antisymmetric_relations(self):
        all_relations = []
        for i in range(self.all_retlation_num):
            binary = bin(i)[2:].zfill(self.size * self.size)
            is_antisymmetric = True
            for j in range(self.size):
                for k in range(self.size):
                    index1 = j * self.size + k
                    index2 = k * self.size + j
                    if binary[index1] == '1' and binary[index2] == '1' and j != k:
                        is_antisymmetric = False
                        break
                if not is_antisymmetric:
                    break
            if is_antisymmetric:
                all_relations.append(''.join(binary))
        return all_relations

    # Generate a matrix corresponding to all antisymmetry relationships on n elements
    def generate_antisymmetric_relations_as_matrices(self):
        antisymmetric_matrices = []
        for i in range(self.all_retlation_num):
            binary = bin(i)[2:].zfill(self.size * self.size)
            is_antisymmetric = True
            for j in range(self.size):
                for k in range(self.size):
                    index1 = j * self.size + k
                    index2 = k * self.size + j
                    if binary[index1] == '1' and binary[index2] == '1' and j != k:
                        is_antisymmetric = False
                        break
                if not is_antisymmetric:
                    break
            if is_antisymmetric:
                matrix = np.array(list(binary)).reshape(self.size, self.size)
                antisymmetric_matrices.append(matrix)
        return antisymmetric_matrices

    # Count reflexive and symmetric relations
    def count_reflexive_symmetric_relations(self):
        if self.size < 0:
            raise ValueError("The function parameter is invalid.")

        return 2 ** ((self.size ** 2 - self.size) // 2)

    # Generate a binary representation of a reflexivite and symmetrical binary relationship on a set of n elements
    def generate_all_reflexive_symmetric_relations(self):
        all_relations = []
        for i in range(2 ** (self.size * (self.size + 1) // 2)):
            binary = bin(i)[2:].zfill(self.size * (self.size + 1) // 2)
            binary_new = ['0'] * (self.size * self.size)
            k = 0
            flag = True
            for j in range(self.size):
                for l in range(j, self.size):
                    index1 = j * self.size + l
                    index2 = l * self.size + j
                    binary_new[index1] = binary[k]
                    binary_new[index2] = binary[k]
                    k += 1
            # Check for reflexive relationships
            for h in range(self.size):
                if binary_new[h * self.size + h] != '1':
                    flag = False
                    break
            if flag == True:
                all_relations.append(''.join(binary_new))
        return all_relations

    # Generate a matrix corresponding to all reflexivite and symmetry relationships on n elements
    def generate_reflexive_symmetric_relations_as_matrices(self):
        symmetric_matrices = []
        for i in range(2 ** (self.size * (self.size + 1) // 2)):
            binary = bin(i)[2:].zfill(self.size * (self.size + 1) // 2)
            relation = [int(bit) for bit in binary]
            relation_matrix = np.zeros((self.size, self.size), dtype=int)
            triu_indices = np.triu_indices(self.size)  
            relation_matrix[triu_indices] = relation
            symmetric_matrix = np.maximum(relation_matrix, relation_matrix.T)  
            diagonal_elements = np.diag(symmetric_matrix)
            all_ones = np.all(diagonal_elements == 1)
            if all_ones:
                symmetric_matrices.append(symmetric_matrix)
        return symmetric_matrices

    # Count irreflexive and symmetric relations
    def count_irreflexive_symmetric_relations(self):
        if self.size < 0:
            raise ValueError("The function parameter is invalid.")

        return 2 ** ((self.size ** 2 - self.size) // 2)

    # Generate a binary representation of a irreflexive and symmetrical binary relationship on a set of n elements
    def generate_all_irreflexive_symmetric_relations(self):
        all_relations = []
        for i in range(2 ** (self.size * (self.size + 1) // 2)):
            binary = bin(i)[2:].zfill(self.size * (self.size + 1) // 2)
            binary_new = ['0'] * (self.size * self.size)
            k = 0
            flag = True
            for j in range(self.size):
                for l in range(j, self.size):
                    index1 = j * self.size + l
                    index2 = l * self.size + j
                    binary_new[index1] = binary[k]
                    binary_new[index2] = binary[k]
                    k += 1
            # Check for irreflexive relationships
            for h in range(self.size):
                if binary_new[h * self.size + h] != '0':
                    flag = False
                    break
            if flag == True:
                all_relations.append(''.join(binary_new))
        return all_relations

    # Generate a matrix corresponding to all irreflexive and symmetry relationships on n elements
    def generate_irreflexive_symmetric_relations_as_matrices(self):
        symmetric_matrices = []
        for i in range(2 ** (self.size * (self.size + 1) // 2)):
            binary = bin(i)[2:].zfill(self.size * (self.size + 1) // 2)
            relation = [int(bit) for bit in binary]
            relation_matrix = np.zeros((self.size, self.size), dtype=int)
            triu_indices = np.triu_indices(self.size)  
            relation_matrix[triu_indices] = relation
            symmetric_matrix = np.maximum(relation_matrix, relation_matrix.T)  
            diagonal_elements = np.diag(symmetric_matrix)
            all_zeros = np.all(diagonal_elements == 0)
            if all_zeros:
                symmetric_matrices.append(symmetric_matrix)
        return symmetric_matrices

    # Count not reflexivite and not irreflexive relations
    def count_nonreflexive_nonirreflexive_relations(self):
        if self.size < 0:
            raise ValueError("The function parameter is invalid.")

        return self.all_retlation_num - 2 ** (self.size ** 2 - self.size + 1)

    # Generate all not reflexivite and not irreflexive binary relationships on a set of n elements, represented as binary numbers
    def generate_all_nonreflexive_nonirreflexive_relations(self):
        all_relations = []
        for i in range(self.all_retlation_num):
            binary = bin(i)[2:].zfill(self.size * self.size)
            relation = [int(bit) for bit in binary]
            relation_str = ''.join(str(bit) for bit in relation)
            # Check for reflexive relationships
            ref_flag = True
            for h in range(self.size):
                if relation_str[h * self.size + h] != '1':
                    ref_flag = False
                    break
            # Check for irreflexive relationships
            anti_flag = True
            for h in range(self.size):
                if relation_str[h * self.size + h] != '0':
                    anti_flag = False
                    break
            if ref_flag == False and anti_flag == False:
                all_relations.append(relation_str)
        return all_relations

    # Generate a matrix corresponding to all not reflexivite and not irreflexive relationships on n elements
    def generate_nonreflexive_nonirreflexive_relations_as_matrices(self):
        relation_matrices = []
        for i in range(self.all_retlation_num):
            binary = bin(i)[2:].zfill(self.size * self.size)
            relation = [int(bit) for bit in binary]
            matrix = np.array(relation).reshape(self.size, self.size)
            diagonal_elements = np.diag(matrix)
            all_ones = np.all(diagonal_elements == 1)
            all_zeros = np.all(diagonal_elements == 0)
            if all_ones == False and all_zeros == False:
                relation_matrices.append(matrix)
        return relation_matrices

    # Count not reflexivite ,not antireflexivite Symmetric relations
    def count_nonreflexive_nonirreflexive_symmetric_relations(self):
        if self.size < 0:
            raise ValueError("The function parameter is invalid.")

        return (2 ** self.size - 2) * 2 ** ((self.size ** 2 - self.size) // 2)

    # Generate a binary representation of a not reflexivite ,not antireflexivite Symmetric binary relationship on a set of n elements
    def generate_all_nonreflexive_nonirreflexive_symmetric_relations(self):
        all_relations = []
        for i in range(2 ** (self.size * (self.size + 1) // 2)):
            binary = bin(i)[2:].zfill(self.size * (self.size + 1) // 2)
            binary_new = ['0'] * (self.size * self.size)
            k = 0
            for j in range(self.size):
                for l in range(j, self.size):
                    index1 = j * self.size + l
                    index2 = l * self.size + j
                    binary_new[index1] = binary[k]
                    binary_new[index2] = binary[k]
                    k += 1
            # Check for reflexive relationships
            ref_flag = True
            for h in range(self.size):
                if binary_new[h * self.size + h] != '1':
                    ref_flag = False
                    break
            # Check for antireflexive relationships
            anti_flag = True
            for h in range(self.size):
                if binary_new[h * self.size + h] != '0':
                    anti_flag = False
                    break
            if ref_flag == False and anti_flag == False:
                all_relations.append(''.join(binary_new))
        return all_relations

    # Generate a matrix corresponding to all not reflexivite ,not antireflexivite Symmetric relationships on n elements
    def generate_nonreflexive_nonirreflexive_symmetric_relations_as_matrices(self):
        symmetric_matrices = []
        for i in range(2 ** (self.size * (self.size + 1) // 2)):
            binary = bin(i)[2:].zfill(self.size * (self.size + 1) // 2)
            relation = [int(bit) for bit in binary]
            relation_matrix = np.zeros((self.size, self.size), dtype=int)
            triu_indices = np.triu_indices(self.size)
            relation_matrix[triu_indices] = relation
            symmetric_matrix = np.maximum(relation_matrix, relation_matrix.T)
            diagonal_elements = np.diag(symmetric_matrix)
            all_ones = np.all(diagonal_elements == 1)
            all_zeros = np.all(diagonal_elements == 0)
            if all_ones == False and all_zeros == False:
                symmetric_matrices.append(symmetric_matrix)
        return symmetric_matrices

    # Count transitive relations
    def count_transitive_relations(self):
        if self.size < 0 or self.size > 18:
            raise ValueError("The function parameter is invalid.")
        
        return TRANSITIVE_RELATIONS[self.size]

    # Generate all transitive binary relationships on a set of n elements, represented as binary numbers
    def generate_all_transitive_relations(self):
        all_relations = []
        for i in range(self.all_retlation_num):
            binary = bin(i)[2:].zfill(self.size * self.size)
            relation = [int(bit) for bit in binary]
            matrix = np.array(relation).reshape(self.size, self.size)
            m = logicMulti(matrix, matrix)
            if ((m > matrix).sum() == 0):
                binary = ''.join(str(bit) for row in matrix for bit in row)
                all_relations.append(binary)
        return all_relations

    # Generate all transitive binary relationships on a set of n elements, represented in the form of a matrix of relations
    def generate_transitive_relations_as_matrices(self):
        relation_matrices = []
        for i in range(self.all_retlation_num):
            binary = bin(i)[2:].zfill(self.size * self.size)
            relation = [int(bit) for bit in binary]
            matrix = np.array(relation).reshape(self.size, self.size)
            m = logicMulti(matrix, matrix)
            if ((m > matrix).sum() == 0):
                relation_matrices.append(matrix)
        return relation_matrices

    # Count PartialOrder relations
    def count_partialOrder_relations(self):
        if self.size < 0 or self.size > 18:
            raise ValueError("The function parameter is invalid.")

        return POSETS_NUM[self.size]

    # Generate all PartialOrder binary relationships on a set of n elements, represented as binary numbers
    def generate_all_partialOrder_relations(self):
        all_relations = []
        for i in range(self.all_retlation_num):
            binary = bin(i)[2:].zfill(self.size * self.size)
            relation = [int(bit) for bit in binary]
            matrix = np.array(relation).reshape(self.size, self.size)
            diagonal_elements = np.diag(matrix)
            all_ones = np.all(diagonal_elements == 1)
            m = logicMulti(matrix, matrix)
            m1 = np.copy(matrix)
            np.fill_diagonal(m1, 0)
            m2 = np.transpose(m1)
            m3 = m1 + m2
            # transactive、reflective、antisymmetry
            if ((m > matrix).sum() == 0) and all_ones and np.all(m3 < 1.5):
                binary = ''.join(str(bit) for row in matrix for bit in row)
                all_relations.append(binary)
        return all_relations

    # Generate all PartialOrde binary relationships on a set of n elements, represented in the form of a matrix of relations
    def generate_partialOrder_relations_as_matrices(self):
        relation_matrices = []
        for i in range(self.all_retlation_num):
            binary = bin(i)[2:].zfill(self.size * self.size)
            relation = [int(bit) for bit in binary]
            matrix = np.array(relation).reshape(self.size, self.size)
            # reflective
            diagonal_elements = np.diag(matrix)
            all_ones = np.all(diagonal_elements == 1)
            # transactive
            m = logicMulti(matrix, matrix)
            isTransactive = ((m > matrix).sum() == 0)
            # antisymmetry
            m1 = np.copy(matrix)
            np.fill_diagonal(m1, 0)
            m2 = np.transpose(m1)
            m3 = m1 + m2
            isAntisymmetry = np.all(m3 < 1.5)
            if all_ones and isTransactive and isAntisymmetry:
                relation_matrices.append(matrix)
        return relation_matrices

    # Count Quasi-ordering relations
    def count_quasiOrder_relations(self):
        if self.size < 0 or self.size > 18:
            raise ValueError("The function parameter is invalid.")

        return QUASI_ORDER[self.size]

    # Generate all Quasi-ordering binary relationships on a set of n elements, represented as binary numbers
    def generate_all_quasiOder_relations(self):
        all_relations = []
        for i in range(self.all_retlation_num):
            binary = bin(i)[2:].zfill(self.size * self.size)
            relation = [int(bit) for bit in binary]
            matrix = np.array(relation).reshape(self.size, self.size)
            diagonal_elements = np.diag(matrix)
            all_zeros = np.all(diagonal_elements == 1)
            m = logicMulti(matrix, matrix)
            # transactive、reflective
            if ((m > matrix).sum() == 0) and all_zeros:
                binary = ''.join(str(bit) for row in matrix for bit in row)
                all_relations.append(binary)
        return all_relations

    # Generate all Quasi-ordering binary relationships on a set of n elements, represented in the form of a matrix of relations
    def generate_quasiOder_relations_as_matrices(self):
        relation_matrices = []
        for i in range(self.all_retlation_num):
            binary = bin(i)[2:].zfill(self.size * self.size)
            relation = [int(bit) for bit in binary]
            matrix = np.array(relation).reshape(self.size, self.size)
            # reflective
            diagonal_elements = np.diag(matrix)
            all_zeros = np.all(diagonal_elements == 1)
            # transactive
            m = logicMulti(matrix, matrix)
            isTransactive = ((m > matrix).sum() == 0)
            if all_zeros and isTransactive:
                relation_matrices.append(matrix)
        return relation_matrices

