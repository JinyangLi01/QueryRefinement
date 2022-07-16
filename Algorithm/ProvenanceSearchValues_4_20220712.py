"""
executable but only for relaxation/contraction
Pure relaxations/contractions and refinements are treated differently.
Use recursion


Difference from 2:
2 uses recursion which is not appreciated

Here I use loop

Bug: due to optimization, the positions is incorrect since some parts of the columns that
are already checked are deleted.

Fix this bug by tightening the last fixed column after binary search


"""

import copy
from typing import List, Any
import numpy as np
import pandas as pd
import time
from intbitset import intbitset
import json
from Algorithm import LatticeTraversal_2_2022405 as lt




def num2string(pattern):
    st = ''
    for i in pattern:
        if i != -1:
            st += str(i)
        st += '|'
    st = st[:-1]
    return st



def subtract_provenance(data, selected_attributes, sensitive_attributes, fairness_constraints,
                        numeric_attributes, categorical_attributes, selection_numeric_attributes,
                        selection_categorical_attributes):
    """
Get provenance expressions
    :param all_sensitive_attributes: list of all att involved in fairness constraints
    :param fairness_constraints: [{'Gender': 'F', 'symbol': '>=', 'number': 3}]
    :param data: dataframe
    :param selected_attributes: attributes in selection conditions
    :return: a list of dictionaries
    """
    fairness_constraints_provenance_greater_than = []
    fairness_constraints_provenance_smaller_than = []
    data['protected_greater_than'] = 0
    data['protected_smaller_than'] = 0
    data['satisfy'] = 0

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

    # if one direction, evaluate whether a row satisfies selection conditions
    def test_satisfying_rows(row):
        terms = row[selected_attributes].to_dict()
        for k in terms:
            if k in selection_numeric_attributes:
                if not eval(
                        str(terms[k]) + selection_numeric_attributes[k][0] + str(selection_numeric_attributes[k][1])):
                    return 0
            else:
                if terms[k] not in selection_categorical_attributes[k]:
                    return 0
        return 1

    if only_greater_than:
        data['satisfy'] = data.apply(test_satisfying_rows, axis=1)
        all_relevant_attributes = sensitive_attributes + selected_attributes + \
                                  ['protected_greater_than', 'protected_smaller_than', 'satisfy']
        data = data[all_relevant_attributes]
        data = data.groupby(all_relevant_attributes, dropna=False, sort=False).size().reset_index(name='occurrence')

        def get_provenance_relax_only(row, fc_dic, fc):
            sensitive_att_of_fc = list(fc["sensitive_attributes"].keys())
            sensitive_values_of_fc = {k: fc["sensitive_attributes"][k] for k in sensitive_att_of_fc}
            fairness_value_of_row = row[sensitive_att_of_fc]
            if sensitive_values_of_fc == fairness_value_of_row.to_dict():
                if row['satisfy'] == 1:
                    fc_dic['number'] -= row['occurrence']
                else:
                    terms = row[selected_attributes]
                    term_dic = terms.to_dict()
                    term_dic['occurrence'] = row['occurrence']
                    fc_dic['provenance_expression'].append(term_dic)
                    row['protected_greater_than'] = 1
            return row

        for fc in fairness_constraints:
            fc_dic = dict()
            fc_dic['symbol'] = fc['symbol']
            fc_dic['number'] = fc['number']
            fc_dic['provenance_expression'] = []
            data = data[all_relevant_attributes + ['occurrence']].apply(get_provenance_relax_only,
                                                                        args=(fc_dic, fc),
                                                                        axis=1)
            fairness_constraints_provenance_greater_than.append(fc_dic)
        data = data[data['satisfy'] == 0]
        data_rows_greater_than = data[data['protected_greater_than'] == 1]
        data_rows_smaller_than = data[data['protected_smaller_than'] == 1]
        return fairness_constraints_provenance_greater_than, fairness_constraints_provenance_smaller_than, \
               data_rows_greater_than, data_rows_smaller_than, only_greater_than, only_smaller_than

    elif only_smaller_than:
        data['satisfy'] = data.apply(test_satisfying_rows, axis=1)

    all_relevant_attributes = sensitive_attributes + selected_attributes + \
                              ['protected_greater_than', 'protected_smaller_than', 'satisfy']
    data = data[all_relevant_attributes]
    data = data.groupby(all_relevant_attributes, dropna=False, sort=False).size().reset_index(name='occurrence')

    def get_provenance(row, fc_dic, fc, protected_greater_than):
        sensitive_att_of_fc = list(fc["sensitive_attributes"].keys())
        sensitive_values_of_fc = {k: fc["sensitive_attributes"][k] for k in sensitive_att_of_fc}
        fairness_value_of_row = row[sensitive_att_of_fc]
        if sensitive_values_of_fc == fairness_value_of_row.to_dict():
            if only_greater_than and row['satisfy'] == 1:
                fc_dic['number'] -= row['occurrence']
            elif not (only_smaller_than and row['satisfy'] == 0):
                terms = row[selected_attributes]
                term_dic = terms.to_dict()
                term_dic['occurrence'] = row['occurrence']
                fc_dic['provenance_expression'].append(term_dic)
            if protected_greater_than:
                row['protected_greater_than'] = 1
            else:
                row['protected_smaller_than'] = 1
        return row

    for fc in fairness_constraints:
        fc_dic = dict()
        fc_dic['symbol'] = fc['symbol']
        fc_dic['number'] = fc['number']
        fc_dic['provenance_expression'] = []
        data = data[all_relevant_attributes + ['occurrence']].apply(get_provenance,
                                                                    args=(fc_dic,
                                                                          fc,
                                                                          (fc['symbol'] == ">" or
                                                                           fc[
                                                                               'symbol'] == ">=")),
                                                                    axis=1)

        if fc_dic['symbol'] == "<" or fc_dic['symbol'] == "<=":
            fairness_constraints_provenance_smaller_than.append(fc_dic)
        else:
            fairness_constraints_provenance_greater_than.append(fc_dic)
    # if one direction, remove rows that already satisfy/dissatisfy selection conditions
    if only_smaller_than:
        data = data[data['satisfy'] == 1]
    # only get rows that are envolved w.r.t. fairness constraint
    data_rows_greater_than = data[data['protected_greater_than'] == 1]
    data_rows_smaller_than = data[data['protected_smaller_than'] == 1]

    return fairness_constraints_provenance_greater_than, fairness_constraints_provenance_smaller_than, \
           data_rows_greater_than, data_rows_smaller_than, only_greater_than, only_smaller_than




