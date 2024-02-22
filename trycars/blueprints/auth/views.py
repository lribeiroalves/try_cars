from flask import render_template

from .forms import RegisterForm

def register_views(bp):
    @bp.route('/register', methods=['GET', 'POST'])
    def register():
        form = RegisterForm()
        return render_template('auth/register.html', form=form)
