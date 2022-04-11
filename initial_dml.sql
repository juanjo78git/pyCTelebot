set transaction read write;

insert into users
(USER_ID, TELEGRAM_ID, EMAIL, ROLE, EXCHANGE, APIKEY, SECRET, PASSPHRASE)
values
('binance', '0', 'noreply@pyCTelebot', 'READ_ONLY', 'binance', 'xxxxxxxxxxxxxxxxxxxxxxx', 'xxxxxxxxxxxxxxxxxxxxxxx', null);
commit;

insert into strategies
(strategy_id, description)
VALUES
('STRATEGY_01', 'Test Strategy_01');
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
