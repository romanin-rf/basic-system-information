from rich.console import Console
console = Console()

try: 
    import bsipack.bsi as bsi
    from rich.console import Console

    bsi.init(__file__)

    if __name__ == "__main__":
        bsi.start_bsi()

except: console.print_exception(word_wrap=True, show_locals=True)