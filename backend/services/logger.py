from models.log import Log
from sqlalchemy.orm import Session

def save_log(db: Session, user_id: int, router_id: int, action: str, commands: list[str], output: str):
    log = Log(
        user_id=user_id,
        router_id=router_id,
        action=action,
        commands="\n".join(commands),
        output=output
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log


def save_log(db, router_id: int, action: str, commands: list[str], output: str):
    log = Log(
        router_id=router_id,
        action=action,
        commands="\n".join(commands),
        output=output
    )
    db.add(log)
    db.commit()

def save_log(db: Session, user_id: int, router_id: int, action: str, commands: list[str], output: str):
    log = Log(
        user_id=user_id,
        router_id=router_id,
        action=action,
        commands="\n".join(commands),
        output=output
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log