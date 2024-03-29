# calculate_profit

# import os


def filter_name(input_string, indices):
    words = input_string.split()
    selected_words = [words[min(i, len(words) - 1)] for i in indices]
    result = " ".join(selected_words)
    return result


def filter_types(objects, object_types, name_slices):
    filtered_objs = {item: [] for item in object_types}
    for obj in objects:
        obj["name"] = filter_name(obj.get("name"), name_slices)
        for obj_type in object_types:
            if obj_type in obj.get("name") and "Skittering" not in obj.get("name"):
                filtered_objs[obj_type].append(obj)
    return filtered_objs


def get_total_chaos_value(objects):
    total_chaos_value = sum(obj.get("chaosValue") for obj in objects)
    return total_chaos_value


def start_calculations(
    OBJECT_NAME,
    object_types,
    LIFEFORCE_PER_REFORGE,
    LIFEFORCE_PER_CHAOS,
    CHAOS_AQUISITION_TYPES,
    FILE_DESTINATION,
    STACK_LIMIT,
    CURRENCY_DATA,
):
    with open(FILE_DESTINATION, "a") as file:
        file.write(f"\n----------{OBJECT_NAME}----------\n\n")
    chaos_per_reforge = LIFEFORCE_PER_REFORGE / LIFEFORCE_PER_CHAOS

    for object_type, objects in object_types.items():
        total_chaos_value = get_total_chaos_value(objects)
        profitable_objects, unprofitable_objects, average_profits = maximize_profit(
            objects,
            total_chaos_value,
            chaos_per_reforge,
            CHAOS_AQUISITION_TYPES[object_type],
        )

        if profitable_objects is not None:
            # file_name = f"{file_destination}_{object_type.lower()}.txt"
            write_to_file(FILE_DESTINATION, profitable_objects, average_profits)
            with open(FILE_DESTINATION, "a") as file:
                file.write(
                    f"Average Profit ({STACK_LIMIT}x): {round(average_profits * STACK_LIMIT, 2)} \n"
                )

                stacks_per_div = get_stacks_per_div(
                    CHAOS_AQUISITION_TYPES[object_type], CURRENCY_DATA
                )

                file.write(
                    f"Average Profit per Div ({round(stacks_per_div, 2)}x): {round(average_profits * stacks_per_div, 2)} \n"
                )

                lower_type_cheaper, next_type = check_lower_type(
                    CHAOS_AQUISITION_TYPES, object_type
                )
                if lower_type_cheaper:
                    file.write(f"Upgrading {next_type} is Profitable\n")
                else:
                    file.write(f"Upgrading {next_type} is NOT Profitable\n")

                file.write(f"Buy {unprofitable_objects}\n\n")

        else:
            with open(FILE_DESTINATION, "a") as file:
                file.write(f"{object_type} Not Profitable\n\n")

    # os.system(f"start {FILE_DESTINATION}")


def get_stacks_per_div(type_chaos, CURRENCY_DATA):
    divine_chaos = next(
        (
            item["chaosEquivalent"]
            for item in CURRENCY_DATA
            if "Divine Orb" in item["currencyTypeName"]
        ),
        None,
    )

    if divine_chaos:
        stacks_per_div = divine_chaos / type_chaos
        return stacks_per_div
    else:
        return None


def check_lower_type(CHAOS_AQUISITION_TYPES, current_type):
    keys = list(CHAOS_AQUISITION_TYPES.keys())

    index = keys.index(current_type)

    if index < len(keys) - 1:
        next_type = keys[index + 1]
        next_value = CHAOS_AQUISITION_TYPES[next_type]

        if CHAOS_AQUISITION_TYPES[current_type] >= 3 * next_value:
            return True, next_type

    return False, None


def maximize_profit(
    objects,
    total_chaos_value,
    chaos_per_reforge,
    chaos_acquisition,
):
    valuable_objects = []
    unvaluable_objects = []
    num_objects = len(objects)

    total_revenue = 0

    for obj in objects:
        potential_profit = (total_chaos_value - obj.get("chaosValue")) / (
            num_objects - 1
        ) - chaos_per_reforge

        if obj.get("chaosValue") >= potential_profit:
            valuable_objects.append(obj)
            total_revenue += obj.get("chaosValue")
        else:
            unvaluable_objects.append(obj.get("name").split()[-1])

    num_valuable_objects = len(valuable_objects)

    if valuable_objects:
        average_revenue = round(total_revenue / len(valuable_objects), 2)

        average_cost = (
            num_objects / num_valuable_objects * chaos_per_reforge + chaos_acquisition
        )

        if average_revenue > average_cost:
            average_profit = round(average_revenue - average_cost, 2)
            return valuable_objects, unvaluable_objects, average_profit

    return None, None, None


def write_to_file(file_name, objects, average_profit):
    with open(file_name, "a") as file:
        for obj in objects:
            formatted_line = f"{obj.get('name'):20} | {obj.get('chaosValue'):10}"
            file.write(formatted_line + "\n")
        # file.write(f"Average Profit: {average_profit} \n")