def build_PVT_relax_only(data, selected_attributes, numeric_attributes,
                         categorical_attributes, selection_numeric, selection_categorical,
                         sensitive_attributes, fairness_constraints,
                         fairness_constraints_provenance_greater_than,
                         fairness_constraints_provenance_smaller_than,
                         data_rows_greater_than, data_rows_smaller_than
                         ):
    """
    to build the sorted table
    :param fairness_constraints_provenance_greater_than:
    :param fairness_constraints_provenance_smaller_than:
    :param data_rows_smaller_than:
    :param data_rows_greater_than:
    :param selected_attributes:
    :param data: dataframe
    :param numeric_attributes: list of names of numeric attributes [city, major, state]
    :param categorical_attributes: dictionary: {city: [domain of city], major: [domain of major]}
    :param selection_numeric: dictionary: {grade:[80, >], age:[30, <], hours: [100, <=]}
    :param selection_categorical: dictionary: {city: [accepted cities], major: [accepted majors]}
    :return: return the whole sorted table, including rows that already satisfy the selection conditions;
            also return delta table
    """
    PVT_head = numeric_attributes.copy()
    for att, domain in categorical_attributes.items():
        for value in domain:
            if value in selection_categorical[att]:
                continue
            else:
                col = att + "_" + value
                PVT_head.append(col)

    # build delta table
    def iterrow(row, greater_than=True):  # greater than is symbol in fairness constraint (relaxation term)
        nonlocal possible_values_sets
        for att in numeric_attributes:
            if not eval(str(row[att]) + selection_numeric[att][0] + str(selection_numeric[att][1])):
                possible_values_sets[att].add(row[att])

    data_rows_greater_than = data_rows_greater_than.drop_duplicates(
        subset=selected_attributes,
        keep='first').reset_index(drop=True)
    possible_values_sets = {x: set() for x in PVT_head}
    for att in selection_numeric:
        possible_values_sets[att].add(selection_numeric[att][1])
    data_rows_greater_than.apply(iterrow, args=(True,), axis=1)

    possible_values_lists = {x: list(possible_values_sets[x]) for x in possible_values_sets}
    for att in PVT_head:
        if att in selection_numeric:
            if selection_numeric[att][0] == '>' or selection_numeric[att][0] == '>=':
                possible_values_lists[att].sort(reverse=True)
            else:
                possible_values_lists[att].sort()
        else:
            possible_values_lists[att] = [0, 1]
    # print("possible_values_lists:\n", possible_values_lists)
    possible_value_table = pd.DataFrame({key: pd.Series(value) for key, value in possible_values_lists.items()})
    print("possible_value_table:\n", possible_value_table)
    possible_value_table = possible_value_table.drop_duplicates().reset_index(drop=True)
    categorical_att_columns = [item for item in PVT_head if item not in numeric_attributes]
    max_index_PVT = [len(value) - 1 for value in possible_values_lists.values()]
    return possible_value_table, PVT_head, categorical_att_columns, max_index_PVT


def build_PVT_contract_only(data, selected_attributes, numeric_attributes,
                            categorical_attributes, selection_numeric, selection_categorical,
                            sensitive_attributes, fairness_constraints,
                            fairness_constraints_provenance_greater_than,
                            fairness_constraints_provenance_smaller_than,
                            data_rows_greater_than, data_rows_smaller_than
                            ):
    """
    to build the sorted table
    :param fairness_constraints_provenance_greater_than:
    :param fairness_constraints_provenance_smaller_than:
    :param data_rows_smaller_than:
    :param data_rows_greater_than:
    :param selected_attributes:
    :param data: dataframe
    :param numeric_attributes: list of names of numeric attributes [city, major, state]
    :param categorical_attributes: dictionary: {city: [domain of city], major: [domain of major]}
    :param selection_numeric: dictionary: {grade:[80, >], age:[30, <], hours: [100, <=]}
    :param selection_categorical: dictionary: {city: [accepted cities], major: [accepted majors]}
    :return: return the whole sorted table, including rows that already satisfy the selection conditions;
            also return delta table
    """

    PVT_head = numeric_attributes.copy()
    for att, domain in categorical_attributes.items():
        for value in domain:
            if value in selection_categorical[att]:
                continue
            else:
                PVT_head.append(att + "_" + value)

    # build delta table
    def iterrow(row, smaller_than=True):  # greater than is symbol in fairness constraint (relaxation term)
        nonlocal possible_values_sets
        for att in numeric_attributes:
            if eval(str(row[att]) + selection_numeric[att][0] + str(selection_numeric[att][1])):
                possible_values_sets[att].add(row[att])

    data_rows_smaller_than = data_rows_smaller_than.drop_duplicates(
        subset=selected_attributes,
        keep='first').reset_index(drop=True)
    possible_values_sets = {x: set() for x in PVT_head}
    for att in selection_numeric:
        possible_values_sets[att].add(selection_numeric[att][1])
    data_rows_smaller_than.apply(iterrow, args=(True,), axis=1)

    possible_values_lists = {x: list(possible_values_sets[x]) for x in possible_values_sets}
    for att in PVT_head:
        if att in selection_numeric:
            if selection_numeric[att][0] == '<' or selection_numeric[att][0] == '<=':
                possible_values_lists[att].sort(reverse=True)
            else:
                possible_values_lists[att].sort()
        else:
            possible_values_lists[att] = [0, 1]
    # print("possible_values_lists:\n", possible_values_lists)
    possible_value_table = pd.DataFrame({key: pd.Series(value) for key, value in possible_values_lists.items()})
    print("possible_value_table:\n", possible_value_table)
    possible_value_table = possible_value_table.drop_duplicates().reset_index(drop=True)
    categorical_att_columns = [item for item in PVT_head if item not in numeric_attributes]
    max_index_PVT = [len(value) - 1 for value in possible_values_lists.values()]
    return possible_value_table, PVT_head, categorical_att_columns, max_index_PVT



def assign_to_provenance_relax_only(value_assignment, numeric_attributes, categorical_attributes, selection_numeric,
                                    selection_categorical, columns_delta_table, num_columns,
                                    fairness_constraints_provenance_greater_than):
    # greater than
    for fc in fairness_constraints_provenance_greater_than:
        sum = 0
        satisfy_this_fairness_constraint = False
        for pe in fc['provenance_expression']:
            fail = False
            for att in pe:
                if att == 'occurrence':
                    continue
                if pd.isnull(pe[att]):
                    fail = True
                    break
                if att in numeric_attributes:
                    if att not in value_assignment.keys():
                        continue
                    if selection_numeric[att][0] == ">=" or selection_numeric[att][0] == ">":
                        if eval(str(pe[att]) + selection_numeric[att][0] + str(value_assignment[att])):
                            continue
                        else:
                            fail = True
                            break
                    else:
                        if eval(str(pe[att]) + selection_numeric[att][0] + str(value_assignment[att])):
                            continue
                        else:
                            fail = True
                            break
                else:  # att in categorical
                    column_name = att + "_" + pe[att]
                    if column_name not in columns_delta_table:
                        continue
                    if column_name not in value_assignment.keys():
                        continue
                    if pe[att] in selection_categorical[att]:
                        if 1 + value_assignment[column_name] == 1:
                            continue
                        else:
                            fail = True
                            break
                    else:
                        if value_assignment[column_name] == 1:
                            continue
                        else:
                            fail = True
                            break
            if not fail:
                sum += pe['occurrence']
                if eval(str(sum) + fc['symbol'] + str(fc['number'])):
                    satisfy_this_fairness_constraint = True
                    break
        if not satisfy_this_fairness_constraint:
            return False
    return True


