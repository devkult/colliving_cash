import orjson


def convert_event_to_broker_message(event: NodeEvent) -> bytes: 
    return orjson.dumps(event)

def convert_event_to_json(event: BaseEvent)
    ...