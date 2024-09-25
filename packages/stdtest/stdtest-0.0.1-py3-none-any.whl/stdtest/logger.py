import logging, os
import traceback
import sys
from datetime import datetime
import collections
import io
import shutil

def token_itr(s: str):
    for line in io.StringIO(s):
        for tk in line.split():
            if tk:
                yield tk
        yield "\n"

def formatanswer(s):
    return f"\033[3m{s}\033[0m"

def formatquery(s):
    return f"\033[9m{s}\033[0m"

def formatdiff(answer, actual):
    return f"{answer} ≠ {actual}"

def formatgreen(s):
    return f"\033[32m{s}\033[0m"
    
def formatred(s):
    return f"\033[31m{s}\033[0m"

def headline(s):
    return f"\033[4m{s}\033[0m"

class Logger:

    def __init__(self, testId: int) -> None:
        self.testId = testId

        # self.inputHead = headline(f"Test #{testId} input:")
        # self.outputHead = headline(f"Test #{testId} Output:")
        # self.verdictHead = headline(f"Test #{testId} Verdict:")
        # self.concludeHead = headline(f"Conclusion:")
        # self.actualToks = collections.deque()
        # self.answerToks = collections.deque()
        # self.idx = 0

    def title(self):
        print(f"Test #{self.testId}".center(shutil.get_terminal_size().columns), file=sys.stderr)
        
    def header(self, text: str):
        print(headline(f"{text.title()}:"), file=sys.stderr)
        
    def output(self, content: str):
        print(content, end="", flush=True, file=sys.stderr)

    def verdict(
            self, 
        cpu: int,
        cpulimit: int,
        mem: int,
        memlimit: int,
        scode: int = 0, 
        ccode: int = 0, 
        answer: io.TextIOBase = None,
        actual: io.TextIOBase = None,
        interactive: bool = False,
    ) -> bool:
        self.header("verdict")
        def print_footer(content: str):
            s = formatgreen(content) if "ok" in content.lower() else formatred(content)
            s += f" in {cpu}s and {mem}mb"
            print(s, flush=True, file=sys.stderr)
        if interactive:
            if scode:
                print_footer(
                    "A solution finishing with exit code other than 0 (without exceeding time \n"
                    "or memory limits) would be interpreted as a Runtime Error in the system."
                )
                return False
            elif ccode:
                print_footer(
                    "Fails: "
                    "A solution finishing with exit code 0 (without exceeding time \n"
                    "or memory limits) and a judge finishing with exit code other \n"
                    "than 0 would be interpreted as a Wrong Answer (or query limit exceeded) \n"
                    "in the system.\n"
                )
                return False
        else:
            if scode:
                print_footer(f"Solver exit with code {scode}")
                return False
            if ccode:
                print_footer(f"Comparator exit with code {scode}")
                return False
            if answer:
                WA = False
                actuals = [tk for line in actual for tk in line.split()]
                # for line in answer:
                #     for answerTk in line.split():
                #         actualTk = next(actuals, None)
                #         if actualTk:
                #             eq = True
                #             try:
                #                 eq = abs(float(answerTk) - float(actualTk)) < 1e-6
                #             except ValueError:
                #                 eq = actualTk == answerTk
                #             if not eq:
                #                 print(f"{formatdiff(answerTk, actualTk)}", end=" ", flush=True)
                #                 WA = True
                #             else:
                #                 print(formatanswer(answerTk), end=" ")
                #         else:
                #             print(formatanswer(answerTk), end=" ")
                #     print()
                # while True:
                #     actualTk = next(actuals, None)
                #     if not actualTk:
                #         break
                #     WA = True
                #     print(formatactual(answerTk), end="")
                answers = [tk for line in answer for tk in line.split()]
                rows = max(len(actuals), len(answers))
                rowW = len(str(rows))
                ACTUAL = "Actual"
                ANSWER = "Answer"
                actualW = max(len(ACTUAL), max(map(len, actuals)))
                answerW = max(len(ANSWER), max(map(len, answers)))
                
                print(f"{' ' * rowW} {ANSWER.rjust(answerW)} {ACTUAL.rjust(actualW)}")
                import itertools
                for row, (actualTk, answerTk) in enumerate(itertools.zip_longest(actuals, answers), start=1):
                    if not actualTk:
                        actualTk = ""
                    if not answerTk:
                        answerTk = ""
                    print(str(row).ljust(rowW), end="")
                    print(" ", end="")
                    print(answerTk.rjust(answerW), end="")
                    print(" ", end="")
                    print(' ' * (actualW - len(actualTk)), end="")
                    eq = True
                    try:
                        eq = abs(float(answerTk) - float(actualTk)) < 1e-6
                    except ValueError:
                        eq = actualTk == answerTk
                    if not eq:
                        actualTk = formatred(actualTk) 
                        WA = True
                    else:
                        actualTk = formatgreen(actualTk) 
                    print(actualTk)
                if WA:
                    print_footer("Wrong Answer")
                    return False
        if mem > memlimit:
            print_footer("Memory limit exceeded")
            return False
        if cpu > cpulimit:
            print_footer("Time limit exceeded")
            return False
        print_footer("OK")
        return True


    def conclusion(self, content: str):
        s = formatgreen(content) if "pass" in content.lower() else formatred(content)
        print(s.center(shutil.get_terminal_size().columns), file=sys.stderr)

    def query(self, content: str):
        print(formatquery(content), end="", flush=True, file=sys.stderr)
    
    def answer(self, content: str):
        print(formatanswer(content), end="", flush=True, file=sys.stderr)
    
    def error(self, content: str):
        print(formatred(content), end="", flush=True, file=sys.stderr)

    def info(self, content: str):
        print(content, end=("\n" if not content.endswith("\n") else ""), flush=True, file=sys.stderr)
    
    def clear(self):
        print("\033c\033[3J", file=sys.stderr)

logger = Logger(0)

# def excepthook(exc_type, exc_value, exc_tb):
#     tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
#     logger.exception(tb)

# sys.excepthook = excepthook
