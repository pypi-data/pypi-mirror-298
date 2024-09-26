"""Message entity"""

from datetime import datetime
from typing import Any

from layrz_sdk.entities.general.asset import Asset

from .message import Message
from .position import Position


class LastMessage(Message):
  """
  Message definition
  ---
  Attributes
    - pk : Message ID
    - asset_id : Asset ID
    - position : Geographic position
    - payload : Message raw payload
    - sensors : Calculated sensor values
    - received_at : Message reception date and time
  """

  def __init__(
    self,
    pk: int,
    asset_id: int,
    asset: Asset,
    position: Position = None,
    payload: Any = None,
    sensors: Any = None,
    received_at: datetime = None,
  ) -> None:
    """Constructor"""
    super().__init__(pk, asset_id, position, payload, sensors, received_at)
    self.asset = asset

  def __str__(self) -> str:
    """String representation"""
    return f'LastMessage(pk: {self.pk}, asset_id: {self.asset_id}, received_at: {self.received_at})'
