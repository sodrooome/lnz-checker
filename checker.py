import itertools, json, matplotlib
import matplotlib.pyplot


coverage_metrix = {"put": 0, "get": 0}


def assert_put(state, key, value):
    assert state.get(key) == value


def assert_get(state, key, exp_value):
    assert state.get(key) == exp_value


def assert_status_code(state, exp_status_code):
    assert state == exp_status_code


def is_linearizable(operations: list) -> bool:
    operations.sort(key=lambda x: x["start_time"])
    for permutate in itertools.permutations(operations):
        if check_linear_history(list(permutate)):
            return True
    return False


def check_linear_history(history: list) -> bool:
    initial_state = {}
    operation_list = []

    for operation in history:
        # name, _, _, result = operation
        name = operation["operation_name"].lower()
        status_code = operation["status_code"]

        if name == "put":
            request_payload = operation["request_payload"]
            k, v = request_payload["key"], request_payload["value"]
            if status_code in [200, 201]:
                initial_state[k] = v
            # assert_status_code(status_code, 200)
            coverage_metrix["put"] += 1
            operation_list.append(("put", k, v, status_code))

        elif name == "get":
            request_payload = operation["request_payload"]
            k = request_payload["key"]
            resp_payload = operation["response_payload"]
            if status_code in [200, 201]:
                expected_value = initial_state.get(k)
                if expected_value is not None:
                    assert resp_payload["data"]["value"] == expected_value
                else:
                    # instead of intercepting and terminate if there's an error raised,
                    # for now, all of the "expected failure" condition will be passed by,
                    # to give the clear visualization what's going on during sequences
                    print("just passing by")
            # assert_status_code(status_code, 200)
            coverage_metrix["get"] += 1
            operation_list.append(("get", k, resp_payload, status_code))

    visualize_checkers(operation_list)
    return True # wait, something buggy in here


def visualize_checkers(operations: list):
    _, ax = matplotlib.pyplot.subplots()
    y_labels = []
    y_values = []
    colors = []

    for idx, operation in enumerate(operations):
        # there is an issue in here
        op_type, k, v, status_code = operation
        y_labels.append(f"{op_type} {k}")
        y_values.append(idx)
        if status_code in [200, 201]:
            colors.append("green")
        else:
            colors.append("red")

    ax.scatter([1] * len(operations), y_values, c=colors, s=100)
    ax.set_yticks(y_values)
    ax.set_yticklabels(y_labels)
    ax.set_xticks([])

    for idx, operation in enumerate(operations):
        k, v, status_code = operation, operation, operation
        ax.text(1.01, idx, f"{v}", va="center")

    matplotlib.pyplot.show()


with open("failure_logs.json", "r") as f:
    logs = json.load(f)

# operations = [
#     ("put", 1, 2, ("x", 1)),
#     ("get", 3, 4, ("x", 1)),
#     ("put", 5, 6, ("x", 2)),
#     ("get", 7, 8, ("x", 2)),
# ]

operations = [log for log in logs]

print(is_linearizable(operations))
print(coverage_metrix)
