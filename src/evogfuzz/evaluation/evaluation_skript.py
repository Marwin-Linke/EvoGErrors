import numpy as np

#Specify the paths to the .txt files with the corresponding outputs:
with open(r"evogfuzz_output.txt", "r") as f:
    output_evogfuzz = f.read()

with open(r"evogerrors_output.txt", "r") as f:
    output_evogerrors = f.read()

with open(r"evogerrors_output_1.txt", "r") as f:
    output_evogerrors_1 = f.read()


def find_all(a_string, sub):
    result = []
    k = 0
    while k < len(a_string):
        k = a_string.find(sub, k)
        if k == -1:
            return result
        else:
            result.append(k)
            k += 1
    return result

def durchschnitt(list):
    sum = 0
    for i in range(len(list)):
        sum += list[i]
    return (sum / len(list))

# Runtime evaluation
runtime_list_evogfuzz = []
runtime_list_evogerrors = []
runtime_list_evogerrors_1 = []
for i in find_all(output_evogfuzz, "Runtime") : 
    runtime_list_evogfuzz.append(float(str(output_evogfuzz[i:len(output_evogfuzz)].partition('\n')[0])[9:]))
for i in find_all(output_evogerrors, "Runtime") : 
    runtime_list_evogerrors.append(float(str(output_evogerrors[i:len(output_evogerrors)].partition('\n')[0])[9:]))
for i in find_all(output_evogerrors_1, "Runtime") : 
    runtime_list_evogerrors_1.append(float(str(output_evogerrors_1[i:len(output_evogerrors_1)].partition('\n')[0])[9:]))

#print(runtime_list_evogfuzz)
print(durchschnitt(runtime_list_evogfuzz))
print(np.median(runtime_list_evogfuzz))
#print(runtime_list_evogerrors)
print(durchschnitt(runtime_list_evogerrors))
print(np.median(runtime_list_evogerrors))
#print(runtime_list_evogerrors_1)
print(durchschnitt(runtime_list_evogerrors_1))
print(np.median(runtime_list_evogerrors_1))

buginputs_list_evogfuzz = []
for i in find_all(output_evogfuzz, "BugInputs") :
    buginputs_list_evogfuzz.append(int(str(output_evogfuzz[i:len(output_evogfuzz)].partition('\n')[0])[10:]))
#print(buginputs_list_evogfuzz)
#print(durchschnitt(buginputs_list_evogfuzz))

errorfound_list_evogfuzz = []
for i in buginputs_list_evogfuzz:
    errorfound_list_evogfuzz.append(int(i > 0))      
print(errorfound_list_evogfuzz) # How many different Exception types were found

errortypes_list_evogerrors = []
for i in find_all(output_evogerrors, "Exceptiontypes") :
    errortypes_list_evogerrors.append(int(str(output_evogerrors[i:len(output_evogerrors)].partition('\n')[0])[16:]))

print(errortypes_list_evogerrors)
print(durchschnitt(errortypes_list_evogerrors)) # How many different Exception types were found

errortypes_list_evogerrors_1 = []
for i in find_all(output_evogerrors_1, "Exceptiontypes") :
    errortypes_list_evogerrors_1.append(int(str(output_evogerrors_1[i:len(output_evogerrors_1)].partition('\n')[0])[16:]))

print(errortypes_list_evogerrors_1)
print(durchschnitt(errortypes_list_evogerrors_1)) # How many different Exception types were found

# Runtime per execution
print(durchschnitt(runtime_list_evogfuzz) / 10)
print(durchschnitt(runtime_list_evogerrors_1) / (1 * 65 + durchschnitt(errortypes_list_evogerrors_1) * 9))
print(durchschnitt(runtime_list_evogerrors) / (3 * 65 + durchschnitt(errortypes_list_evogerrors) * 7))

# Runtime as Boxplot
import matplotlib.pyplot as plt
import numpy as np

evogfuzz_color = "blue"
evogerrors_color = "#e0dc02"
evogerrors_1_color = "#dd4d6f"

def first_image():
    plt.plot(errorfound_list_evogfuzz, marker='o', label="EvoGFuzz", color=evogfuzz_color)
    plt.plot(errortypes_list_evogerrors_1, marker='o', label="EvoGErrors(1 Iteration)", color=evogerrors_1_color)
    plt.plot(errortypes_list_evogerrors, marker='o', label="EvoGErrors(3 Iterations)", color=evogerrors_color)
    plt.legend()
    plt.xlabel("Executions")
    plt.ylabel("Exception types")
    plt.title("Numer of found exception types")
    plt.show()
