"""Модуль для контроля качества нефтепродуктов (Вариант 5)."""

def check_viscosity_range(samples, min_v=2.0, max_v=8.0):
    return [s for s in samples if min_v <= s <= max_v]

def group_by_grade(oil_dict):
    result = {}
    for grade, sample in oil_dict.items():
        result.setdefault(sample, []).append(grade)
    return result

def get_unique_impurities(impurity_lists):
    return set().union(*impurity_lists)

if __name__ == '__main__':
    print(check_viscosity_range([1.5, 3.2, 9.1]))