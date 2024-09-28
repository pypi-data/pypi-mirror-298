import gc
from typing import Any, Union


def tidy_up_list(lst: list, bool_mode: bool = False, eval_mode: bool = False, float_mode: bool = False,
                 int_mode: bool = False, none_mode: bool = False) -> list:

    # 判断是否是list类型，否则返回形参原本值
    if type(lst) is not list and not (len(lst) <= 0):
        return lst

    bool_mode = bool(bool_mode)
    eval_mode = bool(eval_mode)
    float_mode = bool(float_mode)
    int_mode = bool(int_mode)

    _lst_types: list = []
    _point_j: int = 0
    _point_l: list = []
    _str_app_l: list = []
    _type_content: dict = {'str': [], 'int': [], 'float': [], 'lst': [], 'dic': [], 'set': [], 'tuple': [],
                           'complex': [],
                           'None': []}

    # 保存原有特殊变量原本值
    for i in range(len(lst)):
        if isinstance(lst[i], str) and (lst[i] not in _type_content['str']):
            _type_content['str'].append(lst[i])

        if isinstance(lst[i], int) and (lst[i] not in _type_content['int']):
            _type_content['int'].append(lst[i])

        if isinstance(lst[i], float) and (lst[i] not in _type_content['float']):
            _type_content['float'].append(lst[i])

        if type(lst[i]) is None and (lst[i] not in _type_content['None']):
            _type_content['None'].append(lst[i])

        if type(lst[i]) is list and (lst[i] not in _type_content['lst']):
            _type_content['lst'].append(lst[i])

        if type(lst[i]) is dict and (lst[i] not in _type_content['dic']):
            _type_content['dic'].append(lst[i])

        if type(lst[i]) is set and (lst[i] not in _type_content['set']):
            _type_content['set'].append(lst[i])

        if type(lst[i]) is tuple and (lst[i] not in _type_content['tuple']):
            _type_content['tuple'].append(lst[i])
        if type(lst[i]) is complex and (lst[i] not in _type_content['complex']):
            _type_content['complex'].append(lst[i])

        lst[i] = str(lst[i])

    # 排序+去除重复值
    lst = list(set(lst))
    for i in range(len(lst)):
        lst[i] = str(lst[i])
    lst = sorted(lst, key=str.lower)

    # 判断列表值是何类型1
    for i in range(len(lst)):
        _point_l.append([])
        _str_app_l.append([])
        for j in lst[i]:
            if 48 <= ord(j) <= 57:
                continue
            elif j == '.':
                if not _point_l[i]:
                    _point_l[i].append(True)
                else:
                    continue
            else:
                if not _str_app_l[i]:
                    _str_app_l[i].append(True)
                else:
                    continue

    # 判断列表值是何类型2
    for i in range(len(_point_l)):
        if True in _str_app_l[i]:
            _lst_types.append('str')
        elif True in _point_l[i] and _str_app_l[i] == []:
            for j in range(len(lst[i])):
                if lst[i][j] == '.':
                    _point_j += 1
            if _point_j == 1:
                _lst_types.append('float')
                _point_j = 0
            else:
                _lst_types.append('str')
                _point_j = 0
        else:
            _lst_types.append('int')

    # 转换类型
    for i in range(len(_lst_types)):
        if _lst_types[i] == 'str':
            if eval_mode:
                try:
                    lst[i] = eval(lst[i])
                except:
                    pass
            pass
        try:
            if _lst_types[i] == 'float':
                lst[i] = float(lst[i])
            if _lst_types[i] == 'int':
                lst[i] = int(lst[i])
        except ValueError:
            pass

    # code burger(bushi     (将收集到的特殊数据插入回列表)
    for i in range(len(_type_content['complex'])):
        lst.remove(str(_type_content['complex'][i]))
        lst.append(_type_content['complex'][i])
    for i in range(len(_type_content['tuple'])):
        lst.remove(str(_type_content['tuple'][i]))
        lst.append(_type_content['tuple'][i])
    for i in range(len(_type_content['lst'])):
        lst.remove(str(_type_content['lst'][i]))
        lst.append(_type_content['lst'][i])
    for i in range(len(_type_content['set'])):
        lst.remove(str(_type_content['set'][i]))
        lst.append(_type_content['set'][i])
    for i in range(len(_type_content['dic'])):
        lst.remove(str(_type_content['dic'][i]))
        lst.append(_type_content['dic'][i])

    if bool_mode:
        for i in range(len(lst)):
            if lst[i] == 'True':
                lst[i] = bool(1)
            elif lst[i] == 'False':
                lst[i] = bool(0)

    del _lst_types, _point_j, _point_l, _str_app_l, _type_content
    gc.collect()

    return lst


