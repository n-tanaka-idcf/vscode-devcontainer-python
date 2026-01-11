from pydantic import BaseModel, Field


class TaskBase(BaseModel):
    title: str | None = Field(default=None, examples=["クリーニングを取りに行く"])


class TaskCreate(TaskBase):
    pass


class TaskCreateResponse(TaskBase):
    id: int

    class Config:
        orm_mode = True


class Task(TaskBase):
    id: int
    done: bool = Field(default=False, description="完了フラグ")

    class Config:
        orm_mode = True
