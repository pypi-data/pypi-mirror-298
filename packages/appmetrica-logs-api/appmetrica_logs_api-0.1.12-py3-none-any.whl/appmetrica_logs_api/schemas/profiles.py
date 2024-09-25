from datetime import date
from typing import Optional

from pydantic import BaseModel, Field


class ProfilesSchema(BaseModel):
    """
    Профили.
    https://appmetrica.yandex.ru/docs/mobile-api/logs/endpoints.html#profiles
    """
    profile_id: Optional[str] = Field(
        description='Идентификатор пользовательского профиля.'
    )
    appmetrica_gender: Optional[str] = Field(
        description='Пол.'
    )
    appmetrica_birth_date: Optional[str] = Field(
        description='Возраст.'
    )
    appmetrica_notifications_enabled: Optional[bool] = Field(
        description='Push разрешены.'
    )
    appmetrica_name: Optional[str] = Field(
        description='Имя.'
    )
    appmetrica_crashes: Optional[int] = Field(
        description='Количество крэшей.'
    )
    appmetrica_errors: Optional[int] = Field(
        description='Количество ошибок.'
    )
    appmetrica_first_session_date: Optional[date] = Field(
        description='Дата начала первой сессии.'
    )
    appmetrica_last_start_date: Optional[date] = Field(
        description='Дата последнего запуска приложения.'
    )
    appmetrica_push_opens: Optional[int] = Field(
        description='Количество открытых push-уведомлений.'
    )
    appmetrica_sdk_version: Optional[int] = Field(
        description='Версия AppMetrica SDK.'
    )
    appmetrica_sessions: Optional[int] = Field(
        description='Количество сессий.'
    )
    android_id: Optional[str] = Field(
        description='Идентификатор Android.'
    )
    appmetrica_device_id: Optional[str] = Field(
        description='Уникальный идентификатор устройства, который устанавливает AppMetrica.'
    )
    city: Optional[str] = Field(
        description='Название города на английском языке, где был произведен клик.'
    )
    connection_type: Optional[str] = Field(
        description='Тип подключения устройства. Возможные значения: wifi | cell | unknown.'
    )
    country_iso_code: Optional[str] = Field(
        description='ISO-код страны.'
    )
    device_manufacturer: Optional[str] = Field(
        description='Производитель устройства, определяется сервисом AppMetrica.'
    )
    device_model: Optional[str] = Field(
        description='Модель устройства, определяется сервисом AppMetrica.'
    )
    device_type: Optional[str] = Field(
        description='Тип устройства, определяется сервисом AppMetrica. Возможные значения: phone | tablet | unknown.'
    )
    google_aid: Optional[str] = Field(
        description='Google AID устройства в формате, в котором получен от устройства.'
    )
    ios_ifa: Optional[str] = Field(
        description='IFA устройства в формате, в котором получен от устройства.'
    )
    ios_ifv: Optional[str] = Field(
        description='IFV для приложения в формате, в котором получен от устройства.'
    )
    mcc: Optional[int] = Field(
        description='Мобильный код страны.'
    )
    mnc: Optional[int] = Field(
        description='Код мобильной сети.'
    )
    operator_name: Optional[str] = Field(
        description='Имя оператора сотовой связи.'
    )
    os_name: Optional[str] = Field(
        description='Операционная система на устройстве пользователя: ios | android | windows.'
    )
    os_version: Optional[str] = Field(
        description='Версия операционной системы на устройстве пользователя.'
    )
    windows_aid: Optional[str] = Field(
        description='Windows AID устройства в формате, в котором получен от устройства.'
    )
    app_build_number: Optional[int] = Field(
        description='Номер сборки приложения.'
    )
    app_framework: Optional[int] = Field(
        description='Тип фреймворка.'
    )
    app_package_name: Optional[str] = Field(
        description='Имя пакета для Android или Bundle ID для iOS.'
    )
    app_version_name: Optional[str] = Field(
        description='Версия приложения в виде, как указана разработчиком.'
    )
