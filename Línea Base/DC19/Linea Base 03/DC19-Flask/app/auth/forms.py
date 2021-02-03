from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    remember_me = BooleanField('Mantenerme conectado')
    submit = SubmitField('Ingresar')


class RegistrationForm(FlaskForm):
    full_name = StringField('Nombres y Apellidos', validators=[DataRequired(), Length(1, 64)])
    dni = StringField('DNI', validators=[DataRequired(), Length(8, 8)])
    cui = StringField('CUI', validators=[DataRequired(), Length(1, 1)])
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    alias = StringField('Alias', validators=[
        DataRequired(), Length(1, 64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               'Los nombres de usuario deben tener solo letras, números, puntos o guiones bajos ')])
    password = PasswordField('Contraseña', validators=[
        DataRequired(), EqualTo('password2', message='Las contraseñas deben coincidir.')])
    password2 = PasswordField('Confime contraseña', validators=[DataRequired()])
    submit = SubmitField('Registrarte')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('El email ya esta registrado.')

    def validate_alias(self, field):
        if User.query.filter_by(alias=field.data).first():
            raise ValidationError('El alias ya esta en uso.')

    def validate_dni(self, field):
        if User.query.filter_by(dni=field.data).first():
            raise ValidationError('El DNI ya esta registrado')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Contraseña antigua', validators=[DataRequired()])
    password = PasswordField('Nueva contraseña', validators=[
        DataRequired(), EqualTo('password2', message='Las contraseñas deben coincidir.')])
    password2 = PasswordField('Confirma nueva contraseña',
                              validators=[DataRequired()])
    submit = SubmitField('Actualizar contraseña')


class PasswordResetRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    submit = SubmitField('Recuperar contraseña')


class PasswordResetForm(FlaskForm):
    password = PasswordField('Nueva contraseña', validators=[
        DataRequired(), EqualTo('password2', message='Las contraseñas deben coincidir.')])
    password2 = PasswordField('Confirmar contraseña', validators=[DataRequired()])
    submit = SubmitField('Guardar contraseña')


class ChangeEmailForm(FlaskForm):
    email = StringField('Nuevo email', validators=[DataRequired(), Length(1, 64),
                                                 Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Actualizar email')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError('El email ya esta registrado.')