def assign_to_provenance(value_assignment, numeric_attributes, categorical_attributes, selection_numeric,
                         selection_categorical, columns_delta_table, num_columns,
                         fairness_constraints_provenance_greater_than,
                         fairness_constraints_provenance_smaller_than):
    va_dict = dict(zip(columns_delta_table, value_assignment))
    if value_assignment == [0, 4, 1, 1, 0]:
        print("value_assignment = {}".format(value_assignment))

    # va_dict = value_assignment.to_dict()
    # greater than

    def assign(fairness_constraints_provenance, relaxation=True):
        for fc in fairness_constraints_provenance:
            sum = 0
            satisfy_this_fairness_constraint = not relaxation
            for pe in fc['provenance_expression']:
                fail = False
                for att in pe:
                    if att == 'occurrence':
                        continue
                    if pd.isnull(pe[att]):
                        fail = True
                        break
                    if att in numeric_attributes:
                        if selection_numeric[att][0] == ">=" or selection_numeric[att][0] == ">":
                            after_refinement = selection_numeric[att][1] - va_dict[att]
                            if eval(str(pe[att]) + selection_numeric[att][0] + str(after_refinement)):
                                continue
                            else:
                                fail = True
                                break
                        else:
                            after_refinement = selection_numeric[att][1] + va_dict[att]
                            if eval(str(pe[att]) + selection_numeric[att][0] + str(after_refinement)):
                                continue
                            else:
                                fail = True
                                break
                    else:  # att in categorical
                        column_name = att + "_" + pe[att]
                        if column_name not in columns_delta_table:
                            continue
                        if pe[att] in selection_categorical[att]:
                            if 1 + va_dict[column_name] == 1:
                                continue
                            else:
                                fail = True
                                break
                        else:
                            if va_dict[column_name] == 1:
                                continue
                            else:
                                fail = True
                                break
                if not fail:
                    sum += pe['occurrence']
                    if relaxation:
                        if eval(str(sum) + fc['symbol'] + str(fc['number'])):
                            satisfy_this_fairness_constraint = True
                            break
                    else:
                        if not eval(str(sum) + fc['symbol'] + str(fc['number'])):
                            satisfy_this_fairness_constraint = False
                            break
            if not satisfy_this_fairness_constraint:
                return False
        return True

    survive = assign(fairness_constraints_provenance_greater_than, relaxation=True)
    if not survive:
        return False
    survive = assign(fairness_constraints_provenance_smaller_than, relaxation=False)
    return survive


def get_relaxation(terms, delta_table):
    """
To get skyline of all terms in list terms
    :param terms: list of indices of terms. [1,3,5]
    :param delta_table: delta table returned by func build_sorted_table()
    :return: return Ture or false whether terms can have a legitimate value assignment .
    """
    column_names = delta_table.columns.tolist()
    value_assignment = delta_table[column_names].loc[terms].max().tolist()
    return value_assignment


def get_refinement(terms, delta_table, delta_table_multifunctional):
    """
To get skyline of all terms in list terms
    :param terms: list of indices of terms. [1,3,5]
    :param delta_table: delta table returned by func build_sorted_table()
    :return: return Ture or false whether terms can have a legitimate value assignment .
    """
    column_names = delta_table.columns.tolist()

    column_names.remove('relaxation_term')
    num_col = len(column_names) + 1

    value_assignments = [[]]
    mark_satisfied_terms = [0]

    rows_to_compare = delta_table.loc[terms]
    rows_to_compare_with_multifunctional = delta_table_multifunctional.loc[terms]
    rows_to_compare_indices = rows_to_compare.index.tolist()

    rows_to_compare.round(2)
    rows_to_compare_with_multifunctional.round(2)

    all_included = 0
    for i in rows_to_compare_indices:
        all_included = (1 << i) | all_included
    for i in range(num_col):
        if i == num_col - 1:
            num_result = len(value_assignments)
            j = 0
            while j < num_result:
                if mark_satisfied_terms[j] != all_included:
                    del value_assignments[j]
                    del mark_satisfied_terms[j]
                    num_result -= 1
                else:
                    j += 1
            return (len(value_assignments) != 0), value_assignments
        col = column_names[i]
        max_in_col = rows_to_compare[col].max()
        if max_in_col > 0:
            #  term_w_max = rows_to_compare[col].idxmax(axis=0)
            for va in value_assignments:
                va.append(max_in_col)
            positive_terms_int = 0
            indices = rows_to_compare[rows_to_compare[col] > 0].index.tolist()
            for d in indices:
                positive_terms_int = (1 << d) | positive_terms_int
            for k in range(len(mark_satisfied_terms)):
                mark_satisfied_terms[k] |= positive_terms_int
            continue
        unique_values = rows_to_compare[col].drop_duplicates()
        non_zeros = unique_values[unique_values < 0].index.tolist()
        relaxation_terms_idx = rows_to_compare[rows_to_compare['relaxation_term']].index.tolist()
        if len(non_zeros) == 0:
            for v in value_assignments:
                v.append(0)
            continue
        mark_satisfied_terms_new = []
        value_assignments_new = []
        for n in non_zeros:
            positive_terms_int = (1 << n)  # | positive_terms_int
            for k in range(len(mark_satisfied_terms)):
                if mark_satisfied_terms[k] & positive_terms_int == 0:
                    maximum_to_contract = rows_to_compare_with_multifunctional[col].loc[relaxation_terms_idx].min()
                    maximum_to_contract = round(maximum_to_contract, 2)
                    b = round(rows_to_compare.loc[n][col], 2)
                    if maximum_to_contract == 0 or maximum_to_contract <= b:
                        v_ = value_assignments[k].copy()
                        v_.append(rows_to_compare.loc[n][col])
                        value_assignments_new.append(v_)
                        covered = [x for x in non_zeros if rows_to_compare.loc[x][col] >= rows_to_compare.loc[n][col]]
                        to_append = mark_satisfied_terms[k]
                        for c in covered:
                            to_append |= 1 << c
                        mark_satisfied_terms_new.append(to_append)

        for s in value_assignments:
            s.append(0)
            value_assignments_new.append(s)
        mark_satisfied_terms_new = mark_satisfied_terms_new + mark_satisfied_terms
        value_assignments = value_assignments_new.copy()
        mark_satisfied_terms = mark_satisfied_terms_new.copy()

    return True, value_assignments


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



def dominated_by_minimal_set(minimal_added_relaxations, r):
    for mr in minimal_added_relaxations:
        if mr == r:
            return True
        if dominate(mr, r):
            return True
    return False


def transform_refinement_format(this_refinement, num_numeric_att,
                                selection_numeric_attributes, numeric_attributes):
    minimal_added_refinement_values = copy.deepcopy(this_refinement)
    for i in range(num_numeric_att):
        if minimal_added_refinement_values[i] == -1:
            minimal_added_refinement_values[i] = 0
        else:
            minimal_added_refinement_values[i] = minimal_added_refinement_values[i] - \
                                                 selection_numeric_attributes[numeric_attributes[i]][1]
    return minimal_added_refinement_values


def update_minimal_relaxation(minimal_added_relaxations, r):
    dominated = []
    for mr in minimal_added_relaxations:
        if mr == r:
            return True, minimal_added_relaxations
        if dominate(mr, r):
            return False, minimal_added_relaxations
        elif dominate(r, mr):
            dominated.append(mr)
    if len(dominated) > 0:
        minimal_added_relaxations = [x for x in minimal_added_relaxations if x not in dominated]
    minimal_added_relaxations.append(r)
    return True, minimal_added_relaxations



def position_dominate(p1, p2):
    p1_higher = False
    p2_higher = False
    length = len(p1)
    for i in range(length):
        if p1[i] < p2[i]:
            p1_higher = True
        elif p2[i] < p1[i]:
            p2_higher = True
    if p1_higher and not p2_higher:
        return True
    else:
        return False


def update_minimal_relaxation_and_position(minimal_refinements, minimal_refinements_positions,
                                           full_value_assignment, full_value_assignment_positions, shifted_length):
    num = len(minimal_refinements_positions)
    dominated = []
    dominated_refinements = []
    full_value_assignment_positions = [full_value_assignment_positions[i] + shifted_length[i] for i in range(len(shifted_length))]
    for i in range(num):
        p = minimal_refinements_positions[i]
        if position_dominate(p, full_value_assignment_positions):
            return minimal_refinements, minimal_refinements_positions
        elif position_dominate(full_value_assignment_positions, p):
            dominated.append(p)
            to_remove_refinement = minimal_refinements[i]
            dominated_refinements.append(to_remove_refinement)
    minimal_refinements_positions = [p for p in minimal_refinements_positions if p not in dominated]
    minimal_refinements_positions.append(full_value_assignment_positions)
    minimal_refinements = [p for p in minimal_refinements if p not in dominated_refinements]
    minimal_refinements.append(full_value_assignment)
    return minimal_refinements, minimal_refinements_positions


