from django.db import models
from django.conf import settings
from translation.models import TranslatedLesson, TranslatedStep
from django.core.cache import cache

from.constants import RequestedObject

import requests


class SingletonModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super(SingletonModel, self).save(*args, **kwargs)
        self.set_cache()

    def set_cache(self):
        cache.set(self.__class__.__name__, self)

    @classmethod
    def load(cls):
        if cache.get(cls.__name__) is None:
            object, created = cls.objects.get_or_create(pk=1)
            if not created:
                object.set_cache()
        return cache.get(cls.__name__)


class ApiController(SingletonModel):
    oauth_credentials = {
        "client_id": settings.STEPIK_CLIENT_ID,
        "client_secret": settings.STEPIK_CLIENT_SECRET,
    }
    api_version = models.FloatField(default=0.1)
    api_host = models.CharField(max_length=255, default="https://stepik.org")
    token = None

    def stepik_oauth(self):

        auth = requests.auth.HTTPBasicAuth(self.oauth_credentials["client_id"], self.oauth_credentials["client_secret"])
        response = requests.post('https://stepik.org/oauth2/token/',
                                 data={'grant_type': 'client_credentials'},
                                 auth=auth)
        self.token = response.json().get('access_token', None)
        if not self.token:
            return False
        return True

    def fetch_stepik_object(self, obj_class, obj_id):
        api_url = '{}/api/{}s/{}'.format(self.api_host, obj_class, obj_id)
        response = requests.get(api_url,
                                headers={'Authorization': 'Bearer ' + self.token}).json()
        if '{}s'.format(obj_class) in response:
            return response['{}s'.format(obj_class)][0]
        return None

    def fetch_stepik_objects(self, obj_class, obj_ids, keep_order=True):
        objs = []
        load_size = 30  # don't wanna hit HTTP request limits
        for i in range(0, len(obj_ids), load_size):
            slice = obj_ids[i:i + load_size]
            api_url = '{}/api/{}s/?{}'.format(self.api_host, obj_class, "&".join("ids[]={}".format(x) for x in slice))
            response = requests.get(api_url,
                                    headers={'Authorization': 'Bearer ' + self.token}).json()
            objs += response['{}s'.format(obj_class)]
        if keep_order:
            return sorted(objs, key=lambda x: obj_ids.index(x['id']))
        return objs

    def fetch_stepik_step(self, pk):
        return self.fetch_stepik_object("step", pk)

    def fetch_stepik_lesson(self, pk):
        return self.fetch_stepik_object("lesson", pk)

    def steps_text(self, ids):
        texts = []
        steps = self.fetch_stepik_objects("step", ids)
        for step in steps:
            if step is None or 'text' not in step['block']:
                texts.append("")
            else:
                texts.append(step['block']['text'])
        return texts

    def create_translation(self, obj_type, pk, service_name=None, lang=None):
        translation_service = self.translation_services.filter(service_name=service_name.lower())
        if not translation_service:
            return None

        if obj_type is RequestedObject.STEP:
            translation = self.get_translation(obj_type, pk, service_name, lang)
            if translation is not None:
                return translation
            created = self.fetch_stepik_object(obj_type, pk)
            if created is None:
                return None
            ts = None
            translated_text = translation_service.create_step_translation(created['block']['text'], lang=lang)
            tl = TranslatedLesson.objects.create(stepik_id=created['lesson'], service_name=service_name)
            ts = TranslatedStep.objects.create(stepik_id=pk, lang=lang, service_name=service_name,
                                               text=translated_text, lesson=tl)

            return ts
        elif obj_type is RequestedObject.LESSON:
            translation = self.get_translation(obj_type, pk, service_name, lang)
            if translation is not None:
                return translation
            stepik_lesson = self.fetch_stepik_object(obj_type, pk)
            if stepik_lesson is None:
                return None
            new_lesson = TranslatedLesson.objects.create(stepik_id=pk, service_name="yandex")
            texts = self.steps_text(stepik_lesson['steps'])
            translation_service.create_lesson_translation(pk, stepik_lesson['steps'], texts, lang=lang)
            return new_lesson

    def get_translation(self, obj_type, pk, service_name=None, lang=None):
        result = None
        if service_name is None:
            if obj_type is RequestedObject.STEP:
                if lang is None:
                    result = TranslatedStep.objects.filter(stepik_id=pk)
                else:
                    result = TranslatedStep.objects.filter(stepik_id=pk, lang=lang)
            elif obj_type is RequestedObject.LESSON:
                if lang is None:
                    result = TranslatedLesson.objects.filter(stepik_id=pk)
                else:
                    result = TranslatedLesson.objects.filter(stepik_id=pk, lang=lang)
        else:
            translation_service = self.translation_services.filter(service_name=service_name.lower()).first()
            if not translation_service:
                return None

            if obj_type == RequestedObject.LESSON:
                result = translation_service.get_lesson_translated_steps(pk, lang)
            elif obj_type == RequestedObject.STEP:
                result = translation_service.get_step_translation(pk, lang)
        if result is None or result.exists() == 0:
            return None
        return result

    def get_available_languages(self, obj_type, service_name, pk):
        translation_service = self.translation_services.filter(service_name=service_name.lower())
        if not translation_service:
            return None

        if obj_type is RequestedObject.SERVICE:
            result = translation_service.get_available_languages()
        elif obj_type is RequestedObject.STEP:
            result = translation_service.filter(pk=pk)
        elif obj_type is RequestedObject.LESSON:
            result = self.translation_services.filter(pk=pk)
        # TODO add obj_type "course"
        # TODO make json serializer
        return
        # def get_translation_ratio(self, obj_type, pk):
        #    self.translation_service.get_translation_ratio(obj_type, )
        # TODO add get_service for every method

    def get_translational_ratio(self, pk, obj_type, lang=None, service_name=None):
        translation_service = self.translation_services.filter(service_name=service_name.lower())
        if not translation_service:
            return None
        return translation_service.get_translation_ratio(pk, obj_type, lang)