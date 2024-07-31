# Serializers define the API representation.
from rest_framework import serializers
from crawls.models import FilterRule, FilterSet, CrawlJob


class FilterRuleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = FilterRule
        fields = ['id', 'filter_set', 'rule', 'include', 'created_at', 'updated_at', 'page_type', 'count', 'cumulative_count', 'position']
        # order rules by position, ascending

    # serialize, but don't deserialize count
    count = serializers.ReadOnlyField()
    cumulative_count = serializers.ReadOnlyField()


    # if position is updated, call move_to on the FilterRule
    def update(self, instance, validated_data):
        if 'count' in validated_data:
            validated_data.pop('count')
        if 'position' in validated_data:
            instance.move_to(validated_data['position'])
            validated_data.pop('position')
        return super().update(instance, validated_data)


class InlineFilterRuleSerializer(serializers.HyperlinkedModelSerializer):
    """ Serializer for FilterRule, omits the urls of the rule and the set. """
    class Meta:
        model = FilterRule
        fields = ['id', 'rule', 'include', 'created_at', 'updated_at', 'page_type', 'count', 'cumulative_count', 'position']


# Add "url_count" to crawl_job
class CrawlJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrawlJob
        fields = '__all__'

    # order rules by position, ascending
    url_count = serializers.SerializerMethodField('get_url_count')

    def get_url_count(self, obj: CrawlJob):
        return obj.crawled_urls.count()

class FilterSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = FilterSet
        fields = ['id', 'crawl_job', 'remaining_urls', 'name', 'created_at', 'updated_at', 'url', 'rules']
        depth = 1

    # order rules by position, ascending
    rules = serializers.SerializerMethodField('get_rules')
    crawl_job = CrawlJobSerializer(read_only=True)
    # crawl_job = serializers.HyperlinkedRelatedField(view_name='crawl-job-detail', read_only=True)

    def get_rules(self, obj):
        rules = obj.rules.order_by('position')
        return InlineFilterRuleSerializer(rules, many=True, context=self.context).data
    