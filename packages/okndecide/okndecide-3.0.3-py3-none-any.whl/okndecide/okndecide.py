import sys
import argparse
import json
import commentjson
from ehdg_tools.ehdg_okn_checker import signal_checker, apply_okn_detection_rule


def main():
    parser = argparse.ArgumentParser(prog='okndecide',
                                     description='OKN config file modifier program.')
    parser.add_argument('--version', action='version', version='3.0.3'),
    parser.add_argument("-i", dest="input_file", required=True, default=sys.stdin,
                        help="input file", metavar="input file")
    parser.add_argument("-c", dest="config_file", required=True, default=sys.stdin,
                        help="config file", metavar="config file")
    parser.add_argument('-v', '--verbose', dest="verbose_boolean", help="verbose boolean",
                        action='store_true')

    args = parser.parse_args()
    input_file = str(args.input_file)
    config_file = str(args.config_file)
    verbose_boolean = args.verbose_boolean
    rule_found = False
    rule_set = None
    default_rule_set = None

    # Opening oknserver config
    with open(config_file) as f:
        config_info = commentjson.load(f)
        try:
            okn_rule = config_info["rule"]
            rule_found = True
        except KeyError:
            okn_rule = None
            if verbose_boolean:
                print("//OKN rule is not found!")
                print("//Looking for rule set.")
        if not okn_rule:
            try:
                rule_set = config_info["rule_set"]
                if verbose_boolean:
                    print("//Rule set is found.")
            except KeyError:
                print("OKN rule set is not found too!", file=sys.stderr)
                print("Please check spelling of \"rule\" in the given config.", file=sys.stderr)
                print("Example rule", file=sys.stderr)
                print("\"rule\": {\"min_chain_length\": 2, \"min_unchained_okn\": 3, "
                      "\"sptrack\": true, \"sp_long_limit\": 1.5}", file=sys.stderr)
                print(f"okndecide could not be run with this config {config_file}.", file=sys.stderr)
                print("Example rule set", file=sys.stderr)
                rule_set_example = {
                    "rule_set": [
                        {"name": "main1", "min_chain_length": 2, "min_unchained_okn": 3,
                         "sptrack": True, "sp_long_limit": 1.5},
                        {"name": "main2", "min_chain_length": 2, "min_unchained_okn": 4,
                         "sptrack": True, "sp_long_limit": 1.5},
                        {"name": "main3", "min_chain_length": 3, "min_unchained_okn": 3,
                         "sptrack": True, "sp_long_limit": 1.5},
                        {"name": "main4", "min_chain_length": 2, "min_unchained_okn": 2,
                         "sptrack": True, "sp_long_limit": 1.5}
                    ],
                    "default_rule_set": "main1",
                }
                j_obj = json.dumps(rule_set_example, indent=2)
                print(f"{j_obj}", file=sys.stderr)
        if rule_set:
            try:
                default_rule_set = config_info["default_rule_set"]
            except KeyError:
                print("OKN rule set is found but default rule set could not be found.!", file=sys.stderr)
                print(f"okndecide could not be run with this config {config_file}.", file=sys.stderr)
                print("Example rule set", file=sys.stderr)
                rule_set_example = {
                    "rule_set": [
                        {"name": "main1", "min_chain_length": 2, "min_unchained_okn": 3,
                         "sptrack": True, "sp_long_limit": 1.5},
                        {"name": "main2", "min_chain_length": 2, "min_unchained_okn": 4,
                         "sptrack": True, "sp_long_limit": 1.5},
                        {"name": "main3", "min_chain_length": 3, "min_unchained_okn": 3,
                         "sptrack": True, "sp_long_limit": 1.5},
                        {"name": "main4", "min_chain_length": 2, "min_unchained_okn": 2,
                         "sptrack": True, "sp_long_limit": 1.5}
                    ],
                    "default_rule_set": "main1",
                }
                j_obj = json.dumps(rule_set_example, indent=2)
                print(f"{j_obj}", file=sys.stderr)
        if default_rule_set:
            for rule in rule_set:
                if rule["name"] == default_rule_set:
                    okn_rule = rule
                    rule_found = True
                    break
            if not rule_found:
                print(f"Default rule set:{default_rule_set} "
                      f"could not be found in the rule set:{rule_set}.", file=sys.stderr)
        if rule_found:
            min_chain_length = okn_rule["min_chain_length"]
            min_unchained_okn = okn_rule["min_unchained_okn"]

            try:
                sptrack = okn_rule["sptrack"]
                if verbose_boolean:
                    print(f"//Rule:sptrack is found.")
                    print(f"//Rule:sptrack: {sptrack}")
            except TypeError:
                sptrack = None
            except KeyError:
                sptrack = None

            sp_long_limit = None
            if sptrack is not None:
                string_slow_phase_track = str(sptrack).lower()
                if string_slow_phase_track == "true":
                    if verbose_boolean:
                        print(f"//The sptrack is true.")
                        print(f"//Therefore, sptrack will be used in decision.")
                        print(f"//Looking for the sp_long_limit.")
                    try:
                        sp_long_limit = okn_rule["sp_long_limit"]
                        if verbose_boolean:
                            print(f"//Rule:sp_long_limit is found.")
                            print(f"//Rule:sp_long_limit: {sp_long_limit}")
                    except TypeError:
                        sp_long_limit = None
                        if verbose_boolean:
                            print(f"//WARNING: sp_long_limit is not found.")
                            print(f"//WARNING: the decision will be made without slow phase duration calculation.")
                    except KeyError:
                        sp_long_limit = None
                        if verbose_boolean:
                            print(f"//WARNING: sp_long_limit is not found.")
                            print(f"//WARNING: the decision will be made without slow phase duration calculation.")
                else:
                    if string_slow_phase_track == "false":
                        if verbose_boolean:
                            print(f"//The sptrack is false.")
                            print(f"//Therefore, sptrack will be not used in decision.")
                    else:
                        if verbose_boolean:
                            print(f"//The sptrack is neither true or false.")
                            print(f"//Therefore, sptrack will be not used in decision.")

            if verbose_boolean:
                print(f"//Rule:min_chain_length: {min_chain_length}")
                print(f"//Rule:min_unchained_okn: {min_unchained_okn}")
                if sp_long_limit is not None:
                    print(f"//Rule:sp_long_limit: {sp_long_limit}")

            signal_data = signal_checker(input_file, signal_csv_name=None, print_string=verbose_boolean)
            is_there_okn = apply_okn_detection_rule(signal_data, min_chain_length, min_unchained_okn,
                                                    min_sp_duration=sp_long_limit,
                                                    print_string=verbose_boolean)
            signal_data_max_chain_length = signal_data["max_chain_length"]
            signal_data_unchained_okn_total = signal_data["unchained_okn_total"]
            if sp_long_limit is not None:
                signal_data_max_sp_duration = signal_data["max_sp_duration"]

            if verbose_boolean:
                print(f"//Signal Result, max chain length:{signal_data_max_chain_length}")
                print(f"//Signal Result, unchained okn total:{signal_data_unchained_okn_total}")
                if sp_long_limit is not None:
                    print(f"//Signal Result, max slow phase duration:{signal_data_max_sp_duration}")
                yes_no_answer = "Yes" if is_there_okn is True else "No"
                print(f"//Is there OKN? {yes_no_answer}")

            config_info["max_chain_length"] = signal_data_max_chain_length
            config_info["unchained_okn_total"] = signal_data_unchained_okn_total
            if sp_long_limit is not None:
                config_info["max_sp_duration"] = signal_data_max_sp_duration
            config_info["okn_present"] = is_there_okn

            config_info_json = json.dumps(config_info, indent=2)

            print(config_info_json)
