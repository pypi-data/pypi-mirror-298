from typing import Callable, Optional, TypedDict, Union, List, Literal, Tuple
from pydantic import BaseModel
from datetime import datetime


class ButtonPayload(BaseModel):
    """
    Represents the payload data related to the button.

    Attributes:
        title (str): The title of the button.
        payload (str): The payload associated with the button.
        execute (str): The execute command associated with the action.
        sent (str): The timestamp when the message was sent. Format (yyyy-mm-ddThh:mm:ss) in GMT 0
        fromNum (str): The sender's phone number.
    """

    title: Optional[str] = None
    payload: Optional[str] = None
    execute: Optional[str] = None
    sent: str
    fromNum: str


# Types related to crafting a message
MediaType = Union[
    Literal["text"],
    Literal["image"],
    Literal["audio"],
    Literal["video"],
    Literal["file"],
]
"""
MediaType represents the type of media that can be sent in a message.

Attributes:
    text: Represents a text message.
    image: Represents an image message.
    audio: Represents an audio message.
    video: Represents a video message.
    file: Represents a file message.
"""


class MessagePayload(BaseModel):
    """
    Represents the payload data related to the message.

    Attributes:
        text (str): The text of the message.
        mediaType (MediaType): The type of media being sent.
        media (str): The URL of the media being sent.
        sent (str): The timestamp when the message was sent. Format (yyyy-mm-ddThh:mm:ss) in GMT 0
        fromNum (str): The sender's phone number.
    """

    text: Optional[str] = None
    mediaType: Optional[MediaType] = None
    media: Optional[str] = None
    sent: str
    fromNum: str


class PayloadData(BaseModel):
    """
    Represents the payload data received from a message.

    Attributes:
        messageType (str): The type of the message (e.g., "message", "postback").
        buttonPayload (Optional[ButtonPayload]): The payload data related to the button, if applicable.
        messagePayload (Optional[MessagePayload]): The payload data related to the message, if applicable.
    """

    messageType: str
    buttonPayload: Optional[ButtonPayload] = None
    messagePayload: Optional[MessagePayload] = None


OnMessageCallback = Callable[[PayloadData], None]

ActionType = Union[
    Literal["weburl"],
    Literal["call"],
    Literal["postback"],
    Literal["share_location"],
    Literal["view_location"],
    Literal["calendar"],
]
"""
ActionType represents the type of action that can be performed.

Attributes:
    weburl: Represents an action that opens a web URL.
    call: Represents an action that initiates a phone call.
    postback: Represents an action that sends data back to the server.
    share_location: Represents an action that requests the user's location.
    view_location: Represents an action that displays a location.
    calendar: Represents an action that creates a calendar event.
"""


class LatLng(TypedDict):
    """
    Latitude and Longitude coordinates.

    Attributes:
        lat (float): Latitude.
        lng (float): Longitude.
    """

    lat: float
    lng: float


