WITH link_counts AS (
    SELECT
        u.email,
        u.date_joined,
        COUNT(l.id) AS count_links,
        SUM(CASE WHEN l.type = 'website' THEN 1 ELSE 0 END) AS website,
        SUM(CASE WHEN l.type = 'book' THEN 1 ELSE 0 END) AS book,
        SUM(CASE WHEN l.type = 'article' THEN 1 ELSE 0 END) AS article,
        SUM(CASE WHEN l.type = 'music' THEN 1 ELSE 0 END) AS music,
        SUM(CASE WHEN l.type = 'video' THEN 1 ELSE 0 END) AS video,
        SUM(CASE WHEN l.type = 'object' THEN 1 ELSE 0 END) AS object,
        SUM(CASE WHEN l.type = 'error' THEN 1 ELSE 0 END) AS error
    FROM
        api_customuser AS u
    LEFT JOIN
        api_link AS l ON u.id = l.user_id
    GROUP BY
        u.id, u.email, u.date_joined
)
SELECT
    email,
    count_links,
    website,
    book,
    article,
    music,
    video,
    object,
    error,
    date_joined
FROM
    link_counts
ORDER BY
    count_links DESC,
    date_joined ASC
LIMIT 10;
