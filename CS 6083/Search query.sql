select * from topic;
select * from subtopics;
select * from questions;
#select * from likes;
select * from answers;
select * from post_answers;
select * from users;
#select * from post_question;

select answers.aid, body, Floor(Power(10, MATCH(answers.body) AGAINST ('address' IN BOOLEAN MODE))) AS count
from answers
;

SELECT answers.aid, Floor(Power(10, MATCH(answers.body) AGAINST ("TESTING" IN BOOLEAN MODE))) AS count
FROM answers left join post_answers on answers.aid
WHERE MATCH(answers.body) AGAINST ("TESTING")
and answers.aid = post_answers.aid
group by answers.aid
;

/*
SELECT qid, title, body, Floor(Power(10, MATCH(body) AGAINST ("TESTING" IN BOOLEAN MODE))) AS Score
FROM questions
WHERE MATCH(body) AGAINST ('TESTING');

SELECT qid, title, body, Floor(Power(10, MATCH(title) AGAINST ("Difference" IN BOOLEAN MODE))) AS Score
FROM questions
WHERE MATCH(title) AGAINST ('Difference');
*/

with count_answers as (SELECT questions.qid, sum(Floor(Power(3, MATCH(answers.body) AGAINST ('difference' IN BOOLEAN MODE)))-1) AS count
FROM answers, questions, post_answers
WHERE MATCH(answers.body) AGAINST ('difference')
and answers.aid = post_answers.aid
and questions.qid = post_answers.qid
group by post_answers.qid
),
count_title as (SELECT qid, title, body, Floor(Power(10, MATCH(body) AGAINST ('difference' IN BOOLEAN MODE))) AS count
FROM questions
WHERE MATCH(title) AGAINST ('difference')),
count_body as (SELECT qid, title, body, Floor(Power(10, MATCH(body) AGAINST ('difference' IN BOOLEAN MODE))) AS count
FROM questions
WHERE MATCH(questions.body) AGAINST ('difference'))
Select questions.qid, questions.title, questions.body, coalesce((select count_answers.count where questions.qid = count_answers.qid), 0) + count_title.count + count_body.count  as occurences
FROM questions left join count_answers on questions.qid, count_title, count_body, topic, subtopic
WHERE count_title.qid = questions.qid
and count_body.qid = questions.qid
#and count_answers.qid = questions.qid
AND questions.stid = subtopics.stid
And subtopics.tid = topics.tid
AND tname = "Computer Science"
GROUP BY questions.qid, count_answers.qid
ORDER BY occurences desc;