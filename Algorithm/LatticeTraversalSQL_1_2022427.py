"""
Executable
For one or two directions in fairness constraints inequalities
Assume data is in mysql

"""

import copy
import json
import time
import pymysql
from decimal import Decimal

import numpy as np
import pandas as pd


def num2string(pattern):
    st = ''
    for i in pattern:
        if i != -1:
            st += str(i)
        st += '|'
    st = st[:-1]
    return st


def transform_to_refinement_format(minimal_added_refinements, numeric_attributes, selection_numeric_attributes,
                                   selection_categorical_attributes, numeric_att_domain_to_relax,
                                   categorical_att_domain_too_add, categorical_att_domain_too_remove):
    minimal_refinements = []
    for ar in minimal_added_refinements:
        select_numeric = copy.deepcopy(selection_numeric_attributes)
        select_categorical = copy.deepcopy(selection_categorical_attributes)
        i = 0
        for att in numeric_attributes:
            select_numeric[att][1] += ar[i]
            i += 1
        for k in categorical_att_domain_too_add:
            if ar[i] == 1:
                select_categorical[k[0]].append(k[1])
            i += 1
        for k in categorical_att_domain_too_remove:
            if ar[i] == 1:
                select_categorical[k[0]].remove(k[1])
            i += 1
        minimal_refinements.append({'numeric': select_numeric, 'categorical': select_categorical})
    return minimal_refinements


def whether_satisfy_fairness_constraints(data, selected_attributes, sensitive_attributes, fairness_constraints,
                                         numeric_attributes, categorical_attributes, selection_numeric_attributes,
                                         selection_categorical_attributes, sql_file_read, sql_connection):
    # # get data selected
    # def select(row):
    #     for att in selection_numeric_attributes:
    #         if pd.isnull(row[att]):
    #             return 0
    #         if not eval(
    #                 str(row[att]) + selection_numeric_attributes[att][0] + str(selection_numeric_attributes[att][1])):
    #             return 0
    #     for att in selection_categorical_attributes:
    #         if pd.isnull(row[att]):
    #             return 0
    #         if row[att] not in selection_categorical_attributes[att]:
    #             return 0
    #     return 1
    # data['satisfy_selection'] = data[selected_attributes].apply(select, axis=1)
    # data_selected = data[data['satisfy_selection'] == 1]

    # execute sql selection
    global data_selected
    num_numeric = 0
    params = dict()
    for att in selection_numeric_attributes:
        num_numeric += 1
        params['numeric'+str(num_numeric)] = selection_numeric_attributes[att][1] # FIXME???

    num_cate = 0
    for att in selection_categorical_attributes:
        num_cate += 1
        params['categorical' + str(num_cate)] = tuple(selection_categorical_attributes[att])

    # params = {
    #     'Param1': "1995-03-10",
    #     'Param2': "1995-03-10",
    #     'Param3': "AUTOMOBILE"
    # }

    cursor = sql_connection.cursor()
    cursor.execute(sql_file_read, params)
    fetch_result = cursor.fetchall()
    data_selected = pd.DataFrame(fetch_result)
    print(data_selected)

    sql_connection.commit()

    # whether satisfy fairness constraint
    for fc in fairness_constraints:
        sensitive_attributes = fc['sensitive_attributes']
        df1 = data_selected[list(sensitive_attributes.keys())]
        df2 = pd.DataFrame([sensitive_attributes])
        data_selected_satisfying_fairness_constraint = df1.merge(df2)
        num = len(data_selected_satisfying_fairness_constraint)
        if not eval(str(num) + fc['symbol'] + str(fc['number'])):
            return False
    return True


def dominate(a, b):
    """
    whether relaxation a dominates b. relaxation has all delta values. it is not a selection condition
    :param a: relaxation, format of sorted table
    :param b: relaxation
    :return: true if a dominates b (a is minimal compared to b), return true if equal
    """
    if a == b:
        return True
    non_zero_a = sum(x != 0 for x in a)
    non_zero_b = sum(x != 0 for x in b)
    if non_zero_a > non_zero_b:
        return False
    length = len(a)
    for i in range(length):
        if abs(a[i]) > abs(b[i]):
            return False
    return True


