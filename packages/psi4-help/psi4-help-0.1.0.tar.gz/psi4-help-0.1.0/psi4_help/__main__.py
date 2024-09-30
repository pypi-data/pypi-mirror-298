from .psi4_help import Psi4KeywordsCLI

def run_psi4_help():
    cli = Psi4KeywordsCLI()
    cli.cmdloop()