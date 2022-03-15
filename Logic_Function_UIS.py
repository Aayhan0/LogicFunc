from tkinter.messagebox import NO
from xmlrpc.client import boolean
import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.properties import StringProperty,ObjectProperty
from pathlib import Path
from Lambda_Function import string_to_lambda_components
from Generate_Output import logicals_function, minimize, gen_VDNF, gen_KDNF
from kivy.uix.screenmanager import ScreenManager, Screen
from copy import deepcopy
from newprint import list_to_string_intervalls, string_not_covered
Builder.load_file(str(Path(__file__).parent.resolve())+"\\UIS.kv")
print("bibliotheken")

class Choose_Application(Screen):
    pass

class Evaluate_Logical_Function(Screen):
    logical_function = None
    components_lambda_function = None
    str_logical_function = ""
    global on_set
    on_set = None
    global off_set
    off_set = None
    bool_tabel = None
    last_button = None
    global bool_tabel_global
    bool_tabel_global = ""
    global boolean_function
    boolean_function = ""
    def update_outputs(self):
        self.logicalFunction = string_to_lambda_components(self.components_lambda_function)
        global boolean_function
        global bool_tabel_global
        global on_set
        global off_set
        if not self.logicalFunction[0]:
            self.ids.generated_function.text = self.logicalFunction[1]
            boolean_function = self.logicalFunction[0]
            bool_tabel_global = self.logicalFunction[1]
        else:
            self.str_logical_function = "f(" + ", ".join(self.logicalFunction[0]) + ") = " + self.logicalFunction[1]
            self.ids.generated_function = self.str_logical_function
            self.bool_tabel, on_set, off_set = logicals_function(*self.logicalFunction)
            bool_tabel_global = self.bool_tabel
            boolean_function = self.str_logical_function

    def button_color(self,id):
        if id == "on_set":
            self.ids.on_set.background_color = 0.8, 0.8, 0.8, 0.8
        else:
            self.ids.on_set.background_color = 1, 1, 1, 1
        if id == "off_set":
            self.ids.off_set.background_color = 0.8, 0.8, 0.8, 0.8
        else:
            self.ids.off_set.background_color = 1, 1, 1, 1
        if id == "VDNF":
            self.ids.VDNF.background_color = 0.8, 0.8, 0.8, 0.8
        else:
            self.ids.VDNF.background_color = 1, 1, 1, 1
        if id == "KDNF":
            self.ids.KDNF.background_color = 0.8, 0.8, 0.8, 0.8
        else:
            self.ids.KDNF.background_color = 1, 1, 1, 1

    def last_button_pressed(self,called_from):
        comparison = self.last_button != called_from
        if comparison:
            self.last_button=called_from
        return comparison
    
    def logical_function_change(self):
        comparison = self.components_lambda_function != self.ids.input_function.text
        if comparison:
            self.components_lambda_function = self.ids.input_function.text
            self.update_outputs()
        return comparison
    
    def button_pressed_on_set(self):
        self.button_color("on_set")
        boolean = False
        if self.logical_function_change():
            boolean = True
        if self.last_button_pressed("on-set"):
            boolean = True
        if boolean:
            if on_set:
                output_text = list_to_string_intervalls(on_set)
            else:
                output_text = "empty"
            self.ids.output.text = output_text

    def button_pressed_off_set(self):
        self.button_color("off_set")
        boolean = False
        if self.logical_function_change():
            boolean = True
        if self.last_button_pressed("off-set"):
            boolean = True
        if boolean:
            if off_set:
                output_text = list_to_string_intervalls(off_set)
            else:
                output_text = "empty"
            self.ids.output.text = output_text

    def button_pressed_VDNF(self):
        self.button_color("VDNF")
        boolean = False
        if self.logical_function_change():
            boolean = True
        if self.last_button_pressed("VDNF"):
            boolean = True
        if boolean:
            if on_set:
                self.ids.output.text = "f(" + ", ".join(self.logicalFunction[0]) + ") = " + gen_VDNF(on_set)
            else:
                self.ids.output.text = "empty"

    def button_pressed_KDNF(self):
        self.button_color("KDNF")
        boolean = False
        if self.logical_function_change():
            boolean = True
        if self.last_button_pressed("KDNF"):
            boolean = True
        if boolean:
            if on_set:
                self.ids.output.text = "f(" + ", ".join(self.logicalFunction[0]) + ") = " + gen_KDNF(on_set)
            else:
                self.ids.output.text = "empty"

    def button_pressed_bool_tabel(self):
        self.logical_function_change()
        self.last_button_pressed("bool Tabel")

    def button_pressed_minimized(self):
        self.logical_function_change()
        self.last_button_pressed("minimize")

