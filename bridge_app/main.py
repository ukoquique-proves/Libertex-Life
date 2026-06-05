import os
from fastapi import FastAPI, HTTPException
from fastapi.concurrency import run_in_threadpool
from pydantic import BaseModel
from contextlib import asynccontextmanager
import bridge_app.mt5_client as mt5_client
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration from environment variables
MT5_ACCOUNT = os.getenv("MT5_ACCOUNT")
MT5_PASSWORD = os.getenv("MT5_PASSWORD")
MT5_SERVER = os.getenv("MT5_SERVER")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Conectar con MT5
    success = await run_in_threadpool(mt5_client.initialize_mt5, MT5_ACCOUNT, MT5_PASSWORD, MT5_SERVER)
    if not success:
        logger.error("Failed to connect to MT5 on startup.")
    yield
    # Shutdown: Desconectar
    await run_in_threadpool(mt5_client.shutdown)

app = FastAPI(title="MT5 Bridge API", lifespan=lifespan)

# Risk parameters (could also be env variables)
MAX_DAILY_DRAWDOWN_PCT = 0.05  # 5%
MAX_ALLOWED_SPREAD_PIPS = 10   # Max spread to allow entry

class TradeRequest(BaseModel):
    symbol: str
    action: str  # "BUY" or "SELL"
    volume: float = None
    sl_pips: float = None
    tp_pips: float = None
    risk_percent: float = 1.0  # Default 1% risk if volume is not provided

class ModifyRequest(BaseModel):
    ticket: int
    sl: float = None
    tp: float = None

async def check_drawdown():
    """
    Check if daily drawdown exceeds MAX_DAILY_DRAWDOWN_PCT.
    Stateless implementation: calculates based on real-time MT5 history.
    """
    from datetime import datetime
    
    account = await run_in_threadpool(mt5_client.get_account_info)
    if not account:
        return False, "Could not check drawdown"
        
    balance = account.get("balance")
    equity = account.get("equity")
    
    # 1. Profit from closed trades today
    daily_realized_profit = await run_in_threadpool(mt5_client.get_daily_profit)
    
    # 2. Floating profit/loss from current open positions
    # Floating Drawdown = Balance - Equity (if Equity < Balance)
    # We use a conservative approach: Realized Profit + Floating Profit
    floating_profit = equity - balance
    
    total_daily_pnl = daily_realized_profit + floating_profit
    
    # Drawdown is reached if total PnL is negative and exceeds the limit
    if total_daily_pnl < 0 and abs(total_daily_pnl) >= balance * MAX_DAILY_DRAWDOWN_PCT:
        logger.warning(f"DAILY DRAWDOWN REACHED: {total_daily_pnl}. Executing panic close.")
        await run_in_threadpool(mt5_client.close_all_positions)
        return True, f"Daily drawdown limit ({MAX_DAILY_DRAWDOWN_PCT*100}%) reached. Trading blocked."
        
    return False, None

def is_high_impact_news_near(symbol: str):
    """
    Filtro Fundamental (Placeholder Crítico):
    Determina si hay noticias de alto impacto (ej. tasas de la Fed, NFP) próximas.
    
    Riesgo Operativo: Operar durante noticias puede causar gaps y slippage masivo
    que supere el 'deviation' configurado. 
    
    Implementación futura recomendada: 
    Integrar con API de ForexFactory o Investing.com para bloquear 30 min antes/después.
    """
    # Por ahora retorna False, asumiendo que el trader filtra manualmente o 
    # acepta el riesgo de volatilidad extrema.
    return False

@app.get("/api/v1/status")
async def get_status():
    terminal_info = await run_in_threadpool(lambda: mt5_client.mt5.terminal_info())
    return {"status": "running", "mt5_connected": terminal_info is not None}

@app.get("/api/v1/account")
async def get_account():
    info = await run_in_threadpool(mt5_client.get_account_info)
    if not info:
        raise HTTPException(status_code=500, detail="Could not retrieve account info")
    return info

@app.get("/api/v1/price/{symbol}")
async def get_price(symbol: str):
    price_info = await run_in_threadpool(mt5_client.get_symbol_price, symbol)
    if not price_info:
        raise HTTPException(status_code=404, detail=f"Symbol {symbol} not found or MT5 not connected")
    return price_info

@app.get("/api/v1/positions")
async def get_positions():
    return await run_in_threadpool(mt5_client.get_open_positions)

