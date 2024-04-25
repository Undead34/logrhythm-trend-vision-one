import winreg
import os

def logs_cleanup():
    log_sources = os.environ.get("LOG_SOURCES_ID").split(",")
    
    if len(log_sources) == 0:
        print("Log source IDs are invalid")
    for index in range(len(log_sources)):
        log_sources[index] = log_sources[index].strip()

    for id in log_sources:
        _clear_logs(id)


def _clear_logs(log_source_id: str):
    try:
        # X:\LogRhythm\LogRhythm System Monitor\state\[ID]
        state_path_RAW = f"{_get_agent_state()}state\\{log_source_id}"
        state_path = os.path.normpath(state_path_RAW)

        print(f"Cleaning residues for agent {state_path}")

        file_count = 0

        if not os.path.exists(state_path):
            print("[Aborting!] LogRhythm status directory not found.")
            return

        # Iterate through all files in the directory
        for file in os.listdir(state_path):
            if not file.endswith(".pos"):
                continue

            try:
                with open(os.path.join(state_path, file), "r") as f:  # Open the file
                    # Pos file example content:
                    # X:\path\to\vision_one.log
                    # 12478343
                    # 638408987240279906
                    # pos_file = [path, number, number]
                    pos_file = f.read().split("\n")

                    # Check if the file exists
                    if not os.path.exists(pos_file[0]):
                        continue

                    # Check if the file size is equal to the size in the .pos file
                    if os.path.getsize(pos_file[0]) == int(pos_file[1]):
                        os.remove(pos_file[0])
                        print(f"Read of {pos_file[0]} complete.")
                        file_count += 1
            except Exception as e:
                print(f"Type: {type(e)}\n{e}")

        print(f"{file_count} files removed.")
    except Exception as e:
        print(f"Type: {type(e)}\n{e}")


def _get_agent_state():
    """
        Getting Agent state location from registry.
    """
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                             r"SOFTWARE\LogRhythm\scsm")
        agent_state, _ = winreg.QueryValueEx(key, "STATEPATH")
        return agent_state
    except FileNotFoundError:
        raise print(
            "The agent status location could not be found. Please make sure that the agent is installed.")
    except Exception as e:
        print(f"Type: {type(e)}\n{e}")


def get_region(code: str):
    """
        return URL for region by region code e.g US -> api.xdr.trendmicro.com
    """

    if code == "AU":
        return "api.au.xdr.trendmicro.com"
    elif code == "EU":
        return "api.eu.xdr.trendmicro.com"
    elif code == "IN":
        return "api.in.xdr.trendmicro.com"
    elif code == "JP":
        return "api.xdr.trendmicro.co.jp"
    elif code == "SG":
        return "api.sg.xdr.trendmicro.com"
    elif code == "US":
        return "api.xdr.trendmicro.com"
    elif code == "USGOV":
        return "api.usgov.xdr.trendmicro.com"
    else:
        return "api.xdr.trendmicro.com"


def valid_unicode(t: str | bytes):
    try:
        t = t.encode() if isinstance(t, str) else t

        t.decode('utf-8')
        return True
    except UnicodeDecodeError:
        return False


def size_text_to_bytes(size: str):
    """
    Converts a size string to a number of bytes
    Args:
        size (str): The size string to convert
    Returns:
        int: The number of bytes
    """
    size = size.upper()

    if size and size[-1] == "B":
        size = size[:-1]
    if size and (size[-1] == "K" or size[-2:] == "KB"):
        return int(float(size[:-1]) * 1000)
    elif size and (size[-1] == "M" or size[-2:] == "MB"):
        return int(float(size[:-1]) * 1000 * 1000)
    elif size and (size[-1] == "G" or size[-2:] == "GB"):
        return int(float(size[:-1]) * 1000 * 1000 * 1000)
    else:
        return int(size)


def dict_to_key_value(d, parent_key='', sep='_'):
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}".upper() if parent_key else k.upper()
        if isinstance(v, dict):
            items.extend(dict_to_key_value(v, new_key, sep=sep).items())
        elif isinstance(v, list):
            for i, item in enumerate(v):
                if isinstance(item, dict):
                    items.extend(dict_to_key_value(
                        item, f"{new_key}_EXTRA_INFO_{i}", sep=sep).items())
                else:
                    items.append((f"{new_key}_EXTRA_INFO_{i}", item))
        else:
            items.append((new_key, v))
    return dict(items)


def order_dict_by_relevance(d, whitelist):
    # Split the whitelist into a list
    whitelist = whitelist.split()

    # Create two empty dictionaries
    whitelisted_dict = {}
    non_whitelisted_dict = {}

    # Iterate over the items in the dictionary
    for k, v in d.items():
        # If the key is in the whitelist, add it to the whitelisted_dict
        if k in whitelist:
            whitelisted_dict[k] = v
        # Otherwise, add it to the non_whitelisted_dict
        else:
            non_whitelisted_dict[k] = v

    # Merge the two dictionaries
    ordered_dict = {**whitelisted_dict, **non_whitelisted_dict}

    # Return the ordered dictionary
    return ordered_dict
