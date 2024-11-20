flag = "flag{??????????????}"

def next(x):
    x = (287*x + 123213) % 26
    return x

def function(msg):
    output = ""
    y = 7
    for letter in msg:
        letter_as_num = ord(letter)
        y = next(y)
        new_num = letter_as_num + y
        output += chr(new_num)
    return output

output = function(flag)
print(output) # lqej}c4zuzA~n@p||9um