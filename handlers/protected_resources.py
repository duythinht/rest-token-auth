from bottle import *
from auth import login_required

@get('/resource')
@login_required
def resource():
  return dict(ok=True, message='Welcome to Marvel Universal', uid=request.uid)
