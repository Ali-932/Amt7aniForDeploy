from allauth.account.signals import email_confirmed
from django.dispatch import receiver
from ninja import Router
from django.contrib.auth.password_validation import validate_password
from .schemas import FourOFourOut, TwoOTwo, ResetPasswordRequest, TwoOO, ResetPassword, FourOO, FourOThree, TokenOut
from config import status
from .authorization import create_token_for_user
from .schemas import AccountIn, AuthOut, SigninIn
from django.core import exceptions
from allauth.account.utils import *
from Home.models import Profile, Stage,StageChoices,Gender

auth_router = Router(tags=['auth'])
User = get_user_model()

@auth_router.post('signup', response={
    400: FourOFourOut,
    202: TwoOTwo,
    201:TwoOO
},auth=None)
def signup(request, account_in: AccountIn):
    if account_in.password1 != account_in.password2:
        return status.BAD_REQUEST_400, {'detail': 'Passwords don\'t match'}
    try:
        validate_password(password=account_in.password1)
    except exceptions.ValidationError as e:
        return status.BAD_REQUEST_400, {'detail': '{}'.format(e)}
    try:
        st = Stage.objects.get(stages=account_in.stage)
    except:
        return status.BAD_REQUEST_400, {'detail': 'stage does not exist'}

    try:
        User.objects.get(email=account_in.email)
    except User.DoesNotExist:
        new_user = User.objects.create_user(
            full_name=account_in.fullname,
            email=account_in.email,
            password=account_in.password1
        )
        new_user.is_active = False
        new_user.save()
        try:
            send_email_confirmation(request, new_user, True)
        except:
            new_user.delete()
            return status.BAD_REQUEST_400, {'detail': 'connection error'}

        @receiver(email_confirmed)
        def email_confirmed_(request, email_address, **kwargs):

            user = User.objects.get(email=email_address.email)
            user.is_active = True
            user.save()
            Profile.objects.create(user=user,stage=st,gender='Male')
            return status.CREATED_201, {'detail': 'user is created'}



        return status.ACCEPTED_202, {
            'detail': 'signed up successfully,check your email',
            'account': new_user
        }

    return status.BAD_REQUEST_400, {'detail': 'Email is taken'}

@auth_router.get('/get_stages',auth=None)
def get_stages(request):
    return status.OK_200,{t[0]: t[1] for t in StageChoices.stages}
@auth_router.get('/get_gender',auth=None)
def get_stages(request):
    return status.OK_200,{t[0]: t[1] for t in Gender.gender}

@auth_router.post('signin', response={
    200: AuthOut,
    404: FourOFourOut,
    403: FourOThree
},auth=None)
def signin(request, signin_in: SigninIn):
    try:
        user = User.objects.get(email=signin_in.email)
        if user.is_active == False:
            return status.FORBIDDEN_403, {'detail': 'Email is not activated '}

    except User.DoesNotExist:
        user = None

    else:
        if user.check_password(signin_in.password):
            token = create_token_for_user(user)
            return status.OK_200, {
                'token': token,
                'account': user
            }
        else:
            return status.FORBIDDEN_403, {'detail': 'password is not correct '}

    if not user:
        return status.NOT_FOUND_404, {'detail': 'User is not registered'}


@auth_router.post('password_resert_request', response={
    200: TokenOut,
    404: FourOFourOut,
    202: TwoOTwo,
    403: FourOThree
},auth=None)
def reset_password_request(request, pass_reset: ResetPasswordRequest):
    try:
        user = User.objects.get(email=pass_reset.email)
    except User.DoesNotExist:
        return status.NOT_FOUND_404, {'detail': 'User is not registered'}
    else:
        if user.is_active == False:
            return status.FORBIDDEN_403, {'detail': 'Email is not activated '}

        send_email_confirmation(request, user, True)

        @receiver(email_confirmed)
        def email_confirmed1(request, email_address, **kwargs):
            token = create_token_for_user(user)
            print(token)
            return status.OK_200, {'access': token}#need token

        return status.ACCEPTED_202, {'detail': 'email sent'}


@auth_router.put('/set_new_password', response={
    200: TwoOO,
    404: FourOFourOut,
    400: FourOO,
    403: FourOThree
})
def reset_password(request, pass_reset: ResetPassword):
    try:
        user = User.objects.get(email=pass_reset.email)
    except User.DoesNotExist:
        return status.NOT_FOUND_404, {'detail': 'User is not registered'}
    else:
        if user.is_active == False:
            return status.FORBIDDEN_403, {'detail': 'Email is not activated '}
        if pass_reset.password1 != pass_reset.password2:
            return status.BAD_REQUEST_400, {'detail': 'Passwords don\'t match'}
    try:
        validate_password(password=pass_reset.password1)

    except exceptions.ValidationError as e:
        return status.BAD_REQUEST_400, {'detail': '{}'.format(e)}
    else:
        user.set_password(pass_reset.password1)
        user.save()
        return status.OK_200, {'detail': 'Password changed'}