def update_minimal_refinement(minimal_added_relaxations, r):
    dominated = []
    for mr in minimal_added_relaxations:
        if mr == r:
            return minimal_added_relaxations
        if dominate(mr, r):
            return minimal_added_relaxations
        elif dominate(r, mr):
            dominated.append(mr)
    if len(dominated) > 0:
        minimal_added_relaxations = [x for x in minimal_added_relaxations if x not in dominated]
    minimal_added_relaxations.append(r)
    return minimal_added_relaxations


def transform_refinement_format(this_refinement, numeric_att_domain_to_relax, num_numeric_att,
                                selection_numeric_attributes, numeric_attributes):
    minimal_refinement_values = copy.deepcopy(this_refinement)
    for i in range(num_numeric_att):
        if minimal_refinement_values[i] == -1:
            minimal_refinement_values[i] = 0
        else:
            minimal_refinement_values[i] = minimal_refinement_values[i] - \
                                           selection_numeric_attributes[numeric_attributes[i]][1]
    return minimal_refinement_values


def LatticeTraversal(data, selected_attributes, sensitive_attributes, fairness_constraints,
                     numeric_attributes, categorical_attributes, selection_numeric_attributes,
                     selection_categorical_attributes, sql_file_read, sql_connection, time_limit=5 * 60):
    # whether it's single-direction
    only_smaller_than = True
    only_greater_than = True
    for fc in fairness_constraints:
        if fc['symbol'] == ">=" or fc['symbol'] == ">":
            only_smaller_than = False
        else:
            only_greater_than = False
        if (not only_greater_than) and (not only_smaller_than):
            break

    if only_greater_than:
        return LatticeTraversalGreaterThan(data, selected_attributes, sensitive_attributes, fairness_constraints,
                                           numeric_attributes, categorical_attributes, selection_numeric_attributes,
                                           selection_categorical_attributes, sql_file_read, sql_connection,
                                           time_limit=5 * 60)
    elif only_smaller_than:
        return LatticeTraversalSmallerThan(data, selected_attributes, sensitive_attributes, fairness_constraints,
                                           numeric_attributes, categorical_attributes, selection_numeric_attributes,
                                           selection_categorical_attributes, sql_file_read, sql_connection,
                                           time_limit=5 * 60)
    else:
        return LatticeTraversalBidirectional(data, selected_attributes, sensitive_attributes, fairness_constraints,
                                             numeric_attributes, categorical_attributes, selection_numeric_attributes,
                                             selection_categorical_attributes, sql_file_read, sql_connection,
                                             time_limit=5 * 60)


