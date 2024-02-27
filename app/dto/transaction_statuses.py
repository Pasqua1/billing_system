from pydantic import BaseModel, ConfigDict
from app.usecase.utils.responses import ResponseModel


class TransactionStatusBaseModel(BaseModel):
    status_id: int
    model_config = ConfigDict(from_attributes=True)


class TransactionStatusInsertModel(BaseModel):
    status_name: str


class TransactionStatusFullModel(TransactionStatusBaseModel, TransactionStatusInsertModel):
    pass


class TransactionStatusResponseModel(ResponseModel):
    transaction_status: TransactionStatusFullModel


class TransactionStatusListModel(ResponseModel):
    transaction_statuses: list[TransactionStatusFullModel]
