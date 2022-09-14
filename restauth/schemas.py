from django.contrib.auth.password_validation import validate_password
from ninja import Schema
from ninja.errors import ValidationError
from pydantic import EmailStr, Field


class AccountIn(Schema):
    fullname: str
    email: EmailStr
    password1: str = Field(min_length=9)
    password2: str = Field(min_length=9)
    gender:str
    stage:str


class TokenOut(Schema):
    access: str


class AccountOut(Schema):
    first_name: str
    last_name: str
    email: EmailStr


class AuthOut(Schema):
    token: TokenOut
    account: AccountOut

class ResetPassword(Schema):

    password1: str = Field(min_length=9)
    password2: str = Field(min_length=9)
    email: EmailStr

class SigninIn(Schema):
    email: EmailStr
    password: str


class FourOFourOut(Schema):
    detail: str

class ResetPasswordRequest(Schema):
    email: EmailStr


class TwoOTwo(Schema):
    detail: str




class TwoOO(Schema):
    detail: str

class FourOO(Schema):
    detail: str
class FourOThree(Schema):
    detail: str
