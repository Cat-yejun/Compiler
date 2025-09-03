from SLR_Table import table as slr
import os
import sys
from tree import TreeNode, Tree

# ---------------| ACTION STATE DEFINITION |---------------

ACTION_STATE = [['vtype', 0],
                ['id', 1],
                ['semi', 2],
                ['assign', 3],
                ['literal', 4],
                ['character', 5],
                ['boolstr', 6],
                ['addsub', 7],
                ['multdiv', 8],
                ['lparen', 9],
                ['rparen', 10],
                ['num', 11],
                ['lbrace', 12],
                ['rbrace', 13],
                ['comma', 14],
                ['if', 15],
                ['while', 16],
                ['comp', 17],
                ['else', 18],
                ['return', 19],
                ['class', 20],
                ['end', 21]]

# ----------------| GOTO STATE DEFINITION |-------------------

GOTO_STATE = [['S', 22],
              ['CODE', 23],
              ['VDECL', 24],
              ['ASSIGN', 25],
              ['RHS', 26],
              ['EXPR', 27],
              ['T', 28],
              ['F', 29],
              ['FDECL', 30],
              ['ARG', 31],
              ['MOREARGS', 32],
              ['BLOCK', 33],
              ['STMT', 34],
              ['COND', 35],
              ['CONDT', 36],
              ['ELSE', 37],
              ['RETURN', 38],
              ['CDECL', 39],
              ['ODECL', 40]]

# --------------------| SLR GRAMMAR |------------------------

GRAMMAR = [ ['S', 'CODE'],
            ['CODE', 'VDECL', 'CODE'],
            ['CODE', 'FDECL', 'CODE'],
            ['CODE', 'CDECL', 'CODE'],
            ['CODE', ''],
            ['VDECL', 'vtype', 'id', 'semi'],
            ['VDECL', 'vtype', 'ASSIGN', 'semi'],
            ['ASSIGN','id', 'assign', 'RHS'],
            ['RHS', 'EXPR'],
            ['RHS', 'literal'],
            ['RHS', 'character'],
            ['RHS', 'boolstr'],
            ['EXPR', 'T', 'addsub', 'EXPR'],
            ['EXPR', 'T'],
            ['T', 'F', 'multdiv', 'T'],
            ['T', 'F'],
            ['F', 'lparen', 'EXPR', 'rparen'],
            ['F', 'id'],
            ['F', 'num'],
            ['FDECL', 'vtype', 'id', 'lparen', 'ARG', 'rparen', 'lbrace', 'BLOCK', 'RETURN', 'rbrace'],
            ['ARG', 'vtype', 'id', 'MOREARGS'],
            ['ARG', ''],
            ['MOREARGS', 'comma', 'vtype', 'id', 'MOREARGS'],
            ['MOREARGS', ''],
            ['BLOCK', 'STMT', 'BLOCK'],
            ['BLOCK', ''],
            ['STMT', 'VDECL'],
            ['STMT', 'ASSIGN', 'semi'],
            ['STMT', 'if', 'lparen', 'COND', 'rparen', 'lbrace', 'BLOCK', 'rbrace', 'ELSE'],
            ['STMT', 'while', 'lparen', 'COND', 'rparen', 'lbrace', 'BLOCK', 'rbrace'],
            ['COND', 'CONDT', 'comp', 'COND'],
            ['COND', 'CONDT'],
            ['CONDT', 'boolstr'],
            ['ELSE', 'else', 'lbrace', 'BLOCK', 'rbrace'],
            ['ELSE',''],
            ['RETURN', 'return', 'RHS', 'semi'],
            ['CDECL', 'class', 'id', 'lbrace', 'ODECL', 'rbrace'],
            ['ODECL', 'VDECL', 'ODECL'],
            ['ODECL', 'FDECL', 'ODECL'],
            ['ODECL', ''] ]

# ---------------------| MAIN |--------------------------
newFile = sys.argv[1]

with open(newFile, "r") as file: #txt 파일 읽기
    inputStr = file.read()

file.close()

list(inputStr)
inputStr = inputStr.split(' ')
inputStr.append('end')

stack = []
nextInput = 0
column = 0
goto = 0

treeArray = [] #트리의 node를 담는 array
for item in inputStr: #input 문장을 tree에 담음. 가장 하위 노드가 됨.
    node = TreeNode(item)
    treeArray.append(node)


stack.append(0)

