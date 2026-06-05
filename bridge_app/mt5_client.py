import MetaTrader5 as mt5
import logging

logger = logging.getLogger(__name__)

# Identificador único para las órdenes enviadas por este bot
MAGIC_NUMBER = 202606

def initialize_mt5(account=None, password=None, server=None):
    """
    Initialize connection to MT5. Optionally login if credentials are provided.
    """
    logger.info("Initializing MetaTrader 5...")
    
    # Intenta inicializar. Retorna True si tiene éxito
    if not mt5.initialize():
        logger.error(f"mt5.initialize() failed, error code = {mt5.last_error()}")
        return False
        
    logger.info("MT5 Initialized successfully")
    
    if account and password and server:
        logger.info(f"Attempting to login to account {account} on server {server}...")
        authorized = mt5.login(int(account), password=password, server=server)
        if authorized:
            logger.info("Login successful")
            return True
        else:
            logger.error(f"Login failed, error code = {mt5.last_error()}")
            return False
            
    return True

def get_symbol_price(symbol: str):
    """
    Get the current tick price for a symbol.
    """
    tick = mt5.symbol_info_tick(symbol)
    if tick is None:
        logger.error(f"Failed to get tick for symbol: {symbol}")
        return None
    
    return {
        "symbol": symbol,
        "ask": tick.ask,
        "bid": tick.bid,
        "last": tick.last,
        "time": tick.time
    }

def get_account_info():
    """
    Get current account information (balance, equity, margin).
    """
    account_info = mt5.account_info()
    if account_info is None:
        logger.error(f"Failed to get account info, error code = {mt5.last_error()}")
        return None
    
    return account_info._asdict()

def is_connected():
    """
    Check if MT5 is initialized and connected to the server.
    """
    terminal_info = mt5.terminal_info()
    if terminal_info is None:
        return False
    return True

def place_order(symbol, action, volume, sl_pips=None, tp_pips=None):
    """
    Place a market order with optional SL and TP.
    """
    if not is_connected():
        return {"error": "MT5 not connected"}

    symbol_info = mt5.symbol_info(symbol)
    if symbol_info is None:
        return {"error": f"Symbol {symbol} not found"}

    if not symbol_info.visible:
        if not mt5.symbol_select(symbol, True):
            return {"error": f"Failed to select symbol {symbol}"}

    tick = mt5.symbol_info_tick(symbol)
    if tick is None:
        return {"error": f"Failed to get tick for {symbol}"}

    order_type = mt5.ORDER_TYPE_BUY if action.upper() == "BUY" else mt5.ORDER_TYPE_SELL
    price = tick.ask if action.upper() == "BUY" else tick.bid
    point = symbol_info.point

    sl = None
    tp = None

    if sl_pips:
        sl = price - (sl_pips * point) if action.upper() == "BUY" else price + (sl_pips * point)
    
    if tp_pips:
        tp = price + (tp_pips * point) if action.upper() == "BUY" else price - (tp_pips * point)

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": float(volume),
        "type": order_type,
        "price": price,
        "deviation": 20,
        "magic": MAGIC_NUMBER,
        "comment": "Bot Automatizado - Bridge API",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_FOK,
    }

    if sl:
        request["sl"] = sl
    if tp:
        request["tp"] = tp

    result = mt5.order_send(request)
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        logger.error(f"Order failed: {result.retcode}, comment: {result.comment}")
        return {"error": result.comment, "retcode": result.retcode}

    return result._asdict()

def get_daily_profit():
    """
    Calculate total profit/loss for the current day.
    """
    from datetime import datetime, time
    today_start = datetime.combine(datetime.now().date(), time.min)
    
    # Get history for today
    history_deals = mt5.history_deals_get(today_start, datetime.now())
    if history_deals is None:
        return 0.0
        
    total_profit = sum(deal.profit for deal in history_deals)
    return total_profit

def close_all_positions():
    """
    Panic function: Close all open positions.
    """
    positions = mt5.positions_get()
    if positions is None:
        return True
        
    results = []
    for pos in positions:
        symbol = pos.symbol
        ticket = pos.ticket
        volume = pos.volume
        pos_type = pos.type
        
        # Opposite order to close
        order_type = mt5.ORDER_TYPE_SELL if pos_type == mt5.ORDER_TYPE_BUY else mt5.ORDER_TYPE_BUY
        tick = mt5.symbol_info_tick(symbol)
        if tick is None:
            results.append({"error": f"Could not get tick for {symbol}"})
            continue
            
        price = tick.bid if pos_type == mt5.ORDER_TYPE_BUY else tick.ask
        
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": volume,
            "type": order_type,
            "position": ticket,
            "price": price,
            "deviation": 20,
            "magic": MAGIC_NUMBER,
            "comment": "Panic Close - Daily Drawdown reached",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_FOK,
        }
        results.append(mt5.order_send(request))
    
    return results

def get_open_positions():
    """
    Get all current open positions.
    """
    positions = mt5.positions_get()
    if positions is None:
        return []
    
    return [p._asdict() for p in positions]

def get_history(days=7):
    """
    Get deal history for the last N days.
    """
    from datetime import datetime, timedelta
    start_date = datetime.now() - timedelta(days=days)
    end_date = datetime.now()
    
    deals = mt5.history_deals_get(start_date, end_date)
    if deals is None:
        return []
        
    return [d._asdict() for d in deals]

def modify_position_sl_tp(ticket, sl=None, tp=None):
    """
    Modify SL and/or TP of an existing position.
    """
    position = mt5.positions_get(ticket=ticket)
    if not position:
        return {"error": f"Position {ticket} not found"}
    
    pos = position[0]
    symbol = pos.symbol
    
    request = {
        "action": mt5.TRADE_ACTION_SLTP,
        "symbol": symbol,
        "position": ticket,
        "sl": float(sl) if sl is not None else pos.sl,
        "tp": float(tp) if tp is not None else pos.tp,
    }
    
    result = mt5.order_send(request)
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        return {"error": result.comment, "retcode": result.retcode}
        
    return result._asdict()

def close_position(ticket):
    """
    Close a specific position by ticket.
    """
    position = mt5.positions_get(ticket=ticket)
    if not position:
        return {"error": f"Position {ticket} not found"}
    
    pos = position[0]
    symbol = pos.symbol
    volume = pos.volume
    pos_type = pos.type
    
    order_type = mt5.ORDER_TYPE_SELL if pos_type == mt5.ORDER_TYPE_BUY else mt5.ORDER_TYPE_BUY
    tick = mt5.symbol_info_tick(symbol)
    if tick is None:
        return {"error": f"Could not get tick for {symbol}"}
        
    price = tick.bid if pos_type == mt5.ORDER_TYPE_BUY else tick.ask
    
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": volume,
        "type": order_type,
        "position": ticket,
        "price": price,
        "deviation": 20,
        "magic": MAGIC_NUMBER,
        "comment": "Manual Close via API",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_FOK,
    }
    
    result = mt5.order_send(request)
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        return {"error": result.comment, "retcode": result.retcode}
        
    return result._asdict()

def get_symbol_info(symbol: str):
    """
    Get detailed information for a symbol.
    """
    info = mt5.symbol_info(symbol)
    if info is None:
        return None
    return info._asdict()

def shutdown():
    mt5.shutdown()
