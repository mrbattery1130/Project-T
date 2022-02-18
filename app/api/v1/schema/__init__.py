from typing import List, Optional

from lin import BaseModel


class BookQuerySearchSchema(BaseModel):
    q: Optional[str] = str()


class BookInSchema(BaseModel):
    title: str
    author: str
    image: str
    summary: str


class BookOutSchema(BaseModel):
    id: int
    title: str
    author: str
    image: str
    summary: str


class BookSchemaList(BaseModel):
    __root__: List[BookOutSchema]


class CatalogueOutSchema(BaseModel):
    id: int
    name: str
    name_en: str


class CatalogueSchemaList(BaseModel):
    __root__: List[CatalogueOutSchema]


class AppInSchema(BaseModel):
    name: str
    name_en: str
    catalogue_id: int
    developer_name: Optional[str] = None
    description: Optional[str] = None
    priority: int


class AppOutSchema(BaseModel):
    id: int
    name: str
    name_en: str
    catalogue_id: int
    developer_name: Optional[str] = None
    description: Optional[str] = None
    priority: int
    catalogue: Optional[CatalogueOutSchema] = None


class AppPageSchemaList(BasePageSchema):
    items: List[AppOutSchema]


class AppQuerySearchSchema(BaseModel):
    keyword: Optional[str] = None
    count: int = Field(5, gt=0, lt=16, description="0 < count < 16")
    page: int = 0

    @staticmethod
    def offset_handler(req, resp, req_validation_error, instance):
        g.offset = req.context.query.count * req.context.query.page


class AppRelInSchema(BaseModel):
    package_name: str
    launch_name: Optional[str] = None
    app_id: int


class AppRelOutSchema(BaseModel):
    id: int
    package_name: str
    launch_name: Optional[str] = None
    app_id: int


class AppRelSchemaList(BaseModel):
    __root__: List[AppRelOutSchema]


class AppIconQuerySearchSchema(BaseModel):
    package_name: Optional[str] = None


class PackageNameQuerySearchSchema(BaseModel):
    app_name: Optional[str] = None


class IconInSchema(BaseModel):
    id: int
    url: str
    iconpack_id: int
    app_id: int


class IconOutSchema(BaseModel):
    id: int
    url: str
    iconpack_id: int
    app_id: int


class IconSchemaList(BaseModel):
    __root__: List[IconOutSchema]


class IconpackInSchema(BaseModel):
    name: str
    description: Optional[str] = None


class IconpackOutSchema(BaseModel):
    id: int
    name: str
    description: Optional[str] = None


class IconpackSchemaList(BaseModel):
    __root__: List[IconpackOutSchema]


class IconSpiderOutSchema(BaseModel):
    app_store: str
    app_name: str
    app_icon_url: str
    app_url: str


class IconSpiderOutListSchema(BaseModel):
    app_icons: List[IconSpiderOutSchema]
    package_name: str


class PackageNameSpiderOutSchema(BaseModel):
    app_store: str
    package_name: str
    app_name: str
    app_icon_url: str


class PackageNameSpiderOutListSchema(BaseModel):
    __root__: List[PackageNameSpiderOutSchema]
