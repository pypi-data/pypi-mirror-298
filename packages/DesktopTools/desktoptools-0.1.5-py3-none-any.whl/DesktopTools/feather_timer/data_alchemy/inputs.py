from sqlalchemy import desc

from ...tools import today
from .models import KeyMouse, Session


def add_count_keymouse(char_name, device, vk="") -> int:
    try:
        # 创建Session类实例
        session = Session()
        key_mouse = (
            session.query(KeyMouse)
            .filter(
                KeyMouse.name == char_name, KeyMouse.create_time.like(today() + "%")
            )
            .first()
        )
        if key_mouse:
            key_mouse.count += 1
        else:
            key_mouse = KeyMouse(name=char_name, vk=(vk or ""), device=device)
            key_mouse.count = 1
            session.add(key_mouse)
        session.commit()
        session.close()
        return 1
    except Exception as err:
        print(err)
        pass
        return 0


def iter_count_on(date=today()) -> iter:
    session = Session()
    iter_count = (
        session.query(KeyMouse)
        .order_by(desc(KeyMouse.count))
        .filter(KeyMouse.create_time.like(date + "%"))
    )
    session.close()
    return iter_count
