
WITH BUDGET_MONTH AS (
SELECT 
	bi.id
	, bi.name
	, sum(t.amount) as 'monthly_total'
FROM BUDGET_ITEMS bi
LEFT JOIN TRANSACTIONS t
	ON bi.id = t.budget_item_id
WHERE bi.is_active = TRUE
AND t.transaction_year = 2023
and t.transaction_month = 1
GROUP BY bi.id
ORDER BY bi.sequence
)
SELECT 
	bi2.id
	, bi2.name
	, CASE 
		WHEN bm.monthly_total is NULL THEN bi2.budget_amount
		ELSE bm.monthly_total
	END as monthly_total2
FROM BUDGET_ITEMS bi2
LEFT JOIN BUDGET_MONTH bm
	ON bi2.id = bm.id
ORDER BY bi2.sequence