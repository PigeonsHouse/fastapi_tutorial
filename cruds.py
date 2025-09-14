from fastapi import HTTPException
from sqlalchemy.orm.session import Session
from schemas import UserSchema
from db import User
from utils import get_password_hash


def add_user(db: Session, email: str, name: str, password: str) -> UserSchema:
    users_orm = db.query(User).filter(User.email == email).all()
    if users_orm:
        raise HTTPException(status_code=400, detail="this email is already exist")

    user_orm = User(email=email, name=name, password_hash=get_password_hash(password))

    db.add(user_orm)
    db.commit()
    db.refresh(user_orm)
    user_info = UserSchema.model_validate(user_orm)
    return user_info


def get_user_id(db: Session, email: str, password: str) -> str:
    user: User = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="user not found")

    password_hash = get_password_hash(password)
    if user.password_hash != password_hash:
        raise HTTPException(status_code=401, detail="authentication failed")

    return user.id


def get_user_by_id(db: Session, user_id: str) -> UserSchema:
    user_orm = db.query(User).filter(User.id == user_id).first()
    if user_orm is None:
        raise HTTPException(status_code=404, detail="this user is not found")
    user = UserSchema.model_validate(user_orm)
    return user


## 作る関数1
# contentsを全件取得する関数を作りたい。(fetch_contents関数で使いたい)
# 1. db.queryでcontentsのテーブルにあるデータを全て取ってくる
# 2. 取ってきた1つ1つのデータをmodel_validateを使って、APIが返す用のschemaに変換する
# 3. 変換したデータのリストをreturnする

## 作る関数2
# contentを作成する関数を作りたい。(post_content関数で使用したい)
# 1. 引数から、contentsテーブルにcontentを作るために必要なデータを全て受け取る
#    hint: db.pyの定義がテーブルの定義。defaultのないColumnのデータはcontentを作るために必要になる
# 2. 引数の値を使い、DBで扱う方のContentのクラスを組み立て、DBにcommit, refreshする
#    hint: cruds.pyのadd_userで、Userクラスで同じようなことをしているので、参考にしてみよう
# 3. model_validateでAPIが返す用のschemaに変換し、returnする
