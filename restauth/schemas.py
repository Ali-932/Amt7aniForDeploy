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
    stage:int


class TokenOut(Schema):
    access: str


class AccountOut(Schema):
    email: EmailStr

class StageOut(Schema):
    stages: str
    type: str
    id:int

class ProfileOut(Schema):
    name:str
    gender:str
    stage:StageOut
    id:int
class AuthOut(Schema):
    token: TokenOut
    account: AccountOut
    profile_out: ProfileOut

class ResetPassword(Schema):

    password1: str = Field(min_length=9)
    password2: str = Field(min_length=9)

class SigninIn(Schema):
    email: EmailStr
    password: str


class FourOFourOut(Schema):
    detail: str

class ResetPasswordRequest(Schema):
    email: EmailStr

class Codein(Schema):
    code:str
    email:EmailStr
class TwoOTwo(Schema):
    detail: str

class TwoOO(Schema):
    detail: str

class FourOO(Schema):
    detail: str
class FourOThree(Schema):
    detail: str
