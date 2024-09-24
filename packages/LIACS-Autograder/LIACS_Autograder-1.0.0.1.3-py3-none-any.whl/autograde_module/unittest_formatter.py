import re
import sys
import unittest
from unittest.result import STDOUT_LINE, STDERR_LINE

class MyTextTestRunner(unittest.TextTestRunner):
    def __init__(self, *args, max_unittest_code_lines_4_report=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_unittest_code_lines_4_report = max_unittest_code_lines_4_report

    def _makeResult(self):
        return MyTextTestResult(self.stream, self.descriptions, self.verbosity, self.max_unittest_code_lines_4_report)

class MyTextTestResult(unittest.runner.TextTestResult):
    def __init__(self, stream, descriptions, verbosity, max_unittest_code_lines_4_report):
        super().__init__(stream, descriptions, verbosity)
        self.max_unittest_code_lines_4_report = max_unittest_code_lines_4_report

    def _exc_info_to_string(self, err, test):
        """Converts a sys.exc_info()-style tuple of values into a string."""
        exctype, value, tb = err
        tb = self._clean_tracebacks(exctype, value, tb, test)

        # This tries to find the local variables and print them using their representation (repr)
        # unittest.runner.result.traceback.TracebackException creates the std feedback report
        variables_not_printed = None
        try:
            tb_e = unittest.runner.result.traceback.TracebackException(
                exctype, value, tb,
                capture_locals=self.tb_locals, compact=True)
        except:  # There is an error in the repr method, this can be almost any error therefore except everything
            tb_e = unittest.runner.result.traceback.TracebackException(
                exctype, value, tb,
                capture_locals=None, compact=True)
            variables_not_printed = "Variables can not be printed as some of them have an incorrect __repr__ method!"

        # the error message as a list of messages
        msgLines = list(tb_e.format())

        # find the error of the student.
        for msg in msgLines:
            try:
                file = re.search('".*py"', msg.split("\n")[0].split(",")[0])[0][1:-1]
                line = int(re.split(' line ', msg.split("\n")[0].split(",")[1])[1])
            except TypeError:
                pass
            else:
                break

        # add the variables at the right place
        if variables_not_printed is not None:
            msgLines.insert(0, variables_not_printed)

        # add the (partial) unittest code that created the error
        test_case = "Partial Unittest Code:\n"
        with open(file, 'r') as f:
            test_case += "".join(f.readlines()[line-self.max_unittest_code_lines_4_report:line+1])
        msgLines.insert(0, test_case)

        # original code, see source code
        if self.buffer:
            output = sys.stdout.getvalue()
            error = sys.stderr.getvalue()
            if output:
                if not output.endswith('\n'):
                    output += '\n'
                msgLines.append(STDOUT_LINE % output) # what is this?
            if error:
                if not error.endswith('\n'):
                    error += '\n'
                msgLines.append(STDERR_LINE % error) # what is this?
        return ''.join(msgLines)
