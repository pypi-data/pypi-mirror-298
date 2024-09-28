import typing
from dataclasses import dataclass
from typing import get_args, get_origin, Optional, Union


@dataclass
class UserDefinedType:
    name: str
    fields: list['FieldDefinition']
    comment: Optional[str] = None

    def with_comment(self, c: str):
        self.comment = c
        return self

    def to_dict(self):
        ret = dict(
            type='UserDefinedType',
            name=self.name,
            fields=[x.to_dict() for x in self.fields],
        )
        if self.comment is not None:
            ret['comment'] = self.comment

        return ret


@dataclass
class PrimitiveType:
    """
    Supported types:
    int
    float
    str
    bool
    list
    dict
    any
    """
    name: str
    comment: Optional[str] = None

    def with_comment(self, c: str):
        self.comment = c
        return self

    @staticmethod
    def create_from_class_or_none(clz) -> Optional['PrimitiveType']:

        if clz is int:
            return PrimitiveType(name='int')

        elif clz is float:
            return PrimitiveType(name='float')

        elif clz is bool:
            return PrimitiveType(name='bool')

        elif clz is str:
            return PrimitiveType(name='str')

        elif clz is list:
            return PrimitiveType(name='list')

        elif clz is dict:
            return PrimitiveType(name='dict')

        elif clz is tuple:
            return PrimitiveType(name='list')

        return None

    def to_dict(self):
        ret = dict(
            type='PrimitiveType',
            name=self.name,
        )
        if self.comment is not None:
            ret['comment'] = self.comment

        return ret


@dataclass
class InlineType:
    fields: list['FieldDefinition']
    comment: Optional[str] = None

    def with_comment(self, c: str):
        self.comment = c
        return self

    def to_dict(self):
        ret = dict(
            type='InlineType',
            fields=[x.to_dict() for x in self.fields],
        )
        if self.comment is not None:
            ret['comment'] = self.comment

        return ret


@dataclass
class ParameterizedType:
    """
    Supported types:
        * List
        * Dict
        * Tuple
        * Union
        * Optional
    """
    name: str
    params: list['ResolvedType']
    comment: Optional[str] = None

    def with_comment(self, c: str):
        self.comment = c
        return self

    def to_dict(self):
        ret = dict(
            type='ParameterizedType',
            name=self.name,
            params=[x.to_dict() for x in self.params],
        )
        if self.comment is not None:
            ret['comment'] = self.comment

        return ret

    @staticmethod
    def get_parameterized_type_or_none(clz, origin):
        name = None

        if origin is list or origin is typing.List:
            name = 'list'
        elif origin is dict or origin is typing.Dict:
            name = 'dict'
        elif origin is tuple or origin is typing.Tuple:
            name = 'tuple'
        elif origin is typing.Union:
            # note: typing.Optional also has origin Union
            name = 'union'

        if name is not None:
            args = get_args(clz)

            if name == 'union':
                if len(args) == 2 and args[-1] is type(None):
                    # recast union of A | None to Optional[None]
                    name = 'optional'
                    args = [args[0]]

            children = [resolve_type(a) for a in args]
            return ParameterizedType(name=name, params=children)

        # In all other case, we will return none, and let caller handle this.
        return None


@dataclass
class EnumType:
    choices: list[str]
    comment: Optional[str] = None
    name: Optional[str] = None

    def with_comment(self, c: str):
        self.comment = c
        return self

    def with_name(self, name: str):
        self.name = name
        return self

    def to_dict(self):
        ret = dict(
            type='EnumType',
            choices=[x for x in self.choices],
        )

        if self.comment is not None:
            ret['comment'] = self.comment

        if self.name is not None:
            ret['name'] = self.name

        return ret


@dataclass
class FieldDefinition:
    name: str
    type: Union[PrimitiveType, UserDefinedType, InlineType]
    comment: Optional[str] = None

    def with_comment(self, c: str):
        self.comment = c
        return self

    def to_dict(self):
        ret = dict(
            name=self.name,
            type=self.type.to_dict(),
        )

        if self.comment is not None:
            ret['comment'] = self.comment

        return ret


ResolvedType = Union[UserDefinedType, InlineType, PrimitiveType, ParameterizedType, EnumType]


def is_resolved_type(type_def):
    if isinstance(type_def, UserDefinedType):
        return True
    if isinstance(type_def, InlineType):
        return True
    if isinstance(type_def, PrimitiveType):
        return True
    if isinstance(type_def, ParameterizedType):
        return True
    if isinstance(type_def, EnumType):
        return True
    return False


class TypeBuilder:
    @staticmethod
    def create(name: str, **kwargs) -> UserDefinedType:
        return UserDefinedType(
            name=name,
            fields=[
                FieldDefinition(name=k, type=resolve_type(v)) for k, v in kwargs.items()
            ]
        )


def is_list_of_strings(variable):
    return isinstance(variable, list) and all(isinstance(item, str) for item in variable)


def parse_unresolved_type(type_def) -> Union[PrimitiveType, ParameterizedType, EnumType]:
    """
    unresolved_type can be a primitive type or parameterizedType
    """
    origin = get_origin(type_def)
    if origin is not None:
        # Load things like List[xxx], Dict[A,B]
        pt = ParameterizedType.get_parameterized_type_or_none(type_def, origin)
        if pt is not None:
            return pt
    else:
        pt = PrimitiveType.create_from_class_or_none(type_def)
        if pt is not None:
            return pt

    return PrimitiveType(name='any')


def resolve_type(type_def) -> ResolvedType:
    if is_resolved_type(type_def):
        return type_def
    elif isinstance(type_def, dict):
        return InlineType(
            fields=[
                FieldDefinition(name=k, type=resolve_type(v)) for k, v in type_def.items()
            ]
        )
    elif is_list_of_strings(type_def):
        return EnumType(choices=type_def)
    else:
        return parse_unresolved_type(type_def)
