def test_get_by_id(setup_categories):
    manager = setup_categories
    cat = manager.get_by_id(1)
    assert cat is not None
    assert cat.name == "Top Level"

def test_get_by_name(setup_categories):
    manager = setup_categories
    cat = manager.get_by_name("Top Level")
    assert cat is not None
    assert cat.description == "Main"

def test_get_top_level_cats(setup_categories):
    manager = setup_categories
    top_cats = manager.get_top_level_cats()
    assert len(top_cats) == 1
    assert top_cats[0].parent_id is None

def test_get_subcats_by_parent_id(setup_categories):
    manager = setup_categories
    sub_cats = manager.get_subcats_by_parent_id(1)
    assert len(sub_cats) == 1
    assert sub_cats[0].name == "Sub Level"
