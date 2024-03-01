from email_validator import validate_email, EmailNotValidError

email = "lucasribeiroalves@live.com"
# email = "lu_ks_2009@hotmail.com"
# email = "my+address@example.org"

try:

  # Check that the email address is valid. Turn on check_deliverability
  # for first-time validations like on account creation pages (but not
  # login pages).
  emailinfo = validate_email(email, check_deliverability=True)

  # After this point, use only the normalized form of the email address,
  # especially before going to a database query.
  email = emailinfo.normalized
  print(email)

except EmailNotValidError as e:

  # The exception message is human-readable explanation of why it's
  # not a valid (or deliverable) email address.
  print(str(e))


  """
  [default]
SECRET_KEY = "3ec9611465644c07eada0eb02bf1974299d00f8cd63da3640429a1e727d5dcdc"
SECURITY_PASSWORD_SALT = '99282770629822221225002529929327221620'

# Flask-mail
MAIL_USERNAME = 'no_reply_trycars@outlook.com'
MAIL_PASSWORD = 'dP>Q7E156_b'
# MAIL_USERNAME = 'noreply.trycars@gmail.com'
# MAIL_PASSWORD = 'ekay hsmh rjca zfzl'

#ReCaptcha
RECAPTCHA_PUBLIC_KEY = '6LfCLHspAAAAAEh31OgTKSzdGqfjZX0DdUveFvdf'
RECAPTCHA_PRIVATE_KEY  = '6LfCLHspAAAAANYymjlStdsGH-bMtKKfHYlEK4KY'
"""