class Screen_Bool_Tabel(Screen):
    def on_pre_enter(self):
        global bool_tabel_global
        global boolean_function
        if not boolean_function:
            self.ids.function.text = bool_tabel_global
            self.ids.output.text = "please go back and correct your Input"
        else:
            self.ids.function.text = boolean_function
            self.ids.output.text = bool_tabel_global

class Screen_Minimized_Function(Screen):
    prim_elements = None
    steps = None
    cover = None
    global on_set
    global boolean_function
    def on_pre_enter(self):
        global on_set
        global boolean_function
        if not boolean_function:
            self.ids.function.text = bool_tabel_global
            self.ids.output.text = "please go back and correct your Input"
        else:
            self.prim_elements, self.steps, self.cover = minimize(deepcopy(on_set))
            self.ids.McCluskey.background_color = 0.8, 0.8, 0.8, 0.8
            self.ids.function.text = boolean_function
            self.ids.output.text = str(self.steps)

    def button_pressed_McCluskey(self):
        self.ids.output.text = str(self.steps)
        self.ids.McCluskey.background_color = 0.8, 0.8, 0.8, 0.8
        self.ids.prime.background_color = 1, 1, 1, 1
        self.ids.optimized.background_color = 1, 1, 1, 1 

    def button_pressed_prime(self):
        self.ids.output.text = str(self.prim_elements)
        self.ids.McCluskey.background_color = 1, 1, 1, 1
        self.ids.prime.background_color = 0.8, 0.8, 0.8, 0.8 
        self.ids.optimized.background_color = 1, 1, 1, 1 

    def button_pressed_optimized(self):
        self.ids.output.text = "needed elements:\n    " + list_to_string_intervalls(self.cover[0]) + "\n" + string_not_covered(self.cover[1])
        self.ids.McCluskey.background_color = 1, 1, 1, 1
        self.ids.prime.background_color = 1, 1, 1, 1 
        self.ids.optimized.background_color = 0.8, 0.8, 0.8, 0.8

class Compare_Logical_Functions(Screen):
    def button_pressed_compare(self):
        function_1 = string_to_lambda_components(self.ids.input_function_1.text)
        function_2 = string_to_lambda_components(self.ids.input_function_2.text)
        if not function_1[0]:
            self.ids.output.text = "Problem with Function 1:\n" + function_1[1]
        elif not function_2[0]:
            self.ids.output.text = "Problem with Function 2:\n" + function_2[1]
        else:
            functions = "f(" + ", ".join(function_1[0]) + ") = " + function_1[1] + "\ng(" + ", ".join(function_2[0]) + ") = " + function_2[1] + "\n"
            on_set_1 = logicals_function(*function_1)[1]
            on_set_2 = logicals_function(*function_2)[1]
            boolean = True
            for i in range(len(on_set_1) if len(on_set_1)<len(on_set_2) else len(on_set_2)):
                if on_set_1[i] != on_set_2[i]:
                    self.ids.output.text = functions + "different(" + str(on_set_1[i]) + ", " + str(on_set_2[i]) +")"
                    boolean = False
                    break
            if boolean:
                self.ids.output.text = functions + "the same!"

class Main_Menu_App(App):
    def build(self):
        global screen_manager
        screen_manager = ScreenManager()
        screen_manager.add_widget(Choose_Application(name = 'Choose_Application'))
        screen_manager.add_widget(Evaluate_Logical_Function(name = 'Evaluate_Logical_Function'))
        screen_manager.add_widget(Screen_Bool_Tabel(name = 'Screen_Bool_Tabel'))
        screen_manager.add_widget(Screen_Minimized_Function(name = 'Screen_Minimized_Function'))
        screen_manager.add_widget(Compare_Logical_Functions(name = 'Compare_Logical_Functions'))
        return screen_manager

if __name__ == "__main__":
    print("started")
    Main_Menu_App().run()