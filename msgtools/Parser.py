import pickle

class HeaderParser:
    def __init__(self, variable_to_record = "Preception"): # dataPath : /+name
        self.type = type
        if variable_to_record == "Perception":
            self.variable_to_record = ['perception_obstacle-acceleration-x',
                                       'perception_obstacle-acceleration-y',
                                       'perception_obstacle-acceleration-z',
                                       'perception_obstacle-position-x',
                                    'perception_obstacle-position-y',
                                    'perception_obstacle-position-z',
                                    'perception_obstacle-theta',
                                    'perception_obstacle-velocity-x',
                                    'perception_obstacle-velocity-y',
                                    'perception_obstacle-velocity-z']
        elif variable_to_record == "Prediction":
            self.variable_to_record = ['prediction_obstacle-perception_obstacle-acceleration-x',
                                    'prediction_obstacle-perception_obstacle-acceleration-y',
                                    'prediction_obstacle-perception_obstacle-acceleration-z',
                                    'prediction_obstacle-perception_obstacle-position-x',
                                    'prediction_obstacle-perception_obstacle-position-y',
                                    'prediction_obstacle-perception_obstacle-position-z',
                                    'prediction_obstacle-perception_obstacle-theta',
                                    'prediction_obstacle-perception_obstacle-velocity-x',
                                    'prediction_obstacle-perception_obstacle-velocity-y',
                                    'prediction_obstacle-perception_obstacle-velocity-z'] 
        elif variable_to_record == "Localization_Pos":
            self.variable_to_record = ['pose-position-x',
                                    'pose-position-y',
                                    'pose-position-z',
                                    'pose-heading']
        
    def parse(self,msg_str):
        variable_prefix_stack = []
        d = dict()
        current_depth = 0
        for s in msg_str.split('\n'):
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
                if len(self.variable_to_record) > 0: 
                    if variable_name in self.variable_to_record:
                        d[variable_name] = value
                else:
                    d[variable_name] = value
        return d

    def test_perception(self):
        self.variable_to_record = ['perception_obstacle-acceleration-x',
                                    'perception_obstacle-acceleration-y',
                                    'perception_obstacle-acceleration-z',
                                    'perception_obstacle-position-x',
                                'perception_obstacle-position-y',
                                'perception_obstacle-position-z',
                                'perception_obstacle-theta',
                                'perception_obstacle-velocity-x',
                                'perception_obstacle-velocity-y',
                                'perception_obstacle-velocity-z']
        with open('/apollo/cyber/python/examples/batch_parse_demo_perception_header.txt','r') as f:
            content = f.read()
        d = self.parse(content)
        for key in d:
            print(key+':'+d[key])

    def test_prediction(self):
        self.variable_to_record = ['prediction_obstacle-perception_obstacle-acceleration-x',
                                    'prediction_obstacle-perception_obstacle-acceleration-y',
                                    'prediction_obstacle-perception_obstacle-acceleration-z',
                                    'prediction_obstacle-perception_obstacle-position-x',
                                    'prediction_obstacle-perception_obstacle-position-y',
                                    'prediction_obstacle-perception_obstacle-position-z',
                                    'prediction_obstacle-perception_obstacle-theta',
                                    'prediction_obstacle-perception_obstacle-velocity-x',
                                    'prediction_obstacle-perception_obstacle-velocity-y',
                                    'prediction_obstacle-perception_obstacle-velocity-z'] 
        # self.variable_to_record = []
        with open('/apollo/cyber/python/examples/batch_parse_demo_prediction_header.txt','r') as f:
            content = f.read()
        d = self.parse(content)
        for key in d:
            print(key+':'+d[key])
    
    def test_localization_pos(self):
        self.variable_to_record = ['pose-position-x',
                                    'pose-position-y',
                                    'pose-position-z',
                                    'pose-heading']
        # self.variable_to_record = []
        with open('/apollo/cyber/python/examples/batch_parse_demo_localization_estimate_header.txt','r') as f:
            content = f.read()
        d = self.parse(content)
        for key in d:
            print(key+':'+d[key])
     
if __name__ == '__main__':
    test_parser = HeaderParser()
    # test_parser.test_perception()
    test_parser.test_localization_pos()
    print('end')
