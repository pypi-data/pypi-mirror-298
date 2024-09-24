from .grader import *
from .utils import construct_prompt
from .parser import *
from .trajectory import *
from .python_executor import PythonExecutor


def basic_check(pred, answer):
    """
    This function compares the prediction and the ground truth (answer),
    and returns True if they are the same, otherwise returns False.

    Args:
    pred: The predicted value or output from a model or function.
    answer: The ground truth to compare against.

    Returns:
    bool: True if the prediction is correct, otherwise False.
    """
    return math_equal(pred, answer, timeout=True)


def check(data_name, target, pred):
    prompt_type = "cot"
    # parse question and answer
    gt_cot, gt_ans = parse_ground_truth(target, data_name)

    base_path = os.path.dirname(__file__)
    if base_path.endswith("/"):
        base_path = base_path[:len(base_path) - 1]
    prompt_path = base_path + "/prompts"

    full_prompt = construct_prompt(target, data_name, prompt_type, prompt_path)
    sample = {'idx': 0, 'gt': gt_ans}

    # add remain fields
    for key in ['level', 'type', 'unit', 'solution_type', 'choices', 'solution', 'ques_type', \
        'ans_type', 'answer_type', 'dataset', 'subfield', 'filed', 'theorem', 'answer']:
        if key in target:
            sample[key] = target[key]

    end_prompts = []
    remain_prompts = []
    remain_codes = []

    output = pred.rstrip()
    query = full_prompt + output
    if prompt_type == "pal":
        remain_prompts.append((0, query))
        if "```python" in output:
            output = extract_program(query)
        remain_codes.append(output)
    elif prompt_type == "cot":
        end_prompts.append((0, query))
    elif ("boxed" not in output and output.endswith("```")):
        program = extract_program(query)
        remain_prompts.append((0, query))
        remain_codes.append(program)
    else:
        end_prompts.append((0, query))

    remain_results = []

    if len(remain_codes) > 0:
        code_snippet = PythonExecutor.process_generation_to_code(remain_codes)[0]

        try:
            if "pal" in prompt_type:
                result = PythonExecutor.execute(
                    code_snippet,
                    get_answer_from_stdout=False,
                    answer_expr='solution()',
                    timeout_length=5
                )
            else:
                result = PythonExecutor.execute(
                    code_snippet,
                    get_answer_from_stdout=True,
                    timeout_length=5
                )
            res, report = result
        except TimeoutError as error:
            print(error)
            res, report = "", "Timeout Error"
        except Exception as error:
            print(error)
            exit()

        res, report = PythonExecutor.truncate(str(res).strip()), PythonExecutor.truncate(str(report).strip())
        remain_results = [(res, report)]

    for k in range(len(remain_prompts)):
        i, query = remain_prompts[k]
        res, report = remain_results[k]
        exec_result = res if res else report
        if "pal" in prompt_type:
            exec_result = "\\boxed{" + exec_result + "}"
        exec_result = f"\n```output\n{exec_result}\n```\n"
        query += exec_result
        remain_prompts[k] = (i, query)

    # unsolved samples
    end_prompts.extend(remain_prompts)
    code = end_prompts[0][1].split(full_prompt)[-1].strip()
    sample.update({'code': [code]})
    gt_cot, gt = parse_ground_truth(sample, data_name)

    # execute
    if prompt_type in ["pot", "pal"]:
        if "pal" in prompt_type:
            executor = PythonExecutor(get_answer_expr="solution()")
        else:
            executor = PythonExecutor(get_answer_from_stdout=True)
    else:
        executor = None

    pred, report = run_execute(executor, code, prompt_type, data_name, execute=True)

    try:
        result = math_equal_process((0, pred, gt))
        return result
    except TimeoutError as error:
        print(error)
        return False
    except Exception as error:
        print(error)
        exit()
