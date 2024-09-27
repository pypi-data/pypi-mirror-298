import requests
from io import BytesIO
from PIL import Image
import os
from IPython.display import Audio, Video
from IPython.display import Image as ipyImage
import time
import re
import json
import ast
import shutil
import segmind_workflow
from importlib.resources import read_text

funcition_call_url = "https://api.segmind.com/v1"
function_call_sequence_url = "https://e1a5-194-68-245-76.ngrok-free.app"
upload_call_url = 'https://7492da7838b66280a2ffc7fb22866b3d.serveo.net/upload'

class Workflow:
    def __init__(self, api_key, output_dir = "outputs/"):
        self.api_key = api_key
        self.context = ""
        self.query_sequence = []
        self.call_sequence = []
        self.results = None
        self.credits_left = None
        self.price_list = {
            "function1": 10,
            "function2": 20,
            "function3": 30
        }
        # script_dir = os.path.dirname(os.path.abspath(__file__))
        # self.output_dir = os.path.join(script_dir, output_dir)
        self.output_dir = os.path.abspath(output_dir)
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        self.sequence_generated = False
        self.call_made = False
        self.audio_extensions = ['.mp3', '.wav']
        self.video_extensions = ['.mp4', '.mov']
        self.image_extensions = ['.jpg', '.jpeg', '.png']
        self.slug_data_filepath = 'model_files/slug_data.json'
        self.models_data_filepath = 'model_files/models_data.json'
        with open(self.slug_data_filepath) as f:
            self.slug_data = json.load(f)
        with open(self.models_data_filepath) as f:
            self.models_data = json.load(f)
        # file_content = read_text(segmind_workflow, self.slug_data_filepath)
        # self.slug_data = json.loads(file_content)
        # file_content = read_text(segmind_workflow, self.models_data_filepath)
        # self.models_data = json.loads(file_content)
        # new_models_data = {}
        # for model_name, item in self.models_data.items():
        #     model_name = model_name.replace('-','_').replace('/','_').replace('.','_').replace(' ', '_').replace("'",'').lower()
        #     new_models_data[model_name] = item
        # self.models_data = new_models_data

    def correct_sequence(self, input_list):
        inp_count = 0
        output_list = []
        for item in input_list:
            modified_item = item
            while 'INP' in modified_item:
                modified_item = modified_item.replace('INP', f'INP{inp_count}', 1)
                inp_count += 1
            
            output_list.append(modified_item)
        return output_list

    def query(self, prompt):
        t = time.time()
        print("Getting the Function call sequence")
        params = {
            "query": prompt,
            "prev_query": self.context,
            "sequence": str(self.call_sequence)
        }
        response = requests.get(function_call_sequence_url, params=params)
        if response.status_code == 200:
            data = response.json()
            self.call_sequence = data.get("result")
            self.call_sequence = self.correct_sequence(self.call_sequence)
            self.context = data.get("next_query")
            self.query_sequence.append(prompt)
            self.sequence_generated = True
        else:
            raise Exception(f"Failed to query the API to get the function call sequence with status code {response.status_code}, Error message is {response.text}.")
        print(f"Function call sequence obtained in {int(time.time() - t)}s")
    
    def get_sequence(self):
        if not self.sequence_generated:
            raise Exception("Error: No query sequence generated yet. Please call query() first.")
        return self.call_sequence

    def convert_to_call_sequence(self, function_name, input_data):
        param_list = []
        for key, value in input_data.items():
            if isinstance(value, str):
                param_list.append(f"{key}='{value}'")
            else:
                param_list.append(f"{key}={value}")
        params = ', '.join(param_list)
        return f"{function_name}({params})"

    def change_params(self, data):
        # data = {'func1': {'param1':'value1'}, 'func2': {'param1':'value1', 'param2':'value2'}}
        if not self.sequence_generated:
            raise Exception("Error: No query sequence generated yet. Please call query() first.")
        for  function in data:
            for i, result in enumerate(self.call_sequence):
                _, input_data = self.get_function_call_details(result)
                function_name = result.split('(')[0]
                if function_name == function:
                    input_data.update(data[function])
                    self.call_sequence[i] = self.convert_to_call_sequence(function_name, input_data)
                    break


    def change_function_names(self, data):
        # data = [['func1', 'func1'], ['func1', 'func1']]
        if not self.sequence_generated:
            raise Exception("Error: No query sequence generated yet. Please call query() first.")
        l0 = [d[0] for d in data]
        l1 = [d[1] for d in data]
        for idx, function in enumerate(l0):
            for i, result in enumerate(self.call_sequence):
                _, input_data = self.get_function_call_details(result)
                function_name = result.split('(')[0]
                if function_name == function:
                    sequence = self.convert_to_call_sequence(l1[idx], input_data)
                    self.call_sequence[i] = sequence
                    break


    def upload_file(self, file_path):
        with open(file_path, "rb") as file:
            response = requests.post(upload_call_url, files={"file": file})
        response = response.json()
        url = response['file_url']
        return url

    def correct_input_type(self, input_value):
        url_pattern = r'^(http|https)://[^\s]+'
        if re.match(url_pattern, input_value):
            return input_value

        if os.path.isfile(input_value):
            _, ext = os.path.splitext(input_value)
            ext = ext.lower()

            if ext in self.audio_extensions:
                url = self.upload_file(input_value)
                return url
            elif ext in self.video_extensions:
                url = self.upload_file(input_value)
                return url
            elif ext in self.image_extensions:
                # img = Image.open(input_value)
                # buffered = BytesIO()
                # img.save(buffered, format="PNG")
                # url = base64.b64encode(buffered.getvalue()).decode('utf-8')
                url = self.upload_file(input_value)
                return url
            else:
                raise NotImplementedError

        return input_value
    
    def call(self, data):
        if not self.sequence_generated:
            raise Exception("Error: Call sequence not generated. Please call query() first.")
        
        self.results = []
        for i, function_call in enumerate(self.call_sequence):
            for _ in range(function_call.count("INP")):
                match = re.search(r"INP__(\d+)", function_call)
                idx = int(match.group(1))
                d = self.correct_input_type(data[idx])
                inp_idx = function_call.find("INP")
                function_call = function_call[:inp_idx] + d + function_call[inp_idx+3+len(str(idx)):]
                
            for _ in range(function_call.count("OUT[")):
                match = re.search(r"OUT\[(\d+)\]", function_call)
                idx = int(match.group(1))
                d = self.correct_input_type(self.results[idx])
                inp_idx = function_call.find("OUT[")
                function_call = function_call[:inp_idx] + d + function_call[inp_idx+5+len(str(idx)):]

            result = self.make_function_call(function_call, i)
            self.results.append(result)
        self.call_made = True

    def save_response(self, response, content_type, i):
        if 'image' in content_type or 'octet-stream' in content_type:
            path = f'{i}.png'
            path = os.path.join(self.output_dir, path)
            img = Image.open(BytesIO(response.content))
            img.save(path)
            return path
        elif 'json' in content_type:
            data = response.json()
            d = find_text_or_content(data)
            path = f'{i}.txt'
            path = os.path.join(self.output_dir, path)
            if d is not None:
                d=str(d)
                with open(path, 'wb') as file:
                    file.write(d)
                return d
            else:
                data = str(data)
                with open(path, 'wb') as file:
                    file.write(data)
                return data
        elif 'text' in content_type:
            path = f'{i}.txt'
            path = os.path.join(self.output_dir, path)
            try:
                data = response.json()
                d = find_text_or_content(data)
                if d is not None:
                    d=str(d)
                    with open(path, 'wb') as file:
                        file.write(d)
                    return d
                else:
                    data = str(data)
                    with open(path, 'wb') as file:
                        file.write(data)
                    return data
            except:
                with open(path, 'wb') as file:
                    file.write(response.text)
                return response.text
        elif 'video' in content_type:
            path = f'{i}.mp4'
            path = os.path.join(self.output_dir, path)
            with open(path, 'wb') as video_file:
                video_file.write(response.content)
            return path
        elif 'audio' in content_type:
            path = f'{i}.mp3'
            path = os.path.join(self.output_dir, path)
            with open(path, 'wb') as audio_file:
                audio_file.write(response.content)
            return path
        else:
            print(content_type)
            return response
        
    def get_function_call_details(self, function_call):
        function_call = function_call.replace('\n', '')
        function_name = function_call.split('(')[0]
        function_name = self.slug_data[function_name]
        params_string = function_call.split('(')[1].split(')')[0]
        params_list = params_string.split(',')
        params_list = [p for p in params_list if p != ""]
        input_data = {}
        for param in params_list:
            try:
                key, value = param.split('=')
            except Exception as e:
                key = list(input_data.keys())[-1]
                input_data[key] = input_data[key] + ',' + param
                continue
            input_data[str(key)] = value

        for key in input_data:
            try:
                input_data[key] = ast.literal_eval(input_data[key])
            except Exception as e:
                pass

        input_data = {key.strip(): value for key, value in input_data.items()}
        return function_name, input_data

    def make_api_call(self, function_call, org_input_data):
        model = "gpt-4"
        model = "llama-v3p1-8b-instruct"
        model = "claude-3.5-sonnet"
        t = time.time()
        print('_'*100)
        print(f'Making Function call for {model}')
        url = f"{funcition_call_url}/{model}"
        # org_input_data = re.sub(r"[^a-zA-Z0-9\s\.\-,\'=]", '', str(org_input_data))
        org_input_data = str(org_input_data).encode().decode('unicode_escape')
        data = {
            "messages": [{
                "role": "user",
                "content" :f"""Correct this function call as this function call has some parameter names which are incorrectly labeled or also sometimes in different format.
{function_call}
The original parameters it should take are these (It also has default values, ignore them).
It has required and optional values, in the final function call sequence all the required values should be present and optional values only need to be present if they are given or named differently (see for similar names like messages and prompt fields are same) in the given sequence.
{org_input_data}
Add the optional values only if they are given in original call sequence or else don't add them unnecessarily.
Now return the original function call sequences with the parameters as required as original parameters and in correct format and only output the function call sequence and nothing else and take parameter values from the given function call sequence and just the parameter names from the original input data list.
"""
    }],
        "instruction": "Only change parameter names or add new if required, don't change parameter values if not needed and only output the final functional call sequence and nothing else.",
        "temperature": 0.1,
        }
        response = requests.post(url, json=data, headers={'x-api-key': self.api_key})
        if response.status_code == 200:
            self.credits_left = response.headers.get('x-remaining-credits')
            data = find_text_or_content(response.json())
            if data.startswith("```python"):
                data = data[len("```python"):]
            if data.endswith("```"):
                data = data[:-len("```")]
            print(f'Completed making Function call for {model} in {int(time.time()-t)}s')
            return data
        else:
            raise Exception(
                    f"Failed to call request for {model}\n"
                    f"Failed to call request for data\n{print(data)}\n"
                    # f"Response is\n{response.content}\n"
                    f"Status Code: {response.status_code}\n"
                    f"Error Message: {response.text}"
                )

    def correct_function_call(self, function_call):
        function_name, input_data = self.get_function_call_details(function_call)
        org_input_data = self.models_data[function_call.split('(')[0]]

        l1 = list(input_data.keys())
        l2 = list(org_input_data['required'].keys())
        if all(elem in l1 for elem in l2):
            return function_name, input_data
        else:
            new_function_call = self.make_api_call(function_call, org_input_data)
            print(new_function_call)
            function_name, input_data = self.get_function_call_details(new_function_call)
            return function_name, input_data

    def make_function_call(self, function_call, i):
        # print('function_call', function_call)
        function_name, input_data = self.correct_function_call(function_call)
        t = time.time()
        print('_'*100)
        print(f'Making Function call for {function_name}')
        url = f"{funcition_call_url}/{function_name}"
        response = requests.post(url, json=input_data, headers={'x-api-key': self.api_key})
        if response.status_code == 200:
            self.credits_left = response.headers.get('x-remaining-credits')
            content_type = response.headers.get('Content-Type')
            response = self.save_response(response, content_type, i)
            print(f'Completed making Function call for {function_name} in {int(time.time()-t)}s')
            return response
        else:
            raise Exception(
                    f"Failed to call request for {function_name}\n"
                    f"Failed to call request for data\n{input_data}\n"
                    f"Status Code: {response.status_code}\n"
                    f"Error Message: {response.text}"
                )
        
    def get_result(self):
        if not self.call_made:
            raise Exception("Error: No function call made yet. Please call the call() function first.")
        return self.results

    def call_cost(self):
        if not self.sequence_generated:
            raise Exception("Error: No function sequence available. Please call query() first.")
        
        # total_cost = sum(self.price_list.get(func, 0) for func in self.call_sequence)
        total_cost = 0
        print("Total Cost calculation not implemented till now!")
        return total_cost

    def credits_left(self):
        if self.credits_left is None:
            raise Exception("Error: No function call has been made yet. Please call the call() function first to know the credits left.")
        return self.credits_left

    def reset(self, outputs = False):
        self.context = ""
        self.query_sequence = []
        self.call_sequence = []
        self.results = None
        self.sequence_generated = False
        self.call_made = False
        if outputs:
            shutil.rmtree(self.output_dir)

    def visualize(self):
        if not self.call_made:
            raise Exception("Error: No function call made yet. Please call the call() function first.")
        pass

    def print(self):
        if not self.call_made:
            raise Exception("Error: No function call made yet. Please call the call() function first.")
        for i, result in enumerate(self.results):
            print(f"Output of {self.call_sequence[i].split('(')[0]} is:")
            if os.path.isfile(result):
                _, ext = os.path.splitext(result)
                ext = ext.lower()
                if ext in self.audio_extensions:
                    Audio(result, width=600, height=400)
                elif ext in self.video_extensions:
                    Video(result, width=600, height=400)
                elif ext in self.image_extensions:
                    ipyImage(result, width=600, height=400)
                else:
                    print(result)

def find_key(data, key):
    if isinstance(data, dict):
        if key in data:
            return data[key]
        for value in data.values():
            result = find_key(value, key)
            if result is not None:
                return result
    elif isinstance(data, list):
        for item in data:
            result = find_key(item, key)
            if result is not None:
                return result
    return None

def find_text_or_content(data):
    text_value = find_key(data, 'text')
    if text_value is not None:
        return text_value
    
    content_value = find_key(data, 'content')
    return content_value