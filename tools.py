import numpy as np
import os,copy

def iterate_list(current_loop, max_loop, input_list, current_list = [], result = None):

    if result == None:
        result = []

    if current_loop > max_loop:
        result.append(current_list)
        return

    index = len(input_list) - (max_loop - current_loop + 1)
    assert index >= 0, \
        'length of input_list and the number of loops are not compatible!'

    loop_range = len(input_list[index])

    for i in range(loop_range):
        if isinstance(input_list[index][i], list):
            for j in range(len(input_list[index][i])):
                iterate_list(current_loop + 1, max_loop, input_list, current_list + [input_list[index][i][j]], result)
        elif input_list[index][i] == None:
            iterate_list(current_loop + 1, max_loop, input_list, current_list, result)
        else:
            iterate_list(current_loop + 1, max_loop, input_list, current_list + [input_list[index][i]], result)

    return result

def insert_into_input_list(input_list, insert_index, insert_list):
    
    output_list = []
    temp_list = []
    current_list = []
    temp1_list = []
    #* input_list is a two layer list

    dim1 = len(input_list)

    assert len(input_list[0]) >= len(insert_index), \
        "The maximum index of insert_index should be smaller than the length of input_list."
    
    assert len(insert_index) == len(insert_list), \
        "The length of insert_index and insert_list should be the same."

    for list_element in input_list:
        temp_list = []
        counter = 0
        temp_list.append(copy.deepcopy(list_element))
        #* For every list_element in input_list, create a temp_list: temp_list = [] , then deepcopy
        #* Here temp_list is a two layer list: [list_element]
        #! be careful to use append, since the history result will still remians in the list

        for i in range(len(insert_index)):
            if isinstance(insert_list[i], list):
                current_list = []
                current_list = copy.deepcopy(temp_list)
                temp_list = []

                #* a copy of the temp_list that have not came into the for loop
                #* then delete temp_list, to creaete len(insert_list[i]) copies of current_list

                for j in range(len(insert_list[i])):
                    temp1_list = copy.deepcopy(current_list)
                    for i_temp in range(len(current_list)):
                        temp1_list[i_temp].insert(insert_index[i] + counter + 1, insert_list[i][j])
                    temp_list.append(copy.deepcopy(temp1_list))
                    #* in the loop of append, the layers should remains unchanged
                    #* or the elements will not share the same number of layer

                #*before: temp_list = [[[A1],[A2]],[[B1],[B2]],[[C1],[C2]]]
                temp_list = [sublist[i] for sublist in temp_list for i in range(len(sublist))]
                #* to keep the number of layers be same
                counter += 1

            elif insert_list[i] == None:
                pass
            else:
                for i_temp in range(len(temp_list)):
                    temp_list[i_temp].insert(insert_index[i] + counter + 1, insert_list[i])
                counter += 1

        output_list.append(copy.deepcopy(temp_list))
    #! the dimension change must be written out of the loop
    #* Here, out of loop, temp_list is a three layer list: [[[A1],[A2]],[[B1],[B2]],[[C1],[C2]]]
    output_list = [sublist[i] for sublist in output_list for i in range(len(sublist))]
    return output_list

def get_file_list():
    all_list = []
    all_files_list = []
    all_list = os.listdir(os.getcwd())
    all_files_list = [file for file in all_list if os.path.isfile(file)]
    #* select all files in the current directory, and exclude the subdirectory
    return all_files_list

def Multiwfn_exe(prefix_name, name_list_pre, Multiwfn_output_list):
    diff_files_list = []
    file_before = []
    file_after = []
    new_name_list = []

    name_list = [f"{prefix_name}{name_list_pre[i]}" for i in range(len(name_list_pre))]
    assert len(Multiwfn_output_list) == len(name_list), \
            "The name_list and the input_list are not compatible!"

    for i in range(len(Multiwfn_output_list)):
        
        file_before = get_file_list()

        with open('temp.txt','w') as temp:
            for j in range(len(Multiwfn_output_list[i])):
                temp.write(str(Multiwfn_output_list[i][j]) + '\n')
        os.system("Multiwfn < temp.txt > temp.log")

        file_after = get_file_list()

        diff_files_list = list(set(file_after) - set(file_before))

        new_name_list = [f"{diff_files_list[j].split('.')[0]}{name_list[i]}.{diff_files_list[j].split('.')[1]}" for j in range(len(diff_files_list))]

        for k in range(len(diff_files_list)):
            os.rename(diff_files_list[k], new_name_list[k])