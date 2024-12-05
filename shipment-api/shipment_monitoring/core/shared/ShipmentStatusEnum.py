import enum
class ShipmentStatus(str, enum.Enum):
    READY_FOR_PICKUP = "ready_for_pickup"
    OUT_FOR_DELIVERY = "out_for_delivery"
    DELIVERED = "delivered"
    FAILED_ATTEMPT ="failed_attempt"
    RETURNED_TO_SENDER="returned_to_sender"
    LOST="lost"
    DAMAGED="damaged"