from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class InstallationsSchema(BaseModel):
    """
    Установки приложения.
    https://appmetrica.yandex.ru/docs/mobile-api/logs/endpoints.html#installations
    """
    application_id: Optional[int] = Field(
        description='Уникальный числовой идентификатор приложения в AppMetrica.'
    )
    installation_id: Optional[str] = Field(
        description='Идентификатор установки.'
    )
    attributed_touch_type: Optional[str] = Field(
        description='Тип рекламного взаимодействия: click | impression | unknown.'
    )
    click_datetime: Optional[datetime] = Field(
        description='Дата и время клика/показа в формате yyyy-mm-dd hh:mm:ss.'
    )
    click_id: Optional[str] = Field(
        description='Идентификатор клика/показа или '' (пустая строка, если недоступен).'
    )
    click_ipv6: Optional[str] = Field(
        description='IP-адрес в момент клика/показа в формате IPv6.'
    )
    click_timestamp: Optional[int] = Field(
        description='Время клика/показа в формате UNIX-time в секундах.'
    )
    click_url_parameters: Optional[str] = Field(
        description='Параметры, как они представлены в ссылке.'
    )
    click_user_agent: Optional[str] = Field(
        description='User-agent клика/показа.'
    )
    profile_id: Optional[str] = Field(
        description='Идентификатор пользовательского профиля.'
    )
    publisher_id: Optional[int] = Field(
        description='ID партнера в AppMetrica.'
    )
    publisher_name: Optional[str] = Field(
        description='Название партнера AppMetrica.'
    )
    tracker_name: Optional[str] = Field(
        description='Название трекера, который добавляется в интерфейсе AppMetrica.'
    )
    tracking_id: Optional[int] = Field(
        description='ID трекера в AppMetrica. '
    )
    install_datetime: Optional[datetime] = Field(
        description='Дата и время установки в формате yyyy-mm-dd hh:mm:ss.'
    )
    install_ipv6: Optional[str] = Field(
        description='IP-адрес в момент установки в формате IPv6.'
    )
    install_receive_datetime: Optional[datetime] = Field(
        description='Дата и время получения сервером события об установке.'
    )
    install_receive_timestamp: Optional[int] = Field(
        description='Время получения сервером события об установке в формате UNIX-time.'
    )
    install_timestamp: Optional[int] = Field(
        description='Время установки в формате UNIX-time в секундах.'
    )
    is_reattribution: Optional[bool] = Field(
        description='Признак реатрибутирования установки новому источнику. Возможные значения: true | false.'
    )
    is_reinstallation: Optional[bool] = Field(
        description='Признак переустановки приложения. Возможные значения: true | false.'
    )
    match_type: Optional[str] = Field(
        description='Способ атрибуции: fingerprint | referrer | identifier | '' (пустая строка).'
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
    device_locale: Optional[str] = Field(
        description='Язык интерфейса устройства.'
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
    oaid: Optional[str] = Field(
        description='Huawei OAID устройства в формате, в котором получен от устройства.'
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
    app_package_name: Optional[str] = Field(
        description='Имя пакета для Android или Bundle ID для iOS.'
    )
    app_version_name: Optional[str] = Field(
        description='Версия приложения в виде, как указана разработчиком.'
    )
