from datetime import datetime
from fastapi import APIRouter, Depends, Query
from fastapi.responses import PlainTextResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator, Optional

from database import async_session_maker
from models import TradeResult
from serializers import TradeResultSerializer

router = APIRouter()


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


@router.get("/", response_class=PlainTextResponse)
async def get_trade_results(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(TradeResult))
    trade_results = result.scalars().all()
    lines = []
    for tr in trade_results:
        lines.append(
            f"ID: {tr.id}\n"
            f"Product ID: {tr.exchange_product_id}\n"
            f"Product Name: {tr.exchange_product_name}\n"
            f"Oil ID: {tr.oil_id}\n"
            f"Delivery Basis: {tr.delivery_basis_name}\n"
            f"Volume: {tr.volume}\n"
            f"Total: {tr.total}\n"
            f"Count: {tr.count}\n"
            f"Date: {tr.date}\n"
            f"----"
        )
    return "\n\n======================\n\n".join(lines)


@router.get("/last-dates", response_class=PlainTextResponse)
async def get_last_trading_dates(
    session: AsyncSession = Depends(get_session),
    count: int = Query(5, gt=0, le=100)
):
    result = await session.execute(
        select(TradeResult.date)
        .distinct()
        .order_by(TradeResult.date.desc())
        .limit(count)
    )
    dates = [row[0].strftime("%Y-%m-%d") for row in result.fetchall()]
    return "\n".join(dates)


@router.get("/get-dynamics", response_model=list[TradeResultSerializer])
async def get_dynamics(
    session: AsyncSession = Depends(get_session),
    oil_id: Optional[str] = Query(None),
    delivery_type_id: Optional[str] = Query(None),
    delivery_basis_id: Optional[str] = Query(None),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
):
    query = select(TradeResult)

    if oil_id:
        query = query.where(TradeResult.oil_id == oil_id)
    if delivery_type_id:
        query = query.where(TradeResult.delivery_type_id == delivery_type_id)
    if delivery_basis_id:
        query = query.where(TradeResult.delivery_basis_id == delivery_basis_id)
    if start_date:
        try:
            dt_start = datetime.strptime(start_date, "%Y-%m-%d")
            query = query.where(TradeResult.date >= dt_start)
        except ValueError:
            return PlainTextResponse(
                "Неверный формат start_date, используйте YYYY-MM-DD",
                status_code=400
                )
    if end_date:
        try:
            dt_end = datetime.strptime(end_date, "%Y-%m-%d")
            query = query.where(TradeResult.date <= dt_end)
        except ValueError:
            return PlainTextResponse(
                "Неверный формат end_date, используйте YYYY-MM-DD",
                status_code=400
            )

    query = query.order_by(TradeResult.date)
    result = await session.execute(query)
    trades = result.scalars().all()

    lines = []
    for tr in trades:
        line = (
            f"ID: {tr.id}\n"
            f"Product ID: {tr.exchange_product_id}\n"
            f"Product Name: {tr.exchange_product_name}\n"
            f"Oil ID: {tr.oil_id}\n"
            f"Delivery Basis: {tr.delivery_basis_name}\n"
            f"Volume: {tr.volume}\n"
            f"Total: {tr.total}\n"
            f"Count: {tr.count}\n"
            f"Date: {tr.date}\n"
            "----"
        )
        lines.append(line)

    if not lines:
        return PlainTextResponse(
            "Нет данных по заданным условиям.", status_code=200
        )

    output = "\n\n======================\n\n".join(lines)
    return PlainTextResponse(output)


@router.get("/get_trading_results", response_class=PlainTextResponse)
async def get_trading_results(
    oil_id: str = Query(None),
    delivery_type_id: str = Query(None),
    delivery_basis_id: str = Query(None),
    limit: int = Query(10, ge=1, le=100),
    session: AsyncSession = Depends(get_session),
):
    query = select(TradeResult)

    if oil_id:
        query = query.where(TradeResult.oil_id == oil_id)
    if delivery_type_id:
        query = query.where(TradeResult.delivery_type_id == delivery_type_id)
    if delivery_basis_id:
        query = query.where(TradeResult.delivery_basis_id == delivery_basis_id)

    query = query.order_by(TradeResult.date.desc()).limit(limit)

    result = await session.execute(query)
    trades = result.scalars().all()

    if not trades:
        return PlainTextResponse("За последние дни данных не найдено.")

    lines = []
    for tr in trades:
        lines.append(
            f"ID: {tr.id}\n"
            f"Product ID: {tr.exchange_product_id}\n"
            f"Product Name: {tr.exchange_product_name}\n"
            f"Oil ID: {tr.oil_id}\n"
            f"Delivery Basis: {tr.delivery_basis_name}\n"
            f"Volume: {tr.volume}\n"
            f"Total: {tr.total}\n"
            f"Count: {tr.count}\n"
            f"Date: {tr.date}\n"
            f"----"
        )
    return "\n\n======================\n\n".join(lines)
