set transaction read write;

insert into exchanges
(exchange, APIKEY, SECRET, PASSPHRASE)
values
('binance', 'xxxxxxxxxxxxxxxxxxxxxxx', 'xxxxxxxxxxxxxxxxxxxxxxx', null);
commit;

insert into users
(USER_ID, TELEGRAM_ID, EMAIL, ROLE)
values
('somebody', '0', 'noreply@pyCTelebot', 'ADMIN');

insert into users
(USER_ID, EXCHANGE, APIKEY, SECRET, PASSPHRASE)
values
('somebody',  'binance', 'xxxxxxxxxxxxxxxxxxxxxxx', 'xxxxxxxxxxxxxxxxxxxxxxx', null);
commit;

insert into strategies
(strategy_id, description, strategy_type)
VALUES
('STRATEGY_01', 'Test Strategy_01', 'COMPUTE');
commit;

insert into strategy_symbols
(strategy_id, exchange, symbol, unit_value, take_profit, buy_in_callback)
values
('STRATEGY_01', 'binance', 'ETH/USDT', 1, 5,  0.1);
commit;

INSERT INTO strategy_steps
(strategy_id, exchange, symbol, step, step_type, margin, units)
values
('STRATEGY_01', 'binance', 'ETH/USDT', 1, 'BUY', 1, 1);
INSERT INTO strategy_steps
(strategy_id, exchange, symbol, step, step_type, margin, units)
values
('STRATEGY_01', 'binance', 'ETH/USDT', 2, 'BUY', 1, 1);
INSERT INTO strategy_steps
(strategy_id, exchange, symbol, step, step_type, margin, units)
values
('STRATEGY_01', 'binance', 'ETH/USDT', 3, 'BUY', 1, 1);
INSERT INTO strategy_steps
(strategy_id, exchange, symbol, step, step_type, margin, units)
values
('STRATEGY_01', 'binance', 'ETH/USDT', 4, 'BUY', 1, 1);
INSERT INTO strategy_steps
(strategy_id, exchange, symbol, step, step_type, margin, units)
values
('STRATEGY_01', 'binance', 'ETH/USDT', 5, 'BUY', 1, 1);
INSERT INTO strategy_steps
(strategy_id, exchange, symbol, step, step_type, margin, units)
values
('STRATEGY_01', 'binance', 'ETH/USDT', 6, 'BUY', 1, 1);
INSERT INTO strategy_steps
(strategy_id, exchange, symbol, step, step_type, margin, units)
values
('STRATEGY_01', 'binance', 'ETH/USDT', 7, 'BUY', 1, 1);
INSERT INTO strategy_steps
(strategy_id, exchange, symbol, step, step_type, margin, units)
values
('STRATEGY_01', 'binance', 'ETH/USDT', 8, 'BUY', 1, 1);
INSERT INTO strategy_steps
(strategy_id, exchange, symbol, step, step_type, margin, units)
values
('STRATEGY_01', 'binance', 'ETH/USDT', 9, 'BUY', 1, 1);
INSERT INTO strategy_steps
(strategy_id, exchange, symbol, step, step_type, margin, units)
values
('STRATEGY_01', 'binance', 'ETH/USDT', 10, 'BUY', 1, 1);
INSERT INTO strategy_steps
(strategy_id, exchange, symbol, step, step_type, margin, units)
values
('STRATEGY_01', 'binance', 'ETH/USDT', 11, 'BUY', 1, 1);
INSERT INTO strategy_steps
(strategy_id, exchange, symbol, step, step_type, margin, units)
values
('STRATEGY_01', 'binance', 'ETH/USDT', 12, 'BUY', 1, 1);
INSERT INTO strategy_steps
(strategy_id, exchange, symbol, step, step_type, margin, units)
values
('STRATEGY_01', 'binance', 'ETH/USDT', 13, 'BUY', 1, 1);
INSERT INTO strategy_steps
(strategy_id, exchange, symbol, step, step_type, margin, units)
values
('STRATEGY_01', 'binance', 'ETH/USDT', 14, 'BUY', 1, 1);
INSERT INTO strategy_steps
(strategy_id, exchange, symbol, step, step_type, margin, units)
values
('STRATEGY_01', 'binance', 'ETH/USDT', 15, 'BUY', 1, 1);
commit;
insert into exchange_prices
(
exchange, symbol,
last_buy_price, current_buy_price, buy_price_variation_percentage,
last_sell_price, current_sell_price, sell_price_variation_percentage,
last_audit_date, current_audit_date
)
values
('kucoin', 'BTC/USDT',
1, 1, 1,
1, 1, 1,
current_date, current_date);
insert into exchange_prices
(
exchange, symbol,
last_buy_price, current_buy_price, buy_price_variation_percentage,
last_sell_price, current_sell_price, sell_price_variation_percentage,
last_audit_date, current_audit_date
)
values
('kucoin', 'ETH/USDT',
1, 1, 1,
1, 1, 1,
current_date, current_date);
insert into exchange_prices
(
exchange, symbol,
last_buy_price, current_buy_price, buy_price_variation_percentage,
last_sell_price, current_sell_price, sell_price_variation_percentage,
last_audit_date, current_audit_date
)
values
('kucoin', 'LINK/USDT',
1, 1, 1,
1, 1, 1,
current_date, current_date);
insert into exchange_prices
(
exchange, symbol,
last_buy_price, current_buy_price, buy_price_variation_percentage,
last_sell_price, current_sell_price, sell_price_variation_percentage,
last_audit_date, current_audit_date
)
values
('kucoin', 'CRO/USDT',
1, 1, 1,
1, 1, 1,
current_date, current_date);
insert into exchange_prices
(
exchange, symbol,
last_buy_price, current_buy_price, buy_price_variation_percentage,
last_sell_price, current_sell_price, sell_price_variation_percentage,
last_audit_date, current_audit_date
)
values
('binance', 'BTC/USDT',
1, 1, 1,
1, 1, 1,
current_date, current_date);
insert into exchange_prices
(
exchange, symbol,
last_buy_price, current_buy_price, buy_price_variation_percentage,
last_sell_price, current_sell_price, sell_price_variation_percentage,
last_audit_date, current_audit_date
)
values
('binance', 'ETH/USDT',
1, 1, 1,
1, 1, 1,
current_date, current_date);
commit;