def deeply_tidy_up_list(lst: list) -> list:

    if type(lst) is not list:
        return lst

    _j: int = 0
    lst = tidy_up_list(lst)

    for _i in lst:
        if type(_i) is list:
            lst[_j] = deeply_tidy_up_list(_i)
        _j += 1

    return lst


def bubble_sort(lst: list, if_round: bool = False, in_reverse_order: bool = False) -> list:

    if type(lst) is not list:
        return lst

    _i: int = 0
    if_round = bool(if_round)
    lst_T = lst.copy()

    for _i in range(len(lst_T)):
        if (not (isinstance(lst_T[_i], int) or isinstance(lst_T[_i], float))) or len(lst_T) == 0:
            return lst_T

    if if_round:
        try:
            from math import ceil
            for _i in range(len(lst_T)):
                if isinstance(lst_T[_i], float):
                    lst_T[_i] = ceil(lst_T[_i])
        except ImportError:
            def ceil() -> None:
                ceil()

            for _i in range(len(lst_T)):
                if isinstance(lst_T[_i], float):
                    lst_T[_i] = round(lst_T[_i])

    lst_len = len(lst_T)
    for _i in range(lst_len):
        for _j in range(lst_len - 1 - _i):
            if in_reverse_order:
                if lst_T[_j + 1] >= lst_T[_j]:
                    lst_T[_j], lst_T[_j + 1] = lst_T[_j + 1], lst_T[_j]
            else:
                if lst_T[_j + 1] <= lst_T[_j]:
                    lst_T[_j], lst_T[_j + 1] = lst_T[_j + 1], lst_T[_j]

    try:
        del _i, _j
    except UnboundLocalError:
        pass
    gc.collect()

    return lst_T


