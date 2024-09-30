import yaml,cmd,os,sys
from colorama import Fore, Back, Style, init
from pkg_resources import resource_filename
init(autoreset=True)
def print_tree(data, indent=0):
    if isinstance(data, dict):
        for key, value in data.items():
            print(f"{Colors.BOLD}{' ' * indent}{key}{Colors.RESET}")
            print_tree(value, indent + 2)
    elif isinstance(data, list):
        for item in data:
            print_tree(item, indent + 2)
    else:
        print(f"{' ' * (indent + 2)}{data}")
class Colors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'

    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'
def read_yaml(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)
def print_all(file):
    top_keys1=list(file.keys())
    for top_keys in top_keys1:
        print(f"{Colors.BOLD}{Colors.BG_RED}{top_keys}{Colors.RESET}")
        top2_keys=list(file[top_keys].keys())
        for l in top2_keys:
            #print(file[top_keys][l])
            l1="%30s"%l
            type="%12s"%file[top_keys][l]["type"]
            default="%12s"%file[top_keys][l]["default"]
            descrip=file[top_keys][l]["description"]
            try:
                optional="%30s"%file[top_keys][l]["optional"]
                print("      "+f"{Colors.UNDERLINE}{Colors.RED}{l1}{Colors.RESET}"+"    "
                f"{Colors.BLUE}{type}{Colors.RESET}"+"    "+f"{Colors.BOLD}{Colors.WHITE}{default}{Colors.RESET}"\
                +"    "+f"{Colors.BOLD}{Colors.WHITE}{optional}{Colors.RESET}" +"  "+ descrip)
            except:
                print("      "+f"{Colors.UNDERLINE}{Colors.RED}{l1}{Colors.RESET}"+"    "
                f"{Colors.BLUE}{type}{Colors.RESET}"+"    "+f"{Colors.BOLD}{Colors.WHITE}{default}{Colors.RESET}"+"  "+ descrip)
def print_all_keys(file):
    top_keys1=list(file.keys())
    for top_keys in top_keys1:
        print(f"{Colors.BOLD}{Colors.BG_RED}{top_keys}{Colors.RESET}")
        top2_keys=list(file[top_keys].keys())
        for l in top2_keys:
            #print(file[top_keys][l])
            l1="%30s"%l
            type="%12s"%file[top_keys][l]["type"]
            default="%12s"%file[top_keys][l]["default"]
            try:
                optional="%30s"%file[top_keys][l]["optional"]
                print("      "+f"{Colors.UNDERLINE}{Colors.RED}{l1}{Colors.RESET}"+"    "
                f"{Colors.BLUE}{type}{Colors.RESET}"+"    "+f"{Colors.BOLD}{Colors.WHITE}{default}{Colors.RESET}"\
                +"    "+f"{Colors.BOLD}{Colors.WHITE}{optional}{Colors.RESET}")
            except:
                print("      "+f"{Colors.UNDERLINE}{Colors.RED}{l1}{Colors.RESET}"+"    "
                f"{Colors.BLUE}{type}{Colors.RESET}"+"    "+f"{Colors.BOLD}{Colors.WHITE}{default}{Colors.RESET}")
def print_top_keys(yaml_data):
    top_keys=list(yaml_data.keys())
    print(f"{Colors.RED}keys number: %s{Colors.RESET}"%len(top_keys))
    for i, keyword in enumerate(top_keys, 1):
        l1="%10s"%keyword
        print(f"{Colors.BOLD}{Colors.BG_RED}{l1}{Colors.RESET}", end="\t")
        if i % 6 == 0:
            print()
    
