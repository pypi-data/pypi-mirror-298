import logging
import re
from typing import Optional, TypedDict

import xmltodict
from requests import Session

from parcelhub.client import RestClient


class ServiceResult(TypedDict):
    success: bool
    error_code: int
    error_message: str
    internal_error_message: str
    has_warning: bool
    warning_message: str


class Shipment(TypedDict):
    shipment_key: str
    account_id: str
    courier_name: str
    courier_tracking_number: str
    event_category_id: int
    event_category_description: str
    event_sub_category_id: int
    event_sub_category_description: str
    event_location: str
    event_description: str
    event_signatory: str
    event_timestamp: str
    longitude: float
    latitude: float
    coutier_tracking_event_code: str


class ShipmentTracking(TypedDict):
    event_timestamp: str
    longitude: float
    latitude: float


class TrackingEvent(TypedDict):
    event_category_id: int
    event_category_description: str
    event_sub_category_id: int
    event_sub_category_description: str
    event_location: str
    event_description: str
    event_signatory: str
    event_timestamp: str
    longitude: float
    latitude: float
    coutier_tracking_event_code: str


class ShipmentTrackingEvent(TrackingEvent):
    pass


class PackageTrackingEvent(TrackingEvent):
    pass


class SearchResult(TypedDict):
    shipment_key: str
    courier_name: str
    tracking_number: str
    has_shipment_tracking: bool
    shipment_tracking: ShipmentTracking
    package_tracking_event: PackageTrackingEvent
    successful: bool
    search_error_message: str


class Package(TypedDict):
    tracking_number: str
    package_tracking_events: list[TrackingEvent]


class ListShipmentsResponse(TypedDict):
    transaction_message_id: str
    service_result: ServiceResult
    from_date: str
    to_date: str
    shipments: list[Shipment]


class GetLatestTrackingEventResponse(TypedDict):
    transaction_message_id: str
    service_result: ServiceResult
    tracking_result: SearchResult


class GetTrackingHistoryResponse(TypedDict):
    transaction_message_id: str
    service_result: ServiceResult
    shipment_key: str
    courier_name: str
    tracking_number: str
    has_shipment_tracking: bool
    shipment_tracking_events: list[ShipmentTracking]
    packages: list[Package]


class ShipmentSearchResult(TypedDict):
    shipment_key: str
    account_id: str
    courier_name: str
    courier_tracking_number: str
    delivery_postcode: str
    reference1: str
    reference2: str
    deleted: bool
    event_category_id: int
    event_category_description: str
    event_sub_category_id: int
    event_sub_category_description: str
    event_location: str
    event_description: str
    event_signatory: str
    event_timestamp: str
    longitude: float
    latitude: float
    coutier_tracking_event_code: str


class SearchShipmentResponse(TypedDict):
    transaction_message_id: str
    service_result: ServiceResult
    shipments: list[ShipmentSearchResult]


class Parcelhub:
    """Dixa API Client"""

    def __init__(
        self,
        account_id: str,
        access_code: str,
        max_retries: int = 3,
        retry_delay: int = 2,
        session: Optional[Session] = None,
        logger: Optional[logging.Logger] = None,
        logger_level: int = logging.DEBUG,
    ):
        """Initializes the Parcelhub API client."""

        self._base_url = "https://trackapi.parcelhub.net/v1/trackingservice"
        self._client = RestClient(
            account_id,
            access_code,
            max_retries,
            retry_delay,
            session,
            logger,
            logger_level,
        )

    def pre_process(self, response: dict, key: str) -> dict:
        data = response.get(key, {})
        if isinstance(data, dict):
            return self.pre_process_inner(data)
        return {}

    def pre_process_inner(self, data: dict) -> dict:
        output = {}
        for k, v in data.items():
            if "@" in k:
                continue
            k = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", k).lower()
            output[k] = self.pre_process_inner(v) if isinstance(v, dict) else v
        return output

    def list_shipments(self, from_date: str, to_date: str) -> ListShipmentsResponse:
        body = {
            "ListShipmentsRequest": {
                "Authentication": {
                    "AccountID": self._client._account_id,
                    "AccessCode": self._client._access_code,
                },
                "TransactionMessageID": "test transaction message",
                "FromDate": from_date,
                "ToDate": to_date,
            }
        }

        data = self._client.post(
            f"{self._base_url}/listshipments", xmltodict.unparse(body)
        )
        data = self.pre_process(data, "ListShipmentsResponse")
        return ListShipmentsResponse(**data)

    def get_latest_tracking_event(
        self, tracking_numbers: list[str]
    ) -> GetLatestTrackingEventResponse:
        body = {
            "GetLatestTrackingEventRequest": {
                "Authentication": {
                    "AccountID": self._client._account_id,
                    "AccessCode": self._client._access_code,
                },
                "TransactionMessageID": "test transaction message",
                "TrackingNumbers": {"TrackingNumber": [tracking_numbers]},
            }
        }

        data = self._client.post(
            f"{self._base_url}/getlatesttrackingevent",
            xmltodict.unparse(body, expand_iter="TrackingNumber"),
        )
        data = self.pre_process(data, "GetLatestTrackingEventResponse")
        return GetLatestTrackingEventResponse(**data)

    def get_tracking_history(
        self, search_type: str, search_term: str
    ) -> GetTrackingHistoryResponse:
        body = {
            "GetTrackingHistoryRequest": {
                "Authentication": {
                    "AccountID": self._client._account_id,
                    "AccessCode": self._client._access_code,
                },
                "TransactionMessageID": "test transaction message",
                "SearchType": search_type,
                "SearchTerm": search_term,
            }
        }

        data = self._client.post(
            f"{self._base_url}/gettrackinghistory", xmltodict.unparse(body)
        )
        data = self.pre_process(data, "GetTrackingHistoryResponse")
        return GetTrackingHistoryResponse(**data)

    def search_shipments(self, search_term: str) -> SearchShipmentResponse:
        body = {
            "SearchShipmentsRequest": {
                "Authentication": {
                    "AccountID": self._client._account_id,
                    "AccessCode": self._client._access_code,
                },
                "TransactionMessageID": "test transaction message",
                "SearchTerm": search_term,
            }
        }

        data = self._client.post(
            f"{self._base_url}/searchshipments", xmltodict.unparse(body)
        )
        data = self.pre_process(data, "SearchShipmentsResponse")
        return SearchShipmentResponse(**data)


__all__ = ["Parcelhub"]