def searchPVT(PVT, PVT_head, numeric_attributes, categorical_attributes,
              selection_numeric, selection_categorical, num_columns, fairness_constraints_provenance_greater_than,
              full_PVT, full_PVT_head, max_index_PVT,
              checked_assignments_satisfying, checked_assignments_not_satisfying):
    PVT_stack = [PVT]
    PVT_head_stack = [PVT_head]
    max_index_PVT_stack = [max_index_PVT]
    parent_PVT_stack = [pd.DataFrame()]
    parent_PVT_head_stack = [[]]
    parent_max_index_PVT_stack = [pd.DataFrame()]
    col_idx_in_parent_PVT_stack = [0]
    idx_in_this_col_in_parent_PVT_stack = [0]
    find_relaxation = {x: [] for x in range(1, len(full_PVT_head) + 1)}
    fixed_value_assignments_stack = [{}]
    fixed_value_assignments_positions_stack = [{}]
    fixed_value_assignments_to_tighten_stack = [[]]
    left_side_binary_search_stack = [0]
    shifted_length_stack = [[0]*num_columns]
    to_put_to_stack = []
    minimal_refinements = []  # result set
    minimal_refinements_positions = []  # positions of result set
    fixed_value_assignments = {}
    fixed_value_assignments_positions = {}


    while PVT_stack:
        PVT = PVT_stack.pop()
        # if len(PVT) == 0:
        #     break
        PVT_head = PVT_head_stack.pop()
        max_index_PVT = max_index_PVT_stack.pop()
        parent_PVT = parent_PVT_stack.pop()
        parent_PVT_head = parent_PVT_head_stack.pop()
        parent_max_index_PVT = parent_max_index_PVT_stack.pop()
        col_idx_in_parent_PVT = col_idx_in_parent_PVT_stack.pop()
        idx_in_this_col_in_parent_PVT = idx_in_this_col_in_parent_PVT_stack.pop()
        fixed_value_assignments = fixed_value_assignments_stack.pop()
        fixed_value_assignments_positions = fixed_value_assignments_positions_stack.pop()
        shifted_length = shifted_length_stack.pop()
        find_bounding_relaxation = False
        num_columns = len(PVT_head)
        last_in_this_level = False
        print("==========================  searchPVT  ========================== ")
        print("PVT_head: {}".format(PVT_head))
        print("PVT:\n{}".format(PVT))
        print("fixed_value_assignments: {}".format(fixed_value_assignments))
        print("shifted_length: {}".format(shifted_length))

        satisfying_row_id = 0
        new_value_assignment = []
        last_satisfying_new_value_assignment = []
        full_value_assignment = {}
        last_satisfying_full_value_assignment = {}
        last_satisfying_bounding_relaxation_location = []
        left = left_side_binary_search_stack.pop()
        print("left = {}".format(left))
        right = max(max_index_PVT)

        # binary search can't use apply
        while left <= right:
            print("left = {}, right={}".format(left, right))
            cur_row_id = int((right + left) / 2)
            new_bounding_relaxation_location = [cur_row_id if cur_row_id < x else x for x in max_index_PVT]
            new_value_assignment = [PVT.iloc[new_bounding_relaxation_location[x], x] for x in range(len(PVT_head))]
            full_value_assignment = dict(zip(PVT_head, new_value_assignment))
            full_value_assignment = {**full_value_assignment, **fixed_value_assignments}
            print("value_assignment: ", full_value_assignment)
            full_value_assignment_str = num2string([full_value_assignment[k] for k in full_PVT_head])
            if full_value_assignment_str in checked_assignments_satisfying:
                print("{} satisfies constraints".format(full_value_assignment))
                satisfying_row_id = cur_row_id
                right = cur_row_id - 1
                last_satisfying_full_value_assignment = full_value_assignment
                last_satisfying_new_value_assignment = new_value_assignment
                last_satisfying_bounding_relaxation_location = new_bounding_relaxation_location
                find_bounding_relaxation = True
            elif full_value_assignment_str in checked_assignments_not_satisfying:
                print("{} doesn't satisfy constraints".format(full_value_assignment))
                left = cur_row_id + 1
            elif assign_to_provenance_relax_only(full_value_assignment, numeric_attributes, categorical_attributes,
                                               selection_numeric, selection_categorical, full_PVT_head,
                                               num_columns, fairness_constraints_provenance_greater_than):
                checked_assignments_satisfying.append(full_value_assignment_str)
                print("{} satisfies constraints".format(full_value_assignment))
                satisfying_row_id = cur_row_id
                right = cur_row_id - 1
                last_satisfying_full_value_assignment = full_value_assignment
                last_satisfying_new_value_assignment = new_value_assignment
                last_satisfying_bounding_relaxation_location = new_bounding_relaxation_location
                find_bounding_relaxation = True
            else:
                print("{} doesn't satisfy constraints".format(full_value_assignment))
                checked_assignments_not_satisfying.append(full_value_assignment_str)
                left = cur_row_id + 1

        col_idx = 0
        find_relaxation[num_columns].append(find_bounding_relaxation)  # FIXME: is this find_relaxation necessary?
        if not find_bounding_relaxation:
            if len(PVT_head_stack) > 0:
                next_col_num_in_stack = len(PVT_head_stack[-1])
            else:
                next_col_num_in_stack = len(full_PVT_head)
                # FIXME
            check_to_put_to_stack(to_put_to_stack, next_col_num_in_stack, num_columns, find_relaxation,
                                  PVT_stack, PVT_head_stack, max_index_PVT_stack, parent_PVT_stack,
                                  parent_PVT_head_stack,
                                  parent_max_index_PVT_stack, col_idx_in_parent_PVT_stack,
                                  idx_in_this_col_in_parent_PVT_stack,
                                  fixed_value_assignments_stack, fixed_value_assignments_positions_stack,
                                  fixed_value_assignments_to_tighten_stack, left_side_binary_search_stack,
                                  shifted_length_stack,
                                  idx_in_this_col_in_parent_PVT,
                                  PVT, PVT_head, max_index_PVT, parent_PVT, parent_PVT_head, parent_max_index_PVT,
                                  col_idx_in_parent_PVT, fixed_value_assignments, fixed_value_assignments_positions)
            continue

        max_index_in_col_tight = satisfying_row_id
        if num_columns > 1:
            full_value_assignment = last_satisfying_full_value_assignment
            new_value_assignment = last_satisfying_new_value_assignment
            nan_row = PVT.iloc[satisfying_row_id].isnull()
            col_non_tightenable = -1
            if sum(k is False for k in nan_row) == 1:
                true_lst = np.where(nan_row)[0]
                range_lst = range(0, num_columns)
                col_non_tightenable = [x for x in range_lst if x not in true_lst][0]
                print("col {} doesn't need to be tightened".format(col_non_tightenable))

            print("try to tighten the result of {}".format([last_satisfying_full_value_assignment[k] for k in PVT_head]))

            tmp_max_idx_of_ol = 0
            def tighten_result(column):
                nonlocal col_idx
                nonlocal last_satisfying_full_value_assignment
                nonlocal tmp_max_idx_of_ol
                idx_in_this_col = last_satisfying_bounding_relaxation_location[col_idx]
                if col_idx == col_non_tightenable:
                    col_idx += 1
                    tmp_max_idx_of_ol = max(tmp_max_idx_of_ol, idx_in_this_col)
                    return
                while idx_in_this_col > 0:
                    idx_in_this_col -= 1
                    new_value_assignment[col_idx] = column[idx_in_this_col]
                    full_value_assignment[PVT_head[col_idx]] = column[idx_in_this_col]
                    print("value_assignment: ", full_value_assignment)
                    full_value_assignment_str = num2string([full_value_assignment[k] for k in full_PVT_head])
                    if full_value_assignment_str in checked_assignments_satisfying:
                        print("{} satisfies constraints".format(full_value_assignment))
                        last_satisfying_full_value_assignment = full_value_assignment
                        last_satisfying_bounding_relaxation_location[col_idx] = idx_in_this_col
                        smallest_row = idx_in_this_col
                    elif full_value_assignment_str in checked_assignments_not_satisfying:
                        print("{} doesn't satisfy constraints".format(full_value_assignment))
                        smallest_row = idx_in_this_col + 1
                        # last_satisfying_bounding_relaxation_location[col_idx] = smallest_row
                        new_value_assignment[col_idx] = column[smallest_row]
                        full_value_assignment[PVT_head[col_idx]] = column[smallest_row]
                        break
                    elif assign_to_provenance_relax_only(full_value_assignment, numeric_attributes, categorical_attributes,
                                                       selection_numeric, selection_categorical,
                                                       full_PVT_head,
                                                       num_columns, fairness_constraints_provenance_greater_than):
                        checked_assignments_satisfying.append(full_value_assignment_str)
                        print("{} satisfies constraints".format(full_value_assignment))
                        last_satisfying_full_value_assignment = full_value_assignment
                        last_satisfying_bounding_relaxation_location[col_idx] = idx_in_this_col
                        smallest_row = idx_in_this_col
                    else:
                        print("{} doesn't satisfy constraints".format(full_value_assignment))
                        checked_assignments_not_satisfying.append(full_value_assignment_str)
                        smallest_row = idx_in_this_col + 1
                        # last_satisfying_bounding_relaxation_location[col_idx] = smallest_row
                        new_value_assignment[col_idx] = column[smallest_row]
                        full_value_assignment[PVT_head[col_idx]] = column[smallest_row]
                        break

                col_idx += 1
                return

            PVT.apply(tighten_result, axis=0)
            print("tight relaxation: {}".format(new_value_assignment))

        # optimization: tighten the last fixed column
        # TODO
        if idx_in_this_col_in_parent_PVT > 0:
            values_above = fixed_value_assignments_to_tighten_stack.pop()
            # binary search to tighten this column
            left = 0
            right = len(values_above)
            fixed_att = list(fixed_value_assignments.keys())[-1]
            tight_value_idx = 0
            print("tighten the last fixed column {}: {}".format(fixed_att, values_above))
            while left <= right:
                cur_value_id = int((right + left) / 2)
                cur_fixed_value = values_above[cur_value_id]
                fixed_value_assignments[fixed_att] = cur_fixed_value
                full_value_assignment = {**dict(zip(PVT_head, new_value_assignment)), **fixed_value_assignments}
                print("value_assignment: ", full_value_assignment)
                full_value_assignment_str = num2string([full_value_assignment[k] for k in full_PVT_head])
                if full_value_assignment_str in checked_assignments_satisfying:
                    print("{} satisfies constraints".format(full_value_assignment))
                    right = cur_value_id - 1
                    tight_value_idx = cur_value_id
                elif full_value_assignment_str in checked_assignments_not_satisfying:
                    print("{} doesn't satisfy constraints".format(full_value_assignment))
                    left = cur_value_id + 1
                elif assign_to_provenance_relax_only(full_value_assignment, numeric_attributes, categorical_attributes,
                                                   selection_numeric, selection_categorical,
                                                   full_PVT_head,
                                                   num_columns, fairness_constraints_provenance_greater_than):
                    checked_assignments_satisfying.append(full_value_assignment_str)
                    print("{} satisfies constraints".format(full_value_assignment))
                    right = cur_value_id - 1
                    tight_value_idx = cur_value_id
                else:
                    print("{} doesn't satisfy constraints".format(full_value_assignment))
                    checked_assignments_not_satisfying.append(full_value_assignment_str)
                    left = cur_value_id + 1
            if tight_value_idx < idx_in_this_col_in_parent_PVT:
                # tight this fixed column successfully
                # last_satisfying_bounding_relaxation_location[PVT_head.index(fixed_att)] = tight_value_idx
                fixed_value_assignments[fixed_att] = values_above[tight_value_idx]
                full_value_assignment[fixed_att] = values_above[tight_value_idx]
                idx_in_this_col_in_parent_PVT = tight_value_idx
                if idx_in_this_col_in_parent_PVT == 0:
                    to_put_to_stack.pop()
                else:
                    to_put_to_stack[-1]['idx_in_this_col_in_parent_PVT'] = idx_in_this_col_in_parent_PVT - 1
                    to_put_to_stack[-1]['fixed_value_assignments'][fixed_att] = values_above[tight_value_idx - 1]
                    to_put_to_stack[-1]['fixed_value_assignments_to_tighten'] = values_above[: tight_value_idx - 1]

        fva = [full_value_assignment[k] for k in full_PVT_head]
        full_value_assignment_positions = dict(zip(PVT_head, last_satisfying_bounding_relaxation_location))
        full_value_assignment_positions = {**full_value_assignment_positions, **fixed_value_assignments_positions}

        minimal_refinements, minimal_refinements_positions = \
            update_minimal_relaxation_and_position(minimal_refinements, minimal_refinements_positions,
                                                   fva, [full_value_assignment_positions[x] for x in full_PVT_head],
                                                   shifted_length)

        # minimal_refinements.append([full_value_assignment[k] for k in full_PVT_head])

        print("minimal_refinements: {}".format(minimal_refinements))
        if num_columns == 1:
            if len(PVT_head_stack) > 0:
                next_col_num_in_stack = len(PVT_head_stack[-1])
            else:
                next_col_num_in_stack = len(full_PVT_head)
            # FIXME
            check_to_put_to_stack(to_put_to_stack, next_col_num_in_stack, num_columns, find_relaxation,
                                  PVT_stack, PVT_head_stack, max_index_PVT_stack, parent_PVT_stack,
                                  parent_PVT_head_stack,
                                  parent_max_index_PVT_stack, col_idx_in_parent_PVT_stack,
                                  idx_in_this_col_in_parent_PVT_stack,
                                  fixed_value_assignments_stack, fixed_value_assignments_positions_stack,
                                  fixed_value_assignments_to_tighten_stack, left_side_binary_search_stack,
                                  shifted_length_stack,
                                  idx_in_this_col_in_parent_PVT,
                                  PVT, PVT_head, max_index_PVT, parent_PVT, parent_PVT_head, parent_max_index_PVT,
                                  col_idx_in_parent_PVT, fixed_value_assignments, fixed_value_assignments_positions)
            continue
        # recursion
        col_idx = 0

        index_to_insert_to_stack = len(PVT_stack)
        insert_idx_fixed_value_assignments_to_tighten_stack = len(fixed_value_assignments_to_tighten_stack)
        index_to_insert_to_put = len(to_put_to_stack)
        original_max_index_PVT = max_index_PVT.copy()
        def recursion(column):
            nonlocal col_idx
            nonlocal new_value_assignment
            nonlocal last_satisfying_bounding_relaxation_location
            idx_in_this_col = last_satisfying_bounding_relaxation_location[col_idx]
            # optimization: if there are no other columns to be moved down, return
            if sum(last_satisfying_bounding_relaxation_location[i] < original_max_index_PVT[i] for i in range(len(PVT_head)) if
                   i != col_idx) == 0:
                col_idx += 1
                return
            if idx_in_this_col == 0:
                col_idx += 1
                return
            idx_in_this_col -= 1
            # optimization: fixing this value doesn't dissatisfy inequalities
            one_more_fix = copy.deepcopy(fixed_value_assignments)
            one_more_fix[PVT_head[col_idx]] = column[idx_in_this_col]

            if not assign_to_provenance_relax_only(one_more_fix, numeric_attributes, categorical_attributes,
                                                   selection_numeric, selection_categorical,
                                                   full_PVT_head,
                                                   num_columns, fairness_constraints_provenance_greater_than):
                print("fixing {} = {} dissatisfies constraints".format(PVT_head[col_idx], column[idx_in_this_col]))
                col_idx += 1
                return
            fixed_value_assignments_for_stack = copy.deepcopy(fixed_value_assignments)
            fixed_value_assignments_for_stack[PVT_head[col_idx]] = column[idx_in_this_col]
            fixed_value_assignments_positions_for_stack = copy.deepcopy(fixed_value_assignments_positions)
            fixed_value_assignments_positions_for_stack[PVT_head[col_idx]] = idx_in_this_col

            new_PVT_head = [PVT_head[x] for x in range(len(PVT_head)) if x != col_idx]
            new_max_index_PVT = max_index_PVT[:col_idx] + max_index_PVT[col_idx + 1:]
            # optimization: if there is only one column left to be moved down,
            #  this column in the new recursion should start from where it stopped before
            if len(new_PVT_head) == 1:
                PVT_for_recursion = PVT[new_PVT_head].iloc[
                                    last_satisfying_bounding_relaxation_location[1 - col_idx] + 1:
                                    max(new_max_index_PVT) + 1].reset_index(drop=True)
                new_max_index_PVT = [len(PVT_for_recursion) - 1]
            else:
                PVT_for_recursion = PVT[new_PVT_head].head(max(new_max_index_PVT) + 1)
            PVT_stack.insert(index_to_insert_to_stack, PVT_for_recursion)
            PVT_head_stack.insert(index_to_insert_to_stack, new_PVT_head)
            max_index_PVT_stack.insert(index_to_insert_to_stack, new_max_index_PVT)
            parent_PVT_stack.insert(index_to_insert_to_stack, PVT)
            parent_PVT_head_stack.insert(index_to_insert_to_stack, PVT_head)
            parent_max_index_PVT_stack.insert(index_to_insert_to_stack, max_index_PVT)
            col_idx_in_parent_PVT_stack.insert(index_to_insert_to_stack, col_idx)
            idx_in_this_col_in_parent_PVT_stack.insert(index_to_insert_to_stack, idx_in_this_col)
            fixed_value_assignments_stack.insert(index_to_insert_to_stack, fixed_value_assignments_for_stack)
            fixed_value_assignments_positions_stack.insert(index_to_insert_to_stack, fixed_value_assignments_positions_for_stack)
            before_shift = last_satisfying_bounding_relaxation_location[:col_idx] + \
                           last_satisfying_bounding_relaxation_location[col_idx+1:]
            shift_for_col = [shifted_length[PVT_head.index(att)] for att in PVT_head]
            shift_len = shift_for_col[:col_idx] + shift_for_col[col_idx + 1:]
            after_shift = [before_shift[i] - shift_len[i] for i in range(num_columns-1)]
            for_left_binary = max(after_shift)
            left_side_binary_search_stack.insert(index_to_insert_to_stack, for_left_binary)
            shifted_length_stack.insert(index_to_insert_to_stack, copy.deepcopy(shifted_length))
            if idx_in_this_col > 0:
                fixed_value_assignments_to_tighten_stack.insert(insert_idx_fixed_value_assignments_to_tighten_stack, column[:idx_in_this_col].copy())
                # to_put_to_stack
                to_put = dict()
                to_put['PVT'] = PVT_for_recursion.copy()
                to_put['PVT_head'] = new_PVT_head.copy()
                to_put['max_index_PVT'] = new_max_index_PVT.copy()
                to_put['parent_PVT'] = PVT.copy()
                to_put['parent_PVT_head'] = PVT_head.copy()
                to_put['parent_max_index_PVT'] = max_index_PVT.copy()
                to_put['col_idx_in_parent_PVT'] = col_idx
                to_put['idx_in_this_col_in_parent_PVT'] = idx_in_this_col - 1
                fixed_value_assignments_to_put = copy.deepcopy(fixed_value_assignments_for_stack)
                fixed_value_assignments_to_put[PVT_head[col_idx]] = column[idx_in_this_col - 1]
                to_put['fixed_value_assignments'] = fixed_value_assignments_to_put
                fixed_value_assignments_positions_to_put = copy.deepcopy(fixed_value_assignments_positions_for_stack)
                fixed_value_assignments_positions_to_put[PVT_head[col_idx]] = idx_in_this_col - 1
                to_put['fixed_value_assignments_positions'] = fixed_value_assignments_positions_to_put
                if to_put['idx_in_this_col_in_parent_PVT'] > 0:
                    to_put['fixed_value_assignments_to_tighten'] = column[:idx_in_this_col-1].copy()
                to_put['for_left_binary'] = for_left_binary
                to_put['shifted_length'] = copy.deepcopy(shifted_length)
                to_put_to_stack.insert(index_to_insert_to_put, to_put)

            # TODO: avoid repeated checking: for columns that are done with moving up,
            #  we need to remove values above the 'stop line'
            seri = PVT[PVT_head[col_idx]]
            PVT[PVT_head[col_idx]] = seri.shift(periods=-last_satisfying_bounding_relaxation_location[col_idx])
            max_index_PVT[col_idx] -= last_satisfying_bounding_relaxation_location[col_idx]
            shifted_length[full_PVT_head.index(PVT_head[col_idx])] += last_satisfying_bounding_relaxation_location[col_idx]
            col_idx += 1
            return

        PVT.apply(recursion, axis=0)
        if len(PVT_head_stack) > 0:
            next_col_num_in_stack = len(PVT_head_stack[-1])
        else:
            next_col_num_in_stack = len(full_PVT_head)
        check_to_put_to_stack(to_put_to_stack, next_col_num_in_stack, num_columns, find_relaxation,
                              PVT_stack, PVT_head_stack, max_index_PVT_stack, parent_PVT_stack, parent_PVT_head_stack,
                              parent_max_index_PVT_stack, col_idx_in_parent_PVT_stack, idx_in_this_col_in_parent_PVT_stack,
                              fixed_value_assignments_stack, fixed_value_assignments_positions_stack,
                              fixed_value_assignments_to_tighten_stack, left_side_binary_search_stack, shifted_length_stack,
                              idx_in_this_col_in_parent_PVT,
                              PVT, PVT_head, max_index_PVT, parent_PVT, parent_PVT_head, parent_max_index_PVT,
                              col_idx_in_parent_PVT, fixed_value_assignments, fixed_value_assignments_positions)
    return minimal_refinements


