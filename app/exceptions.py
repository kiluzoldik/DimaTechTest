from fastapi import HTTPException


class BaseDimaTechException(Exception):
    detail = "Неожиданная ошибка"
    
    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)
    

class BaseDimaTechHTTPException(HTTPException):
    status_code = 500
    detail = None
    
    def __init__(self):
        super().__init__(detail=self.detail, status_code=self.status_code)
        
        
class SignatureValidationException(BaseDimaTechException):
    detail = "Подпись транзакции не совпадает"
    
    
class SignatureValidationHTTPException(BaseDimaTechHTTPException):
    status_code = 400
    detail = "Подпись транзакции не совпадает"
    
    
class ObjectNotFoundException(BaseDimaTechException):
    detail = "Объект не найден"
    
    
class AccountNotFoundException(BaseDimaTechException):
    detail = "Счет не найден"
    
    
class AccountNotFoundHTTPException(BaseDimaTechHTTPException):
    status_code = 404
    detail = "Такого финансового счета у вас нет"
    
    
class UserNotFoundException(BaseDimaTechException):
    detail = "Пользователь не найден"
    
    
class UserEmailNotFoundException(BaseDimaTechException):
    detail = "Пользователь с таким email не найден"
    
    
class UserEmailNotFoundHTTPException(BaseDimaTechHTTPException):
    status_code = 404
    detail = "Пользователь с таким email не найден"
    
    
class UserNotFoundHTTPException(BaseDimaTechHTTPException):
    status_code = 404
    detail = "Пользователь не найден"
    
    
class EmailPasswordValidationException(BaseDimaTechException):
    detail = "Неверный email или пароль"
    
    
class EmailPasswordValidationHTTPException(BaseDimaTechHTTPException):
    status_code = 401
    detail = "Неверный email или пароль"
    
    
class ObjectAlreadyExistsException(BaseDimaTechException):
    detail = "Объект уже существует"
    
    
class UserEmailAlreadyExistsException(BaseDimaTechException):
    detail = "Пользователь с таким email уже существует"
    
    
class UserEmailAlreadyExistsHTTPException(BaseDimaTechHTTPException):
    status_code = 409
    detail = "Пользователь с таким email уже существует"
    
    
class FullNameLengthHTTPException(BaseDimaTechHTTPException):
    status_code = 400
    detail = "ФИО должно содержать не менее 10 символов"
    
    
class FullNameValidationHTTPException(BaseDimaTechHTTPException):
    status_code = 400
    detail = "ФИО не должно содержать чисел"
    
    
class LengthPasswordHTTPException(BaseDimaTechHTTPException):
    status_code = 400
    detail = "Пароль должен быть не менее 8 символов"


class DigitPasswordHTTPException(BaseDimaTechHTTPException):
    status_code = 400
    detail = "Пароль должен содержать хотя бы одну цифру"


class UpperLetterPasswordHTTPException(BaseDimaTechHTTPException):
    status_code = 400
    detail = "Пароль должен содержать хотя бы одну заглавную букву"


class SpecialSimbolPasswordHTTPException(BaseDimaTechHTTPException):
    status_code = 400
    detail = "Пароль должен содержать хотя бы один спецсимвол"
    
    
class EmailException(BaseDimaTechException):
    detail = "Неверный формат Email"


class EmailHTTPException(BaseDimaTechHTTPException):
    status_code = 400
    detail = "Неверный формат Email"


class DeleteAccountBalanceNotNullException(BaseDimaTechException):
    detail = "Нельзя удалить счет, на нём остались средства"


class DeleteAccountBalanceNotNullHTTPException(BaseDimaTechHTTPException):
    status_code = 409
    detail = "Нельзя удалить счет, на нём остались средства"
    
    
class TransactionIdAlreadyExistsException(BaseDimaTechException):
    detail = "Данная транзакция была выполнена успешно до этого"
    
    
class TransactionIdAlreadyExistsHTTPException(BaseDimaTechHTTPException):
    status_code = 409
    detail = "Данная транзакция была выполнена успешно до этого"