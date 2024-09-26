from django.urls import path
from oscar.apps.dashboard.reports import apps
from oscar.core.loading import get_class


class ReportsDashboardConfig(apps.ReportsDashboardConfig):
    name = "oscarreports"

    def ready(self):
        super().ready()
        from . import handlers  # NOQA

        self.index_view = get_class("reports_dashboard.views", "IndexView")
        self.download_view = get_class("reports_dashboard.views", "ReportDownloadView")
        self.delete_view = get_class("reports_dashboard.views", "ReportDeleteView")

    def get_urls(self):
        urls = [
            path("", self.index_view.as_view(), name="reports-index"),
            path(
                "<uuid:uuid>/download/",
                self.download_view.as_view(),
                name="reports-download",
            ),
            path(
                "<uuid:uuid>/delete/",
                self.delete_view.as_view(),
                name="reports-delete",
            ),
        ]
        return self.post_process_urls(urls)