# Big CSV_Project(Finished!)
def list_calculation(*args: list, calculation: str = "+", multi_calculation: str = "", nesting: bool = False) -> list:

    if len(args) <= 0 or len(calculation) <= 0:
        raise ValueError("No any list given")

    if len(calculation) > 1:
        raise ValueError("the length of calculation symbol can only be 1")

    if nesting:
        args = eval(str(args)[1:len(str(args)) - 2:])

    args = list(args)
    if_multi_calculation: bool = False
    if len(multi_calculation) != 0:
        if_multi_calculation = True
        multi_calculation = multi_calculation[:len(args) - 1:]
    length: dict = {}
    length_keys: list = []
    length_values: list = []

    # 清除掉长度为0的list元素和不是list类的元素
    for _i in range(len(args)):
        if not (isinstance(args[_i], list) or len(args[_i]) == 0):
            args.pop(_i)

    # 如果list里面的list的元素不是int或者float就报错
    for _i in range(len(args)):
        for _j in range(len(args[_i])):
            if not (isinstance(args[_i][_j], int) or isinstance(args[_i][_j], float)):
                raise ValueError(f"element cannot be {type(args[_i][_j])}")

    # 记录每个列表的长度
    # _i是第几个列表
    for _i in range(len(args)):
        length.update({_i: len(args[_i])})

    # 依照长度从小到大排序
    length_l = sorted(length.items(), key=lambda x: x[1])

    # key对应的是列表里面的第几个列表,value对应的是列表内的列表长度
    for key, value in length_l:
        length_keys.append(key)
        length_values.append(value)

    # 将列表倒序变成从大到小排序
    length_keys, length_values = list(reversed(length_keys)), list(reversed(length_values))
    # result取长度最长的列表
    result = args[length_keys[0]].copy()

    if not if_multi_calculation:
        for _i in range(len(length_l)):
            try:
                for _j in range(length_values[_i + 1]):
                    if calculation == "+":
                        result[_j] += (args[length_keys[_i + 1]].copy())[_j]
                    elif calculation == "-":
                        result[_j] -= (args[length_keys[_i + 1]].copy())[_j]
                    elif calculation == "*":
                        result[_j] *= (args[length_keys[_i + 1]].copy())[_j]
                    elif calculation == "**":
                        result[_j] **= (args[length_keys[_i + 1]].copy())[_j]
                    elif calculation == "/":
                        result[_j] /= (args[length_keys[_i + 1]].copy())[_j]
                    elif calculation == "//":
                        result[_j] //= (args[length_keys[_i + 1]].copy())[_j]
                    elif calculation == "%":
                        result[_j] %= (args[length_keys[_i + 1]].copy())[_j]
            except IndexError:
                pass

    if if_multi_calculation:
        calculation_lst = multi_calculation.split(",")
        for _i in range(len(length_l)):
            try:
                for _j in range(length_values[_i + 1]):
                    if calculation_lst[_i] == "+":
                        result[_j] += (args[length_keys[_i + 1]].copy())[_j]
                    elif calculation_lst[_i] == "-":
                        result[_j] -= (args[length_keys[_i + 1]].copy())[_j]
                    elif calculation_lst[_i] == "*":
                        result[_j] *= (args[length_keys[_i + 1]].copy())[_j]
                    elif calculation_lst[_i] == "**":
                        result[_j] **= (args[length_keys[_i + 1]].copy())[_j]
                    elif calculation_lst[_i] == "/":
                        result[_j] /= (args[length_keys[_i + 1]].copy())[_j]
                    elif calculation_lst[_i] == "//":
                        result[_j] //= (args[length_keys[_i + 1]].copy())[_j]
            except IndexError:
                pass

    try:
        del _i, _j, length, length_l, length_keys, length_values
    except UnboundLocalError:
        pass
    gc.collect()

    return result


def var_in_list(lst: list, __class: type, return_lst: bool = False, only_return_lst: bool = False) -> Union[int, tuple, list]:

    if return_lst and only_return_lst:
        raise ValueError("return_lst and only_return_lst cannot be True at the same time")

    def in_def_var_in_list(lst2: list) -> Union[int, tuple, list]:
        if return_lst:
            if globals().get("$all_result") is None:
                globals().update({"$all_result": 0})
            if globals().get("$all_result_lst") is None:
                globals().update({"$all_result_lst": list([])})
        elif only_return_lst:
            if globals().get("$all_result_lst") is None:
                globals().update({"$all_result_lst": list([])})
        else:
            if globals().get("$all_result") is None:
                globals().update({"$all_result": 0})
        for _i in range(len(lst2)):
            if isinstance(lst2[_i], __class):
                if return_lst:
                    globals().update({"$all_result": globals().get("$all_result") + 1}), globals().get(
                        "$all_result_lst").append(lst2[_i])
                elif only_return_lst:
                    globals().get("$all_result_lst").append(lst2[_i])
                else:
                    globals().update({"$all_result": globals().get("$all_result") + 1})
            elif isinstance(lst2[_i], list):
                in_def_var_in_list(lst2[_i])
        if return_lst:
            return globals().get("$all_result"), globals().get("$all_result_lst")
        elif only_return_lst:
            return globals().get("$all_result_lst")
        else:
            return globals().get("$all_result")

    return_lst = bool(return_lst)
    result = in_def_var_in_list(lst)
    if return_lst:
        globals().pop("$all_result"), globals().pop("$all_result_lst")
    elif only_return_lst:
        globals().pop("$all_result_lst")
    else:
        globals().pop("$all_result")
    return result