def LatticeTraversalBidirectional(data, selected_attributes, sensitive_attributes, fairness_constraints,
                                  numeric_attributes, categorical_attributes, selection_numeric_attributes,
                                  selection_categorical_attributes, sql_file_read, sql_connection, time_limit=5 * 60):
    categorical_att_domain_too_remove = []
    for att in categorical_attributes:
        s = [(att, v) for v in selection_categorical_attributes[att]]
        categorical_att_domain_too_remove += s

    categorical_att_domain_too_add = []
    for att in categorical_attributes:
        s = [(att, v) for v in categorical_attributes[att] if v not in selection_categorical_attributes[att]]
        categorical_att_domain_too_add += s

    numeric_att_domain_to_relax = dict()
    for att in numeric_attributes:
        unique_values = data[att].unique().tolist() + [selection_numeric_attributes[att][1]]
        unique_values.sort()  # ascending
        if selection_numeric_attributes[att][0] == ">=":
            unique_values = [x + 1 if x >= selection_numeric_attributes[att][1] else x for x in unique_values]
        elif selection_numeric_attributes[att][0] == ">":
            unique_values = [x - 1 if x < selection_numeric_attributes[att][1] else x for x in unique_values]
        elif selection_numeric_attributes[att][0] == "<=":
            unique_values = [x - 1 if x <= selection_numeric_attributes[att][1] else x for x in unique_values]
        else:  # selection_numeric_attributes[att][0] == "<":
            unique_values = [x + 1 if x > selection_numeric_attributes[att][1] else x for x in unique_values]
        if selection_numeric_attributes[att][1] not in unique_values:
            unique_values.append(selection_numeric_attributes[att][1])
        # FIXME: DO I need to sort unique_values again? The value in originala selection is appended at lasat.
        numeric_att_domain_to_relax[att] = unique_values
    num_numeric_att = len(selection_numeric_attributes)
    num_cate_variables_to_add = len(categorical_att_domain_too_add)
    num_cate_variables_to_remove = len(categorical_att_domain_too_remove)
    # print("categorical_att_domain_too_add:\n", categorical_att_domain_too_add)
    # print("categorical_att_domain_too_remove:\n", categorical_att_domain_too_remove)
    # print("numeric_att_domain_to_relax:\n", numeric_att_domain_to_relax)
    minimal_refinements = []
    if whether_satisfy_fairness_constraints(data, selected_attributes, sensitive_attributes, fairness_constraints,
                                            numeric_attributes, categorical_attributes, selection_numeric_attributes,
                                            selection_categorical_attributes, sql_file_read, sql_connection):
        return [0] * num_numeric_att + [0] * (num_cate_variables_to_add + num_cate_variables_to_remove), \
               numeric_att_domain_to_relax, categorical_att_domain_too_add, categorical_att_domain_too_remove
        # return [{'numeric': selection_numeric_attributes, 'categorical': selection_categorical_attributes}]

    # I need to remember where I was last time
    att_idx = num_numeric_att + num_cate_variables_to_add + num_cate_variables_to_remove
    last_time_selection = [0] * num_numeric_att + [0] * (num_cate_variables_to_add + num_cate_variables_to_remove)
    this_refinement = [numeric_att_domain_to_relax[a][0] for a in numeric_attributes] + \
                      [0] * (num_cate_variables_to_add + num_cate_variables_to_remove)
    new_selection_numeric_attributes = copy.deepcopy(selection_numeric_attributes)
    for k in numeric_attributes:
        new_selection_numeric_attributes[k][1] = numeric_att_domain_to_relax[k][0]
    new_selection_categorical_attributes = copy.deepcopy(selection_categorical_attributes)
    while att_idx >= 0:
        # if time.time() - time1 > time_limit:
        #     break
        if att_idx == num_numeric_att + num_cate_variables_to_add + num_cate_variables_to_remove:
            if whether_satisfy_fairness_constraints(data, selected_attributes, sensitive_attributes,
                                                    fairness_constraints, numeric_attributes, categorical_attributes,
                                                    new_selection_numeric_attributes,
                                                    new_selection_categorical_attributes,
                                                    sql_file_read, sql_connection):
                # print("{} satisfies".format(this_refinement))
                minimal_refinement_values = transform_refinement_format(this_refinement, numeric_att_domain_to_relax,
                                                                        num_numeric_att, selection_numeric_attributes,
                                                                        numeric_attributes)
                minimal_refinements = update_minimal_refinement(minimal_refinements, minimal_refinement_values)
            att_idx -= 1
        if att_idx < num_numeric_att:  # numeric
            if last_time_selection[att_idx] + 1 == len(numeric_att_domain_to_relax[numeric_attributes[att_idx]]):
                last_time_selection[att_idx] = -1
                this_refinement[att_idx] = -1
                new_selection_numeric_attributes[numeric_attributes[att_idx]][1] = \
                    selection_numeric_attributes[numeric_attributes[att_idx]][1]
                att_idx -= 1
                continue
            this_refinement[att_idx] = numeric_att_domain_to_relax[numeric_attributes[att_idx]][
                last_time_selection[att_idx] + 1]
            last_time_selection[att_idx] += 1
            new_selection_numeric_attributes[numeric_attributes[att_idx]][1] = this_refinement[att_idx]
            att_idx += 1
        elif att_idx < num_numeric_att + num_cate_variables_to_add:  # categorical to add
            if last_time_selection[att_idx] == 1:
                last_time_selection[att_idx] = -1
                this_refinement[att_idx] = -1
                new_selection_categorical_attributes[
                    categorical_att_domain_too_add[att_idx - num_numeric_att][0]].remove(
                    categorical_att_domain_too_add[att_idx - num_numeric_att][1])
                att_idx -= 1
                continue
            this_refinement[att_idx] += 1
            last_time_selection[att_idx] += 1
            if this_refinement[att_idx] == 1:
                new_selection_categorical_attributes[
                    categorical_att_domain_too_add[att_idx - num_numeric_att][0]].append(
                    categorical_att_domain_too_add[att_idx - num_numeric_att][1])
            att_idx += 1
        else:  # categorical to remove
            if last_time_selection[att_idx] == 1:
                last_time_selection[att_idx] = -1
                this_refinement[att_idx] = -1
                new_selection_categorical_attributes[
                    categorical_att_domain_too_remove[att_idx - num_numeric_att - num_cate_variables_to_add][0]].append(
                    categorical_att_domain_too_remove[att_idx - num_numeric_att - num_cate_variables_to_add][1])
                att_idx -= 1
                continue
            this_refinement[att_idx] += 1
            last_time_selection[att_idx] += 1
            if this_refinement[att_idx] == 1:
                new_selection_categorical_attributes[
                    categorical_att_domain_too_remove[att_idx - num_numeric_att - num_cate_variables_to_add][0]].remove(
                    categorical_att_domain_too_remove[att_idx - num_numeric_att - num_cate_variables_to_add][1])
            att_idx += 1
    return minimal_refinements, numeric_att_domain_to_relax, categorical_att_domain_too_add, \
           categorical_att_domain_too_remove


