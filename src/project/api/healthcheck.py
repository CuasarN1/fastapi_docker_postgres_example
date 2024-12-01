from fastapi import APIRouter, status

from project.api.depends import database, user_repo
from project.schemas.healthcheck import HealthCheckSchema
from project.core.exceptions import DatabaseError

healthcheck_router = APIRouter()


@healthcheck_router.get("/healthcheck", response_model=HealthCheckSchema, status_code=status.HTTP_200_OK)
async def check_health() -> HealthCheckSchema:
    try:
        async with database.session() as session:
            db_is_ok = await user_repo.check_connection(session=session)
    except DatabaseError as error:
        db_is_ok = False

    return HealthCheckSchema(
        db_is_ok=db_is_ok,
    )
