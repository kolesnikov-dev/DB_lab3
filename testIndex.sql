\timing on

DROP TABLE IF EXISTS "test_btree";
CREATE TABLE "test_btree"(
	"id" bigserial PRIMARY KEY,
	"test_text" varchar(255)
);

INSERT INTO "test_btree"("test_text")
SELECT
	substr(characters, (random() * length(characters) + 1)::integer, 10)
FROM
	(VALUES('qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM')) as symbols(characters), generate_series(1, 1000000) as q;

SELECT COUNT(*) FROM "test_btree" WHERE "id" % 2 = 0;
SELECT COUNT(*) FROM "test_btree" WHERE "id" % 2 = 0 OR "test_text" LIKE 'b%';
SELECT COUNT(*), SUM("id") FROM "test_btree" WHERE "test_text" LIKE 'b%' GROUP BY "id" % 2;

DROP INDEX IF EXISTS "test_btree_test_text_index";
CREATE INDEX "test_btree_test_text_index" ON "test_btree" USING btree ("test_text");

SELECT COUNT(*) FROM "test_btree" WHERE "id" % 2 = 0;
SELECT COUNT(*) FROM "test_btree" WHERE "id" % 2 = 0 OR "test_text" LIKE 'b%';
SELECT COUNT(*), SUM("id") FROM "test_btree" WHERE "test_text" LIKE 'b%' GROUP BY "id" % 2;

--------------------------------------------------------------------------------------------------------------------------------

DROP TABLE IF EXISTS "test_gin";
CREATE TABLE "test_gin"(
	"id" bigserial PRIMARY KEY,
	"test_time" timestamp
);

INSERT INTO "test_gin"("test_time")
SELECT
	(timestamp '2021-01-01' + random() * (timestamp '2020-01-01' - timestamp '2022-01-01'))
FROM
	(VALUES('qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM')) as symbols(characters), generate_series(1, 1000000) as q;


SELECT COUNT(*) FROM "test_gin" WHERE "id" % 2 = 0;
SELECT COUNT(*) FROM "test_gin" WHERE "test_time" >= '20200505' AND "test_time" <= '20210505';
SELECT COUNT(*), SUM("id") FROM "test_gin" WHERE "test_time" >= '20200505' AND "test_time" <= '20210505' GROUP BY "id" % 2;

DROP INDEX IF EXISTS "test_gin_test_time_index";
CREATE INDEX "test_gin_test_time_index" ON "test_gin" USING gin ("test_time");

SELECT COUNT(*) FROM "test_gin" WHERE "id" % 2 = 0;
SELECT COUNT(*) FROM "test_gin" WHERE "test_time" >= '20200505' AND "test_time" <= '20210505';
SELECT COUNT(*), SUM("id") FROM "test_gin" WHERE "test_time" >= '20200505' AND "test_time" <= '20210505' GROUP BY "id" % 2;