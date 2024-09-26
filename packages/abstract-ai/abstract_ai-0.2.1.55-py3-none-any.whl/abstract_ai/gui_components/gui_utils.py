import os
import PySimpleGUIWeb as sg
from abstract_utilities import get_closest_match_from_list
from abstract_utilities.list_utils import ensure_nested_list,find_original_case
from abstract_utilities.class_utils import get_all_functions_for_instance,get_all_params,get_fun
class SimpleGuiFunctionsManager:
    def __init__(self):
        self.instance = sg
        self.function_names = get_all_functions_for_instance(instance=self.instance)
        self.function_names_dict = {}

    def _resolve_function_name(self, function_name):
        original_input = function_name
        # Check if the function name is already known
        if function_name in self.function_names_dict:
            return function_name
        for key,values in self.function_names_dict.items():
            if original_input in values["names"]:
                return key
        # Try to find the function name in the list of all functions
        if function_name not in self.function_names:
            function_name = find_original_case(self.function_names, function_name)
            if function_name == None:
                function_name = get_closest_match_from_list(comp_str=original_input, total_list=self.function_names)
                print(f"Function name: {original_input} resolved to closest match: {function_name}")
            else:
                print(f"Function name: {original_input} resolved to case match: {function_name}")
        # Add the resolved function name to the dictionary for future reference
        if function_name not in self.function_names_dict:
            all_params = self.get_all_parameters(function_name)
            self.function_names_dict[function_name] = {
                "names": [],
                "all_params": all_params,
                "required_params": all_params["names"]
            }
        if original_input not in self.function_names_dict[function_name]["names"]:
            self.function_names_dict[function_name]["names"].append(original_input)

        return function_name

    def get_all_parameters(self, function_name):
        return get_all_params(instance=self.instance, function_name=function_name)

    def get_gui_function(self, function_name: str = '', *args_2, args: dict = {}, **kwargs):
        function_name = self._resolve_function_name(function_name)
        fn_dict = self.function_names_dict[function_name]
        required_params = fn_dict["required_params"]

        # Map positional arguments to their respective required_params
        for i, param in enumerate(required_params):
            if i < len(args_2) and param not in args:
                args[param] = args_2[i]

        # Ensure default values for certain parameters
        for param in required_params:
            if param not in args:
                default_values = {"title": "", "layout": [[]], "values": [], "text": ""}
                if param in default_values:
                    args[param] = default_values[param]
                    if function_name != 'Window':
                        print(f"{param} for {function_name} not in arguments, using default {param} = {args[param]}")

        # Nested list for layout parameter
        if "layout" in fn_dict["all_params"]["names"]:
            args["layout"] = ensure_nested_list(args.get("layout", []))

        return get_fun({"instance": self.instance, "name": function_name, "args": args})

    def make_component(self, function_name, *args, **kwargs):
        if 'args' in kwargs:
            arges = kwargs['args']
            del kwargs['args']
            kwargs.update(arges)
        return self.get_gui_function(function_name, *args, args=kwargs)

class SimpleGuiFunctionsManagerSingleton:
    _instance = None
    @staticmethod
    def get_instance():
        if SimpleGuiFunctionsManagerSingleton._instance is None:
            SimpleGuiFunctionsManagerSingleton._instance = SimpleGuiFunctionsManager()
        return SimpleGuiFunctionsManagerSingleton._instance
def get_gui_fun(function_name: str = '', args: dict = {}):
    """
    Returns a callable object for a specific PySimpleGUI function with the provided arguments.

    Args:
        function_name (str): The name of the PySimpleGUI function.
        *args_2: Variable-length positional arguments.
        args (dict): The arguments to pass to the PySimpleGUI function.
        **kwargs: Variable-length keyword arguments.

    Returns:
        callable: A callable object that invokes the PySimpleGUI function with the specified arguments when called.
    """
    simple_gui_fun_mgr = SimpleGuiFunctionsManagerSingleton.get_instance()
    return simple_gui_fun_mgr.get_gui_function(function_name=function_name,args=args)

def make_component(function_name,*args,**kwargs):
    simple_gui_fun_mgr = SimpleGuiFunctionsManagerSingleton.get_instance()
    return simple_gui_fun_mgr.make_component(function_name,*args,**kwargs)


from abstract_gui import AbstractWindowManager,AbstractBrowser,text_to_key,ensure_nested_list,expandable,RightClickManager,get_screen_dimensions
right_click_mgr=RightClickManager()
def get_standard_screen_dimensions(width=0.70,height=0.80):
    return get_screen_dimensions(width=width,height=height)
window_width,window_height=get_standard_screen_dimensions()
def get_left_right_nav(name,section=True,push=True):
    insert = f"{name} {'section ' if section else ''}"
    nav_bar = [make_component("Button",button_text="<-",key=text_to_key(f"{insert}back"),enable_events=True),
         make_component("input",default_text='0',key=text_to_key(f"{insert}number"),size=(4,1)),
         make_component("Button",button_text="->",key=text_to_key(f"{insert}forward"),enable_events=True)]
    if push:
        nav_bar=[make_component("Push")]+nav_bar+[make_component("Push")]
    return nav_bar
def generate_bool_text(title:str,args:dict={})->object:
    return make_component("Frame",title, layout=[[get_right_click_multi(key=text_to_key(text=title,section='text'),args=args)]],**expandable())
def get_tab_layout(title:str,layout:list=None)->object:
    if not layout:
        layout = get_right_click_multi(key=text_to_key(title),args={**expandable(size=(None, 5))})
    return make_component("Tab",title.upper(),ensure_nested_list(layout))
def get_column(layout:list,args:dict={})->object:
    return make_component("Column",ensure_nested_list(layout),**args)
def get_tab_group(grouped_tabs:list,args:dict={})->object:
    return make_component("TabGroup",ensure_nested_list(grouped_tabs),**args)
def get_right_click_multi(key:str,args:dict={})->object:
    return make_component("Multiline",**args,right_click_menu=right_click_mgr.get_right_click(key=key),key=key)
completion_token_keys = ['completion tokens available','completion tokens desired','completion tokens used']
prompt_token_keys = ['prompt tokens available','prompt tokens desired','prompt tokens used']
chunk_data_keys=['max chunk size','chunk length','chunk total']
all_token_keys = completion_token_keys+prompt_token_keys+chunk_data_keys+['chunk sectioned data']
response_types = ['instruction', 'json', 'bash', 'text']
model_type_keys=['role','response type']
percentage_keys = ['prompt percentage','completion percentage']
file_options_keys = ['auto chunk title','reuse chunk data','append chunks','scan mode all']
test_options_keys = ['test run','test files','test file input','test browse']
instructions_keys = ["instructions","additional_responses","suggestions","abort","database_query","notation","generate_title","additional_instruction","request_chunks","prompt_as_previous","token_adjustment"]
api_keys = ["header",'api key','api env']
