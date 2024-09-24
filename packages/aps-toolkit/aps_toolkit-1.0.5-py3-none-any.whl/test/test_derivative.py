from unittest import TestCase

from .context import Derivative
from .context import Auth


class TestDerivative(TestCase):
    def setUp(self):
        self.urn = "dXJuOmFkc2sud2lwcHJvZDpmcy5maWxlOnZmLk9kOHR4RGJLU1NlbFRvVmcxb2MxVkE_dmVyc2lvbj0yNA"
        self.token = Auth().auth2leg()

    def test_translate_job(self):
        self.urn = "dXJuOmFkc2sub2JqZWN0czpvcy5vYmplY3Q6Y2h1b25nX2J1Y2tldC9NeUhvdXNlLm53Yw"
        derivative = Derivative(self.urn, self.token)
        response = derivative.translate_job("Project Completion.ifc")
        self.assertNotEquals(response, "")

    def test_check_job_status(self):
        self.urn = "dXJuOmFkc2sub2JqZWN0czpvcy5vYmplY3Q6Y2h1b25nX2J1Y2tldC9NeUhvdXNlLm53Yw"
        derivative = Derivative(self.urn, self.token)
        response = derivative.check_job_status()
        self.assertNotEquals(response, "")

    def test_read_svf_manifest_items(self):
        derivative = Derivative(self.urn, self.token)
        manifest_items = derivative.read_svf_manifest_items()
        self.assertNotEquals(len(manifest_items), 0)

    def test_read_svf_resource(self):
        derivative = Derivative(self.urn, self.token)
        svf_resources = derivative.read_svf_resource()
        self.assertNotEquals(len(svf_resources), 0)

    def test_read_svf_resource_item(self):
        derivative = Derivative(self.urn, self.token)
        manifest_items = derivative.read_svf_manifest_items()
        svf_resources = derivative.read_svf_resource_item(manifest_items[0])
        self.assertNotEquals(len(svf_resources), 0)

    def test_read_metadata(self):
        derivative = Derivative(self.urn, self.token)
        manifest_items = derivative.read_svf_manifest_items()
        for manifest_item in manifest_items:
            metadata = derivative.read_svf_metadata(manifest_item.urn)
            self.assertNotEquals(metadata, "")

    def test_get_metadata(self):
        derivative = Derivative(self.urn, self.token)
        df = derivative.get_metadata()
        self.assertNotEquals(df, "")
