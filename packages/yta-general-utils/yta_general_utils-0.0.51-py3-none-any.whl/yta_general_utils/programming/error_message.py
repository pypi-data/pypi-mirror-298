from yta_general_utils.file.filename import FileType


class ErrorMessage:
    @classmethod
    def parameter_not_provided(cls, parameter_name: str):
        return f'The parameter "{parameter_name}" was not provided.'
    
    @classmethod
    def parameter_is_not_string(cls, parameter_name: str):
        return f'The parameter "{parameter_name}" provided is not a string.'
    
    @classmethod
    def parameter_is_not_positive_number(cls, parameter_name: str):
        return f'The parameter "{parameter_name}" provided is not a valid and positive number.'
    
    @classmethod
    def parameter_is_file_that_doesnt_exist(cls, parameter_name: str):
        return f'The "{parameter_name}" parameter provided is not a file that exists.'
    
    @classmethod
    def parameter_is_not_file_of_file_type(cls, parameter_name: str, file_type: FileType):
        return f'The "{parameter_name}" provided is not a {file_type.value} filename.'
    
    @classmethod
    def parameter_is_not_valid_url(cls, parameter_name: str):
        return f'The provided "{parameter_name}" parameter is not a valid url.'
