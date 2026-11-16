# Задание 5. Заполнение резервуара
def fill_tank_simulation(v_max, v_inc):
    """
    Моделирует подачу жидкости в резервуар порциями.
    Возвращает итоговый объем и количество импульсов насоса.
    """
    current_volume = 0.0
    pulses_count = 0
    limit_volume = v_max * 0.95
    
    print(f"--- Запуск симуляции заполнения (Макс. объем: {v_max} л, Порция: {v_inc} л) ---")
    
    while True:
        # Защита от бесконечного цикла, если порция больше объема резервуара
        if pulses_count > 10000: 
            print("Симуляция прервана: превышен лимит импульсов.")
            break
            
        pulses_count += 1
        
        # Проверяем, не превысит ли следующая порция 95% объема
        if current_volume + v_inc >= limit_volume:
            # Наливаем ровно до 95% (последняя неполная порция)
            current_volume = limit_volume
            print(f"Достигнуто 95% объема. Цикл завершен по break.")
            break
        else:
            current_volume += v_inc
            print(f"Импульс {pulses_count}: налито {current_volume:.2f} л.")
            
    return current_volume, pulses_count


# --- Блок тестирования и разбора результатов ---
print("\n=== ТЕСТ 1 ===")
# Пример: резервуар на 100 литров, насос качает по 10 литров за раз
total_vol, total_pulses = fill_tank_simulation(100.0, 10.0)
print(f"\nРезультат: Итоговый объем = {total_vol:.2f} л, Количество импульсов = {total_pulses}")

print("\n=== ТЕСТ 2 ===")
# Пример: резервуар на 50 литров, порция 7.5 литров
total_vol_2, total_pulses_2 = fill_tank_simulation(50.0, 7.5)
print(f"\nРезультат: Итоговый объем = {total_vol_2:.2f} л, Количество импульсов = {total_pulses_2}")