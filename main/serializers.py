from django.utils.html import strip_tags
from rest_framework import serializers

from main.models import Projects


class ProjectSerializer(serializers.ModelSerializer):
    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()
    starred_by_names = serializers.SerializerMethodField()

    class Meta:
        model = Projects
        fields = [
            "id", "project_name", "project_desc", "tech_stack", "uploaded_date", "thumbnail",
            "project_link",
            "star_count", "is_starred", "starred_by_names",
        ]
        read_only_fields = ["id", "uploaded_date"]

    def validate_project_name(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError("Project name cannot be empty.")
        return value

    def validate_project_desc(self, value):
        return strip_tags(value)

    def validate_tech_stack(self, value):
        return strip_tags(value)

    def validate_project_link(self, value):
        if value and not value.lower().startswith(("http://", "https://")):
            raise serializers.ValidationError("Link must start with http:// or https://.")
        return value

    def get_star_count(self, obj):
        return obj.starred_by.count()

    def get_is_starred(self, obj):
        request = self.context.get("request")
        if request is None or not request.user.is_authenticated:
            return False
        return request.user in obj.starred_by.all()

    def get_starred_by_names(self, obj):
        return ", ".join(user.username for user in obj.starred_by.all())