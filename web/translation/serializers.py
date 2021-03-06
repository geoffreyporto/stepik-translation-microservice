from enumfields.drf.serializers import EnumSupportSerializerMixin
from rest_framework import serializers

from translation.models import TranslatedLesson, TranslatedCourse, TranslatedStep, TranslatedStepSource


class FilteredListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        if self.context is not None and "lang" in self.context and self.context["lang"] is not None:
            data = data.filter(lang=self.context["lang"])
        data = data.order_by("position")
        return super(FilteredListSerializer, self).to_representation(data)


class TranslatedStepSerializer(serializers.ModelSerializer):
    class Meta:
        list_serializer_class = FilteredListSerializer
        model = TranslatedStep
        fields = (
            "pk", "stepik_id", "create_date", "update_date", "stepik_update_date", "lang", "text", "service_name",
            "position")


class TranslatedLessonSerializer(serializers.ModelSerializer):
    steps = TranslatedStepSerializer(many=True)

    class Meta:
        model = TranslatedLesson
        fields = (
            "pk", "stepik_id", "create_date", "update_date", "stepik_update_date", "service_name", "steps_count",
            "steps")


class TranslatedCourseSerializer(serializers.ModelSerializer):
    lessons = TranslatedLesson

    class Meta:
        model = TranslatedCourse
        fields = (
            "pk", "stepik_id", "create_date", "update_date", "stepik_update_date", "service_name", "steps_count")


class TranslatedStepSourceSerializer(EnumSupportSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = TranslatedStepSource
        fields = (
            "pk", "stepik_id", "create_date", "update_date", "stepik_update_date", "service_name", "lang", "type",
            "source")
