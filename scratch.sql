USE ffft;
-- TEST DATA INTO TABLES

call sp_truncate_exchange_decom();

call sp_insert_exchange_decom('1', 'Salisbury', 'Salisbury', 'STSALIS', '2020-12-01 00:00:00', '2019-12-01', 'Trial notification ');
call sp_insert_exchange_decom('2', 'Swansea', 'Swansea', 'SWSX', '2021-10-13 00:00:00', '2021-05-10', 'Tranche 1b');


call sp_insert_exchange_query('01179771960', None, None, None, None, 5, None, 23, None);
call sp_insert_exchange_query('01179771960', None, None, None, None, 5, None, 23, None, None);
call sp_insert_exchange_query('01484711152', None, None, None, None, 10, None, 23, None, None);
call sp_insert_exchange_query(None, 'WWLEED', None, None, None, -10, None, 23, None);
call sp_insert_exchange_query(None, 'NIBRH', None, None, None, 1001, None, 23, None);

call sp_insert_file_upload('craig@2deviate.com', '06206.csv', '/home/craig/python/p...ta/uploads', 157, "2022-08-18", 1);
call sp_insert_file_upload('craig@2deviate.com', '6ae6a.csv', '/home/app/app/data/uploads', 157, datetime.datetime(2022, 8, 19, 11, 34, 41, 808579), 1, None);


call sp_insert_exchange_query('01179771960', None, None, None, None, 1, None, 5)
call sp_insert_exchange_query(None, 'NIBRH', None, None, None, 1001, None, 8)