def check_to_put_to_stack(to_put_to_stack, next_col_num_in_stack, this_num_columns, find_relaxation,
                          PVT_stack, PVT_head_stack, max_index_PVT_stack, parent_PVT_stack, parent_PVT_head_stack,
                          parent_max_index_PVT_stack, col_idx_in_parent_PVT_stack, idx_in_this_col_in_parent_PVT_stack,
                          fixed_value_assignments_stack, fixed_value_assignments_positions_stack,
                          fixed_value_assignments_to_tighten_stack, left_side_binary_search_stack, shifted_length_stack,
                          idx_in_this_col_in_parent_PVT,
                          PVT, PVT_head, max_index_PVT, parent_PVT, parent_PVT_head, parent_max_index_PVT,
                          col_idx_in_parent_PVT, fixed_value_assignments, fixed_value_assignments_positions):
    if idx_in_this_col_in_parent_PVT == 0:
        return False
    to_put = to_put_to_stack.pop()
    PVT_from_to_put = False
    print("next_col_num_in_stack = {}, this_num_columns = {}".format(next_col_num_in_stack, this_num_columns))
    if len([k for k in find_relaxation[this_num_columns] if k is True]) > 0:
        if to_put != {}:
            PVT_stack.append(to_put['PVT'])
            PVT_head_stack.append(to_put['PVT_head'])
            max_index_PVT_stack.append(to_put['max_index_PVT'])
            parent_PVT_stack.append(to_put['parent_PVT'])
            parent_PVT_head_stack.append(to_put['parent_PVT_head'])
            parent_max_index_PVT_stack.append(to_put['parent_max_index_PVT'])
            col_idx_in_parent_PVT_stack.append(to_put['col_idx_in_parent_PVT'])
            idx_in_this_col_in_parent_PVT_stack.append(to_put['idx_in_this_col_in_parent_PVT'])
            fixed_value_assignments_stack.append(to_put['fixed_value_assignments'])
            fixed_value_assignments_positions_stack.append(to_put['fixed_value_assignments_positions'])
            left_side_binary_search_stack.append(to_put['for_left_binary'])
            shifted_length_stack.append(to_put['shifted_length'])
            if to_put['idx_in_this_col_in_parent_PVT'] > 0:
                fixed_value_assignments_to_tighten_stack.append(to_put['fixed_value_assignments_to_tighten'])

            if to_put['idx_in_this_col_in_parent_PVT'] > 0:
                # FIXMe: should I copy from to_put
                to_put2 = dict()
                to_put2['PVT'] = PVT
                to_put2['PVT_head'] = PVT_head
                to_put2['max_index_PVT'] = max_index_PVT
                to_put2['parent_PVT'] = parent_PVT
                to_put2['parent_PVT_head'] = parent_PVT_head
                to_put2['parent_max_index_PVT'] = parent_max_index_PVT
                to_put2['col_idx_in_parent_PVT'] = col_idx_in_parent_PVT
                to_put2['idx_in_this_col_in_parent_PVT'] = to_put['idx_in_this_col_in_parent_PVT'] - 1
                fixed_value_assignments_to_put = copy.deepcopy(fixed_value_assignments)
                fixed_value_assignments_to_put[PVT_head[col_idx_in_parent_PVT]] \
                    = parent_PVT.iloc[to_put['idx_in_this_col_in_parent_PVT'] - 1, col_idx_in_parent_PVT]
                to_put2['fixed_value_assignments'] = fixed_value_assignments_to_put
                fixed_value_assignments_positions_to_put = copy.deepcopy(fixed_value_assignments_positions)
                fixed_value_assignments_positions_to_put[PVT_head[col_idx_in_parent_PVT]] \
                    = to_put['idx_in_this_col_in_parent_PVT']
                to_put2['fixed_value_assignments_positions'] = fixed_value_assignments_positions_to_put
                to_put2['for_left_binary'] = to_put['for_left_binary']
                to_put2['shifted_length'] = to_put['shifted_length']
                if to_put['idx_in_this_col_in_parent_PVT'] > 1:
                    to_put2['fixed_value_assignments_to_tighten'] = to_put['fixed_value_assignments_to_tighten'][:-1]
                to_put_to_stack.append(to_put2)
    find_relaxation[this_num_columns] = []
    return PVT_from_to_put