class Action:
    """
    Represents an action that can be performed in response to a user interaction.

    Attributes:
        title (str): The title of the action (e.g., text for button or quick reply).
        action_type (ActionType): The type of action to be performed.
        payload (Optional[str]): The payload to be sent with the action.
        execute (Optional[str]): Metadata sent when the button/quick reply is clicked.
        query (Optional[str]): The query for location search.
        lat_lng (Optional[LatLng]): The latitude and longitude of a location.
        label (Optional[str]): The label for the location.
        start_time (Optional[str]): The start time of a calendar event.
        end_time (Optional[str]): The end time of a calendar event.
        event_title (Optional[str]): The title of the calendar event.
        event_description (Optional[str]): The description of the calendar event.
    """

    title: str
    action_type: Optional[ActionType] = None

    # weburl, call, postback
    payload: Optional[str] = None

    # postback
    execute: Optional[str] = None

    # view_location
    query: Optional[str] = None
    lat_lng: Optional[LatLng] = None
    label: Optional[str] = None

    # calendar
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    event_title: Optional[str] = None
    event_description: Optional[str] = None

    def __init__(
        self,
        title: str,
    ):
        """
        Initialize an Action object.
        :param title: The title of the action (e.g., text for button or quick reply). The max length is 25 characters.
        :raises ValueError: If the title exceeds 25 characters.
        """

        if len(title) > 25:
            raise ValueError("Title cannot exceed 25 characters.")

        self.title = title[:25]

    def weburl(self, url: str):
        """
        Set the action type to weburl and assign the URL to open.
        :param url: The URL to open when the action is triggered.
        :raises ValueError: If the URL is invalid.
        :return: self
        """
        if not url.startswith("http://") and not url.startswith("https://"):
            raise ValueError(
                "Invalid URL format. It should start with 'http://' or 'https://'."
            )
        self.action_type = "weburl"
        self.payload = url

        return self

    def call(self, phone_number: str):
        """
        Set the action type to call and assign the phone number to call.
        :param phone_number: The phone number to call (should be in the E.164 format +[country code][number]).
        :raises ValueError: If the phone number is invalid.
        :return: self
        """
        if (
            not phone_number.startswith("+")
            or not phone_number[1:].isdigit()
            or len(phone_number) < 10
        ):
            raise ValueError(
                "Invalid phone number format. It should start with '+' followed by country code and phone number."
            )
        self.action_type = "call"
        self.payload = phone_number
        return self

    def postback(self, payload: str, execute: Optional[str] = None):
        """
        Set the action type to postback and assign the payload to send back to the server when the button/quick reply is clicked.
        :param payload: The payload to send back to the server (max 1,000 characters).
        :param execute: Optional. Metadata sent when the button/quick reply is clicked.
        :raises ValueError: If the payload exceeds 1000 characters.
        :return: self
        """
        if len(payload) > 1000:
            raise ValueError("Payload cannot exceed 1000 characters.")

        self.action_type = "postback"
        self.payload = payload[:1000]  # Truncate payload to 1000 characters
        self.execute = execute
        return self

    def share_location(self):
        """
        Set the action type to share_location and request the user's location.
        :return: self
        """
        self.action_type = "share_location"
        return self

    def view_location(
        self, latitude: float, longitude: float, place_name: Optional[str] = None
    ):
        """
        Set the action type to view_location and send the user a location.
        :param latitude: The latitude of the location.
        :param longitude: The longitude of the location.
        :param place_name: Optional name for the location
        :return: self
        """
        self.action_type = "view_location"
        self.lat_lng = LatLng(lat=latitude, lng=longitude)
        self.label = place_name

        return self

    def calendar(
        self,
        start_time: datetime,
        end_time: datetime,
        title: str,
        description: Optional[str] = None,
    ):
        """
        Set the action type to calendar and assign the event details.
        :param start_time: The start time of the event. Will be converted to ISO format.
        :param end_time: The end time of the event. Will be converted to ISO format.
        :param title: The title of the event.
        :param description: Optional description of the event.
        :return: self
        """
        self.action_type = "calendar"
        self.start_time = start_time.isoformat()
        self.end_time = end_time.isoformat()
        self.event_title = title
        self.event_description = description
        return self

    def to_dict(self):
        """
        Convert the action to a dictionary representation.
        :return: A dictionary representation of the action.
        """

        return self.__dict__


class Message:
    """
    Represents a message to be sent.

    Attributes:
        quick_replies: List[Action]: A list of quick reply actions.
    """

    quick_replies: List[Action]

    def __init__(self):
        pass

    def with_quick_replies(self, quick_replies: List[Action]):
        """
        Add quick replies to the message.
        :param quick_replies: A list of quick reply actions.
        :raises ValueError: If the number of quick replies exceeds 11.
        :return: self
        """
        if len(quick_replies) > 11:
            raise ValueError("A card can have a maximum of 11 buttons.")
        self.quick_replies = quick_replies
        return self

    def to_dict(self):
        """
        Convert the message to a dictionary representation.
        :return: A dictionary representation of the message.
        """

        def convert_to_dict(obj):
            if isinstance(obj, list):
                return [convert_to_dict(item) for item in obj]
            elif isinstance(obj, dict):
                return {
                    key: convert_to_dict(value)
                    for key, value in obj.items()
                    if value is not None
                }
            elif hasattr(obj, "__dict__"):
                return {
                    key: convert_to_dict(value)
                    for key, value in obj.__dict__.items()
                    if value is not None
                }
            else:
                return obj

        return convert_to_dict(self)


CardOrientation = Union[
    Literal["horizontal"],
    Literal["vertical"],
]
"""
CardOrientation represents the orientation of a card in a carousel.

Attributes:
    horizontal: Represents a horizontal card orientation.
    vertical: Represents a vertical card orientation.
"""

CardWidth = Union[
    Literal["small"],
    Literal["medium"],
]
"""
CardWidth represents the width of a card in a carousel.

Attributes:
    short: Represents a small card width.
    medium: Represents a medium card width.
    large: Represents a large card width.
"""

MediaHeight = Union[
    Literal["short"],
    Literal["medium"],
    Literal["tall"],
]
"""
MediaHeight represents the height of media in a rich card.

Attributes:
    small: Represents a small media height.
    medium: Represents a medium media height.
    large: Represents a large media height.
"""

CardImageAlignment = Union[Literal["left"], Literal["right"]]
"""
CardImageAlignment represents the alignment of the image in a rich card.

Attributes:
    left: Represents left alignment.
    right: Represents right alignment.
"""


class CardStyle(TypedDict):
    """
    Represents the style of a card in a carousel.

    Attributes:
        orientation (Optional[CardOrientation]): The orientation of the card.
        width (Optional[CardWidth]): The width of the card.
        thumbnail_url (Optional[str]): The URL of the thumbnail image.
        image_alignment (Optional[CardImageAlignment]): The alignment of the image in the card. Only available for orientation "horizontal".
        media_height (Optional[MediaHeight]): The height of the media. Only available for orientation "vertical".
    """

    orientation: Optional[CardOrientation]
    width: Optional[CardWidth]
    thumbnail_url: Optional[str]
    image_alignment: Optional[CardImageAlignment]
    media_height: Optional[MediaHeight]


