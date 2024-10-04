import os
import typing
from dataclasses import dataclass
from .exceptions import *
from .parsers import special_parsers


class PCTransformer:
    def __init__(self, replace: typing.List[
            typing.Tuple[
                typing.Tuple[str, typing.Callable[[typing.Any], typing.Any]], # inital
                typing.Tuple[str, typing.Callable[[typing.Any], typing.Any]] # replaced
            ]
        ] = None):
        if replace is None:
            replace = list()
        self.replace = replace

    def _replace(self, data: dict) -> dict:
        new_data = dict()
        for key, value in data.items():
            skip = False
            for (initial_key, _), (replaced_key, replaced_value_type) in self.replace:
                if key == initial_key:
                    key = replaced_key
                    try:
                        value = replaced_value_type(value)
                    except:
                        skip = True
            if skip:
                continue
            new_data[key] = value
        return new_data
    
    def _unreplace(self, data: dict) -> dict:
        initial_data = dict()
        for key, value in data.items():
            for (initial_key, initial_value_type), (replaced_key, _) in self.replace:
                if key == replaced_key:
                    key = initial_key
                    value = initial_value_type(value)
            initial_data[key] = value
        return initial_data
    
    def parse(self, value: typing.Any) -> typing.Dict:
        raise NotImplementedError

    def compile(self, data: typing.Dict) -> typing.Any:
        raise NotImplementedError
    

@dataclass
class Field:
    """
    Represents a configuration key for environment variables or configuration parsing.
    
    key : str
        The key used to look up the value in the .env file or other configuration sources.
    
    required : bool, optional
        Indicates whether this key is mandatory. Default is True.
    
    default : typing.Any, optional
        The default value if the key is not found or not provided. Default is None.
    
    parser_value_type : typing.Callable[[typing.Any], typing.Any], optional
        A callable that specifies the type of the values to be parsed inside complex structures like 
        lists or dictionaries. For example, if the value is a list of integers, this would be `int`. 
        If the value is a dictionary, this could define the type of its values.
        The default is `str` for handling simple string values.
    
    parser : typing.Callable[[typing.Any], typing.Any], optional
        A custom function or callable to parse the value from the configuration source. If not provided, 
        the default behavior uses annotated class.
    
    pc_transformer : PCTransformer, optional
        A transformer object used for parsing other replaceable values, if applicable. This can handle
        more complex transformations of the config value based on external logic. Check the `config.py`
        for examples of such transformations.
    """
    key: str = None
    required: bool = True
    default: typing.Any = None

    parser_value_type: typing.Callable[[typing.Any], typing.Any] = str
    parser: typing.Callable[[typing.Any], typing.Any] = None
    pc_transformer: PCTransformer = None


class BaseConfig:    
    def __init__(self, prefix: str = None):
        if prefix is not None:
            self._prefix = f"{prefix}_" 
        else:
            self._prefix = ""

        self._data = dict()
        self._fields = self._get_fields()
        
        for k, (cls, field) in self._fields.items():
            value = self._get_value(k, field)
            if value is None:
                continue

            value = self._parse_value(value, cls, field)
            self._data[k] = value

            self._pc_parse(value, field)
        
        self._pc_compile()
        self._check_required()

        self.set_values_to(self)

    def _get_fields(self) -> typing.Dict[str, typing.Tuple[object, Field]]:
        fields = dict()
        for k, cls in self.__annotations__.items():
            field: Field = getattr(self, k, None)
            if field is None:
                continue
            if not isinstance(field, Field):
                continue

            fields[k] = (cls, field)
        
        return fields

    def _get_key(self, key: str, field: Field) -> str:
        return f"{self._prefix}{field.key or key}"
    
    def _get_value(self, key: str, field: Field) -> typing.Union[str, None]:
        default = lambda: field.default() if callable(field.default) else field.default
        return os.getenv(self._get_key(key, field), self._data.get(key, default()))
    
    def _parse_value(self, value: typing.Union[str, None], cls: object, field: Field) -> typing.Any: 
        parser = cls
        parser_params = dict()
        if field.parser is not None:
            parser = field.parser
        elif cls in special_parsers:
            parser = special_parsers[cls]
            if cls is not bool:
                parser_params["value_type"] = field.parser_value_type
        
        return parser(value, **parser_params)

    def _pc_parse(self, value: typing.Union[str, None], field: Field):
        try:
            if field.pc_transformer is not None:
                self._data.update(field.pc_transformer.parse(value))
        except NotImplementedError:
            pass

    def _pc_compile(self):
        try:
            for k, (_, f) in self._fields.items():
                if f.pc_transformer is not None:
                    self._data[k] = f.pc_transformer.compile(self._data)
        except NotImplementedError:
            pass

    def _check_required(self):
        for k, (_, f) in self._fields.items():
            if f.required and k not in self._data:
                raise FieldIsRequiredException(f"the key {k} is required")

    def get_env_example(self) -> str:
        example = f"# {self._prefix.strip('_') + ' ' if self._prefix else ''}{self.__class__.__name__}\n"
        for k, (_, f) in self._fields.items():
            example += f"{self._get_key(k, f)}=\n"
        return example
    
    def set_values_to(self, destination: object):
        for k, v in self._data.items():
            setattr(destination, k, v)

    def items(self):
        return self._data.items()
    

def generate_env_example(*configs: BaseConfig, output="example.env"):
    example = ""
    for config in configs:
        example += config.get_env_example()
        example += '\n\n'
    
    with open(output, 'w') as f:
        f.write(example)