def whether_value_assignment_is_tight_minimal(must_included_term_delta_values, value_assignment, numeric_attributes,
                                              categorical_attributes,
                                              selection_numeric, selection_categorical,
                                              columns_delta_table, num_columns,
                                              fairness_constraints_provenance_greater_than,
                                              fairness_constraints_provenance_smaller_than,
                                              minimal_added_relaxations):
    value_idx = 0
    for v in value_assignment:
        if v == 0:
            value_idx += 1
            continue
        if v == must_included_term_delta_values[value_idx]:
            value_idx += 1
            continue
        smaller_value_assignment = value_assignment.copy()
        att = columns_delta_table[value_idx]
        if value_idx < len(numeric_attributes):  # numeric
            while True:
                if smaller_value_assignment[value_idx] == 0:
                    break
                if smaller_value_assignment[value_idx] < 0:
                    smaller_value_assignment[value_idx] += selection_numeric[att][2]
                    if smaller_value_assignment[value_idx] > 0:
                        break
                elif smaller_value_assignment[value_idx] > 0:
                    smaller_value_assignment[value_idx] -= selection_numeric[att][2]
                    if smaller_value_assignment[value_idx] < 0:
                        break
                if assign_to_provenance_relax_only(smaller_value_assignment, numeric_attributes, categorical_attributes,
                                                   selection_numeric, selection_categorical, columns_delta_table,
                                                   num_columns,
                                                   fairness_constraints_provenance_greater_than):
                    if not dominated_by_minimal_set(minimal_added_relaxations, smaller_value_assignment):
                        return False
                else:
                    break
        else:  # categorical
            smaller_value_assignment[value_idx] = 0
            if assign_to_provenance_relax_only(smaller_value_assignment, numeric_attributes, categorical_attributes,
                                               selection_numeric, selection_categorical, columns_delta_table,
                                               num_columns,
                                               fairness_constraints_provenance_greater_than):
                if not dominated_by_minimal_set(minimal_added_relaxations, smaller_value_assignment):
                    return False
        value_idx += 1
    return True



