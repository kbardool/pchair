__author__ = 'KBardool'

DEBUG  = True

# frozen set is immutable
ADMINS = frozenset([ os.environ.get(ADMIN_ACCOUNT) ])