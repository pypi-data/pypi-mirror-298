from time import sleep
from datetime import datetime
from requests import request as http_request
from requests.exceptions import ConnectionError

from appmetrica_logs_api.constants import APIResources
from appmetrica_logs_api.schemas.events import EventsSchema
from appmetrica_logs_api.schemas.installations import InstallationsSchema
from appmetrica_logs_api.schemas.profiles import ProfilesSchema
from appmetrica_logs_api.schemas.revenue_events import RevenueEventsSchema
from appmetrica_logs_api.schemas.deeplinks import DeeplinksSchema
from appmetrica_logs_api.schemas.clicks import ClicksSchema
from appmetrica_logs_api.schemas.postbacks import PostbacksSchema
from appmetrica_logs_api.schemas.sessions_starts import SessionsStartsSchema
from appmetrica_logs_api.schemas.errors import ErrorsSchema
from appmetrica_logs_api.schemas.crashes import CrashesSchema
from appmetrica_logs_api.schemas.push_tokens import PushTokensSchema

from appmetrica_logs_api.exceptions import AppmetricaClientError, AppmetricaApiError


RESOURCES_SCHEMA_MAPPING = {
    APIResources.EVENTS: EventsSchema,
    APIResources.INSTALLATIONS: InstallationsSchema,
    APIResources.PROFILES: ProfilesSchema,
    APIResources.REVENUE_EVENTS: RevenueEventsSchema,
    APIResources.DEEPLINKS: DeeplinksSchema,
    APIResources.CLICKS: ClicksSchema,
    APIResources.POSTBACKS: PostbacksSchema,
    APIResources.SESSIONS_STARTS: SessionsStartsSchema,
    APIResources.ERRORS: ErrorsSchema,
    APIResources.CRASHES: CrashesSchema,
    APIResources.PUSH_TOKENS: PushTokensSchema,
}


class AppMetrica:
    def __init__(self, app_token: str, **kwargs) -> None:
        self.__app_token = app_token
        self._api_endpoint = 'https://api.appmetrica.yandex.ru/logs/v1/export'
        self._request_latency = kwargs.get('request_latency', 10)  # Базовая задержка между запросами API

    def _make_request(self, url: str, params: dict, headers: dict, stream: bool):
        """
        Общая функция отправки запросов к API.
        :param url: Конечная точка запроса.
        :param params: Параметры запросы.
        :param headers: Заголовки запроса.
        :param stream: Если True, можно выполнять потоковую обработку результата запроса.
        :return:
        """
        # Параметры для регулирования скорости выполнения повторных запросов на скачивание файла.
        retry_count = 0

        headers.update({
            'Authorization': f'OAuth {self.__app_token}'
        })

        while True:
            try:
                response = http_request('GET', url=url, params=params, headers=headers, stream=stream)
                # Принудительная обработка ответа в кодировке UTF-8
                response.encoding = 'utf-8'

                if response.status_code == 200:
                    return response
                elif response.status_code in (201, 202):
                    # Увеличение задержки с каждой неудачной попыткой
                    retry_count += 1
                    latency_time = self._request_latency * 2 ** retry_count
                    sleep(latency_time)
                    if latency_time >= 1200:
                        # Сбрасываем счётчик, если время ожидания больше 20 минут
                        retry_count = 0
                else:
                    raise AppmetricaApiError(response.text)
            except ConnectionError:
                raise AppmetricaClientError(ConnectionError)

    def export(self, resource: str, application_id: str, fields: list[str] = None,
               date_from: datetime = None, date_to: datetime = None, **kwargs):
        """
        Экспорт данных из ресурса.
        :param resource: Название ресурса.
        :param application_id: Идентификатор приложения в AppMetrica.
        :param fields: Список полей для выборки. Если не задан, запрашиваются все доступные поля ресурса.
        :param date_from: Начало интервала дат в формате yyyy-mm-dd hh:mm:ss.
        :param date_to: Конец интервала дат в формате yyyy-mm-dd hh:mm:ss.
        :param kwargs: Другие параметры ресурса и заголовка Cache-Control в формате snake_case.
        Также доступен кастомный параметр export_format, который определяет формат данных (csv/json).
        Параметры запроса: stream, chunk_size, decode_unicode
        :return:
        """
        # Формат даты и времени, требуемый для параметров запроса.
        dt_format = '%Y-%m-%d %H:%M:%S'
        # Формат данных
        export_format = kwargs.pop('export_format', 'csv')
        # Параметры для потоковой обработки ответа
        stream = kwargs.pop('stream', False)
        chunk_size = kwargs.pop('chunk_size', 10 * 1024 * 1024)  # Размер одного чанка в байтах, по умолчанию 10MB
        decode_unicode = kwargs.pop('decode_unicode', False)

        api_url = '/'.join([self._api_endpoint, f'{resource}']) + f'.{export_format}'

        if resource in RESOURCES_SCHEMA_MAPPING.keys():
            fields = ','.join(list(RESOURCES_SCHEMA_MAPPING[resource].model_fields.keys())) if fields is None else ','.join(fields)
        else:
            raise AppmetricaClientError(f'Ресурс {resource} не доступен для экспорта.')

        headers = {
            # Отвечает за то, будет сформирован новый файл при повторном запросе или отдан сформированный ранее
            'Cache-Control': kwargs.pop('cache_control', 'no-cache'),
            'Accept-Encoding': 'gzip'  # Сжатие gzip
        }

        params = {
            'application_id': application_id,
            'fields': fields,
            **kwargs
        }

        # Для всех ресурсов, кроме profiles и push_tokens надо указать диапазон дат.
        if resource not in (APIResources.PROFILES, APIResources.PUSH_TOKENS):
            if all([date_from, date_to]):
                params.update({'date_since': date_from.strftime(dt_format), 'date_until': date_to.strftime(dt_format)})
            else:
                raise AppmetricaClientError(f'Для ресурса {resource} требуется указать диапазон дат - '
                                            f'параметры date_from и date_to')

        response = self._make_request(api_url, params, headers, stream)

        if stream is True:
            return response.iter_content(chunk_size=chunk_size, decode_unicode=decode_unicode)
        elif export_format == 'csv':
            return response.content
        else:
            return response.json()