def transform_to_refinement_format(minimal_added_refinements, numeric_attributes, selection_numeric_attributes,
                                   selection_categorical_attributes, columns_delta_table):
    minimal_refinements = []
    num_numeric_att = len(numeric_attributes)
    num_att = len(columns_delta_table)
    for ar in minimal_added_refinements:
        select_numeric = copy.deepcopy(selection_numeric_attributes)
        select_categorical = copy.deepcopy(selection_categorical_attributes)
        for att_idx in range(num_att):
            if att_idx < num_numeric_att:
                select_numeric[numeric_attributes[att_idx]][1] -= ar[att_idx]
            elif ar[att_idx] == 1:
                at, va = columns_delta_table[att_idx].rsplit('_', 1)
                select_categorical[at].append(va)
            elif ar[att_idx] == -1:
                at, va = columns_delta_table[att_idx].rsplit('_', 1)
                select_categorical[at].remove(va)
        minimal_refinements.append({'numeric': select_numeric, 'categorical': select_categorical})
    return minimal_refinements


########################################################################################################################


def FindMinimalRefinement(data_file, query_file, constraint_file):
    data = pd.read_csv(data_file)
    with open(query_file) as f:
        query_info = json.load(f)

    selection_numeric_attributes = query_info['selection_numeric_attributes']
    selection_categorical_attributes = query_info['selection_categorical_attributes']
    numeric_attributes = list(selection_numeric_attributes.keys())
    categorical_attributes = query_info['categorical_attributes']
    selected_attributes = numeric_attributes + [x for x in categorical_attributes]
    print("selected_attributes", selected_attributes)

    with open(constraint_file) as f:
        constraint_info = json.load(f)

    sensitive_attributes = constraint_info['all_sensitive_attributes']
    fairness_constraints = constraint_info['fairness_constraints']

    pd.set_option('display.float_format', '{:.2f}'.format)

    time1 = time.time()
    fairness_constraints_provenance_greater_than, fairness_constraints_provenance_smaller_than, \
    data_rows_greater_than, data_rows_smaller_than, only_greater_than, only_smaller_than \
        = subtract_provenance(data, selected_attributes, sensitive_attributes, fairness_constraints,
                              numeric_attributes, categorical_attributes, selection_numeric_attributes,
                              selection_categorical_attributes)
    time_provenance2 = time.time()
    provenance_time = time_provenance2 - time1
    # print("provenance_expressions")
    # print(*fairness_constraints_provenance_greater_than, sep="\n")
    # print(*fairness_constraints_provenance_smaller_than, sep="\n")

    if only_greater_than:
        time_table1 = time.time()
        already_satisfy = True
        for fc in fairness_constraints_provenance_greater_than:
            if not eval('0' + fc['symbol'] + str(fc['number'])):
                already_satisfy = False
                break
        if already_satisfy:
            return {}, time.time() - time1

        PVT, PVT_head, categorical_att_columns, max_index_PVT = build_PVT_relax_only(data, selected_attributes,
                                                                                     numeric_attributes,
                                                                                     categorical_attributes,
                                                                                     selection_numeric_attributes,
                                                                                     selection_categorical_attributes,
                                                                                     sensitive_attributes,
                                                                                     fairness_constraints,
                                                                                     fairness_constraints_provenance_greater_than,
                                                                                     fairness_constraints_provenance_smaller_than,
                                                                                     data_rows_greater_than,
                                                                                     data_rows_smaller_than)
        print("max_index_PVT: {}".format(max_index_PVT))
        time_table2 = time.time()
        table_time = time_table2 - time_table1
        # print("delta table:\n{}".format(delta_table))
        time_search1 = time.time()

        checked_satisfying_constraints = set()  # set of bit arrays
        checked_unsatisfying_constraints = set()
        checked_assignments_satisfying = []
        checked_assignments_unsatisfying = []
        minimal_refinements = searchPVT(PVT, PVT_head, numeric_attributes,
                                        categorical_attributes, selection_numeric_attributes,
                                        selection_categorical_attributes, len(PVT_head),
                                        fairness_constraints_provenance_greater_than, PVT, PVT_head,
                                        max_index_PVT,
                                        checked_assignments_satisfying, checked_assignments_unsatisfying)
        time_search2 = time.time()
        # print("checked_assignments_satisfying:{}".format(checked_assignments_satisfying))
        # print("checked_assignments_unsatisfying:{}".format(checked_assignments_unsatisfying))
        # minimal_refinements = transform_to_refinement_format(minimal_added_refinements, numeric_attributes,
        #                                                      selection_numeric_attributes,
        #                                                      selection_categorical_attributes,
        #                                                      PVT_head)
        time2 = time.time()
        print("provenance time = {}".format(provenance_time))
        print("table time = {}".format(table_time))
        print("searching time = {}".format(time_search2 - time_search1))
        # print("minimal_added_relaxations:{}".format(minimal_added_refinements))
        return minimal_refinements, time2 - time1

    elif only_smaller_than:
        time_table1 = time.time()
        PVT, PVT_head, categorical_att_columns, max_index_PVT = build_PVT_relax_only(data, selected_attributes,
                                                                                     numeric_attributes,
                                                                                     categorical_attributes,
                                                                                     selection_numeric_attributes,
                                                                                     selection_categorical_attributes,
                                                                                     sensitive_attributes,
                                                                                     fairness_constraints,
                                                                                     fairness_constraints_provenance_greater_than,
                                                                                     fairness_constraints_provenance_smaller_than,
                                                                                     data_rows_greater_than,
                                                                                     data_rows_smaller_than)
        print("max_index_PVT: {}".format(max_index_PVT))
        time_table2 = time.time()
        table_time = time_table2 - time_table1
        # print("delta table:\n{}".format(delta_table))
        time_search1 = time.time()

        checked_satisfying_constraints = set()  # set of bit arrays
        checked_unsatisfying_constraints = set()
        checked_assignments_satisfying = []
        checked_assignments_unsatisfying = []

        minimal_refinements = searchPVT(PVT, PVT_head, numeric_attributes,
                                        categorical_attributes, selection_numeric_attributes,
                                        selection_categorical_attributes, len(PVT_head),
                                        fairness_constraints_provenance_greater_than, PVT, PVT_head,
                                        max_index_PVT,
                                        checked_assignments_satisfying, checked_assignments_unsatisfying)
        time_search2 = time.time()
        # print("checked_assignments_satisfying:{}".format(checked_assignments_satisfying))
        # print("checked_assignments_unsatisfying:{}".format(checked_assignments_unsatisfying))
        # minimal_refinements = transform_to_refinement_format(minimal_added_refinements, numeric_attributes,
        #                                                      selection_numeric_attributes,
        #                                                      selection_categorical_attributes,
        #                                                      PVT_head)
        time2 = time.time()
        print("provenance time = {}".format(provenance_time))
        print("table time = {}".format(table_time))
        print("searching time = {}".format(time_search2 - time_search1))
        # print("minimal_added_relaxations:{}".format(minimal_added_refinements))
        return minimal_refinements, time2 - time1


    time_search1 = time.time()

    time_search2 = time.time()

    time2 = time.time()

    return [], [], time2 - time1




