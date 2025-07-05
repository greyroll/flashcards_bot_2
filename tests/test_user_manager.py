def test_create_and_get_user(user_manager):
    user = user_manager.create(tg_id=999, name="Test User")
    fetched = user_manager.get_by_tg_id(999)
    assert fetched is not None
    assert fetched.name == "Test User"

