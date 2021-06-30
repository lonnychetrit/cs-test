import pytest
import tftest


@pytest.fixture
def plan():
  tf = tftest.TerraformTest(".")
  tf.setup(extra_files=['unit_test.tfvars'])
  return tf.plan(output=True)


# def test_variables(plan):
#   assert 'prefix' in plan.variables
#   assert plan.variables['names'] == ['one', 'two']



# def test_outputs(plan):
#   assert sorted(plan.outputs['gcs_buckets'].keys()) == plan.variables['names']

def test_outputs(plan):
  assert plan.outputs['unit_test'] == "ok"

# def test_root_resource(plan):
#   res = plan.resources['google_project_iam_member.test_root_resource']
#   assert res['values']['project'] == plan.variables['project_id']


# def test_modules(plan):
#   mod = plan.modules['module.gcs-buckets']
#   res = mod.resources['google_storage_bucket.buckets[0]']
#   assert res['values']['location'] == plan.variables['gcs_location']