def in_list_calculation(lst: list, calculation: str = "+", multi_calculation: str = "") -> Union[int, float, list]:

    import gc

    if not isinstance(lst, list):
        return lst

    nums_lst = var_in_list(lst, int, only_return_lst=True) + var_in_list(lst, float, only_return_lst=True)

    if not nums_lst:
        return lst
    else:
        result: int = nums_lst[0]
        if multi_calculation == "":
            result: int = nums_lst[0]
            nums_lst.pop(0)
            for _i in range(len(nums_lst)):
                if calculation == "+":
                    result += nums_lst[_i]
                elif calculation == "-":
                    result -= nums_lst[_i]
                elif calculation == "*":
                    result *= nums_lst[_i]
                elif calculation == "**":
                    result **= nums_lst[_i]
                elif calculation == "/":
                    result /= nums_lst[_i]
                elif calculation == "//":
                    result //= nums_lst[_i]
                elif calculation == "%":
                    result %= nums_lst[_i]
        else:
            lst_cal = multi_calculation.split(",")
            if len(lst_cal) > len(nums_lst) - 1:
                lst_cal = list(multi_calculation)[:len(nums_lst):]
            elif len(lst_cal) < len(nums_lst) - 1:
                lst_cal_copy = lst_cal.copy()
                lst_cal_copy_subscript: int = 0
                tmp_lst = [_ for _ in range(0, len(nums_lst), len(lst_cal))]
                for _i in range(len(nums_lst) - 1 - len(lst_cal)):
                    if _i in tmp_lst:
                        lst_cal_copy_subscript = 0
                    lst_cal.append(lst_cal_copy[lst_cal_copy_subscript])
                    lst_cal_copy_subscript += 1
            for _i in range(len(nums_lst)):
                if _i == 0:
                    continue
                if _i == len(lst_cal) + 1:
                    break
                if lst_cal[_i - 1] == "+":
                    result += nums_lst[_i]
                elif lst_cal[_i - 1] == "-":
                    result -= nums_lst[_i]
                elif lst_cal[_i - 1] == "*":
                    result *= nums_lst[_i]
                elif lst_cal[_i - 1] == "**":
                    result **= nums_lst[_i]
                elif lst_cal[_i - 1] == "/":
                    result /= nums_lst[_i]
                elif lst_cal[_i - 1] == "//":
                    result //= nums_lst[_i]
                elif lst_cal[_i - 1] == "%":
                    result %= nums_lst[_i]

    try:
        del nums_lst
        del lst_cal
        del lst_cal_copy, lst_cal_copy_subscript, tmp_lst
    except UnboundLocalError:
        pass
    gc.collect()

    return result


def csv_to_lst_or_dic(csv, dict_mode: bool = False) -> Union[list, dict, None]:

    try:
        import pandas as pd
    except ModuleNotFoundError:
        return

    if not isinstance(csv, pd.DataFrame):
        return

    dict_mode = bool(dict_mode)

    if not dict_mode:
        two_dimensional_arrays: list = []
        columns = csv.columns.tolist()
        rows = csv[columns]

        for _i in range(len(columns)):
            two_dimensional_arrays.append([])
            for _j in range(csv.shape[0]):
                two_dimensional_arrays[_i].append(str(rows.loc[_j, columns[_i]]))

        return two_dimensional_arrays

    else:
        _dict: dict = {}
        columns = csv.columns.tolist()
        rows = csv[columns]

        for _i in range(len(columns)):
            _dict.update({f"{columns[_i]}": []})
            for _j in range(csv.shape[0]):
                _dict[columns[_i]].append(str(rows.loc[_j, columns[_i]]))

        return _dict


