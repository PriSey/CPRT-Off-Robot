import json

def load_hsv():
    with open('hsv.json','r') as f:
        params = json.load(f)
        mask_upper = [params['upper']['h'], params['upper']['s'], params['upper']['v']]
        mask_lower = [params['lower']['h'], params['lower']['s'], params['lower']['v']]
        return (mask_upper,mask_lower)
        
def write_hsv(upper,lower):
    with open('hsv.json','w') as f:
        parent_dict = {
            'upper':upper,
            'lower':lower
        }
        d = json.dumps(parent_dict)
        f.write(d)
    
def load_gestures():
  with open('gestures.json') as f:
    gestures = json.load(f)
  return gestures

def add_gesture(name, gesture):
  json_content = load_gestures()
  json_content[name] = gesture
  d = json.dumps(json_content)
  with open('gestures.json') as f:
      f.write(d)
    