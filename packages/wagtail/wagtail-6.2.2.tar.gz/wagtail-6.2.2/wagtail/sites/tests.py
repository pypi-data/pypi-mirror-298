from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from django.urls import reverse

from wagtail import hooks
from wagtail.admin.admin_url_finder import AdminURLFinder
from wagtail.models import Page, Site
from wagtail.test.utils import WagtailTestUtils
from wagtail.test.utils.template_tests import AdminTemplateTestUtils


class TestSiteIndexView(AdminTemplateTestUtils, WagtailTestUtils, TestCase):
    def setUp(self):
        self.login()
        self.home_page = Page.objects.get(id=2)

    def get(self, params={}):
        return self.client.get(reverse("wagtailsites:index"), params)

    def test_simple(self):
        response = self.get()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "wagtailadmin/generic/index.html")
        self.assertBreadcrumbsItemsRendered(
            [{"url": "", "label": "Sites"}],
            response.content,
        )

    def test_num_queries(self):
        # Warm up the cache
        self.get()
        with self.assertNumQueries(9):
            self.get()

        sites = [
            Site(hostname=f"host {i}", port=f"800{i}", root_page_id=2)
            for i in range(10)
        ]
        Site.objects.bulk_create(sites)

        with self.assertNumQueries(9):
            self.get()


class TestSiteCreateView(AdminTemplateTestUtils, WagtailTestUtils, TestCase):
    def setUp(self):
        self.login()
        self.home_page = Page.objects.get(id=2)
        self.localhost = Site.objects.all()[0]

    def get(self, params={}):
        return self.client.get(reverse("wagtailsites:add"), params)

    def post(self, post_data={}):
        return self.client.post(reverse("wagtailsites:add"), post_data)

    def create_site(
        self, hostname="testsite", port=80, is_default_site=False, root_page=None
    ):
        root_page = root_page or self.home_page
        Site.objects.create(
            hostname=hostname,
            port=port,
            is_default_site=is_default_site,
            root_page=root_page,
        )

    def test_default_fixtures_present(self):
        # we should have loaded with a single site
        self.assertEqual(self.localhost.hostname, "localhost")
        self.assertEqual(self.localhost.port, 80)
        self.assertIs(self.localhost.is_default_site, True)
        self.assertEqual(self.localhost.root_page, self.home_page)

    def test_simple(self):
        response = self.get()
        self.assertEqual(response.status_code, 200)
        self.assertBreadcrumbsItemsRendered(
            [
                {"label": "Sites", "url": "/admin/sites/"},
                {"label": "New: Site", "url": ""},
            ],
            response.content,
        )

    def test_create(self):
        response = self.post(
            {
                "hostname": "testsite",
                "port": "80",
                "root_page": str(self.home_page.id),
            }
        )

        # Should redirect back to index
        self.assertRedirects(response, reverse("wagtailsites:index"))

        # Check that the site was created
        self.assertEqual(Site.objects.filter(hostname="testsite").count(), 1)

    def test_duplicate_defaults_not_allowed(self):
        response = self.post(
            {
                "hostname": "also_default",
                "port": "80",
                "is_default_site": "on",
                "root_page": str(self.home_page.id),
            }
        )

        # Should return the form with errors
        self.assertEqual(response.status_code, 200)
        self.assertIs(bool(response.context["form"].errors), True)

        # Check that the site was not created
        sites = Site.objects.filter(hostname="also_default")
        self.assertEqual(sites.count(), 0)

    def test_duplicate_hostnames_on_different_ports_allowed(self):
        response = self.post(
            {
                "hostname": "localhost",
                "port": "8000",
                "root_page": str(self.home_page.id),
            }
        )

        # Should redirect back to index
        self.assertRedirects(response, reverse("wagtailsites:index"))

        # Check that the site was created
        self.assertEqual(Site.objects.filter(hostname="localhost").count(), 2)

    def test_duplicate_hostnames_on_same_port_not_allowed(self):
        # Confirm there's one localhost already
        self.assertEqual(Site.objects.filter(hostname="localhost").count(), 1)

        response = self.post(
            {
                "hostname": "localhost",
                "port": "80",
                "root_page": str(self.home_page.id),
            }
        )

        # Should return the form with errors
        self.assertEqual(response.status_code, 200)
        self.assertIs(bool(response.context["form"].errors), True)

        # Check that the site was not created, still only one localhost entry
        self.assertEqual(Site.objects.filter(hostname="localhost").count(), 1)

    def test_duplicate_hostnames_case_variant_not_allowed(self):
        # Confirm there's one localhost already
        self.assertEqual(Site.objects.filter(hostname="localhost").count(), 1)

        response = self.post(
            {"hostname": "Localhost", "port": "80", "root_page": str(self.home_page.id)}
        )

        # Should return the form with errors
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context["form"].errors,
            {"__all__": ["Site with this Hostname and Port already exists."]},
        )

        # Check that the site was not created, still only one localhost entry
        self.assertEqual(Site.objects.filter(hostname="localhost").count(), 1)

    def test_non_field_errors_are_displayed(self):
        self.assertEqual(Site.objects.filter(hostname="localhost").count(), 1)

        response = self.post(
            {"hostname": "localhost", "port": "80", "root_page": str(self.home_page.id)}
        )
        expected_html = """
            <li class="error">
                <svg class="class="icon icon-warning messages-icon"" aria-hidden="true">
                    <use href="#icon-warning"></use>
                </svg>
                The site could not be saved due to errors.
                <ul class="errorlist">
                <li>
                Site with this Hostname and Port already exists.
                </li>
                </ul>
            </li>
        """
        self.assertTagInHTML(expected_html, response.content.decode())