# it only considers contraction
def LatticeTraversalSmallerThan(data, selected_attributes, sensitive_attributes, fairness_constraints,
                                numeric_attributes, categorical_attributes, selection_numeric_attributes,
                                selection_categorical_attributes, sql_file_read, sql_connection, time_limit=5 * 60):
    categorical_att_domain_too_remove = []
    for att in categorical_attributes:
        s = [(att, v) for v in selection_categorical_attributes[att]]
        categorical_att_domain_too_remove += s

    numeric_att_domain_to_contract = dict()
    for att in numeric_attributes:
        if selection_numeric_attributes[att][0] == "<" or selection_numeric_attributes[att][0] == "<=":
            unique_values = data[att].unique().tolist()
            unique_values.sort(reverse=True)  # descending
            domain = unique_values
            for idx_domain in range(len(domain)):
                if domain[idx_domain] < selection_numeric_attributes[att][1]:
                    numeric_att_domain_to_contract[att] = [selection_numeric_attributes[att][1]] + domain[idx_domain:]
                    break
        else:
            unique_values = data[att].unique().tolist()
            unique_values.sort()  # ascending
            domain = unique_values
            for idx_domain in range(len(domain)):
                if domain[idx_domain] > selection_numeric_attributes[att][1]:
                    numeric_att_domain_to_contract[att] = [selection_numeric_attributes[att][1]] + domain[idx_domain:]
                    break
    num_numeric_att = len(selection_numeric_attributes)
    num_cate_variables = len(categorical_att_domain_too_remove)
    print("categorical_att_domain_too_add:\n", categorical_att_domain_too_remove)
    print("numeric_att_domain_to_relax:\n", numeric_att_domain_to_contract)
    minimal_refinements = []
    if whether_satisfy_fairness_constraints(data, selected_attributes, sensitive_attributes, fairness_constraints,
                                            numeric_attributes, categorical_attributes, selection_numeric_attributes,
                                            selection_categorical_attributes, sql_file_read, sql_connection):
        return [0] * num_numeric_att + [0] * num_cate_variables, numeric_att_domain_to_contract, \
           [], categorical_att_domain_too_remove

    # I need to remember where I was last time
    att_idx = num_numeric_att + num_cate_variables
    last_time_selection = [0] * num_numeric_att + [0] * num_cate_variables
    this_refinement = [numeric_att_domain_to_contract[a][0] for a in numeric_attributes] + [0] * num_cate_variables
    new_selection_numeric_attributes = copy.deepcopy(selection_numeric_attributes)
    new_selection_categorical_attributes = copy.deepcopy(selection_categorical_attributes)
    while att_idx >= 0:
        # if time.time() - time1 > time_limit:
        #     break
        if att_idx == num_numeric_att + num_cate_variables:
            if whether_satisfy_fairness_constraints(data, selected_attributes, sensitive_attributes,
                                                    fairness_constraints, numeric_attributes, categorical_attributes,
                                                    new_selection_numeric_attributes,
                                                    new_selection_categorical_attributes,
                                                    sql_file_read, sql_connection):
                minimal_refinement_values = transform_refinement_format(this_refinement, numeric_att_domain_to_contract,
                                                                        num_numeric_att, selection_numeric_attributes,
                                                                        numeric_attributes)
                minimal_refinements = update_minimal_refinement(minimal_refinements, minimal_refinement_values)
            att_idx -= 1
        if att_idx < num_numeric_att:  # numeric
            if last_time_selection[att_idx] + 1 == len(numeric_att_domain_to_contract[numeric_attributes[att_idx]]):
                last_time_selection[att_idx] = -1
                this_refinement[att_idx] = -1
                new_selection_numeric_attributes[numeric_attributes[att_idx]][1] = \
                    selection_numeric_attributes[numeric_attributes[att_idx]][1]
                att_idx -= 1
                continue
            this_refinement[att_idx] = numeric_att_domain_to_contract[numeric_attributes[att_idx]][
                last_time_selection[att_idx] + 1]
            last_time_selection[att_idx] += 1
            new_selection_numeric_attributes[numeric_attributes[att_idx]][1] = this_refinement[att_idx]
            att_idx += 1
        else:  # categorical
            """
            -1 means waiting to assign a value
            0 means keeps original selections unchanged
            1 means remove this value
            """
            if last_time_selection[att_idx] == 1:
                last_time_selection[att_idx] = -1
                this_refinement[att_idx] = -1
                new_selection_categorical_attributes[
                    categorical_att_domain_too_remove[att_idx - num_numeric_att][0]].append(
                    categorical_att_domain_too_remove[att_idx - num_numeric_att][1])
                att_idx -= 1
                continue
            this_refinement[att_idx] += 1
            last_time_selection[att_idx] += 1
            if this_refinement[att_idx] == 1:
                new_selection_categorical_attributes[
                    categorical_att_domain_too_remove[att_idx - num_numeric_att][0]].remove(
                    categorical_att_domain_too_remove[att_idx - num_numeric_att][1])
            att_idx += 1
    return minimal_refinements, numeric_att_domain_to_contract, [], categorical_att_domain_too_remove