class Card(Message):
    """
    Represents a card to be sent.

    Attributes:
        title (str): The title of the card.
        subtitle (Optional[str]): The subtitle of the card.
        image_url (Optional[str]): The URL of the image to be displayed on the card.
        buttons (List[Action]): A list of actions (buttons) associated with the card.
        card_style (Optional[CardStyle]): The style of the card.

    """

    title: str
    subtitle: Optional[str]
    image_url: Optional[str]
    buttons: List[Action]
    card_style: Optional[CardStyle]

    def __init__(
        self,
        title: str,
        subtitle: Optional[str] = None,
        image_url: Optional[str] = None,
    ):
        """
        Initialize a Card object.
        :param title: The title of the card. The max length is 80 characters.
        :param subtitle: The subtitle of the card. The max length is 80 characters.
        :param image_url: The URL of the image to be displayed on the card.
        :raises ValueError: If the title or subtitle exceeds the maximum length.
        """
        if len(title) > 80:
            raise ValueError("Title cannot exceed 80 characters.")
        if subtitle and len(subtitle) > 80:
            raise ValueError("Subtitle cannot exceed 80 characters.")

        self.title = title
        self.subtitle = subtitle
        self.image_url = image_url
        self.buttons = []

    def with_buttons(self, buttons: List[Action]):
        """
        Add buttons to the card.
        :param buttons: A list of action buttons.
        :raises ValueError: If the number of buttons exceeds 4.
        :return: self
        """
        if len(buttons) > 4:
            raise ValueError("A card can have a maximum of 4 buttons.")
        self.buttons = buttons
        return self

    def with_horizontal_style(
        self,
        width: Optional[CardWidth] = None,
        thumbnail_url: Optional[str] = None,
        image_alignment: Optional[CardImageAlignment] = None,
    ):
        """
        Add horizontal style to the card.
        :param width: The width of the card.
        :param thumbnail_url: The URL of the thumbnail image.
        :param image_alignment: The alignment of the image in the card.
        :return: self
        """

        self.card_style = {
            "width": width,
            "orientation": "horizontal",
            "thumbnail_url": thumbnail_url,
            "image_alignment": image_alignment,
            "media_height": None,
        }
        return self

    def with_vertical_style(
        self,
        width: Optional[CardWidth] = None,
        thumbnail_url: Optional[str] = None,
        media_height: Optional[MediaHeight] = None,
    ):
        """
        Add vertical style to the card.
        :param width: The width of the card.
        :param thumbnail_url: The URL of the thumbnail image.
        :param media_height: The height of the media.
        :return: self
        """

        self.card_style = {
            "width": width,
            "orientation": "vertical",
            "thumbnail_url": thumbnail_url,
            "image_alignment": None,
            "media_height": media_height,
        }
        return self


class Carousel(Message):
    """
    Represents carousels to be sent.

    Attributes:
        cards (List[Card]): A list of cards in the carousel. Maximum of 10 cards.
    """

    cards: List[Card]

    def __init__(self, cards: List[Card]):
        """
        Initialize a Carousel object.
        :param cards: A list of Card objects.
        :raises ValueError: If the number of cards exceeds 10
        :raises ValueError: If the number of buttons in a card exceeds 2
        """
        super().__init__()
        if len(cards) > 10:
            raise ValueError("A carousel can have a maximum of 10 cards.")
        if len(cards) > 1:
            for card in cards:
                if len(card.buttons) > 2:
                    raise ValueError(
                        "Cards inside a carousel can have a maximum of 2 buttons."
                    )
        self.cards = cards


class RCSBasicMessage(Message):
    """
    Represents a basic message to be sent.

    Attributes:
        text (str): The text of the message.
    """

    text: str

    def __init__(self, text: str):
        """
        Initialize an RCSBasicMessage object.
        :param text: The text of the message.
        """
        super().__init__()
        self.text = text


class RCSMediaMessage(Message):
    """
    Represents a media message to be sent.

    Attributes:
        media_url (str): The URL of the media to be sent.
        media_type (MediaType): The type of media being sent.
    """

    media_url: str
    media_type: MediaType

    def __init__(self, media_url: str, media_type: MediaType):
        """
        Initialize an RCSMediaMessage object.
        :param media_url: The URL of the media to be sent.
        :param media_type: The type of media being sent.
        """
        super().__init__()
        self.media_url = media_url
        self.media_type = media_type


class SMSMessage(Message):
    """
    Represents an SMS message to be sent.

    Attributes:
        body (str): The body of the SMS message.
        mediaUrl (Optional[str]): The URL of the media to be sent with the SMS.

    """

    body: str
    mediaUrl: Optional[str] = None

    def __init__(self, body: str, mediaUrl: Optional[str] = None):
        """
        Initialize an SMSMessage object.
        :param body: The text of the SMS message.
        :param mediaUrl: Optional. The URL of the media to be sent with the SMS.
        """
        super().__init__()
        self.body = body
        self.mediaUrl = mediaUrl
