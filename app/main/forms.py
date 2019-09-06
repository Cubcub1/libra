from flask_pagedown.fields import PageDownField
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, SubmitField, BooleanField, SelectField, TextAreaField, FileField
from wtforms.validators import DataRequired, Length, Email, Regexp

from ..models import Role, User


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('提交')


class EditProfileForm(FlaskForm):
    avatar = FileField('头像', validators=[FileAllowed(['jpg', 'png'], '只接受.jpg和.png的图片')])
    name = StringField('姓名', validators=[Length(0, 64)])
    location = StringField('地理位置', validators=[Length(0, 64)])
    about_me = TextAreaField('自我介绍')
    submit = SubmitField('提交')


class EditProfileAdminForm(FlaskForm):
    avatar = FileField('头像', validators=[FileAllowed(['jpg', 'png'], '只接受.jpg和.png的图片')])
    email = StringField('邮箱', validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField('用户名', validators=[DataRequired(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                                                                    '用户名仅由字母，数字，_构成')])
    confirmed = BooleanField('确认')
    role = SelectField('角色', coerce=int)
    name = StringField('真实姓名', validators=[Length(0, 64)])
    location = StringField('地理位置', validators=[Length(0, 64)])
    about_me = TextAreaField('自我介绍')
    submit = SubmitField('提交')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name) for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and User.query.filter_by(email=field.data).first():
            raise ValueError('邮箱已经存在！')

    def validate_username(self, field):
        if field.data != self.user.username and User.query.filter_by(username=field.data).first():
            raise ValueError('用户名已存在！')


class PostForm(FlaskForm):
    body = PageDownField("想要说点什么？", validators=[DataRequired()])
    submit = SubmitField('发布')


class CommentForm(FlaskForm):
    body = StringField('', validators=[DataRequired()])
    submit = SubmitField('评论')