# it only considers relaxation
def LatticeTraversalGreaterThan(data, selected_attributes, sensitive_attributes, fairness_constraints,
                                numeric_attributes, categorical_attributes, selection_numeric_attributes,
                                selection_categorical_attributes, sql_file_read, sql_connection, time_limit=5 * 60):
    categorical_att_domain_too_add = []
    for att in categorical_attributes:
        s = [(att, v) for v in categorical_attributes[att] if v not in selection_categorical_attributes[att]]
        categorical_att_domain_too_add += s

    numeric_att_domain_to_relax = dict()
    for att in numeric_attributes:
        if selection_numeric_attributes[att][0] == ">" or selection_numeric_attributes[att][0] == ">=":
            unique_values = data[att].unique().tolist()
            unique_values.sort(reverse=True)  # descending
            domain = unique_values
            for idx_domain in range(len(domain)):
                if domain[idx_domain] < selection_numeric_attributes[att][1]:
                    numeric_att_domain_to_relax[att] = [selection_numeric_attributes[att][1]] + domain[idx_domain:]
                    break
        else:
            unique_values = data[att].unique().tolist()
            unique_values.sort()  # ascending
            domain = unique_values
            for idx_domain in range(len(domain)):
                if domain[idx_domain] > selection_numeric_attributes[att][1]:
                    numeric_att_domain_to_relax[att] = [selection_numeric_attributes[att][1]] + domain[idx_domain:]
                    break

    num_numeric_att = len(selection_numeric_attributes)
    num_cate_variables = len(categorical_att_domain_too_add)
    print("categorical_att_domain_too_add:\n", categorical_att_domain_too_add)
    print("numeric_att_domain_to_relax:\n", numeric_att_domain_to_relax)
    minimal_refinements = []
    if whether_satisfy_fairness_constraints(data, selected_attributes, sensitive_attributes, fairness_constraints,
                                            numeric_attributes, categorical_attributes, selection_numeric_attributes,
                                            selection_categorical_attributes, sql_file_read, sql_connection):
        return [0] * num_numeric_att + [0] * num_cate_variables, numeric_att_domain_to_relax, \
               categorical_att_domain_too_add, []
    # I need to remember where I was last time
    att_idx = num_numeric_att + num_cate_variables
    last_time_selection = [0] * num_numeric_att + [0] * num_cate_variables
    this_refinement = [numeric_att_domain_to_relax[a][0] for a in numeric_attributes] + [0] * num_cate_variables
    new_selection_numeric_attributes = copy.deepcopy(selection_numeric_attributes)
    new_selection_categorical_attributes = copy.deepcopy(selection_categorical_attributes)
    while att_idx >= 0:
        # if time.time() - time1 > time_limit:
        #     break
        if att_idx == num_numeric_att + num_cate_variables:
            if whether_satisfy_fairness_constraints(data, selected_attributes, sensitive_attributes,
                                                    fairness_constraints, numeric_attributes, categorical_attributes,
                                                    new_selection_numeric_attributes,
                                                    new_selection_categorical_attributes,
                                                    sql_file_read, sql_connection):
                minimal_refinement_values = transform_refinement_format(this_refinement, numeric_att_domain_to_relax,
                                                                        num_numeric_att, selection_numeric_attributes,
                                                                        numeric_attributes)
                minimal_refinements = update_minimal_refinement(minimal_refinements, minimal_refinement_values)
            att_idx -= 1
        if att_idx < num_numeric_att:  # numeric
            if last_time_selection[att_idx] + 1 == len(numeric_att_domain_to_relax[numeric_attributes[att_idx]]):
                last_time_selection[att_idx] = -1
                this_refinement[att_idx] = -1
                new_selection_numeric_attributes[numeric_attributes[att_idx]][1] = \
                    selection_numeric_attributes[numeric_attributes[att_idx]][1]
                att_idx -= 1
                continue
            this_refinement[att_idx] = numeric_att_domain_to_relax[numeric_attributes[att_idx]][
                last_time_selection[att_idx] + 1]
            last_time_selection[att_idx] += 1
            new_selection_numeric_attributes[numeric_attributes[att_idx]][1] = this_refinement[att_idx]
            att_idx += 1
        else:  # categorical
            """
            -1 means waiting to assign a value
            0 means keeps original selections unchanged
            1 means add this value
            """
            if last_time_selection[att_idx] == 1:
                last_time_selection[att_idx] = -1
                this_refinement[att_idx] = -1
                new_selection_categorical_attributes[
                    categorical_att_domain_too_add[att_idx - num_numeric_att][0]].remove(
                    categorical_att_domain_too_add[att_idx - num_numeric_att][1])
                att_idx -= 1
                continue
            this_refinement[att_idx] += 1
            last_time_selection[att_idx] += 1
            if this_refinement[att_idx] == 1:
                new_selection_categorical_attributes[
                    categorical_att_domain_too_add[att_idx - num_numeric_att][0]].append(
                    categorical_att_domain_too_add[att_idx - num_numeric_att][1])
            att_idx += 1
    return minimal_refinements, numeric_att_domain_to_relax, categorical_att_domain_too_add, []


