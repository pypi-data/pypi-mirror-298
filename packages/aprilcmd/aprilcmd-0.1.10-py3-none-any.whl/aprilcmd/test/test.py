from util.conf import *
import sys
import io
old_stdout = sys.stdout
new_stdout = io.StringIO()
sys.stdout = new_stdout
try:
    help(JsonConfigFile.add)
finally:
    sys.stdout = old_stdout

help_output = new_stdout.getvalue()
print(help_output)

print("init")
testf = JsonConfigFile("./testf",None)
print('add {"a":1, "b":2}')
testf.add("",{"a":1, "b":2})
print('add {"a":3, "c":1}')
testf.add("",{"a":3, "c":1})
print(testf.get(""))
print('add c haha')
testf.add("c","haha")
print(testf.get(""))
print('set b tt')
testf.set("b","tt")
print(testf.get(""))