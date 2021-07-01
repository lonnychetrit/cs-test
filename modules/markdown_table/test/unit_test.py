import pytest
import tftest


@pytest.fixture
def plan():
  tf = tftest.TerraformTest(".")
  tf.setup(extra_files=["test/unit_test.auto.tfvars"])
  return tf.plan(output=True)

def test_outputs(plan):
  assert plan.outputs['markdown_table_string'] == "|Name|Age|\n|:--:|--:|\n|Jhon|32|\n|Doe|23|"