with open('output.txt', 'w') as file:
    while True:
        #----------------------------------------------------
        # 이 부분은 parsing 과정을 보여주는 부분으로, 현재 splitter가 어디있는지와 함께 매 step마다의 상황을 출력해준다.
        for i in range(nextInput):
            file.write(str(inputStr[i]) + ' ')
        file.write('| ')
        for i in range(len(inputStr)-nextInput):
            file.write(str(inputStr[nextInput+i]) + ' ')
        file.write('\n')
        #-----------------------------------------------------
        
        for i in range(len(ACTION_STATE)): # 현재 input symbol이 action state의 어떠한 열번호와 일치하는지 확인해주고, column 변수에 저장한다.
            if ACTION_STATE[i][0] == inputStr[nextInput]:
                column = ACTION_STATE[i][1]

        state = slr[stack[-1]][column] # SLR Table에서 현재 State와 input symbol에 대한 다음 transition 정보를 state 변수에 저장한다.

        error = []
        for i in range(21): # 현재 state에 대한 행에서 비어있지 않은 state의 열에 해당하는 input symbol을 모두 error의 후보로 생각한다.
            if isinstance(slr[stack[-1]][i], str):
                error.append(ACTION_STATE[i][0])

        file.write('\n')

        
        if type(state) is str: # state에 저장된 것의 type이 string인 경우, 즉 transition을 해야 하는 경우
            if state[0] == 's': # shift를 해야 하는 경우
                nextInput = nextInput + 1 # 다음 input symbol의 index를 하나 증가시킨다.
                stack.append(int(state[1:])) # transition 해야 하는 state를 stack에 append 시킨다.

            elif state[0] == 'r': # reduction을 해야 하는 경우
                parentNode = TreeNode(GRAMMAR[int(state[1:])][0]) #부모 노드 생성
                
                if GRAMMAR[int(state[1:])][1] == '': # grammar에서 epsilon move인 경우
                    inputStr.insert(nextInput, GRAMMAR[int(state[1:])][0]) # reduction 해야 하는 non-terminal을 input string에 삽입한다.
                    treeArray.insert(nextInput, parentNode)
                    
                else: # epsilon move가 아닌 경우
                    parentNode = TreeNode(GRAMMAR[int(state[1:])][0]) #부모 노드 생성
                    selected_elements = treeArray[(nextInput-len(GRAMMAR[int(state[1:])])+1):nextInput] #parentNode의 자식 노드 선정

                    for element in selected_elements:
                        parentNode.add_child(element) #자식 노드로 추가

                    del inputStr[(nextInput-len(GRAMMAR[int(state[1:])])+1):nextInput] # 현재 input string에서 grammar의 length만큼 삭제시켜준다.
                    del treeArray[(nextInput-len(GRAMMAR[int(state[1:])])+1):nextInput] #treeArray에서 기존 자식 node 삭제.

                    nextInput = nextInput - len(GRAMMAR[int(state[1:])]) + 1 # input string의 전체 길이가 달라졌으므로 nextInput 변수도 업데이트 시켜준다.
                    inputStr.insert(nextInput, GRAMMAR[int(state[1:])][0]) # reduction 해야 하는 non-terminal을 삽입시켜준다.
                    treeArray.insert(nextInput, parentNode) #treeArray에 부모 노드를 insert. (이후에 다시 자식 노드로 쓰기 위함)
                    
                    for _ in range(len(GRAMMAR[int(state[1:])])-1):
                        stack.pop() # grammar의 length만큼 현재 stack에서 pop 시켜준다.
                    
                nextInput = nextInput + 1 # 다음 input symbol을 읽을 준비, nextInput 변수를 업데이트 시켜준다.
                
                for i in range(len(GOTO_STATE)): # reduction 후 state transition을 위해 GOTO state에 대한 정보를 받아온다.
                    if GOTO_STATE[i][0] == GRAMMAR[int(state[1:])][0]:
                        goto = GOTO_STATE[i][1]

                stack.append(int(slr[stack[-1]][goto])) # 해당되는 state를 stack에 append 한다.

            elif state == 'acc': # 최종적으로 문장이 accept 되는 경우
                print("accepted!") # accept 되었음을 알리는 문장을 출력한다.
                break # while문을 빠져나와 프로그램이 종료된다.
                
        elif type(state) is int: # SLR parsing table에서 다음 transition에 대한 state가 비어있는 경우, 즉 -1인 경우.
            if state == -1:
                errorFinal=[]
                for j in range(len(error)):
                    stackGuess = []
                    stackGuess = stack[:]
                    
                    for i in range(len(ACTION_STATE)): # 이전에 정의 하였던 error들의 후보를 input string에 있었다고 가정하고 state를 구한다.
                        if (ACTION_STATE[i][0] == error[j]):
                            columnGuess = ACTION_STATE[i][1]
                            
                    stateGuess = slr[stackGuess[-1]][columnGuess] # 그대로 transition을 한번 진행한다.
                    
                    if stateGuess[0] == 's':
                        stackGuess.append(int(stateGuess[1:]))
                        
                    elif stateGuess[0] == 'r':
                        errorFinal.append(error[j])
                        continue
                    
                    for i in range(len(ACTION_STATE)):
                        if (ACTION_STATE[i][0] == inputStr[nextInput]):
                            columnGuess = ACTION_STATE[i][1]
                            
                    stateGuess = slr[stackGuess[-1]][columnGuess]
                    
                    if type(stateGuess) is str: # 한번의 transition을 더 수행하였을 때, 다음 SLR Table의 state가 비어있지 않다면, 이것이 정상적인 symbol이었음으로 가정하고 errorFinal에 append 한다.
                        errorFinal.append(error[j])

                if len(errorFinal) == 0: # 만약 연속된 2가지 이상의 symbol의 부재로 오류가 생긴 것이라면, 처음에 예상했던 후보를 모두 에러의 후보로 정의한다.
                    error_str = "\" or \"".join(error)
                    
                else:
                    error_str = "\" or \"".join(errorFinal)
                
                file.write("<<ERROR : expected \"" + error_str + "\">>") # expected 되었던 symbol들을 출력해준다.
                break

    parseTree = Tree(treeArray[0])
    if (parseTree.root.data == 'CODE'): #정상적인 parseTree일 경우 출력
        parseTree.print_tree()
        
        if parseTree.root.data == 'CODE':
            file.write("Input: " + newFile + "\n"+"\n")
            file.write("accepted!"+"\n"+"\n")
            tree_text = parseTree.collect_tree()
            file.write(tree_text)
