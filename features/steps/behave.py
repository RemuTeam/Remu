from behave import *


@given('nothing special has happened')
def step_impl(context):
    pass


@when('this test is run')
def step_impl(context):
    assert True is not False


@then('the test should pass')
def step_impl(context):
    assert context.failed is False