import os
import json
import subprocess
import argparse

def extract_test_words(file_path):
    test_words = []

    with open(file_path, "r") as file:
        for line in file:
            if line.startswith("Test:"):
                test_word = line.split("Test:")[1].strip()
                if ".py" in test_word:
                    continue
                test_words.append(test_word + ".json")

    return test_words

def find_and_read_json(json_name, search_directory):
    for root, _, files in os.walk(search_directory):
        for file in files:
            if file == json_name:
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r") as json_file:
                        data = json.load(json_file)
                        relative_path = os.path.relpath(file_path, search_directory)
                        return relative_path.replace(os.sep, "/"), data
                except Exception as e:
                    print(f"Error al leer {file_path}: {e}")
    return None, None

def process_jsons(json_list, search_directory):

    results = {}

    for json_name in json_list:
        file_key, data = find_and_read_json(json_name, search_directory)
        if data is not None:
            results[file_key] = data
        else:
            print(f"No se encontró el archivo: {json_name}")

    return results

def execute_evmasm(bytecode):
    try:
        process = subprocess.run(
            ["evmasm", "-d"],
            input=bytecode,
            text=True,
            capture_output=True,
            check=True
        )
        return process.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error ejecutando evmasm: {e.stderr}")
        return None


def analyze_opcodes(opcodes):
    target_opcodes = {"CALL", "CREATE", "CREATE2"}
    found_opcodes = set()

    for line in opcodes.splitlines():
        parts = line.split(":")
        if len(parts) > 1:
            opcode = parts[1].strip().split()[0]
            if opcode in target_opcodes:
                found_opcodes.add(opcode)

    if len(found_opcodes) == 0:
        return "No CALL, CREATE, or CREATE2 found."
    elif len(found_opcodes) == 1:
        return f"Found: {', '.join(found_opcodes)}."
    else:
        return f"Multiple opcodes found: {', '.join(found_opcodes)}."


def process_json(data):
    for key, value in data.items():
        post = value.get("post")
        if not post or "Cancun" not in post:
            print("Test is not Cancun.")
            continue

        transaction = value.get("transaction", {})
        pre = value.get("pre", {})

        if "to" in transaction and transaction["to"]:
            # Transacción con 'to'
            to = transaction["to"]
            to_data = pre.get(to)
            if to_data and "code" in to_data:
                code = to_data["code"]
                opcodes = execute_evmasm(code)
                print(f"CALL Transaction - to: {to}:")
                if opcodes:
                    print(opcodes)
                    analysis = analyze_opcodes(opcodes)
                    print(analysis)
            else:
                print(f"No 'code' found for 'to': {to}")


        else:
            # Transacción CREATE
            print(f"CREATE Transaction - sender: {transaction.get('sender')}")

def main():
    parser = argparse.ArgumentParser(
        description="Process JSON files and analyze opcodes from LEVM test results."
    )
    parser.add_argument(
        "--path",
        help="Path to the LEVM test folder containing 'levm_ef_tests_report.txt' and the 'vectors' directory.",
        required=True,
    )
    args = parser.parse_args()

    if not os.path.exists(args.path):
        print(f"Error: The provided path '{args.path}' does not exist.")
        return

    txt_test_path = os.path.join(args.path, "levm_ef_tests_report.txt")
    search_directory = os.path.join(args.path, "vectors")

    if not os.path.isfile(txt_test_path):
        print(f"Error: File '{txt_test_path}' not found.")
        return

    if not os.path.isdir(search_directory):
        print(f"Error: Directory '{search_directory}' not found.")
        return

    json_list = extract_test_words(txt_test_path)
    results = process_jsons(json_list, search_directory)

    print(f"JSON que fallan: {len(json_list)}. Leídos de vector: {len(results)}")

    for key, value in results.items():
        print(key)
        process_json(value)


if __name__ == "__main__":
    main()
