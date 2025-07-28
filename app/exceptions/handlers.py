from app.exceptions.event_exceptions import EventNotFound
from app.exceptions.inventory_exceptions import InventoryNotFound
from app.exceptions.offer_exceptions import OfferNotFound
from app.exceptions.representation_exceptions import RepresentationNotFound
from app.exceptions.user_exceptions import UserAlreadyExists
from app.exceptions.waiting_list_exceptions import TicketsStillAvailable, AlreadyInWaitingList, WaitingListNotFound, \
    RepresentationEventAndOfferEventDontMatch
from fastapi.responses import JSONResponse
from fastapi import Request


def register_exception_handlers(app):
    @app.exception_handler(InventoryNotFound)
    async def inventory_not_found_handler(request: Request, exc: InventoryNotFound):
        return JSONResponse(
            status_code=404,
            content={"detail": "Inventory not found."},
        )

    @app.exception_handler(EventNotFound)
    async def event_not_found_handler(request: Request, exc: EventNotFound):
        return JSONResponse(
            status_code=404,
            content={"detail": "Event not found."},
        )

    @app.exception_handler(OfferNotFound)
    async def offer_not_found_handler(request: Request, exc: OfferNotFound):
        return JSONResponse(
            status_code=404,
            content={"detail": "Offer not found."},
        )

    @app.exception_handler(RepresentationNotFound)
    async def representation_not_found_handler(request: Request, exc: RepresentationNotFound):
        return JSONResponse(
            status_code=404,
            content={"detail": "Representation not found."},
        )

    @app.exception_handler(WaitingListNotFound)
    async def waiting_list_not_found_handler(request: Request, exc: WaitingListNotFound):
        return JSONResponse(
            status_code=404,
            content={"detail": "WaitingList not found."},
        )

    @app.exception_handler(RepresentationEventAndOfferEventDontMatch)
    async def invalid_event_handler(request: Request, exc: RepresentationEventAndOfferEventDontMatch):
        return JSONResponse(
            status_code=400,
            content={"detail": "Provided representation_id and offer_id dont match the same event."},
        )

    @app.exception_handler(TicketsStillAvailable)
    async def tickets_still_available_handler(request: Request, exc: TicketsStillAvailable):
        return JSONResponse(
            status_code=400,
            content={"detail": "Tickets are still available — no need to join the waiting list."},
        )

    @app.exception_handler(AlreadyInWaitingList)
    async def already_in_waiting_list_handler(request: Request, exc: AlreadyInWaitingList):
        return JSONResponse(
            status_code=400,
            content={"detail": "User is already on the waiting list."},
        )

    @app.exception_handler(UserAlreadyExists)
    async def already_in_waiting_list_handler(request: Request, exc: UserAlreadyExists):
        return JSONResponse(
            status_code=400,
            content={"detail": "User's email already is use."},
        )