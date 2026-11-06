"""N-central (RMM) mimic under /ncentral/."""

from __future__ import annotations

from fastapi import APIRouter, Depends, Query

from .common import ApiError, NcPage, nc_list, nc_page, require_auth
from .store import store

router = APIRouter(prefix="/ncentral", tags=["N-central"], dependencies=[Depends(require_auth)])


def S():
    return store.d


def _one(items: list[dict], key: str, value: int, what: str) -> dict:
    for it in items:
        if it[key] == value:
            return it
    raise ApiError(404, f"{what} {value} not found")


def _customer(customer_id: int) -> dict:
    return _one(S().nc_customers, "customerId", customer_id, "Customer")


def _device_list(items: list[dict], pg: NcPage):
    return nc_list(items, pg)


@router.get("/customers", summary="List customers",
            responses={200: {"content": {"application/json": {"example": {"data": [{
                "customerId": 5001, "customerName": "Tidewater Ledger CPAs", "externalId": "1001", "deviceCount": 18}],
                "pageNumber": 1, "pageSize": 50, "totalItems": 25, "totalPages": 1}}}}})
def list_customers(pg: NcPage = Depends(nc_page)):
    """Customers (clients) known to the RMM. `externalId` usually holds the Accelo company id, but not always."""
    return nc_list(S().nc_customers, pg)


@router.get("/customers/{customer_id}", summary="Get one customer")
def get_customer(customer_id: int):
    return {"data": _customer(customer_id)}


@router.get("/customers/{customer_id}/devices", summary="List devices for a customer")
def customer_devices(customer_id: int, pg: NcPage = Depends(nc_page), device_class: str | None = None,
                     online: bool | None = None):
    _customer(customer_id)
    items = [d for d in S().nc_devices if d["customerId"] == customer_id]
    items = _filter_devices(items, device_class, online, None, None, None)
    return nc_list(items, pg)


@router.get("/customers/{customer_id}/sites", summary="List sites for a customer")
def customer_sites(customer_id: int, pg: NcPage = Depends(nc_page)):
    _customer(customer_id)
    return nc_list([s for s in S().nc_sites if s["customerId"] == customer_id], pg)


@router.get("/sites", summary="List all sites")
def list_sites(pg: NcPage = Depends(nc_page), customer_id: int | None = None):
    items = S().nc_sites
    if customer_id is not None:
        items = [s for s in items if s["customerId"] == customer_id]
    return nc_list(items, pg)


def _filter_devices(items, device_class, online, os_contains, warranty_expired, q):
    if device_class:
        items = [d for d in items if d["deviceClass"] == device_class]
    if online is not None:
        items = [d for d in items if d["online"] == online]
    if os_contains:
        items = [d for d in items if os_contains.lower() in (d["os"] or "").lower()]
    if warranty_expired is not None:
        items = [d for d in items if d["warrantyExpired"] == warranty_expired]
    if q:
        ql = q.lower()
        items = [d for d in items if ql in d["hostname"].lower() or ql in (d["serialNumber"] or "").lower()]
    return items


@router.get("/devices", summary="List devices")
def list_devices(
    pg: NcPage = Depends(nc_page),
    customer_id: int | None = Query(None, description="N-central customerId (5001 to 5025)"),
    device_class: str | None = Query(None, description="workstation, laptop, server, firewall, switch, printer"),
    online: bool | None = Query(None, description="true: online, false: offline"),
    os: str | None = Query(None, description="Case insensitive substring of the OS name, e.g. 'Windows 10'"),
    warranty_expired: bool | None = None,
    q: str | None = Query(None, description="Search hostname or serial number"),
):
    """Monitored devices across all customers. Each device has `assignedContactId`, an Accelo contact id."""
    items = S().nc_devices
    if customer_id is not None:
        items = [d for d in items if d["customerId"] == customer_id]
    return nc_list(_filter_devices(items, device_class, online, os, warranty_expired, q), pg)


@router.get("/devices/{device_id}", summary="Get one device")
def get_device(device_id: int):
    return {"data": _one(S().nc_devices, "deviceId", device_id, "Device")}


@router.get("/devices/{device_id}/patch-status", summary="Patch status for a device")
def device_patch_status(device_id: int):
    """Missing patch counts, last scan, and reboot flag. Network gear and printers return `patchManaged: false`."""
    _one(S().nc_devices, "deviceId", device_id, "Device")
    return {"data": S().nc_patch[device_id]}


@router.get("/patch-status", summary="Patch status for many devices")
def list_patch_status(pg: NcPage = Depends(nc_page), customer_id: int | None = None,
                      status: str | None = Query(None, description="compliant, attention, critical, not-applicable"),
                      reboot_pending: bool | None = None):
    """Convenience endpoint (not in the real product) so dashboards do not need one call per device."""
    items = list(S().nc_patch.values())
    if customer_id is not None:
        items = [p for p in items if p["customerId"] == customer_id]
    if status:
        items = [p for p in items if p["status"] == status]
    if reboot_pending is not None:
        items = [p for p in items if p["rebootPending"] == reboot_pending]
    return nc_list(items, pg)


@router.get("/alerts", summary="List alerts (active and cleared)")
def list_alerts(
    pg: NcPage = Depends(nc_page),
    customer_id: int | None = None,
    device_id: int | None = None,
    active: bool | None = Query(None, description="true: only active alerts, false: only cleared"),
    severity: str | None = Query(None, description="critical, warning, info"),
    service_name: str | None = None,
):
    """Alerts, newest first. History covers about 12 months."""
    items = S().nc_alerts
    if customer_id is not None:
        items = [a for a in items if a["customerId"] == customer_id]
    if device_id is not None:
        items = [a for a in items if a["deviceId"] == device_id]
    if active is not None:
        items = [a for a in items if a["active"] == active]
    if severity:
        items = [a for a in items if a["severity"] == severity]
    if service_name:
        items = [a for a in items if service_name.lower() in a["serviceName"].lower()]
    items = sorted(items, key=lambda a: (a["triggeredAt"], a["alertId"]), reverse=True)
    return nc_list(items, pg)
