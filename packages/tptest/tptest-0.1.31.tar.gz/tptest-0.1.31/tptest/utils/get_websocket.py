import asyncclick as click


def get_websocket():
    # Get the current context object
    ctx = click.get_current_context()

    # Check if a WebSocket connection is active
    if ctx.obj and hasattr(ctx.obj, 'websocket'):
        websocket = ctx.obj.websocket
    else:
        # If no WebSocket connection is active, create a new one
        websocket = None
    return websocket
