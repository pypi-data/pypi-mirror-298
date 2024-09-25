from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class EventsSchema(BaseModel):
    """
    События приложения.
    https://appmetrica.yandex.ru/docs/mobile-api/logs/endpoints.html#events
    """
    event_datetime: Optional[datetime] = Field(
        description='Дата и время события в формате yyyy-mm-dd hh:mm:ss.'
    )
    event_json: Optional[str] = Field(
        description='Атрибуты события, сериализованные в JSON.'
    )
    event_name: Optional[str] = Field(
        description='Имя события (как передано в SDK).'
    )
    event_receive_datetime: Optional[datetime] = Field(
        description='Дата и время получения сервером события.'
    )
    event_timestamp: Optional[int] = Field(
        description='Время события в формате UNIX-time.'
    )
    session_id: Optional[int] = Field(
        description='Идентификатор сессии.'
    )
    installation_id: Optional[str] = Field(
        description='Идентификатор установки.'
    )
    appmetrica_device_id: Optional[str] = Field(
        description='Уникальный идентификатор устройства, который устанавливает AppMetrica.'
    )
    profile_id: Optional[str] = Field(
        description='Идентификатор пользовательского профиля.'
    )
    city: Optional[str] = Field(
        description='Название города на английском языке, где был произведен клик.'
    )
    country_iso_code: Optional[str] = Field(
        description='ISO-код страны.'
    )
    connection_type: Optional[str] = Field(
        description='Тип подключения устройства. Возможные значения: wifi | cell | unknown.'
    )
    device_ipv6: Optional[str] = Field(
        description='IP-адрес в момент совершения события в формате IPv6.'
    )
    device_locale: Optional[str] = Field(
        description='Язык интерфейса устройства.'
    )
    device_manufacturer: Optional[str] = Field(
        description='Производитель устройства.'
    )
    device_model: Optional[str] = Field(
        description='Модель устройства.'
    )
    original_device_model: Optional[str] = Field(
        description='Заводская модель устройства.'
    )
    device_type: Optional[str] = Field(
        description='Тип устройства. Возможные значения: phone | tablet | unknown.'
    )
    google_aid: Optional[str] = Field(
        description='Google AID устройства в формате, в котором получен от устройства.'
    )
    windows_aid: Optional[str] = Field(
        description='Windows AID устройства в формате, в котором получен от устройства.'
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
    app_build_number: Optional[int] = Field(
        description='Номер сборки приложения.'
    )
    app_package_name: Optional[str] = Field(
        description='Имя пакета для Android или Bundle ID для iOS.'
    )
    app_version_name: Optional[str] = Field(
        description='Версия приложения в виде, как указана разработчиком.'
    )
    application_id: Optional[int] = Field(
        description='Уникальный числовой идентификатор приложения в AppMetrica.'
    )