def print_top2_keys(file,top_keys, des=False):
    top2_keys=list(file[top_keys].keys())
    print(f"{Colors.BOLD}{Colors.BG_RED}{top_keys}{Colors.RESET}")
    for l in top2_keys:
        #print(file[top_keys][l])
        l1="%30s"%l
        type="%12s"%file[top_keys][l]["type"]
        default="%12s"%file[top_keys][l]["default"]
        descrip=file[top_keys][l]["description"]
        if not des:
            try:
                optional="%30s"%file[top_keys][l]["optional"]
                print("      "+f"{Colors.UNDERLINE}{Colors.RED}{l1}{Colors.RESET}"+"    "
                f"{Colors.BLUE}{type}{Colors.RESET}"+"    "+f"{Colors.BOLD}{Colors.WHITE}{default}{Colors.RESET}"\
                +"    "+f"{Colors.BOLD}{Colors.WHITE}{optional}{Colors.RESET}")
            except:
                print("      "+f"{Colors.UNDERLINE}{Colors.RED}{l1}{Colors.RESET}"+"    "
                f"{Colors.BLUE}{type}{Colors.RESET}"+"    "+f"{Colors.WHITE}{default}{Colors.RESET}")
        else:
            try:
                optional="%30s"%file[top_keys][l]["optional"]
                print("      "+f"{Colors.UNDERLINE}{Colors.RED}{l1}{Colors.RESET}"+"    "
                f"{Colors.BLUE}{type}{Colors.RESET}"+"    "+f"{Colors.BOLD}{Colors.WHITE}{default}{Colors.RESET}"\
                +"    "+f"{Colors.BOLD}{Colors.WHITE}{optional}{Colors.RESET}" +"  "+ descrip)
            except:
                print("      "+f"{Colors.UNDERLINE}{Colors.RED}{l1}{Colors.RESET}"+"    "
                f"{Colors.BLUE}{type}{Colors.RESET}"+"    "+f"{Colors.WHITE}{default}{Colors.RESET}" +"  "+ descrip)

class Psi4KeywordsCLI(cmd.Cmd):
    intro = "Welcome to the Psi4 Keywords CLI. Type help or ? to list commands.\n Type \"show <module>\" like \"show ADC\".  \n \
Or use \"show <module> d\" to show description \n \"top\" or \"mod\" for module keys.\n"
    prompt = "(psi4_help-cli) $ "
    def __init__(self):
        super().__init__()
        file_path = resource_filename('psi4_help', 'psi4_keywords.yaml')
        self.yaml_data = read_yaml(file_path)
        print_top_keys(self.yaml_data)
    def do_exit(self, arg):
        """Exit the CLI."""
        print("Exiting...")
        return True
    def do_e(self, arg):
        """Exit the CLI."""
        print("Exiting...")
        return True
#    def do_list(self, arg):
#        """List all top-level PSI4 keys."""
#        print_top_keys(self.yaml_data)
    def do_mod(self, arg):
        """List all top-level PSI4 keys."""
        print_top_keys(self.yaml_data)
    def do_module(self, arg):
        """List all top-level PSI4 keys."""
        print_top_keys(self.yaml_data)
    def do_mod(self, arg):
        """List all top-level PSI4 keys."""
        print_top_keys(self.yaml_data)
    def do_top(self, arg):
        """List all top-level PSI4 keys."""
        print_top_keys(self.yaml_data)

    def do_all(self, arg):
        """List all PSI4 keys."""
        print_all_keys(self.yaml_data)
    def do_all_keys(self, arg):
        """List all PSI4 keys."""
        print_all_keys(self.yaml_data)

    def do_show(self, arg):
        """Show detailed information for a specific top-level key.
        Usage: show <top_key> [des]
        Example: show DETCI
                 show DETCI des
        """
        args = arg.split()
        if not args:
            print("Usage: show <top_key> [des]")
            return
        top_key = args[0].upper()
        with_description = len(args) > 1 and args[1] in 'description'
        if top_key in self.yaml_data:
            print_top2_keys(self.yaml_data, top_key, with_description)
        else:
            print(f"Top-level key '{top_key}' not found.")
    def do_list(self, arg):
        """Show detailed information for a specific top-level key.
        Usage: show <top_key> [des]
        Example: show DETCI
                 show DETCI des
        """
        args = arg.split()
        if not args:
            print("Usage: show <top_key> [des]")
            return
        top_key = args[0].upper()
        with_description = len(args) > 1 and args[1] in 'description'
        if top_key in self.yaml_data:
            print_top2_keys(self.yaml_data, top_key, with_description)
        else:
            print(f"Top-level key '{top_key}' not found.")
    
    def do_tree(self, arg):
        """Print the tree structure of the YAML file."""
        print_tree(self.yaml_data)

if __name__ == "__main__":
    Psi4KeywordsCLI().cmdloop()