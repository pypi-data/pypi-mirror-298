from django.core.management import call_command
from django.test import TestCase


class CollectStaticTestCase(TestCase):
    def test_run_collectstatic(self):
        """
        Run `collectstatic`

        `collectstatic` and possibly other commands often call
        the database `close` method before running to make sure
        the state is clean. In our database wrapper we check whether
        connections are active before closing and running the upload
        function.
        """

    def test_collectstatic(self):
        call_command("collectstatic", interactive=False, clear=True)