# data_file = r"../InputData/Pipelines/healthcare/incomeK/before_selection_incomeK.csv"
# query_file = r"../InputData/Pipelines/healthcare/incomeK/relaxation/query4.json"
# constraint_file = r"../InputData/Pipelines/healthcare/incomeK/relaxation/constraint2.json"

data_file = r"toy_examples/example4.csv"
query_file = r"toy_examples/query2.json"
constraint_file = r"toy_examples/constraint4.json"

print("\nnaive algorithm:\n")

minimal_refinements2, minimal_added_refinements2, running_time2 = lt.FindMinimalRefinement(data_file, query_file,
                                                                                           constraint_file)

# minimal_refinements2 = [[float(y) for y in x] for x in minimal_refinements2]

print(*minimal_refinements2, sep="\n")
print("running time = {}".format(running_time2))

# naive_ans = [[300, 4, 5, 1, 1],
# [300, 4, 3, 1, 0],
# [300, 4, 1, 0, 1],
# [300, 5, 6, 1, 1],
# [300, 5, 4, 1, 0],
# [300, 5, 2, 0, 1],
# [300, 5, 0, 0, 0],
# [322, 4, 6, 1, 1],
# [324, 4, 4, 1, 0],
# [324, 5, 5, 1, 0],
# [343, 4, 2, 0, 1],
# [343, 4, 0, 0, 0],
# [343, 5, 3, 0, 1],
# [343, 5, 1, 0, 0],
# [353, 4, 3, 0, 1],
# [382, 5, 4, 0, 1],
# [413, 5, 6, 1, 0],
# [417, 4, 5, 1, 0],
# [418, 5, 7, 1, 1],
# [423, 4, 4, 0, 1],
# [423, 5, 5, 0, 1]]

print("\nour algorithm:\n")

minimal_refinements, running_time = FindMinimalRefinement(data_file, query_file, constraint_file)

# minimal_refinements = [[float(y) for y in x] for x in minimal_refinements]

print(*minimal_refinements, sep="\n")
print("running time = {}".format(running_time))

print("in naive_ans but not our:\n")
for na in minimal_refinements2:
    if na not in minimal_refinements:
        print(na)

print("in our but not naive_ans:\n")
for na in minimal_refinements:
    if na not in minimal_refinements2:
        print(na)
