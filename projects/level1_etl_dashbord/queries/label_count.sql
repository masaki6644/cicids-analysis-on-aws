SELECT Label, COUNT(*) AS count 
FROM ids_logs_db.processed 
GROUP BY Label 
ORDER BY count DESC;
