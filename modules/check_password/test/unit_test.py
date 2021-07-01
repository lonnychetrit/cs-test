import pytest
import tftest


@pytest.fixture
def plan():
  tf = tftest.TerraformTest(".")
  tf.setup(extra_files=["test/unit_test.auto.tfvars"])
  return tf.plan(output=True)

def test_outputs(plan):
  assert plan.outputs['passwords'] == {"non_secured_password": False, "securedpassword27!": True}