#first_image() # uncomment to get an image output

def boxplot(inp, title: str, xlabel: str, ylabel: str):
    plt.boxplot(inp)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()


#boxplot(runtime_list_evogfuzz, "Runtime EvoGFuzz", "", "Runtime in seconds")
#boxplot(runtime_list_evogerrors_1, "Runtime EvoGErrors (1 Iteration)", "", "Runtime in seconds")
#boxplot(runtime_list_evogerrors, "Runtime EvoGErrors (3 Iterations)", "", "Runtime in seconds")

#plt.figure(figsize=(10, 6))
#data = [runtime_list_evogfuzz, runtime_list_evogerrors_1]
#plt.boxplot(data, positions=[1, 2], labels=["EvoGFuzz", "EvoGErrors"])
#plt.ylim(ymin=0)
#plt.show()


# Extract ValueError from Probabilistic Grammar
# EvoGErrors 3 Iterations
terminal_list = ["<term> / <term>", "sqrt", "tan", "cos", "sin", "log", "len", "inc", "factorial", "is_int", "-<value>", "<integer>.<integer>", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"] # 23 nichtterminale
ValueError_list_evogerrors = []
temp_terminal_list = []
for terminal in terminal_list:
    temp_terminal_list.append(terminal)
    for i in find_all(output_evogerrors, "('"+terminal):
        line = str(output_evogerrors[i:len(output_evogerrors)].partition('\n')[0])[str(output_evogerrors[i:len(output_evogerrors)].partition('\n')[0]).find("ValueError")+13:]
        line = line[0:line.find(",")].replace("}", "")
        if not line == "None":
            temp_terminal_list.append(float(line))
    ValueError_list_evogerrors.append(durchschnitt(temp_terminal_list[1:]))
    #print(str(temp_terminal_list[0:1])+str(durchschnitt(temp_terminal_list[1:])))
    temp_terminal_list = []


# EvoGErrors 1 Tteration
ValueError_list_evogerrors_1 = []
for terminal in terminal_list:
    temp_terminal_list.append(terminal)
    for i in find_all(output_evogerrors_1, "('"+terminal):
        line = str(output_evogerrors_1[i:len(output_evogerrors_1)].partition('\n')[0])[str(output_evogerrors_1[i:len(output_evogerrors_1)].partition('\n')[0]).find("ValueError")+13:]
        line = line[0:line.find(",")].replace("}", "")
        if not line == "None":
            temp_terminal_list.append(float(line))
    ValueError_list_evogerrors_1.append(durchschnitt(temp_terminal_list[1:]))
    #print(str(temp_terminal_list[0:1])+str(durchschnitt(temp_terminal_list[1:])))
    temp_terminal_list = []

# EvoGFuzz
ValueError_list_evogfuzz = []
for terminal in terminal_list:
    temp_terminal_list.append(terminal)
    for i in find_all(output_evogfuzz, "('"+terminal):
        line = output_evogfuzz[i:]
        line = line[line.find("prob")+7:line.find(")")-1]
        if not line == "None":
            temp_terminal_list.append(float(line))
    ValueError_list_evogfuzz.append(durchschnitt(temp_terminal_list[1:]))
    #print(str(temp_terminal_list[0:1])+str(durchschnitt(temp_terminal_list[1:])))
    temp_terminal_list = []

formatted_terminal_list = ["/", "sqrt", "tan", "cos", "sin", "log", "len", "inc", "factorial", "is_int", "-", ".", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]

# print the diagramm
y = np.arange(len(formatted_terminal_list))
plt.barh(y+0.2, ValueError_list_evogfuzz, 0.2, label = "EvoGFuzz", color=evogfuzz_color)
plt.barh(y, ValueError_list_evogerrors_1, 0.2, label = "EvoGErrors (1 Iteration)", color=evogerrors_1_color)
plt.barh(y-0.2, ValueError_list_evogerrors, 0.2, label = "EvoGErrors (3 Iterations)", color=evogerrors_color)
plt.legend()
plt.xlabel("Probability")
plt.ylabel("Terminal symbols")
plt.title("ValueError")
plt.yticks(y, formatted_terminal_list)
#plt.show()