########################################################################################################################



def FindMinimalRefinement(data, selection_file, sql_file_read, sql_connection):

    with open(selection_file) as f:
        info = json.load(f)

    sensitive_attributes = info['all_sensitive_attributes']
    fairness_constraints = info['fairness_constraints']
    selection_numeric_attributes = info['selection_numeric_attributes']
    selection_categorical_attributes = info['selection_categorical_attributes']
    numeric_attributes = list(selection_numeric_attributes.keys())
    categorical_attributes = info['categorical_attributes']
    selected_attributes = list(categorical_attributes.keys()) + numeric_attributes
    print("selected_attributes", selected_attributes)

    pd.set_option('display.float_format', '{:.3f}'.format)

    time1 = time.time()
    minimal_added_refinements, numeric_att_domain_to_relax, categorical_att_domain_too_add, categorical_att_domain_too_remove \
        = LatticeTraversal(data, selected_attributes, sensitive_attributes, fairness_constraints,
                           numeric_attributes, categorical_attributes, selection_numeric_attributes,
                           selection_categorical_attributes, sql_file_read, sql_connection, time_limit=5 * 60)

    print("minimal_added_relaxations:{}".format(minimal_added_refinements))


    minimal_refinements = transform_to_refinement_format(minimal_added_refinements, numeric_attributes,
                                                         selection_numeric_attributes, selection_categorical_attributes,
                                                         numeric_att_domain_to_relax, categorical_att_domain_too_add,
                                                         categorical_att_domain_too_remove)

    time2 = time.time()
    return minimal_refinements, minimal_added_refinements, time2 - time1




data_file = r"../InputData/Pipelines/healthcare/incomeK/before_selection_incomeK.csv"
selection_file = r"../InputData/Pipelines/healthcare/incomeK/relaxation/selection2.json"


# data_file = r"toy_examples/example2.csv"
# selection_file = r"toy_examples/selection2.json"

minimal_refinements, minimal_added_refinements, running_time = FindMinimalRefinement(data_file, selection_file)

print(*minimal_refinements, sep="\n")
print("running time = {}".format(running_time))