class TestSiteEditView(AdminTemplateTestUtils, WagtailTestUtils, TestCase):
    def setUp(self):
        self.user = self.login()
        self.home_page = Page.objects.get(id=2)
        self.localhost = Site.objects.all()[0]

    def get(self, params={}, site_id=None):
        return self.client.get(
            reverse("wagtailsites:edit", args=(site_id or self.localhost.id,)), params
        )

    def post(self, post_data={}, site_id=None):
        site_id = site_id or self.localhost.id
        site = Site.objects.get(id=site_id)
        post_defaults = {
            "hostname": site.hostname,
            "port": site.port,
            "root_page": site.root_page.id,
        }
        for k, v in post_defaults.items():
            post_data[k] = post_data.get(k, v)
        if "default" in post_data:
            if post_data[
                "default"
            ]:  # only include the is_default_site key if we want to set it
                post_data["is_default_site"] = "on"
        elif site.is_default_site:
            post_data["is_default_site"] = "on"
        return self.client.post(
            reverse("wagtailsites:edit", args=(site_id,)), post_data
        )

    def test_simple(self):
        response = self.get()
        self.assertEqual(response.status_code, 200)
        self.assertBreadcrumbsItemsRendered(
            [
                {"url": "/admin/sites/", "label": "Sites"},
                {"url": "", "label": str(self.localhost)},
            ],
            response.content,
        )

        url_finder = AdminURLFinder(self.user)
        expected_url = "/admin/sites/edit/%d/" % self.localhost.id
        self.assertEqual(url_finder.get_edit_url(self.localhost), expected_url)

    def test_nonexistent_redirect(self):
        self.assertEqual(self.get(site_id=100000).status_code, 404)

    def test_edit(self):
        edited_hostname = "edited"
        response = self.post(
            {
                "hostname": edited_hostname,
            }
        )

        # Should redirect back to index
        self.assertRedirects(response, reverse("wagtailsites:index"))

        # Check that the site was edited
        self.assertEqual(
            Site.objects.get(id=self.localhost.id).hostname, edited_hostname
        )

    def test_changing_the_default_site_workflow(self):
        # First create a second, non-default, site
        second_site = Site.objects.create(
            hostname="not_yet_default",
            port=80,
            is_default_site=False,
            root_page=self.home_page,
        )

        # Make the original default no longer default
        response = self.post(
            {
                "default": False,
            },
            site_id=self.localhost.id,
        )

        # Should redirect back to index
        self.assertRedirects(response, reverse("wagtailsites:index"))
        # Check that the site is no longer default
        self.assertIs(Site.objects.get(id=self.localhost.id).is_default_site, False)

        # Now make the second site default
        response = self.post(
            {
                "default": True,
            },
            site_id=second_site.id,
        )

        # Should redirect back to index
        self.assertRedirects(response, reverse("wagtailsites:index"))
        # Check that the second site is now set as default
        self.assertIs(Site.objects.get(id=second_site.id).is_default_site, True)

    def test_making_a_second_site_the_default_not_allowed(self):
        second_site = Site.objects.create(
            hostname="also_default",
            port=80,
            is_default_site=False,
            root_page=self.home_page,
        )
        response = self.post(
            {
                "default": True,
            },
            site_id=second_site.id,
        )

        # Should return the form with errors
        self.assertEqual(response.status_code, 200)
        self.assertIs(bool(response.context["form"].errors), True)

        # Check that the site was not editd

        self.assertIs(Site.objects.get(id=second_site.id).is_default_site, False)

    def test_duplicate_hostnames_case_variant_not_allowed(self):
        second_site = Site.objects.create(
            hostname="something_different",
            port=80,
            is_default_site=False,
            root_page=self.home_page,
        )
        response = self.post(
            {
                "hostname": "Localhost",
            },
            site_id=second_site.id,
        )

        # Should return the form with errors
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context["form"].errors,
            {"__all__": ["Site with this Hostname and Port already exists."]},
        )

    def test_non_field_errors_are_displayed(self):
        second_site = Site.objects.create(
            hostname="something_different",
            port=80,
            is_default_site=False,
            root_page=self.home_page,
        )
        response = self.post(
            {
                "hostname": "Localhost",
            },
            site_id=second_site.id,
        )
        expected_html = """
            <li class="error">
                <svg class="class="icon icon-warning messages-icon"" aria-hidden="true">
                    <use href="#icon-warning"></use>
                </svg>
                The site could not be saved due to errors.
                <ul class="errorlist">
                <li>
                Site with this Hostname and Port already exists.
                </li>
                </ul>
            </li>
        """
        self.assertTagInHTML(expected_html, response.content.decode())


