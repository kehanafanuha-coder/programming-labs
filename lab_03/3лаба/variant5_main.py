import sys
from variant5_mod import check_viscosity_range, group_by_grade, get_unique_impurities

max_v = float(sys.argv[1]) if len(sys.argv) > 1 else 7.0

raw_samples = [1.2, 2.5, 3.8, 7.5, 8.1, 4.2]
grades = {'Проба1': 'АИ-92', 'Проба2': 'АИ-95', 'Проба3': 'АИ-92'}
impurities = [{'вода', 'сера'}, {'сера', 'смолы'}]

valid = check_viscosity_range(raw_samples, max_v=max_v)
grouped = group_by_grade(grades)
unique_imp = get_unique_impurities(impurities)

print(f"Валидные пробы: {valid}")
print(f"Группы по сортам: {grouped}")
print(f"Уникальные примеси: {unique_imp}")