def len_sorted_lst(lst: list, reverse: bool = False, filtration: bool = True) -> list:

    if not isinstance(lst, list):
        return lst
    else:
        lst_t = lst.copy()
        other_lst: list = []
        for _i in range(len(lst)):
            if not isinstance(lst[_i], list) and filtration:
                other_lst.append(_i)
            elif not isinstance(lst[_i], list) and not filtration:
                other_lst.append(lst[_i])
        if other_lst and filtration:
            other_lst = list(reversed(other_lst))
            for _i in range(len(other_lst)):
                lst_t.pop(other_lst[_i])
        elif other_lst and not filtration:
            for _i in range(len(other_lst)):
                lst_t.remove(other_lst[_i])

    len_dic: dict = {}
    len_lsts: list
    new_lst: list = []

    for _i in range(len(lst_t)):
        len_dic.update({_i: len(lst_t[_i])})

    if reverse:
        len_lsts = list(reversed(sorted(len_dic.items(), key=lambda x: x[1])))
    else:
        len_lsts = sorted(len_dic.items(), key=lambda x: x[1])

    for _i in range(len(len_lsts)):
        new_lst.append(lst_t[len_lsts[_i][0]])

    if not filtration:
        for _i in range(len(other_lst)):
            new_lst.append(other_lst[_i])

    return new_lst


def populate_lsts(*args, _type=0, nesting: bool = False) -> None:

    if bool(nesting):
        args = args[0]

    for _i in range(len(args)):
        if not isinstance(args[_i], list):
            return

    len_dic: dict = {}
    len_lsts: list
    for _i in range(len(args)):
        len_dic.update({_i: len(args[_i])})

    len_lsts = list(reversed(sorted(len_dic.items(), key=lambda x: x[1])))
    for _i in range(len(len_lsts)):
        len_lsts[_i] = list(len_lsts[_i])

    for _i in range(len(len_lsts)):
        try:
            for _j in range(len_lsts[0][1] - len_lsts[_i + 1][1]):
                args[len_lsts[_i + 1][0]].append(_type)
        except IndexError:
            pass


def list_internal_situation(lst: list) -> None:

    def in_list_internal_situation(lst2: list) -> None:
        def cur() -> None:
            print('->', end=" ")

        if not isinstance(lst2, list):
            return
        if globals().get("$in_index") is None:
            globals().update({"$in_index": []})

        iter_lst = iter(lst2.copy())

        try:
            _i: int = 0
            while True:
                next(iter_lst)
                if globals().get("$in_index"):
                    for _j in range(len(globals().get("$in_index"))):
                        print("in_index({})".format(globals().get("$in_index")[_j]), end=" "), cur()
                print(f"{_i}", end=" "), cur(), print(f"value: {lst2[_i]}", end=" "), print(f"{type(lst2[_i])}")
                if isinstance(lst2[_i], list):
                    globals().get("$in_index").append(_i)
                    in_list_internal_situation(lst2[_i])
                _i += 1
        except StopIteration:
            if len(globals().get("$in_index")) == 0:
                globals().pop("$in_index")
            else:
                globals().get("$in_index").pop(len(globals().get("$in_index")) - 1)

    in_list_internal_situation(lst)
    try:
        globals().pop("$in_index")
    except KeyError:
        pass


def get_variable(value: Any) -> list:

    eligible_lst = []

    for __temp, __temp2 in globals().items():
        if __temp2 == value:
            eligible_lst.append(__temp)
    return eligible_lst


def index_len(__obj) -> int:

    i: int = -1
    if isinstance(__obj, list) or isinstance(__obj, dict) or isinstance(__obj, set):
        __obj = iter(__obj.copy())
    while True:
        try:
            next(__obj)
            i += 1
        except StopIteration:
            return i
