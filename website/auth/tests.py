from website.auth import User2


def test_user_is_complete():
  u = User2()
  assert not u.is_complete()