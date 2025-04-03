# FastAPI 기능 가져오기
from fastapi import FastAPI

# 입력값을 검사하기 위한 클래스 정의 기능 가져오기
from pydantic import BaseModel

# FastAPI 앱 만들기
app = FastAPI()

# 데이트 저장용 딕셔너리. 메모리에 저장됨.
items = {}


# 사용자 입력을 위한 데이터 구조 정의
# name: 문자열 / description : 문자열
class Item(BaseModel):
    name: str
    description: str


# GET 요청: 특정 아이템 조회 기기능


@app.get("/items/{item_id}")
def read_item(item_id: int):
    # 아이템이 존재하는 경우 > 해당 아이템 반환
    if item_id in items:
        return items[item_id]
    # 아이템이 없는 경우> 에러 메시지 반환
    return {"error": "Item not found"}


# POST 요청: 새로운 아이템 생성 기능
@app.post("/items/{item_id}")
def create_item(item_id: int, item: Item):
    # 입력받은 item을 딕셔너리로 변환 후 저장 (Pydantic v2 기준)
    items[item_id] = item.model_dump()
    # 성공 메시지와 저장된 아이템 반환
    return {"message": "Item created", "item": item[item_id]}


# PUT 요청: 기존 아이템 수정 기능
@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    # 아이템이 없는 경우 > 에러 메시지 반환
    if item_id not in items:
        return {"error": ":Item not found"}
    # 아이템이 있는 경우 > 새 값으로 업데이트
    items[item_id] = item.model_dump()
    return {"message": "Item updated", "item": item[item_id]}


# DElETE 요청: 아이템 삭제 기능
@app.delete("/item/{item_id}")
def delete_item(item_id: int):
    # 아이템이 존재하는 경우 > 삭제 후 메시지 반환
    if item_id in items:
        del items[item_id]
        return {"message": "Item deleted"}
    # 없는 경우 > 에러 메시지 반환
    return {"error": "Item not found"}
