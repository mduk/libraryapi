#!/usr/bin/env python3

import responder

from library import LibraryService

api = responder.API()
library = LibraryService()

@api.route("/request")
@api.route("/request/{request_id}")
async def request(req, resp, *, request_id=None):
    if req.method == 'get' and request_id is None:
        models = library.list_reservations()
        resp.media = [ m.__dict__ for m in models ]
        return

    if req.method == 'get' and request_id is not None:
        resp.media = library.get_reservation_by_id(request_id).__dict__
        return

    if req.method == 'delete' and request_id is None:
        resp.status_code = 405
        resp.media = { "error": "Method Not Allowed" }
        return

    if req.method == 'delete' and request_id is not None:
        library.cancel_reservation(request_id)
        resp.status_code = 204
        return

    if req.method == 'post' and request_id is None:
        request_data = await req.media()
        try:
            resp.media = library.reserve_book(
                title=request_data[ 'title' ],
                email=request_data[ 'email' ],
            ).__dict__
        except KeyError as key:
            resp.media = { 'error': f"Missing required field: {key}"}
        return

    if req.method == 'post' and request_id is not None:
        resp.status_code = 400
        resp.media = { "error": "Bad Request" }
        return


if __name__ == '__main__':
    api.run()
