import pickle

data = ''
variable_prefix_stack = []

def headers_to_dict(raw_headers):
    d = dict()
    for i in raw_headers.split('\n'):
        if ":" in i:
            k = i.split(":", 1)
            if k[0].strip() in variable_to_record:
                d[k[0].strip()] = k[1].strip()
    return d

with open('/apollo/cyber/python/examples/batch_parse_demo_header.txt','r') as f:
  content = f.read()

# print(content)


d = dict()

current_depth = 0
for s in content.split('\n'):
    if "{" in s:
        current_depth += 1
        k = s.split("{", 1)[0]
        variable_prefix_stack.append(k.strip())

    elif "}" in s:
        current_depth -= 1
        variable_prefix_stack.pop()

    elif ":" in s:
        k = s.split(":", 1)
        key = k[0].strip()
        value = k[1].strip()
        variable_name = ""
        if current_depth > 0:
            for depth in range(current_depth):
                if depth >0:
                    variable_name = variable_name + "-" +  variable_prefix_stack[depth]
                else:
                    variable_name =  variable_prefix_stack[depth]
            variable_name = variable_name + "-" + key
        else:
            variable_name = key
        d[variable_name] = value

for key in d:
    print(key+':'+d[key])