class TestSiteDeleteView(AdminTemplateTestUtils, WagtailTestUtils, TestCase):
    def setUp(self):
        self.login()
        self.home_page = Page.objects.get(id=2)
        self.localhost = Site.objects.all()[0]

    def get(self, params={}, site_id=None):
        return self.client.get(
            reverse("wagtailsites:delete", args=(site_id or self.localhost.id,)), params
        )

    def post(self, post_data={}, site_id=None):
        return self.client.post(
            reverse("wagtailsites:delete", args=(site_id or self.localhost.id,)),
            post_data,
        )

    def test_simple(self):
        response = self.get()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "wagtailadmin/generic/confirm_delete.html")
        self.assertBreadcrumbsNotRendered(response.content)

    def test_nonexistent_redirect(self):
        self.assertEqual(self.get(site_id=100000).status_code, 404)

    def test_posting_deletes_site(self):
        response = self.post()

        # Should redirect back to index
        self.assertRedirects(response, reverse("wagtailsites:index"))

        # Check that the site was edited
        with self.assertRaises(Site.DoesNotExist):
            Site.objects.get(id=self.localhost.id)


class TestLimitedPermissions(WagtailTestUtils, TestCase):
    def setUp(self):
        # Create a user
        user = self.create_user(username="test", password="password")
        user.user_permissions.add(
            Permission.objects.get(codename="access_admin"),
            Permission.objects.get(codename="add_site"),
            Permission.objects.get(codename="change_site"),
            Permission.objects.get(codename="delete_site"),
        )

        # Login
        self.login(username="test", password="password")

        self.home_page = Page.objects.get(id=2)
        self.localhost = Site.objects.all()[0]

    def test_get_index(self):
        response = self.client.get(reverse("wagtailsites:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "wagtailadmin/generic/index.html")

    def test_get_create_view(self):
        response = self.client.get(reverse("wagtailsites:add"))
        self.assertEqual(response.status_code, 200)

    def test_create(self):
        response = self.client.post(
            reverse("wagtailsites:add"),
            {
                "hostname": "testsite",
                "port": "80",
                "root_page": str(self.home_page.id),
            },
        )

        # Should redirect back to index
        self.assertRedirects(response, reverse("wagtailsites:index"))

        # Check that the site was created
        self.assertEqual(Site.objects.filter(hostname="testsite").count(), 1)

    def test_get_edit_view(self):
        edit_url = reverse("wagtailsites:edit", args=(self.localhost.id,))
        response = self.client.get(edit_url)
        self.assertEqual(response.status_code, 200)

    def test_edit(self):
        edit_url = reverse("wagtailsites:edit", args=(self.localhost.id,))
        edited_hostname = "edited"
        response = self.client.post(
            edit_url,
            {
                "hostname": edited_hostname,
                "port": 80,
                "root_page": self.home_page.id,
            },
        )

        # Should redirect back to index
        self.assertRedirects(response, reverse("wagtailsites:index"))

        # Check that the site was edited
        self.assertEqual(
            Site.objects.get(id=self.localhost.id).hostname, edited_hostname
        )

    def test_get_delete_view(self):
        delete_url = reverse("wagtailsites:delete", args=(self.localhost.id,))
        response = self.client.get(delete_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "wagtailadmin/generic/confirm_delete.html")

    def test_delete(self):
        delete_url = reverse("wagtailsites:delete", args=(self.localhost.id,))
        response = self.client.post(delete_url)

        # Should redirect back to index
        self.assertRedirects(response, reverse("wagtailsites:index"))

        # Check that the site was edited
        with self.assertRaises(Site.DoesNotExist):
            Site.objects.get(id=self.localhost.id)


class TestAdminPermissions(WagtailTestUtils, TestCase):
    def test_registered_permissions(self):
        site_ct = ContentType.objects.get_for_model(Site)
        qs = Permission.objects.none()
        for fn in hooks.get_hooks("register_permissions"):
            qs |= fn()
        registered_permissions = qs.filter(content_type=site_ct)
        self.assertEqual(
            set(registered_permissions.values_list("codename", flat=True)),
            {"add_site", "change_site", "delete_site"},
        )
