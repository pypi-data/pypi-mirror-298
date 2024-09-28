from yta_general_utils.programming.error_message import ErrorMessage
from yta_general_utils.file.filename import filename_is_type, FileType
from yta_general_utils.checker.type import variable_is_positive_number
from yta_general_utils.file.checker import file_exists
from yta_general_utils.checker.url import url_is_ok
from typing import Union


class ParameterValidator:
    @classmethod
    def validate_mandatory_parameter(cls, name: str, value):
        if not value:
            raise Exception(ErrorMessage.parameter_not_provided(name))
        
    @classmethod
    def validate_string_parameter(cls, name: str, value: str):
        if not isinstance(value, str):
            raise Exception(ErrorMessage.parameter_is_not_string(name))

    @classmethod
    def validate_bool_parameter(cls, name: str, value: bool):
        if not isinstance(value, bool):
            raise Exception(ErrorMessage.parameter_is_not_boolean(name))
        
    @classmethod
    def validate_file_exists(cls, name: str, value: str):
        if not file_exists(value):
            raise Exception(ErrorMessage.parameter_is_file_that_doesnt_exist(name))
        
    @classmethod
    def validate_filename_is_type(cls, name: str, value: str, file_type: FileType = FileType.IMAGE):
        if not filename_is_type(value, file_type):
            raise Exception(ErrorMessage.parameter_is_not_file_of_file_type(name, file_type))
        
    @classmethod
    def validate_url_is_ok(cls, name: str, value: str):
        if not url_is_ok(value):
            raise Exception(ErrorMessage.parameter_is_not_valid_url(name))
        
    @classmethod
    def validate_positive_number(cls, name: str, value: Union[int, float]):
        if not variable_is_positive_number(value):
            raise Exception(ErrorMessage.parameter_is_not_positive_number(name))

    @classmethod
    def validate_is_class(cls, name: str, value, class_names: Union[list[str], str]):
        """
        Validates if the provided 'value' is one of the provided 'class_names'
        by using the 'type(value).__name__' checking.
        """
        if isinstance(class_names, str):
            class_names = [class_names]

        if not type(value).__name__ in class_names:
            raise Exception(ErrorMessage.parameter_is_not_class(name, class_names))
        
    # Complex ones below
    @classmethod
    def validate_string_mandatory_parameter(cls, name: str, value: str):
        """
        Validates if the provided 'value' is a valid and non
        empty string.
        """
        cls.validate_mandatory_parameter(name, value)
        cls.validate_string_parameter(name, value)

    @classmethod
    def validate_numeric_positive_mandatory_parameter(cls, name: str, value: str):
        """
        Validates if the provided 'value' is a positive numeric
        value.
        """
        cls.validate_mandatory_parameter(name, value)
        cls.validate_positive_number(name, value)