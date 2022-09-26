from functools import partial

from tkinter import Tk, StringVar
from tkinter import ttk
from turtle import width

from typing import Protocol


from dndresmanager.resource import Resource
from dndresmanager.constants import RestTypes

class BackendProtocol(Protocol):
    character_name:str
    character_resources:dict[int, Resource]

    def decrement_resource(self, resource_rank:int)->int:
        ...

    def increment_resource(self, resource_rank:int)->int:
        ...

    def take_rest(self, rest_type:RestTypes):
        ...


class Gui():
    resource_uses_labels:dict[int,StringVar] = {}

    def __init__(self, backend:BackendProtocol):
        self.backend = backend
        self.root = Tk()
        self.root.title(self.backend.character_name)
        self.construct_from_character()
        self.set_all_string_vars()
        self.root.mainloop()
    
    def construct_from_character(self):
        self.main_frame = ttk.Frame(self.root, padding=20)
        self.main_frame.grid()
        ttk.Label(self.main_frame, text=self.backend.character_name).grid(column=0, row=0, columnspan=2)
        resources_frame = ttk.Frame(self.main_frame, padding=5)
        resources_frame.grid(column=0, row=1, columnspan=2)

        self.resource_uses_labels = {}
        for i, (rank, resource) in enumerate(self.backend.character_resources.items()):
            resource_frame = ttk.Frame(resources_frame, padding=5)
            resource_frame.grid(column=0, row=i, sticky="w")

            ttk.Label(resource_frame, text=resource.resource_name).grid(column=0, row=0, sticky="w",columnspan=3)

            self.resource_uses_labels[rank] = StringVar()
            uses_label = ttk.Label(resource_frame, textvariable = self.resource_uses_labels[rank], width=8, justify='center')

            ttk.Button(resource_frame, text = "-", command=partial(self.inc_dec_button, False, rank, uses_label) , width=10).grid(column=0, row=1, sticky="w")
            uses_label.grid(column=1, row=1, sticky="w")
            ttk.Button(resource_frame, text = "+", command=partial(self.inc_dec_button, True, rank, uses_label), width=10).grid(column=2, row=1, sticky="w")
        
        short_rest_button = ttk.Button(self.main_frame, text = "Short Rest", command=partial(self.rest_button_command, RestTypes.SHORT), width=10)
        long_rest_button = ttk.Button(self.main_frame, text = "Long Rest", command=partial(self.rest_button_command, RestTypes.LONG), width=10)
        short_rest_button.grid(row=2,column=0)
        long_rest_button.grid(row=2,column=1)


    def inc_dec_button(self, inc:bool, rank:int, label:ttk.Label):
        if inc:
            be_func = self.backend.increment_resource
        else:
            be_func = self.backend.decrement_resource

        uses_left, max_uses = be_func(rank)
        self.set_string_var(rank)

    def set_all_string_vars(self):
        for rank in self.resource_uses_labels:
            self.set_string_var(rank)

    def set_string_var(self, rank):
            be_resource = self.backend.character_resources[rank]
            self.resource_uses_labels[rank].set(f"{be_resource.uses_left} / {be_resource.max_uses}")

    def rest_button_command(self, rest_type:RestTypes):
        self.backend.take_rest(rest_type)
        self.set_all_string_vars()


