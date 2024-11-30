import pytest
from todolist.models import *

@pytest.mark.django_db
def test_model_creation():
    instance = Label.objects.create(name="Test")
    assert instance.name == "Test"
