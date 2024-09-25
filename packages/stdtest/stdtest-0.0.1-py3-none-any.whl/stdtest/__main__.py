from argparse import ArgumentParser
from .listener import listen
from .combine import combine
import os, sys
from .testsync import test
import json

def main():
    try:
        p = ArgumentParser(prog="StdTest", description="standard test")
        # p.add_argument("solver")
        # p.add_argument("-i", dest="input", default="i.txt", help="test input file")
        # p.add_argument("-o", dest="output", help="test answer file")
        
        subp = p.add_subparsers(title="subcommands", dest="subcommand")
        
        comp = subp.add_parser("compare", aliases=["check", "verdict"])
        comp.add_argument("solver")
        comp.add_argument("-i", dest="input")
        comp.add_argument("-o", dest="output")
        comp.add_argument("-g", dest="generator")
        comp.add_argument("-c", dest="checker")
        comp.add_argument("-cpu", dest="cpulimit", type=int, default="1", help="<= (cpu) seconds")
        comp.add_argument("-mem", dest="memlimit", type=int, default="256", help="<= (mem) megabytes")
        comp.add_argument("-ff", dest="failed_first", action="store_true", default=True)

        intp = subp.add_parser("interact")
        intp.add_argument("solver")
        intp.add_argument("checker")
        intp.add_argument("-i", dest="input")
        intp.add_argument("-g", dest="generator")
        intp.add_argument("-cpu", dest="cpulimit", type=int, default="1", help="<= (cpu) seconds")
        intp.add_argument("-mem", dest="memlimit", type=int, default="256", help="<= (mem) megabytes")
        intp.add_argument("-ff", dest="failed_first", action="store_true", default=True)

        listenp = subp.add_parser("listen")
        listenp.add_argument("-p", dest="port", type=int, default=27121)

        newp = subp.add_parser("new")
        newp.add_argument("taskname")
        newp.add_argument("-f", dest="isfile", action="store_true", default=False)

        combp = subp.add_parser("combine")
        combp.add_argument("file")

        args = p.parse_args()

        match args.subcommand:
            case "listen":
                print(f"Listen for [+ Competitive Companion] on {args.port}...")
                listen(args.port)
            case "combine":
                print(combine(args.file))
            case "compare" | "check" | "verdict":
                task = json.loads(open("task.json").read())
                cpu = args.cpulimit
                mem = args.memlimit
                if not args.input and not args.output and not args.generator and not args.checker:
                    tests = list(map(lambda d: (d["input"], d["output"]), task["tests"]))
                    test(args.solver, tests, cpu, mem)
            case "interact":
                pass

    except KeyboardInterrupt:
        sys.exit(0)
    except BaseException as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()