SELECT  
    CASE  
        WHEN Label = 'BENIGN' THEN 'Normal' 
        ELSE 'Attack' 
    END AS Type, 
    COUNT(*) AS count 
FROM ids_logs_db.processed 
GROUP BY  
    CASE  
        WHEN Label = 'BENIGN' THEN 'Normal' 
        ELSE 'Attack' 
    END; 

