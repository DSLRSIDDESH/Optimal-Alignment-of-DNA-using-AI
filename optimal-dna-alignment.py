def a_star_search(seq1, seq2, subst_cost, gap_cost):
    sequence1,sequence2 = seq1, seq2
    goal_node = None

    # defined heuristic function as the number of mismatches in the given two sequences
    def heuristic(seq1,seq2):
        n1 = len(seq1)
        n2 = len(seq2)
        n = min(n1,n2)
        sum1 = sum([seq1[i] != seq2[i] for i in range(n)])
        if n1 == n2:
            return sum1
        elif n1 > n2:
            return (sum1 + (n1 - n2))
        else:
            return (sum1 + (n2 - n1))

    # function to get the successor nodes of the given node
    def successors(node):
        seq1, seq2, g_cost, curr_cost, parent, h_value, f_value, position = node
        suc_list = []

        # adding successor with substitution in sequence-2
        mn = min(len(seq1), len(seq2))
        for i in range(mn):
            if seq1[i] != seq2[i]:
                suc_seq2 = seq2[:i] + seq1[i] + seq2[i+1:]
                suc_g_cost = g_cost + subst_cost
                h_value = heuristic(sequence1, suc_seq2)
                f_value = suc_g_cost + h_value
                suc_node = (seq1, suc_seq2, suc_g_cost, curr_cost + 1, node, h_value, f_value, i)
                suc_list.append(suc_node)

        # adding successor with inserting a gap in sequence-2
        for i in range(len(seq2)):
            suc_seq2 = seq2[:i] + "-" + seq2[i:]
            suc_g_cost = g_cost + gap_cost
            h_value = heuristic(sequence1, suc_seq2)
            f_value = suc_g_cost + h_value
            suc_node = (seq1, suc_seq2, suc_g_cost, curr_cost + 1, node, h_value, f_value, i)
            suc_list.append(suc_node)

        # adding successor with deletion in sequence-2
        for i in range(len(seq2)):
            suc_seq2 = seq2[:i] + seq2[i+1:]
            suc_g_cost = g_cost + gap_cost
            h_value = heuristic(sequence1, suc_seq2)
            f_value = suc_g_cost + h_value
            suc_node = (seq1, suc_seq2, suc_g_cost, curr_cost + 1, node, h_value, f_value, i)
            suc_list.append(suc_node)

        return suc_list

    # function to find and get the node with the lowest f-value (i.e. g+h value)
    def minimum_f_node(open_list):
        min_f = float('inf')
        min_node = None
        for node in open_list:
            node_f_value = node[6]
            if node_f_value < min_f:
                min_f = node_f_value
                min_node = node
        return min_node

    # implementation of A* search algorithm for the given problem
    h_cost = heuristic(sequence1, sequence2)
    f_cost = h_cost
    start_node = (sequence1, sequence2, 0, 0, None, h_cost, f_cost, 0)
    open_list = [start_node]
    closed_list = []
    while open_list:
        curr_node = minimum_f_node(open_list)
        open_list.remove(curr_node)
        closed_list.append(curr_node)
        if curr_node[1] == seq1:
            goal_node = curr_node
            break
        suc_list = successors(curr_node)
        for suc_node in suc_list:
            if suc_node in closed_list:
                continue
            if suc_node not in open_list:
                open_list.append(suc_node)
            else:
                index = open_list.index(suc_node)
                if open_list[index][2] > suc_node[2]:
                    open_list[index] = suc_node
                    open_list[index][4] = curr_node

    # reconstructing the path from start node to goal node
    path = [goal_node]
    current_node = goal_node
    while current_node[4] is not None:
        current_node = current_node[4]
        path.append(current_node)
    path.reverse()
    return path


# taking input from the user
seq1 = input("Enter the first DNA sequence: ")
seq2 = input("Enter the second DNA sequence: ")
subst_cost = int(input("Enter the cost for substitution: "))
gap_cost = int(input("Enter the cost for gap insertion/deletion: "))

result = a_star_search(seq1, seq2, subst_cost , gap_cost)

print("\nThe optimal alignment is:\n")
print(result[0][0],"    Cost: ",result[0][2])
print(result[0][1],"\n")
for i in range(1,len(result)):
    prev_cost = result[i-1][2]
    curr_cost = result[i][2]
    print(result[i][0],end="")
    print(f"     Cost: {prev_cost}+{curr_cost-prev_cost} = {curr_cost}")
    print(result[i][1])
    print(" " * result[i][-1] + "^")
    print()
print("Total optimal alignment cost:", result[-1][2])