def open_file(filename):
    data = open(filename, "r").read();
    data += "<EOF>"
    return data


i = ""
tokens = []
nums = []
sym = {}


# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
def lex(contents):
    tok = ""
    state = 0
    ise = 0
    vars = 0
    ism = 0
    var = ""
    string = ""
    expr = ""
    contents = list(contents)


    for char in contents:
        if char == " ":
            char = ""
        tok += char
        #print(tok)
        if ism == 1:
            if tok == " ":
                if state == 0:
                    tok = ""
                else:
                    tok = " "
            elif char == '[':
                if expr != "":
                    tokens.append("NUM:" + expr)
                    expr = ""
                elif var != "":
                    var = var[:]
                    tokens.append("VAR:" + var)
                    var = ""
                    vars = 0
                tokens.append("[")
                tok = ""
            elif tok == "\n" or tok == "<EOF>":
                if expr != "" and ise == 1:
                    tokens.append("EXPR:" + expr)
                    expr = ""
                elif expr != "":
                    tokens.append("NUM:" + expr)
                    expr = ""
                elif var != "":
                    tokens.append("VAR:" + var)
                    var = ""
                    vars = 0
                tok = ""
            elif tok == "=" and state == 0:
                if expr != "":
                    tokens.append("NUM:" + expr)
                    expr = ""
                if var != "":
                    tokens.append("VAR:" + var)
                    var = ""
                    vars = 0
                if tokens[-1] == "EQUALS":
                    tokens[-1] = "EQEQ"
                else:
                    tokens.append("EQUALS")
                tok = ""
            elif tok == "var" and state == 0:
                vars = 1
                tok = ""
            elif vars == 1:
                if tok == "<" or tok == ">":
                    if var != "":
                        tokens.append("VAR:" + var)
                        var = ""
                        vars = 0
                var += tok
                tok = ""
            elif tok == "DISPLAY" or tok == "display":
                tokens.append("DISPLAY")
                tok = ""
            elif tok == "IMPORT" or tok == "import":
                tokens.append("IMPORT")
                tok = ""
            elif tok == "]":
                tokens.append("]")
                tok = ""
            elif tok == "IF" or tok == "if":
                tokens.append("IF")
                tok = ""
            elif tok == "1" or tok == "2" or tok == "3" or tok == "4" or tok == "5" or tok == "6" or tok == "7" or tok == "8" or tok == "9" or tok == "0":
                expr += tok
                tok = ""
            elif tok == "+" or tok == "-" or tok == "*" or tok == "/" or tok == "(" or tok == ")":
                expr += tok
                ise = 1
                tok = ""
            elif tok == "\t":
                tok = ""
            #Try to change # -> "
            elif tok == "#" or tok == " #":
                if state == 0:
                    state = 1
                    tok = ""
                elif state == 1:
                    tokens.append("STRING:" + string)
                    string = ""
                    state = 0
                    tok = ""
            elif state == 1:
                #print(tok)
                string += tok
                tok = ""
            elif tok == "}":
                ism = 0
                tok = ""
        elif tok == "voidmain{}{":
            ism = 1
            tok = ""
    #print(tokens)
    #return ''
    return tokens


# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
def evale(expr):
    return eval(expr)


def avar(vname, vval):
    sym[vname] = vval


def gvar(vname):
    if vname in sym:
        return sym[vname]
    else:
        return "VAR ERROR: Undefined Variable"


def imv(vname):
    i = input()
    sym[vname] = i


# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
def parse(toks):
    i = 0
    while i < len(toks):
        if toks[i] == "]":
            i += 1
        elif toks[i] + " " + toks[i+1][0:6] == "DISPLAY STRING" or toks[i] + " " + toks[i+1][0:3] == "DISPLAY NUM"\
                or toks[i] + " " + toks[i+1][0:4] == "DISPLAY EXPR" or toks[i] + " " + toks[i+1][0:3] == "DISPLAY VAR":
            if toks[i + 1][0:6] == "STRING":
                print(toks[i+1][7:])
            elif toks[i + 1][0:3] == "NUM":
                print(toks[i + 1][4:])
            elif toks[i + 1][0:4] == "EXPR":
                print(evale(toks[i + 1][5:]))
            elif toks[i + 1][0:3] == "VAR":
                print(gvar(toks[i + 1][4:]))
            i += 2
        elif toks[i] + " " + toks[i + 1][0:3] == "IMPORT VAR":
            if toks[i + 1][0:3] == "VAR":
                imv(toks[i + 1][4:])
            i += 2
        elif toks[i][0:3] + " " + toks[i+1] + " " + toks[i+2][0:6] == "VAR EQUALS STRING"\
                or toks[i][0:3] + " " + toks[i+1] + " " + toks[i+2][0:3] == "VAR EQUALS NUM"\
                or toks[i][0:3] + " " + toks[i+1] + " " + toks[i+2][0:4] == "VAR EQUALS EXPR" \
                or toks[i][0:3] + " " + toks[i+1] + " " + toks[i+2][0:3] == "VAR EQUALS VAR":
            if toks[i + 2][0:6] == "STRING":
                avar(toks[i][4:], toks[i+2][7:])
            elif toks[i + 2][0:3] == "NUM":
                avar(toks[i][4:], toks[i+2][4:])
            elif toks[i + 2][0:4] == "EXPR":
                avar(toks[i][4:], evale(toks[i+2][5:]))
            elif toks[i + 2][0:3] == "VAR":
                avar(toks[i][4:], gvar(toks[i+2][4:]))
            i += 3
        elif toks[i] + " " + toks[i+1][0:3] + " " + toks[i+2] + " " + toks[i+3][0:3] + " " + toks[i+4]\
                == "IF VAR EQEQ VAR ["\
                or toks[i] + " " + toks[i+1][0:3] + " " + toks[i + 2] + " " + toks[i + 3][0:3] + " " + toks[i + 4] \
                == "IF NUM EQEQ VAR ["\
                or toks[i] + " " + toks[i+1][0:3] + " " + toks[i+2] + " " + toks[i+3][0:3] + " " + toks[i+4]\
                == "IF NUM EQEQ NUM ["\
                or toks[i] + " " + toks[i+1][0:3] + " " + toks[i+2] + " " + toks[i+3][0:3] + " " + toks[i+4]\
                == "IF VAR EQEQ NUM [":
            if toks[i+1][0:3] + toks[i+3][0:3] == "VARVAR":
                if gvar(toks[i+1][4:]) == gvar(toks[i+3][4:]):
                    print("vv true")
                else:
                    print("vv false")
            elif toks[i+1][0:3] + toks[i+3][0:3] == "NUMVAR":
                if toks[i+1][4:] == gvar(toks[i+3][4:]):
                    print("nv true")
                else:
                    print("nv false")
            elif toks[i+1][0:3] + toks[i+3][0:3] == "VARNUM":
                if gvar(toks[i+1][4:]) == toks[i+3][4:]:
                    print("vn true")
                else:
                    print("vn false")
            elif toks[i+1][0:3] + toks[i+3][0:3] == "NUMNUM":
                if toks[i+1][4:] == toks[i+3][4:]:
                    print("nn true")
                else:
                    print("nn false")
            i += 5
    #print(sym)


def run():
    i = input()
    data = open_file(i)
    toks = lex(data)
    parse(toks)


run()
