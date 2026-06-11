from database.supabase_client import get_supabase_client
import inspect

c = get_supabase_client()
print('supabase auth class', type(c.auth))
print('auth methods:', [m for m in dir(c.auth) if not m.startswith('_')])
print('sign_up repr:', repr(c.auth.sign_up))
print('sign_in_with_password repr:', repr(c.auth.sign_in_with_password))
print('sign_up signature:', inspect.signature(c.auth.sign_up))
print('sign_in_with_password signature:', inspect.signature(c.auth.sign_in_with_password))
try:
    print('sign_up doc:', c.auth.sign_up.__doc__)
except Exception as e:
    print('doc error', e)
