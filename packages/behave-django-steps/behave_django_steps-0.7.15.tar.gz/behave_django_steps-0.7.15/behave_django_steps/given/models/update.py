"""Model update steps."""

from behave import given
from behave.runner import Context


@given('context "{model_name}" values set to')
def set_model_fields_values(context: Context, model_name: str) -> None:
    """Set context model fields to specified values.

    Args:
        context (behave.runner.Context): The behave context.
        model_name (str): name of the model to pick up an object from context.

    Returns:
        None
    """
    context.execute_steps(f'Given a "{model_name}" model is available')

    obj = getattr(context, model_name)

    context.test.assertTrue(context.table)
    context.test.assertTrue(context.table[0].as_dict())

    values = context.table[0].as_dict()

    for key, value in values.items():
        if value is None or value == "" or value == '""':
            value = None
        setattr(obj, key, value)

    obj.save()
