from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, \
    TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Email, \
    Regexp, ValidationError
from flask_pagedown.fields import PageDownField
from ..models import Role, User


class NameForm(FlaskForm):
    name = StringField('Cual es tu nombre?', validators=[DataRequired()])
    submit = SubmitField('Submit')


class PostForm(FlaskForm):
    body = PageDownField("Haz una publicación:", validators=[DataRequired()])
    submit = SubmitField('Publicar')


class EditProfileForm(FlaskForm):
    # name = StringField('Real name', validators=[Length(0, 64)])
    location = StringField('Ubicación', validators=[Length(0, 64)])
    about_me = TextAreaField('Sobre mi')
    submit = SubmitField('Guardar')


class EditProfileAdminForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    alias = StringField('Alias', validators=[
        DataRequired(), Length(1, 64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               'Los nombres de usuario deben tener solo letras, números, puntos o guiones bajos ')])
    confirmed = BooleanField('Confirmado')
    role = SelectField('Rol', coerce=int)
    # name = StringField('Real name', validators=[Length(0, 64)])
    location = StringField('Ubicacion', validators=[Length(0, 64)])
    about_me = TextAreaField('Sobre mi')
    submit = SubmitField('Guardar')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError('El email ya esta registrado.')

    def validate_alias(self, field):
        if field.data != self.user.alias and \
                User.query.filter_by(alias=field.data).first():
            raise ValidationError('El alias ya esta en uso.')