@app.get("/api/v1/history")
async def get_history(days: int = 7):
    return await run_in_threadpool(mt5_client.get_history, days)

@app.get("/api/v1/summary")
async def get_summary():
    """
    Dashboard summary: Account health, active risk, and performance.
    """
    account = await run_in_threadpool(mt5_client.get_account_info)
    positions = await run_in_threadpool(mt5_client.get_open_positions)
    daily_profit = await run_in_threadpool(mt5_client.get_daily_profit)
    
    if not account:
        raise HTTPException(status_code=500, detail="Could not retrieve account info")
        
    balance = account.get("balance")
    equity = account.get("equity")
    floating_pnl = equity - balance
    
    return {
        "account_info": {
            "balance": balance,
            "equity": equity,
            "margin_free": account.get("margin_free"),
            "daily_profit": daily_profit,
            "floating_pnl": floating_pnl
        },
        "active_risk": {
            "open_positions_count": len(positions),
            "current_drawdown_pct": round(abs(min(0, daily_profit + floating_pnl)) / balance * 100, 2)
        },
        "status": "safe" if (daily_profit + floating_pnl) > -balance * MAX_DAILY_DRAWDOWN_PCT else "danger"
    }

@app.post("/api/v1/order")
async def place_order(trade: TradeRequest):
    # 1. Check Daily Drawdown
    is_blocked, reason = await check_drawdown()
    if is_blocked:
        raise HTTPException(status_code=403, detail=reason)
        
    # 2. Check News Filter
    if is_high_impact_news_near(trade.symbol):
        raise HTTPException(status_code=403, detail="High impact news near. Trading blocked for this symbol.")

    # 3. Check Spread
    price_info = await run_in_threadpool(mt5_client.get_symbol_price, trade.symbol)
    if not price_info:
        raise HTTPException(status_code=404, detail=f"Symbol {trade.symbol} not found")
        
    symbol_info = await run_in_threadpool(mt5_client.get_symbol_info, trade.symbol)
    spread_pips = (price_info['ask'] - price_info['bid']) / symbol_info['point']
    
    if spread_pips > MAX_ALLOWED_SPREAD_PIPS:
        raise HTTPException(status_code=403, detail=f"Spread too high: {spread_pips} pips. Limit is {MAX_ALLOWED_SPREAD_PIPS}.")

    # 4. Calculate Volume if needed
    volume = trade.volume
    if volume is None:
        if trade.sl_pips is None:
            raise HTTPException(status_code=400, detail="Volume or SL Pips must be provided for risk calculation")
        
        # Risk management logic
        account = await run_in_threadpool(mt5_client.get_account_info)
        balance = account.get("balance")
        risk_amount = balance * (trade.risk_percent / 100)
            
        tick_value = symbol_info.get('trade_tick_value')
        tick_size = symbol_info.get('trade_tick_size')
        
        if tick_value == 0 or tick_size == 0:
            tick_value = 10.0 # fallback for major forex
            tick_size = 0.0001
            
        # Lot calculation: Risk / (SL_in_points * (TickValue/TickSize))
        # Points = SL_Pips * (Point / TickSize) -- simplification
        # Standard formula: Lots = RiskAmount / (StopLossDistance * TickValue/TickSize)
        
        sl_points = trade.sl_pips * (symbol_info['point'] / tick_size)
        volume = risk_amount / (sl_points * tick_value)
        
        # Adjust to step volume
        vol_step = symbol_info.get('volume_step', 0.01)
        volume = round(volume / vol_step) * vol_step
        
        # Ensure within min/max volume
        vol_min = symbol_info.get('volume_min', 0.01)
        vol_max = symbol_info.get('volume_max', 100.0)
        volume = max(vol_min, min(vol_max, volume))
        
        volume = round(volume, 2)

    result = await run_in_threadpool(
        mt5_client.place_order,
        trade.symbol,
        trade.action,
        volume,
        trade.sl_pips,
        trade.tp_pips
    )
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
        
    return result

@app.put("/api/v1/order/modify")
async def modify_order(modify: ModifyRequest):
    result = await run_in_threadpool(
        mt5_client.modify_position_sl_tp,
        modify.ticket,
        modify.sl,
        modify.tp
    )
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@app.delete("/api/v1/order/close/{ticket}")
async def close_order(ticket: int):
    result = await run_in_threadpool(mt5_client.close_position, ticket)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("bridge_app.main:app", host="0.0.0.0", port=8000, reload=True)
