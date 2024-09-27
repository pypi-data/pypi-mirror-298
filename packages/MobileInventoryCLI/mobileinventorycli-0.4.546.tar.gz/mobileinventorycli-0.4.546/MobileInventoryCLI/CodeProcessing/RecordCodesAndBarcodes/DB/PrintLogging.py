from pathlib import Path
from colored import Fore,Back,Style
import re
import sys
def print_factory(argument):
    def decorator(function):
        def wrapper(*args,**kwargs):
            print(args,kwargs)            
            return args,kwargs
        return wrapper
    return decorator
    
def prinL(*args,**kwargs):
    args=[str(i) for i in args]
    out_args=[]
    for num,i in enumerate(args):
        tmp=''
        for c in Back._COLORS:
            tmp=i.replace(getattr(Back,c),'')
        for c in Fore._COLORS:
            tmp=tmp.replace(getattr(Fore,c),'')
        for c in Style._STYLES:
            tmp=tmp.replace(getattr(Style,c),'')
        reaesc = re.compile(r'\x1b[^m]*m')
        new_text = reaesc.sub('', tmp)
        out_args.append(new_text)


    needs_clear=False
    total=0
    try:
        with Path("STDOUT.TXT").open("r") as ifile:
            total=len(ifile.readlines())
            if len(ifile.readlines()) >= 10000:
                needs_clear=True
        if needs_clear:
            with Path("STDOUT.TXT").open("w+") as out:
                out.write(f'')
    except Exception as e:
        print(e,"File will be created!")

    sep=' '
    if 'sep' in kwargs.keys():
        sep=kwargs.get("sep")

    with Path("STDOUT.TXT").open("a") as out:
        out.write(f'{str(f"{sep}".join(out_args))}\n')
    print(f"{Fore.grey_35}HFL:{total}{Style.reset}",*args,**kwargs)

def logInput(text):
        try:
            needs_clear=False
            with Path("STDOUT.TXT").open("r") as ifile:
                if len(ifile.readlines()) >= 10000:
                    needs_clear=True
            if needs_clear:
                with Path("STDOUT.TXT").open("w+") as out:
                    out.write(f'')
        except Exception as e:
            prinL(e,"File will be created!")

        try:
            with Path("STDOUT.TXT").open("a") as out:
                out.write(f'#USER INPUT# -> :"{text}"\n')
        except Exception as e:
            prinL(e)