from __future__ import annotations
from django.contrib import admin
from django.http import HttpRequest
from django.utils.safestring import mark_safe

from .models import CrawlJob, CrawledURL

# Register your models here.

# class CrawledURLInline(admin.TabularInline):
#     model = CrawledURL
#     extra = 0
#     fields = ['content', 'created_at', 'updated_at']
    
#     readonly_fields = ['url', 'content', 'created_at', 'updated_at']
#     can_delete = False


class CrawlJobAdmin(admin.ModelAdmin):
    list_display = ['start_url', 'follow_links', 'created_at', 'updated_at']
    fields = ['start_url', 'follow_links', 'created_at', 'updated_at', 'crawled_urls']
    #readonly_fields = ['start_url', 'follow_links', 'created_at', 'updated_at']
    # inlines = [
    #     CrawledURLInline,
    # ]
    date_hierarchy = 'created_at'

    # admin list title

    

    # link to the admin page for the related crawled urls
    @mark_safe
    def crawled_urls(self, obj: CrawlJob) -> str:
        try:
            count = obj.crawled_urls.count()
            if count == 0:
                return 'No crawled URLs'
            return f'<a href="/admin/crawls/crawledurl/?crawl_job__id__exact={obj.id}">{count} Crawled URLs</a>'
        except Exception as e:
            print("Error in crawled_urls", e)
            return 'Error'

    # make this model read only
    def has_change_permission(self, request: HttpRequest, obj: CrawlJob=None) -> bool:
        return False
        #return super().has_change_permission(request, obj)

class CrawlJobFilter(admin.SimpleListFilter):
    title = 'Crawl Job'
    parameter_name = 'crawl_job__id__exact'
    
    def lookups(self, request: HttpRequest, model_admin: admin.ModelAdmin) -> list:
        job_id = self.value()

        if job_id:
            job = CrawlJob.objects.get(id=job_id)
            description = f"Job {job_id}: {job.start_url} at {job.created_at}"
            return [
                (job_id, description),
            ]
        # return [
        #     (job.id, job.start_url) for job in crawl_jobs
        # ]
        # if job_id:
        #     return [(job.id, job.start_url) for job in crawl_jobs if job.id == int(job_id)]
        # return [(job.id, job.start_url) for job in crawl_jobs]

    def queryset(self, request: HttpRequest, queryset):
        if self.value():
            return queryset.filter(crawl_job__id=self.value())
        return queryset
    # def __init__(self, field, request, params, model, model_admin, field_path):
    #     self.lookup_kwarg = "%s__in" % field_path
    #     super().__init__(field, request, params, model, model_admin, field_path)

    # def expected_parameters(self):
    #     return [self.lookup_kwarg]
    
    # def choices(self, changelist):
    #     return []

class CrawledURLAdmin(admin.ModelAdmin):
    model = CrawledURL
    list_display = ['url', 'crawl_job', 'created_at', 'updated_at']
    # fields = ['url', 'crawl_job', 'content', 'created_at', 'updated_at']
    # readonly_fields = ['url', 'crawl_job', 'content', 'created_at', 'updated_at']
    # date_hierarchy = 'created_at'

    # allow to filter by crawl job
    # list_filter = [(CrawlJobFilter)]
    list_filter = ['crawl_job']



admin.site.register(CrawlJob, CrawlJobAdmin)
admin.site.register(CrawledURL, CrawledURLAdmin)
