from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define, field as _attrs_field

from ..models.heartbeat_type import HeartbeatType

T = TypeVar("T", bound="UpdateHeartbeatStateInput")


@_attrs_define
class UpdateHeartbeatStateInput:
    """
    Attributes:
        type (HeartbeatType):
        cron_expression (Union[None, str]):
        cron_timezone (Union[None, str]):
        interval_seconds (Union[None, int]):
        timeout_seconds (int):
        muted (bool):
        resolve_incident (bool):
    """

    type: HeartbeatType
    cron_expression: Union[None, str]
    cron_timezone: Union[None, str]
    interval_seconds: Union[None, int]
    timeout_seconds: int
    muted: bool
    resolve_incident: bool
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type.value

        cron_expression: Union[None, str]
        cron_expression = self.cron_expression

        cron_timezone: Union[None, str]
        cron_timezone = self.cron_timezone

        interval_seconds: Union[None, int]
        interval_seconds = self.interval_seconds

        timeout_seconds = self.timeout_seconds

        muted = self.muted

        resolve_incident = self.resolve_incident

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
                "cron_expression": cron_expression,
                "cron_timezone": cron_timezone,
                "interval_seconds": interval_seconds,
                "timeout_seconds": timeout_seconds,
                "muted": muted,
                "resolve_incident": resolve_incident,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        type = HeartbeatType(d.pop("type"))

        def _parse_cron_expression(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        cron_expression = _parse_cron_expression(d.pop("cron_expression"))

        def _parse_cron_timezone(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        cron_timezone = _parse_cron_timezone(d.pop("cron_timezone"))

        def _parse_interval_seconds(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        interval_seconds = _parse_interval_seconds(d.pop("interval_seconds"))

        timeout_seconds = d.pop("timeout_seconds")

        muted = d.pop("muted")

        resolve_incident = d.pop("resolve_incident")

        update_heartbeat_state_input = cls(
            type=type,
            cron_expression=cron_expression,
            cron_timezone=cron_timezone,
            interval_seconds=interval_seconds,
            timeout_seconds=timeout_seconds,
            muted=muted,
            resolve_incident=resolve_incident,
        )

        update_heartbeat_state_input.additional_properties = d
        return update_heartbeat_state_input

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
